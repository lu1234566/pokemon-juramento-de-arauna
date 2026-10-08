"""Run production C selectors, Safari lifecycle/feeding and terrain predicates."""
import ctypes,re
from pathlib import Path
from safari_05_common import ROOT,NAMES,inventory
from dive_04_c_checks import function,library
from render_native_map import words
import host_visual_selector_v2 as host

def selector(folder):
 folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);host.ROOT=ROOT;host.compile_selector(folder)
 node,ls,maps=inventory(ROOT);header=(ROOT/'src/data/arauna_cave_visuals_v2.h').read_text();records=re.findall(r'\{(\d+), sVisual_(\w+)\}',header)
 header=re.sub(r'INCBIN_U16\("([^"]+)"\)',lambda m:'{'+','.join(map(str,words(ROOT/m[1])))+'}',header)
 (folder/'data').mkdir(exist_ok=True);(folder/'data/arauna_cave_visuals_v2.h').write_text(header)
 (folder/'caves.c').write_text((ROOT/'src/arauna_cave_visuals.c').read_text())
 indices={int(i):n for i,n in records};indices.update({node['layouts'].index(ls[maps[n]['layout']]):n for n in NAMES});indices.update({675:'Route111',711:'Route111_NoTower',738:'Route103'})
 src='#include "global.h"\n#include "arauna_cave_visuals.h"\n#include "arauna_border_visuals.h"\n';borders=(ROOT/'src/arauna_border_visuals.c').read_text();syms=re.findall(r'extern const struct Tileset (\w+);',borders)
 src+=''.join(f'const struct Tileset {s}={{{i+1}}};\n' for i,s in enumerate(syms))
 for idx,n in indices.items():
  l=node['layouts'][idx];g=words(ROOT/l['blockdata_filepath']);src+=f'static const u16 grid{idx}[]={{'+','.join(map(str,g))+'};\n'
  ptr='&'+l['secondary_tileset'] if l['secondary_tileset'] in syms else 'NULL'
  src+=f'static const struct MapLayout layout{idx}={{NULL,{ptr},{l["width"]},{l["height"]},grid{idx}}};\n'
 src+='const struct MapLayout *const gMapLayouts[]={'+','.join('&layout'+str(i) if i in indices else 'NULL' for i in range(len(node['layouts'])))+'};\n'
 src+='u16 probe(int layout,int x,int y,u16 id){return AraunaBorderVisualMetatile(gMapLayouts[layout],x,y,id);}\n'
 (folder/'bridge.c').write_text(src)
 import subprocess
 so=folder/'combined.so';r=subprocess.run(['cc','-Wall','-Wextra','-Werror','-shared','-fPIC','-I'+str(folder),'-I'+str(ROOT/'include'),str(folder/'caves.c'),str(ROOT/'src/arauna_border_visuals.c'),str(folder/'bridge.c'),'-o',str(so)],capture_output=True,text=True);assert r.returncode==0,r.stderr
 dll=ctypes.CDLL(str(so));dll.probe.argtypes=[ctypes.c_int]*3+[ctypes.c_uint16];dll.probe.restype=ctypes.c_uint16
 return dll,indices

