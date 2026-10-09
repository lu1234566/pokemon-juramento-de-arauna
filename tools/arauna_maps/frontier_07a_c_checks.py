"""Execute the production door router, footprints and synchronized Multi door."""
import itertools,json,re
from frontier_07a_common import ROOT
from dive_04_c_checks import library

def extract(text,name):
    match=re.search(r'^static [^\n;]*\b'+name+r'\([^;]*?\)\n\{',text,re.M);assert match,name
    start=match.start();end=text.index('{',start)+1;depth=1
    while depth:depth+=(text[end]=='{')-(text[end]=='}');end+=1
    return text[start:end]

def checks(folder):
    text=(ROOT/'src/field_door.c').read_text();table=re.search(r'static const struct DoorGraphics sDoorAnimGraphicsTable\[\] =\n\{.*?\n\};',text,re.S)[0]
    special='\n'.join(re.findall(r'static const struct DoorGraphics sDoorGraphics_\w+\s*=\s*\{.*?\};',text,re.S))
    refs=table+'\n'+special;tile_names=sorted(set(re.findall(r'\bsDoorAnimTiles_\w+',refs)));pal_names=sorted(set(re.findall(r'\bsDoorAnimPalettes_\w+',refs)))
    palettes='\n'.join(re.search(r'static const u8 '+n+r'\[\] = \{.*?\};',text,re.S)[0] for n in pal_names)
    rows=re.findall(r'\{(METATILE_\w+|0x[0-9a-fA-F]+),\s*DOOR_SOUND_\w+,\s*(\d+),',table)
    labels={k:int(v,16) for k,v in re.findall(r'#define (METATILE_\w+)\s+(0x[\da-fA-F]+)',(ROOT/'include/constants/metatile_labels.h').read_text())}
    ids=[labels[n] if n in labels else int(n,16) for n,_ in rows]
    source='''#include <stdint.h>
#include <stddef.h>
#include <string.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef uint8_t bool8;
#define TRUE 1
#define FALSE 0
#define MAP_OFFSET 7
#define DOOR_SOUND_NORMAL 0
#define DOOR_SOUND_SLIDING 1
#define DOOR_SOUND_ARENA 2
#define DOOR_TILE_START_SIZE1 1016
#define DOOR_TILE_START_SIZE2 1008
#include "constants/metatile_labels.h"
#include "constants/maps.h"
#include "constants/flags.h"
struct Tileset {int tag;};
static const struct Tileset privateBank={0},gTileset_AraunaTrainerHill06APavilionBase={1},gTileset_AraunaInicioBaseV1={2},gTileset_AraunaBorderOldaleTownBaseUivoV1={3};
static struct {const struct Tileset *primaryTileset;} layout;
static struct {__typeof__(layout) *mapLayout;} gMapHeader={&layout};
struct DoorGraphics {u16 metatileNum;u8 sound,size;const void *tiles,*palettes;};
struct DoorAnimFrame {u8 time;u16 offset;};
static struct {struct {int mapGroup,mapNum;} location;} save;
static __typeof__(save) *gSaveBlock1Ptr=&save;
static int flag,count,copies,xs[8],ys[8],kinds[8];static u16 drawn[8][8],gSpecialVar_0x8004,gSpecialVar_0x8005;
static int FlagGet(int id){(void)id;return flag;}
static void DrawDoorMetatileAt(int x,int y,u16 *p){xs[count]=x;ys[count]=y;kinds[count]=1;memcpy(drawn[count++],p,16);}
static void CurrentMapDrawMetatileAt(int x,int y){xs[count]=x;ys[count]=y;kinds[count++]=0;}
static void CopyDoorTilesToVram(const struct DoorGraphics *g,const struct DoorAnimFrame *f){(void)g;(void)f;copies++;}
'''+''.join('static const u8 '+n+'[]={0};\n' for n in tile_names)+palettes+'\n'+special+'\n'+table+'\n'
    names=['GetDoorGraphics','BuildDoorTiles','DrawCurrentDoorAnimFrame','DrawClosedDoorTiles','ShouldUseMultiCorridorDoor','DrawDoor']
    source+='\n'.join(extract(text,n) for n in names)+'''
int route(int mode,int mid){const struct Tileset *banks[]={&privateBank,&gTileset_AraunaTrainerHill06APavilionBase,&gTileset_AraunaInicioBaseV1,&gTileset_AraunaBorderOldaleTownBaseUivoV1};layout.primaryTileset=banks[mode];const struct DoorGraphics *g=GetDoorGraphics(sDoorAnimGraphicsTable,mid);if(!g)return -1;if(g==&sDoorGraphics_AraunaTrainerHillLobbyElevator)return 900;if(g==&sDoorGraphics_AraunaTrainerHillRoofElevator)return 901;if(g==&sDoorGraphics_AraunaInicioMadeira)return 902;return g-sDoorAnimGraphicsTable;}
void frame(int size,int enabled,int correctMap,int closed){
 static const u8 p[16]={7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7};
 struct DoorGraphics g={0,0,(u8)size,p,p};struct DoorAnimFrame f={4,closed?0xffff:0};flag=enabled;count=copies=0;gSpecialVar_0x8004=14;gSpecialVar_0x8005=1;
 save.location.mapGroup=MAP_GROUP(MAP_BATTLE_FRONTIER_BATTLE_TOWER_MULTI_CORRIDOR);save.location.mapNum=correctMap?MAP_NUM(MAP_BATTLE_FRONTIER_BATTLE_TOWER_MULTI_CORRIDOR):255;
 DrawDoor(&g,&f,8,8);
}
int value(int field,int i,int j){switch(field){case 0:return count;case 1:return copies;case 2:return xs[i];case 3:return ys[i];case 4:return kinds[i];case 5:return drawn[i][j];}return -1;}
'''
    # A source-only checkout need not have mapjson's ignored map_groups.h yet.
    # Derive the one location fixture from the same canonical JSON group order.
    groups=json.loads((ROOT/'data/maps/map_groups.json').read_text())
    positions=[(gi,groups[name].index('BattleFrontier_BattleTowerMultiCorridor')) for gi,name in enumerate(groups['group_order']) if 'BattleFrontier_BattleTowerMultiCorridor' in groups[name]]
    assert len(positions)==1;gi,mi=positions[0]
    macros='\n'.join(line for line in (ROOT/'include/constants/maps.h').read_text().splitlines() if line.startswith(('#define MAP_GROUP(','#define MAP_NUM(')))
    source=source.replace('#include "constants/maps.h"',f'#define MAP_BATTLE_FRONTIER_BATTLE_TOWER_MULTI_CORRIDOR {mi | gi<<8}\n'+macros)
    dll=library(folder,'battle_tower_doors',source);routes=0
    for mid in range(1024):
        expected=ids.index(mid) if mid in ids else -1
        assert dll.route(0,mid)==expected,('private door router',mid);routes+=1
    for name,tag in [('METATILE_TrainerHill_Door_Elevator_Lobby',900),('METATILE_TrainerHill_Door_Elevator_Roof',901)]:
        assert dll.route(1,labels[name])==tag;routes+=1
    frames=0
    for size,enabled,correct,closed in itertools.product((1,2),(0,1),(0,1),(0,1)):
        dll.frame(size,enabled,correct,closed);origins=[(8,8)]+([(21,8)] if enabled and correct else [])
        coords=[(x+dx,y+dy) for x,y in origins for dx in range(size) for dy in (-1,0)]
        assert dll.value(0,0,0)==len(coords) and dll.value(1,0,0)==int(not closed)
        for i,(x,y) in enumerate(coords):
            assert (dll.value(2,i,0),dll.value(3,i,0),dll.value(4,i,0))==(x,y,int(not closed))
            if not closed:
                slot=i%(size*2);start=(1016 if size==1 else 1008)+slot*4
                for j in range(4):assert dll.value(5,i,j)==(7<<12)|(start+j)
                for j in range(4,8):assert dll.value(5,i,j)&1023==0
        frames+=1
    return {'status':'PASS','door_router_cases':routes,'door_frame_cases':frames,'source_functions':names,'scope':'Production C router and drawing/flag logic; explicit host flag/location/draw/VRAM services. Canonical table and palettes retained. Full VRAM animation, tasks and sprites require emulator.'}
