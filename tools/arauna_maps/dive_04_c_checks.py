"""Execute production selectors, Dive predicates/warp dispatcher and fog code."""
import ctypes,json,re,subprocess
from pathlib import Path
from dive_04_common import ROOT,inventory,NAMES
from render_native_map import words
import host_visual_selector_v2 as host

def function(text,name):
 match=re.search(r'^(?:static )?\w+ '+name+r'\([^;]*?\)\n\{',text,re.M);assert match,name
 start=match.start();end=text.index('{',start)+1;depth=1
 while depth:depth+=(text[end]=='{')-(text[end]=='}');end+=1
 return text[start:end]

def library(folder,name,source,extra=()):
 folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);c=folder/(name+'.c');so=folder/(name+'.so');c.write_text(source)
 result=subprocess.run(['cc','-Wall','-Wextra','-Werror','-shared','-fPIC','-iquote',str(ROOT/'include'),str(c),*extra,'-o',str(so)],capture_output=True,text=True)
 assert result.returncode==0,result.stderr
 return ctypes.CDLL(str(so))

def selector(folder):
 folder=Path(folder);folder.mkdir(exist_ok=True);host.ROOT=ROOT;host.compile_selector(folder)
 node,ls,maps=inventory(ROOT);header=(ROOT/'src/data/arauna_cave_visuals_v2.h').read_text();records=re.findall(r'\{(\d+), sVisual_(\w+)\}',header)
 header=re.sub(r'INCBIN_U16\("([^"]+)"\)',lambda m:'{'+','.join(map(str,words(ROOT/m[1])))+'}',header)
 (folder/'data').mkdir(exist_ok=True);(folder/'data/arauna_cave_visuals_v2.h').write_text(header)
 src=(ROOT/'src/arauna_cave_visuals.c').read_text();(folder/'caves.c').write_text(src)
 indices={int(idx):name for idx,name in records};indices.update({675:'Route111',711:'Route111_NoTower',738:'Route103'})
 source='#include "global.h"\n#include "arauna_cave_visuals.h"\n#include "arauna_border_visuals.h"\n'
 borders=(ROOT/'src/arauna_border_visuals.c').read_text();symbols=re.findall(r'extern const struct Tileset (\w+);',borders)
 source+=''.join(f'const struct Tileset {s}={{{i+1}}};\n' for i,s in enumerate(symbols))
 for idx,name in indices.items():
  l=node['layouts'][idx];g=words(ROOT/l['blockdata_filepath']);source+=f'static const u16 grid{idx}[]={{'+','.join(map(str,g))+'};\n'
  bank=l['secondary_tileset'];ptr='&'+bank if bank in symbols else 'NULL'
  source+=f'static const struct MapLayout layout{idx}={{NULL,{ptr},{l["width"]},{l["height"]},grid{idx}}};\n'
 source+='const struct MapLayout *const gMapLayouts[]={'+','.join('&layout'+str(i) if i in indices else 'NULL' for i in range(len(node['layouts'])))+'};\n'
 source+='u16 probe(int layout,int x,int y,u16 id){return AraunaBorderVisualMetatile(gMapLayouts[layout],x,y,id);}\n'
 source+='u16 unknown(int x,int y,u16 id){struct MapLayout l={NULL,NULL,1,1,grid738};return AraunaCaveVisualMetatile(&l,x,y,id);}\n'
 (folder/'bridge.c').write_text(source);so=folder/'combined.so'
 subprocess.run(['cc','-Wall','-Wextra','-Werror','-shared','-fPIC','-I'+str(folder),'-I'+str(ROOT/'include'),str(folder/'caves.c'),str(ROOT/'src/arauna_border_visuals.c'),str(folder/'bridge.c'),'-o',str(so)],capture_output=True,text=True,check=True)
 dll=ctypes.CDLL(str(so));dll.probe.argtypes=[ctypes.c_int]*3+[ctypes.c_uint16];dll.probe.restype=ctypes.c_uint16
 return dll,indices

