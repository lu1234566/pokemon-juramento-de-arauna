#!/usr/bin/env python3
"""Verify the native English cinematic, every decoded frame and audio format."""
import hashlib
import json
import struct
import wave
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DIR=ROOT/'graphics/arauna_opening_native_en'

def lz_decode(data):
    assert data[0]==0x10
    size=int.from_bytes(data[1:4],'little')
    assert size<=39000
    result=bytearray();pos=4
    while len(result)<size:
        flag=data[pos];pos+=1
        for bit in range(7,-1,-1):
            if len(result)==size: break
            if flag&(1<<bit):
                first,second=data[pos:pos+2];pos+=2
                length=(first>>4)+3;distance=((first&15)<<8)+second+1
                assert distance<=len(result)
                for _ in range(length): result.append(result[-distance])
            else: result.append(data[pos]);pos+=1
            assert len(result)<=size
    return bytes(result)

def unpack_tiles(data):
    pixels=bytearray(240*160);pos=0
    for ty in range(20):
        for tx in range(30):
            count=data[pos];pos+=1
            assert 1<=count<=8
            if count==0:
                tile=data[pos:pos+64];pos+=64
            else:
                assert count<=8
                local=data[pos:pos+count];pos+=count
                width=(count-1).bit_length()
                payload=data[pos:pos+width*8];pos+=width*8
                bits=int.from_bytes(payload,'little')
                mask=(1<<width)-1
                values=[]
                for _ in range(64):
                    value=bits&mask;bits>>=width
                    assert value<count
                    values.append(local[value])
                tile=bytes(values)
            assert len(tile)==64
            for y in range(8):
                start=(ty*8+y)*240+tx*8
                pixels[start:start+8]=tile[y*8:y*8+8]
    assert pos==len(data),(pos,len(data))
    return bytes(pixels)

def verify():
    manifest=json.loads((DIR/'manifest.json').read_text())
    assert (manifest['language'],manifest['width'],manifest['height'],manifest['frame_count'],manifest['fps'])==('en',240,160,660,15)
    assert manifest['source_zip_sha256']=='f5259711dea2f14249d2a5a1ee95d6f0c58ff339bb443a3b8587b748c708ca83'
    chunks=[]
    for record in manifest['chunks']:
        data=(DIR/record['name']).read_bytes()
        assert len(data)==record['bytes'] and hashlib.sha256(data).hexdigest()==record['sha256']
        chunks.append(data)
    assert len(list(DIR.glob('chunk_*.bin')))==len(chunks)
    assert sum(map(len,chunks))==manifest['encoded_frame_bytes']<=10*1024*1024
    palette_bytes=manifest['palette_colors']*2
    maximum=0
    for i,record in enumerate(manifest['frames']):
        assert i==record['frame'] and record['offset']%4==0
        block=chunks[record['chunk']][record['offset']:record['offset']+record['bytes']]
        assert len(block)==record['bytes']
        palette=block[:palette_bytes]
        assert max(struct.unpack('<'+'H'*manifest['palette_colors'],palette))<32768
        raw=lz_decode(block[palette_bytes:]);maximum=max(maximum,len(raw))
        assert len(raw)<=19800
        pixels=unpack_tiles(raw)
        assert max(pixels)<manifest['palette_colors']
        assert hashlib.sha256(palette+pixels).hexdigest()==record['indexed_sha256'],i
    title=(DIR/'title.bin').read_bytes()
    assert len(lz_decode(title[palette_bytes:]))==38400
    audio=ROOT/'sound/direct_sound_samples/arauna_opening_en.wav'
    assert hashlib.sha256(audio.read_bytes()).hexdigest()==manifest['audio_sha256']
    with wave.open(str(audio)) as wav:
        assert (wav.getframerate(),wav.getsampwidth(),wav.getnchannels(),wav.getnframes())==(13379,1,1,manifest['audio_samples'])
    print(f'English opening: PASS (660 frames, native title, audio; {sum(map(len,chunks))} ROM bytes, {maximum} decode bytes)')

if __name__=='__main__': verify()
