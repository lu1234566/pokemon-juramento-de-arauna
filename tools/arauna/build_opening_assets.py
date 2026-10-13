#!/usr/bin/env python3
"""Convert the supplied English opening ZIP to GBA tile-palette/LZ77 assets."""
import argparse
import collections
import numpy as np
import ctypes
import hashlib
import io
import json
import struct
import subprocess
import tempfile
import wave
import zipfile
from pathlib import Path

from PIL import Image, __version__ as pillow_version

ROOT = Path(__file__).resolve().parents[2]
COLORS = 48
CHUNK_SIZE = 256 * 1024
SOURCE_SHA = 'f5259711dea2f14249d2a5a1ee95d6f0c58ff339bb443a3b8587b748c708ca83'
parser = argparse.ArgumentParser()
parser.add_argument('source_zip', type=Path)
parser.add_argument('--limit', type=int, default=660)
args = parser.parse_args()
assert hashlib.sha256(args.source_zip.read_bytes()).hexdigest() == SOURCE_SHA, 'Use the verified English gba_assets (1).zip'
directory = ROOT / 'graphics/arauna_opening_native_en'
directory.mkdir(parents=True, exist_ok=True)

with tempfile.TemporaryDirectory(prefix='arauna-opening-codec-') as temp:
    libpath = Path(temp) / 'lz.so'
    subprocess.run(['cc', '-shared', '-fPIC', '-O3', str(ROOT/'tools/arauna/opening_lz.c'), '-o', str(libpath)], check=True)
    lib = ctypes.CDLL(str(libpath))
    lib.AraunaOpeningCompress.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    def compress(data, min_distance=1):
        out = ctypes.create_string_buffer(len(data)*2+32)
        size = lib.AraunaOpeningCompress(data, len(data), out, min_distance)
        assert size>0
        return out.raw[:size]
    records=[]
    chunks=[bytearray()]
    title=None
    with zipfile.ZipFile(args.source_zip) as archive:
        for index in range(args.limit):
            raw_png=archive.read(f'gba_assets/frames/f{index+1:04d}.png')
            im=Image.open(io.BytesIO(raw_png))
            assert im.size==(240,160)
            q=im.quantize(colors=COLORS,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
            pixels=q.tobytes()
            rgb=q.getpalette()
            rgb += [0]*(COLORS*3-len(rgb))
            pal=struct.pack('<'+'H'*COLORS,*[(rgb[3*i]>>3)|((rgb[3*i+1]>>3)<<5)|((rgb[3*i+2]>>3)<<10) for i in range(COLORS)])
            color_values=np.array(rgb[:COLORS*3],dtype=np.int32).reshape(COLORS,3)
            distances=np.sum((color_values[:,None,:]-color_values[None,:,:])**2,axis=2)
            tiles=bytearray()
            native_pixels=bytearray(240*160)
            for ty in range(20):
                for tx in range(30):
                    tile=bytes(pixels[(ty*8+y)*240+tx*8+x] for y in range(8) for x in range(8))
                    local=list(dict.fromkeys(tile))
                    if len(local)>8:
                        frequencies=collections.Counter(tile)
                        weights=np.array([frequencies[v] for v in local])
                        costs=distances[np.ix_(local,local)]
                        chosen=[int(np.argmax(weights))]
                        closest=costs[:,chosen[0]].copy()
                        for _ in range(7):
                            next_color=int(np.argmax(closest*np.sqrt(weights)))
                            chosen.append(next_color)
                            closest=np.minimum(closest,costs[:,next_color])
                        selected=[local[i] for i in chosen]
                        nearest=np.argmin(distances[np.ix_(local,selected)],axis=1)
                        replace={v:selected[int(nearest[i])] for i,v in enumerate(local)}
                        tile=bytes(replace[v] for v in tile)
                        local=list(dict.fromkeys(tile))
                    for y in range(8):
                        start=(ty*8+y)*240+tx*8
                        native_pixels[start:start+8]=tile[y*8:y*8+8]
                    bits=(len(local)-1).bit_length()
                    if 1+len(local)+bits*8 >= 65:
                        tiles.append(0);tiles.extend(tile)
                    else:
                        tiles.append(len(local));tiles.extend(local)
                        mapping={value:i for i,value in enumerate(local)}
                        accumulator=available=0
                        for value in tile:
                            accumulator |= mapping[value]<<available
                            available += bits
                            while available>=8:
                                tiles.append(accumulator&255);accumulator >>= 8;available -= 8
                        assert available==0
            assert len(tiles)<=19800
            encoded=pal+compress(bytes(tiles))
            if len(chunks[-1])+len(encoded)>CHUNK_SIZE: chunks.append(bytearray())
            chunk=len(chunks)-1;offset=len(chunks[-1]);chunks[-1].extend(encoded)
            records.append({'frame':index,'chunk':chunk,'offset':offset,'bytes':len(encoded),
                            'indexed_sha256':hashlib.sha256(pal+native_pixels).hexdigest(),
                            'source_png_sha256':hashlib.sha256(raw_png).hexdigest()})
            if index==630:
                title=pal+compress(pixels,2)
            if (index+1)%60==0: print(f'encoded {index+1} frames: {sum(map(len,chunks))} bytes',flush=True)
        audio=archive.read('gba_assets/audio_13379hz_8bit_mono.wav')
        with wave.open(io.BytesIO(audio)) as wav:
            assert (wav.getframerate(),wav.getsampwidth(),wav.getnchannels())==(13379,1,1)
            samples=wav.getnframes()
    for stale in directory.glob("chunk_*.bin"): stale.unlink()
    for index,chunk in enumerate(chunks): (directory/f'chunk_{index:03d}.bin').write_bytes(chunk)
    header=['// Generated native English cinematic; see build_opening_assets.py.']
    for index in range(len(chunks)):
        header.append(f'static const u8 ALIGNED(4) sOpeningChunk{index:03d}[] = INCBIN_U8("graphics/arauna_opening_native_en/chunk_{index:03d}.bin");')
    header.extend(['', 'static const u8 *const sOpeningFrames[] =', '{'])
    for r in records: header.append(f'    sOpeningChunk{r["chunk"]:03d} + {r["offset"]},')
    header.append('};')
    header.extend([f'#define ARAUNA_OPENING_FRAMES {len(records)}',f'#define ARAUNA_OPENING_AUDIO_SAMPLES {samples}',f'#define ARAUNA_OPENING_PALETTE_BYTES {COLORS*2}'])
    if title is not None:
        (directory/'title.bin').write_bytes(title)
        header.append('static const u8 ALIGNED(4) sOpeningTitle[] = INCBIN_U8("graphics/arauna_opening_native_en/title.bin");')
    (ROOT/'src/data/arauna_opening_en.h').write_text('\n'.join(header)+'\n')
    (ROOT/'sound/direct_sound_samples/arauna_opening_en.wav').write_bytes(audio)
    manifest={'source_zip_sha256':SOURCE_SHA,'language':'en','width':240,'height':160,'fps':15,
              'frame_count':len(records),'palette_colors':COLORS,'tile_palette_limit':8,'codec':'RGB555 global palette + BIOS LZ77 tile-local palettes and variable-width pixel indices',
              'pillow_version':pillow_version,'audio_rate':13379,'audio_samples':samples,
              'audio_sha256':hashlib.sha256(audio).hexdigest(),'title_source_frame':631,
              'encoded_frame_bytes':sum(map(len,chunks)),'chunks':[{"name":f'chunk_{i:03d}.bin',"bytes":len(c),"sha256":hashlib.sha256(c).hexdigest()} for i,c in enumerate(chunks)],
              'frames':records}
    (directory/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Opening assets: {len(records)} frames, {len(chunks)} chunks, {sum(map(len,chunks))} frame bytes',flush=True)
