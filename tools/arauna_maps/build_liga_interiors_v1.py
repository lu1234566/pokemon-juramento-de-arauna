#!/usr/bin/env python3
"""Build the League hall, four voices and support interiors from native assets."""
import json,shutil,struct,subprocess
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
MAPS=tuple(p.parent.name for p in sorted((ROOT/'data/maps').glob('EverGrandeCity_*/map.json')))
SPECS={
 'AraunaLigaPedra':('primary','building','arauna_liga_pedra','InitTilesetAnim_Building'),
 'AraunaLigaVozes':('secondary','elite_four','arauna_liga_vozes','InitTilesetAnim_EliteFour'),
 'AraunaLigaHall':('secondary','pokemon_center','arauna_liga_hall','NULL'),
 'AraunaLigaMemoria':('secondary','cable_club','arauna_liga_memoria','NULL'),
}
ROOMS=('EverGrandeCity_SidneysRoom','EverGrandeCity_PhoebesRoom','EverGrandeCity_GlaciasRoom','EverGrandeCity_DrakesRoom')
ELITE_BASE=844
HALL_BASE=744
TABLET_BASE=850

def words(path):
 b=path.read_bytes();return list(struct.unpack('<%dH'%(len(b)//2),b))
def dump(path,node):path.write_text(json.dumps(node,indent=2,ensure_ascii=False)+'\n')
def target(symbol):kind,_,slug,_=SPECS[symbol];return ROOT/'data/tilesets'/kind/slug
def source(symbol):kind,slug,_,_=SPECS[symbol];return ROOT/'data/tilesets'/kind/slug
def layout_id(name):return 'LAYOUT_ARAUNA_LIGA_'+name.removeprefix('EverGrandeCity_').upper()+'_V1'
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
  assert s.count(anchor)==1;(path.write_text(s.replace(anchor,block+anchor)))
def medallion(w,h):
 art=Image.new('P',(w,h),0);d=ImageDraw.Draw(art)
 d.ellipse((2,2,w-3,h-3),fill=1,outline=3,width=2)
 d.ellipse((6,5,w-7,h-6),outline=4,width=1)
 cx,cy=w//2,h//2
 for x,y in ((cx,6),(w-9,cy),(cx,h-7),(8,cy)):
  d.polygon([(x,y-3),(x+3,y),(x,y+3),(x-3,y)],fill=6,outline=5)
 d.line((cx,9,cx,cy-2,w-12,cy,cx,cy+2,cx,h-10,12,cy,cx,cy-2),fill=4,width=1)
 d.ellipse((cx-5,cy-5,cx+5,cy+5),fill=2,outline=7)
 d.polygon([(cx,cy-4),(cx+4,cy),(cx,cy+4),(cx-4,cy)],fill=5)
 return art
def tablet():
 art=Image.new('P',(32,96),1);d=ImageDraw.Draw(art)
 d.rectangle((1,1,30,94),outline=3,width=2)
 d.line((4,4,27,4,27,91,4,91,4,4),fill=4,width=1)
 d.ellipse((6,10,25,33),fill=2,outline=3,width=1)
 d.polygon([(16,13),(22,22),(16,30),(10,22)],fill=6,outline=5)
 for y in (41,47,53,59,65,71,77,83):
  d.line((8,y,23,y),fill=2,width=1)
  d.line((10+(y%3),y,19+(y%4),y),fill=5,width=1)
 return art
def graft(path,art):
 """Use only graphic slots absent from the original metatile table."""
 sheet=Image.open(path/'tiles.png');assert sheet.mode=='P' and sheet.width==128 and sheet.height<=256
 if sheet.height<256:
  expanded=Image.new('P',(128,256),0);expanded.putpalette(sheet.getpalette());expanded.paste(sheet,(0,0));sheet=expanded
 used={v&1023 for v in words(path/'metatiles.bin')}
 free=[i for i in range(512,1024) if i not in used and i not in range(992,996) and i!=1016]
 need=art.width*art.height//64;slots=free[-need:];assert len(slots)==need
 for i,idx in enumerate(slots):
  x=i%(art.width//8)*8;y=i//(art.width//8)*8
  sheet.paste(art.crop((x,y,x+8,y+8)),((idx-512)%16*8,(idx-512)//16*8))
 sheet.save(path/'tiles.png');return slots
def glyph_entries(slots,columns,x,y,pal):
 q=y*2*columns+x*2;return [slots[i]|(pal<<12) for i in (q,q+1,q+columns,q+columns+1)]

def assets():
 for symbol in SPECS:clone(source(symbol),target(symbol))
 p=target('AraunaLigaPedra')
 palette(p/'palettes/00.pal',{1:(64,77,99),2:(115,132,149),3:(178,190,191),4:(235,236,220),5:(82,99,113),6:(121,144,157),7:(164,181,183),8:(215,224,211),9:(196,200,174),10:(57,128,142),11:(96,162,177),12:(161,195,192),13:(215,181,88),15:(132,137,89)})
 palette(p/'palettes/01.pal',{1:(44,66,94),2:(110,133,149),3:(170,187,182),4:(235,233,214),9:(117,88,49),10:(165,127,64),11:(205,171,89),12:(238,210,133)})
 p=target('AraunaLigaVozes')
 palette(p/'palettes/06.pal',{1:(41,58,83),2:(108,130,149),3:(179,200,209),4:(234,236,219),5:(222,184,91),6:(183,142,62),7:(132,100,51),8:(231,207,124),9:(116,181,205),10:(76,145,177),11:(52,111,147),12:(37,81,109),13:(171,188,192),14:(209,175,111),15:(128,169,170)})
 shades=[[(178,159,207),(156,136,187),(119,104,154),(88,76,119)],[(213,167,197),(185,134,171),(149,103,145),(112,76,115)],[(162,199,225),(123,169,205),(89,130,169),(60,95,132)],[(154,203,182),(111,173,151),(76,138,119),(48,101,92)]]
 for k,colors in enumerate(shades):
  palette(p/'palettes'/f'{7+k:02}.pal',{1:(45,58,82),3:(198,208,214),4:(233,234,219),5:colors[0],6:colors[1],7:colors[2],8:colors[3]})
  palette(p/'palettes'/f'{12+k:02}.pal',{1:colors[3],2:colors[2],3:(221,186,98),4:(245,219,146),5:(204,218,217),6:colors[0],7:(250,238,193)})
 palette(p/'palettes/11.pal',{1:(43,61,86),2:(85,111,128),3:(128,154,163),4:(187,207,203),5:(232,235,219),6:(183,209,209),7:(130,178,190),8:(82,143,165),9:(50,110,139),10:(44,89,113),11:(72,125,147),12:(94,127,172),14:(213,220,222)})
 combined=Image.new('P',(48,192),0);combined.paste(medallion(48,64),(0,0));combined.paste(medallion(48,32),(0,64));combined.paste(tablet(),(0,96))
 slots=graft(p,combined);meta=words(p/'metatiles.bin');attrs=words(p/'metatile_attributes.bin')
 for k in range(4):
  for i,src in enumerate((537,538,539,545,546,547,553,554,555,561,562,563)):
   src+=48*k;start=(src-512)*8
   meta[start:start+4]=meta[(556+48*k-512)*8:(556+48*k-512)*8+4]
   meta[start+4:start+8]=glyph_entries(slots,6,i%3,i//3,12+k)
 floor=meta[(787-512)*8+4:(787-512)*8+8]
 for i in range(6):meta.extend(floor+glyph_entries(slots,6,i%3,4+i//3,12));attrs.append(attrs[787-512])
 layouts=json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']
 for k,name in enumerate(ROOMS):
  original=json.loads(subprocess.check_output(['git','show',f'HEAD:data/maps/{name}/map.json'],cwd=ROOT))
  layout=next(r for r in layouts if r['id']==original['layout']);cells=words(ROOT/layout['blockdata_filepath']);w=layout['width']
  for side in range(2):
   for i in range(12):
    x=(0 if side==0 else 11)+i%2;y=4+i//2;src=cells[y*w+x]&1023
    meta.extend(meta[(src-512)*8:(src-512)*8+4]+glyph_entries(slots,6,i%2,6+i//2,12+k));attrs.append(attrs[src-512])
 (p/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(meta),*meta));(p/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(attrs),*attrs))
 p=target('AraunaLigaHall')
 palette(p/'palettes/06.pal',{1:(45,63,89),2:(112,136,153),3:(181,199,198),4:(234,237,219),5:(40,78,113),6:(60,113,148),7:(95,155,180),8:(171,207,213),9:(107,133,151),10:(142,168,181),11:(179,197,202),12:(215,221,212),13:(102,159,184),14:(218,189,97),15:(94,127,161)})
 palette(p/'palettes/07.pal',{1:(42,61,89),2:(112,131,154),3:(167,183,190),4:(233,237,219),5:(112,129,162),6:(147,168,189),7:(225,211,162),8:(213,179,104),9:(174,133,70),10:(228,229,195),11:(119,92,48),12:(82,121,102),13:(179,138,59),14:(147,215,225),15:(108,150,125)})
 palette(p/'palettes/15.pal',{1:(45,77,108),2:(64,113,143),3:(215,178,91),4:(241,216,142),5:(196,224,220),6:(112,182,202),7:(249,238,186)})
 slots=graft(p,medallion(64,64));meta=words(p/'metatiles.bin');attrs=words(p/'metatile_attributes.bin');assert len(attrs)==232
 floor=meta[(576-512)*8:(576-512)*8+4]
 for i in range(16):meta.extend(floor+glyph_entries(slots,8,i%4,i//4,15));attrs.append(attrs[576-512])
 (p/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(meta),*meta));(p/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(attrs),*attrs))
 p=target('AraunaLigaMemoria')
 palette(p/'palettes/06.pal',{1:(43,60,86),2:(201,223,224),3:(162,196,208),4:(111,158,180),5:(80,128,155),6:(58,99,128),7:(229,239,224),8:(169,151,115),9:(147,111,55),10:(194,157,78),11:(57,110,134),12:(134,181,197),13:(184,214,213)})

def register():
 for symbol,(kind,_,slug,callback) in SPECS.items():
  refs='\n'.join(f'    INCGFX_U16("data/tilesets/{kind}/{slug}/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
  insert(ROOT/'src/data/tilesets/graphics.h','const u32 gTilesetTiles_AraunaAmanhecer[]',f'const u32 gTilesetTiles_{symbol}[] = INCGFX_U32("data/tilesets/{kind}/{slug}/tiles.png", ".4bpp.lz");\nconst u16 gTilesetPalettes_{symbol}[][16] =\n{{\n'+refs+'\n};\n\n',f'const u32 gTilesetTiles_{symbol}[]')
  insert(ROOT/'src/data/tilesets/metatiles.h','const u16 gMetatiles_AraunaAmanhecer[]',f'const u16 gMetatiles_{symbol}[] = INCBIN_U16("data/tilesets/{kind}/{slug}/metatiles.bin");\nconst u16 gMetatileAttributes_{symbol}[] = INCBIN_U16("data/tilesets/{kind}/{slug}/metatile_attributes.bin");\n\n',f'const u16 gMetatiles_{symbol}[]')
  insert(ROOT/'src/data/tilesets/headers.h','const struct Tileset gTileset_AraunaAmanhecer =',f'const struct Tileset gTileset_{symbol} =\n{{\n    .isCompressed = TRUE,\n    .isSecondary = '+('FALSE' if kind=='primary' else 'TRUE')+f',\n    .tiles = gTilesetTiles_{symbol},\n    .palettes = gTilesetPalettes_{symbol},\n    .metatiles = gMetatiles_{symbol},\n    .metatileAttributes = gMetatileAttributes_{symbol},\n    .callback = {callback},\n}};\n\n',f'const struct Tileset gTileset_{symbol} =')

def main():
 assets();register();path=ROOT/'data/layouts/layouts.json';node=json.loads(path.read_text());report={}
 for name in MAPS:
  map_path=ROOT/'data/maps'/name/'map.json';event=json.loads(map_path.read_text());baseline=json.loads(subprocess.check_output(['git','show',f'HEAD:data/maps/{name}/map.json'],cwd=ROOT))
  original=next(r for r in node['layouts'] if r['id']==baseline['layout']);w,h=original['width'],original['height'];old=words(ROOT/original['blockdata_filepath']);new=list(old)
  occupied={(int(e['x']),int(e['y'])) for group in ('warp_events','object_events','coord_events','bg_events') for e in event[group]}
  if name=='EverGrandeCity_PokemonLeague_1F':
   for i in range(16):
    x,y=8+i%4,5+i//4;assert (x,y) not in occupied
    new[y*w+x]=(old[y*w+x]&~1023)|(HALL_BASE+i)
  if name=='EverGrandeCity_ChampionsRoom':
   for i in range(6):
    x,y=5+i%3,6+i//3;assert (x,y) not in occupied and old[y*w+x]&1023==787
    new[y*w+x]=(old[y*w+x]&~1023)|(ELITE_BASE+i)
  if name in ROOMS:
   k=ROOMS.index(name)
   for side in range(2):
    for i in range(12):
     x=(0 if side==0 else 11)+i%2;y=4+i//2;assert (x,y) not in occupied
     new[y*w+x]=(old[y*w+x]&~1023)|(TABLET_BASE+k*24+side*12+i)
  secondary={'gTileset_EliteFour':'gTileset_AraunaLigaVozes','gTileset_PokemonCenter':'gTileset_AraunaLigaHall','gTileset_CableClub':'gTileset_AraunaLigaMemoria'}[original['secondary_tileset']]
  folder=ROOT/'data/layouts'/('AraunaLiga_'+name.removeprefix('EverGrandeCity_'));folder.mkdir(exist_ok=True)
  (folder/'map.bin').write_bytes(struct.pack('<%dH'%len(new),*new));shutil.copyfile(ROOT/original['border_filepath'],folder/'border.bin')
  record=dict(original,id=layout_id(name),name=folder.name+'_Layout',primary_tileset='gTileset_AraunaLigaPedra',secondary_tileset=secondary,blockdata_filepath=str((folder/'map.bin').relative_to(ROOT)),border_filepath=str((folder/'border.bin').relative_to(ROOT)))
  current=next((r for r in node['layouts'] if r['id']==record['id']),None)
  if current:current.update(record)
  else:node['layouts'].append(record)
  event['layout']=record['id'];dump(map_path,event);report[name]={'size':[w,h],'warps':len(event['warp_events']),'changed_cells':sum(a!=b for a,b in zip(old,new))}
 dump(path,node);print(json.dumps(report,indent=2))

if __name__=='__main__':main()
