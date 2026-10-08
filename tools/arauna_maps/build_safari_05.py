#!/usr/bin/env python3
"""Eight Safari maps, private native banks, original IDs and original grids."""
import argparse,json,subprocess
from pathlib import Path
from native_visuals_v2 import Pair,dump,declarations,marked
from safari_05_common import BASE,ROOT,OUT,GROUPS,inventory
from safari_05_art import GROUND,WOOD,SHALLOWS,floor,grass,tree_piece,recolor_palettes,wall,pond,shallows
from render_native_map import words

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve()
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
 node,ls,maps=inventory(base);report={'base_commit':BASE,'maps':{},'banks':{}};decl={k:'' for k in ('graphics.h','metatiles.h','headers.h')}
 for theme,names in GROUPS.items():
  first=ls[maps[names[0]]['layout']];p=Pair(base,first,repack=True)
  p.pals=recolor_palettes(p.pals,theme);used={v&1023 for n in names for f in ('blockdata_filepath','border_filepath') for v in words(base/ls[maps[n]['layout']][f])};redrawn=[]
  if theme=='mata':
   p.pals[6]=GROUND;p.pals[12]=SHALLOWS
   p.pals[2][1:5]=[(144,176,104),(104,144,72),(48,88,48),(32,48,24)]
   p.pals[2][12]=(192,160,104);p.pals[2][13]=GROUND[5];p.pals[3][15]=GROUND[5]
   for mid in (1,0xd3,0xd4,0x1ce,0x1cf):p.put(mid,floor('ground',mid%3),6);redrawn.append(mid)
   p.put(0xd,grass(),6);redrawn.append(0xd)
   for row,ids in enumerate(((0x1d4,0x1d5,0x1d6,0x1d7),(0x1dc,0x1dd,0x1de,0x1df),(0x1e4,0x1e5,0x1e6,0x1e7))):
    for k,mid in enumerate(ids):p.put(mid,tree_piece(k%2,0 if row==0 else 1,bottom=row==2),6);redrawn.append(mid)
   # Native stairs, rails, feeders and roofs keep their silhouettes and layers.
   p.put(0x121,floor('path'),6);redrawn.append(0x121)
   p.put(0xb1,pond(),0);redrawn.append(0xb1)
   for mid in (0xc9,0xd1):p.put(mid,shallows(),12);redrawn.append(mid)
  elif theme=='pouso':
   p.pals[12]=WOOD
   p.pals[6][5:10]=[(136,104,64),(160,128,80),(104,80,56),(120,96,56),(184,152,104)]
   for mid,lower in ((0x205,False),(0x20d,True)):p.put(mid,wall(lower),12);redrawn.append(mid)
   # Floor ID 0x223 is the inherited plank floor; wall/furniture footprints stay native.
   for mid in used:
    if mid==0:continue
    if mid in (0x223,0x224):p.put(mid,floor('wood'),12);redrawn.append(mid)
  else:
   p.pals[11]=WOOD
   # Existing entrance already uses bespoke Arauna assets. Warm its native floor,
   # retaining the counter, fern, door, and Pokeblock information board.
   for mid in used:
    if mid<512:continue
    entries=p.meta[1][(mid-512)*8:(mid-512)*8+8]
    if all(e>>12==11 for e in entries[:4]) and all((e&1023)==0 for e in entries[4:]):
     p.put(mid,floor('wood'),11);redrawn.append(mid)
  paths=[ROOT/f'data/tilesets/{kind}/arauna_safari05_{theme}' for kind in ('primary','secondary')];syms=['AraunaSafari05'+theme.title()+suffix for suffix in ('Base','Art')]
  p.write(paths);d=declarations(paths,syms,p.callbacks)
  for k,v in d.items():decl[k]+=v
  for n in names:
   l=ls[maps[n]['layout']];idx=node['layouts'].index(l);l['primary_tileset']='gTileset_'+syms[0];l['secondary_tileset']='gTileset_'+syms[1]
   report['maps'][n]={'layout_index':idx,'theme':theme,'cells':l['width']*l['height'],'native_ids_used':sorted(v&1023 for v in words(base/l['blockdata_filepath'])),'draw_selector':'native ID, no new aliases'}
  report['banks'][theme]={'paths':[p.relative_to(ROOT).as_posix() for p in paths],'source_paths':[p.relative_to(base).as_posix() for p in p.paths],'symbols':syms,'callbacks':p.callbacks,'allocated_static_tiles':sorted(p.touched),'redrawn_native_ids':redrawn,'original_attribute_counts':list(map(len,p.attrs))}
 for k,v in decl.items():marked(ROOT/'src/data/tilesets'/k,'SAFARI_05',v)
 dump(ROOT/'data/layouts/layouts.json',node);dump(OUT/'build.json',report)
 print(json.dumps({'maps':len(report['maps']),'banks':{k:{'allocated_tiles':len(v['allocated_static_tiles']),'redrawn_ids':len(v['redrawn_native_ids'])} for k,v in report['banks'].items()}}))

if __name__=='__main__':main()
