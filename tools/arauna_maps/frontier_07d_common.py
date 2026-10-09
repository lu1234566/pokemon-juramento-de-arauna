"""Battle Factory native art on the official corrected 07C integration."""
import re, subprocess
from native_visuals_v2 import ROOT, callback
from safari_05_common import inventory
from frontier_07c_common import renderer as previous_renderer, render as previous_render
from PIL import Image
from render_native_map import words, indexed_tiles

BASE='8d7cafa5d7eef106eea69bc1ad18e3097d7e343b'
PREVIOUS='638d523c088ddc9991617031e07808119712caf7'
EARLIER='9f0a056e90fd42fa426030aca2f2e241401c0700'
OLDER='989c33c94fb89b92c5f608f78233fdd8deded4c4'
OUT=ROOT/'review/frontier_07d'
NAMES=tuple('BattleFrontier_BattleFactory'+s for s in ('Lobby','PreBattleRoom','BattleRoom'))
MUTABLE={'data/layouts/layouts.json',*('src/data/tilesets/'+f for f in ('graphics.h','metatiles.h','headers.h'))}
MATERIAL=[(0,0,0),(24,32,40),(48,64,64),(64,80,80),(88,104,96),(120,144,136),(168,184,168),(216,216,184),(88,48,32),(136,72,40),(176,112,56),(216,160,80),(32,72,64),(48,120,96),(88,184,152),(168,232,192)]

def require_base(repo):
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==BASE

def renderer(repo,layout,frame=-1):
    r=previous_renderer(repo,layout,frame)
    if frame>=0 and callback(repo,layout['primary_tileset'])=='InitTilesetAnim_Building':
        from frontier_07d_animation_checks import frame_table
        table=frame_table(repo);im,row,_=indexed_tiles(repo/table['paths'][frame%len(table['paths'])]);raw=r._tile
        def tile(t):
            if 496<=t<500:
                i=t-496;return im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8))
            return raw(t)
        r._tile=tile
    return r

def render(repo,layout,frame=0):
    r=renderer(repo,layout,frame);cache={};im=Image.new('RGBA',(layout['width']*16,layout['height']*16))
    for i,v in enumerate(words(repo/layout['blockdata_filepath'])):
        mid=v&1023
        if mid not in cache:cache[mid]=r.metatile(mid)
        im.alpha_composite(cache[mid],(i%layout['width']*16,i//layout['width']*16))
    return im.convert('RGB')

def door_records(repo):
    _,ls,maps=inventory(repo);result={}
    for n in NAMES:
        l=ls[maps[n]['layout']];g=words(repo/l['blockdata_filepath']);text=(repo/'data/maps'/n/'scripts.inc').read_text()
        coords={(int(x),int(y)) for x,y in re.findall(r'^\s*(?:open|close)door (\d+), (\d+)',text,re.M)}
        result[n]=[{'x':x,'y':y+dy,'id':g[(y+dy)*l['width']+x]&1023} for x,y in sorted(coords) for dy in (-1,0)]
    return result
