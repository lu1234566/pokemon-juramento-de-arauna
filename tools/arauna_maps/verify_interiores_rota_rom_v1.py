#!/usr/bin/env python3
"""Compare all new native sources with their actual linked ROM bytes."""
import argparse, hashlib, json, struct, subprocess
from pathlib import Path
from PIL import Image
from check_interiors_native_encoding_v1 import pack_tiles, unpack_tiles, unlz10
from render_native_map import palette
ROOT = Path(__file__).resolve().parents[2]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rom', type=Path, required=True)
    ap.add_argument('--elf', type=Path, required=True)
    ap.add_argument('--nm', default='arm-none-eabi-nm')
    ap.add_argument('--output', type=Path, default=ROOT/'review/interiores_rota_v1/encoding.json')
    a = ap.parse_args()
    rom = a.rom.read_bytes()
    lines = subprocess.check_output([a.nm, '-an', str(a.elf)], text=True).splitlines()
    symbols = {n:int(addr,16)-0x08000000 for addr,k,n in
               (line.split() for line in lines if len(line.split()) == 3)}
    build = json.loads((ROOT/'review/interiores_rota_v1/build.json').read_text())
    paths = [ROOT/'data/tilesets/primary/arauna_rota_base_v1'] + [
        ROOT/f'data/tilesets/secondary/arauna_rota_{key}_v1' for key in build['banks']]
    report = {'status':'PASS', 'banks':{}}
    for p in paths:
        slug = p.name
        symbol = ''.join(part.capitalize() for part in slug.split('_'))
        im = Image.open(p/'tiles.png'); raw = pack_tiles(im)
        assert unpack_tiles(raw, im.size) == im.tobytes()
        assert unlz10(rom[symbols['gTilesetTiles_'+symbol]:]) == raw, slug
        off = symbols['gTilesetPalettes_'+symbol]
        for i in range(16):
            expected = struct.pack('<16H', *[r>>3|(g>>3)<<5|(b>>3)<<10
                for r,g,b in palette(p/f'palettes/{i:02}.pal')])
            assert rom[off+i*32:off+(i+1)*32] == expected, (slug,i)
        for name,prefix in [('metatiles.bin','gMetatiles_'),
                            ('metatile_attributes.bin','gMetatileAttributes_')]:
            data = (p/name).read_bytes(); off = symbols[prefix+symbol]
            assert rom[off:off+len(data)] == data, (slug,name)
        report['banks'][slug] = {'4bpp_bytes':len(raw),
            'tiles_palettes_metatiles_attributes_identical_to_linked_ROM':True}
    report['rom_sha256'] = hashlib.sha256(rom).hexdigest()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: all 15 banks identical to linked ROM; '+report['rom_sha256'])

if __name__ == '__main__': main()
