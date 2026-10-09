"""Six Palace/Arena maps on the official GitHub 9f integration of 07B."""
import re,subprocess
from native_visuals_v2 import ROOT
from safari_05_common import inventory
from navel_06b_common import renderer as _renderer
from native_visuals_v2 import callback
from render_native_map import indexed_tiles
from PIL import Image
from render_native_map import words
BASE='9f0a056e90fd42fa426030aca2f2e241401c0700'
PREVIOUS='868226c157fc24b36c24ebfc3ac0c6b83008bae7'
GITHUB='52e6f87e1b9e0b9452de3c40383440622a30f35a'
OLDER='989c33c94fb89b92c5f608f78233fdd8deded4c4'
OUT=ROOT/'review/frontier_07c'
NAMES=tuple('BattleFrontier_Battle'+f+s for f in ('Palace','Arena') for s in ('Lobby','Corridor','BattleRoom'))
GROUPS={'palace_lobby':NAMES[:1],'palace_garden':NAMES[1:3],'arena':NAMES[3:]}
MUTABLE={'data/layouts/layouts.json',*('src/data/tilesets/'+f for f in ('graphics.h','metatiles.h','headers.h'))}
ARENA=[(0,0,0),(24,24,32),(48,40,32),(80,56,40),(112,80,48),(144,104,64),(176,136,88),(216,184,120),(40,56,48),(64,88,64),(104,128,88),(56,64,72),(88,96,104),(128,136,136),(184,192,176),(232,224,192)]
PALACE=[(0,0,0),(32,24,32),(48,40,32),(88,48,32),(136,64,40),(176,88,48),(200,128,64),(232,184,96),(32,56,48),(56,88,64),(96,136,88),(48,64,72),(88,104,104),(136,144,136),(192,192,160),(240,224,184)]
def require_base(repo):assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==BASE

def door_records(repo):
    _,ls,maps=inventory(repo);result={}
    for n in NAMES:
        l=ls[maps[n]['layout']];g=words(repo/l['blockdata_filepath']);text=(repo/'data/maps'/n/'scripts.inc').read_text()
        coords={(int(x),int(y)) for x,y in re.findall(r'^\s*(?:open|close)door (\d+), (\d+)',text,re.M)}
        result[n]=[{'x':x,'y':y+dy,'id':g[(y+dy)*l['width']+x]&1023} for x,y in sorted(coords) for dy in (-1,0)]
    return result

def protected_ids(repo,names):return {c['id'] for n,cells in door_records(repo).items() if n in names for c in cells}

def renderer(repo,l,frame=-1):
    r=_renderer(repo,l,-1)
    if frame>=0 and callback(repo,l['primary_tileset'])=='InitTilesetAnim_General':
        from frontier_07c_animation_checks import frame_tables
        frames=[]
        for d in frame_tables(repo).values():
            im,row,_=indexed_tiles(repo/d['paths'][frame%len(d['paths'])]);frames.append((d['start'],d['tiles'],im,row))
        raw=r._tile
        def tile(t):
            for start,count,im,row in frames:
                if start<=t<start+count:
                    i=t-start;return im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8))
            return raw(t)
        r._tile=tile
    return r

def render(repo,l,frame=0):
    r=renderer(repo,l,frame);cache={};im=Image.new('RGBA',(l['width']*16,l['height']*16))
    for i,v in enumerate(words(repo/l['blockdata_filepath'])):
        mid=v&1023
        if mid not in cache:cache[mid]=r.metatile(mid)
        im.alpha_composite(cache[mid],(i%l['width']*16,i//l['width']*16))
    return im.convert('RGB')
