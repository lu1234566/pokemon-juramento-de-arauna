"""Host fixtures execute unchanged production puzzle functions and native writes.

Task/audio/party access are stubs; predicates, bit masks and fieldmap writes are
copied verbatim from production source, whose complete bytes are hash-frozen.
This is a host regression check, not a ROM/emulator claim.
"""
import ctypes,json,re,subprocess
from pathlib import Path
from build_cavernas_03b import ROOT,OUT,NAMES
from render_native_map import words

HOST_CONSTANTS=['FLAG_SYS_BRAILLE_DIG','FLAG_SYS_REGISTEEL_PUZZLE_COMPLETED','FLAG_SYS_REGIROCK_PUZZLE_COMPLETED','FLAG_SYS_BRAILLE_REGICE_COMPLETED','FLAG_TEMP_REGICE_PUZZLE_STARTED','FLAG_TEMP_REGICE_PUZZLE_FAILED','VAR_REGICE_STEPS_1','VAR_REGICE_STEPS_2','VAR_REGICE_STEPS_3']
FUNCTIONS=['ShouldDoBrailleDigEffect','DoBrailleDigEffect','CheckRelicanthWailord','ShouldDoBrailleRegirockEffect','DoBrailleRegirockEffect','ShouldDoBrailleRegisteelEffect','DoBrailleRegisteelEffect','ShouldDoBrailleRegicePuzzle']

def function(text,name):
    start=re.search(r'^(?:static )?(?:bool8|void) '+re.escape(name)+r'\([^\n;]*\)\n\{',text,re.M).start()
    pos=text.index('{',start);depth=1;end=pos+1
    while depth:
        depth+=(text[end]=='{')-(text[end]=='}');end+=1
    return text[start:end]+'\n'

