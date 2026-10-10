"""Original facade-door router/drawing and both flag callbacks, with host services."""
import re,struct
import ctypes
from pathlib import Path
from frontier_07i_common import ROOT,NAMES,flags,door_records,inventory,renderer
from frontier_07c_c_checks import extract
from frontier_07c_animation_checks import raw_4bpp
from dive_04_c_checks import library,function
from render_native_map import indexed_tiles
def door_indexed(path):
    from PIL import Image
    im=Image.open(path)
    if im.mode!='P':return indexed_tiles(path)
    out=Image.new('L',im.size);out.putdata([v%16 for v in im.get_flattened_data()])
    return out,im.width//8,im.width*im.height//64
def converter_checks(folder,paths):
    # Run gbagfx's actual bit-depth and tile-order functions without libpng.
    png=(ROOT/'tools/gbagfx/convert_png.c').read_text();gfx=(ROOT/'tools/gbagfx/gfx.c').read_text()
    source='#include <stdlib.h>\n#include <stdbool.h>\n'+extract(png,'ConvertBitDepth')+'\n'+extract(gfx,'AdvanceMetatilePosition')+'\n'+extract(gfx,'ConvertToTiles4Bpp')+'''
void pack(unsigned char *src,unsigned char *out,int w,int h){unsigned char *p=ConvertBitDepth(src,8,4,w*h);ConvertToTiles4Bpp(p,out,w*h/64,w/8,1,1,false);free(p);}
'''
    dll=library(folder,'gbagfx_door_conversion',source);dll.pack.argtypes=[ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int,ctypes.c_int]
    from PIL import Image
    for path in paths:
        original=Image.open(ROOT/path)
        if original.mode=='P':pixels=list(original.get_flattened_data())
        else:pixels=list(indexed_tiles(ROOT/path)[0].get_flattened_data())
        a=(ctypes.c_ubyte*len(pixels))(*pixels);b=(ctypes.c_ubyte*(len(pixels)//2))();dll.pack(a,b,original.width,original.height)
        im,row,n=door_indexed(ROOT/path);expected=bytearray()
        for i in range(n):
            p=list(im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8)).get_flattened_data());expected.extend(p[j]|p[j+1]<<4 for j in range(0,64,2))
        assert bytes(b)==bytes(expected),path
    return {'status':'PASS','assets':len(paths),'functions':['ConvertBitDepth','AdvanceMetatilePosition','ConvertToTiles4Bpp'],'scope':'Production gbagfx C packing, including the Poke Mart PNG indices above 15. libpng decoding supplied as explicit Pillow pixel fixture.'}
def door_table(repo):
    text=(repo/'src/field_door.c').read_text();table=re.search(r'static const struct DoorGraphics sDoorAnimGraphicsTable\[\] =\n\{.*?\n\};',text,re.S)[0]
    labels={k:int(v,16) for k,v in re.findall(r'#define (METATILE_\w+)\s+(0x[\da-fA-F]+)',(repo/'include/constants/metatile_labels.h').read_text())}
    paths=dict(re.findall(r'static const u8 (sDoorAnimTiles_\w+)\[\] = INCGFX_U8\("([^"]+)"',text))
    pals={k:[int(n) for n in re.findall(r'\d+',v)] for k,v in re.findall(r'static const u8 (sDoorAnimPalettes_\w+)\[\] = \{(.*?)\}',text,re.S)}
    out={}
    for i,(name,sound,size,tiles,pal) in enumerate(re.findall(r'\{(METATILE_\w+|0x[\da-fA-F]+),\s*(DOOR_SOUND_\w+),\s*(\d+),\s*(sDoorAnimTiles_\w+),\s*(sDoorAnimPalettes_\w+)',table)):
        mid=labels[name] if name in labels else int(name,16)
        if mid not in out:out[mid]={'index':i,'size':int(size),'path':paths[tiles],'palettes':pals[pal],'sound':sound}
    return out
