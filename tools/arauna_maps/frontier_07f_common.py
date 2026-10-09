"""Pyramid art: fixed lobby/top banks and runtime floors using the original seven palettes."""
import re,subprocess
from PIL import Image
from native_visuals_v2 import ROOT,callback
from safari_05_common import inventory
from frontier_07d_common import renderer as earlier_renderer
from render_native_map import words,indexed_tiles

BASE='9a3f9464ea6ba1e30b599c76648e4eb0e1a49405'
PREVIOUS='a679c2084336894210ab3ad76cfcba91d4d2f7e8'
EARLIER='38d7879ae14817d242ef07ca4f22fb60d3df96da'
GITHUB_9F='9f0a056e90fd42fa426030aca2f2e241401c0700'
OLDER='989c33c94fb89b92c5f608f78233fdd8deded4c4'
OUT=ROOT/'review/frontier_07f'
NAMES=tuple('BattleFrontier_BattlePyramid'+s for s in ('Lobby','Floor','Top'))
SQUARES=tuple('BattlePyramidSquare%02d'%i for i in range(1,17))
MUTABLE={'data/layouts/layouts.json',*('src/data/tilesets/'+f for f in ('graphics.h','metatiles.h','headers.h'))}
ANIMATED=set(range(647,655))|set(range(663,671))
MATERIAL=[(0,0,0),(24,32,40),(40,48,56),(64,80,80),(96,112,104),(160,176,152),(56,40,40),(88,56,40),(128,80,48),(176,120,64),(208,160,88),(232,200,128),(248,232,184),(32,80,80),(248,104,24),(248,216,72)]

def require_base(repo):
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==BASE

def floor_palettes(repo):
    lines=(repo/'graphics/battle_frontier/pyramid_floor.pal').read_text().splitlines()
    colors=[tuple(int(c)>>3<<3 for c in s.split()) for s in lines[3:]]
    assert len(colors)==112
    return [colors[i:i+16] for i in range(0,112,16)]

def animation_tables(repo):
    src=(repo/'src/tileset_anims.c').read_text();out=[]
    for suffix,start in (('Torch',663),('StatueShadow',647)):
        sym='gTilesetAnims_BattlePyramid_'+suffix
        declarations=dict(re.findall(r'const u16 ('+sym+r'_Frame\d+)\[\] = INCGFX_U16\("([^"]+)"',src))
        table=re.search(r'const u16 \*const '+sym+r'\[\] = \{.*?\};',src,re.S)[0]
        refs=re.findall(sym+r'_Frame\d+',table)
        out.append({'symbol':sym,'table':table,'refs':refs,'paths':[declarations[n] for n in refs],'start':start,'tiles':8})
    return out

def renderer(repo,layout,frame=-1,floor=None):
    r=earlier_renderer(repo,layout,frame)
    if floor is not None:r.palettes[6]=floor_palettes(repo)[floor]
    if frame>=0 and callback(repo,layout['secondary_tileset'])=='InitTilesetAnim_BattlePyramid':
        replacements={}
        for table in animation_tables(repo):
            im,row,_=indexed_tiles(repo/table['paths'][frame%len(table['paths'])])
            for i in range(table['tiles']):replacements[table['start']+i]=im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8))
        raw=r._tile
        r._tile=lambda t:replacements[t] if t in replacements else raw(t)
    return r

def render_grid(repo,layout,grid,width,height,frame=0,floor=None):
    r=renderer(repo,layout,frame,floor);im=Image.new('RGBA',(width*16,height*16));cache={}
    for i,v in enumerate(grid):
        mid=v&1023
        if mid not in cache:cache[mid]=r.metatile(mid)
        im.alpha_composite(cache[mid],(i%width*16,i//width*16))
    return im.convert('RGB')

def render(repo,layout,frame=0,floor=None):
    return render_grid(repo,layout,words(repo/layout['blockdata_filepath']),layout['width'],layout['height'],frame,floor)
