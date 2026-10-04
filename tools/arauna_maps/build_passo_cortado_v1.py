#!/usr/bin/env python3
"""Adapt Jagged Pass to the Bible's natural volcanic descent."""
import json,shutil,struct,subprocess
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
MAPS=('JaggedPass',)
SPECS={
 'AraunaPassoPedra':('primary','general','arauna_passo_pedra','InitTilesetAnim_General'),
 'AraunaPassoCortado':('secondary','lavaridge','arauna_passo_cortado','NULL'),
}
BASE=953
def words(path):
 b=path.read_bytes();return list(struct.unpack('<%dH'%(len(b)//2),b))
def dump(path,node):path.write_text(json.dumps(node,indent=2,ensure_ascii=False)+'\n')
def source(symbol):kind,slug,_,_=SPECS[symbol];return ROOT/'data/tilesets'/kind/slug
def target(symbol):kind,_,slug,_=SPECS[symbol];return ROOT/'data/tilesets'/kind/slug
def layout_id(name):return 'LAYOUT_ARAUNA_PASSO_CORTADO_V1'
def clone(src,dst):
 dst.mkdir(parents=True,exist_ok=True)
 for n in ('tiles.png','metatiles.bin','metatile_attributes.bin'):shutil.copyfile(src/n,dst/n)
 (dst/'palettes').mkdir(exist_ok=True)
 for i in range(16):shutil.copyfile(src/'palettes'/f'{i:02}.pal',dst/'palettes'/f'{i:02}.pal')
def palette(path,changes):
 lines=path.read_text().splitlines();assert lines[:3]==['JASC-PAL','0100','16'] and len(lines)==19
 for i,rgb in changes.items():lines[i+3]=' '.join(map(str,rgb))
 path.write_text('\n'.join(lines)+'\n')
def insert(path,anchor,block,marker):
 s=path.read_text()
 if marker not in s:
  assert s.count(anchor)==1;path.write_text(s.replace(anchor,block+anchor))

def assets():
 for symbol in SPECS:clone(source(symbol),target(symbol))
 p=target('AraunaPassoPedra')
 palette(p/'palettes/03.pal',{
  1:(219,221,217),2:(184,189,187),3:(152,158,162),4:(120,128,137),
  5:(92,100,116),8:(43,42,61),9:(189,183,171),10:(158,149,139),
  11:(131,118,115),12:(103,90,96),13:(77,65,82),14:(52,45,64)})
 p=target('AraunaPassoCortado')
 palette(p/'palettes/10.pal',{
  1:(190,185,178),2:(163,156,151),3:(137,128,128),4:(109,99,107),
  5:(82,75,89),8:(38,35,49),9:(170,153,132),10:(143,122,107),
  11:(119,97,92),12:(94,74,78),13:(72,54,64),14:(49,40,53)})
 palette(p/'palettes/11.pal',{
  1:(223,217,202),2:(190,182,167),3:(157,147,138),4:(125,115,116),
  6:(92,87,99),8:(65,62,79),9:(207,197,164),10:(176,160,131),
  11:(144,127,111),12:(113,97,94),13:(87,73,80),14:(63,53,67),15:(69,67,61)})
 palette(p/'palettes/12.pal',{
  1:(54,50,64),2:(77,70,82),3:(112,104,111),4:(150,143,138),
  5:(185,181,166),6:(143,119,95),7:(97,82,86)})
 original=Image.open(p/'tiles.png');assert original.mode=='P' and original.size==(128,232)
 sheet=Image.new('P',(128,256),0);sheet.putpalette(original.getpalette());sheet.paste(original,(0,0))
 meta=words(p/'metatiles.bin');attrs=words(p/'metatile_attributes.bin');assert len(attrs)==441
 assert not {x&1023 for x in meta}.intersection(range(1016,1024))
 for variant in range(2):
  art=Image.new('P',(16,16),0);d=ImageDraw.Draw(art)
  if variant==0:
   d.line((1,11,4,9,7,10,10,7,14,8),fill=3,width=1)
   d.line((5,5,7,6,8,4),fill=2,width=1)
   for x,y in ((2,3),(12,12),(11,3),(4,13)):d.point((x,y),fill=5)
  else:
   for x,y in ((2,3),(9,5),(5,11),(12,12)):
    d.polygon([(x,y),(x+2,y-1),(x+3,y+1),(x+1,y+2)],fill=3,outline=2)
    d.point((x+1,y),fill=4)
  for i,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):
   idx=1016+variant*4+i;sheet.paste(art.crop((x,y,x+8,y+8)),((idx-512)%16*8,(idx-512)//16*8))
  meta.extend(meta[(625-512)*8:(625-512)*8+4]+[(1016+variant*4+i)|(12<<12) for i in range(4)]);attrs.append(attrs[625-512])
 sheet.save(p/'tiles.png');(p/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(meta),*meta));(p/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(attrs),*attrs))

def register():
 for symbol,(kind,_,slug,callback) in SPECS.items():
  refs='\n'.join(f'    INCGFX_U16("data/tilesets/{kind}/{slug}/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
  insert(ROOT/'src/data/tilesets/graphics.h','const u32 gTilesetTiles_AraunaAmanhecer[]',f'const u32 gTilesetTiles_{symbol}[] = INCGFX_U32("data/tilesets/{kind}/{slug}/tiles.png", ".4bpp.lz");\nconst u16 gTilesetPalettes_{symbol}[][16] =\n{{\n'+refs+'\n};\n\n',f'const u32 gTilesetTiles_{symbol}[]')
  insert(ROOT/'src/data/tilesets/metatiles.h','const u16 gMetatiles_AraunaAmanhecer[]',f'const u16 gMetatiles_{symbol}[] = INCBIN_U16("data/tilesets/{kind}/{slug}/metatiles.bin");\nconst u16 gMetatileAttributes_{symbol}[] = INCBIN_U16("data/tilesets/{kind}/{slug}/metatile_attributes.bin");\n\n',f'const u16 gMetatiles_{symbol}[]')
  insert(ROOT/'src/data/tilesets/headers.h','const struct Tileset gTileset_AraunaAmanhecer =',f'const struct Tileset gTileset_{symbol} =\n{{\n    .isCompressed = TRUE,\n    .isSecondary = '+('FALSE' if kind=='primary' else 'TRUE')+f',\n    .tiles = gTilesetTiles_{symbol},\n    .palettes = gTilesetPalettes_{symbol},\n    .metatiles = gMetatiles_{symbol},\n    .metatileAttributes = gMetatileAttributes_{symbol},\n    .callback = {callback},\n}};\n\n',f'const struct Tileset gTileset_{symbol} =')

def main():
 assets();register();path=ROOT/'data/layouts/layouts.json';node=json.loads(path.read_text())
 name='JaggedPass';map_path=ROOT/'data/maps'/name/'map.json';event=json.loads(map_path.read_text());baseline=json.loads(subprocess.check_output(['git','show',f'HEAD:data/maps/{name}/map.json'],cwd=ROOT))
 old_layout=next(r for r in node['layouts'] if r['id']==baseline['layout']);w,h=old_layout['width'],old_layout['height'];old=words(ROOT/old_layout['blockdata_filepath']);new=list(old)
 occupied={(int(e['x']),int(e['y'])) for group in ('warp_events','object_events','coord_events','bg_events') for e in event[group]}
 counts=[0,0]
 for y in range(2,h-2):
  for x in range(2,w-2):
   i=y*w+x
   if old[i]&1023!=625 or any(abs(x-a)+abs(y-b)<3 for a,b in occupied):continue
   if (x*17+y*29+x*y)%19 in (3,11):
    kind=(x+y)%2;new[i]=(old[i]&~1023)|(BASE+kind);counts[kind]+=1
 folder=ROOT/'data/layouts/AraunaPassoCortado';folder.mkdir(exist_ok=True);(folder/'map.bin').write_bytes(struct.pack('<%dH'%len(new),*new));shutil.copyfile(ROOT/old_layout['border_filepath'],folder/'border.bin')
 record=dict(old_layout,id=layout_id(name),name='AraunaPassoCortado_Layout',primary_tileset='gTileset_AraunaPassoPedra',secondary_tileset='gTileset_AraunaPassoCortado',blockdata_filepath='data/layouts/AraunaPassoCortado/map.bin',border_filepath='data/layouts/AraunaPassoCortado/border.bin')
 current=next((r for r in node['layouts'] if r['id']==record['id']),None)
 if current:current.update(record)
 else:node['layouts'].append(record)
 event['layout']=record['id'];dump(map_path,event);dump(path,node)
 print(json.dumps({'size':[w,h],'ash_and_flat_fragments':counts,'warps':len(event['warp_events']),'objects':len(event['object_events'])}))

if __name__=='__main__':main()
