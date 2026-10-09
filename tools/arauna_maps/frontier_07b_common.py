"""Battle Dome: native private art, light masks and unchanged tournament logic."""
import re,subprocess
from native_visuals_v2 import ROOT
from safari_05_common import inventory
from navel_06b_common import renderer as _renderer
from render_native_map import palette
from PIL import Image
from render_native_map import words

BASE='fc408a604b0f2c0b1cc28b3e20a7a9aac6b20596'
PREVIOUS='7e9d29dc5fdab047ac663dd2953a83ff9a51c0b8'
OUT=ROOT/'review/frontier_07b'
NAMES=tuple('BattleFrontier_BattleDome'+v for v in ('Lobby','Corridor','PreBattleRoom','BattleRoom'))
MUTABLE={'data/layouts/layouts.json',*('src/data/tilesets/'+f for f in ('graphics.h','metatiles.h','headers.h'))}
MATERIAL=[(0,0,0),(24,24,32),(48,40,32),(80,56,40),(112,80,48),(144,104,64),(176,136,88),(216,184,120),(40,56,48),(64,88,64),(104,128,88),(56,64,72),(88,96,104),(128,136,136),(184,192,176),(232,224,192)]

def require_base(repo):
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==BASE

def door_records(repo):
    _,ls,maps=inventory(repo);result={}
    for n in NAMES:
        l=ls[maps[n]['layout']];g=words(repo/l['blockdata_filepath'])
        text=(repo/'data/maps'/n/'scripts.inc').read_text()
        coords={(int(x),int(y)) for x,y in re.findall(r'^\s*(?:open|close)door (\d+), (\d+)',text,re.M)}
        # Dome doors are explicitly opened by their unchanged map scripts.
        cells=[]
        for x,y in sorted(coords):
            mid=g[y*l['width']+x]&1023;width=1
            for dx in range(width):
                for dy in (-1,0):
                    assert 0<=x+dx<l['width'] and 0<=y+dy<l['height']
                    cells.append({'x':x+dx,'y':y+dy,'id':g[(y+dy)*l['width']+x+dx]&1023})
        result[n]=cells
    return result

def protected_ids(repo):
    return {c['id'] for cells in door_records(repo).values() for c in cells}

def renderer(repo,layout,frame=-1):
    r=_renderer(repo,layout,-1)
    if frame>=0:
        r.palettes[8]=[tuple(c>>3<<3 for c in rgb) for rgb in palette(repo/f'graphics/battle_frontier/dome_anim{frame%4+1}.pal')]
    return r

def render(repo,layout,frame=0):
    r=renderer(repo,layout,frame);cache={};im=Image.new('RGBA',(layout['width']*16,layout['height']*16))
    for i,v in enumerate(words(repo/layout['blockdata_filepath'])):
        mid=v&1023
        if mid not in cache:cache[mid]=r.metatile(mid)
        im.alpha_composite(cache[mid],(i%layout['width']*16,i//layout['width']*16))
    return im.convert('RGB')
