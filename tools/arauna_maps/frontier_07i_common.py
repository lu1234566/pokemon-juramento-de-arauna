"""Three Frontier exteriors, native flags and exact animated facade door footprints."""
import re,subprocess
from PIL import Image
from native_visuals_v2 import ROOT,callback
from safari_05_common import inventory
from frontier_07h_common import renderer as earlier_renderer
from render_native_map import words,indexed_tiles
BASE='725f8fe44f427b827221fdbcc3beca70e92e3b72'
PREVIOUS='531352ce3715e41389382de692e917a32b9e60be'
EARLIER='4122b9fa98db5604cb302468ff89dfc0145865a0'
GITHUB_9F='9f0a056e90fd42fa426030aca2f2e241401c0700'
OLDER='989c33c94fb89b92c5f608f78233fdd8deded4c4'
MAIN='979fb6c1b6731561f3c993efd6045a9bbf096c54'
OUT=ROOT/'review/frontier_07i'
NAMES=tuple('BattleFrontier_'+s for s in ('OutsideEast','OutsideWest','ReceptionGate'))
ROLES=('Terraços orientais — Torre, Arena, Palace e Pyramid','Praças ocidentais — Dome, Factory e Pike','Pavilhão de recepção')
MUTABLE={'data/layouts/layouts.json',*('src/data/tilesets/'+f for f in ('graphics.h','metatiles.h','headers.h'))}
def require_base(repo):assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==BASE
def flags(repo,side):
    src=(repo/'src/tileset_anims.c').read_text();sym='gTilesetAnims_BattleFrontierOutside'+side+'_Flag'
    table=re.search(r'const u16 \*const '+sym+r'\[\] = \{.*?\};',src,re.S)[0];refs=re.findall(sym+r'_Frame\d+',table);decs=dict(re.findall(r'const u16 ('+sym+r'_Frame\d+)\[\] = INCGFX_U16\("([^"]+)"',src))
    return {'symbol':sym,'table':table,'refs':refs,'paths':[decs[n] for n in refs],'start':730,'tiles':6}
def renderer(repo,l,frame=-1):
    r=earlier_renderer(repo,l,frame);cb=callback(repo,l['secondary_tileset'])
    if frame>=0 and cb in ('InitTilesetAnim_BattleFrontierOutsideEast','InitTilesetAnim_BattleFrontierOutsideWest'):
        side='East' if cb.endswith('East') else 'West';d=flags(repo,side);im,row,_=indexed_tiles(repo/d['paths'][frame%4]);raw=r._tile
        def tile(t):
            if 730<=t<736:
                i=t-730;return im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8))
            return raw(t)
        r._tile=tile
    return r
def render_grid(repo,l,g,width,height,frame=0,floor=None):
    if floor is not None:
        from frontier_07h_common import render_grid as prior_grid
        return prior_grid(repo,l,g,width,height,frame,floor)
    r=renderer(repo,l,frame);im=Image.new('RGBA',(width*16,height*16));cache={}
    for i,v in enumerate(g):
        mid=v&1023
        if mid not in cache:cache[mid]=r.metatile(mid)
        im.alpha_composite(cache[mid],(i%width*16,i//width*16))
    return im.convert('RGB')
def render(repo,l,frame=0):return render_grid(repo,l,words(repo/l['blockdata_filepath']),l['width'],l['height'],frame)
def door_records(repo):
    from native_visuals_v2 import Pair
    _,ls,ms=inventory(repo);out=[]
    for n in NAMES[:2]:
        l=ls[ms[n]['layout']];p=Pair(repo,l);g=words(repo/l['blockdata_filepath'])
        for e in ms[n]['warp_events']:
            x,y=e['x'],e['y'];mid=g[y*l['width']+x]&1023
            if p.attrs[mid>=512][mid%512]&255==0x69:
                out.append({'map':n,'x':x,'y':y,'id':mid,'upper_id':g[(y-1)*l['width']+x]&1023,'destination':e['dest_map']})
    return out
