#!/usr/bin/env python3
"""Native first-act composition. Keep the three scripted staging areas.

The five-map compatibility bank retains every ID used by the two adjacent
routes and every incoming border ID. New IDs/tiles use only the remaining
static slots; palettes and animation slots remain byte-for-byte unchanged.
"""
import json, re, struct
from pathlib import Path
from PIL import Image, ImageDraw
from render_native_map import Renderer, resolve_tileset, words, indexed_tiles
from connection_cache import rectangle

ROOT=Path(__file__).resolve().parents[2]
BASE='42cff21717'
MARK='INICIO_GEOMETRIA_V1'
MAPS=('LittlerootTown','OldaleTown','Route101','Route102','Route103')
TARGETS=MAPS[:3]
NAMES=('home','timber','lab','clinic','shop','inn','araucaria','ipe','sign','fence','bench','fern','grass','earth','capim','rock')
def dump(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def marked(p,s):
 t=p.read_text();t=re.sub(r'\n// BEGIN '+MARK+r'.*?// END '+MARK+r'\n','\n',t,flags=re.S)
 p.write_text(t.rstrip()+'\n\n// BEGIN '+MARK+'\n'+s+'// END '+MARK+'\n')
def oldfile(p):
 import subprocess
 return subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT)
def oldjson(p):return json.loads(oldfile(p))

