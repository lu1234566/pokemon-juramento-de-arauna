#!/usr/bin/env python3
"""Check actual linked bytes against the native PNG/palette sources."""
import argparse,json,struct,subprocess,hashlib
from pathlib import Path
from PIL import Image
from check_interiors_native_encoding_v1 import pack_tiles,unpack_tiles,unlz10
from render_native_map import palette
ROOT=Path(__file__).resolve().parents[2]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--elf',type=Path,required=True);ap.add_argument('--nm',default='arm-none-eabi-nm');a=ap.parse_args()
 rom=a.rom.read_bytes();output=subprocess.check_output([a.nm,'-an',str(a.elf)],text=True)
 symbols={n:int(addr,16)-0x08000000 for addr,k,n in (l.split() for l in output.splitlines() if len(l.split())==3)};report={}
 for kind,slug,symbol in [('primary','arauna_inicio_base_v1','AraunaInicioBaseV1'),('secondary','arauna_inicio_sul_v1','AraunaInicioSulV1')]:
  p=ROOT/f'data/tilesets/{kind}/{slug}';im=Image.open(p/'tiles.png');raw=pack_tiles(im)
  assert unpack_tiles(raw,im.size)==im.tobytes();assert unlz10(rom[symbols['gTilesetTiles_'+symbol]:])==raw
  off=symbols['gTilesetPalettes_'+symbol]
  for i in range(16):
   expected=struct.pack('<16H',*[r>>3|(g>>3)<<5|(b>>3)<<10 for r,g,b in palette(p/f'palettes/{i:02}.pal')]);assert rom[off+i*32:off+(i+1)*32]==expected
  report[slug]={'4bpp_bytes':len(raw),'independent_roundtrip':True,'linked_rom_tiles_identical':True,'linked_rgb555_palettes_checked':16}
 report['rom_sha256']=hashlib.sha256(rom).hexdigest();(ROOT/'review/inicio_geometria_v1/encoding.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
