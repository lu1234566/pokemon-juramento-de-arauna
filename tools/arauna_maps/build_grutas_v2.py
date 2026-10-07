#!/usr/bin/env python3
"""Contextual draw-only cliffs, animated-water shores and clear Lanette floor."""
import collections,json,sys
from pathlib import Path
from PIL import Image,ImageDraw
from native_visuals_v2 import ROOT,BASE,Pair,dump,binary,marked
from bancos_nativos import resolve_bank
from render_native_map import words
from build_campanha_grutas_v1 import PARTS,WATER,FLOORS
OUT=ROOT/'review/grutas_bordas_v2'
WALLPAL={
 'victory':[(0,0,0),(24,40,48),(40,64,72),(64,88,96),(96,120,120),(128,152,152),(168,176,152),(200,200,160),(224,216,176),(240,232,192),(152,144,96),(80,112,120),(104,136,136),(128,88,32),(176,128,48),(208,160,64)],
 'seafloor':[(0,0,0),(16,16,24),(32,32,40),(48,48,56),(64,64,72),(80,88,88),(104,104,104),(128,128,120),(160,160,144),(184,176,152),(216,208,176),(240,232,192),(40,32,48),(96,80,64),(120,104,80),(152,136,96)]}
def pieces(f):
 atlas=Image.open(ROOT/f'art/campanha_grutas_v1/{f}_atlas.png').convert('RGBA');raw={}
 for i,n in enumerate(PARTS):
  y,x=divmod(i,4);im=atlas.crop((round(x*atlas.width/4)+8,round(y*atlas.height/4)+8,round((x+1)*atlas.width/4)-8,round((y+1)*atlas.height/4)-8));im.putdata([(r,g,b,0 if r>140 and b>140 and g<140 else 255) for r,g,b,a in im.getdata()]);raw[n]=im.crop(im.getbbox())
 face=raw['top'].resize((48,32),Image.Resampling.NEAREST);parts={'upper':face.crop((16,0,32,16)),'lower':face.crop((16,16,32,32)),'single':face.crop((16,0,32,32)).resize((16,16),Image.Resampling.NEAREST)}
 cap=raw['mass'].resize((32,32),Image.Resampling.NEAREST).crop((8,0,24,16));parts['plateau']=cap
 for n in ('left','right'):parts[n]=raw[n].resize((16,32),Image.Resampling.NEAREST).crop((0,8,16,24))
 out={};pal=WALLPAL[f]
 for n,im in parts.items():
  data=[]
  for r,g,b,a in im.getdata():data.append(0 if not a else min(range(1,16),key=lambda j:sum((u-v)**2 for u,v in zip((r,g,b),pal[j]))))
  idx=Image.new('L',(16,16));idx.putdata(data)
  if n=='plateau':idx.putdata([v or (8 if f=='victory' else 6) for v in idx.getdata()])
  if f=='victory' and n in ('single','lower'):
   # Preserve the concept's geological ochre band at the native pixel scale.
   d=ImageDraw.Draw(idx);row=12 if n=='single' else 9;d.line((0,row,15,row),fill=13);d.line((0,row+1,15,row+1),fill=14);d.line((0,row+2,15,row+2),fill=15)
  out[n]=idx
 return out
def reserve_all(pair,info,maps,layouts,base):
 names=[n for n,d in maps.items() if info in (layouts[d['layout']]['primary_tileset'],layouts[d['layout']]['secondary_tileset'])];pair.reserve(base,names,layouts,maps)
 for mid in range(len(pair.attrs[0])):pair.reserved.add(mid)
 # Named V1 IDs and saved-view aliases must remain native.
 return names
