"""Host fixtures execute the production floor generator and challenge lifecycle."""
import ctypes,re
from pathlib import Path
from dive_04_c_checks import library
from trainer_hill_06a_common import ROOT,NAMES,MODES,inventory,floors,runtime_words

def function(text,name):
    match=re.search(r'^(?:static )?\w+ '+name+r'\([^;]*?\)(?:\s*//[^\n]*)?\n\{',text,re.M)
    assert match,name
    start=match.start();end=text.index('{',start)+1;depth=1
    while depth:depth+=(text[end]=='{')-(text[end]=='}');end+=1
    return text[start:end]

def checks(folder):
    text=(ROOT/'src/trainer_hill.c').read_text();node,ls,maps=inventory(ROOT)
    ids={n:node['layouts'].index(ls[maps[n]['layout']])+1 for n in NAMES}
    defines=''.join(f'#define LAYOUT_TRAINER_HILL_{n.split("TrainerHill_")[1].upper()} {idx}\n' for n,idx in ids.items() if n!='TrainerHill_Elevator')
    maximum=re.search(r'^#define HILL_MAX_TIME\s+(\d+)',text,re.M)[1]
    source='''#include <stdint.h>
#include <string.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef int32_t s32;typedef uint8_t bool8;typedef uint32_t bool32;
#define TRUE 1
#define FALSE 0
#include "constants/trainer_hill.h"
#define NUM_METATILES_IN_PRIMARY 512
#define ELEVATION_DEFAULT 3
#define PACK_ELEVATION(v) ((v)<<12)
#define PACK_COLLISION(v) ((v)<<10)
#define PACK_METATILE(v) ((v)&1023)
'''+defines+'#define HILL_MAX_TIME '+maximum+'''
struct FloorMap {u8 metatileData[256];u16 collisionData[16];};
struct Floor {struct FloorMap map;};
static struct {struct {int numFloors;} challenge;struct Floor floors[4];} data;
static __typeof__(data) *sHillData=&data;
struct Layout {const u16 *map;};static struct Layout layout;
static struct {int mapLayoutId;struct Layout *mapLayout;} gMapHeader;
static struct {u16 *map;int width,height;} gBackupMapLayout;
static u16 fixed[336],generated[1085];
static int setups,frees,loads,onLoads,timerCalls,clearCalls,bagAccept,bagAdds,valid;
struct HillState {u32 timer,bestTime;int mode,field_3D6E_0f,unk_3D6C,spokeToOwner,checkedFinalTime,maybeECardScanDuringChallenge,receivedPrize,hasLost;};
static struct {struct HillState trainerHill;u32 trainerHillTimes[4];} save;
static __typeof__(save) *gSaveBlock1Ptr=&save;
static struct {struct {int trainerFlags,unk_EF9;} frontier;} save2;
static __typeof__(save2) *gSaveBlock2Ptr=&save2;
static int gBattleOutcome,gSpecialVar_Result;static u8 gStringVar2[32];
static u32 *counter;
static void SetUpDataStruct(void){setups++;}
static void FreeDataStruct(void){frees++;}
static void InitMapFromSavedGame(void){loads++;}
static void RunOnLoadMapScript(void){onLoads++;}
static void TrainerHillDummy(void){}
static int ReadTrainerHillAndValidate(void){return valid;}
static void SetTrainerHillVBlankCounter(u32 *p){counter=p;timerCalls++;}
static void ClearTrainerHillVBlankCounter(void){counter=0;clearCalls++;}
static u16 GetPrizeItemId(void){return 123;}
static int AddBagItem(u16 id,int num){if(id!=123 || num!=1)return 0;bagAdds++;return bagAccept;}
static void CopyItemName(u16 id,u8 *p){p[0]=(u8)id;}
'''
    names=['GetCurrentTrainerHillMapId','InTrainerHill','GetFloorId','GetMapDataForFloor','GenerateTrainerHillFloorLayout','GetTimerValue','SetTimerValue','TrainerHillStartChallenge','GetOwnerState','GiveChallengePrize','CheckFinalTime','TrainerHillResumeTimer','TrainerHillSetPlayerLost','TrainerHillGetChallengeStatus']
    source+='\n'.join(function(text,n) for n in names)
    source+='''
void setup(int floor,const u8 *metas,const u16 *collision,const u16 *header){
 memset(&data,0,sizeof(data));memset(generated,0xA5,sizeof(generated));memcpy(data.floors[floor].map.metatileData,metas,256);memcpy(data.floors[floor].map.collisionData,collision,32);memcpy(fixed,header,672);
 layout.map=fixed;gMapHeader.mapLayout=&layout;gMapHeader.mapLayoutId=LAYOUT_TRAINER_HILL_1F+floor;setups=frees=loads=onLoads=0;
 GenerateTrainerHillFloorLayout(generated);
}
int word(int i){return generated[i];}
int geometry(int field){const int a[]={gBackupMapLayout.width,gBackupMapLayout.height,setups,frees,loads,onLoads};return a[field];}
int classify(int layoutId){gMapHeader.mapLayoutId=layoutId;return GetCurrentTrainerHillMapId()*10+InTrainerHill();}
int verify(int which){
 memset(&save,0,sizeof(save));memset(&save2,0,sizeof(save2));counter=0;timerCalls=clearCalls=bagAdds=0;bagAccept=valid=1;gSpecialVar_Result=-1;data.challenge.numFloors=4;
 if(which==0){save.trainerHill.timer=77;save.trainerHill.receivedPrize=1;save2.frontier.trainerFlags=55;TrainerHillStartChallenge();return !save.trainerHill.timer && !save.trainerHill.receivedPrize && !save2.frontier.trainerFlags && counter==&save.trainerHill.timer && !save.trainerHill.field_3D6E_0f;}
 if(which==1){valid=0;TrainerHillStartChallenge();return save.trainerHill.field_3D6E_0f==1;}
 if(which==2){save.trainerHill.timer=123;TrainerHillResumeTimer();return counter==&save.trainerHill.timer && timerCalls==1;}
 if(which==3){save.trainerHill.timer=HILL_MAX_TIME+1;TrainerHillResumeTimer();return save.trainerHill.timer==HILL_MAX_TIME && !timerCalls;}
 if(which==4){save.trainerHill.spokeToOwner=1;TrainerHillResumeTimer();return !timerCalls;}
 if(which==5){GetOwnerState();return save.trainerHill.spokeToOwner && gSpecialVar_Result==0 && clearCalls==1;}
 if(which==6){save.trainerHill.spokeToOwner=1;GetOwnerState();return gSpecialVar_Result==1;}
 if(which==7){save.trainerHill.spokeToOwner=save.trainerHill.receivedPrize=save.trainerHill.checkedFinalTime=1;GetOwnerState();return gSpecialVar_Result==2;}
 if(which==8){GiveChallengePrize();return gSpecialVar_Result==0 && save.trainerHill.receivedPrize && bagAdds==1 && gStringVar2[0]==123;}
 if(which==9){save.trainerHill.receivedPrize=1;GiveChallengePrize();return gSpecialVar_Result==2 && !bagAdds;}
 if(which==10){bagAccept=0;GiveChallengePrize();return gSpecialVar_Result==1 && !save.trainerHill.receivedPrize;}
 if(which==11){data.challenge.numFloors=2;GiveChallengePrize();return gSpecialVar_Result==2 && !bagAdds;}
 if(which==12){save.trainerHill.timer=75;save.trainerHill.bestTime=100;save.trainerHill.mode=3;CheckFinalTime();return gSpecialVar_Result==0 && save.trainerHill.checkedFinalTime && save.trainerHill.bestTime==75 && save.trainerHillTimes[3]==75;}
 if(which==13){save.trainerHill.timer=101;save.trainerHill.bestTime=100;CheckFinalTime();return gSpecialVar_Result==1 && save.trainerHill.bestTime==100 && save.trainerHill.checkedFinalTime;}
 if(which==14){save.trainerHill.checkedFinalTime=1;CheckFinalTime();return gSpecialVar_Result==2;}
 if(which==15){TrainerHillSetPlayerLost();TrainerHillGetChallengeStatus();return gSpecialVar_Result==TRAINER_HILL_PLAYER_STATUS_LOST && !save.trainerHill.hasLost;}
 if(which==16){save.trainerHill.maybeECardScanDuringChallenge=1;TrainerHillGetChallengeStatus();return gSpecialVar_Result==TRAINER_HILL_PLAYER_STATUS_ECARD_SCANNED && !save.trainerHill.maybeECardScanDuringChallenge;}
 if(which==17){TrainerHillGetChallengeStatus();return gSpecialVar_Result==TRAINER_HILL_PLAYER_STATUS_NORMAL;}
 if(which==18 || which==19){gMapHeader.mapLayoutId=which==18?LAYOUT_TRAINER_HILL_ENTRANCE:LAYOUT_TRAINER_HILL_ROOF;loads=setups=frees=0;GenerateTrainerHillFloorLayout(generated);return loads==1 && setups==(which==19) && frees==(which==19);}
 return 0;
}
'''
    dll=library(folder,'trainer_hill_real',source)
    dll.setup.argtypes=[ctypes.c_int,ctypes.POINTER(ctypes.c_uint8),ctypes.POINTER(ctypes.c_uint16),ctypes.POINTER(ctypes.c_uint16)]
    word_cases=guard_cases=0
    for key,record in floors(ROOT).items():
        l,expected=runtime_words(ROOT,record);static=__import__('render_native_map').words(ROOT/l['blockdata_filepath'])
        a=(ctypes.c_uint8*256)(*record['ids']);c=(ctypes.c_uint16*16)(*record['collision']);h=(ctypes.c_uint16*336)(*static)
        dll.setup(record['floor'],a,c,h)
        assert [dll.geometry(i) for i in range(6)]==[31,35,1,1,0,1],key
        populated={224+y*31+x for y in range(21) for x in range(16)}
        for y in range(21):
            for x in range(16):assert dll.word(224+y*31+x)==expected[y*16+x],(key,x,y);word_cases+=1
        for i in set(range(1085))-populated:assert dll.word(i)==0xa5a5,(key,'guard',i);guard_cases+=1
    for n,idx in ids.items():
        expected=(int(n[-2])*10+1) if n.endswith(('1F','2F','3F','4F')) else 50 if n.endswith('Roof') else 60 if n.endswith('Entrance') else 0
        assert dll.classify(idx)==expected,(n,idx)
    old_elevator=node['layouts'].index(ls[maps['BattleFrontier_BattleTowerElevator']['layout']])+1
    assert dll.classify(old_elevator)==dll.classify(ids['TrainerHill_Elevator'])==0
    for i in range(20):assert dll.verify(i)==1,('lifecycle',i)
    return {'status':'PASS','generated_cell_words':word_cases,'untouched_buffer_guards':guard_cases,'mode_floor_combinations':16,'layout_classifications':8,'lifecycle_cases':20,'functions':names,'scope':'Production C bodies executed on host. Floor data come from original input bytes; allocation, script dispatch, bag, flag/save and VBlank services are explicit fixtures. No ROM, full event interpreter or battle engine session.'}