def safari(folder):
 text=(ROOT/'src/safari_zone.c').read_text()
 names=['GetSafariZoneFlag','SetSafariZoneFlag','ResetSafariZoneFlag','ClearPokeblockFeeder','ClearAllPokeblockFeeders','DecrementFeederStepCounters','EnterSafariMode','ExitSafariMode','SafariZoneTakeStep','SafariZoneRetirePrompt','CB2_EndSafariBattle','GetPokeblockFeederInFront','GetPokeblockFeederWithinRange','SafariZoneActivatePokeblockFeeder']
 src='''#include <stdint.h>
#include <string.h>
typedef uint8_t u8;typedef int8_t s8;typedef uint16_t u16;typedef int16_t s16;typedef uint8_t bool8;typedef uint32_t bool32;
#define TRUE 1
#define FALSE 0
#define FLAG_SYS_SAFARI_MODE 1
#define GAME_STAT_ENTERED_SAFARI_ZONE 0
#define NUM_POKEBLOCK_FEEDERS 10
#define B_OUTCOME_CAUGHT 7
#define B_OUTCOME_NO_SAFARI_BALLS 9
struct Pokeblock {u8 color;};
struct PokeblockFeeder {s16 x,y;s8 mapNum;u8 stepCounter;struct Pokeblock pokeblock;};
static struct PokeblockFeeder sPokeblockFeeders[10];
static u8 gNumSafariBalls,sSafariZoneCaughtMons,sSafariZonePkblkUses,gBattleOutcome;
static u16 sSafariZoneStepCounter,gSpecialVar_Result;
static struct {int pokeblockThrows;} gBattleResults;
static struct {struct {int mapNum;} location;struct Pokeblock pokeblocks[20];} save;
static __attribute__((unused)) typeof(save) *gSaveBlock1Ptr=&save;
static int flag,stat,script,warp,stopped,tvCaught,tvThrows,frontX,frontY,playerX,playerY;
static void (*mainCallback)(void);static void (*gFieldCallback)(void);
static const u8 SafariZone_EventScript_TimesUp[]={1},SafariZone_EventScript_RetirePrompt[]={2},SafariZone_EventScript_OutOfBallsMidBattle[]={3},SafariZone_EventScript_OutOfBalls[]={4};
static const u8 emptyName[]={0};static const u8 *gPokeblockNames[256];static u8 gStringVar1[8];
static bool32 FlagGet(int id){(void)id;return flag;}
static void FlagSet(int id){(void)id;flag=1;}
static void FlagClear(int id){(void)id;flag=0;}
static void IncrementGameStat(int id){(void)id;stat++;}
static void TryPutSafariFanClubOnAir(int a,int b){tvCaught=a;tvThrows=b;}
static void ScriptContext_SetupScript(const u8 *p){script=p[0];}
static void RunScriptImmediately(const u8 *p){script=p[0];}
static void ScriptContext_Stop(void){stopped++;}
static void WarpIntoMap(void){warp++;}
static void CB2_ReturnToField(void){}
static void CB2_LoadMap(void){}
static void CB2_ReturnToFieldContinueScriptPlayMapMusic(void){}
static void FieldCB_ReturnToFieldNoScriptCheckMusic(void){}
static void SetMainCallback2(void (*f)(void)){mainCallback=f;}
static void GetXYCoordsOneStepInFrontOfPlayer(s16 *x,s16 *y){*x=frontX;*y=frontY;}
static void PlayerGetDestCoords(s16 *x,s16 *y){*x=playerX;*y=playerY;}
static void StringCopy(u8 *d,const u8 *s){strcpy((char *)d,(const char *)s);}
'''+ '\n'.join(function(text,n) for n in names)+'''
int verify(int which){
 flag=0;stat=0;script=0;warp=0;stopped=0;tvCaught=-1;tvThrows=-1;mainCallback=0;gFieldCallback=0;memset(&save,0,sizeof(save));ClearAllPokeblockFeeders();
 save.location.mapNum=3;frontX=17;frontY=12;playerX=17;playerY=12;save.pokeblocks[0].color=1;gPokeblockNames[1]=emptyName;
 EnterSafariMode();
 if(which==0)return flag && stat==1 && gNumSafariBalls==30 && sSafariZoneStepCounter==500 && !sSafariZoneCaughtMons && !sSafariZonePkblkUses;
 if(which==1){for(int i=0;i<499;i++)if(SafariZoneTakeStep())return 0;return sSafariZoneStepCounter==1 && !script && SafariZoneTakeStep() && script==1 && !sSafariZoneStepCounter;}
 if(which==2){flag=0;return !SafariZoneTakeStep() && sSafariZoneStepCounter==500 && !script;}
 if(which==3){SafariZoneRetirePrompt();return script==2;}
 if(which==4){sSafariZoneCaughtMons=4;sSafariZonePkblkUses=9;ExitSafariMode();return !flag && !gNumSafariBalls && !sSafariZoneStepCounter && tvCaught==4 && tvThrows==9;}
 if(which==5){SafariZoneActivatePokeblockFeeder(0);return sPokeblockFeeders[0].x==17 && sPokeblockFeeders[0].y==12 && sPokeblockFeeders[0].mapNum==3 && sPokeblockFeeders[0].pokeblock.color==1 && sPokeblockFeeders[0].stepCounter==100;}
 if(which==6){SafariZoneActivatePokeblockFeeder(0);for(int i=0;i<99;i++)SafariZoneTakeStep();if(sPokeblockFeeders[0].stepCounter!=1)return 0;SafariZoneTakeStep();return !sPokeblockFeeders[0].x && !sPokeblockFeeders[0].y && !sPokeblockFeeders[0].mapNum && !sPokeblockFeeders[0].stepCounter;}
 if(which==7){SafariZoneActivatePokeblockFeeder(0);GetPokeblockFeederInFront();return gSpecialVar_Result==0;}
 if(which==8){SafariZoneActivatePokeblockFeeder(0);save.location.mapNum=4;GetPokeblockFeederInFront();return gSpecialVar_Result==65535;}
 if(which==9){SafariZoneActivatePokeblockFeeder(0);playerX=20;playerY=14;GetPokeblockFeederWithinRange();return gSpecialVar_Result==0;}
 if(which==10){SafariZoneActivatePokeblockFeeder(0);playerX=20;playerY=15;GetPokeblockFeederWithinRange();return gSpecialVar_Result==65535;}
 if(which==11){for(int i=0;i<11;i++){frontX=10+i;SafariZoneActivatePokeblockFeeder(0);}for(int i=0;i<10;i++)if(sPokeblockFeeders[i].x!=10+i)return 0;return 1;}
 if(which==12){SafariZoneActivatePokeblockFeeder(0);flag=0;SafariZoneTakeStep();return sPokeblockFeeders[0].stepCounter==100;}
 if(which==13){SafariZoneActivatePokeblockFeeder(0);ExitSafariMode();for(int i=0;i<10;i++)if(sPokeblockFeeders[i].stepCounter)return 0;return 1;}
 if(which>=14){gBattleResults.pokeblockThrows=2;gBattleOutcome=which==17?9:7;gNumSafariBalls=which==14?5:0;CB2_EndSafariBattle();
  if(which==14)return sSafariZoneCaughtMons==1 && sSafariZonePkblkUses==2 && mainCallback==CB2_ReturnToField && !script && !warp;
  if(which==15)return sSafariZoneCaughtMons==1 && sSafariZonePkblkUses==2 && script==4 && stopped==1 && mainCallback==CB2_ReturnToFieldContinueScriptPlayMapMusic;
  if(which==16){gBattleOutcome=1;script=0;mainCallback=0;CB2_EndSafariBattle();return !script && !mainCallback;}
  if(which==17)return !sSafariZoneCaughtMons && sSafariZonePkblkUses==2 && script==3 && warp==1 && mainCallback==CB2_LoadMap && gFieldCallback==FieldCB_ReturnToFieldNoScriptCheckMusic;
 }
 return 0;
}
'''
 dll=library(folder,'safari_real',src)
 for i in range(18):assert dll.verify(i)==1,('Safari lifecycle',i)
 return {'status':'PASS','checks':18,'functions':names,'scope':'Actual production C functions. Flag/script/callback/warp services use explicit fixtures; the script interpreter and battle engine are not emulated. 500-step session, 100-step feeder lifetime, retire/exit, feeder capacity/range/map and ball exhaustion branches checked.'}

