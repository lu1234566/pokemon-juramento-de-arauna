"""Native rendering and host execution of the existing production cave selector."""
import ctypes, json, re, struct, subprocess
from pathlib import Path
from PIL import Image
from build_cavernas_03a import ROOT, OUT
from bancos_nativos import resolve_bank
from render_native_map import Renderer, words, indexed_tiles
from validate_grutas_bordas_v2 import animated
import host_visual_selector_v2 as host

def compile_caves(folder):
    folder=Path(folder);host.ROOT=ROOT
    # Reuse production border-selector declarations to get identical scalar types.
    host.compile_selector(folder)
    (folder/'data').mkdir(exist_ok=True)
    header=(ROOT/'src/data/arauna_cave_visuals_v2.h').read_text()
    records=re.findall(r'\{(\d+), sVisual_(\w+)\}',header)
    def literal(m):return '{'+','.join(map(str,words(ROOT/m[1])))+'}'
    header=re.sub(r'INCBIN_U16\("([^"]+)"\)',literal,header)
    (folder/'data/arauna_cave_visuals_v2.h').write_text(header)
    layouts=json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']
    bridge='#include "global.h"\n#include "arauna_cave_visuals.h"\n'
    lookup={}
    for case,(idx,name) in enumerate(records):
        idx=int(idx);l=layouts[idx];g=words(ROOT/l['blockdata_filepath']);lookup[idx]=case
        bridge+=f'static const u16 grid{case}[]={{'+','.join(map(str,g))+'};\n'
        bridge+=f'static const struct MapLayout layout{case}={{NULL,NULL,{l["width"]},{l["height"]},grid{case}}};\n'
    bridge+='const struct MapLayout *const gMapLayouts[]={'+','.join('&layout'+str(lookup[i]) if i in lookup else 'NULL' for i in range(len(layouts)))+'};\n'
    bridge+='static const struct MapLayout *cases[]={'+','.join('&layout'+str(i) for i in range(len(records)))+'};\n'
    bridge+='u16 test_cave(int map,int x,int y,u16 id){return AraunaCaveVisualMetatile(cases[map],x,y,id);}\n'
    (folder/'bridge_caves_03a.c').write_text(bridge)
    (folder/'caves_03a.c').write_text((ROOT/'src/arauna_cave_visuals.c').read_text())
    target=folder/'caves_03a.so'
    subprocess.run(['cc','-Wall','-Wextra','-Werror','-shared','-fPIC','-I'+str(folder),'-I'+str(ROOT/'include'),str(folder/'caves_03a.c'),str(folder/'bridge_caves_03a.c'),'-o',str(target)],check=True)
    dll=ctypes.CDLL(str(target));fn=dll.test_cave;fn.argtypes=[ctypes.c_int]*3+[ctypes.c_uint16];fn.restype=ctypes.c_uint16
    return fn,{name:i for i,(idx,name) in enumerate(records)}

def renderer(repo,layout,frame=0):
    r=animated(Renderer(*[resolve_bank(repo,layout[k]) for k in ('primary_tileset','secondary_tileset')]),repo,frame)
    raw=r._tile
    files=sorted((repo/'data/tilesets/secondary/cave/anim/lava').glob('*.png'))[:4]
    im,row,_=indexed_tiles(files[frame%len(files)])
    def tile(t):
        if 928<=t<932:
            i=t-928;return im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8))
        return raw(t)
    r._tile=tile
    # The hardware stores RGB555, not full 8-bit RGB palette values.
    r.palettes=[[tuple(c>>3<<3 for c in rgb) for rgb in pal] for pal in r.palettes]
    return r

def render(repo,layout,visual=None,frame=0):
    r=renderer(repo,layout,frame);g=visual or [v&1023 for v in words(repo/layout['blockdata_filepath'])];cache={}
    image=Image.new('RGBA',(layout['width']*16,layout['height']*16))
    for i,mid in enumerate(g):
        if mid not in cache:cache[mid]=r.metatile(mid)
        image.alpha_composite(cache[mid],(i%layout['width']*16,i//layout['width']*16))
    return image.convert('RGB')
