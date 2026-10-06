#!/usr/bin/env python3
"""Check forest terrain, story triggers, Cut gates and all six return warps."""
import json
from pathlib import Path
from collections import Counter, deque
from bancos_nativos import resolve_bank, bank_words
from render_native_map import Renderer, words
from build_mata_espera_v1 import ROOT, LAYOUT, TARGET

def main():
    layouts={l['id']:l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
    old=layouts['LAYOUT_PETALBURG_WOODS'];new=layouts[LAYOUT]
    assert (old['width'],old['height'])==(new['width'],new['height'])==(48,44)
    grids=[words(ROOT/l['blockdata_filepath']) for l in (old,new)]
    renderers=[Renderer(resolve_bank(ROOT,l['primary_tileset']),resolve_bank(ROOT,l['secondary_tileset'])) for l in (old,new)]
    assert len(grids[0])==len(grids[1])==48*44
    for i,(a,b) in enumerate(zip(*grids)):
        assert a&0xfc00==b&0xfc00,(i,'collision/elevation changed')
        assert bank_words(renderers[0],a&1023,True)==bank_words(renderers[1],b&1023,True),(i,'behavior changed')
        if a&1023!=1 and not ((a>>10)&3):
            assert a==b,(i,'interactive/encounter tile ID changed')
    event=json.loads((ROOT/'data/maps/PetalburgWoods/map.json').read_text())
    assert event['layout']==LAYOUT and event['weather']=='WEATHER_SHADE'
    assert len(event['warp_events'])==6 and len(event['coord_events'])==2
    for kind in ('warp_events','coord_events','object_events','bg_events'):
        for e in event[kind]:
            i=e['y']*48+e['x'];assert grids[0][i]==grids[1][i],(kind,e)
    route=json.loads((ROOT/'data/maps/Route104/map.json').read_text())
    for wid,e in enumerate(event['warp_events']):
        assert e['dest_map']=='MAP_ROUTE104'
        dest=route['warp_events'][int(e['dest_warp_id'])]
        assert dest['dest_map']=='MAP_PETALBURG_WOODS' and int(dest['dest_warp_id'])==wid
    # Tile passability and all elevations/behaviors are identical, so every
    # directional ledge and scripted movement uses the same engine inputs.
    # Also compare the accessible components with the two Cut objects present.
    cut={(e['x'],e['y']) for e in event['object_events'] if e['graphics_id']=='OBJ_EVENT_GFX_CUTTABLE_TREE'}
    def reachable(grid,start,blocked):
        found={start};queue=deque([start])
        while queue:
            x,y=queue.popleft()
            for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)):
                p=(x+dx,y+dy)
                if 0<=p[0]<48 and 0<=p[1]<44 and p not in found and p not in blocked and ((grid[p[1]*48+p[0]]>>10)&3)==0:
                    found.add(p);queue.append(p)
        return found
    counts={}
    for state,blocked in [('before_cut',cut),('after_cut',set())]:
        for k,start in enumerate([(16,37),(14,6),(36,37)]):
            a,b=[reachable(g,start,blocked) for g in grids];assert a==b
            counts[f'{state}_{k}']=len(a)
    source=ROOT/'data/maps/PetalburgWoods/scripts.inc'
    assert 'setmetatile' not in source.read_text()
    meta=words(TARGET/'metatiles.bin');attrs=words(TARGET/'metatile_attributes.bin')
    assert len(meta)==len(attrs)*8 and len(attrs)<=512 and all(e>>12<13 for e in meta)
    assert all((e&1023)<1008 for e in meta)
    assert (ROOT/old['border_filepath']).read_bytes()==(ROOT/new['border_filepath']).read_bytes()
    print(json.dumps({'status':'PASS','cells_checked':len(grids[0]),'warps':6,'cut_objects':len(cut),
        'story_triggers':2,'behavior_collision_elevation_identical':True,'interactive_grass_ids_preserved':True,'reachable_cells':counts,
        'secondary_metatiles':len(attrs)},indent=2))

if __name__=='__main__':main()
