#!/usr/bin/env python3
"""Check seven native interiors, event access, special metatiles and Wingull."""
import collections,json,struct
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
NAMES=[f'MossdeepCity_House{i}' for i in range(1,5)]+['MossdeepCity_Mart','MossdeepCity_PokemonCenter_1F','MossdeepCity_PokemonCenter_2F']
BANK=ROOT/'data/tilesets/secondary/arauna_missoes_ceu_interiors_v1'
SYMBOL='AraunaMissoesCeuInteriorsV1'
def words(p):
 raw=p.read_bytes();assert len(raw)%2==0
 return struct.unpack('<%dH'%(len(raw)//2),raw)
def reach(grid,w,h,start,objects):
 blocked={(i%w,i//w) for i,v in enumerate(grid) if v&0x400}|objects
 assert start not in blocked,('blocked entry',start)
 seen={start};q=collections.deque([start])
 while q:
  x,y=q.popleft()
  for pos in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
   if 0<=pos[0]<w and 0<=pos[1]<h and pos not in blocked and pos not in seen:seen.add(pos);q.append(pos)
 return seen
def adjacent(seen,p):
 x,y=p;return bool(seen & {(x+1,y),(x-1,y),(x,y+1),(x,y-1)})
def main():
 l={x['id']:x for x in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
 art=Image.open(BANK/'tiles.png');assert art.size==(128,256) and art.mode=='P' and len(set(art.tobytes()))<=16
 attrs=words(BANK/'metatile_attributes.bin')
 assert len(attrs)<=512
 expected={
  'MossdeepCity_House1':(2,2,12,11), 'MossdeepCity_House2':(2,3,10,9),
  'MossdeepCity_House3':(2,1,12,11),'MossdeepCity_House4':(2,3,12,11),
  'MossdeepCity_Mart':(2,4,12,11),'MossdeepCity_PokemonCenter_1F':(3,3,14,9),
  'MossdeepCity_PokemonCenter_2F':(3,5,14,10)}
 report={}
 for name in NAMES:
  e=json.loads((ROOT/'data/maps'/name/'map.json').read_text());rec=l[e['layout']]
  nw,no,w,h=expected[name]
  assert rec['secondary_tileset']=='gTileset_'+SYMBOL and (rec['width'],rec['height'])==(w,h)
  assert len(e['warp_events'])==nw and len(e['object_events'])==no
  grid=words(ROOT/rec['blockdata_filepath']);assert len(grid)==w*h
  assert all((v&0x3ff)>=0x200 and (v&0x3ff)-0x200<len(attrs) for v in grid)
  npcs={(x['x'],x['y']) for x in e['object_events']}
  if name.endswith('House2'):
   before=words(ROOT/'data/layouts/House1/map.bin')
   assert all((a&~0x3ff)==(b&~0x3ff) for a,b in zip(before,grid))
   assert [(x['x'],x['y']) for x in e['object_events']]==[(6,6),(4,4),(4,5)]
   assert [(x['x'],x['y']) for x in e['warp_events']]==[(3,8),(4,8)]
   script=(ROOT/'data/maps'/name/'scripts.inc').read_text()
   assert 'MossdeepCity_House2_Movement_WingullExitNorth' in script
   assert 'MossdeepCity_House2_Movement_WingullExitEast' in script
  if 'PokemonCenter' in name:
   assert [x['x'] for x in e['warp_events']]==([7,6,1] if name.endswith('1F') else [1,5,9])
   original_attrs=words(ROOT/'data/tilesets/secondary/pokemon_center/metatile_attributes.bin')
   assert all(attrs[mid-512]==original_attrs[mid-512] for mid in
              (0x280,0x281,0x288,0x289,0x290,0x291,0x298,0x299,0x2a0,0x2a1,0x2a8,0x2a9))
  if name.endswith('2F'):
   assert grid[1*w+5]&0x3ff==0x264 and grid[1*w+9]&0x3ff==0x264
   for x in (5,9):assert grid[2*w+x]&0x3ff==0x21e and grid[3*w+x]&0x3ff==0x25d
  objects=npcs
  start=(e['warp_events'][0]['x'],e['warp_events'][0]['y']-1)
  seen=reach(grid,w,h,start,objects)
  for warp in e['warp_events']:
   pos=(warp['x'],warp['y'])
   if name.endswith('2F') and pos in ((5,1),(9,1)):
    opened=list(grid)
    for y in (2,3):opened[y*w+pos[0]] &= ~0x400
    later=reach(opened,w,h,start,objects)
    assert pos in later or adjacent(later,pos),(name,'opened link warp',pos)
    continue
   assert pos in seen or adjacent(seen,pos),(name,'warp',pos)
  for npc in e['object_events']:
   pos=(npc['x'],npc['y']);assert adjacent(seen,pos),(name,'npc',pos)
  report[name]={'size':[w,h],'reachable':len(seen),'warps':nw,'npcs':no}
 for file in ('graphics.h','metatiles.h','headers.h'):
  text=(ROOT/'src/data/tilesets'/file).read_text()
  assert text.count('// MISSOES_CEU_INTERIORS_V1_BEGIN')==text.count('// MISSOES_CEU_INTERIORS_V1_END')==1
  assert SYMBOL in text
 print(json.dumps({'status':'PASS','maps':report,'palette_entries_used':len(set(art.tobytes())),
                   'wingull_path_preserved':True,'center_special_metatiles_preserved':True},indent=2))
if __name__=='__main__':main()
