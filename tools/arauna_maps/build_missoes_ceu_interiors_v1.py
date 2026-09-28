#!/usr/bin/env python3
"""Build seven native domestic/service interiors from the coastal science atlas."""
from __future__ import annotations
import json,re,struct,sys
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent))
import build_casa_fogueira_interiors_v2 as common

ATLAS=ROOT/'art/arauna_missoes_ceu_interiors_v1/source_atlas.png'
BANK=Path('data/tilesets/secondary/arauna_missoes_ceu_interiors_v1')
SYMBOL='AraunaMissoesCeuInteriorsV1'
MARK='MISSOES_CEU_INTERIORS_V1'
OUT=ROOT/'review/missoes_ceu_interiors_v1'
NAMES=[f'MossdeepCity_House{i}' for i in range(1,5)]+['MossdeepCity_Mart','MossdeepCity_PokemonCenter_1F','MossdeepCity_PokemonCenter_2F']
ART=[('floor',(32,32),6,(0,0)),('wall',(48,48),6,(0,3)),('window',(48,48),7,(0,1)),('door',(48,48),7,(0,2)),
     ('rug',(48,32),8,(1,0)),('table',(48,48),8,(1,1)),('bed',(32,32),8,(2,1)),('shelf',(32,32),8,(2,0)),
     ('lantern',(16,32),9,(1,3)),('chart',(32,32),9,(2,2)),('hearth',(48,48),9,(1,2)),('plant',(32,32),10,(2,3)),
     ('healer',(64,48),11,(3,0)),('pc',(32,32),11,(3,1)),('link',(48,32),11,(3,2)),('stair',(32,32),7,(3,3))]