def doors(folder,base):
    text=(ROOT/'src/field_door.c').read_text();table=re.search(r'static const struct DoorGraphics sDoorAnimGraphicsTable\[\] =\n\{.*?\n\};',text,re.S)[0]
    special='\n'.join(re.findall(r'static const struct DoorGraphics sDoorGraphics_\w+\s*=\s*\{.*?\};',text,re.S));refs=table+special
    ts=sorted(set(re.findall(r'\bsDoorAnimTiles_\w+',refs)));ps=sorted(set(re.findall(r'\bsDoorAnimPalettes_\w+',refs)))
    palettes='\n'.join(re.search(r'static const u8 '+n+r'\[\] = \{.*?\};',text,re.S)[0] for n in ps)
    router=extract(text,'GetDoorGraphics');symbols=sorted(set(re.findall(r'&gTileset_\w+',router)))
    source='''#include <stdint.h>
#include <stddef.h>
#include <string.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;
#define DOOR_SOUND_NORMAL 0
#define DOOR_SOUND_SLIDING 1
#define DOOR_SOUND_ARENA 2
#define DOOR_TILE_START_SIZE1 1016
#define DOOR_TILE_START_SIZE2 1008
#include "constants/metatile_labels.h"
struct Tileset {int tag;};static const struct Tileset privateBank={0};
struct DoorGraphics {u16 metatileNum;u8 sound,size;const void *tiles,*palettes;};
static struct {const struct Tileset *primaryTileset;} layout={&privateBank};
static struct {__typeof__(layout) *mapLayout;} gMapHeader={&layout};
static int count,xs[4],ys[4],closed;static u16 drawn[4][8];
static void DrawDoorMetatileAt(u32 x,u32 y,u16 *p){xs[count]=x;ys[count]=y;memcpy(drawn[count++],p,16);}
static void CurrentMapDrawMetatileAt(u32 x,u32 y){xs[count]=x;ys[count++]=y;}
'''+''.join('static const struct Tileset '+s[1:]+'={1};\n' for s in symbols)+''.join('static const u8 '+n+'[]={0};\n' for n in ts)+palettes+'\n'+special+'\n'+table+'\n'+router+'\n'+extract(text,'BuildDoorTiles')+'\n'+extract(text,'DrawCurrentDoorAnimFrame')+'\n'+extract(text,'DrawClosedDoorTiles')+'''
int probe(int mid,int isClosed){const struct DoorGraphics *g=GetDoorGraphics(sDoorAnimGraphicsTable,mid);count=0;closed=isClosed;if(!g)return -1;if(isClosed)DrawClosedDoorTiles(g,8,8);else DrawCurrentDoorAnimFrame(g,8,8,g->palettes);return g-sDoorAnimGraphicsTable;}
int value(int f,int i,int j){switch(f){case 0:return count;case 1:return xs[i];case 2:return ys[i];case 3:return drawn[i][j];case 4:return closed;}return -1;}
'''
    dll=library(folder,'frontier_facade_doors',source);lookup=door_table(ROOT);assert lookup==door_table(base)
    _,ls,ms=inventory(ROOT);_,bl,bm=inventory(base);cases=sequence_cases=0
    sequences=[]
    for name in ('sDoorOpenAnimFrames','sDoorCloseAnimFrames'):
        body=re.search(r'static const struct DoorAnimFrame '+name+r'\[\] =\s*\{(.*?)\};',text,re.S)[1]
        sequence=[(int(t,0),int(offset,0)) for t,offset in re.findall(r'\{(\d+),\s*(-?\d+|0x[\da-fA-F]+)\}',body)]
        assert sequence[-1]==(0,0) and all(t==4 for t,o in sequence[:-1]);sequences.append(sequence[:-1])
    assert [o for t,o in sequences[0]]==[-1,0,256,512] and [o for t,o in sequences[1]]==[512,256,0,-1]
    for d in door_records(base):
        n=d['map'];r=renderer(ROOT,ls[ms[n]['layout']]);br=renderer(base,bl[bm[n]['layout']]);entry=lookup[d['id']];assert entry['size']==1
        for mid in (d['id'],d['upper_id']):assert r.metatile(mid).tobytes()==br.metatile(mid).tobytes()
        for c in (0,1):
            assert dll.probe(d['id'],c)==entry['index'] and dll.value(0,0,0)==2
            for part in range(2):
                assert (dll.value(1,part,0),dll.value(2,part,0))==(8,7+part)
                if not c:
                    for q in range(4):assert dll.value(3,part,q)==(entry['palettes'][part*4+q]<<12)|(1016+part*4+q)
                    for q in range(4,8):assert dll.value(3,part,q)&1023==0
            cases+=1
        im,row,count=door_indexed(ROOT/entry['path']);assert count==24
        payloads={-1:(r.metatile(d['upper_id']).tobytes()+r.metatile(d['id']).tobytes(),br.metatile(d['upper_id']).tobytes()+br.metatile(d['id']).tobytes())}
        for frame in range(3):
            a=door_frame(ROOT,d,frame,lookup);b=door_frame(base,d,frame,lookup);assert a.tobytes()==b.tobytes();cases+=1
            payloads[frame*256]=(a.tobytes(),b.tobytes())
        for sequence in sequences:
            for duration,offset in sequence:assert payloads[offset][0]==payloads[offset][1];sequence_cases+=1
    converted=converter_checks(Path(folder)/'gbagfx',{lookup[d['id']]['path'] for d in door_records(base)})
    assert sequence_cases==128
    return {'status':'PASS','animated_facade_doors':16,'door_closed_drawing_and_payload_cases':cases,'open_close_sequence_cases':sequence_cases,'native_asset_conversion':converted,'functions':['GetDoorGraphics','BuildDoorTiles','DrawCurrentDoorAnimFrame','DrawClosedDoorTiles'],'scope':'Original C router and drawing with host map-bank/draw services. All three real indexed frames and source palettes compared at all 16 doors; both canonical sequences checked. Task playback and hardware display remain pending.'}
