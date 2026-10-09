"""Production General callback and native 4bpp frame payloads for water garden."""
import re,struct
from frontier_07c_common import ROOT
from render_native_map import indexed_tiles
from dive_04_c_checks import function,library
FAMILIES=[('Flower',508,4),('Water',432,30),('SandWaterEdge',464,10),('Waterfall',496,6),('LandWaterEdge',480,10)]

def frame_tables(repo):
    src=(repo/'src/tileset_anims.c').read_text();decs=dict(re.findall(r'const u16 (gTilesetAnims_General_\w+)\[\] = INCGFX_U16\("([^"]+)"',src));result={}
    for name,start,count in FAMILIES:
        sym='gTilesetAnims_General_'+name;table=re.search(r'const u16 \*const '+sym+r'\[\] = \{.*?\};',src,re.S)[0]
        refs=re.findall(sym+r'_Frame\d+',table);result[name]={'symbol':sym,'table':table,'paths':[decs[n] for n in refs],'refs':refs,'start':start,'tiles':count}
    return result

def raw_4bpp(path,count):
    im,row,n=indexed_tiles(path);assert n==count
    data=bytearray()
    for k in range(count):
        pixels=list(im.crop((k%row*8,k//row*8,k%row*8+8,k//row*8+8)).getdata())
        data.extend(pixels[i]|pixels[i+1]<<4 for i in range(0,64,2))
    return bytes(data)

def checks(folder):
    src=(ROOT/'src/tileset_anims.c').read_text();tables=frame_tables(ROOT);payloads={};definitions=''
    for d in tables.values():
        for name,path in zip(d['refs'],d['paths']):
            raw=raw_4bpp(ROOT/path,d['tiles']);payloads[name]=raw
        definitions+=d['table']+'\n'
    prefix='''#include <stdint.h>
#include <string.h>
#include <stddef.h>
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
static void TilesetAnim_General(u16);
'''+''.join('static void QueueAnimTiles_General_'+n+'(u16);\n' for n,_,_ in FAMILIES)
    frames=''.join('static const u16 '+name+'[]={'+','.join(str(x) for x in struct.unpack('<%dH'%(len(raw)//2),raw))+'};\n' for name,raw in payloads.items())
    funcs=['InitTilesetAnim_General','TilesetAnim_General',*('QueueAnimTiles_General_'+n for n,_,_ in FAMILIES)]
    source=prefix+frames+definitions+'\n'.join(function(src,n) for n in funcs)+'''
void reset(void){memset(vram,0x55,sizeof(vram));InitTilesetAnim_General();}
void tick(int t){copies=0;sPrimaryTilesetAnimCallback(t);}
int value(int field,int i){switch(field){case 0:return copies;case 1:return lastOffset;case 2:return lastSize;case 3:return vram[i];case 4:return sPrimaryTilesetAnimCounter;case 5:return sPrimaryTilesetAnimCounterMax;}return -1;}
'''
    dll=library(folder,'general_garden_animation',source);dll.reset();assert dll.value(4,0)==0 and dll.value(5,0)==256;calls=0
    for timer in range(256):
        dll.tick(timer);phase=timer%16;assert dll.value(0,0)==int(phase<5)
        if phase<5:
            name,start,count=FAMILIES[phase];d=tables[name];raw=payloads[d['refs'][(timer//16)%len(d['refs'])]]
            assert dll.value(1,0)==start*32 and dll.value(2,0)==count*32
            assert bytes(dll.value(3,start*32+i) for i in range(len(raw)))==raw;calls+=1
        assert dll.value(3,432*32-1)==0x55 and dll.value(3,512*32)==0x55
    return {'status':'PASS','ticks':256,'queue_updates':calls,'water_frames':8,'flower_sequence':[0,1,0,2],'source_functions':funcs,'scope':'Actual production C callback, queue functions and canonical frame tables. Explicit host VRAM-buffer copy; real frame bytes decoded from indexed native PNGs. No GBA display execution.'}
