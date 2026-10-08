"""Production decoration placement and base state functions with host services."""
import ctypes,json,re
from pathlib import Path
from secret_06c1_common import ROOT,NAMES,inventory,parts
from render_native_map import words
from dive_04_c_checks import function,library

def compile_native(folder):
    decor=(ROOT/'src/decoration.c').read_text();secret=(ROOT/'src/secret_base.c').read_text();behavior=(ROOT/'src/metatile_behavior.c').read_text()
    header=(ROOT/'include/decoration.h').read_text();header=header[header.index('enum DecorationPermission'):header.index('extern const struct Decoration')]
    table=(ROOT/'src/data/decoration/header.h').read_text();table=re.sub(r'\s*\.name = .*?,\n','\n',table);table=re.sub(r'\s*\.description = .*?,\n','\n',table)
    positions=re.search(r'static const u8 sSecretBaseEntrancePositions\[.*?\n\};',secret,re.S)[0]
    object_defs='\n'.join(re.findall(r'^#define OBJ_EVENT_GFX_.*', (ROOT/'include/constants/event_objects.h').read_text(), re.M))
    macros='\n'.join(re.findall(r'^#define (?:GET_BASE_\w+\([^\n]*|t(?:Cursor|Initial|Decor)\w* .*).*',secret+'\n'+decor,re.M))
    groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());_,_,maps=inventory(ROOT);map_defs=[];locations={}
    for group,name in enumerate(groups['group_order']):
        for number,n in enumerate(groups[name]):
            if n in maps and n.startswith('SecretBase_'):
                map_defs.append(f'#define {maps[n]["id"]} {(group<<8)|number}')
                locations[n]=(group,number)
    field=(ROOT/'include/global.fieldmap.h').read_text();field_macros='\n'.join(l for l in field.splitlines() if l.startswith('#define ') and not l.startswith('#define GUARD'))
    source='''#include <stdint.h>
#include <string.h>
#include <stddef.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef int8_t s8;typedef int16_t s16;typedef u8 bool8;
#define TRUE 1
#define FALSE 0
#define NUM_TILES_IN_PRIMARY 512
#define MAP_OFFSET 7
#define OBJECT_EVENTS_COUNT 16
#define ELEVATION_INVALID 0xFFFF
#define MAP_GROUP(x) ((x)>>8)
#define MAP_NUM(x) ((x)&255)
#define WARP_ID_NONE -1
#define WARP_ID_SECRET_BASE 0
#define DECOR_MAX_SECRET_BASE 16
#define UNPACK(data,shift,mask) (((data)&(mask))>>(shift))
#define METATILE_LAYER_TYPE_NORMAL 0
#include "constants/decorations.h"
#include "constants/metatile_labels.h"
#include "constants/metatile_behaviors.h"
#include "constants/secret_bases.h"
#include "constants/vars.h"
'''+field_macros+'\n'+object_defs+'\n'+header+'\n'+(ROOT/'src/data/decoration/tiles.h').read_text()+'\n'+table+'\n'+'\n'.join(map_defs)+'\n'+positions+'\n'+macros+'''
static struct {s16 data[16];} gTasks[16];
static struct {u8 active;} gPaletteFade;
static struct {u8 decorations[16],decorationPositions[16],numTimesEntered;} baseRecords[20];
static struct {struct {u8 mapGroup,mapNum;} location; typeof(baseRecords[0]) secretBases[20];} save,*gSaveBlock1Ptr=&save;
static u8 sCurSecretBaseId;static u16 currentBase,initialized;static u16 grid[64][64],attrs[1024];
static int warp[5],dynamicWarp[5],warped,destroyed,locked,objX=-100,objY=-100;
static void (*gFieldCallback)(void);
static void FieldCB_ContinueScriptHandleMusic(void){}
static void CB2_LoadMap(void){}
static void FieldCB_DefaultWarpExit(void){}
static void EnterNewlyCreatedSecretBase_StartFadeIn(void){}
static void SetMainCallback2(void (*cb)(void)){(void)cb;}
static void DestroyTask(u8 id){(void)id;destroyed++;}
static void WarpIntoMap(void){warped++;}
static void LockPlayerFieldControls(void){locked++;}
static void UnlockPlayerFieldControls(void){locked--;}
static void SetWarpDestinationToMapWarp(int group,int number,int id){warp[0]=group;warp[1]=number;warp[2]=id;warp[3]=warp[4]=-1;}
static void SetWarpDestination(int group,int number,int id,int x,int y){SetWarpDestinationToMapWarp(group,number,id);warp[3]=x;warp[4]=y;}
static void SetWarpDestinationToDynamicWarp(int id){if(id==WARP_ID_SECRET_BASE)memcpy(warp,dynamicWarp,sizeof(warp));}
static u16 VarGet(u16 id){return id==VAR_CURRENT_SECRET_BASE?currentBase:id==VAR_SECRET_BASE_INITIALIZED?initialized:0;}
static u16 GetMetatileAttributesById(u16 id){return attrs[id&1023];}
static u16 MapGridGetMetatileIdAt(s16 x,s16 y){return grid[y][x]&1023;}
static u8 MapGridGetMetatileBehaviorAt(s16 x,s16 y){return attrs[MapGridGetMetatileIdAt(x,y)]&255;}
static void MapGridSetMetatileIdAt(s16 x,s16 y,u16 id){grid[y][x]=(grid[y][x]&MAPGRID_ELEVATION_MASK)|(id&~MAPGRID_ELEVATION_MASK);}
static void MapGridSetMetatileEntryAt(s16 x,s16 y,u16 v){grid[y][x]=v;}
static u8 GetObjectEventIdByPosition(s16 x,s16 y,int z){(void)z;return x==objX&&y==objY?1:OBJECT_EVENTS_COUNT;}
static void FindMetatileIdMapCoords(u16 *x,u16 *y,u16 id){for(int yy=7;yy<40;yy++)for(int xx=7;xx<40;xx++)if(MapGridGetMetatileIdAt(xx,yy)==id){*x=xx-7;*y=yy-7;return;}*x=*y=0;}
'''
    pred=['MetatileBehavior_IsNormal','MetatileBehavior_IsSecretBaseNorthWall','MetatileBehavior_IsSecretBaseTrainerSpot','MetatileBehavior_IsSecretBaseHole','MetatileBehavior_IsSecretBaseImpassable','MetatileBehavior_HoldsSmallDecoration','MetatileBehavior_HoldsLargeDecoration']
    source+='\n'.join(function(behavior,n) for n in pred)+'\n'
    for n in ('sDecorationStandElevations','sDecorationSlideElevation'):source+=re.search(r'static const u8 '+n+r'\[\]\s*=\s*\{.*?\};',decor,re.S)[0]+'\n'
    source+='\n'.join(function(decor,n) for n in ('GetDecorationElevation','ShowDecorationOnMap_','ShowDecorationOnMap','IsSecretBaseTrainerSpot','IsntInitialPosition','IsFloorOrBoardAndHole'))+'\n'
    layer=re.search(r'#ifdef BUGFIX\n#define GetLayerType.*?#endif',decor,re.S)[0];source+=layer+'\n'+function(decor,'CanPlaceDecoration')+'\n'
    source+='\n'.join(function(secret,n) for n in ('CurMapIsSecretBase','InitSecretBaseAppearance','SetSecretBaseWarpDestination'))+'\n#define tState data[0]\n'
    source+='\n'.join(function(secret,n) for n in ('Task_EnterSecretBase','Task_EnterNewlyCreatedSecretBase','Task_WarpOutOfSecretBase'))+'''
void reset(void){memset(&save,0,sizeof(save));memset(gTasks,0,sizeof(gTasks));for(int y=0;y<64;y++)for(int x=0;x<64;x++)grid[y][x]=0xc00|0x210;warped=destroyed=locked=0;objX=objY=-100;currentBase=initialized=0;}
void set_attr(int i,int a){attrs[i]=a;}
void set_cell(int x,int y,int v){grid[y+7][x+7]=v;}
int cell(int x,int y){return grid[y+7][x+7];}
int permission(int d){return gDecorations[d].permission;}
int decor_id(int d){return gDecorations[d].id;}
int count_decor(void){return sizeof(gDecorations)/sizeof(gDecorations[0]);}
int can_place(int d,int x,int y,int blocked){
 static const int w[]={1,2,3,4,2,1,1,2,3,3},h[]={1,1,1,2,2,2,3,4,3,2};
 gTasks[0].tCursorX=x+7;gTasks[0].tCursorY=y+7;gTasks[0].tInitialX=gTasks[0].tInitialY=-100;
 gTasks[0].tDecorWidth=w[gDecorations[d].shape];gTasks[0].tDecorHeight=h[gDecorations[d].shape];objX=blocked?x+7:-100;objY=blocked?y+7:-100;
 return CanPlaceDecoration(0,&gDecorations[d]);
}
void show(int d,int x,int y){ShowDecorationOnMap(x+7,y+7,d);}
void appearance(int group,int number,int owner,int init,int hide){save.location.mapGroup=group;save.location.mapNum=number;currentBase=owner;initialized=init;InitSecretBaseAppearance(hide);}
void appearance_decor(int owner,int slot,int d,int x,int y){save.secretBases[owner].decorations[slot]=d;save.secretBases[owner].decorationPositions[slot]=(x<<4)|y;}
void travel(int id,int group,int number,int phase,int active,int entered){sCurSecretBaseId=id;save.location.mapGroup=group;save.location.mapNum=number;gPaletteFade.active=active;gTasks[0].data[0]=phase;save.secretBases[0].numTimesEntered=entered;Task_EnterSecretBase(0);}
void first(int id,int group,int number,int active){sCurSecretBaseId=id;save.location.mapGroup=group;save.location.mapNum=number;gPaletteFade.active=active;Task_EnterNewlyCreatedSecretBase(0);}
void return_step(int phase,int active){gTasks[0].data[0]=phase;gPaletteFade.active=active;dynamicWarp[0]=0;dynamicWarp[1]=12;dynamicWarp[2]=-1;dynamicWarp[3]=19;dynamicWarp[4]=21;Task_WarpOutOfSecretBase(0);}
int value(int i){return i<5?warp[i]:i==5?warped:i==6?destroyed:i==7?save.secretBases[0].numTimesEntered:i==8?gTasks[0].data[0]:locked;}
'''
    dll=library(folder,'native_secret_base',source)
    return dll,locations

