#!/usr/bin/env python3
"""Validate native contest stages, shared scripts, graphics masks and history."""
import json
import re
import subprocess
from contests_08e import BASE,FIXES,NAMES,OUT,ROOT,MUTABLE,TAG,GROUPS,CHECKPOINTS,inventory,sha,reserve_dma
from native_visuals_v2 import Pair,dump
from trainer_hill_06a_art import native_layers
from render_native_map import words,indexed_tiles


def main():
    c=json.loads((OUT/'functional_contract.json').read_text());assert c['base_commit']==BASE and c['protected_fixes']==FIXES
    for rel,h in FIXES.items():assert c['protected_hashes'][rel]==h==sha((ROOT/rel).read_bytes()),rel
    for rel,h in c['protected_hashes'].items():assert (ROOT/rel).is_file() and sha((ROOT/rel).read_bytes())==h,('protected',rel)
    node,ls,ms=inventory();original=json.loads(subprocess.check_output(['git','show',BASE+':data/layouts/layouts.json'],cwd=ROOT));restored=json.loads(json.dumps(node))
    for l in restored['layouts']:
        if l['id'] in {ms[n]['layout'] for n in NAMES}:
            old=next(c['maps'][n]['layout'] for n in NAMES if ms[n]['layout']==l['id']);l['primary_tileset'],l['secondary_tileset']=old['primary_tileset'],old['secondary_tileset']
    assert restored==original and [l['id'] for l in node['layouts']]==c['layout_ids'] and len(c['layout_ids'])==754
    for rel in MUTABLE-{'data/layouts/layouts.json'}:
        text=(ROOT/rel).read_text();stripped=re.sub(r'\n*// '+TAG+r'_BEGIN\n.*?// '+TAG+r'_END\n','\n',text,flags=re.S)
        expected=subprocess.check_output(['git','show',BASE+':'+rel],cwd=ROOT,text=True);assert stripped.rstrip()==expected.rstrip() and text.count('// '+TAG+'_BEGIN')==1,rel
    historical={};scripts={n for n in FIXES if n.endswith('.inc')}
    for folder,exceptions in [('desert_08b1',set(FIXES)),('desert_08b2',set(FIXES)-{'src/party_menu.c'}),('mirage_08b3',scripts),('sstidal_08c',scripts),('islands_08d',set())]:
        old=json.loads((ROOT/'review'/folder/'functional_contract.json').read_text());diff={n for n,h in old['protected_hashes'].items() if sha((ROOT/n).read_bytes())!=h}
        assert diff==exceptions,(folder,diff,exceptions);historical[folder]={'contract':'unchanged','documented_integration_exceptions':sorted(diff)}
    build=json.loads((OUT/'build.json').read_text());groups={};masks=unchanged=quarters=0
    for key,g in GROUPS.items():
        old=reserve_dma(Pair(ROOT,c['maps'][g['names'][0]]['layout']));new=reserve_dma(Pair(ROOT,ls[ms[g['names'][0]]['layout']]));art=build['groups'][key]
        assert old.attrs==new.attrs and old.callbacks==new.callbacks==art['callbacks']==['InitTilesetAnim_General','NULL']
        assert old.pals[:12]==new.pals[:12] and all(v%8==0 for rgb in new.pals[12] for v in rgb)
        assert not any(e>>12==12 and e&1023 for a in old.meta for e in a)
        assert not set(art['new_graphics_slots'])&old.dynamic and set(art['reserved_dma_slots'])==old.dynamic
        for t in old.dynamic:
            a,b=old.reader._tile(t),new.reader._tile(t)
            if a is not None:assert b is not None and a.tobytes()==b.tobytes(),('DMA source',key,t)
        for path in new.paths:
            im,_,count=indexed_tiles(path/'tiles.png');assert count<=512 and max(im.getdata())<=15
            entries,attrs=words(path/'metatiles.bin'),words(path/'metatile_attributes.bin');assert len(entries)==len(attrs)*8 and len(attrs)<=512
            for e in entries:assert e>>12<=12 and (new.reader._tile(e&1023) is not None or e&1023 in old.dynamic),(key,hex(e))
        for mid in art['active_and_runtime_ids']:
            for a,b in zip(native_layers(old.reader,mid),native_layers(new.reader,mid)):
                assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes(),('layer footprint',key,hex(mid));masks+=1
            assert old.reader.metatile(mid).getchannel('A').tobytes()==new.reader.metatile(mid).getchannel('A').tobytes(),('composite footprint',key,hex(mid))
            for a,b in zip(old.meta[mid>=512][mid%512*8:mid%512*8+8],new.meta[mid>=512][mid%512*8:mid%512*8+8]):
                if a&1023 in old.dynamic:assert a==b,('animated quarter word',key,hex(mid));quarters+=1
        for kind,attrs in enumerate(old.attrs):
            for local in range(len(attrs)):
                mid=local+kind*512
                if mid not in art['redrawn_ids']:
                    assert old.reader.metatile(mid).tobytes()==new.reader.metatile(mid).tobytes(),('unredrawn RGB',key,hex(mid));unchanged+=1
        groups[key]={'redrawn_ids':len(art['redrawn_ids']),'new_static_slots':len(art['new_graphics_slots']),
            'callbacks_preserved':old.callbacks,'complete_attributes':'identical','palettes_0_through_11':'identical',
            'runtime_metatile_swaps':'none in the shared hall scripts; lobby swaps are in a separate frozen bank'}
    states={}
    for n in NAMES:
        m=ms[n];assert m==c['maps'][n]['map'];l=ls[m['layout']];grid=words(ROOT/l['blockdata_filepath'])
        assert len(grid)==l['width']*l['height']==165
        source=ms[NAMES[0]]
        if n!=NAMES[0]:assert m['shared_events_map']==m['shared_scripts_map']=='ContestHall'
        states[n]={'cells':len(grid),'shared_event_objects':len(source['object_events']),'static_warps':len(source['warp_events']),
            'scripts_grid_border_collision_elevation':'byte-identical to e740b80190'}
    hall=(ROOT/'data/maps/ContestHall/scripts.inc').read_text();common=(ROOT/'data/scripts/contest_hall.inc').read_text()
    lobby=(ROOT/'data/maps/LilycoveCity_ContestLobby/scripts.inc').read_text()
    assert not re.search(r'\bsetmetatile\b',hall+common)
    for category in ('COOL','BEAUTY','CUTE','SMART','TOUGH'):assert 'setwarp MAP_CONTEST_HALL_'+category+', 7, 5' in lobby
    assert hall.count('warp MAP_LILYCOVE_CITY_CONTEST_LOBBY, 14, 4')==4 and hall.count('warp MAP_LILYCOVE_CITY_CONTEST_LOBBY, 15, 4')==1
    for function in ('DoContestAppeals','ContestResults','GiveWinnerPrize','ShowContestMons','CongratulateWinner'):
        assert 'call ContestHall_EventScript_'+function in common
    for n in ('src/contest.c','src/contest_util.c','src/contest_link.c','src/contest_effect.c','src/contest_painting.c','data/scripts/contest_hall.inc','data/maps/ContestHall/scripts.inc','data/maps/LilycoveCity_ContestLobby/scripts.inc'):
        assert n in c['protected_hashes']
    audience=re.findall(r'createvobject \w+, \d+, (\d+), (\d+), \d+, DIR_\w+',hall)
    assert audience and all(0<=int(x)<15 and 0<=int(y)<11 for x,y in audience)
    report={'status':'PASS','base_commit':BASE,'protected_existing_files':len(c['protected_hashes']),
        'protected_fixes':FIXES,'historical_contracts':historical,'layouts_preserved':len(c['layout_ids']),
        'groups':groups,'redrawn_id_instances':sum(g['redrawn_ids'] for g in groups.values()),'native_layer_masks_checked':masks,
        'unredrawn_pixel_identical_metatiles':unchanged,'animated_quarters_preserved':quarters,'maps':states,
        'scripted_audience_placements_verified':len(audience),'category_entry_points':5,'rank_returns':4,'link_returns':1,
        'mechanics':'all categories/ranks, entrants, scripted audience, appeals, score UI, prizes/ribbons, winner paintings, save flags, lobby gate swaps and link/wireless synchronization frozen',
        'verification_scope':'source hashes, exact native grids/attributes, layer footprints, DMA words and renders; no simulated gameplay',
        'rom_build':'pending; ARM compiler unavailable','mgba':'pending for new 08E; 08D acceptance recorded in INTEGRACAO_08D.md'}
    dump(OUT/'validation.json',report)
    for checkpoint,names in CHECKPOINTS.items():dump(OUT/(checkpoint+'.json'),{'status':'PASS_STATIC','maps':list(names),'base_commit':BASE,'validation':'review/contests_08e/validation.json','runtime_acceptance':'pending mGBA'})
    print(json.dumps({k:v for k,v in report.items() if k not in ('maps','groups','protected_fixes','historical_contracts')},indent=2))


if __name__=='__main__':main()
