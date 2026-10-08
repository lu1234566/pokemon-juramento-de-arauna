"""Execute the original ferry menu and terrain predicates with host services."""
import ctypes,itertools
from navel_06b_common import ROOT
from trainer_hill_06a_c_checks import function
from dive_04_c_checks import library

def checks(folder):
    text=(ROOT/'src/script_menu.c').read_text()
    source='''#include <stdint.h>
#include <string.h>
#include <stddef.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;
#define TRUE 1
#define FALSE 0
#define FONT_NORMAL 0
#define FONTATTR_MAX_LETTER_WIDTH 0
#define TEXT_SKIP_DRAW 0
#define COPYWIN_FULL 3
#include "constants/items.h"
#include "constants/flags.h"
#include "constants/script_menu.h"
#include "constants/field_specials.h"
static u8 sLilycoveSSTidalSelections[SSTIDAL_SELECTION_COUNT];
static const u8 empty[]={0};static const u8 *sLilycoveSSTidalDestinations[SSTIDAL_SELECTION_COUNT];
static u16 gSpecialVar_0x8004,gSpecialVar_Result;static u8 flags[65536],bag[2048];static int scroll;
static int FlagGet(int id){return flags[id];}
static void FlagSet(int id){flags[id]=1;}
static int CheckBagHasItem(int id,int qty){return qty==1 && bag[id];}
static int GetFontAttribute(int a,int b){(void)a;(void)b;return 8;}
static void ShowScrollableMultichoice(void){scroll++;}
static u32 DisplayTextAndGetWidth(const u8 *s,u32 p){(void)s;return p+8;}
static u8 ConvertPixelWidthToTileWidth(u32 p){(void)p;return 4;}
static u8 CreateWindowFromRect(int a,int b,int c,int d){(void)a;(void)b;(void)c;(void)d;return 0;}
static void SetStandardWindowBorderStyle(int a,int b){(void)a;(void)b;}
static void AddTextPrinterParameterized(int a,int b,const u8 *s,int c,int d,int e,void *f){(void)a;(void)b;(void)s;(void)c;(void)d;(void)e;(void)f;}
static void InitMenuInUpperLeftCornerNormal(int a,int b,int c){(void)a;(void)b;(void)c;}
static void CopyWindowToVram(int a,int b){(void)a;(void)b;}
static void InitMultichoiceCheckWrap(int a,int b,int c,int d){(void)a;(void)b;(void)c;(void)d;}
'''+function(text,'CreateLilycoveSSTidalMultichoice')+'\n'+function(text,'GetLilycoveSSTidalSelection')+'''
void setup(int mode,int items,int enabled,int shown,int scott){
 static const int item[]={ITEM_EON_TICKET,ITEM_MYSTIC_TICKET,ITEM_AURORA_TICKET,ITEM_OLD_SEA_MAP};
 static const int enable[]={FLAG_ENABLE_SHIP_SOUTHERN_ISLAND,FLAG_ENABLE_SHIP_NAVEL_ROCK,FLAG_ENABLE_SHIP_BIRTH_ISLAND,FLAG_ENABLE_SHIP_FARAWAY_ISLAND};
 memset(flags,0,sizeof(flags));memset(bag,0,sizeof(bag));scroll=0;
 for(int i=0;i<4;i++){bag[item[i]]=(items>>i)&1;flags[enable[i]]=(enabled>>i)&1;}
 for(int i=0;i<SSTIDAL_SELECTION_COUNT;i++)sLilycoveSSTidalDestinations[i]=empty;
 flags[FLAG_SHOWN_MYSTIC_TICKET]=shown;flags[FLAG_MET_SCOTT_ON_SS_TIDAL]=scott;gSpecialVar_0x8004=mode;
 CreateLilycoveSSTidalMultichoice();
}
int selection(int i){return sLilycoveSSTidalSelections[i];}
int choose(int i){gSpecialVar_Result=i;GetLilycoveSSTidalSelection();return gSpecialVar_Result;}
int marked(void){return flags[FLAG_SHOWN_MYSTIC_TICKET];}
int scrolled(void){return scroll;}
'''
    dll=library(folder/'ferry','native_ferry',source);cases=choices=0
    for mode,items,enabled,shown,scott in itertools.product(range(2),range(16),range(16),range(2),range(2)):
        dll.setup(mode,items,enabled,shown,scott);expected=[]
        if mode==0:expected=[0]+([1] if scott else [])
        for i in range(4):
            if (items>>i)&1 and (enabled>>i)&1 and (mode==0 or i!=1 or not shown):expected.append(i+2)
        expected.append(6);assert [dll.selection(i) for i in range(7)]==expected+[255]*(7-len(expected))
        assert dll.marked()==int(bool(shown or (mode==1 and items&2 and enabled&2)))
        assert dll.scrolled()==int(len(expected)==7)
        for i,value in enumerate(expected):assert dll.choose(i)==value;choices+=1
        assert dll.choose(127)==127;choices+=1;cases+=1
    behavior=(ROOT/'src/metatile_behavior.c').read_text();names=['MetatileBehavior_IsLadder','MetatileBehavior_IsNonAnimDoor','MetatileBehavior_IsDeepSouthWarp']
    src='#include <stdint.h>\ntypedef uint8_t u8;typedef uint8_t bool8;\n#define TRUE 1\n#define FALSE 0\n#include "constants/metatile_behaviors.h"\n'+'\n'.join(function(behavior,n) for n in names)
    src+='\nint probe(int id,int b){switch(id){'+''.join(f'case {i}:return {n}(b);' for i,n in enumerate(names))+'}return -1;}\n'
    src+='int expected(int id,int b){switch(id){case 0:return b==MB_LADDER;case 1:return b==MB_NON_ANIMATED_DOOR || b==MB_WATER_DOOR || b==MB_DEEP_SOUTH_WARP;case 2:return b==MB_DEEP_SOUTH_WARP;}return -1;}\n'
    bdll=library(folder/'terrain','native_terrain',src)
    for i in range(3):
        for b in range(256):assert bdll.probe(i,b)==bdll.expected(i,b)
    return bdll,{'status':'PASS','ferry_menu_configurations':cases,'ferry_selection_cases':choices,'terrain_predicates':768,'functions':['CreateLilycoveSSTidalMultichoice','GetLilycoveSSTidalSelection',*names],'scope':'Original C functions compiled/executed on host. Bag, flags and UI are explicit fixtures, not a full game or ferry animation session.'}
