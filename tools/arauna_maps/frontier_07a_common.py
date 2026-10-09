"""Battle Tower: private art, unchanged layout IDs and engine on 7e9d29dc5f."""
import re,subprocess
from native_visuals_v2 import ROOT
from safari_05_common import inventory
from navel_06b_common import renderer,render
from render_native_map import words

BASE='7e9d29dc5fdab047ac663dd2953a83ff9a51c0b8'
PREVIOUS='989c33c94fb89b92c5f608f78233fdd8deded4c4'
OUT=ROOT/'review/frontier_07a'
NAMES=tuple('BattleFrontier_BattleTower'+s for s in ('Lobby','Elevator','Corridor','BattleRoom','MultiPartnerRoom','MultiCorridor','MultiBattleRoom'))
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
        if n.endswith('MultiCorridor'):coords.add((14,1)) # DrawDoor redirects using VAR_0x8004/5.
        cells=[]
        for x,y in sorted(coords):
            mid=g[y*l['width']+x]&1023;width=2 if mid==0x2ad else 1
            for dx in range(width):
                for dy in (-1,0):
                    assert 0<=x+dx<l['width'] and 0<=y+dy<l['height']
                    cells.append({'x':x+dx,'y':y+dy,'id':g[(y+dy)*l['width']+x+dx]&1023})
        result[n]=cells
    return result

def protected_ids(repo):
    # Include both open passage tiles even though the saved grid is closed.
    return {0x207,0x20f,0x24f,0x257,*[c['id'] for cells in door_records(repo).values() for c in cells]}