class Bank:
 def __init__(self,live,keep):
  self.old=Renderer(resolve_tileset('gTileset_General'),resolve_tileset('gTileset_AraunaAmanhecer'))
  self.pals=self.old.palettes
  self.meta=[0]*8192;self.attrs=[0]*1024;self.tiles={0:bytes(64)};self.cache={bytes(64):0}
  for mid in sorted(keep):
   source=self.old.primary_metatiles if mid<512 else self.old.secondary_metatiles
   attr=words((self.old.primary if mid<512 else self.old.secondary)/'metatile_attributes.bin')
   i=mid%512
   if (i+1)*8>len(source):continue
   self.meta[mid*8:mid*8+8]=source[i*8:i*8+8];self.attrs[mid]=attr[i]
   for e in source[i*8:i*8+8]:
    tid=e&1023;t=self.old._tile(tid)
    if t is not None:self.tiles[tid]=t.tobytes()
  # General animation overwrites these slots. Keep them reserved even when
  # a layout currently has no animated cell. Doors overwrite 992..1023.
  # Compact exact duplicate static pixels, while keeping native metatile IDs
  # and palette/flip bits. Animated slots never serve as static aliases.
  self.cache={bytes(64):0}
  for tid in sorted(self.tiles):
   if tid<432 or 512<=tid<992:self.cache.setdefault(self.tiles[tid],tid)
  for mid in keep:
   for i in range(mid*8,mid*8+8):
    e=self.meta[i];tid=e&1023
    if tid in self.tiles and (tid<432 or 512<=tid<992):self.meta[i]=(e&~1023)|self.cache[self.tiles[tid]]
  used={e&1023 for mid in keep for e in self.meta[mid*8:mid*8+8]}|{0}
  self.tiles={tid:data for tid,data in self.tiles.items() if tid in used}
  self.free_tiles=iter(i for i in list(range(1,432))+list(range(512,992)) if i not in self.tiles)
  self.free_ids=iter(i for i in range(512,1024) if i not in live)
  self.art={};self.custom_ids=[];self.custom_tiles=set();self.known={};self.rgba_cache={}
  src=Image.open(ROOT/'art/inicio_geometria_v1/source_atlas.png').convert('RGB')
  for i,n in enumerate(NAMES):
   y,x=divmod(i,4);im=src.crop((round(x*src.width/4)+9,round(y*src.height/4)+9,round((x+1)*src.width/4)-9,round((y+1)*src.height/4)-9)).convert('RGBA')
   im.putdata([(r,g,b,0 if r>140 and b>140 and g<130 else 255) for r,g,b,a in im.getdata()]);self.art[n]=im.crop(im.getbbox())
  # Quiet native textures make the landmarks readable at 240x160. These are
  # freshly drawn patterns, rather than a colour transform of old floors.
  self.grass=Image.new('RGBA',(16,16),(104,136,80,255));d=ImageDraw.Draw(self.grass)
  for x,y in [(2,3),(11,10)]:
   d.line([(x,y+2),(x,y),(x+1,y+3),(x+2,y+1)],fill=(72,112,64,255))
   d.point((x+3,y+3),fill=(136,160,96,255))
  self.earth=Image.new('RGBA',(16,16),(168,112,72,255));d=ImageDraw.Draw(self.earth)
  for x,y in [(3,5),(11,2),(7,12)]:
   d.line((x,y,x+1,y),fill=(192,136,88,255));d.point((x+1,y+1),fill=(144,88,56,255))
 def asset(self,n,size):return self.art[n].resize(size,Image.Resampling.NEAREST)
 def tile(self,b):
  if b not in self.cache:
   i=next(self.free_tiles);self.tiles[i]=b;self.cache[b]=i;self.custom_tiles.add(i)
  return self.cache[b]
 def block(self,rgba,attr=0,forced=None):
  # Quantize each metatile to the best unchanged palette. No reserved BG
  # palette or transparent colour is consumed by opaque floor pixels.
  im=rgba.convert('RGB');cache_key=(im.tobytes(),attr,forced)
  if cache_key in self.rgba_cache:return self.rgba_cache[cache_key]
  pixels=list(im.getdata());best=None
  for q,pal in enumerate(self.pals):
   mapping={c:min(range(1,16),key=lambda j:sum((a-b)**2 for a,b in zip(c,pal[j]))) for c in set(pixels)}
   loss=sum(sum((a-b)**2 for a,b in zip(c,pal[mapping[c]])) for c in pixels)
   if best is None or loss<best[0]:best=(loss,q,mapping)
  _,q,mp=best;pix=Image.new('L',(16,16));pix.putdata([mp[c] for c in pixels])
  entries=[self.tile(pix.crop((x,y,x+8,y+8)).tobytes()) | q<<12 for y in (0,8) for x in (0,8)]+[0]*4
  key=(tuple(entries),attr)
  if forced is None and key in self.known:
   self.rgba_cache[cache_key]=self.known[key];return self.known[key]
  mid=forced if forced is not None else next(self.free_ids)
  self.meta[mid*8:mid*8+8]=entries;self.attrs[mid]=attr;self.known[key]=mid;self.custom_ids.append(mid)
  self.rgba_cache[cache_key]=mid;return mid
 def floor(self,kind='grass',attr=0):return self.block(self.earth if kind=='earth' else self.grass,attr)
 def sprite(self,n,size):
  im=Image.new('RGBA',size);base=self.grass
  for y in range(0,size[1],16):
   for x in range(0,size[0],16):im.paste(base,(x,y))
  im.alpha_composite(self.asset(n,size));return im
 def write(self):
  for primary,sym,slug in [(True,'AraunaInicioBaseV1','arauna_inicio_base_v1'),(False,'AraunaInicioSulV1','arauna_inicio_sul_v1')]:
   dest=ROOT/'data/tilesets'/('primary' if primary else 'secondary')/slug;dest.mkdir(parents=True,exist_ok=True)
   sheet=Image.new('P',(128,256));sheet.putpalette([v for i in range(256) for v in (i,i,i)])
   for tid,b in self.tiles.items():
    if (tid<512)!=primary:continue
    i=tid%512;sheet.paste(Image.frombytes('P',(8,8),b),((i%16)*8,(i//16)*8))
   sheet.save(dest/'tiles.png',bits=4)
   offset=0 if primary else 512
   (dest/'metatiles.bin').write_bytes(struct.pack('<4096H',*self.meta[offset*8:(offset+512)*8]))
   (dest/'metatile_attributes.bin').write_bytes(struct.pack('<512H',*self.attrs[offset:offset+512]))
   original=self.old.primary if primary else self.old.secondary
   (dest/'palettes').mkdir(exist_ok=True)
   for i in range(16):(dest/f'palettes/{i:02}.pal').write_bytes((original/f'palettes/{i:02}.pal').read_bytes())
   self.declarations.append((primary,sym,dest.relative_to(ROOT).as_posix()))

class Map:
 def __init__(self,n,b,base):
  self.name=n;self.bank=b;self.data=oldjson(f'data/maps/{n}/map.json');self.layout=next(l for l in base['layouts'] if l['id']==self.data['layout']);self.w=self.layout['width'];self.h=self.layout['height']
  self.old=words(ROOT/self.layout['blockdata_filepath']);self.g=[b.floor()|0x3000]*(self.w*self.h)
  self.path=set();self.required=set()
 def set(self,x,y,mid,collision=0):
  if 0<=x<self.w and 0<=y<self.h:self.g[y*self.w+x]=mid|0x3000|(collision<<10)
 def clear(self,x0,y0,x1,y1):
  for y in range(y0,y1+1):
   for x in range(x0,x1+1):self.set(x,y,self.bank.floor())
 def road(self,points,radius=1):
  for (a,b),(c,d) in zip(points,points[1:]):
   length=max(abs(c-a),abs(d-b),1)
   for i in range(length+1):
    x=round(a+(c-a)*i/length);y=round(b+(d-b)*i/length)
    for yy in range(y-radius,y+radius+1):
     for xx in range(x-radius,x+radius+1):
      if 0<=xx<self.w and 0<=yy<self.h:self.path.add((xx,yy))
 def paint_roads(self):
  for x,y in self.path:self.set(x,y,self.bank.floor('earth'))
 def put(self,n,x,y,w,h,door=None):
  im=self.bank.sprite(n,(w*16,h*16))
  for yy in range(h):
   for xx in range(w):self.set(x+xx,y+yy,self.bank.block(im.crop((xx*16,yy*16,(xx+1)*16,(yy+1)*16))),1)
  if door:
   dx,dy,raw=door;self.g[dy*self.w+dx]=raw;self.required.add((dx,dy+1))
 def sign(self,x,y):self.put('sign',x,y,1,1)
 def edge(self):
  # Keep exactly the native crossing cells and their upper flags.
  for y in range(self.h):
   for x in range(self.w):
    if x in (0,self.w-1) or y in (0,self.h-1):
     old=self.old[y*self.w+x]
     if any(e['x']==x and e['y']==y for e in self.data['warp_events']):
      self.g[y*self.w+x]=old
     elif old&0xc00:
      im=self.bank.sprite('fern',(16,16));self.set(x,y,self.bank.block(im),1)
     else:
      self.set(x,y,self.bank.floor('earth'));self.required.add((x,y))
 def finish(self):
  self.edge()
  p=ROOT/f'data/layouts/Arauna{self.name}ComposicaoV1';p.mkdir(parents=True,exist_ok=True)
  (p/'map.bin').write_bytes(struct.pack('<%dH'%len(self.g),*self.g))
  border=self.bank.block(self.bank.sprite('fern',(16,16)))|0x3400
  (p/'border.bin').write_bytes(struct.pack('<4H',*([border]*4)))
  l=dict(self.layout,id='LAYOUT_ARAUNA_'+re.sub(r'([a-z])([A-Z])',r'\1_\2',self.name).upper()+'_COMPOSICAO_V1',name='Arauna'+self.name+'ComposicaoV1_Layout',primary_tileset='gTileset_AraunaInicioBaseV1',secondary_tileset='gTileset_AraunaInicioSulV1',blockdata_filepath=str((p/'map.bin').relative_to(ROOT)),border_filepath=str((p/'border.bin').relative_to(ROOT)))
  self.data['layout']=l['id'];dump(ROOT/f'data/maps/{self.name}/map.json',self.data);return l

def main():
 base=oldjson('data/layouts/layouts.json');ls={l['id']:l for l in base['layouts']};ms={m['id']:m for p in (ROOT/'data/maps').glob('*/map.json') for m in [oldjson(str(p.relative_to(ROOT)))]}
 live=set();keep=set()
 for n in MAPS:
  m=oldjson(f'data/maps/{n}/map.json');l=ls[m['layout']]
  for field in ('blockdata_filepath','border_filepath'):
   used={v&1023 for v in struct.unpack('<%dH'%(len(oldfile(l[field]))//2),oldfile(l[field]))};live.update(used)
   if n not in TARGETS or field=='border_filepath':keep.update(used)
  for c in m['connections']:
   other=ls[ms[c['map']]['layout']];g=struct.unpack('<%dH'%(len(oldfile(other['blockdata_filepath']))//2),oldfile(other['blockdata_filepath']))
   used={g[y*other['width']+x]&1023 for x,y in rectangle(l['width'],l['height'],other['width'],other['height'],c['offset'],c['direction'])};live.update(used)
   if ms[c['map']]['name'] not in TARGETS:keep.update(used)
 keep.update((0x380,0x381,0x61,0x41))
 labels={k:int(v,16) for k,v in re.findall(r'#define (METATILE_General_\w+)\s+(0x[0-9A-Fa-f]+)',(ROOT/'include/constants/metatile_labels.h').read_text())}
 refs=set()
 for p in (ROOT/'src').rglob('*.c'):refs.update(re.findall(r'METATILE_General_\w+',p.read_text()))
 keep.update(labels[n] for n in refs if n in labels);live.update(keep)
 route=ls[oldjson('data/maps/Route101/map.json')['layout']];grid=struct.unpack('<1120H',oldfile(route['blockdata_filepath']))
 for e in oldjson('data/maps/Route101/map.json')['warp_events']:keep.add(grid[e['y']*40+e['x']]&1023)
 b=Bank(live,keep);b.declarations=[];new=[];reports={}
 # Homes retain the truck staging anchors; lab moves to the diagonal south.
 m=Map('LittlerootTown',b,base)
 m.road([(10,0),(11,6),(15,11),(14,16),(20,22)],1);m.road([(6,11),(11,12),(15,11),(24,14)],1);m.paint_roads()
 for args in [('home',4,7,4,4,(6,10,0x3780)),('timber',22,10,4,4,(24,13,0x3780)),('lab',18,19,5,4,(20,22,0x3781))]:m.put(*args)
 for x,y in [(1,1),(1,16),(4,20),(21,2),(25,4),(26,19),(13,22)]:m.put('araucaria',x,y,2,3)
 m.put('ipe',18,13,2,2);m.put('bench',13,17,2,1);m.put('fern',2,7,2,1);m.put('fence',3,14,2,1);m.put('fence',25,16,2,1)
 for x,y in [(17,11),(24,21),(10,11),(27,14)]:m.sign(x,y)
 # Scripted twin/shoes paths and truck unload trajectories stay open.
 for a in [(8,0,11,3),(10,3,11,9),(4,11,7,12),(22,14,25,15)]:m.clear(*a)
 m.data['warp_events'][2].update(x=20,y=22);m.data['bg_events'][1].update(x=24,y=21)
 m.data['object_events'][1].update(x=14,y=13);m.data['object_events'][2].update(x=23,y=18)
 new.append(m.finish());reports[m.name]={'lab_door_before':[12,21],'lab_door_after':[20,22],'home_anchors_preserved':True}
 # Roadside services occupy the arms of a Y, away from a central square.
 m=Map('OldaleTown',b,base)
 m.road([(8,25),(11,21),(14,16),(18,10),(20,0)],1);m.road([(0,10),(7,12),(14,16)],1);m.road([(14,16),(22,20)],1);m.road([(14,16),(7,19)],1);m.road([(18,10),(19,15)],1);m.paint_roads()
 for args in [('inn',6,6,4,4,(8,9,0x3380)),('home',20,17,4,4,(22,20,0x3380)),('clinic',5,16,5,4,(7,19,0x3061)),('shop',18,5,4,4,(20,8,0x3041))]:m.put(*args)
 for x,y in [(1,1),(12,2),(25,2),(25,10),(14,22),(1,20)]:m.put('araucaria',x,y,2,3)
 m.put('ipe',11,10,2,2);m.put('bench',15,19,2,1)
 # Potion tour is translated by (-5,+2), including both player/NPC lanes.
 m.clear(17,9,20,16);m.clear(1,10,2,12);m.clear(8,23,11,25)
 warps=[(8,9),(22,20),(7,19),(20,8)]
 for e,(x,y) in zip(m.data['warp_events'],warps):e.update(x=x,y=y)
 signs=[(16,17),(8,19),(21,8),(9,19),(22,8)]
 for e,(x,y) in zip(m.data['bg_events'],signs):e.update(x=x,y=y);m.sign(x,y)
 m.data['object_events'][0].update(x=13,y=18);m.data['object_events'][1].update(x=19,y=9)
 new.append(m.finish());reports[m.name]={'warps_before':[[6,7],[22,21],[3,18],[25,6]],'warps_after':[list(v) for v in warps],'mart_tour_translation':[-5,2]}
 # The rescue's southern 18x9 staging is kept; the upper trail meanders.
 m=Map('Route101',b,base)
 m.road([(10,0),(13,5),(21,10),(21,14),(14,19)],1);m.road([(21,14),(29,16),(39,16)],1);m.paint_roads()
 for x,y in [(1,2),(5,5),(15,1),(25,3),(29,6),(2,13),(10,11),(24,21),(34,20),(18,22)]:m.put('araucaria',x,y,2,3)
 m.put('ipe',17,6,2,2);m.put('rock',29,11,2,2);m.put('fence',30,19,3,1);m.put('fern',16,13,2,1)
 # Encounters retain their native behavior; add distinct wet capim patches.
 capim=b.sprite('capim',(16,16));tall=b.block(capim,2)
 for x0,y0,x1,y1 in [(4,7,8,10),(25,8,28,10),(27,22,32,24)]:
  for y in range(y0,y1+1):
   for x in range(x0,x1+1):m.set(x,y,tall)
 for y in range(19,28):
  for x in range(18):
   v=m.old[y*m.w+x];mid=v&1023;a=words((b.old.primary if mid<512 else b.old.secondary)/'metatile_attributes.bin')[mid%512];im=b.sprite('fern',(16,16)) if v&0xc00 else b.grass
   if a&255==2:im=capim
   mid=b.block(im,a);m.g[y*m.w+x]=mid|(v&0xfc00)
 # Keep the required First Chamber warp cells and their original behaviors.
 for e in m.data['warp_events']:m.g[e['y']*m.w+e['x']]=m.old[e['y']*m.w+e['x']]
 # One escape gate in the original scene: (14,19). No bypass to the east.
 for y in range(19,28):m.set(18,y,b.block(b.sprite('fence',(16,16))),1)
 for x,y in [(24,11),(35,15)]:m.sign(x,y)
 m.data['object_events'][0].update(x=22,y=7);m.data['object_events'][4].update(x=22,y=12);m.data['object_events'][7].update(x=13,y=11)
 new.append(m.finish());reports[m.name]={'rescue_staging_preserved':[0,19,17,27],'connections_and_chamber_warps_preserved':True}
 # These two routes retain their entire grids and events. Sharing the scoped
 # bank makes the new Oldale border legible without altering neighbor cells.
 for n in MAPS[3:]:
  l=dict(ls[oldjson(f'data/maps/{n}/map.json')['layout']]);l.update(primary_tileset='gTileset_AraunaInicioBaseV1',secondary_tileset='gTileset_AraunaInicioSulV1')
  for i,a in enumerate(base['layouts']):
   if a['id']==l['id']:base['layouts'][i]=l
 base['layouts']+=new;dump(ROOT/'data/layouts/layouts.json',base);b.write()
 for filename in ('graphics.h','metatiles.h','headers.h'):
  out=''
  for primary,sym,slug in b.declarations:
   if filename=='graphics.h':out+=f'const u32 gTilesetTiles_{sym}[] = INCGFX_U32("{slug}/tiles.png", ".4bpp.lz");\nconst u16 gTilesetPalettes_{sym}[][16] =\n{{\n'+''.join(f'    INCGFX_U16("{slug}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n'
   elif filename=='metatiles.h':out+=f'const u16 gMetatiles_{sym}[] = INCBIN_U16("{slug}/metatiles.bin");\nconst u16 gMetatileAttributes_{sym}[] = INCBIN_U16("{slug}/metatile_attributes.bin");\n'
   else:out+=f'const struct Tileset gTileset_{sym} =\n{{\n    .isCompressed = TRUE,\n    .isSecondary = '+('FALSE' if primary else 'TRUE')+f',\n    .tiles = gTilesetTiles_{sym},\n    .palettes = gTilesetPalettes_{sym},\n    .metatiles = gMetatiles_{sym},\n    .metatileAttributes = gMetatileAttributes_{sym},\n    .callback = '+('InitTilesetAnim_General' if primary else 'NULL')+',\n};\n'
  marked(ROOT/'src/data/tilesets'/filename,out)
 # Only absolute coordinates of the translated tour change. All commands,
 # conditions, text, items and movement bytecode remain the same.
 p=ROOT/'data/maps/OldaleTown/scripts.inc';t=oldfile(str(p.relative_to(ROOT))).decode().replace('LOCALID_OLDALE_MART_EMPLOYEE, 24, 13','LOCALID_OLDALE_MART_EMPLOYEE, 19, 15');p.write_text(t)
 p=ROOT/'src/data/heal_locations.json';h=oldjson(str(p.relative_to(ROOT)))
 for e in h['heal_locations']:
  if e['id']=='HEAL_LOCATION_OLDALE_TOWN':e.update(x=7,y=20)
 dump(p,h)
 p=ROOT/'docs/arauna/ARAUNA_OVERWORLD_PLACEMENT.csv'
 import csv,io
 rows=list(csv.DictReader(io.StringIO(oldfile(str(p.relative_to(ROOT))).decode())))
 for row in rows:
  if row['map']=='Route101' and row['channel']=='B':row.update(x='13',y='11')
 stream=io.StringIO();writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows);p.write_text(stream.getvalue())
 (ROOT/'include/constants/arauna_inicio_metatiles.h').write_text('#ifndef GUARD_ARAUNA_INICIO_METATILES_H\n#define GUARD_ARAUNA_INICIO_METATILES_H\n'+f'#define METATILE_AraunaInicio_Campo 0x{b.floor():03X}\n#define METATILE_AraunaInicio_Capim 0x{tall:03X}\n'+'#endif\n')
 reports['bank']={'reserved_metatile_ids':sorted(live),'preserved_metatile_ids':sorted(keep),'custom_metatile_ids':sorted(set(b.custom_ids)),'new_static_tile_slots':sorted(b.custom_tiles),'palettes_unchanged':True,'animation_slots_reserved':[432,511,992,1023],'short_grass_id':b.floor(),'tall_grass_id':tall}
 dump(ROOT/'review/inicio_geometria_v1/build.json',reports);print(json.dumps({k:v for k,v in reports.items() if k!='bank'},indent=2));print('new tiles',len(b.custom_tiles),'new metatiles',len(set(b.custom_ids)))
if __name__=='__main__':main()