def main():
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);a=ap.parse_args();base=a.base.resolve();import subprocess
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
 node=json.loads((base/'data/layouts/layouts.json').read_text());layouts={l['id']:l for l in node['layouts']};maps={m['name']:m for p in (base/'data/maps').glob('*/map.json') for m in [json.loads(p.read_text())]};v1=json.loads((base/'review/campanha_grutas_v1/build.json').read_text());pairs={};report={'base_commit':BASE,'maps':{},'banks':{},'map_grids_unchanged':True};tables=[];counts=collections.Counter()
 for f in ('victory','seafloor'):
  group=[n for n,d in v1['maps'].items() if d['family']==f];art=pieces(f)
  for n in group:
   m=maps[n];l=layouts[m['layout']];key=tuple(l[k] for k in ('primary_tileset','secondary_tileset'))
   if key not in pairs:
    pair=Pair(base,l);pair.free=[i for i in pair.free if i>=512];pair.tile_cache={raw:i for i,raw in pair.tiles.items() if i>=512 and i not in pair.dynamic};pair.reserve(base,group,layouts,maps)
    for k,sym in enumerate(key):
     slug=v1['maps'][n]['primary' if k==0 else 'secondary'];pair.reserved.update(v1['banks'][slug]['required_ids']);pair.reserved.update(int(k) for k in v1['banks'][slug]['aliases']);pair.reserved.update(v1['banks'][slug]['aliases'].values())
    pair.pals[7]=WALLPAL[f]
    # Dedicated shore palette: dry floor, wet sand, foam and deep blue.
    pair.pals[12]=[(0,0,0),(232,224,184),(208,200,160),(184,176,136),(152,144,112),(112,104,80),(56,72,72),(8,48,64),(16,80,96),(24,112,128),(48,144,152),(96,176,176),(152,208,200),(200,232,216),(40,48,56),(80,88,88)]
    # Improve fallback wall art too; scripts continue to draw valid native IDs.
    for k,slug in enumerate((v1['maps'][n]['primary'],v1['maps'][n]['secondary'])):
     floor_mid=next(int(i) for i,role in v1['banks'][slug]['roles'].items() if role=='floor');e=pair.meta[k][floor_mid%512*8:floor_mid%512*8+4];floor=pair.reader.metatile(floor_mid).convert('RGB');idx=Image.new('L',(16,16));palette_slot=0 if not k else 6;idx.putdata([min(range(1,16),key=lambda j:sum((u-v)**2 for u,v in zip(rgb,pair.pals[palette_slot][j]))) for rgb in floor.getdata()])
     for mid,role in v1['banks'][slug]['roles'].items():
      if role=='solid' and k:pair.put(int(mid),idx,palette_slot,(art['single'],7))
    pairs[key]=pair
   pair=pairs[key];g=words(base/l['blockdata_filepath']);w,h=l['width'],l['height'];visual=[];roles={int(mid):role for slug in (v1['maps'][n]['primary'],v1['maps'][n]['secondary']) for mid,role in v1['banks'][slug]['roles'].items()};solid=lambda x,y:0<=x<w and 0<=y<h and roles.get(g[y*w+x]&1023)=='solid';water=lambda x,y:0<=x<w and 0<=y<h and (pair.attrs[(g[y*w+x]&1023)>=512][(g[y*w+x]&1023)%512]&255) in WATER
   for j,v in enumerate(g):
    x,y=j%w,j//w;mid=v&1023;k=mid>=512;entries=pair.meta[k][mid%512*8:mid%512*8+8];role=roles.get(mid,'floor');variant=None
    if role=='solid':
     if not solid(x,y+1):variant='lower' if solid(x,y-1) else 'single'
     elif not solid(x,y+2):variant='upper'
     elif not solid(x-1,y):variant='left'
     elif not solid(x+1,y):variant='right'
     else:variant='plateau'
     image=art[variant];entries=entries[:4]+pair.entries(image,7);counts[variant]+=1
    elif role=='water':
     overlay=Image.new('L',(16,16),0);d=ImageDraw.Draw(overlay);mask=0
     for bit,dx,dy in [(1,0,-1),(2,1,0),(4,0,1),(8,-1,0)]:
      xx,yy=x+dx,y+dy
      if 0<=xx<w and 0<=yy<h and not water(xx,yy) and roles.get(g[yy*w+xx]&1023) not in ('solid','void'):
       mask|=bit
       if bit==1:d.rectangle((0,0,15,2),fill=3);d.line((0,3,15,3),fill=6);d.line((0,4,15,4),fill=12)
       elif bit==2:d.rectangle((13,0,15,15),fill=3);d.line((12,0,12,15),fill=6);d.line((11,0,11,15),fill=12)
       elif bit==4:d.rectangle((0,13,15,15),fill=3);d.line((0,12,15,12),fill=6);d.line((0,11,15,11),fill=12)
       else:d.rectangle((0,0,2,15),fill=3);d.line((3,0,3,15),fill=6);d.line((4,0,4,15),fill=12)
     if mask:entries=entries[:4]+pair.entries(overlay,12);variant='shore';counts['shore']+=1
    elif role=='floor' and not v&0xc00:
     overlay=Image.new('L',(16,16),0);d=ImageDraw.Draw(overlay);edge=False
     for dx,dy,rect in [(0,-1,(0,0,15,1)),(1,0,(14,0,15,15)),(0,1,(0,14,15,15)),(-1,0,(0,0,1,15))]:
      if water(x+dx,y+dy):d.rectangle(rect,fill=5);edge=True
     if solid(x,y-1):d.line((0,0,15,0),fill=14);edge=True
     if edge:entries=entries[:4]+pair.entries(overlay,12);variant='wet_floor';counts['wet_floor']+=1
    alias=pair.alias(mid,entries) if variant else mid;visual.append(alias)
   tables.append((n,list(lay['id'] for lay in node['layouts']).index(l['id']),visual));report['maps'][n]={'cells':len(g),'visual_alias_cells':sum((v&1023)!=a for v,a in zip(g,visual)),'layout_index':tables[-1][1],'primary':str(pair.paths[0].relative_to(base)),'secondary':str(pair.paths[1].relative_to(base))};binary(OUT/'visual_grids'/f'{n}.bin',visual)
 # Lanette: a collision-free cell must read as open floor, even when its native
 # ID is reused by a desk/wall elsewhere. Door mats remain legible exits.
 n='Route114_LanettesHouse';m=maps[n];l=layouts[m['layout']];pair=Pair(base,l);reserve_all(pair,l['secondary_tileset'],maps,layouts,base);g=words(base/l['blockdata_filepath']);floor=pair.meta[1][(0x202-512)*8:(0x203-512)*8];door={(int(e['x']),int(e['y'])) for e in m['warp_events']};visual=[]
 for j,v in enumerate(g):
  mid=v&1023
  if not v&0xc00 and (j%l['width'],j//l['width']) not in door:mid=pair.alias(mid,floor)
  visual.append(mid)
 tables.append((n,list(lay['id'] for lay in node['layouts']).index(l['id']),visual));report['maps'][n]={'cells':len(g),'visual_alias_cells':sum((v&1023)!=a for v,a in zip(g,visual)),'all_free_cells_are_floor_except_marked_exit':True,'layout_index':tables[-1][1],'primary':str(pair.paths[0].relative_to(base)),'secondary':str(pair.paths[1].relative_to(base))};binary(OUT/'visual_grids'/f'{n}.bin',visual)
 # Do not rewrite Lanette's shared primary bank.
 pair.write([ROOT/p.relative_to(base) for p in pair.paths],kinds=(1,));pairs[tuple(l[k] for k in ('primary_tileset','secondary_tileset'))]=pair
 for key,pair in pairs.items():
  pair.write([ROOT/p.relative_to(base) for p in pair.paths],kinds=(1,));report['banks'][key[1]]={'primary':str(pair.paths[0].relative_to(base)),'secondary':str(pair.paths[1].relative_to(base)),'alias_count':len(pair.alias_cache),'new_static_graphics_slots':sorted(pair.touched),'original_callbacks':pair.callbacks}
 c='/* Generated by build_grutas_v2.py. Camera IDs only. */\n'
 for n,idx,grid in tables:c+=f'static const u16 sVisual_{n}[] = INCBIN_U16("review/grutas_bordas_v2/visual_grids/{n}.bin");\n'
 c+='static const struct CaveVisualGrid sCaveVisualGrids[] =\n{\n'+''.join(f'    {{{idx}, sVisual_{n}}}, // {n}\n' for n,idx,g in tables)+'};\n';(ROOT/'src/data/arauna_cave_visuals_v2.h').write_text(c)
 report['cliff_and_shore_cells']=dict(counts);dump(OUT/'grutas_build.json',report);print(json.dumps({'maps':len(tables),'cells_by_piece':dict(counts)},indent=2))
if __name__=='__main__':main()
