"""Execute original Building initializer, dispatch and TV queue using native frames."""
import re,struct
from frontier_07d_common import ROOT
from frontier_07c_animation_checks import raw_4bpp
from dive_04_c_checks import function,library

def frame_table(repo):
    src=(repo/'src/tileset_anims.c').read_text();sym='gTilesetAnims_Building_TvTurnedOn'
    decs=dict(re.findall(r'const u16 ('+sym+r'_Frame\d+)\[\] = INCGFX_U16\("([^"]+)"',src))
    table=re.search(r'const u16 \*const '+sym+r'\[\] = \{.*?\};',src,re.S)[0];refs=re.findall(sym+r'_Frame\d+',table)
    return {'symbol':sym,'table':table,'refs':refs,'paths':[decs[n] for n in refs],'start':496,'tiles':4}

def checks(folder):
    src=(ROOT/'src/tileset_anims.c').read_text();table=frame_table(ROOT)
    payloads={name:raw_4bpp(ROOT/path,4) for name,path in zip(table['refs'],table['paths'])}
    prefix='''#include <stdint.h>
#include <string.h>
typedef uint8_t u8;typedef uint16_t u16;
#define ARRAY_COUNT(a) (sizeof(a)/sizeof((a)[0]))
#define TILE_SIZE_4BPP 32
#define TILE_OFFSET_4BPP(n) ((n)*TILE_SIZE_4BPP)
static u8 vram[65536];
#define BG_VRAM vram
static u16 sPrimaryTilesetAnimCounter,sPrimaryTilesetAnimCounterMax;
static void (*sPrimaryTilesetAnimCallback)(u16);
static int copies,lastOffset,lastSize;
static void AppendTilesetAnimToBuffer(const u16 *src,u16 *dst,u16 size){lastOffset=(u8 *)dst-vram;lastSize=size;memcpy(dst,src,size);copies++;}
static void TilesetAnim_Building(u16);
static void QueueAnimTiles_Building_TVTurnedOn(u16);
'''
    frames=''.join('static const u16 '+n+'[]={'+','.join(str(x) for x in struct.unpack('<%dH'%(len(raw)//2),raw))+'};\n' for n,raw in payloads.items())
    funcs=['InitTilesetAnim_Building','TilesetAnim_Building','QueueAnimTiles_Building_TVTurnedOn']
    source=prefix+frames+table['table']+'\n'+'\n'.join(function(src,n) for n in funcs)+'''
void reset(void){memset(vram,0x55,sizeof(vram));InitTilesetAnim_Building();}
void tick(int t){copies=0;sPrimaryTilesetAnimCallback(t);}
int value(int f,int i){switch(f){case 0:return copies;case 1:return lastOffset;case 2:return lastSize;case 3:return vram[i];case 4:return sPrimaryTilesetAnimCounter;case 5:return sPrimaryTilesetAnimCounterMax;}return -1;}
'''
    dll=library(folder,'factory_building_animation',source);dll.reset();assert dll.value(4,0)==0 and dll.value(5,0)==256;calls=0
    for timer in range(256):
        dll.tick(timer);assert dll.value(0,0)==int(timer%8==0)
        if timer%8==0:
            raw=payloads[table['refs'][(timer//8)%len(table['refs'])]]
            assert dll.value(1,0)==496*32 and dll.value(2,0)==128
            assert bytes(dll.value(3,496*32+i) for i in range(128))==raw;calls+=1
        assert dll.value(3,496*32-1)==0x55 and dll.value(3,500*32)==0x55
    return {'status':'PASS','ticks':256,'queue_updates':calls,'frames':len(table['refs']),'source_functions':funcs,'scope':'Original production C Building callback and VRAM queue execute on host with explicit buffer services and native 4bpp TV frames. Full GBA rendering requires emulator.'}
