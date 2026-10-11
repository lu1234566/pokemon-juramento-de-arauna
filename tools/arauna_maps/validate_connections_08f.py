#!/usr/bin/env python3
"""Validate native connection rooms, shared scripts, graphics masks and history."""
import json
import re
import subprocess
from connections_08f import BASE,FIXES,NAMES,OUT,ROOT,MUTABLE,TAG,GROUPS,CHECKPOINTS,inventory,sha,reserve_dma
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
    for folder,exceptions in [('desert_08b1',set(FIXES)),('desert_08b2',set(FIXES)-{'src/party_menu.c'}),('mirage_08b3',scripts),('sstidal_08c',scripts),('islands_08d',set()),('contests_08e',set())]:
        old=json.loads((ROOT/'review'/folder/'functional_contract.json').read_text());diff={n for n,h in old['protected_hashes'].items() if sha((ROOT/n).read_bytes())!=h}
        assert diff==exceptions,(folder,diff,exceptions);historical[folder]={'contract':'unchanged','documented_integration_exceptions':sorted(diff)}
    build=json.loads((OUT/'build.json').read_text());groups={};masks=unchanged=quarters=0
    for key,g in GROUPS.items():
        old=reserve_dma(Pair(ROOT,c['maps'][g['names'][0]]['layout']));new=reserve_dma(Pair(ROOT,ls[ms[g['names'][0]]['layout']]));art=build['groups'][key]
        assert old.attrs==new.attrs and old.callbacks==new.callbacks==art['callbacks']==['InitTilesetAnim_Building','NULL']
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
            'runtime_metatile_swaps':'none in these rooms; Cable Club gates are in frozen Centers; UnionRoom toggles occupancy flags'}
    states={};event_cells=[]
    for n in NAMES:
        m=ms[n];assert m==c['maps'][n]['map'];l=ls[m['layout']];grid=words(ROOT/l['blockdata_filepath'])
        assert len(grid)==l['width']*l['height']
        for event in m['warp_events']+m['coord_events']:
            x,y=event['x'],event['y'];assert 0<=x<l['width'] and 0<=y<l['height']
            cell=grid[y*l['width']+x];assert not cell&0xc00,(n,'blocked session point',x,y,hex(cell))
            event_cells.append({'map':n,'x':x,'y':y,'cell':hex(cell)})
        assert all(w['dest_map']=='MAP_DYNAMIC' and w['dest_warp_id']=='WARP_ID_DYNAMIC' for w in m['warp_events'])
        states[n]={'cells':len(grid),'objects':len(m['object_events']),'dynamic_return_warps':len(m['warp_events']),
            'coord_events':len(m['coord_events']),'scripts_grid_border_collision_elevation':'byte-identical to f0f08e4ed2'}
    assert sum(m['cells'] for m in states.values())==740 and len(event_cells)==26
    cable=(ROOT/'data/scripts/cable_club.inc').read_text();union_script=(ROOT/'data/maps/UnionRoom/scripts.inc').read_text()
    entries=[('warp MAP_BATTLE_COLOSSEUM_2P, 6, 8'),('warp MAP_BATTLE_COLOSSEUM_4P, 5, 8'),('setwarp MAP_TRADE_CENTER, 5, 8'),('setwarp MAP_RECORD_CORNER, 8, 9'),('warpspinenter MAP_UNION_ROOM, 7, 11')]
    for line in entries:assert line in cable
    for function in ('ColosseumPlayerSpotTriggered','PlayerEnteredTradeSeat','RecordMixingPlayerSpotTriggered','ChooseHalfPartyForBattle'):
        assert 'special '+function in cable
    assert 'special RunUnionRoom' in union_script
    # The eight leader centers and their cross-shaped five-person groups come
    # from production C. All 40 cells must remain reachable and undecorated
    # by a newly-added blocking object; map events and collision stay frozen.
    source=(ROOT/'src/union_room_player_avatar.c').read_text()
    parse=lambda key:[tuple(map(int,m)) for m in re.findall(r'\{\s*(-?\d+),\s*(-?\d+)\s*\}',re.search(key+r'\[.*?= \{(.*?)\};',source,re.S)[1])]
    leaders=parse('sUnionRoomPlayerCoords');offsets=parse('sUnionRoomGroupOffsets');assert len(leaders)==8 and len(offsets)==5
    union_l=ls[ms['UnionRoom']['layout']];grid=words(ROOT/union_l['blockdata_filepath']);group_cells=[]
    for i,(lx,ly) in enumerate(leaders):
        for j,(dx,dy) in enumerate(offsets):
            x,y=lx+dx,ly+dy;assert 0<=x<15 and 0<=y<12
            cell=grid[y*15+x];assert not cell&0xc00,('blocked group slot',i,j,x,y,hex(cell))
            group_cells.append({'leader':i,'member':j,'x':x,'y':y,'cell':hex(cell)})
    assert 'MapGridSetMetatileImpassabilityAt(x, y, TRUE)' in source and 'MapGridSetMetatileImpassabilityAt(x, y, FALSE)' in source
    for n in ('src/union_room.c','src/union_room_player_avatar.c','src/union_room_battle.c','src/union_room_chat.c','src/data/union_room.h','src/link.c','src/link_rfu_2.c','src/link_rfu_3.c','src/cable_club.c','src/trade.c','src/data/trade.h','src/record_mixing.c','data/scripts/cable_club.inc','data/scripts/record_mix.inc','data/maps/UnionRoom/scripts.inc'):
        assert n in c['protected_hashes'],n
    headers=(ROOT/'src/data/tilesets/headers.h').read_text();graphics=(ROOT/'src/data/tilesets/graphics.h').read_text()
    compression=lambda symbol:re.search(r'const struct Tileset '+symbol+r'\s*=\s*\{(.*?)\};',headers,re.S)[1].split('.isCompressed = ',1)[1].split(',',1)[0]=='TRUE'
    for key,g in GROUPS.items():
        old=c['maps'][g['names'][0]]['layout'];new=ls[ms[g['names'][0]]['layout']];art=build['groups'][key]
        flags=[compression(old[f]) for f in ('primary_tileset','secondary_tileset')]
        assert flags==art['is_compressed']==[compression(new[f]) for f in ('primary_tileset','secondary_tileset')]==[True,key=='union']
        for bank,flag in zip(art['banks'],flags):assert bank+'/tiles.png", "'+('.4bpp.lz' if flag else '.4bpp')+'"' in graphics
        groups[key]['compression_preserved']=flags
    report={'status':'PASS','base_commit':BASE,'protected_existing_files':len(c['protected_hashes']),
        'protected_fixes':FIXES,'historical_contracts':historical,'layouts_preserved':len(c['layout_ids']),
        'groups':groups,'redrawn_id_instances':sum(g['redrawn_ids'] for g in groups.values()),'native_layer_masks_checked':masks,
        'unredrawn_pixel_identical_metatiles':unchanged,'animated_quarters_preserved':quarters,'maps':states,
        'event_points_verified':event_cells,'union_room_40_group_cells_verified':group_cells,'entry_points_verified':entries,
        'mechanics':'two/four-player battles, party selection, trade seats, record mixing, dynamic returns, eight wireless groups and dynamic occupancy, session palettes and saved data frozen',
        'verification_scope':'source hashes, exact native grids/attributes, layer footprints, compression, DMA words and renders; no simulated multiplayer session',
        'rom_build':'pending; ARM compiler unavailable','mgba':'pending for new 08F; 08E real contests accepted in INTEGRACAO_08E.md; Link was not tested there'}
    dump(OUT/'validation.json',report)
    for checkpoint,names in CHECKPOINTS.items():dump(OUT/(checkpoint+'.json'),{'status':'PASS_STATIC','maps':list(names),'base_commit':BASE,'validation':'review/connections_08f/validation.json','runtime_acceptance':'pending mGBA and compatible multiplayer session'})
    print(json.dumps({k:v for k,v in report.items() if k not in ('maps','groups','protected_fixes','historical_contracts','event_points_verified','union_room_40_group_cells_verified','entry_points_verified')},indent=2))


if __name__=='__main__':main()
