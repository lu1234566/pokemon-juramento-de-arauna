#!/usr/bin/env python3
"""Build native 4bpp space-center interiors while preserving event geometry."""
from __future__ import annotations
import hashlib,json,re,shutil,struct,sys
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent))
import build_casa_fogueira_interiors_v2 as common

ATLAS=ROOT/'art/arauna_missoes_ceu_space_center_v1/source_atlas.png'
BANK=Path('data/tilesets/secondary/arauna_missoes_ceu_space_center_v1')
SYMBOL='AraunaMissoesCeuSpaceCenterV1'
MARK='MISSOES_CEU_SPACE_CENTER_V1'
OUT=ROOT/'review/missoes_ceu_space_center_v1'
NAMES=['MossdeepCity_SpaceCenter_1F','MossdeepCity_SpaceCenter_2F']
SPECS=[('floor',(32,32),6),('wall',(48,48),6),('window',(48,48),7),('door',(32,32),7),
       ('console',(32,32),8),('telemetry',(32,32),8),('table',(32,16),8),('lamp',(16,32),9),
       ('rocket',(32,48),10),('rail',(48,16),9),('cargo',(32,32),9),('antenna',(32,32),10),
       ('stair',(32,32),7),('observation',(48,32),7),('plant',(16,32),10),('locker',(32,32),8)]

