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
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--elf',type=Path,required=True);ap.add_argument('--output',type=Path,default=ROOT/'review/grutas_bordas_v2/rom_validation.json');a=ap.parse_args();raw=a.rom.read_bytes();nm={}
 for line in subprocess.check_output(['arm-none-eabi-nm','-n',str(a.elf)],text=True).splitlines():
  p=line.split()
  if len(p)==3:nm[p[2]]=int(p[0],16)
 assert not any('Harness' in n or 'TestStub' in n for n in nm)
 gr=json.loads((ROOT/'review/grutas_bordas_v2/grutas_build.json').read_text());br=json.loads((ROOT/'review/grutas_bordas_v2/borders_build.json').read_text());symbols=[s for d in br['maps'].values() for s in d['symbols']]+[n[9:] for n in gr['banks']]
 for s in symbols:
  p=resolve_bank(ROOT,'gTileset_'+s);assert lz(raw,nm['gTilesetTiles_'+s]-0x08000000)==pack_tiles(Image.open(p/'tiles.png')),(s,'4bpp')
  for prefix,field in [('gMetatiles_','metatiles.bin'),('gMetatileAttributes_','metatile_attributes.bin')]:
   data=(p/field).read_bytes();off=nm[prefix+s]-0x08000000;assert raw[off:off+len(data)]==data,(s,field)
  ps=nm['gTilesetPalettes_'+s]-0x08000000
  for q in range(13):
   pal=palette(p/f'palettes/{q:02}.pal');data=struct.pack('<16H',*[r>>3|(g>>3)<<5|(b>>3)<<10 for r,g,b in pal]);assert raw[ps+q*32:ps+(q+1)*32]==data,(s,'palette',q)
 for n in gr['maps']:
  data=(ROOT/'review/grutas_bordas_v2/visual_grids'/f'{n}.bin').read_bytes();off=nm['sVisual_'+n]-0x08000000;assert raw[off:off+len(data)]==data,(n,'visual grid')
 for r in br['regions']:
  data=struct.pack('<%dH'%(len(r['aliases'])*2),*[v for k,a in r['aliases'].items() for v in (int(k),a)]);off=nm[r['array']]-0x08000000;assert raw[off:off+len(data)]==data,(r['array'],'alias table')
 # All native V1 water/waterfall frames still match the disk assets.
 for family in ('victory','seafloor'):
  for kind in ('water','waterfall'):
   for i in range(8):
    n='gAraunaGrutas'+family.title()+kind.title()+'Frame'+str(i)
    # Read the actual symbol spelling from the compiled callback declaration.
    candidates=[k for k in nm if k.lower().endswith(f'{family}_{kind}_{i}'.lower()) or k==n]
    if not candidates:
     import re
     source=(ROOT/'src/tileset_anims.c').read_text();match=re.search(r'const u16 (\w+)\[\] = INCGFX_U16\("graphics/tilesets/arauna_grutas_v1/'+family+'/'+kind+'/'+str(i)+r'\.png"',source);assert match;n=match[1]
    else:n=candidates[0]
    data=pack_tiles(Image.open(ROOT/f'graphics/tilesets/arauna_grutas_v1/{family}/{kind}/{i}.png'));off=nm[n]-0x08000000;assert raw[off:off+len(data)]==data,(n,'animation frame')
 dump(a.output,{'status':'PASS','rom_sha256':hashlib.sha256(raw).hexdigest(),'rom_file_bytes':len(raw),'native_banks':len(symbols),'cave_grid_tables':len(gr['maps']),'border_alias_tables':len(br['regions']),'native_animation_frames':32,'capture_harness_symbols':0});print('PASS compiled ROM assets:',len(symbols),'banks, 14 visual grids, 10 alias tables, 32 animation frames')
if __name__=='__main__':main()
