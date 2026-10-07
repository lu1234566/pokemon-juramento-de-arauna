"""Host-compile actual camera selectors, with literal native review grids."""
import ctypes,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def compile_selector(folder):
 folder=Path(folder)
 (folder/'global.h').write_text('''#include <stdint.h>
#include <stddef.h>
typedef uint16_t u16; typedef uint32_t u32; typedef int32_t s32; typedef uint8_t bool8;
struct Tileset {int dummy;};
struct MapLayout {const struct Tileset *primaryTileset;const struct Tileset *secondaryTileset;int width;int height;const u16 *map;};
#define ARRAY_COUNT(a) (sizeof(a)/sizeof((a)[0]))
''')
 (folder/'fieldmap.h').write_text('#define MAP_OFFSET 7\n')
 text=(ROOT/'src/arauna_border_visuals.c').read_text();symbols=re.findall(r'extern const struct Tileset (\w+);',text)
 table=json.loads((ROOT/'review/grutas_bordas_v2/borders_build.json').read_text());cases={119:'gTileset_AraunaRoute119BorderV1',118:'gTileset_AraunaRoute118BorderV1'};cases.update({r['code']:'gTileset_'+r['symbols'][1] for r in table['maps'].values()})
 extra=ROOT/'review/sul_pampa_v1/borders_build.json'
 if extra.exists():cases.update({r['code']:'gTileset_'+r['symbols'][1] for r in json.loads(extra.read_text())['maps'].values()})
 bridge='#include "global.h"\n#include "arauna_border_visuals.h"\n'+''.join(f'const struct Tileset {s} = {{{i+1}}};\n' for i,s in enumerate(symbols))+'''const struct Tileset otherTileset={0};
u16 AraunaCaveVisualMetatile(const struct MapLayout *l,s32 x,s32 y,u16 id) {(void)l;(void)x;(void)y;return id;}
u16 test_selector(int map,int x,int y,u16 id) {
 struct MapLayout l={&otherTileset,&otherTileset,0,0,NULL};
'''+''.join(f' if(map=={code})l.secondaryTileset=&{s};\n' for code,s in cases.items())+' return AraunaBorderVisualMetatile(&l,x,y,id);\n}\n'
 (folder/'bridge.c').write_text(bridge);target=folder/'selector.so';subprocess.run(['cc','-Wall','-Wextra','-Werror','-shared','-fPIC','-I'+str(folder),'-I'+str(ROOT/'include'),str(ROOT/'src/arauna_border_visuals.c'),str(folder/'bridge.c'),'-o',str(target)],check=True);dll=ctypes.CDLL(str(target));f=dll.test_selector;f.argtypes=[ctypes.c_int]*3+[ctypes.c_uint16];f.restype=ctypes.c_uint16;return f
def compile_caves(folder):
 import struct
 folder=Path(folder);(folder/'data').mkdir(exist_ok=True)
 src=(ROOT/'src/arauna_cave_visuals.c').read_text();h=(ROOT/'src/data/arauna_cave_visuals_v2.h').read_text()
 def literal(m):
  p=ROOT/m[1];raw=p.read_bytes();v=struct.unpack('<%dH'%(len(raw)//2),raw);return '{'+','.join(map(str,v))+'}'
 h=re.sub(r'INCBIN_U16\("([^"]+)"\)',literal,h);(folder/'data/arauna_cave_visuals_v2.h').write_text(h);(folder/'caves.c').write_text(src)
 maps=json.loads((ROOT/'review/grutas_bordas_v2/grutas_build.json').read_text())['maps'];layouts=json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts'];bridge='#include "global.h"\n#include "arauna_cave_visuals.h"\n'
 for i,(n,d) in enumerate(maps.items()):
  l=layouts[d['layout_index']];v=struct.unpack('<%dH'%(l['width']*l['height']),(ROOT/l['blockdata_filepath']).read_bytes());bridge+=f'static const u16 grid{i}[]={{'+','.join(map(str,v))+'};\n'+f'static const struct MapLayout layout{i}={{NULL,NULL,{l["width"]},{l["height"]},grid{i}}};\n'
 lookup={d['layout_index']:i for i,d in enumerate(maps.values())};bridge+='const struct MapLayout *const gMapLayouts[]={'+','.join('&layout'+str(lookup[j]) if j in lookup else 'NULL' for j in range(len(layouts)))+'};\n'+ 'static const struct MapLayout *cases[]={'+','.join('&layout'+str(i) for i in range(len(maps)))+'};\n'+ 'u16 test_cave(int map,int x,int y,u16 id){return AraunaCaveVisualMetatile(cases[map],x,y,id);}\n'
 (folder/'cavebridge.c').write_text(bridge);so=folder/'caves.so';subprocess.run(['cc','-Wall','-Wextra','-Werror','-shared','-fPIC','-I'+str(folder),'-I'+str(ROOT/'include'),str(folder/'caves.c'),str(folder/'cavebridge.c'),'-o',str(so)],check=True);dll=ctypes.CDLL(str(so));f=dll.test_cave;f.argtypes=[ctypes.c_int]*3+[ctypes.c_uint16];f.restype=ctypes.c_uint16;return f
