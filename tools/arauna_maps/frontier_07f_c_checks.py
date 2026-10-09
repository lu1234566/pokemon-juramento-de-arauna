"""Run original Pyramid C assembly, placement, palettes and VRAM animation on host."""
import ctypes,hashlib,json,re,struct
from pathlib import Path
from frontier_07f_common import ROOT,NAMES,SQUARES,inventory,animation_tables,floor_palettes
from render_native_map import words
from dive_04_c_checks import function,library
from frontier_07c_animation_checks import raw_4bpp

GENERATING=['GetPyramidFloorTemplateId','GetPyramidFloorLayoutOffsets','GetPyramidEntranceAndExitSquareIds','GenerateBattlePyramidFloorLayout','TrySetPyramidObjectEventPositionAtCoords','TrySetPyramidObjectEventPositionInSquare','SetPyramidObjectPositionsUniformly','SetPyramidObjectPositionsInAndNearSquare','SetPyramidObjectPositionsNearSquare','LoadBattlePyramidObjectEventTemplates','Task_SetPyramidFloorPalette']

def declaration(src,name):
    return re.search(r'^static const [^;=]+\b'+name+r'[^=]*=\s*\{.*?\};',src,re.M|re.S)[0]

def generator(repo,folder):
    src=(repo/'src/battle_pyramid.c').read_text();node,ls,maps=inventory(repo)
    flooridx=node['layouts'].index(ls[maps[NAMES[1]]['layout']]);assert flooridx==360
    for i,n in enumerate(SQUARES):assert node['layouts'].index(ls[maps[n]['layout']])==flooridx+1+i
    structdef=re.search(r'struct PyramidFloorTemplate\n\{.*?\};',src,re.S)[0]
    prefix='''#include <stdint.h>
#include <stdlib.h>
#include <string.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef uint8_t bool8;
#define TRUE 1
#define FALSE 0
#define ARRAY_COUNT(a) ((int)(sizeof(a)/sizeof((a)[0])))
#define MOD(a,n) (((n)&((n)-1))?((a)%(n)):((a)&((n)-1)))
#define NUM_LAYOUT_OFFSETS 8
#define FRONTIER_STAGES_PER_CHALLENGE 7
#define MAP_OFFSET 7
#define MAP_OFFSET_W 15
#define MAP_OFFSET_H 14
#define MAPGRID_METATILE_ID_MASK 0x03FF
#define MAPGRID_COLLISION_MASK 0x0C00
#define MAPGRID_ELEVATION_MASK 0xF000
#define LAYOUT_BATTLE_FRONTIER_BATTLE_PYRAMID_FLOOR 361
#define OBJECT_EVENT_TEMPLATES_COUNT 64
#define MAP_BATTLE_PYRAMID_SQUARE01 0
#define MAP_GROUP(n) 0
#define MAP_NUM(n) 0
#define BG_PLTT_ID(n) ((n)*16)
#define PLTT_SIZE_4BPP 32
#include "constants/battle_pyramid.h"
#include "constants/metatile_labels.h"
struct ObjectEventTemplate {u16 graphicsId;u8 localId;int x,y;uint64_t payload;};
struct MapLayout {int width,height;const u16 *map;};
struct Events {int objectEventCount;const struct ObjectEventTemplate *objectEvents;};
struct MapHeader {const struct Events *events;};
static struct {struct {int x,y;} pos;struct ObjectEventTemplate objectEventTemplates[64];} save1;
static struct {struct {u16 pyramidRandoms[4],trainerIds[8];u8 curChallengeBattleNum;} frontier;} save2;
static typeof(save1) *gSaveBlock1Ptr=&save1;
static typeof(save2) *gSaveBlock2Ptr=&save2;
static struct {int width,height;u16 *map;} gBackupMapLayout;
static struct {int active;} gPaletteFade;
static u16 gPlttBufferUnfaded[256],buffer[47*46];
static int scripts,destroys,allocs,freed;
static void *allocations[128];
static void *AllocZeroed(int n){void *p=calloc(1,n);allocations[allocs++]=p;return p;}
static void Free(void *p){for(int i=0;i<allocs;i++)if(allocations[i]==p){free(p);allocations[i]=0;freed++;return;}}
static void RunOnLoadMapScript(void){scripts++;}
static void CpuFill32(int value,void *dst,int size){memset(dst,value,size);}
static void CpuCopy16(const void *src,void *dst,int size){memcpy(dst,src,size);}
static void DestroyTask(u8 task){(void)task;destroys++;}
static int GetUniqueTrainerId(u8 id){return 1000+id;}
static u16 GetBattleFacilityTrainerGfxId(int id){return 200+id-1000;}
static const u32 gBitTable[]={1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768};
'''+structdef+'\n'
    gfx=(repo/'include/constants/event_objects.h').read_text()
    wanted={'OBJ_EVENT_GFX_ITEM_BALL'}|{e['graphics_id'] for n in SQUARES for e in maps[n]['object_events']}
    for name in sorted(wanted):
        value=re.search(r'^#define '+name+r'\s+(\d+)\s*$',gfx,re.M)[1]
        prefix+=f'#define {name} {value}\n'
    prefix+='\n'.join(declaration(src,n) for n in ('sPyramidFloorTemplates','sPyramidFloorTemplateOptions','sFloorTemplateOffsets','sBorderedSquareIds'))+'\n'
    fixture='';layoutrefs=['0']*754;headers=[]
    for i,n in enumerate(SQUARES):
        l=ls[maps[n]['layout']];g=words(repo/l['blockdata_filepath'])
        fixture+=f'static const u16 grid{i}[]={{'+','.join(map(str,g))+'};\n'
        fixture+=f'static const struct MapLayout layout{i}={{8,8,grid{i}}};\n';layoutrefs[flooridx+1+i]='&layout'+str(i)
        events=[]
        for j,e in enumerate(maps[n]['object_events']):
            digest=int.from_bytes(hashlib.sha256(json.dumps(e,sort_keys=True).encode()).digest()[:8],'little')
            events.append('{'+f'{e["graphics_id"]},{j+1},{e["x"]},{e["y"]},{digest}ULL'+'}')
        fixture+=f'static const struct ObjectEventTemplate events{i}[]={{'+','.join(events)+'};\n'
        fixture+=f'static const struct Events eventset{i}={{7,events{i}}};\nstatic const struct MapHeader header{i}={{&eventset{i}}};\n';headers.append('&header'+str(i))
    fixture+='static const struct MapLayout *const gMapLayouts[]={'+','.join(layoutrefs)+'};\n'
    fixture+='static const struct MapHeader *const headers[]={'+','.join(headers)+'};\n'
    fixture+='static const struct MapHeader *Overworld_GetMapHeaderByGroupAndId(int group,int num){(void)group;return headers[num];}\n'
    pals=floor_palettes(repo)
    fixture+='static const u16 gBattlePyramidFloor_Pal[][16]={'+','.join('{'+','.join(str((r>>3)|((g>>3)<<5)|((b>>3)<<10)) for r,g,b in p)+'}' for p in pals)+'};\n'
    funcs=[function(src,n) for n in GENERATING];protos='\n'.join(f[:f.index('\n{')]+';' for f in funcs)
    bridge='''
void generate(int floor,int a,int b,int c,int d,int mode){
 memset(&save1,0,sizeof(save1));memset(&save2,0,sizeof(save2));
 save1.pos.x=123;save1.pos.y=124;save2.frontier.curChallengeBattleNum=floor;
 save2.frontier.pyramidRandoms[0]=a;save2.frontier.pyramidRandoms[1]=b;save2.frontier.pyramidRandoms[2]=c;save2.frontier.pyramidRandoms[3]=d;
 for(int i=0;i<47*46;i++)buffer[i]=0xA55A;
 scripts=destroys=allocs=freed=0;GenerateBattlePyramidFloorLayout(buffer,mode);LoadBattlePyramidObjectEventTemplates();
 for(int i=0;i<allocs;i++)if(allocations[i]){free(allocations[i]);allocations[i]=0;}
}
int value(int key,int i){u8 offsets[16],en,ex;switch(key){
 case 0:return buffer[i];case 1:return gBackupMapLayout.width;case 2:return gBackupMapLayout.height;
 case 3:return save1.pos.x;case 4:return save1.pos.y;case 5:return scripts;
 case 6:return GetPyramidFloorTemplateId();case 7:GetPyramidFloorLayoutOffsets(offsets);return offsets[i];
 case 8:GetPyramidEntranceAndExitSquareIds(&en,&ex);return en;case 9:GetPyramidEntranceAndExitSquareIds(&en,&ex);return ex;
 case 10:return sPyramidFloorTemplates[GetPyramidFloorTemplateId()].numTrainers;
 case 11:return sPyramidFloorTemplates[GetPyramidFloorTemplateId()].numItems;
 case 12:return save1.objectEventTemplates[i].x;case 13:return save1.objectEventTemplates[i].y;
 case 14:return save1.objectEventTemplates[i].graphicsId;case 15:return save1.objectEventTemplates[i].localId;
 case 16:return save2.frontier.trainerIds[i];case 17:return allocs;case 18:return freed;
 }return -1;}
uint64_t payload(int i){return save1.objectEventTemplates[i].payload;}
void palette(int floor,int active){save2.frontier.curChallengeBattleNum=floor;gPaletteFade.active=active;memset(gPlttBufferUnfaded,0x55,sizeof(gPlttBufferUnfaded));destroys=0;Task_SetPyramidFloorPalette(0);}
int palvalue(int i){return i<256?gPlttBufferUnfaded[i]:destroys;}
'''
    dll=library(folder,'pyramid_generator',prefix+fixture+protos+'\n'+'\n'.join(funcs)+bridge);dll.payload.restype=ctypes.c_uint64
    return dll

