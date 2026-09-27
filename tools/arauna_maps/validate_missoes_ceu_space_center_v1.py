#!/usr/bin/env python3
"""Verify native 4bpp bank, unchanged scripted topology, warps, and registrations."""
import collections,json,re,struct
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
NAMES=['MossdeepCity_SpaceCenter_1F','MossdeepCity_SpaceCenter_2F']
BANK=ROOT/'data/tilesets/secondary/arauna_missoes_ceu_space_center_v1'
SYMBOL='AraunaMissoesCeuSpaceCenterV1'

def words(p):
 b=p.read_bytes();assert len(b)%2==0
 return struct.unpack('<%dH'%(len(b)//2),b)
def reachable(grid,start,npcs):
 blocked={(i%16,i//16) for i,v in enumerate(grid) if v&0x400}|npcs
 assert start not in blocked
 seen={start};q=collections.deque([start])
 while q:
  x,y=q.popleft()
  for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
   if 0<=p[0]<16 and 0<=p[1]<10 and p not in blocked and p not in seen:
    seen.add(p);q.append(p)
 return seen
def main():
 layouts={x['id']:x for x in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
 facility=words(ROOT/'data/tilesets/secondary/facility/metatile_attributes.bin')
 attrs=words(BANK/'metatile_attributes.bin')
 png=Image.open(BANK/'tiles.png')
 assert png.mode=='P' and png.size==(128,256) and png.info.get('bits',4)==4
 assert len(set(png.tobytes()))<=16
 for mid in (0x206,0x207,0x2bc,0x2cc):assert attrs[mid-512]==facility[mid-512]
 reports={}
 for name in NAMES:
  floor=name[-2:];layout=layouts['LAYOUT_MOSSDEEP_CITY_SPACE_CENTER_'+floor]
  old=words(ROOT/'data/layouts'/name/'map.bin');new=words(ROOT/layout['blockdata_filepath'])
  assert len(old)==len(new)==160 and (layout['width'],layout['height'])==(16,10)
  assert layout['secondary_tileset']=='gTileset_'+SYMBOL
  assert all((a&~0x3ff)==(b&~0x3ff) for a,b in zip(old,new))
  assert all((v&0x3ff)>=0x200 and (v&0x3ff)-0x200<len(attrs) for v in new)
  assert new[1*16+13]&0x3ff==(0x2bc if floor=='1F' else 0x2cc)
  if floor=='1F':assert [new[9*16+x]&0x3ff for x in (7,8)]==[0x206,0x207]
  event=json.loads((ROOT/'data/maps'/name/'map.json').read_text())
  assert event['layout']==layout['id']
  npcs={(e['x'],e['y']) for e in event['object_events']}
  # Some grunts temporarily stand directly before the staircase. Compare
  # static traversal with the actors hidden, as in the post-event state.
  seen=reachable(new,(8,8) if floor=='1F' else (13,5),set())
  for warp in event['warp_events']:
   x,y=warp['x'],warp['y']
   assert (x,y) in seen or bool(seen & {(x-1,y),(x+1,y),(x,y-1),(x,y+1)})
  assert all(bool(seen & {(x-1,y),(x+1,y),(x,y-1),(x,y+1)}) for x,y in npcs if (x,y) not in seen)
  script=(ROOT/'data/maps'/name/'scripts.inc').read_text()
  for match in re.finditer(r'(?:setobjectxyperm|setobjectxy)\s+\w+,\s*(\d+),\s*(\d+)',script):
   x,y=map(int,match.groups());assert 0<=x<16 and 0<=y<10
  reports[name]={'changed_cells':sum(a!=b for a,b in zip(old,new)),'reachable':len(seen),'warps':len(event['warp_events'])}
 for file in ('graphics.h','metatiles.h','headers.h'):
  text=(ROOT/'src/data/tilesets'/file).read_text()
  assert text.count('// MISSOES_CEU_SPACE_CENTER_V1_BEGIN')==1
  assert text.count('// MISSOES_CEU_SPACE_CENTER_V1_END')==1
  assert SYMBOL in text
 print(json.dumps({'status':'PASS','maps':reports,'palette_entries_used':len(set(png.tobytes())),
                   'collision_elevation_and_warp_behaviors_preserved':True},indent=2))
if __name__=='__main__':main()