def artwork():
 src=Image.open(ATLAS).convert('RGB');assert src.width>=1000 and src.height>=1000
 raw={};native=ATLAS.parent/'native_assets';native.mkdir(parents=True,exist_ok=True)
 for i,(name,size,slot) in enumerate(SPECS):
  row,col=divmod(i,4);unit=src.width/4;vunit=src.height/4
  x0=round(col*unit+unit*.12);x1=round((col+1)*unit-unit*.12)
  y0=round(row*vunit+vunit*.12);y1=round((row+1)*vunit-vunit*.12)
  image=src.crop((x0,y0,x1,y1)).convert('RGBA')
  if name=='floor':
   # The atlas shows nine sample pavers separated by a dark display gutter.
   # One complete paver supplies the repeating native floor instead.
   image=src.crop((76,82,131,137)).convert('RGBA')
   # Compress the bright reference sample to the concept's steel-blue room
   # palette before 4bpp quantization; keep it lighter than the wall.
   image.putdata([(int(r*.72),int(g*.80),int(b*.88),a) for r,g,b,a in image.getdata()])
  if name not in ('floor','wall','window','observation'):
   image.putdata([(r,g,b,0 if r<42 and g<68 and b<93 else 255) for r,g,b,_ in image.getdata()])
   image=image.crop(image.getbbox())
  raw[name]=(image.resize(size,Image.Resampling.NEAREST),slot)
 palettes={}
 for slot in range(6,11):
  colors=[(r,g,b) for image,p in raw.values() if p==slot for r,g,b,a in image.getdata() if a]
  sample=Image.new('RGB',(len(colors),1));sample.putdata(colors)
  color_list=sample.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette()[:45]
  palettes[slot]=[(255,0,255)]+[tuple(round(c*31/255)*255//31 for c in color_list[j:j+3]) for j in range(0,45,3)]
 result={}
 for name,(image,slot) in raw.items():
  palette=palettes[slot]
  indices=[0 if not a else min(range(1,16),key=lambda j:sum((p-q)**2 for p,q in zip((r,g,b),palette[j])))
           for r,g,b,a in image.getdata()]
  indexed=Image.new('L',image.size);indexed.putdata(indices);result[name]=(indexed,slot)
  preview=Image.new('RGBA',image.size);preview.putdata([(*palette[v],255 if v else 0) for v in indices]);preview.save(native/(name+'.png'))
 return result,palettes

def words(data):return list(struct.unpack('<%dH'%(len(data)//2),data))
def packed(data):return struct.pack('<%dH'%len(data),*data)
def write_json(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def main():
 common.artwork=artwork;common.BANK=ROOT/BANK;common.SYMBOL=SYMBOL
 common.Tiles.FIXED.update((0x206,0x207,0x2bc,0x2cc))
 t=common.Tiles();floor,fs=t.art['floor'];floorq=t.quarters(floor.crop((0,0,16,16)),fs)
 plain=t.meta(floorq,label='gridded concrete')
 alternate=t.meta(t.quarters(floor.crop((16,16,32,32)),fs),label='concrete seam')
 wall=t.stamp('wall',floorq);window=t.stamp('window',floorq)
 consoles=t.stamp('console',floorq);telemetry=t.stamp('telemetry',floorq)
 table=t.stamp('table',floorq);rail=t.stamp('rail',floorq)
 observation=t.stamp('observation',floorq)
 # The original Facility stairs and exit carry warp metatile behavior.
 attrs=words((ROOT/'data/tilesets/secondary/facility/metatile_attributes.bin').read_bytes())
 door,ds=t.art['door'];stair,ss=t.art['stair']
 for mid,art,x in ((0x206,door,0),(0x207,door,16),(0x2bc,stair,0),(0x2cc,stair,16)):
  slot=ds if mid<0x2bc else ss
  t.fixed(mid,floorq,t.quarters(art.crop((x,0,x+16,16)),slot),attrs[mid-512],'preserved warp')
 layouts_file=ROOT/'data/layouts/layouts.json';layouts=json.loads(layouts_file.read_text())
 report={'maps':{},'atlas':str(ATLAS.relative_to(ROOT)),'source_concept':'10_Centro_Espacial_Missoes_do_Ceu.png'}
 for name in NAMES:
  first=name.endswith('1F')
  original=next(x for x in layouts['layouts'] if x['id']=='LAYOUT_MOSSDEEP_CITY_SPACE_CENTER_'+('1F' if first else '2F'))
  source=ROOT/'data/layouts'/name/'map.bin';old=words(source.read_bytes());assert len(old)==160
  grid=[]
  for y in range(10):
   for x in range(16):
    raw=old[y*16+x]
    if y<2:mid=wall[y%2][x%3]
    elif not first and y==4 and 1<=x<=12:mid=rail[0][(x-1)%3]
    else:mid=plain if (x+2*y)%5 else alternate
    grid.append((raw&~0x3ff)|mid)
  def overlay(shape,x,y,valid=None):
   for dy,row in enumerate(shape):
    for dx,mid in enumerate(row):
     px,py=x+dx,y+dy
     if valid is None or valid(px,py):
      before=grid[py*16+px];grid[py*16+px]=(before&~0x3ff)|mid
  # Continuous observation strip, interrupted only by the return staircase.
  for x in (3,6,9):overlay(window,x,0,lambda px,py:py<2)
  if first:
   for x,y in ((2,5),(4,5),(10,7),(12,7)):overlay(consoles,x,y)
   for x,y in ((10,5),(13,5)):overlay(table,x,y,lambda px,py:py==5)
   # Launch telemetry behind the public hall's visitor counter.
   overlay(telemetry,7,0,lambda px,py:py<2)
  else:
   for x in (2,5,8,11):overlay(consoles,x,6)
   overlay(observation,5,0,lambda px,py:py<2)
   # The blocked railing still spans the original scripted battle stage.
   for x in (1,4,7,10):overlay(rail,x,4,lambda px,py:py==4)
  for x,y,mid in ((7,9,0x206),(8,9,0x207)) if first else ():
   grid[y*16+x]=(grid[y*16+x]&~0x3ff)|mid
  grid[1*16+13]=(grid[1*16+13]&~0x3ff)|(0x2bc if first else 0x2cc)
  # Preserve the exact collision and elevation bits for fixed choreography.
  assert all((a&~0x3ff)==(b&~0x3ff) for a,b in zip(old,grid))
  dest=ROOT/'data/layouts'/(name+'_Arauna');dest.mkdir(parents=True,exist_ok=True)
  (dest/'map.bin').write_bytes(packed(grid))
  (dest/'border.bin').write_bytes((ROOT/'data/layouts'/name/'border.bin').read_bytes())
  original.update(secondary_tileset='gTileset_'+SYMBOL,blockdata_filepath=str((dest/'map.bin').relative_to(ROOT)),
                  border_filepath=str((dest/'border.bin').relative_to(ROOT)))
  report['maps'][name]={'size':[16,10],'original_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                       'sha256':hashlib.sha256(packed(grid)).hexdigest(),'changed_cells':sum(a!=b for a,b in zip(old,grid)),
                       'collision_elevation_unchanged':True}
 write_json(layouts_file,layouts)
 report['metatiles']=t.save();report['new_tiles']=t.used;report['used_metatiles']=len(t.ids)
 for file,body in {
  'graphics.h':f'const u32 gTilesetTiles_{SYMBOL}[] = INCGFX_U32("{BANK}/tiles.png", ".4bpp.lz");\n'+f'const u16 gTilesetPalettes_{SYMBOL}[][16] =\n{{\n'+''.join(f'    INCGFX_U16("{BANK}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n',
  'metatiles.h':f'const u16 gMetatiles_{SYMBOL}[] = INCBIN_U16("{BANK}/metatiles.bin");\n'+f'const u16 gMetatileAttributes_{SYMBOL}[] = INCBIN_U16("{BANK}/metatile_attributes.bin");\n',
  'headers.h':f'const struct Tileset gTileset_{SYMBOL} =\n{{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n    .tiles = gTilesetTiles_{SYMBOL},\n    .palettes = gTilesetPalettes_{SYMBOL},\n    .metatiles = gMetatiles_{SYMBOL},\n    .metatileAttributes = gMetatileAttributes_{SYMBOL},\n    .callback = NULL,\n}};\n',
 }.items():
  p=ROOT/'src/data/tilesets'/file
  clean=re.sub(r'\n*// '+MARK+r'_BEGIN\n.*?// '+MARK+r'_END\n','',p.read_text(),flags=re.S)
  p.write_text(clean.rstrip()+'\n\n// '+MARK+'_BEGIN\n'+body+'// '+MARK+'_END\n')
 write_json(OUT/'geometry.json',report)
 print(json.dumps({'maps':len(NAMES),'new_tiles':t.used,'metatiles':report['metatiles']}))
if __name__=='__main__':main()
