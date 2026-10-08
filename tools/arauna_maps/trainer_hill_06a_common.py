"""Trainer Hill: exact native modes, layouts and base-specific bank rendering."""
import json,re
from pathlib import Path
from PIL import Image
from native_visuals_v2 import ROOT
from safari_05_common import inventory,renderer
from render_native_map import words

BASE='d665dc34ddea776c06c85981653a9f62aa1e19d6'
OUT=ROOT/'review/trainer_hill_06a'
NAMES=('TrainerHill_Entrance','TrainerHill_1F','TrainerHill_2F','TrainerHill_3F','TrainerHill_4F','TrainerHill_Roof','TrainerHill_Elevator')
MODES=('normal','variety','unique','expert')
ELEVATOR_ID='LAYOUT_ARAUNA_TRAINER_HILL_06A_ELEVATOR'
MUTABLE={'data/layouts/layouts.json','data/maps/TrainerHill_Elevator/map.json',*('src/data/tilesets/'+f for f in ('graphics.h','metatiles.h','headers.h'))}

def floors(repo):
    source=(repo/'src/data/battle_frontier/trainer_hill.h').read_text()
    result={}
    for mode in MODES:
        start=source.index('static const struct TrainerHillFloor sFloors_'+mode.title())
        end=source.find('static const struct TrainerHillChallenge',start)
        part=source[start:end if end!=-1 else len(source)]
        records=re.findall(r'\.metatileData = INCBIN_U8\("([^"]+)"\),\s*\.collisionData = INCBIN_U16\("([^"]+)"\),\s*\.trainerCoords = \{\s*COORDS_XY\((\d+),(\d+)\),\s*COORDS_XY\((\d+),(\d+)\)\s*\}',part)
        assert len(records)==4,(mode,len(records))
        for floor,(metas,collision,x1,y1,x2,y2) in enumerate(records):
            ids=list((repo/metas).read_bytes());coll=words(repo/collision)
            assert len(ids)==256 and len(coll)==16
            result[mode+'_'+str(floor)]={'mode':mode,'floor':floor,'metatile_path':metas,'collision_path':collision,'ids':ids,'collision':coll,'trainers':[(int(x1),int(y1)+5),(int(x2),int(y2)+5)]}
    return result

def runtime_words(repo,record):
    _,ls,maps=inventory(repo);name='TrainerHill_'+str(record['floor']+1)+'F'
    l=ls[maps[name]['layout']];fixed=words(repo/l['blockdata_filepath'])[:80]
    generated=[0x3000|(((record['collision'][i//16]>>(15-i%16))&1)<<10)|(512+v) for i,v in enumerate(record['ids'])]
    return l,fixed+generated

def render_words(repo,l,g):
    r=renderer(repo,l);cache={};out=Image.new('RGBA',(l['width']*16,l['height']*16))
    for i,v in enumerate(g):
        mid=v&1023
        if mid not in cache:cache[mid]=r.metatile(mid)
        out.alpha_composite(cache[mid],(i%l['width']*16,i//l['width']*16))
    return out.convert('RGB')