def cases():
    for floor in range(7):
        for i in range(128):
            yield (floor,(i*17329+floor*31)&65535,(i*31337+12345)&65535,(i*379+floor*911)&65535,(i%100)+(i//100)*10000)
        for values in ((0,0,0,0),(65535,65535,65535,65535),(32768,0,32768,32768),(17,19,16,17)):yield (floor,*values)

def checks(base,folder):
    before=generator(base,Path(folder)/'before');after=generator(ROOT,Path(folder)/'after');_,ls,maps=inventory(base)
    grids=[words(base/ls[maps[n]['layout']]['blockdata_filepath']) for n in SQUARES]
    cases_count=cells=objects=guards=palette_cases=0;used=set();templates=set();snapshots=[]
    for args in cases():
        for mode in (0,1):
            before.generate(*args,mode);after.generate(*args,mode)
            assert [after.value(k,0) for k in (1,2,5)]==[47,46,1]
            offsets=[after.value(7,i) for i in range(16)];used.update(offsets);templates.add(after.value(6,0));en=after.value(8,0);ex=after.value(9,0);assert en!=ex
            expected=[0xA55A]*(47*46);player=None;markers=[]
            for square,offset in enumerate(offsets):
                for i,v in enumerate(grids[offset]):
                    x=square%4*8+i%8;y=square//4*8+i//8
                    if v&1023==0x28e:
                        if square==ex:markers.append((x,y))
                        else:
                            v=(v&0xfc00)|0x28d
                            if square==en:player=(x,y)
                    expected[(y+7)*47+x+7]=v
            actual=[after.value(0,i) for i in range(47*46)]
            assert actual==expected==[before.value(0,i) for i in range(47*46)]
            assert len(markers)==1 and player is not None
            assert (after.value(3,0),after.value(4,0))==((123,124) if mode else player)
            assert all(before.value(k,i)==after.value(k,i) for k in range(1,19) for i in (range(16) if k==7 else range(8) if k==16 else range(64) if 12<=k<=15 else (0,)))
            count=after.value(10,0)+after.value(11,0);positions=[]
            for i in range(count):
                x,y,gfx,local=(after.value(k,i) for k in (12,13,14,15));assert 0<=x<32 and 0<=y<32 and local==i+1
                assert (x,y) not in positions;positions.append((x,y));assert actual[(y+7)*47+x+7]&0xc00==0
                assert after.payload(i)==before.payload(i)
                source=maps[SQUARES[offsets[y//8*4+x//8]]]['object_events']
                candidates=[e for e in source if e['x']==x%8 and e['y']==y%8 and (e['graphics_id']=='OBJ_EVENT_GFX_ITEM_BALL')==(gfx==59)]
                assert len(candidates)==1
                digest=int.from_bytes(hashlib.sha256(json.dumps(candidates[0],sort_keys=True).encode()).digest()[:8],'little');assert after.payload(i)==digest
                assert (gfx==59)==(i>=after.value(10,0));objects+=1
            cells+=1024;guards+=47*46-1024;cases_count+=1
            if args[1:]==(args[0]*31,12345,args[0]*911,0) and mode==0:
                snapshots.append({'floor':args[0],'randoms':list(args[1:]),'width':32,'height':32,'grid':[actual[(y+7)*47+x+7] for y in range(32) for x in range(32)],'entrance':list(player),'exit':list(markers[0]),'objects':positions,'layout_offsets':offsets})
    assert used==set(range(16)) and templates==set(range(16)) and len(snapshots)==7
    for floor,pal in enumerate(floor_palettes(ROOT)):
        expected=[(r>>3)|((g>>3)<<5)|((b>>3)<<10) for r,g,b in pal]
        for active in (0,1):
            after.palette(floor,active);before.palette(floor,active)
            for i in range(256):assert after.palvalue(i)==before.palvalue(i)==(expected[i-96] if active and 96<=i<112 else 0x5555)
            assert after.palvalue(256)==active;palette_cases+=1
    return {'status':'PASS','generator_cases':cases_count,'generated_cells':cells,'untouched_padding_cells':guards,'placed_objects':objects,'source_modules':16,'floor_templates':16,'palette_task_cases':palette_cases,'snapshots':snapshots,'source_functions':GENERATING,'scope':'Original production C selectors, 32x32 assembly, entrance/exit handling, both player-position modes, all placement strategies and palette task execute against real module grids/events. Map lookup, allocation, load-script callback and trainer ID/graphics services are explicit host fixtures. Trainer roster RNG, script interpreter, light scanline hardware, battles, bag, saves and progression are preserved by hash, not played.'}

def animation_checks(folder):
    src=(ROOT/'src/tileset_anims.c').read_text();tables=animation_tables(ROOT);payloads={n:raw_4bpp(ROOT/p,8) for t in tables for n,p in zip(t['refs'],t['paths'])}
    prefix='''#include <stdint.h>
#include <string.h>
typedef uint8_t u8;typedef uint16_t u16;
#define ARRAY_COUNT(a) ((int)(sizeof(a)/sizeof((a)[0])))
#define TILE_SIZE_4BPP 32
#define TILE_OFFSET_4BPP(n) ((n)*32)
#define NUM_TILES_IN_PRIMARY 512
static u8 vram[65536];
#define BG_VRAM vram
static u16 sSecondaryTilesetAnimCounter,sSecondaryTilesetAnimCounterMax,sPrimaryTilesetAnimCounterMax=256;
static void (*sSecondaryTilesetAnimCallback)(u16);
static int copies;
static void AppendTilesetAnimToBuffer(const u16 *src,u16 *dst,u16 size){memcpy(dst,src,size);copies++;}
'''
    frames=''.join('static const u16 '+n+'[]={'+','.join(map(str,struct.unpack('<128H',raw)))+'};\n' for n,raw in payloads.items())
    names=['InitTilesetAnim_BattlePyramid','TilesetAnim_BattlePyramid','QueueAnimTiles_BattlePyramid_Torch','QueueAnimTiles_BattlePyramid_StatueShadow'];funcs=[function(src,n) for n in names]
    code=prefix+frames+'\n'.join(t['table'] for t in tables)+'\n'+'\n'.join(f[:f.index('\n{')]+';' for f in funcs)+'\n'+'\n'.join(funcs)+'''
void reset(void){memset(vram,0x55,sizeof(vram));InitTilesetAnim_BattlePyramid();}
void tick(int t){copies=0;sSecondaryTilesetAnimCallback(t);}
int value(int key,int i){switch(key){case 0:return copies;case 1:return vram[i];case 2:return sSecondaryTilesetAnimCounter;case 3:return sSecondaryTilesetAnimCounterMax;}return -1;}
'''
    dll=library(folder,'pyramid_animation',code);dll.reset();assert dll.value(2,0)==0 and dll.value(3,0)==256;updates=0
    for tick in range(256):
        dll.tick(tick);assert dll.value(0,0)==(2 if tick%8==0 else 0)
        if tick%8==0:
            for t in tables:
                expected=payloads[t['refs'][(tick//8)%3]];start=t['start']*32
                assert bytes(dll.value(1,start+i) for i in range(256))==expected
                assert dll.value(1,start-1)==dll.value(1,start+256)==0x55
            updates+=2
    return {'status':'PASS','ticks':256,'queue_updates':updates,'torch_frames':3,'shadow_frames':3,'reserved_slots':[647,648,649,650,651,652,653,654,663,664,665,666,667,668,669,670],'source_functions':names,'scope':'Original initializer, dispatch and both queues run on host with real 4bpp frames and guarded VRAM service.'}
