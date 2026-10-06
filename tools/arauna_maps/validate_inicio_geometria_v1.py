#!/usr/bin/env python3
"""Validate geography migration against an installed base checkout.

This checks semantic invariants, scene gate cuts, translated movement lanes,
neighbor RGB/behavior, safe hardware slots, and unchanged unrelated files.
"""
import argparse, collections, hashlib, json, re, struct, subprocess
from pathlib import Path
from render_native_map import Renderer, render_map, words
from bancos_nativos import resolve_bank
from connection_cache import rectangle

ROOT=Path(__file__).resolve().parents[2]
TARGETS=('LittlerootTown','Route101','OldaleTown')
GROUP=TARGETS+('Route102','Route103')
def read(root,n):return json.loads((root/f'data/maps/{n}/map.json').read_text())
def layouts(root):return {l['id']:l for l in json.loads((root/'data/layouts/layouts.json').read_text())['layouts']}
def bank(root,l):return Renderer(resolve_bank(root,l['primary_tileset']),resolve_bank(root,l['secondary_tileset']))
def attrs(r,i):return words((r.primary if i<512 else r.secondary)/'metatile_attributes.bin')[i%512]
def walk(g,w,h,seed,blocked=()):
 blocked=set(blocked);todo=[seed];seen=set()
 while todo:
  x,y=todo.pop()
  if (x,y) in seen or (x,y) in blocked or not (0<=x<w and 0<=y<h) or g[y*w+x]&0xc00:continue
  seen.add((x,y));todo.extend(((x+1,y),(x-1,y),(x,y+1),(x,y-1)))
 return seen
