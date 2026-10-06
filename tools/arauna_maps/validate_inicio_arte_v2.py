#!/usr/bin/env python3
"""Compare the cosmetic correction with installed Início Composição V1."""
import argparse, ctypes, json, re, subprocess, tempfile
from pathlib import Path
from PIL import Image
from render_native_map import Renderer, words, render_map
from bancos_nativos import resolve_bank
from connection_cache import rectangle
ROOT=Path(__file__).resolve().parents[2]
TARGETS={'LittlerootTown','Route101','OldaleTown'}
GROUP=TARGETS|{'Route102','Route103'}
def read(root,path):return json.loads((root/path).read_text())
def layouts(root):return {l['id']:l for l in read(root,'data/layouts/layouts.json')['layouts']}
def renderer(root,l):return Renderer(resolve_bank(root,l['primary_tileset']),resolve_bank(root,l['secondary_tileset']))
def behavior(r,mid):return words((r.primary if mid<512 else r.secondary)/'metatile_attributes.bin')[mid%512]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);ap.add_argument('--output',type=Path,default=ROOT/'review/inicio_arte_v2/validation.json');a=ap.parse_args();base=a.base.resolve()
 assert read(ROOT,'data/layouts/layouts.json')==read(base,'data/layouts/layouts.json'),'layout IDs or definitions changed'
 ls=layouts(ROOT);ms={m['id']:m for p in (ROOT/'data/maps').glob('*/map.json') for m in [read(ROOT,str(p.relative_to(ROOT))) ]}
 for p in (ROOT/'data/maps').glob('*/map.json'):assert p.read_bytes()==(base/p.relative_to(ROOT)).read_bytes(),p
 for p in (ROOT/'data/maps').glob('*/scripts.inc'):assert p.read_bytes()==(base/p.relative_to(ROOT)).read_bytes(),p
 for p in ('src/overworld.c','src/fldeff_cut.c','src/data/heal_locations.json','docs/arauna/ARAUNA_OVERWORLD_PLACEMENT.csv'):
  assert (ROOT/p).read_bytes()==(base/p).read_bytes(),p
 for l in ls.values():
  for key in ('blockdata_filepath','border_filepath'):
   if 'Arauna' not in l['name'] or l['id'] not in {ms['MAP_'+re.sub(r'([a-z])([A-Z])',r'\1_\2',n).upper()]['layout'] for n in TARGETS}:
    assert (ROOT/l[key]).read_bytes()==(base/l[key]).read_bytes(),l[key]
 report={'base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip(),'map_jsons_identical':len(ms),'maps':{},'borders':[]}
 cache={}
 def bank(root,l):
  k=(root,l['primary_tileset'],l['secondary_tileset'])
  if k not in cache:cache[k]=renderer(root,l)
  return cache[k]
 for n in sorted(GROUP):
  m=next(m for m in ms.values() if m['name']==n);l=ls[m['layout']];r=bank(ROOT,l);br=bank(base,l);g=words(ROOT/l['blockdata_filepath']);bg=words(base/l['blockdata_filepath'])
  assert len(g)==len(bg)
  assert all(u&0xfc00==v&0xfc00 for u,v in zip(g,bg)),(n,'collision/elevation changed')
  assert all(behavior(r,u&1023)==behavior(br,v&1023) for u,v in zip(g,bg)),(n,'behavior changed')
  report['maps'][n]={'cells_checked':len(g),'collision_elevation_behavior_identical':True}
  if n not in TARGETS:
   assert render_map(r,ROOT/l['blockdata_filepath'],l['width'],l['height']).tobytes()==render_map(br,base/l['blockdata_filepath'],l['width'],l['height']).tobytes(),(n,'RGB changed')
   report['maps'][n]['RGB_identical']=True
 # Audit actual receiving-bank RGB, following each source grid's IDs.
 for m in sorted(ms.values(),key=lambda m:m["name"]):
  for c in m['connections'] or []:
   other=ms[c['map']]
   if m['name'] not in GROUP and other['name'] not in GROUP:continue
   l=ls[m['layout']];ol=ls[other['layout']];r=bank(ROOT,l);br=bank(base,l)
   g=words(ROOT/ol['blockdata_filepath']);bg=words(base/ol['blockdata_filepath']);checked=changed=errors_before=errors_after=0
   sr=bank(ROOT,ol);bsr=bank(base,ol)
   for x,y in rectangle(l['width'],l['height'],ol['width'],ol['height'],c['offset'],c['direction']):
    i=y*ol['width']+x
    now=r.metatile(g[i]&1023).tobytes();before=br.metatile(bg[i]&1023).tobytes()
    errors_before+=before!=bsr.metatile(bg[i]&1023).tobytes()
    errors_after+=now!=sr.metatile(g[i]&1023).tobytes()
    if now!=before:
     assert other['name'] in TARGETS and now==sr.metatile(g[i]&1023).tobytes(),(m['name'],other['name'],'unintended border change',x,y)
     changed+=1
    checked+=1
   assert errors_after<=errors_before,(m['name'],other['name'],'border regression')
   report['borders'].append({'from':m['name'],'to':other['name'],'cells_checked':checked,'corrected_object_cells':changed,'wrong_drawing_cells_before':errors_before,'wrong_drawing_cells_after':errors_after})
 b=read(ROOT,'review/inicio_geometria_v1/build.json')['bank'];r=bank(ROOT,ls[ms['MAP_LITTLEROOT_TOWN']['layout']])
 floor=r.primary_metatiles if b['short_grass_id']<512 else r.secondary_metatiles
 floor=floor[(b['short_grass_id']%512)*8:(b['short_grass_id']%512)*8+4]
 layered=[]
 for mid in b['custom_metatile_ids']:
  arr=r.primary_metatiles if mid<512 else r.secondary_metatiles;entries=arr[(mid%512)*8:(mid%512)*8+8]
  for e in entries:assert e>>12<=12 and ((e&1023)<432 or 512<=e&1023<992),(mid,'unsafe slot or palette')
  if entries[:4]==floor and any(e&1023 for e in entries[4:]):layered.append(mid)
 assert layered,'no grass/object layers found'
 report['layered_object_metatiles_with_exact_grass_bottom']=len(layered)
 for kind,slug in [('primary','arauna_inicio_base_v1'),('secondary','arauna_inicio_sul_v1')]:
  for i in range(16):assert (ROOT/f'data/tilesets/{kind}/{slug}/palettes/{i:02}.pal').read_bytes()==(base/f'data/tilesets/{kind}/{slug}/palettes/{i:02}.pal').read_bytes()
 im=Image.open(ROOT/'graphics/door_anims/arauna_inicio_madeira_v2.png');assert im.mode=='P' and im.size==(16,96) and 0<min(im.getdata())<=max(im.getdata())<=15
 assert len({im.crop((0,i*32,16,(i+1)*32)).tobytes() for i in range(3)})==3,'duplicate animation frames'
 # Host-compile the real graphics selector; all foreign bank IDs must keep
 # their previous graphics and sound. Only the two scoped doors can differ.
 source=(ROOT/'src/field_door.c').read_text();old=(base/'src/field_door.c').read_text()
 pattern=r'^static const struct DoorGraphics \*GetDoorGraphics\(.*?^\}'
 routine=re.search(pattern,source,re.M|re.S)[0];original=re.search(pattern,old,re.M|re.S)[0].replace('GetDoorGraphics','OriginalDoorGraphics')
 table=re.search(r'^static const struct DoorGraphics sDoorAnimGraphicsTable\[\] =\n\{.*?^\};',source,re.M|re.S)[0]
 scoped=re.search(r'^static const struct DoorGraphics sDoorGraphics_AraunaInicioMadeira =\n\{.*?^\};',source,re.M|re.S)[0]
 names=set(re.findall(r'sDoorAnim(?:Tiles|Palettes)_\w+',table+scoped))
 bridge='''#include <stdint.h>\n#include <stddef.h>\n#include "constants/metatile_labels.h"\ntypedef uint8_t u8;typedef uint16_t u16;\n#define DOOR_SOUND_NORMAL 0\n#define DOOR_SOUND_SLIDING 1\n#define DOOR_SOUND_ARENA 2\nstruct DoorGraphics {u16 metatileNum;u8 sound,size;const void *tiles,*palettes;};\nstruct Tileset{int unused;};\nconst struct Tileset gTileset_AraunaInicioBaseV1={0},other={1};\nstatic struct {const struct Tileset *primaryTileset;}layout;\nstatic struct {typeof(layout)*mapLayout;}gMapHeader={&layout};\n'''+''.join(f'static const u8 {n}[]={{1}};\n' for n in names)+table+scoped+routine+original+'''
int run(int mid,int owned,int before){layout.primaryTileset=owned?&gTileset_AraunaInicioBaseV1:&other;const struct DoorGraphics *p=before?OriginalDoorGraphics(sDoorAnimGraphicsTable,mid):GetDoorGraphics(sDoorAnimGraphicsTable,mid);if(!p)return -1;if(p==&sDoorGraphics_AraunaInicioMadeira)return 1000;return (int)(p-sDoorAnimGraphicsTable);}
'''
 with tempfile.TemporaryDirectory() as temp:
  p=Path(temp);(p/'door.c').write_text(bridge);subprocess.run(['cc','-shared','-fPIC','-Wall','-Wextra','-Werror','-I'+str(ROOT/'include'),str(p/'door.c'),'-o',str(p/'door.so')],check=True)
  dll=ctypes.CDLL(str(p/'door.so'));f=dll.run;f.argtypes=[ctypes.c_int]*3;f.restype=ctypes.c_int
  for mid in range(1024):
   assert f(mid,0,0)==f(mid,0,1),('foreign door changed',mid)
   assert f(mid,1,0)==(1000 if mid in (0x61,0x41) else f(mid,1,1)),('scoped door mismatch',mid)
 report['door_selector']={'real_C_compiled':True,'foreign_ids_unchanged':1024,'scoped_ids_checked':1024,'distinct_opaque_animation_frames':3}
 report['save_routine_and_continue_warp_priority_identical_to_installed_base']=True
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
