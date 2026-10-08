"""Base, palette stages and private copies of the shared native stair plants."""
import json
from pathlib import Path
from PIL import Image
from native_visuals_v2 import ROOT,callback
from safari_05_common import inventory
from render_native_map import Renderer,words,indexed_tiles
from bancos_nativos import resolve_bank
from validate_grutas_bordas_v2 import animated

BASE='29ae94cdc2309d099cd0f8ac4fecc4775a6aef72'
GITHUB_BASE='d665dc34ddea776c06c85981653a9f62aa1e19d6'
OUT=ROOT/'review/navel_06b'
CORE=('NavelRock_Exterior','NavelRock_Entrance','NavelRock_B1F','NavelRock_Fork',*(f'NavelRock_Up{i}' for i in range(1,5)),'NavelRock_Top',*(f'NavelRock_Down{i:02}' for i in range(1,12)),'NavelRock_Bottom')
NAMES=CORE+('NavelRock_Harbor',)
GROUPS={'coast':('NavelRock_Exterior',),'gallery':('NavelRock_Entrance','NavelRock_B1F','NavelRock_Fork'),'ascent':('NavelRock_Up1','NavelRock_Up2'),'summit':('NavelRock_Up3','NavelRock_Up4','NavelRock_Top'),'depth1':tuple(f'NavelRock_Down{i:02}' for i in range(1,5)),'depth2':tuple(f'NavelRock_Down{i:02}' for i in range(5,9)),'abyss':tuple(f'NavelRock_Down{i:02}' for i in range(9,12))+('NavelRock_Bottom',),'dock':('NavelRock_Harbor',)}
COPIES={n:('LAYOUT_ARAUNA_NAVEL_06B_'+theme.upper()+'_LADDER'+str(1 if int(n[-2:] if 'Down' in n else n[-1])%2 else 2)) for theme in ('summit','depth1','depth2','abyss') for n in GROUPS[theme] if '_Up' in n or '_Down' in n}
COPIES['NavelRock_Harbor']='LAYOUT_ARAUNA_NAVEL_06B_HARBOR'
MUTABLE={'data/layouts/layouts.json',*('src/data/tilesets/'+f for f in ('graphics.h','metatiles.h','headers.h')),*('data/maps/'+n+'/map.json' for n in COPIES)}

def renderer(repo,l,frame=0):
    r=Renderer(*[resolve_bank(repo,l[k]) for k in ('primary_tileset','secondary_tileset')])
    if frame>=0 and callback(repo,l['primary_tileset'])=='InitTilesetAnim_General':r=animated(r,repo,frame)
    if frame>=0 and callback(repo,l['secondary_tileset'])=='InitTilesetAnim_Dewford':
        raw=r._tile
        im,row,_=indexed_tiles(repo/f'data/tilesets/secondary/dewford/anim/flag/{frame%4}.png')
        def tile(t):
            if 682<=t<688:
                i=t-682;return im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8))
            return raw(t)
        r._tile=tile
    r.palettes=[[tuple(c>>3<<3 for c in rgb) for rgb in pal] for pal in r.palettes]
    return r

def render(repo,l,frame=0):
    r=renderer(repo,l,frame);cache={};im=Image.new('RGBA',(l['width']*16,l['height']*16))
    for i,v in enumerate(words(repo/l['blockdata_filepath'])):
        mid=v&1023
        if mid not in cache:cache[mid]=r.metatile(mid)
        im.alpha_composite(cache[mid],(i%l['width']*16,i//l['width']*16))
    return im.convert('RGB')
