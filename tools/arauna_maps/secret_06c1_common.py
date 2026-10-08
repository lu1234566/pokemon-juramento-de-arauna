"""Read Secret Base C registrations: shared metatiles and theme graphics differ."""
import json,re,subprocess
from pathlib import Path
from PIL import Image
from native_visuals_v2 import ROOT,callback
from render_native_map import Renderer,indexed_tiles,words,palette

BASE='2449e12b0645f9aa37ef261ba2d3ce71df93254a'
GITHUB_BASE='d665dc34ddea776c06c85981653a9f62aa1e19d6'
OUT=ROOT/'review/secret_bases_06c1'
COLORS=('Red','Brown','Blue','Yellow')
NAMES=tuple(f'SecretBase_{color}Cave{i}' for color in COLORS for i in range(1,5))
MUTABLE={'data/layouts/layouts.json',*('src/data/tilesets/'+f for f in ('graphics.h','metatiles.h','headers.h'))}

def inventory(repo):
    node=json.loads((repo/'data/layouts/layouts.json').read_text())
    layouts={l['id']:l for l in node['layouts']}
    maps={m['name']:m for p in (repo/'data/maps').glob('*/map.json') for m in [json.loads(p.read_text())]}
    return node,layouts,maps

def parts(repo,symbol):
    headers=(repo/'src/data/tilesets/headers.h').read_text()
    body=re.search(r'const struct Tileset '+re.escape(symbol)+r'\s*=\s*\{(.*?)\};',headers,re.S)[1]
    meta_sym=re.search(r'\.metatiles\s*=\s*(\w+)',body)[1]
    meta_text=(repo/'src/data/tilesets/metatiles.h').read_text()
    meta=repo/re.search(re.escape(meta_sym)+r'\[\]\s*=\s*INCBIN_U16\("([^"]+)"',meta_text)[1]
    tile_sym=re.search(r'\.tiles\s*=\s*(\w+)',body)[1]
    pal_sym=re.search(r'\.palettes\s*=\s*(\w+)',body)[1]
    graphics=(repo/'src/data/tilesets/graphics.h').read_text()
    tile_decl=re.search(re.escape(tile_sym)+r'\[\]\s*=\s*INCGFX_U32\((.*?)\);',graphics,re.S)[1]
    tiles=repo/re.search(r'"([^"]+)"',tile_decl)[1]
    pal_body=re.search(re.escape(pal_sym)+r'\[\]\[16\]\s*=\s*\{(.*?)\};',graphics,re.S)[1]
    pals=[repo/p for p in re.findall(r'INCGFX_U16\("([^"]+)"',pal_body)]
    count=re.search(r'-num_tiles (\d+)',tile_decl)
    return {'metatiles':meta,'attributes':meta.with_name('metatile_attributes.bin'),'tiles':tiles,'palettes':pals,'tile_count':int(count[1]) if count else None,'compressed':'.isCompressed = TRUE' in body,'callback':callback(repo,symbol)}

class SecretRenderer(Renderer):
    def __init__(self,repo,l):
        banks=[parts(repo,l[k]) for k in ('primary_tileset','secondary_tileset')]
        self.primary,self.secondary=[b['metatiles'].parent for b in banks]
        sheets=[]
        for b in banks:
            im,row,count=indexed_tiles(b['tiles']);sheets.append((im,row,b['tile_count'] or count))
        self.primary_tiles,self.secondary_tiles=sheets
        self.primary_metatiles,self.secondary_metatiles=[words(b['metatiles']) for b in banks]
        self.palettes=[palette(banks[0]['palettes'][i]) for i in range(6)]+[palette(banks[1]['palettes'][i]) for i in range(6,13)]
        self.palettes=[[tuple(c>>3<<3 for c in rgb) for rgb in p] for p in self.palettes]

def render(repo,l,grid=None):
    r=SecretRenderer(repo,l);cache={};im=Image.new('RGBA',(l['width']*16,l['height']*16))
    for i,v in enumerate(grid if grid is not None else words(repo/l['blockdata_filepath'])):
        mid=v&1023
        if mid not in cache:cache[mid]=r.metatile(mid)
        im.alpha_composite(cache[mid],(i%l['width']*16,i//l['width']*16))
    return im.convert('RGB')

def require_base(repo):
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==BASE