def door_frame(repo,d,frame,lookup=None):
    from PIL import Image
    lookup=lookup or door_table(repo);e=lookup[d['id']];_,ls,ms=inventory(repo);r=renderer(repo,ls[ms[d['map']]['layout']]);im,row,count=door_indexed(repo/e['path']);out=Image.new('RGB',(16,32),r.palettes[0][0])
    for i in range(8):
        k=frame*8+i;tile=im.crop((k%row*8,k//row*8,k%row*8+8,k//row*8+8));rgba=Image.new('RGB',(8,8));rgba.putdata([r.palettes[e['palettes'][i]][v] if v else r.palettes[0][0] for v in tile.get_flattened_data()]);out.paste(rgba,(i%2*8,i//2*8))
    return out
def flag_checks(folder):
    src=(ROOT/'src/tileset_anims.c').read_text();result={}
    for side in ('East','West'):
        d=flags(ROOT,side);payloads={n:raw_4bpp(ROOT/p,6) for n,p in zip(d['refs'],d['paths'])};sym='BattleFrontierOutside'+side
        prefix='''#include <stdint.h>
#include <string.h>
typedef uint8_t u8;typedef uint16_t u16;
#define ARRAY_COUNT(a) (sizeof(a)/sizeof((a)[0]))
#define TILE_SIZE_4BPP 32
#define TILE_OFFSET_4BPP(n) ((n)*32)
#define NUM_TILES_IN_PRIMARY 512
static u8 vram[65536];
#define BG_VRAM vram
static u16 sSecondaryTilesetAnimCounter,sSecondaryTilesetAnimCounterMax;
static u16 sPrimaryTilesetAnimCounterMax=256;
static void (*sSecondaryTilesetAnimCallback)(u16);
static int copies,lastOffset,lastSize;
static void AppendTilesetAnimToBuffer(const u16 *p,u16 *dst,u16 n){lastOffset=(u8 *)dst-vram;lastSize=n;memcpy(dst,p,n);copies++;}
'''+f'static void TilesetAnim_{sym}(u16);\nstatic void QueueAnimTiles_{sym}_Flag(u16);\n'
        definitions=''.join('static const u16 '+n+'[]={'+','.join(map(str,struct.unpack('<96H',raw)))+'};\n' for n,raw in payloads.items())
        funcs=['InitTilesetAnim_'+sym,'TilesetAnim_'+sym,'QueueAnimTiles_'+sym+'_Flag']
        source=prefix+definitions+d['table']+'\n'+'\n'.join(function(src,n) for n in funcs)+f'\nvoid reset(void){{memset(vram,0x55,sizeof(vram));InitTilesetAnim_{sym}();}}\n'+'''void tick(int t){copies=0;sSecondaryTilesetAnimCallback(t);}
int value(int f,int i){switch(f){case 0:return copies;case 1:return lastOffset;case 2:return lastSize;case 3:return vram[i];case 4:return sSecondaryTilesetAnimCounter;case 5:return sSecondaryTilesetAnimCounterMax;}return -1;}
'''
        dll=library(Path(folder)/side,'native_flag',source);dll.reset();assert dll.value(5,0)==256;calls=0
        for t in range(256):
            dll.tick(t);assert dll.value(0,0)==int(t%8==0)
            if t%8==0:
                raw=payloads[d['refs'][(t//8)%4]];assert dll.value(1,0)==730*32 and dll.value(2,0)==192
                assert bytes(dll.value(3,730*32+i) for i in range(192))==raw;calls+=1
            assert dll.value(3,730*32-1)==0x55 and dll.value(3,736*32)==0x55
        result[side]={'status':'PASS','ticks':256,'updates':calls,'frames':4,'reserved_slots':[730,735],'functions':funcs}
    return result
