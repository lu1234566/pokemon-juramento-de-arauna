"""Battle Pike art on the documented official Factory integration."""
import re,subprocess
from native_visuals_v2 import ROOT,callback
from safari_05_common import inventory
from frontier_07d_common import renderer,render

BASE='38d7879ae14817d242ef07ca4f22fb60d3df96da'
PREVIOUS='2a1838d000482773bb25a2faffc291b1c26cb756'
EARLIER='8d7cafa5d7eef106eea69bc1ad18e3097d7e343b'
OLDER='989c33c94fb89b92c5f608f78233fdd8deded4c4'
GITHUB_9F='9f0a056e90fd42fa426030aca2f2e241401c0700'
OUT=ROOT/'review/frontier_07e'
NAMES=tuple('BattleFrontier_BattlePike'+s for s in ('Lobby','Corridor','ThreePathRoom','RoomNormal','RoomFinal','RoomWildMons'))
MUTABLE={'data/layouts/layouts.json',*('src/data/tilesets/'+f for f in ('graphics.h','metatiles.h','headers.h'))}
MATERIAL=[(0,0,0),(24,24,32),(40,48,48),(64,72,72),(88,104,96),(144,160,144),(48,24,40),(80,32,56),(120,48,64),(160,80,88),(80,48,32),(144,88,48),(208,160,88),(32,80,64),(64,136,104),(144,208,160)]

def require_base(repo):
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==BASE

def curtain_ids(repo):
    src=(repo/'src/field_specials.c').read_text()
    labels=(repo/'include/constants/metatile_labels.h').read_text()
    start=int(re.search(r'#define METATILE_BattlePike_CurtainFrames_Start\s+(0x\w+)',labels)[1],16)
    assert '#define CURTAIN_HEIGHT 4' in src and '#define CURTAIN_WIDTH 3' in src
    dynamic={start+x+y*8+frame*4*8 for frame in range(3) for y in range(4) for x in range(3)}
    named={int(v,16) for v in re.findall(r'#define METATILE_BattlePike_Curtain_Stage\d_Tile\d\s+(0x\w+)',labels)}
    return sorted(dynamic|named)

def door_records(repo):
    _,ls,maps=inventory(repo);result={}
    for n in NAMES:
        l=ls[maps[n]['layout']]
        from render_native_map import words
        g=words(repo/l['blockdata_filepath']);src=(repo/'data/maps'/n/'scripts.inc').read_text()
        coords={(int(x),int(y)) for x,y in re.findall(r'^\s*(?:open|close)door (\d+), (\d+)',src,re.M)}
        result[n]=[{'x':x,'y':y+dy,'id':g[(y+dy)*l['width']+x]&1023} for x,y in sorted(coords) for dy in (-1,0)]
    return result
