#!/usr/bin/env python3
"""Compare compiled ROM native graphics, palettes, attrs, aliases and layouts."""
import argparse,hashlib,json,struct,subprocess
from pathlib import Path
from PIL import Image
from native_visuals_v2 import ROOT,dump
from check_interiors_native_encoding_v1 import pack_tiles
from render_native_map import palette
from bancos_nativos import resolve_bank

def lz(raw,offset):
 assert raw[offset]==16;size=int.from_bytes(raw[offset+1:offset+4],'little');i=offset+4;out=bytearray()
 while len(out)<size:
  flags=raw[i];i+=1
  for bit in range(7,-1,-1):
   if len(out)>=size:break
   if flags&(1<<bit):
    a,b=raw[i:i+2];i+=2;length=(a>>4)+3;distance=((a&15)<<8|b)+1
    for _ in range(length):out.append(out[-distance])
   else:out.append(raw[i]);i+=1
 return bytes(out)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--elf',type=Path,required=True);ap.add_argument('--output',type=Path,default=ROOT/'review/sul_pampa_v1/rom_validation.json');a=ap.parse_args();raw=a.rom.read_bytes();nm={}
 for line in subprocess.check_output(['arm-none-eabi-nm','-n',str(a.elf)],text=True).splitlines():
  p=line.split()
  if len(p)==3:nm[p[2]]=int(p[0],16)
 assert not any('Harness' in n or 'TestStub' in n for n in nm)
 br=json.loads((ROOT/'review/sul_pampa_v1/borders_build.json').read_text());symbols=[s for d in br['maps'].values() for s in d['symbols']]
 for s in symbols:
  p=resolve_bank(ROOT,'gTileset_'+s);assert lz(raw,nm['gTilesetTiles_'+s]-0x08000000)==pack_tiles(Image.open(p/'tiles.png')),(s,'4bpp')
  for prefix,field in [('gMetatiles_','metatiles.bin'),('gMetatileAttributes_','metatile_attributes.bin')]:
   data=(p/field).read_bytes();off=nm[prefix+s]-0x08000000;assert raw[off:off+len(data)]==data,(s,field)
  ps=nm['gTilesetPalettes_'+s]-0x08000000
  for q in range(13):
   pal=palette(p/f'palettes/{q:02}.pal');data=struct.pack('<16H',*[r>>3|(g>>3)<<5|(b>>3)<<10 for r,g,b in pal]);assert raw[ps+q*32:ps+(q+1)*32]==data,(s,'palette',q)
 for r in br['regions']:
  data=struct.pack('<%dH'%(len(r['aliases'])*2),*[v for k,a in r['aliases'].items() for v in (int(k),a)]);off=nm[r['array']]-0x08000000;assert raw[off:off+len(data)]==data,(r['array'],'alias table')
 dump(a.output,{'status':'PASS','rom_sha256':hashlib.sha256(raw).hexdigest(),'file_bytes':len(raw),'native_banks':len(symbols),'alias_tables':len(br['regions']),'loaded_palette_rows':13,'harness_symbols':0});print('PASS compiled ROM assets:',len(symbols),'banks,',len(br['regions']),'alias tables')
if __name__=='__main__':main()
