"""Execute the original Pike curtain task against real dynamic metatile IDs."""
import re
from frontier_07e_common import ROOT
from dive_04_c_checks import function,library

def checks(folder):
    src=(ROOT/'src/field_specials.c').read_text()
    start=int(re.search(r'#define METATILE_BattlePike_CurtainFrames_Start\s+(0x\w+)',(ROOT/'include/constants/metatile_labels.h').read_text())[1],16)
    names=['CloseBattlePikeCurtain','Task_CloseBattlePikeCurtain']
    prefix='''#include <stdint.h>
#include <string.h>
typedef uint8_t u8;typedef uint16_t u16;typedef int16_t s16;
#define MAP_OFFSET 7
#define METATILE_ROW_WIDTH 8
#define CURTAIN_HEIGHT 4
#define CURTAIN_WIDTH 3
#define tFrameTimer data
#define tCurrentFrame data[3]
static struct {s16 data[16];} gTasks[1];
static struct {struct {s16 x,y;} pos;} saveBlock;
static typeof(saveBlock) *gSaveBlock1Ptr=&saveBlock;
static void (*taskCallback)(u8);
static u16 grid[40][40];
static int writes,draws,destroys,resumes,priority;
static void Task_CloseBattlePikeCurtain(u8);
static u8 CreateTask(void (*fn)(u8),u8 prio){taskCallback=fn;priority=prio;return 0;}
static void DestroyTask(u8 id){(void)id;destroys++;taskCallback=0;}
static void ScriptContext_Enable(void){resumes++;}
static void MapGridSetMetatileIdAt(int x,int y,u16 id){grid[y][x]=id;writes++;}
static void DrawWholeMapView(void){draws++;}
'''+f'#define METATILE_BattlePike_CurtainFrames_Start {start}\n'
    source=prefix+'\n'.join(function(src,n) for n in names)+'''
void reset(int x,int y){memset(grid,0x55,sizeof(grid));memset(gTasks,0,sizeof(gTasks));writes=draws=destroys=resumes=0;saveBlock.pos.x=x;saveBlock.pos.y=y;CloseBattlePikeCurtain();}
void tick(void){if(taskCallback)taskCallback(0);}
int value(int key,int x,int y){switch(key){case 0:return writes;case 1:return draws;case 2:return destroys;case 3:return resumes;case 4:return grid[y][x];case 5:return priority;case 6:return gTasks[0].data[x];}return -1;}
'''
    dll=library(folder,'pike_curtain',source);cases=0;changed=set()
    # The production scripts close the curtain on lobby (5,3) and corridor (6,3).
    for px,py in ((5,3),(6,3),(6,5),(1,3),(12,10)):
        dll.reset(px,py);assert dll.value(5,0,0)==8
        for i in range(3):assert dll.value(6,i,0)==4
        assert dll.value(6,3,0)==0
        for tick in range(1,17):
            dll.tick();frames=min(tick//4,3)
            assert dll.value(0,0,0)==12*frames and dll.value(1,0,0)==frames
            assert dll.value(2,0,0)==dll.value(3,0,0)==int(tick>=12)
            frame=frames-1
            for y in range(40):
                for x in range(40):
                    inside=frames>0 and px+6<=x<px+9 and py+4<=y<py+8
                    expected=(start+x-(px+6)+(y-(py+4))*8+frame*32) if inside else 0x5555
                    assert dll.value(4,x,y)==expected,(px,py,tick,x,y)
                    if inside:changed.add(expected)
            cases+=1
    assert len(changed)==36
    return {'status':'PASS','ticks_and_positions':cases,'positions':5,'duration_ticks':12,'frame_ticks':[4,8,12],'metatile_ids':sorted(changed),'writes_per_transition':36,'redraws_per_transition':3,'script_resumes_per_transition':1,'source_functions':names,'scope':'Original production C initialization and task run on host with explicit task, map-grid, redraw and script-resume services. Actual 3x4 frame IDs, timing and map-offset footprint checked; no script interpreter or GBA gameplay.'}
