#!/usr/bin/env python3
"""Build compact, original campaign artwork. Keep functional metatile IDs.

The atlas is new artwork, not a colour transform of Emerald. Conversion here
only crops the atlas modules, scales to native sprite footprints and encodes
their palette. Unused scoped metatiles are transparent rather than carrying
unreferenced Hoenn drawings. Native PC states and six truck door IDs remain.
"""
import json, re, shutil, struct
from pathlib import Path
from PIL import Image, ImageDraw
from render_native_map import indexed_tiles, words, palette
from build_campanha_interiores_v1 import MAPS, SPECS, floor_art, art_palette

ROOT=Path(__file__).resolve().parents[2]
BASE='d561ab72aeb1c98ac72b0dd6661510effaa7362d'
MARK='CAMPANHA_INTERIORES_V2'
OUT=ROOT/'review/campanha_interiores_v2'
ATLAS=ROOT/'art/campanha_interiores_v2/source_atlas.png'
NAMES=('paving','wall','window','door','shelf','table','chair','fern','net','shutter','nursery','counter','pc','weather','stairs','crate')

def dump(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

def artwork():
 src=Image.open(ATLAS).convert('RGB');raw={}
 for i,name in enumerate(NAMES):
  y,x=divmod(i,4)
  im=src.crop((round(x*src.width/4)+12,round(y*src.height/4)+12,round((x+1)*src.width/4)-12,round((y+1)*src.height/4)-12)).convert('RGBA')
  im.putdata([(r,g,b,0 if r>140 and b>140 and g<130 else 255) for r,g,b,a in im.getdata()])
  im=im.crop(im.getbbox());raw[name]=im
 # One shared module palette for timber/plaster, plus richer botanical and
 # device palettes. Each module gets at most 15 opaque RGB555 colours.
 groups={6:tuple(n for n in NAMES if n not in ('fern','nursery','pc','weather')),7:('fern','nursery'),8:('pc','weather')}
 palettes={};art={}
 for slot,names in groups.items():
  samples=[]
  for name in names:
   im=raw[name].resize((48,48),Image.Resampling.NEAREST)
   samples.extend((r,g,b) for r,g,b,a in im.getdata() if a)
  sample=Image.new('RGB',(len(samples),1));sample.putdata(samples)
  p=sample.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette()[:45]
  colors=[(0,0,0)]+[tuple((c>>3)<<3 for c in p[j:j+3]) for j in range(0,45,3)]
  palettes[slot]=colors
  for name in names:
   rgba=raw[name];pix=Image.new('L',rgba.size)
   pix.putdata([0 if not a else min(range(1,16),key=lambda j:sum((a-b)**2 for a,b in zip((r,g,b),colors[j]))) for r,g,b,a in rgba.getdata()])
   art[name]=(pix,slot)
 return art,palettes

ART,PALS=artwork()

def asset(name,size):
 im,pal=ART[name];return im.resize(size,Image.Resampling.NEAREST),pal

def painted(kind,size):
 # These native code modules supply gameplay shapes absent from the atlas.
 # All are newly drawn; none read original tiles or apply colour transforms.
 im=Image.new('L',size,0);d=ImageDraw.Draw(im);w,h=size
 if kind=='bed':
  d.rectangle((2,1,w-3,h-3),fill=4,outline=1);d.rectangle((4,3,w-5,10),fill=6)
  d.rectangle((4,12,w-5,h-6),fill=13,outline=12)
  for y in range(13,h-7,4):d.line((5,y,w-6,y),fill=14)
  for x in (2,w-4):d.rectangle((x,h-5,x+1,h-1),fill=1)
 elif kind=='fence':
  d.line((0,h//2,w,h//2),fill=6,width=2)
  d.line((0,h//2+4,w,h//2+4),fill=4)
  for x in range(2,w,12):
   d.rectangle((x,2,x+2,h-1),fill=4,outline=1);d.line((x,3,x+2,3),fill=5)
 elif kind=='rug':
  d.rectangle((0,0,w-1,h-1),fill=4,outline=1)
  for y in range(2,h-2):
   for x in range(2,w-2):
    if (x+y)%8 in (0,1):d.point((x,y),fill=6)
  d.rectangle((2,2,w-3,h-3),outline=5)
 elif kind=='mat':
  d.rectangle((0,0,w-1,h-1),fill=4)
  for y in range(h):
   for x in range(w):
    if y%4==0:d.point((x,y),fill=3)
    elif (x+y//4)%4==0:d.point((x,y),fill=2)
 elif kind=='chart':
  d.rectangle((1,1,w-2,h-2),fill=4,outline=1);d.rectangle((3,3,w-4,h-5),fill=6)
  for x in range(6,w-4,5):d.line((x,5,x,h-8),fill=7)
  d.line([(5,h-9),(10,h-14),(14,h-11),(20,h-19),(w-6,h-15)],fill=12,width=2)
  d.rectangle((5,h-6,w-6,h-5),fill=15)
 else:raise ValueError(kind)
 return im,12

class Bank:
 def __init__(self,key):
  self.key=key;source,_,self.style=SPECS[key]
  self.src=ROOT/'data/tilesets/secondary'/source
  self.dst=ROOT/'data/tilesets/secondary'/('arauna_campanha_'+key+'_v2')
  self.symbol='AraunaCampanha'+key.title()+'V2'
  self.attrs=words(self.src/'metatile_attributes.bin')
  self.meta=[512]*(len(self.attrs)*8)
  self.tiles=[bytes(64)];self.cache={bytes(64):512}
  self.floor=floor_art(self.style);self.changed=set();self.decorated=set()
  self.dst.mkdir(parents=True,exist_ok=True)
  shutil.copytree(self.src/'palettes',self.dst/'palettes',dirs_exist_ok=True)
  self.colors={**PALS,11:[(0,0,0),(0,0,0)]+[(8,8,8)]*14,12:art_palette(self.style)}
  self.used=set();self.blocked=set();self.border_ids=set();self.grid_ids=set()
  node=json.loads((ROOT/'data/layouts/layouts.json').read_text())
  for name,(lid,k) in MAPS.items():
   if k!=key:continue
   l=next(l for l in node['layouts'] if l['id']==lid)
   for field in ('blockdata_filepath','border_filepath'):
    for raw in words(ROOT/l[field]):
     mid=raw&1023
     if mid>=512:
      self.used.add(mid)
      (self.grid_ids if field=='blockdata_filepath' else self.border_ids).add(mid)
     if raw&0xc00:self.blocked.add(mid)
  if key=='carga':self.used|={0x208,0x210,0x218,0x20d,0x215,0x21d}
  for mid in self.used:
   self.put(mid,self.floor,12,None)

 def tile(self,im):
  p=im.tobytes()
  if p not in self.cache:
   assert len(self.tiles)<480,(self.key,'static tile budget')
   self.cache[p]=512+len(self.tiles);self.tiles.append(p)
  return self.cache[p]

 def entries(self,im,pal):
  return [self.tile(im.crop((x,y,x+8,y+8)))|(pal<<12) for x,y in ((0,0),(8,0),(0,8),(8,8))]

 def put(self,mid,bottom,pal,top=None):
  assert 512<=mid<512+len(self.attrs)
  self.meta[(mid-512)*8:(mid-511)*8]=self.entries(bottom,pal)+(self.entries(top[0],top[1]) if top else [512]*4)
  self.changed.add(mid)

 def module(self,mids,art,bg=None):
  im,pal=art
  assert im.size==(len(mids[0])*16,len(mids)*16),(self.key,mids,im.size)
  for y,row in enumerate(mids):
   for x,mid in enumerate(row):
    if mid is None:continue
    self.put(mid,bg if bg is not None else self.floor,12,(im.crop((x*16,y*16,x*16+16,y*16+16)),pal));self.decorated.add(mid)

 def single(self,mid,name,size=(16,16)):
  self.module(((mid,),),asset(name,size))

 def walls(self,top,low):
  for a,b in zip(top,low):self.module(((a,),(b,)),asset('wall',(16,32)))

 def redraw(self):
  k=self.key
  if k=='briney':
   self.walls([0x215],[0x21d]);self.module(((0x217,),(0x21f,)),asset('window',(16,32)))
   self.module(((0x2b1,0x2b2),(0x2b9,0x2ba),(0x2c1,0x2c2)),asset('shelf',(32,48)))
   self.module(((0x2be,0x2bf),(0x2c6,0x2c7),(0x2ce,0x2cf)),asset('net',(32,48)))
   self.module(((0x24e,0x24f),(0x256,0x257)),asset('table',(32,32)))
   self.module(((0x2a0,),(0x2a8,)),asset('crate',(16,32)))
   for mid in (0x2b3,0x2b4):self.single(mid,'crate')
   self.single(0x244,'chair')
   for triple in ((0x2e3,0x2eb,0x2f3),(0x2e4,0x2ec,0x2f4)):
    self.module(tuple((i,) for i in triple),asset('wall',(16,48)))
   self.module(((0x210,0x211),),painted('rug',(32,16)))
   for mid in (0x318,0x31b,0x320,0x323):
    trim=self.floor.copy();ImageDraw.Draw(trim).line((0,0,15,0),fill=1,width=2);self.put(mid,trim,12)
  elif k=='abrigo':
   self.walls([0x205],[0x20d]);self.module(((0x207,),(0x20f,)),asset('window',(16,32)))
   self.module(((0x279,0x27a),(0x281,0x282),(0x289,0x28a)),asset('net',(32,48)))
   self.module(((0x286,0x287),(0x28e,0x28f),(0x296,0x297)),asset('pc',(32,48)))
   self.module(((0x248,0x249),(0x250,0x251)),asset('table',(32,32)))
   self.single(0x2e2,'chair');self.single(0x22a,'fern')
   self.module(((0x290,),(0x298,)),asset('fern',(16,32)))
   for mid in (0x235,0x236,0x237,0x23d,0x23e,0x23f,0x245,0x246,0x247):
    self.module(((mid,),),painted('mat',(16,16)))
   self.module(((0x208,0x209),),painted('rug',(32,16)))
  elif k=='flores':
   self.walls([0x210,0x211,0x212,0x213],[0x218,0x219,0x21a,0x21b])
   self.module(((0x214,),(0x21c,)),asset('shutter',(16,32)))
   self.module(((0x215,),(0x21d,)),asset('window',(16,32)))
   self.single(0x216,'window')
   self.module(((0x223,0x224),(0x22b,0x22c)),asset('nursery',(32,32)))
   self.module(((0x233,0x234),(0x23b,0x23c)),asset('nursery',(32,32)))
   self.module(((0x225,),(0x235,)),asset('fern',(16,32)))
   self.module(((0x22d,),(0x236,)),asset('nursery',(16,32)))
   self.single(0x22e,'nursery');self.single(0x21e,'nursery')
   self.single(0x217,'fern');self.single(0x227,'fern')
   self.single(0x226,'crate');self.single(0x21f,'crate')
   self.single(0x23d,'chair');self.single(0x22f,'pc')
   self.module(((0x237,),(0x23f,),(0x247,)),asset('counter',(16,48)))
   self.module(((0x245,),(0x23e,),(0x246,)),asset('counter',(16,48)))
  elif k=='daycare':
   self.walls([0x208,0x209,0x20f],[0x210,0x211,0x217])
   self.module(((0x20c,0x20d),(0x224,0x215)),asset('window',(32,32)))
   self.module(((0x235,0x236,0x237),(0x23d,0x23e,0x23f)),asset('door',(48,32)))
   self.single(0x234,'shelf');self.single(0x21c,'shutter')
   self.module(((0x21d,),(0x225,)),asset('fern',(16,32)))
   self.module(((0x220,0x22e,0x221,0x223),),asset('counter',(64,16)))
   self.module(((0x229,0x22a),(0x231,0x232)),asset('table',(32,32)))
   for mid in (0x228,0x230):self.single(mid,'chair')
   for mid in (0x204,0x21a,0x22d,0x238,0x239):self.module(((mid,),),painted('mat',(16,16)))
   for mid in (0x240,0x241,0x243):self.module(((mid,),),painted('fence',(16,16)))
   self.module(((0x23b,0x23c),),painted('rug',(32,16)))
   self.module(((0x20a,),),(asset('pc',(16,32))[0].crop((0,0,16,16)),8))
  elif k=='clima':
   self.walls([0x25f],[0x267])
   # Timber partitions keep the original crossing points, with custom posts.
   for mid in (0x26b,0x270,0x278,0x280,0x281,0x273):self.single(mid,'wall')
   self.module(((0x260,0x261),(0x253,0x254),(0x28a,0x28b)),asset('weather',(32,48)))
   self.module(((0x264,0x265),),asset('weather',(32,16)))
   self.module(((0x22c,0x22d),(0x234,0x235)),painted('chart',(32,32)))
   self.module(((0x26c,0x26d),(0x274,0x275)),painted('bed',(32,32)))
   self.module(((0x288,0x289),(0x290,0x291),(0x298,0x299)),asset('window',(32,48)))
   self.module(((0x27c,0x27d,0x27e),(0x284,0x285,0x286),(0x28c,0x28d,0x28e)),asset('stairs',(48,48)))
   self.single(0x283,'stairs')
   for mid in (0x25d,0x266,0x287):self.single(mid,'fern')
   for mid in (0x256,0x257,0x25e,0x25c):self.single(mid,'pc')
   self.module(((0x206,0x207),),painted('rug',(32,16)))
   # Top section of the native PC occupies the tile immediately above ID 4.
   self.module(((0x26e,),),(asset('pc',(16,32))[0].crop((0,0,16,16)),8))
  elif k=='carga':
   node=json.loads((ROOT/'data/layouts/layouts.json').read_text())
   l=next(l for l in node['layouts'] if l['id']=='LAYOUT_INSIDE_OF_TRUCK')
   cells=words(ROOT/l['blockdata_filepath'])
   canvas=Image.new('L',(80,80));p=canvas.load()
   for y in range(80):
    for x in range(80):p[x,y]=4 if x in (0,1,78,79) or y in (0,1,78,79) else (3 if y%8==0 else 2)
   d=ImageDraw.Draw(canvas)
   for x in range(4,80,12):d.point((x,2),fill=6);d.point((x,77),fill=6)
   for i,raw in enumerate(cells):
    x=i%5;y=i//5;self.put(raw&1023,canvas.crop((x*16,y*16,x*16+16,y*16+16)),12)
   for mid in (0x201,0x209,0x211,0x219,0x21a,0x21b,0x222,0x223,0x224):self.single(mid,'crate')
   self.module(((0x203,0x204),),asset('crate',(32,16)))
   for i,(closed,opened) in enumerate(((0x20d,0x208),(0x215,0x210),(0x21d,0x218))):
    door=Image.new('L',(16,16),4);dd=ImageDraw.Draw(door)
    for y in range(0,16,4):dd.line((0,y,15,y),fill=3)
    dd.line((0,0,0,15),fill=1,width=2)
    if i==1:dd.rectangle((2,6,4,8),fill=15)
    self.put(closed,door,12)
    light=Image.new('L',(16,16),6);ld=ImageDraw.Draw(light);ld.line((0,0,0,15),fill=5,width=2)
    for y in (3,11):ld.line((2,y,15,y),fill=7)
    self.put(opened,light,12)

 def save(self):
  if self.key!='carga':
   for mid in self.blocked & self.used - self.decorated:
    # Border/partition fragments without a dedicated prop stay visibly solid.
    self.single(mid,'wall')
  assert self.key=='carga' or self.blocked & self.used <= self.decorated
  # These IDs are used only outside the room. Native Emerald draws opaque
  # black here, not transparent index zero (which can expose a backdrop).
  black=Image.new('L',(16,16),1)
  for mid in self.border_ids-self.grid_ids:self.put(mid,black,11)
  for slot,colors in self.colors.items():writepal(self.dst,slot,colors)
  savebank(self.dst,self.tiles,self.meta,self.attrs)
  return {'static_tiles_including_transparent':len(self.tiles),'drawn_metatiles':sorted(self.changed),'decorated_metatiles':sorted(self.decorated),'blocked_cells_have_visible_architecture_or_prop':True,'unused_metatiles_transparent':True,'source_tiles_copied':0,'attributes_identical':True}

def writepal(path,slot,colors):
 p=path/f'palettes/{slot:02}.pal';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_bytes(('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in colors)).encode())

def savebank(path,tiles,meta,attrs):
 count=len(tiles);sheet=Image.new('P',(128,((count+15)//16)*8));sheet.putpalette([c for i in range(256) for c in (i,i,i)])
 for i,raw in enumerate(tiles):
  im=Image.frombytes('L',(8,8),raw);sheet.paste(im,(i%16*8,i//16*8))
 sheet.save(path/'tiles.png',bits=4)
 (path/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(meta),*meta))
 (path/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(attrs),*attrs))

def primary():
 dst=ROOT/'data/tilesets/primary/arauna_campanha_base_v2';dst.mkdir(parents=True,exist_ok=True)
 src=ROOT/'data/tilesets/primary/building';shutil.copytree(src/'palettes',dst/'palettes',dirs_exist_ok=True)
 colors=PALS[8];writepal(dst,1,colors);writepal(dst,2,art_palette('garden'))
 backdrop=palette(src/'palettes/00.pal');backdrop[1]=(0,0,0);writepal(dst,0,backdrop)
 tiles=[bytes(64)];cache={bytes(64):0}
 def entries(im,slot):
  out=[]
  for x,y in ((0,0),(8,0),(0,8),(8,8)):
   raw=im.crop((x,y,x+8,y+8)).tobytes()
   if raw not in cache:cache[raw]=len(tiles);tiles.append(raw)
   out.append(cache[raw]|slot<<12)
  return out
 meta=[0]*64;attrs=words(src/'metatile_attributes.bin')[:8]
 meta[8:16]=entries(Image.new('L',(16,16),1),0)+[0]*4
 for mid in (2,3,4,5):
  im=asset('pc',(16,32))[0].crop((0,16,16,32))
  # Keep off/on separate, with a visibly lit green screen in the on state.
  if mid in (3,5):
   im=im.copy();ImageDraw.Draw(im).rectangle((3,1,10,4),fill=min(range(1,16),key=lambda i:sum((a-b)**2 for a,b in zip(colors[i],(72,144,88)))))
  meta[mid*8:(mid+1)*8]=entries(im,1)+[0]*4
 for mid in (6,7):meta[mid*8:(mid+1)*8]=entries(painted('rug',(32,16))[0].crop(((mid-6)*16,0,(mid-5)*16,16)),2)+[0]*4
 savebank(dst,tiles,meta,attrs)
 return dst,'AraunaCampanhaBaseV2'

def main():
 node=json.loads((ROOT/'data/layouts/layouts.json').read_text());old={l['id']:l for l in node['layouts']}
 banks={k:Bank(k) for k in SPECS}
 for b in banks.values():b.redraw()
 pd,ps=primary();registrations=[(pd,ps,False)]+[(b.dst,b.symbol,True) for b in banks.values()]
 report={'base_commit':BASE,'maps':{},'banks':{k:b.save() for k,b in banks.items()}}
 for name,(lid,key) in MAPS.items():
  src=old[lid];dest=ROOT/'data/layouts'/('AraunaCampanhaV2_'+name);dest.mkdir(exist_ok=True)
  for file,field in (('map.bin','blockdata_filepath'),('border.bin','border_filepath')):shutil.copyfile(ROOT/src[field],dest/file)
  id='LAYOUT_ARAUNA_CAMPANHA_V2_'+re.sub(r'(?<=[a-z0-9])(?=[A-Z])','_',name).upper()
  l=dict(src,id=id,name=dest.name+'_Layout',primary_tileset=src['primary_tileset'] if key=='carga' else 'gTileset_'+ps,secondary_tileset='gTileset_'+banks[key].symbol,blockdata_filepath=str((dest/'map.bin').relative_to(ROOT)),border_filepath=str((dest/'border.bin').relative_to(ROOT)))
  found=next((x for x in node['layouts'] if x['id']==id),None)
  if found:found.update(l)
  else:node['layouts'].append(l)
  p=ROOT/'data/maps'/name/'map.json';m=json.loads(p.read_text());m['layout']=id;dump(p,m)
  report['maps'][name]={'layout':id,'source_layout':lid,'bank':key,'width':l['width'],'height':l['height']}
 dump(ROOT/'data/layouts/layouts.json',node)
 bodies={'graphics.h':'','metatiles.h':'','headers.h':''}
 for path,symbol,secondary in registrations:
  prefix=str(path.relative_to(ROOT))
  bodies['graphics.h']+=f'const u32 gTilesetTiles_{symbol}[] = INCGFX_U32("{prefix}/tiles.png", ".4bpp.lz");\nconst u16 gTilesetPalettes_{symbol}[][16] =\n{{\n'+''.join(f'    INCGFX_U16("{prefix}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n'
  bodies['metatiles.h']+=f'const u16 gMetatiles_{symbol}[] = INCBIN_U16("{prefix}/metatiles.bin");\nconst u16 gMetatileAttributes_{symbol}[] = INCBIN_U16("{prefix}/metatile_attributes.bin");\n'
  bodies['headers.h']+=f'const struct Tileset gTileset_{symbol} =\n{{\n    .isCompressed = TRUE,\n    .isSecondary = {"TRUE" if secondary else "FALSE"},\n    .tiles = gTilesetTiles_{symbol},\n    .palettes = gTilesetPalettes_{symbol},\n    .metatiles = gMetatiles_{symbol},\n    .metatileAttributes = gMetatileAttributes_{symbol},\n    .callback = NULL,\n}};\n'
 for filename,body in bodies.items():
  p=ROOT/'src/data/tilesets'/filename;text=re.sub(r'\n*// '+MARK+r'_BEGIN\n.*?// '+MARK+r'_END\n','',p.read_text(),flags=re.S)
  p.write_text(text.rstrip()+'\n\n// '+MARK+'_BEGIN\n'+body+'// '+MARK+'_END\n')
 # Only this object graphics ID uses the moving-box sheet and palette.
 crate,slot=asset('crate',(16,16));im=Image.new('P',crate.size);im.putdata(list(crate.getdata()));im.putpalette([c for rgb in PALS[slot] for c in rgb]+[0]*(768-48))
 im.save(ROOT/'graphics/object_events/pics/misc/moving_box.png',bits=4)
 p=ROOT/'graphics/object_events/palettes/moving_box.pal';p.write_bytes(('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in PALS[slot])).encode())
 dump(OUT/'build.json',report);print(json.dumps({k:v['static_tiles_including_transparent'] for k,v in report['banks'].items()}))

if __name__=='__main__':main()