def dive(folder):
 overworld=(ROOT/'src/overworld.c').read_text();avatar=(ROOT/'src/field_control_avatar.c').read_text();behavior=(ROOT/'src/metatile_behavior.c').read_text()
 source='''#include <stdint.h>
#include <stddef.h>
typedef uint8_t u8;typedef uint16_t u16;typedef int16_t s16;typedef uint8_t bool8;typedef uint32_t bool32;typedef int32_t s32;
#define TRUE 1
#define FALSE 0
#define MAP_OFFSET 7
#include "constants/map_types.h"
#define CONNECTION_DIVE 5
#define CONNECTION_EMERGE 6
#define WARP_ID_NONE -1
#include "constants/metatile_behaviors.h"
struct MapConnection {u8 direction,mapGroup,mapNum;};
struct Warp {int mapGroup,mapNum,x,y;};
struct Header {int mapType;};static struct Header gMapHeader;
static struct MapConnection connection;static int hasConnection,hasScript;static struct Warp sFixedDiveWarp,dest;
static u8 tileBehavior;static s16 px,py;
static const struct MapConnection *GetMapConnection(u8 direction){return hasConnection && connection.direction==direction?&connection:0;}
static void SetWarpDestination(int group,int num,int id,int x,int y){(void)id;dest=(struct Warp){group,num,x,y};}
static void RunOnDiveWarpMapScript(void){sFixedDiveWarp=hasScript?(struct Warp){8,9,12,44}:(struct Warp){-1,-1,-1,-1};}
static bool8 IsDummyWarp(struct Warp *w){return w->mapGroup<0;}
static void SetWarpDestinationToDiveWarp(void){dest=sFixedDiveWarp;}
static void PlayerGetDestCoords(s16 *x,s16 *y){*x=px;*y=py;}
static u8 MapGridGetMetatileBehaviorAt(s16 x,s16 y){(void)x;(void)y;return tileBehavior;}
'''+function(behavior,'MetatileBehavior_IsDiveable')+'\n'+function(behavior,'MetatileBehavior_IsUnableToEmerge')+'\n'+function(overworld,'SetDiveWarp')+'\n'+function(overworld,'SetDiveWarpEmerge')+'\n'+function(overworld,'SetDiveWarpDive')+'\n'+function(avatar,'TrySetDiveWarp')+'''
int probe(int underwater,int behavior,int viaConnection,int script,int x,int y){
 gMapHeader.mapType=underwater?MAP_TYPE_UNDERWATER:MAP_TYPE_ROUTE;tileBehavior=behavior;hasConnection=viaConnection;hasScript=script;
 connection=(struct MapConnection){underwater?6:5,3,4};px=x+7;py=y+7;dest=(struct Warp){-1,-1,-1,-1};return TrySetDiveWarp();
}
int destination(int field){const int values[]={dest.mapGroup,dest.mapNum,dest.x,dest.y};return values[field];}
'''
 dll=library(folder,'dive_real',source);dll.probe.argtypes=[ctypes.c_int]*6;dll.probe.restype=ctypes.c_int
 checks=0
 for underwater in (0,1):
  for b in range(256):
   for via,script in ((0,0),(1,0),(0,1)):
    expected=(1 if underwater else 2) if ((underwater and b not in (0x19,0x2A)) or (not underwater and b in (0x11,0x12,0x14))) and (via or script) else 0
    assert dll.probe(underwater,b,via,script,15,20)==expected,(underwater,b,via,script)
    if expected:assert [dll.destination(i) for i in range(4)]==([3,4,15,20] if via else [8,9,12,44])
    checks+=1
 return dll,{'status':'PASS','predicate_and_dispatch_cases':checks,'sources':['MetatileBehavior_IsDiveable','MetatileBehavior_IsUnableToEmerge','SetDiveWarp','SetDiveWarpEmerge','SetDiveWarpDive','TrySetDiveWarp'],'script_scope':'Dispatcher script callback uses explicit fixture; event script files are frozen, not interpreted.'}

def fog(folder):
 text=(ROOT/'src/field_weather_effect.c').read_text()
 source='''#include <stdint.h>
typedef uint8_t u8;typedef uint16_t u16;
#define TRUE 1
#define FALSE 0
#include "constants/maps.h"
#include "constants/weather.h"
struct Weather {int fogHScrollPosX,fogHScrollOffset,fogHScrollCounter,initStep,currWeather,weatherGfxLoaded;};
struct Save {struct {int mapGroup,mapNum;} location;};
static struct Weather w;static struct Weather *gWeatherPtr=&w;static struct Save save;static struct Save *gSaveBlock1Ptr=&save;static int gSpriteCoordOffsetX;
static int blendA,blendB,blendDelay,sprites;
static void CreateFogHorizontalSprites(void){sprites++;}
static void Weather_SetTargetBlendCoeffs(int a,int b,int d){blendA=a;blendB=b;blendDelay=d;}
static int Weather_UpdateBlend(void){return 1;}
'''+function(text,'FogHorizontal_Main')+'''
int probe(int map,int weather){save.location.mapGroup=map>>8;save.location.mapNum=map&255;w=(struct Weather){0};w.currWeather=weather;blendA=blendB=blendDelay=-1;sprites=0;FogHorizontal_Main();FogHorizontal_Main();return blendA*10000+blendB*100+blendDelay;}
int chamber(int i){const int ids[]={MAP_TERRA_CAVE_END,MAP_MARINE_CAVE_END};return ids[i];}
int state(void){return sprites==1 && w.weatherGfxLoaded && w.initStep==2;}
'''
 dll=library(folder,'fog_real',source);checks=0;special={dll.chamber(0),dll.chamber(1)}
 # Map IDs are literal production constants, generated by the official mapjson.
 node,ls,maps=inventory(ROOT)
 headers=(ROOT/'include/constants/map_groups.h').read_text()
 ids={n:int(g)*256+int(m) for n,g,m in re.findall(r'#define (MAP_\w+)\s+\((\d+)\s*\|\s*\((\d+)\s*<<\s*8\)\)',headers)}
 # Official format may use map number OR map group. Resolve via a C lookup.
 if not ids:
  names=[m['id'] for m in maps.values()]
  lookup=library(folder,'map_ids','#include "constants/maps.h"\nint value(int i){const int a[]={'+','.join(names)+'};return a[i];}\n')
  ids={n:lookup.value(i) for i,n in enumerate(names)}
 for mid in ids.values():
  assert dll.probe(mid,6)==(41603 if mid in special else 120803),(mid,'fog');assert dll.state();checks+=1
  assert dll.probe(mid,10)==41600 and dll.state(),(mid,'underwater');checks+=1
 assert special.issubset(set(ids.values()))
 return {'status':'PASS','actual_c_checks':checks,'chambers':sorted(special),'old_coefficients':[12,8,3],'chamber_coefficients':[4,16,3],'all_other_maps_keep_old_fog':True,'underwater_fog_unchanged':True}
