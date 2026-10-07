#!/usr/bin/env python3
"""Host-execute the actual migration and Cut C routines."""
import argparse,ctypes,json,re,subprocess,tempfile
from pathlib import Path
from native_visuals_v2 import ROOT,dump
from build_sul_pampa_v1 import BASE,TARGETS
from render_native_map import words

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);a=ap.parse_args();base=a.base.resolve();assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
 layouts=[json.loads((p/'data/layouts/layouts.json').read_text())['layouts'] for p in (base,ROOT)];ls=[{l['id']:l for l in ll} for ll in layouts];ids={l['id']:i+1 for i,l in enumerate(layouts[1])};art=json.loads((ROOT/'review/sul_pampa_v1/art_build.json').read_text());source=(ROOT/'src/overworld.c').read_text();routine=re.search(r'^static bool8 AraunaMigrateInitialMapSave\(void\)\n\{.*?^\}',source,re.M|re.S)[0]
 decl=''.join(f'#define {k} {ids[k]}\n' for k in set(re.findall(r'LAYOUT_\w+',routine)))
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
 struct MapLayout layout={w,h,grid};save.mapLayoutId=old;save.pos.x=x;save.pos.y=y;gMapHeader.mapLayoutId=next;gMapHeader.mapLayout=&layout;
 int moved=AraunaMigrateInitialMapSave();out[0]=save.mapLayoutId;out[1]=save.pos.x;out[2]=save.pos.y;return moved;
}
'''
 checked=relocated=current_checked=0;details={}
 with tempfile.TemporaryDirectory() as temp:
  p=Path(temp);(p/'migration.c').write_text(bridge);subprocess.run(['cc','-shared','-fPIC','-Wall','-Wextra','-Werror',str(p/'migration.c'),'-o',str(p/'migration.so')],check=True);dll=ctypes.CDLL(str(p/'migration.so'));f=dll.run;f.argtypes=[ctypes.c_int]*6+[ctypes.POINTER(ctypes.c_uint16),ctypes.POINTER(ctypes.c_int)];f.restype=ctypes.c_int
  for n in TARGETS:
   old=json.loads((base/f'data/maps/{n}/map.json').read_text());new=json.loads((ROOT/f'data/maps/{n}/map.json').read_text());l=ls[1][new['layout']];g=words(ROOT/l['blockdata_filepath']);bg=words(base/ls[0][old['layout']]['blockdata_filepath']);w,h=l['width'],l['height'];arr=(ctypes.c_uint16*len(g))(*g);out=(ctypes.c_int*3)();free=[(i%w,i//w) for i,v in enumerate(g) if not v&0xc00];nchecked=nrelocated=0
   for i,v in enumerate(bg):
    if v&0xc00:continue
    x,y=i%w,i//w;assert f(ids[old['layout']],ids[new['layout']],x,y,w,h,arr,out)==1
    assert out[0]==ids[new['layout']] and not g[out[2]*w+out[1]]&0xc00
    if not g[i]&0xc00:assert (out[1],out[2])==(x,y)
    else:assert abs(out[1]-x)+abs(out[2]-y)==min(abs(xx-x)+abs(yy-y) for xx,yy in free);relocated+=1;nrelocated+=1
    checked+=1;nchecked+=1
    assert f(ids[new['layout']],ids[new['layout']],x,y,w,h,arr,out)==0 and tuple(out)==(ids[new['layout']],x,y);current_checked+=1
   for oi,ni in ((0,ids[new['layout']]),(ids[old['layout']],0)):assert f(oi,ni,10,1,w,h,arr,out)==0 and tuple(out)==(oi,10,1)
   details[n]={'old_positions':nchecked,'repositioned':nrelocated}
 cut=(ROOT/'src/fldeff_cut.c').read_text();oldcut=(base/'src/fldeff_cut.c').read_text();pattern=r'^static void SetCutGrassMetatile\(s16 x, s16 y\)\n\{.*?^\}';current=re.search(pattern,cut,re.M|re.S)[0];original=re.search(pattern,oldcut,re.M|re.S)[0].replace('SetCutGrassMetatile','OriginalCut');symbols=sorted(set(re.findall(r'&?(gTileset_\w+)',current+original)));scoped=[None]+symbols
 bridge='''#include <stdint.h>
#include "constants/metatile_labels.h"
#include "constants/arauna_inicio_metatiles.h"
typedef int16_t s16; typedef uint16_t u16;
struct Tileset {int unused;};
'''+''.join(f'const struct Tileset {s}={{{i+1}}};\n' for i,s in enumerate(symbols))+'''const struct Tileset other={-1};
static struct {const struct Tileset *primaryTileset;}layout;
static struct {typeof(layout) *mapLayout;}gMapHeader={&layout};
static u16 cell;
static u16 MapGridGetMetatileIdAt(s16 x,s16 y){(void)x;(void)y;return cell;}
static void MapGridSetMetatileIdAt(s16 x,s16 y,u16 id){(void)x;(void)y;cell=id;}
'''+current+original+'\nconst struct Tileset *banks[]={&other,'+','.join('&'+s for s in symbols)+'};\nint run(int mid,int bank,int before){cell=mid;layout.primaryTileset=banks[bank];if(before)OriginalCut(0,0);else SetCutGrassMetatile(0,0);return cell;}\n'
 custom=0
 with tempfile.TemporaryDirectory() as temp:
  p=Path(temp);(p/'cut.c').write_text(bridge);subprocess.run(['cc','-shared','-fPIC','-Wall','-Wextra','-Werror','-I'+str(ROOT/'include'),str(p/'cut.c'),'-o',str(p/'cut.so')],check=True);dll=ctypes.CDLL(str(p/'cut.so'));f=dll.run;f.argtypes=[ctypes.c_int]*3;f.restype=ctypes.c_int
  for mid in range(1024):assert f(mid,0,0)==f(mid,0,1),('foreign bank Cut',mid)
  for n,d in art['maps'].items():
   if not d['cut_outputs']:continue
   bank=scoped.index('gTileset_AraunaBorder'+n+'BaseSulV1')
   for mid,out in d['cut_outputs'].items():assert f(int(mid),bank,0)==out;custom+=1
  oldbank=scoped.index('gTileset_AraunaInicioBaseV1');newbank=scoped.index('gTileset_AraunaBorderOldaleTownBaseSulV1')
  for mid in range(1024):assert f(mid,newbank,0)==f(mid,oldbank,1),('Oldale Cut',mid)
 body=source[source.index('void CB2_ContinueSavedGame(void)'):];priority=body.index('if (UseContinueGameWarp() == TRUE)')<body.index('else if (migratedInitialMap)');assert priority
 report={'status':'PASS','actual_C_old_save_positions':checked,'positions_relocated':relocated,'current_layouts_not_migrated':current_checked,'Cut_custom_ids':custom,'continue_warp_priority_preserved':priority,'maps':details};dump(ROOT/'review/sul_pampa_v1/migration_cut_validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