def load(dll,repo,l):
    for k in ('primary_tileset','secondary_tileset'):
        p=parts(repo,l[k]);start=0 if k=='primary_tileset' else 512
        for i,a in enumerate(words(p['attributes'])):dll.set_attr(start+i,a)
    dll.reset()
    for i,v in enumerate(words(repo/l['blockdata_filepath'])):dll.set_cell(i%l['width'],i//l['width'],v)

def checks(folder,base):
    dll,locations=compile_native(folder);_,ls,ms=inventory(ROOT);_,bl,bm=inventory(base);cases=placements=allowed=shown=saved_slots=0;details={}
    catalog=dll.count_decor();assert catalog>100
    for group,n in enumerate(NAMES):
        l=ls[ms[n]['layout']];old=bl[bm[n]['layout']];where=locations[n];native=words(base/old['blockdata_filepath']);pc=next((i%l['width'],i//l['width']) for i,v in enumerate(native) if v&1023==0x220)
        # All 16 saved decoration slots and the owner/register/hide PC states.
        for owner,init,hide in ((0,0,0),(0,1,0),(0,1,1),(1,0,0),(19,1,1)):
            load(dll,ROOT,l);dll.appearance(*where,owner,init,hide);expected=(0xc00|0x221) if owner else (0xc00|0x20a) if init and hide else native[pc[1]*l['width']+pc[0]]&0xfff
            assert dll.cell(*pc)&0xfff==expected;cases+=1
        # Drive all 16 saved slots through the actual appearance function.
        load(dll,ROOT,l)
        spot=next((x,y) for y in range(1,min(16,l['height'])) for x in range(1,min(16,l['width'])) if dll.can_place(1,x,y,0))
        load(dll,ROOT,l);dll.show(1,*spot)
        expected=[dll.cell(x,y) for y in range(l['height']) for x in range(l['width'])]
        for slot in range(16):
            load(dll,ROOT,l);dll.appearance_decor(0,slot,1,*spot);dll.appearance(*where,0,0,0)
            assert [dll.cell(x,y) for y in range(l['height']) for x in range(l['width'])]==expected;saved_slots+=1
        for active in (0,1):
            dll.reset();dll.first(group*10+1,*where,active)
            if active:assert dll.value(5)==0
            else:assert [dll.value(i) for i in (0,1,2,3,4)]==[*where,-1,pc[0],pc[1]+1]
            cases+=1
        for entered in (0,254,255):
            dll.reset();dll.travel(group*10+1,*where,1,0,entered);assert [dll.value(i) for i in range(5)]==[*where,0,-1,-1];assert dll.value(7)==min(255,entered+1);assert dll.value(5)==dll.value(6)==1;cases+=1
        dll.reset();dll.travel(group*10+1,*where,0,1,0);assert dll.value(8)==0 and dll.value(5)==0;cases+=1
        dll.reset();dll.travel(group*10+1,*where,0,0,0);assert dll.value(8)==1 and dll.value(5)==0;cases+=1
        # Compare the production placement decision at every map cell for the
        # entire native catalog, with and without an object occupying the spot.
        native_decisions=[]
        for repo,plant in ((base,old),(ROOT,l)):
            load(dll,repo,plant);result=[]
            for d in range(1,catalog):
                for y in range(l['height']):
                    for x in range(l['width']):
                        for blocked in (0,1):result.append(dll.can_place(d,x,y,blocked))
            if repo==base:native_decisions=result
            else:assert result==native_decisions;placements+=len(result);allowed+=sum(result)
        # Actually write every non-sprite decoration at a bounded test fixture,
        # including boards, wall variants, stand/slide elevations and doors.
        for d in range(1,catalog):
            if dll.permission(d)==4:continue
            outputs=[]
            for repo,plant in ((base,old),(ROOT,l)):
                load(dll,repo,plant);dll.show(d,2,4);outputs.append([dll.cell(x,y) for y in range(1,6) for x in range(2,7)])
            assert outputs[0]==outputs[1];shown+=1
        details[n]={'placement_cases':len(native_decisions),'allowed_placement_cases':sum(native_decisions),'pc':pc,'map_group_number':where}
    dll.reset();dll.return_step(0,0);assert dll.value(8)==1 and dll.value(9)==1;cases+=1
    dll.return_step(1,1);assert dll.value(8)==1 and dll.value(5)==0;cases+=1
    dll.return_step(1,0);assert dll.value(8)==2 and dll.value(5)==0;cases+=1
    dll.return_step(2,0);assert [dll.value(i) for i in range(5)]==[0,12,-1,19,21] and dll.value(5)==dll.value(6)==1 and dll.value(9)==0;cases+=1
    assert allowed>100
    return dll,{'status':'PASS','native_catalog_entries':catalog,'pc_entry_return_cases':cases,'saved_decoration_slot_cases':saved_slots,'decoration_placement_cases':placements,'allowed_placement_cases':allowed,'actual_decoration_write_cases':shown,'maps':details,'scope':'Production C functions and native catalog on host; map grid, variables, save records, objects, fades/tasks and warp callbacks are explicit services. No full ROM interpreter, record mixing link session, sprite engine or emulator.'}

if __name__=='__main__':
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        _,report=checks(Path(d),ROOT.parent/'arauna-base-06c1');print(json.dumps(report,indent=2))