def invariant(m):
 m=json.loads(json.dumps(m));m.pop('layout')
 for section in ('object_events','warp_events','coord_events','bg_events'):
  for e in m.get(section,[]):e.pop('x');e.pop('y')
 return m
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);ap.add_argument('--output',type=Path,default=ROOT/'review/inicio_geometria_v1/validation.json');a=ap.parse_args()
 before=layouts(a.base);after=layouts(ROOT);report={'base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.base,text=True).strip(),'maps':{},'neighbors':{},'checks':[]}
 for n in TARGETS:
  old,new=read(a.base,n),read(ROOT,n);l=after[new['layout']];bl=before[old['layout']];r=bank(ROOT,l);br=bank(a.base,bl);g=words(ROOT/l['blockdata_filepath']);bg=words(a.base/bl['blockdata_filepath']);w,h=l['width'],l['height']
  assert invariant(old)==invariant(new),(n,'functional event data changed')
  assert (w,h)==(bl['width'],bl['height'])
  assert old['connections']==new['connections']
  for y in range(h):
   for x in range(w):
    if x in (0,w-1) or y in (0,h-1):assert g[y*w+x]&0xfc00==bg[y*w+x]&0xfc00,(n,'crossing flags changed',x,y)
  reachable=walk(g,w,h,(10,3) if n=='LittlerootTown' else (10,1) if n=='Route101' else (10,24))
  doors=[]
  for i,e in enumerate(new['warp_events']):
   x,y=e['x'],e['y'];raw=g[y*w+x];source=bg[old['warp_events'][i]['y']*w+old['warp_events'][i]['x']]
   assert raw==source,(n,'warp native ID/flags changed',i)
   assert attrs(r,raw&1023)==attrs(br,source&1023)
   assert (x,y) in reachable or (x,y+1) in reachable,(n,'door has no reachable approach',i)
   doors.append({'id':i,'from':[old['warp_events'][i]['x'],old['warp_events'][i]['y']],'to':[x,y]})
  for e in new['bg_events']:
   x,y=e['x'],e['y'];assert any(p in reachable for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1))),(n,'unreadable sign',x,y)
  for e in new['object_events']:
   if e['graphics_id'] in ('OBJ_EVENT_GFX_TRUCK','OBJ_EVENT_GFX_MOM'):continue
   assert (e['x'],e['y']) in reachable,(n,'blocked NPC anchor',e['x'],e['y'])
  report['maps'][n]={'dimensions':[w,h],'reachable_cells':len(reachable),'doors':doors,'collision_cells_changed':sum((x&0xc00)!=(y&0xc00) for x,y in zip(g,bg)),'native_behavior_cells_changed':sum(attrs(r,x&1023)!=attrs(br,y&1023) for x,y in zip(g,bg))}
  if n=='Route101':
   for y in range(19,28):
    for x in range(18):
     u,v=g[y*w+x],bg[y*w+x];assert u&0xfc00==v&0xfc00;assert attrs(r,u&1023)==attrs(br,v&1023),(n,'rescue behavior changed',x,y)
   triggers=[(e['x'],e['y']) for e in new['coord_events'] if e['var_value']=='2']
   locked=walk(g,w,h,(11,23),triggers)
   assert (12,24) in locked,'starter bag unreachable'
   assert all(y>=19 and x<18 for x,y in locked),'rescue escape gate can be bypassed'
   report['maps'][n]['rescue_gate_cut_cells']=len(locked)
  if n=='OldaleTown':
   # Trace the actual player/NPC movement sequences in all four interactions.
   text=(ROOT/'data/maps/OldaleTown/scripts.inc').read_text()
   def trace(label,start):
    body=re.search(r'^'+label+r':\n(.*?)(?=^\w|\Z)',text,re.M|re.S)[1];x,y=start
    result=[(x,y)]
    for cmd in re.findall(r'^\s*(walk_(?:fast_)?(?:up|down|left|right))\s*$',body,re.M):
     dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[cmd.split('_')[-1]];x+=dx;y+=dy;assert (x,y) in reachable,(label,'collision',x,y);result.append((x,y))
    return result
   pairs=[('South',(19,14),(19,15)),('North',(19,16),(19,15)),('East',(18,15),(19,15)),('West',(20,15),(19,15))]
   for direction,player,npc in pairs:
    trace('OldaleTown_Movement_Player'+direction,player);trace('OldaleTown_Movement_Employee'+('East' if direction=='West' else direction),npc)
   report['maps'][n]['potion_tour_directions_checked']=4
 for n in GROUP:
  m=read(ROOT,n);l=after[m['layout']];r=bank(ROOT,l);old=read(a.base,n);bl=before[old['layout']];br=bank(a.base,bl)
  if n not in TARGETS:
   assert m==old
   for f in ('blockdata_filepath','border_filepath'):assert (ROOT/l[f]).read_bytes()==(a.base/bl[f]).read_bytes()
   g=words(ROOT/l['blockdata_filepath']);assert all(attrs(r,v&1023)==attrs(br,v&1023) for v in g)
   assert render_map(r,ROOT/l['blockdata_filepath'],l['width'],l['height']).tobytes()==render_map(br,a.base/bl['blockdata_filepath'],bl['width'],bl['height']).tobytes(),(n,'neighbor RGB changed')
   report['neighbors'][n]={'cells_checked':len(g),'pixels_identical':True,'behavior_identical':True}
  for c in m['connections']:
   other=next(read(ROOT,p.parent.name) for p in (ROOT/'data/maps').glob('*/map.json') if json.loads(p.read_text())['id']==c['map']);ol=after[other['layout']]
   if other['name'] not in TARGETS:
    grid=words(ROOT/ol['blockdata_filepath'])
    for x,y in rectangle(l['width'],l['height'],ol['width'],ol['height'],c['offset'],c['direction']):
     mid=grid[y*ol['width']+x]&1023
     # Original receiver interpretation, including existing color differences,
     # must remain identical after the scoped bank allocation.
     assert r.metatile(mid).tobytes()==br.metatile(mid).tobytes(),(n,'incoming border changed',mid)
 b=json.loads((ROOT/'review/inicio_geometria_v1/build.json').read_text())['bank']
 assert not set(b['new_static_tile_slots'])&set(range(432,512))
 assert not set(b['new_static_tile_slots'])&set(range(992,1024))
 rr=bank(ROOT,after[read(ROOT,'LittlerootTown')['layout']])
 for mid in b['custom_metatile_ids']:
  meta=rr.primary_metatiles if mid<512 else rr.secondary_metatiles
  for entry in meta[(mid%512)*8:(mid%512)*8+8]:
   tid=entry&1023;assert tid<432 or 512<=tid<992,('new artwork uses an animated slot',mid,tid)
 for kind,slug,original in [('primary','arauna_inicio_base_v1','general'),('secondary','arauna_inicio_sul_v1','arauna_amanhecer')]:
  for i in range(16):assert (ROOT/f'data/tilesets/{kind}/{slug}/palettes/{i:02}.pal').read_bytes()==(a.base/f'data/tilesets/{kind}/{original}/palettes/{i:02}.pal').read_bytes()
 # All target scripts remain exact, except the declared coordinate translation.
 for n in TARGETS:
  x=(a.base/f'data/maps/{n}/scripts.inc').read_text();y=(ROOT/f'data/maps/{n}/scripts.inc').read_text()
  if n=='OldaleTown':x=x.replace('LOCALID_OLDALE_MART_EMPLOYEE, 24, 13','LOCALID_OLDALE_MART_EMPLOYEE, 19, 15')
  assert x==y,(n,'script logic changed')
 old_heals=json.loads((a.base/'src/data/heal_locations.json').read_text());new_heals=json.loads((ROOT/'src/data/heal_locations.json').read_text())
 for e in old_heals['heal_locations']:
  if e['id']=='HEAL_LOCATION_OLDALE_TOWN':e.update(x=7,y=20)
 assert old_heals==new_heals
 import csv
 path='docs/arauna/ARAUNA_OVERWORLD_PLACEMENT.csv'
 old_rows=list(csv.DictReader((a.base/path).open()));new_rows=list(csv.DictReader((ROOT/path).open()))
 for row in old_rows:
  if row['map']=='Route101' and row['channel']=='B':row.update(x='13',y='11')
 assert old_rows==new_rows,'creature registry drift'
 allowed={'data/layouts/layouts.json','src/data/heal_locations.json','src/overworld.c','src/fldeff_cut.c','data/maps/OldaleTown/scripts.inc',path}|{f'data/maps/{n}/map.json' for n in TARGETS}|{f'src/data/tilesets/{n}.h' for n in ('graphics','headers','metatiles')}
 protected=subprocess.check_output(['git','ls-files','data','src','include','graphics'],cwd=a.base,text=True).splitlines();count=0
 for p in protected:
  if p in allowed:continue
  assert (a.base/p).read_bytes()==(ROOT/p).read_bytes(),('unrelated file changed',p);count+=1
 report['protected_files_unchanged']=count
 # Compile the actual migration routine on the host, including all legacy
 # walkable cells and cases that must never migrate (new/unrelated layouts).
 import ctypes,tempfile
 source=(ROOT/'src/overworld.c').read_text()
 routine=re.search(r'^static bool8 AraunaMigrateInitialMapSave\(void\)\n\{.*?^\}',source,re.M|re.S)[0]
 # mapjson assigns IDs in layouts.json order (1-based). Read the source
 # directly so this validator also works before generated headers/builds.
 ids={k:i+1 for i,k in enumerate(after)}
 with tempfile.TemporaryDirectory() as temp:
  p=Path(temp);decl=''.join(f'#define {k} {ids[k]}\n' for k in set(re.findall(r'LAYOUT_\w+',routine)))
  bridge='''#include <stdint.h>
#include <stdlib.h>
typedef int32_t s32; typedef uint16_t u16; typedef uint8_t bool8;
#define TRUE 1
#define FALSE 0
#define MAPGRID_COLLISION_MASK 0xc00
struct MapLayout {int width,height; const u16 *map;};
struct Save {u16 mapLayoutId; struct {int x,y;}pos;};
static struct Save save,*gSaveBlock1Ptr=&save;
static struct {u16 mapLayoutId;const struct MapLayout *mapLayout;}gMapHeader;
static void SetCurrentMapLayout(u16 id){save.mapLayoutId=id;}
'''+decl+routine+'''
int run(int old,int next,int x,int y,int w,int h,u16 *grid,int *out){
 struct MapLayout layout={w,h,grid};save.mapLayoutId=old;save.pos.x=x;save.pos.y=y;
 gMapHeader.mapLayoutId=next;gMapHeader.mapLayout=&layout;
 int moved=AraunaMigrateInitialMapSave();out[0]=save.mapLayoutId;out[1]=save.pos.x;out[2]=save.pos.y;return moved;
}
'''
  (p/'bridge.c').write_text(bridge);subprocess.run(['cc','-shared','-fPIC','-Wall','-Wextra','-Werror',str(p/'bridge.c'),'-o',str(p/'migration.so')],check=True)
  dll=ctypes.CDLL(str(p/'migration.so'));f=dll.run;f.argtypes=[ctypes.c_int]*6+[ctypes.POINTER(ctypes.c_uint16),ctypes.POINTER(ctypes.c_int)];f.restype=ctypes.c_int
  checked=relocated=0
  for n in TARGETS:
   old=read(a.base,n);new=read(ROOT,n);l=after[new['layout']];g=words(ROOT/l['blockdata_filepath']);bg=words(a.base/before[old['layout']]['blockdata_filepath']);w,h=l['width'],l['height'];arr=(ctypes.c_uint16*len(g))(*g);out=(ctypes.c_int*3)();free=[(i%w,i//w) for i,v in enumerate(g) if not v&0xc00]
   for i,v in enumerate(bg):
    if v&0xc00:continue
    x,y=i%w,i//w;assert f(ids[old['layout']],ids[new['layout']],x,y,w,h,arr,out)==1
    assert out[0]==ids[new['layout']] and not g[out[2]*w+out[1]]&0xc00
    if not g[i]&0xc00:assert (out[1],out[2])==(x,y)
    else:
     assert abs(out[1]-x)+abs(out[2]-y)==min(abs(xx-x)+abs(yy-y) for xx,yy in free);relocated+=1
    checked+=1
   for old_id,new_id in [(ids[new['layout']],ids[new['layout']]),(0,ids[new['layout']]),(ids[old['layout']],0)]:
    assert f(old_id,new_id,10,1,w,h,arr,out)==0 and tuple(out)==(old_id,10,1)
  report['save_migration']={'legacy_walkable_positions_checked':checked,'positions_relocated_to_nearest_floor':relocated,'new_and_unrelated_caches_untouched':True,'real_c_routine_compiled':True}
 # Exercise the real Cut selector, including all IDs in every other bank.
 cut=(ROOT/'src/fldeff_cut.c').read_text();oldcut=(a.base/'src/fldeff_cut.c').read_text()
 pattern=r'^static void SetCutGrassMetatile\(s16 x, s16 y\)\n\{.*?^\}'
 current=re.search(pattern,cut,re.M|re.S)[0];original=re.search(pattern,oldcut,re.M|re.S)[0].replace('SetCutGrassMetatile','OriginalCut')
 with tempfile.TemporaryDirectory() as temp:
  p=Path(temp);bridge='''#include <stdint.h>
#include "constants/metatile_labels.h"
#include "constants/arauna_inicio_metatiles.h"
typedef int16_t s16; typedef uint16_t u16;
struct Tileset {int unused;};
const struct Tileset gTileset_AraunaInicioBaseV1={0},other={1};
static struct {const struct Tileset *primaryTileset;}layout;
static struct {typeof(layout) *mapLayout;}gMapHeader={&layout};
static u16 cell;
static u16 MapGridGetMetatileIdAt(s16 x,s16 y){(void)x;(void)y;return cell;}
static void MapGridSetMetatileIdAt(s16 x,s16 y,u16 id){(void)x;(void)y;cell=id;}
'''+current+original+'''
int run(int mid,int scoped,int before){cell=mid;layout.primaryTileset=scoped?&gTileset_AraunaInicioBaseV1:&other;if(before)OriginalCut(0,0);else SetCutGrassMetatile(0,0);return cell;}
'''
  (p/'cut.c').write_text(bridge);subprocess.run(['cc','-shared','-fPIC','-Wall','-Wextra','-Werror','-I'+str(ROOT/'include'),str(p/'cut.c'),'-o',str(p/'cut.so')],check=True)
  dll=ctypes.CDLL(str(p/'cut.so'));f=dll.run;f.argtypes=[ctypes.c_int]*3;f.restype=ctypes.c_int
  for mid in range(1024):assert f(mid,0,0)==f(mid,0,1),('foreign bank Cut changed',mid)
  assert f(b['tall_grass_id'],1,0)==b['short_grass_id']
  assert rr._tile(rr.secondary_metatiles[(b['short_grass_id']-512)*8]&1023) is not None
 report['cut']={'foreign_metatile_ids_unchanged':1024,'custom_capim_becomes_custom_campo':True,'real_c_selector_compiled':True}
 report['checks']=['event identities/flags/warp destinations unchanged','connections/dimensions/crossing flags unchanged','all warp approaches and signs reachable','rescue collision/behavior staging exact and gate cut closed','four potion tour movement lanes open','Route102/103 grids, RGB and behaviors exact','incoming unchanged-neighbor strips exact','palette bytes and animation slots protected','script logic unchanged; heal point migrated']
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