def behavior(folder):
 text=(ROOT/'src/metatile_behavior.c').read_text();names=['MetatileBehavior_IsPokeGrass','MetatileBehavior_IsTallGrass','MetatileBehavior_IsLongGrass','MetatileBehavior_IsBumpySlope','MetatileBehavior_IsVerticalRail','MetatileBehavior_IsHorizontalRail','MetatileBehavior_IsPokeblockFeeder']
 src='#include <stdint.h>\ntypedef uint8_t u8;typedef uint8_t bool8;\n#define TRUE 1\n#define FALSE 0\n#include "constants/metatile_behaviors.h"\n'+'\n'.join(function(text,n) for n in names)
 src+='\nint probe(int id,int b){switch(id){'+''.join(f'case {i}:return {n}(b);' for i,n in enumerate(names))+'}return -1;}\n'
 src+='int expected(int id,int b){switch(id){case 0:return b==MB_TALL_GRASS || b==MB_LONG_GRASS;'+''.join(f'case {i}:return b=={n};' for i,n in enumerate(['MB_TALL_GRASS','MB_LONG_GRASS','MB_BUMPY_SLOPE','MB_VERTICAL_RAIL','MB_HORIZONTAL_RAIL','MB_POKEBLOCK_FEEDER'],1))+'}return -1;}\n'
 dll=library(folder,'behavior_real',src)
 for i in range(len(names)):
  for b in range(256):assert dll.probe(i,b)==dll.expected(i,b),(i,b)
 return dll,{'status':'PASS','predicate_cases':len(names)*256,'functions':names}