def artwork():
 src=Image.open(ATLAS).convert('RGB');assert src.width>=1000 and src.height>=1000
 raw={};native=ATLAS.parent/'native_assets';native.mkdir(parents=True,exist_ok=True)
 for name,size,slot,(row,col) in ART:
  uw=src.width/4;uh=src.height/4
  x0=round(col*uw+uw*.11);x1=round((col+1)*uw-uw*.11)
  y0=round(row*uh+uh*.11);y1=round((row+1)*uh-uh*.11)
  if name=='floor':x0,y0,x1,y1=75,75,132,132
  if name=='wall':x0,y0,x1,y1=1033,86,1051,278
  im=src.crop((x0,y0,x1,y1)).convert('RGBA')
  if name not in ('floor','wall','window','door'):
   im.putdata([(r,g,b,0 if min(r,g,b)>232 else 255) for r,g,b,a in im.getdata()])
   im=im.crop(im.getbbox())
  raw[name]=(im.resize(size,Image.Resampling.NEAREST),slot)
 palettes={}
 for slot in range(6,12):
  colors=[(r,g,b) for im,p in raw.values() if p==slot for r,g,b,a in im.getdata() if a]
  if not colors:continue
  sample=Image.new('RGB',(len(colors),1));sample.putdata(colors)
  values=sample.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette()[:45]
  palettes[slot]=[(255,0,255)]+[tuple(round(v*31/255)*255//31 for v in values[j:j+3]) for j in range(0,45,3)]
 output={}
 for name,(im,slot) in raw.items():
  palette=palettes[slot]
  ids=[0 if not a else min(range(1,16),key=lambda j:sum((u-v)**2 for u,v in zip((r,g,b),palette[j]))) for r,g,b,a in im.getdata()]
  indexed=Image.new('L',im.size);indexed.putdata(ids);output[name]=(indexed,slot)
  preview=Image.new('RGBA',im.size);preview.putdata([(*palette[v],255 if v else 0) for v in ids]);preview.save(native/(name+'.png'))
 return output,palettes

def words(raw):return struct.unpack('<%dH'%(len(raw)//2),raw)
def packed(data):return struct.pack('<%dH'%len(data),*data)
def write_json(p,node):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(node,indent=2,ensure_ascii=False)+'\n')

def mail_house(t):
 # Preserve every collision/elevation cell and event coordinate in the mail
 # house: the Wingull's two exit animations use fixed steps from (4,5).
 src=ROOT/'data/layouts/House1/map.bin';old=words(src.read_bytes());assert len(old)==90
 floor,slot=t.art['floor'];f=t.quarters(floor.crop((0,0,16,16)),slot)
 plain=t.meta(f,label='coastal stone');wall=t.stamp('wall',f);window=t.stamp('window',f)
 table=t.stamp('table',f);chart=t.stamp('chart',f);rug=t.stamp('rug',f,blocking=False)
 grid=[]
 for y in range(9):
  for x in range(10):
   raw=old[y*10+x]
   mid=wall[y%2][x%3] if y<2 else plain
   grid.append((raw&~0x3ff)|mid)
 def overlay(shape,x,y):
  for dy,row in enumerate(shape):
   for dx,mid in enumerate(row):
    old_raw=grid[(y+dy)*10+x+dx];grid[(y+dy)*10+x+dx]=(old_raw&~0x3ff)|mid
 overlay(window,5,0)
 # Only the original blocked 2x2 table cells receive the desk art.
 for dy in range(2):
  for dx in range(2):
   before=grid[(4+dy)*10+2+dx];grid[(4+dy)*10+2+dx]=(before&~0x3ff)|table[dy][dx]
 # A wall chart is read from the dry side of the room.
 before=grid[1*10+8];grid[1*10+8]=(before&~0x3ff)|chart[0][0]
 overlay(rug,6,6)
 threshold=t.meta(f,attr=0x1065,label='coastal threshold')
 for x in (3,4):grid[8*10+x]=(grid[8*10+x]&~0x3ff)|threshold
 assert all((a&~0x3ff)==(b&~0x3ff) for a,b in zip(old,grid))
 return grid,{'collision_elevation_unchanged':True,'wingull_path_fixed':True}

def main():
 common.artwork=artwork;common.BANK=ROOT/BANK;common.SYMBOL=SYMBOL
 t=common.Tiles();layouts_file=ROOT/'data/layouts/layouts.json';layout_data=json.loads(layouts_file.read_text())
 report={'maps':{},'atlas':str(ATLAS.relative_to(ROOT))}
 for name in NAMES:
  p=ROOT/'data/maps'/name/'map.json';data=json.loads(p.read_text());current=data['layout']
  source_id={'MossdeepCity_House1':'LAYOUT_HOUSE2','MossdeepCity_House2':'LAYOUT_HOUSE1',
             'MossdeepCity_House3':'LAYOUT_HOUSE2','MossdeepCity_House4':'LAYOUT_HOUSE_WITH_BED',
             'MossdeepCity_Mart':'LAYOUT_MART','MossdeepCity_PokemonCenter_1F':'LAYOUT_POKEMON_CENTER_1F',
             'MossdeepCity_PokemonCenter_2F':'LAYOUT_POKEMON_CENTER_2F'}[name]
  template=next(r for r in layout_data['layouts'] if r['id']==source_id)
  if name.endswith('House2'):
   grid,extra=mail_house(t);w,h=10,9;kind='mail';variant=2
  elif name.endswith('1F') or name.endswith('2F'):
   kind='center1' if name.endswith('1F') else 'center2';variant=0;w,h=(14,9) if kind=='center1' else (14,10)
   grid,_,modules,_=common.build_room(t,w,h,kind)
   if kind=='center1':data['object_events'][0].update(x=7,y=3,elevation=3)
   extra={'modules':modules}
  else:
   kind='house';variant={'MossdeepCity_House1':1,'MossdeepCity_House3':3,'MossdeepCity_House4':4,'MossdeepCity_Mart':2}[name]
   w,h=12,11;grid,_,modules,_=common.build_room(t,w,h,kind,variant)
   for warp,(x,y) in zip(data['warp_events'],((5,10),(6,10))):warp.update(x=x,y=y,elevation=0)
   coords={
    'MossdeepCity_House1':((4,7),(8,6)),
    'MossdeepCity_House3':((5,7),),
    'MossdeepCity_House4':((4,7),(8,6),(5,8)),
    'MossdeepCity_Mart':((4,6),(6,7),(9,7),(8,5)),
   }[name]
   for event,(x,y) in zip(data['object_events'],coords):event.update(x=x,y=y,elevation=3)
   extra={'modules':modules}
  new_id='LAYOUT_ARAUNA_MISSOES_CEU_INTERIORS_'+name.removeprefix('MossdeepCity_').upper()
  assert current in (source_id,new_id),(name,current)
  record=dict(template);record.update(id=new_id,name=name+'_Arauna_Layout',width=w,height=h,
   secondary_tileset='gTileset_'+SYMBOL,border_filepath=f'data/layouts/{name}_Arauna/border.bin',
   blockdata_filepath=f'data/layouts/{name}_Arauna/map.bin')
  existing=next((r for r in layout_data['layouts'] if r['id']==new_id),None)
  if existing:existing.update(record)
  else:layout_data['layouts'].append(record)
  data['layout']=new_id;write_json(p,data)
  dst=ROOT/'data/layouts'/(name+'_Arauna');dst.mkdir(parents=True,exist_ok=True)
  (dst/'map.bin').write_bytes(packed(grid));(dst/'border.bin').write_bytes((ROOT/template['border_filepath']).read_bytes())
  report['maps'][name]={'layout':new_id,'size':[w,h],
   'warps':[(e['x'],e['y'],e['dest_map'],e['dest_warp_id']) for e in data['warp_events']],
   'npcs':[(e['x'],e['y'],e['script']) for e in data['object_events']],**extra}
 write_json(layouts_file,layout_data)
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
 print(json.dumps({'maps':len(NAMES),'tiles':t.used,'metatiles':report['metatiles']}))
if __name__=='__main__':main()
