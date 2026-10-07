#!/usr/bin/env python3
"""Check native files against bytes in the final linked ROM (not distributed)."""
import argparse,hashlib,json,struct,subprocess
from pathlib import Path
from PIL import Image
from check_interiors_native_encoding_v1 import pack_tiles,unlz10
from render_native_map import palette
ROOT=Path(__file__).resolve().parents[2]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--elf',type=Path,required=True);ap.add_argument('--nm',default='arm-none-eabi-nm');a=ap.parse_args();rom=a.rom.read_bytes();s={p[2]:int(p[0],16)-0x08000000 for line in subprocess.check_output([a.nm,str(a.elf)],text=True).splitlines() if len(p:=line.split())==3};build=json.loads((ROOT/'review/campanha_grutas_v1/build.json').read_text());report={'status':'PASS','banks':{},'animation_frames_checked':32}
 for slug,b in build['banks'].items():
  p=ROOT/b['path'];sym=b['symbol'];raw=pack_tiles(Image.open(p/'tiles.png'));assert unlz10(rom[s['gTilesetTiles_'+sym]:])==raw
  off=s['gTilesetPalettes_'+sym]
  for i in range(13):expected=struct.pack('<16H',*[r>>3|(g>>3)<<5|(b>>3)<<10 for r,g,b in palette(p/f'palettes/{i:02}.pal')]);assert rom[off+i*32:off+(i+1)*32]==expected
  for filename,prefix in [('metatiles.bin','gMetatiles_'),('metatile_attributes.bin','gMetatileAttributes_')]:raw=(p/filename).read_bytes();off=s[prefix+sym];assert rom[off:off+len(raw)]==raw
  report['banks'][slug]={'native_sources_identical_to_linked_ROM':True}
 for family in ('victory','seafloor'):
  for kind in ('water','waterfall'):
   for i in range(8):raw=pack_tiles(Image.open(ROOT/f'graphics/tilesets/arauna_grutas_v1/{family}/{kind}/{i}.png'));off=s[f'sAraunaGrutas{family.title()}V1{kind}{i}'];assert rom[off:off+len(raw)]==raw
 report.update(rom_sha256=hashlib.sha256(rom).hexdigest(),rom_bytes=len(rom));(ROOT/'review/campanha_grutas_v1/rom_encoding.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