def compile_puzzles(folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    source=(ROOT/'src/braille_puzzles.c').read_text();array=re.search(r'static const u8 sRegicePathCoords\[\]\[2\] =\n\{.*?\n\};',source,re.S)[0]
    macros='\n'.join(line for line in (ROOT/'include/global.fieldmap.h').read_text().splitlines() if line.startswith('#define MAPGRID_'))
    bridge=r'''
#include <stdint.h>
#include <string.h>
typedef uint8_t u8; typedef uint8_t bool8; typedef uint16_t u16; typedef int32_t s32;
#define TRUE 1
#define FALSE 0
#define MAP_OFFSET 7
#define ARRAY_COUNT(a) (sizeof(a)/sizeof((a)[0]))
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/metatile_labels.h"
#include "constants/species.h"
#define MON_DATA_SPECIES_OR_EGG 0
#define SE_BANG 0
struct Save {struct {u8 mapGroup,mapNum;} location;struct {s32 x,y;} pos;};
static struct Save save; static struct Save *gSaveBlock1Ptr=&save;
static u8 flags[65536]; static u16 vars[65536];
struct Mon {u16 species;};static struct Mon gPlayerParty[6];static u8 gPlayerPartyCount;
static bool8 sIsRegisteelPuzzle;
static bool8 FlagGet(u16 n){return flags[n];}
static void FlagSet(u16 n){flags[n]=1;}
static void FlagClear(u16 n){flags[n]=0;}
static u16 VarGet(u16 n){return vars[n];}
static void VarSet(u16 n,u16 v){vars[n]=v;}
static u16 GetMonData(struct Mon *m,int field,int p){(void)field;(void)p;return m->species;}
static void CalculatePlayerPartyCount(void){int i;gPlayerPartyCount=0;for(i=0;i<6;i++)if(gPlayerParty[i].species)gPlayerPartyCount++;}
static void DrawWholeMapView(void){}
static void PlaySE(int se){(void)se;}
static void UnlockPlayerFieldControls(void){}
static u16 cells[40*60];
static struct {u16 *map;s32 width,height;} gBackupMapLayout={cells,40,60};
static bool8 AreCoordsWithinMapGridBounds(s32 x,s32 y){return x>=0&&y>=0&&x<40&&y<60;}
'''+macros+'\n'+function((ROOT/'src/fieldmap.c').read_text(),'MapGridSetMetatileIdAt')+array+'\n'+''.join(function(source,n) for n in FUNCTIONS)+r'''
void test_reset(int map,int x,int y){memset(flags,0,sizeof(flags));memset(vars,0,sizeof(vars));memset(gPlayerParty,0,sizeof(gPlayerParty));memset(cells,0,sizeof(cells));save.location.mapGroup=map>>8;save.location.mapNum=map&255;save.pos.x=x;save.pos.y=y;}
void test_pos(int x,int y){save.pos.x=x;save.pos.y=y;}
void test_flag(int n,int v){flags[n]=v;}
int test_getflag(int n){return flags[n];}
void test_var(int n,int v){vars[n]=v;}
int test_getvar(int n){return vars[n];}
void test_party(int i,int species){gPlayerParty[i].species=species;}
void test_cell(int x,int y,int word){cells[x+7+(y+7)*40]=word;}
int test_read(int x,int y){return cells[x+7+(y+7)*40];}
void test_open(int mode){if(mode==0)DoBrailleDigEffect();else if(mode==1)DoBrailleRegisteelEffect();else DoBrailleRegirockEffect();}
int test_map(int mode){switch(mode){case 0:return MAP_SEALED_CHAMBER_OUTER_ROOM;case 1:return MAP_ANCIENT_TOMB;case 2:return MAP_ISLAND_CAVE;default:return MAP_DESERT_RUINS;}}
int test_species(int mode){return mode==0?SPECIES_WAILORD:SPECIES_RELICANTH;}
'''
    bridge+='\nint test_constant(int i){const int values[]={'+','.join(HOST_CONSTANTS)+'};return values[i];}\n'
    (folder/'puzzles.c').write_text(bridge);target=folder/'puzzles.so'
    subprocess.run(['cc','-Wall','-Wextra','-Werror','-shared','-fPIC','-iquote',str(ROOT/'include'),str(folder/'puzzles.c'),'-o',str(target)],check=True,capture_output=True,text=True)
    dll=ctypes.CDLL(str(target))
    for n in FUNCTIONS:
        if n.startswith(('Should','Check')):getattr(dll,n).restype=ctypes.c_uint8
    return dll

def constants():
    result={}
    for name in ('flags','vars','metatile_labels'):
        result.update({k:int(v,0) for k,v in re.findall(r'^#define (\w+)\s+(0x[0-9a-fA-F]+|\d+)\b',(ROOT/f'include/constants/{name}.h').read_text(),re.M)})
    return result

def script_writes(name,label):
    text=(ROOT/f'data/maps/{name}/scripts.inc').read_text();block=text.split(label+'::')[1].split('\n\n')[0];labels=constants()
    return [(int(x),int(y),labels[mid]|(0xc00 if collision=='TRUE' else 0)) for x,y,mid,collision in re.findall(r'setmetatile (\d+), (\d+), (METATILE_\w+), (TRUE|FALSE)',block)]

def run(folder):
    dll=compile_puzzles(folder);c=constants();c.update({n:dll.test_constant(i) for i,n in enumerate(HOST_CONSTANTS)});checks=[]
    def ok(cond,label):
        assert cond,label;checks.append(label)
    def flag(label,value=1):dll.test_flag(c[label],value)
    def reset(mode,x,y):dll.test_reset(dll.test_map(mode),x,y)
    # Dig at each supported wall position; flag, map and position negatives.
    for x in (9,10,11):
        reset(0,x,3);ok(dll.ShouldDoBrailleDigEffect()==1,f'Dig allowed at {x},3')
        flag('FLAG_SYS_BRAILLE_DIG');ok(dll.ShouldDoBrailleDigEffect()==0,f'Dig already opened at {x},3')
    for mode,x,y in [(0,8,3),(0,10,4),(1,10,3)]:
        reset(mode,x,y);ok(dll.ShouldDoBrailleDigEffect()==0,f'Dig rejects map/position {mode},{x},{y}')
    # Exactly the inherited Emerald party order, including shorter/full parties.
    for count in (2,6):
        reset(0,0,0)
        for i in range(count):dll.test_party(i,1)
        dll.test_party(0,dll.test_species(0));dll.test_party(count-1,dll.test_species(1))
        ok(dll.CheckRelicanthWailord()==1,f'Party order valid ({count} members)')
        dll.test_party(0,dll.test_species(1));dll.test_party(count-1,dll.test_species(0))
        ok(dll.CheckRelicanthWailord()==0,f'Reversed party rejected ({count} members)')
    reset(0,0,0);dll.test_party(0,dll.test_species(0));dll.test_party(1,1);ok(dll.CheckRelicanthWailord()==0,'Missing last Relicanth rejected')
    # Ancient Tomb Flash center and shared Desert Ruins Rock Smash dependency.
    for mode,fn,positions,completed in [(1,dll.ShouldDoBrailleRegisteelEffect,[(8,25)],'FLAG_SYS_REGISTEEL_PUZZLE_COMPLETED'),(3,dll.ShouldDoBrailleRegirockEffect,[(5,23),(6,23),(7,23)],'FLAG_SYS_REGIROCK_PUZZLE_COMPLETED')]:
        for x,y in positions:
            reset(mode,x,y);ok(fn()==1,f'Field move predicate allows {mode}:{x},{y}')
            flag(completed);ok(fn()==0,f'Completed field move rejected {mode}:{x},{y}')
        reset(mode,8,24);ok(fn()==0,f'Field move wrong position {mode}')
        reset(2,*positions[0]);ok(fn()==0,f'Field move wrong map {mode}')
    contract=json.loads((OUT/'functional_contract.json').read_text());path=contract['regice_perimeter']
    reset(2,8,21);ok(dll.ShouldDoBrailleRegicePuzzle()==0,'Regice inactive does not start automatically')
    flag('FLAG_TEMP_REGICE_PUZZLE_STARTED');ok(dll.ShouldDoBrailleRegicePuzzle()==0,'Regice incomplete lap rejected')
    for x,y in path:
        dll.test_pos(x,y);dll.ShouldDoBrailleRegicePuzzle()
    ok([dll.test_getvar(c[f'VAR_REGICE_STEPS_{i}']) for i in (1,2,3)]==[65535,65535,15],'Regice all 36 mask bits reached')
    dll.test_pos(4,22);ok(dll.ShouldDoBrailleRegicePuzzle()==0,'Complete Regice lap needs return to inscription')
    dll.test_pos(8,21);ok(dll.ShouldDoBrailleRegicePuzzle()==1,'Complete Regice lap opens only at 8,21')
    flag('FLAG_SYS_BRAILLE_REGICE_COMPLETED');ok(dll.ShouldDoBrailleRegicePuzzle()==0,'Regice completed flag blocks repeated puzzle')
    perimeter=set(map(tuple,path));walk=[(8,21),(9,21)]
    while len(walk)<len(perimeter):
        x,y=walk[-1];neighbors=[p for p in perimeter if abs(p[0]-x)+abs(p[1]-y)==1 and p!=walk[-2]]
        assert len(neighbors)==1;walk.append(neighbors[0])
    ok(set(walk)==perimeter and abs(walk[-1][0]-8)+abs(walk[-1][1]-21)==1,'Regice perimeter is a continuous closed 36-cell lap')
    reset(2,8,21);flag('FLAG_TEMP_REGICE_PUZZLE_STARTED')
    for x,y in walk[:-1]:dll.test_pos(x,y);dll.ShouldDoBrailleRegicePuzzle()
    dll.test_pos(8,21);ok(dll.ShouldDoBrailleRegicePuzzle()==0,'Regice 35-cell partial lap cannot open')
    dll.test_pos(*walk[-1]);dll.ShouldDoBrailleRegicePuzzle();dll.test_pos(8,21)
    ok(dll.ShouldDoBrailleRegicePuzzle()==1,'Regice continuous physical lap and return opens')
    reset(2,8,25);flag('FLAG_TEMP_REGICE_PUZZLE_STARTED');ok(dll.ShouldDoBrailleRegicePuzzle()==0 and dll.test_getflag(c['FLAG_TEMP_REGICE_PUZZLE_FAILED'])==1 and dll.test_getflag(c['FLAG_TEMP_REGICE_PUZZLE_STARTED'])==0,'Regice interior step fails and clears start')
    reset(2,8,21);flag('FLAG_TEMP_REGICE_PUZZLE_STARTED');flag('FLAG_TEMP_REGICE_PUZZLE_FAILED');ok(dll.ShouldDoBrailleRegicePuzzle()==0,'Regice failed session blocked')
    reset(1,8,21);flag('FLAG_TEMP_REGICE_PUZZLE_STARTED');ok(dll.ShouldDoBrailleRegicePuzzle()==0,'Regice wrong map rejected')
    # Actual production C fieldmap writer preserves elevation; predicates open
    # exactly the six native IDs. Script collision TRUE differs on top rows.
    states={}
    for n,mode,top_y,x0,completed in [('SealedChamber_OuterRoom',0,1,9,'FLAG_SYS_BRAILLE_DIG'),('AncientTomb',1,19,7,'FLAG_SYS_REGISTEEL_PUZZLE_COMPLETED'),('DesertRuins',3,19,7,'FLAG_SYS_REGIROCK_PUZZLE_COMPLETED')]:
        reset(mode,0,0)
        closed_label=n+'_EventScript_'+('CloseInnerRoomEntrance' if mode==0 else 'HideRegiEntrance')
        closed=script_writes(n,closed_label)
        for x,y,v in closed:dll.test_cell(x,y,0x3000|v)
        dll.test_open(0 if mode==0 else 1 if mode==1 else 2)
        opened=[(x0+dx,top_y+dy,dll.test_read(x0+dx,top_y+dy)) for dy in (0,1) for dx in (0,1,2)]
        ok([v&1023 for x,y,v in opened]==[554,555,556,562,563,564],n+' actual C six opening IDs')
        ok([v&0xc00 for x,y,v in opened]==[0,0,0,0xc00,0,0xc00],n+' actual C center passable, sides closed')
        ok(all(v&0xf000==0x3000 for x,y,v in opened),n+' real fieldmap writer preserves elevation')
        ok(dll.test_getflag(c[completed])==1,n+' actual C completion flag set')
        if n in NAMES:states[n]={'closed':closed,'open':[(x,y,v&0xfff) for x,y,v in opened]}
    states['IslandCave']={'closed':script_writes('IslandCave','IslandCave_EventScript_HideRegiEntrance'),'open':script_writes('IslandCave','IslandCave_EventScript_OpenRegiEntrance')}
    ok(len(states['IslandCave']['open'])==6 and [v&1023 for x,y,v in states['IslandCave']['open']]==[554,555,556,562,563,564],'Regice script opens exact six native pieces')
    # Execute unchanged fieldmap writer on script output, not an alternate grid update.
    for label,patch in states['IslandCave'].items():
        reset(2,0,0)
        for x,y,v in patch:dll.test_cell(x,y,0x3000);dll.MapGridSetMetatileIdAt(x+7,y+7,v)
        ok(all(dll.test_read(x,y)==0x3000|v for x,y,v in patch),'Regice '+label+' script write preserves elevation/collision')
    return {'status':'PASS','checks':len(checks),'cases':checks,'source':'src/braille_puzzles.c and src/fieldmap.c extracted verbatim','scope':'host predicates/masks/writes; script branches preserved by whole-file hashes, not emulated','door_states':states}
