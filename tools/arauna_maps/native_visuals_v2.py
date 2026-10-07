"""Indexed native pair editor; all allocation excludes hardware animation slots."""
import json,re,struct
from pathlib import Path
from PIL import Image
from bancos_nativos import resolve_bank
from render_native_map import Renderer,words,palette
ROOT=Path(__file__).resolve().parents[2]
BASE='73312e48f3542a78377024913fcaf44da5e771c0'
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def binary(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(struct.pack('<%dH'%len(v),*v))
def marked(p,tag,body):
 text=p.read_text();block='\n\n// '+tag+'_BEGIN\n'+body+'// '+tag+'_END\n';pattern=r'\n*// '+tag+r'_BEGIN\n.*?// '+tag+r'_END\n';p.write_text(re.sub(pattern,lambda _:block,text,flags=re.S) if '// '+tag+'_BEGIN' in text else text.rstrip()+block)
def callback(repo,sym):return re.search(r'const struct Tileset '+sym+r'\s*=\s*\{.*?\.callback = (\w+)',(repo/'src/data/tilesets/headers.h').read_text(),re.S)[1]
class Pair:
 def __init__(self,repo,layout,repack=False):
  self.layout=layout;self.paths=[resolve_bank(repo,layout[k]) for k in ('primary_tileset','secondary_tileset')];self.reader=Renderer(*self.paths);self.meta=[words(p/'metatiles.bin') for p in self.paths];self.attrs=[words(p/'metatile_attributes.bin') for p in self.paths];self.pals=[list(p) for p in self.reader.palettes];self.callbacks=[callback(repo,layout[k]) for k in ('primary_tileset','secondary_tileset')];self.dynamic=set(range(432,512))|set(range(992,1024))
  if self.callbacks[0].startswith('InitTilesetAnim_AraunaGrutas'):self.dynamic.update(range(424,432))
  if self.callbacks[1]=='InitTilesetAnim_Mauville':self.dynamic.update(range(608,672))
  if self.callbacks[1]=='InitTilesetAnim_EverGrande':self.dynamic.update(range(736,768))
  self.tiles={i:self.reader._tile(i).tobytes() for i in range(1024) if self.reader._tile(i) is not None};self.tile_cache={};self.touched=set()
  if repack:
   source=dict(self.tiles);self.tiles={i:raw for i,raw in source.items() if i in self.dynamic};self.tiles[0]=bytes(64);self.tile_cache={bytes(64):0};self.free=[i for i in list(range(1,432))+list(range(512,992)) if i not in self.dynamic]
   remap={}
   for entries in self.meta:
    for j,e in enumerate(entries):
     t=e&1023
     if t in self.dynamic:continue
     if t not in remap:remap[t]=self.tile(Image.frombytes('L',(8,8),source.get(t,bytes(64))))
     entries[j]=(e&~1023)|remap[t]
  else:
   used={e&1023 for a in self.meta for e in a}|self.dynamic;self.free=[i for i in list(range(1,424))+list(range(512,992)) if i not in used];self.tile_cache={raw:i for i,raw in self.tiles.items() if i not in self.dynamic}
  self.reserved=set();self.alias_cache={}
 def tile(self,im):
  raw=im.tobytes()
  if raw not in self.tile_cache:
   assert self.free,'No safe static graphics slot';i=self.free.pop(0);self.tiles[i]=raw;self.tile_cache[raw]=i;self.touched.add(i)
  return self.tile_cache[raw]
 def entries(self,im,pal):return [self.tile(im.crop((x,y,x+8,y+8)))|pal<<12 for x,y in ((0,0),(8,0),(0,8),(8,8))]
 def put(self,mid,bottom,pal,top=None):
  entries=self.entries(bottom,pal)+(self.entries(*top) if top else [0]*4);self.meta[mid>=512][mid%512*8:mid%512*8+8]=entries;return entries
 def alias(self,native,entries,attribute=None):
  attr=self.attrs[native>=512][native%512] if attribute is None else attribute;key=(attr,tuple(entries))
  if key in self.alias_cache:return self.alias_cache[key]
  mid=next((i for i in range(512,1024) if i not in self.reserved),None);assert mid is not None,'No secondary metatile ID';self.reserved.add(mid);local=mid-512
  while len(self.attrs[1])<=local:self.attrs[1].append(0);self.meta[1].extend([0]*8)
  self.attrs[1][local]=attr;self.meta[1][local*8:local*8+8]=entries;self.alias_cache[key]=mid;return mid
 def write(self,paths,kinds=(0,1)):
  for kind,path in enumerate(paths):
   if kind not in kinds:continue
   path.mkdir(parents=True,exist_ok=True);(path/'palettes').mkdir(exist_ok=True);off=512*kind;count=max([i-off+1 for i in self.tiles if off<=i<off+512] or [1]);count=(count+15)//16*16;im=Image.new('P',(128,count//16*8));im.putpalette([c for i in range(256) for c in (i,i,i)])
   for i,raw in self.tiles.items():
    if off<=i<off+count:im.paste(Image.frombytes('L',(8,8),raw),((i-off)%16*8,(i-off)//16*8))
   im.save(path/'tiles.png',bits=4);binary(path/'metatiles.bin',self.meta[kind]);binary(path/'metatile_attributes.bin',self.attrs[kind])
   for q in range(13):
    colors=self.pals[q] if (q<6)==(kind==0) else [(0,0,0)]*16;(path/f'palettes/{q:02}.pal').write_bytes(('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in colors)).encode())
 def reserve(self,repo,names,layouts,maps):
  for n in names:
   m=maps[n];l=layouts[m['layout']]
   self.reserved.update(v&1023 for field in ('blockdata_filepath','border_filepath') for v in words(repo/l[field]))
  labels={k:int(v,16) for k,v in re.findall(r'#define (METATILE_\w+)\s+(0x[\da-fA-F]+)',(repo/'include/constants/metatile_labels.h').read_text())};text=''.join(p.read_text(errors='ignore') for p in (repo/'src').glob('*.c'))
  for n in names:text+=''.join(p.read_text() for p in (repo/'data/maps'/n).glob('*.inc'))
  self.reserved.update(labels[k] for k in set(re.findall(r'METATILE_\w+',text)) if k in labels)
def declarations(paths,symbols,callbacks):
 out={k:'' for k in ('graphics.h','metatiles.h','headers.h')}
 for kind,(p,s,cb) in enumerate(zip(paths,symbols,callbacks)):
  p=p.relative_to(ROOT).as_posix();out['graphics.h']+=f'const u32 gTilesetTiles_{s}[] = INCGFX_U32("{p}/tiles.png", ".4bpp.lz");\nconst u16 gTilesetPalettes_{s}[][16] =\n{{\n'+''.join(f'    INCGFX_U16("{p}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(13))+'};\n';out['metatiles.h']+=f'const u16 gMetatiles_{s}[] = INCBIN_U16("{p}/metatiles.bin");\nconst u16 gMetatileAttributes_{s}[] = INCBIN_U16("{p}/metatile_attributes.bin");\n';out['headers.h']+=f'const struct Tileset gTileset_{s} =\n{{\n    .isCompressed = TRUE,\n    .isSecondary = {"TRUE" if kind else "FALSE"},\n    .tiles = gTilesetTiles_{s},\n    .palettes = gTilesetPalettes_{s},\n    .metatiles = gMetatiles_{s},\n    .metatileAttributes = gMetatileAttributes_{s},\n    .callback = {cb},\n}};\n'
 return out
