"""Execute the native Dome palette callbacks and actual RGB555 fade function."""
import re
from frontier_07b_common import ROOT
from render_native_map import palette
from dive_04_c_checks import function,library

def animation_checks(folder):
    text=(ROOT/'src/tileset_anims.c').read_text();util=(ROOT/'src/util.c').read_text()
    names=['InitTilesetAnim_BattleDome','TilesetAnim_BattleDome','TilesetAnim_BattleDome2','BlendAnimPalette_BattleDome_FloorLights','BlendAnimPalette_BattleDome_FloorLightsNoBlend']
    colors=[]
    for i in range(1,5):colors.append([sum((c>>3)<<(5*j) for j,c in enumerate(rgb)) for rgb in palette(ROOT/f'graphics/battle_frontier/dome_anim{i}.pal')])
    structs=re.search(r'struct PlttData\n\{.*?\};',(ROOT/'include/gba/types.h').read_text(),re.S)[0]
    source='''#include <stdint.h>
#include <stddef.h>
#include <string.h>
typedef uint8_t u8;typedef int8_t s8;typedef uint16_t u16;
#define ARRAY_COUNT(a) (sizeof(a)/sizeof((a)[0]))
#define BG_PLTT_ID(i) ((i)*16)
#define PLTT_SIZE_4BPP 32
#define TASK_NONE 255
#define RGB(r,g,b) ((r)|((g)<<5)|((b)<<10))
static u16 gPlttBufferUnfaded[256],gPlttBufferFaded[256];
static struct {u8 y;u16 blendColor;} gPaletteFade;
static u16 sSecondaryTilesetAnimCounter,sSecondaryTilesetAnimCounterMax,sPrimaryTilesetAnimCounterMax;
static void (*sSecondaryTilesetAnimCallback)(u16);
static int task,copyCount;
static void Task_BattleTransition_Intro(void){}
static int FindTaskIdByFunc(void (*f)(void)){(void)f;return task?0:TASK_NONE;}
static void CpuCopy16(const void *src,void *dst,int size){memcpy(dst,src,size);copyCount++;}
static void TilesetAnim_BattleDome(u16);
static void TilesetAnim_BattleDome2(u16);
static void BlendAnimPalette_BattleDome_FloorLights(u16);
static void BlendAnimPalette_BattleDome_FloorLightsNoBlend(u16);
'''+structs+'\n'+''.join('static const u16 gTilesetAnims_BattleDomePals0_'+str(i)+'[]={'+','.join(map(str,p))+'};\n' for i,p in enumerate(colors))
    source+=re.search(r'static const u16 \*const sTilesetAnims_BattleDomeFloorLightPals\[\] = \{.*?\};',text,re.S)[0]+'\n'+function(util,'BlendPalette')+'\n'+'\n'.join(function(text,n) for n in names)+'''
void reset(int coeff,int color){memset(gPlttBufferUnfaded,0x55,sizeof(gPlttBufferUnfaded));memset(gPlttBufferFaded,0x33,sizeof(gPlttBufferFaded));task=copyCount=0;gPaletteFade.y=coeff;gPaletteFade.blendColor=color;sPrimaryTilesetAnimCounterMax=256;InitTilesetAnim_BattleDome();}
void step(int timer,int active){task=active;if(sSecondaryTilesetAnimCallback)sSecondaryTilesetAnimCallback(timer);}
int value(int mode,int i){switch(mode){case 0:return gPlttBufferUnfaded[i];case 1:return gPlttBufferFaded[i];case 2:return copyCount;case 3:return sSecondaryTilesetAnimCounterMax;case 4:return sSecondaryTilesetAnimCallback==NULL;case 5:return sSecondaryTilesetAnimCounter;}return -1;}
'''
    dll=library(folder,'dome_floor_lights',source);cases=0
    for coeff in range(17):
        for target in (0,0x7fff,0x4210):
            dll.reset(coeff,target);assert dll.value(3,0)==256 and dll.value(5,0)==0
            for timer in range(16):
                dll.step(timer,0);assert dll.value(2,0)==timer//4+1
                frame=timer//4
                for i,c in enumerate(colors[frame]):
                    channels=[(c>>(j*5))&31 for j in range(3)]
                    dest=[(target>>(j*5))&31 for j in range(3)]
                    expected=sum((v+(dest[j]-v)*coeff//16)<<(j*5) for j,v in enumerate(channels))
                    assert dll.value(0,128+i)==c and dll.value(1,128+i)==expected
                for i in (0,127,144,255):assert dll.value(0,i)==0x5555 and dll.value(1,i)==0x3333
                cases+=1
    # The intro switches callbacks, suspends fade and countdown while its task
    # exists, then performs exactly 32 palette updates before disabling itself.
    dll.reset(7,0x7fff);dll.step(0,1);assert dll.value(3,0)==32
    saved=[dll.value(1,128+i) for i in range(16)]
    for timer in range(4,20):
        dll.step(timer,1);assert dll.value(3,0)==32
        assert saved==[dll.value(1,128+i) for i in range(16)];cases+=1
    for n in range(32):
        dll.step(n*4,0);assert dll.value(3,0)==31-n and dll.value(4,0)==int(n==31);cases+=1
    count=dll.value(2,0);dll.step(128,0);assert dll.value(2,0)==count;cases+=1
    return {'status':'PASS','cases':cases,'palette':8,'frames':4,'animated_indices':[13,15],'fade_coefficients':17,'transition_updates':32,'source_functions':names+['BlendPalette'],'scope':'Actual production C callbacks, RGB555 fade and task-state branches. Explicit host task lookup and CPU-copy services; GBA display and battle interpreter require emulator.'}
