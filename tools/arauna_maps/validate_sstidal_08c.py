#!/usr/bin/env python3
"""Verify ferry art, native door animation stacks and all integrated dependencies."""
import json
import re
import subprocess
from sstidal_08c import BASE,FIXES,NAMES,OUT,ROOT,MUTABLE,TAG,DOOR_IDS,inventory,sha
from native_visuals_v2 import Pair,dump
from trainer_hill_06a_art import native_layers
from render_native_map import words,indexed_tiles


def main():
    c=json.loads((OUT/'functional_contract.json').read_text())
    assert c['base_commit']==BASE and c['protected_fixes']==FIXES
    for rel,h in FIXES.items():assert c['protected_hashes'][rel]==h==sha((ROOT/rel).read_bytes()),rel
    for rel,h in c['protected_hashes'].items():
        assert (ROOT/rel).is_file() and sha((ROOT/rel).read_bytes())==h,('protected file',rel)
    node,ls,ms=inventory()
    original=json.loads(subprocess.check_output(['git','show',BASE+':data/layouts/layouts.json'],cwd=ROOT))
    restored=json.loads(json.dumps(node))
    for l in restored['layouts']:
        if l['id'] in {ms[n]['layout'] for n in NAMES}:
            old=next(c['maps'][n]['layout'] for n in NAMES if ms[n]['layout']==l['id'])
            l['primary_tileset'],l['secondary_tileset']=old['primary_tileset'],old['secondary_tileset']
    assert restored==original and [l['id'] for l in node['layouts']]==c['layout_ids']
    for rel in MUTABLE-{'data/layouts/layouts.json'}:
        text=(ROOT/rel).read_text()
        stripped=re.sub(r'\n*// '+TAG+r'_BEGIN\n.*?// '+TAG+r'_END\n','\n',text,flags=re.S)
        expected=subprocess.check_output(['git','show',BASE+':'+rel],cwd=ROOT,text=True)
        assert stripped.rstrip()==expected.rstrip() and text.count('// '+TAG+'_BEGIN')==1,rel
    historical={}
    for checkpoint,exceptions in (('08b1',set(FIXES)),('08b2',set(FIXES)-{'src/party_menu.c'})):
        contract=json.loads((ROOT/f'review/desert_{checkpoint}/functional_contract.json').read_text())
        differences={rel for rel,h in contract['protected_hashes'].items() if sha((ROOT/rel).read_bytes())!=h}
        assert differences==exceptions,(checkpoint,differences)
        historical[checkpoint]={'contract':'unchanged','intentional_integration_exceptions':sorted(differences)}
    previous=json.loads((ROOT/'review/mirage_08b3/functional_contract.json').read_text())
    for rel,h in previous['protected_hashes'].items():assert sha((ROOT/rel).read_bytes())==h,('08B3 historical dependency',rel)
    historical['08b3']={'contract':'unchanged','intentional_integration_exceptions':[]}
    old=Pair(ROOT,c['maps'][NAMES[0]]['layout']);new=Pair(ROOT,ls[ms[NAMES[0]]['layout']])
    art=json.loads((OUT/'build.json').read_text());assert old.attrs==new.attrs
    assert old.callbacks==new.callbacks==['InitTilesetAnim_General','NULL']
    assert old.pals[:12]==new.pals[:12] and all(v%8==0 for rgb in new.pals[12] for v in rgb)
    assert not set(art['new_graphics_slots'])&old.dynamic
    for t in old.dynamic:
        a,b=old.reader._tile(t),new.reader._tile(t)
        if a is not None:assert b is not None and a.tobytes()==b.tobytes(),('DMA source',t)
    for path in new.paths:
        im,_,count=indexed_tiles(path/'tiles.png');assert count<=512 and max(im.getdata())<=15
        entries,attrs=words(path/'metatiles.bin'),words(path/'metatile_attributes.bin')
        assert len(entries)==8*len(attrs) and len(attrs)<=512
        for e in entries:assert e>>12<=12 and (new.reader._tile(e&1023) is not None or e&1023 in old.dynamic)
    masks=unchanged=0
    for mid in art['active_ids']:
        for a,b in zip(native_layers(old.reader,mid),native_layers(new.reader,mid)):
            assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes(),('native layer footprint',hex(mid));masks+=1
        assert new.reader.metatile(mid).getextrema()[3]==(255,255),('opaque state',hex(mid))
    for kind,attrs in enumerate(old.attrs):
        for local in range(len(attrs)):
            mid=local+kind*512
            if mid not in art['redrawn_ids']:
                assert old.reader.metatile(mid).tobytes()==new.reader.metatile(mid).tobytes(),('unredrawn ID',hex(mid));unchanged+=1

    for mid in DOOR_IDS:
        assert mid not in art['redrawn_ids']
        assert old.meta[1][(mid-512)*8:(mid-512)*8+8]==new.meta[1][(mid-512)*8:(mid-512)*8+8]
        assert old.reader.metatile(mid).tobytes()==new.reader.metatile(mid).tobytes()
    labels=(ROOT/'include/constants/metatile_labels.h').read_text()
    assert re.search(r'#define METATILE_InsideShip_IntactDoor_Bottom_Unlocked\s+0x22B',labels)
    assert re.search(r'#define METATILE_InsideShip_IntactDoor_Bottom_Interior\s+0x297',labels)
    door_source=(ROOT/'src/field_door.c').read_text()
    assert 'sDoorAnimTiles_AbandonedShip, sDoorAnimPalettes_AbandonedShip' in door_source
    assert 'sDoorAnimTiles_AbandonedShipRoom, sDoorAnimPalettes_AbandonedShipRoom' in door_source
    assert old.pals[7]==new.pals[7]
    states={};stacks=0
    for name in NAMES:
        l=ls[ms[name]['layout']];assert l['primary_tileset']==ls[ms[NAMES[0]]['layout']]['primary_tileset']
        assert l['secondary_tileset']==ls[ms[NAMES[0]]['layout']]['secondary_tileset']
        grid=words(ROOT/l['blockdata_filepath']);doors=[]
        for event in ms[name]['warp_events']:
            x,y=event['x'],event['y'];mid=grid[y*l['width']+x]&1023
            if mid in (0x22b,0x297):
                above=grid[(y-1)*l['width']+x]&1023
                assert above in DOOR_IDS
                for i in (mid,above):assert old.reader.metatile(i).tobytes()==new.reader.metatile(i).tobytes()
                doors.append({'x':x,'y':y,'bottom':hex(mid),'top':hex(above)});stacks+=1
        states[name]={'cells':len(grid),'warp_count':len(ms[name]['warp_events']),
            'object_count':len(ms[name]['object_events']),'bg_event_count':len(ms[name]['bg_events']),
            'animated_door_stacks':doors,'scripts_events_collision_elevation':'byte-identical'}
    assert stacks==8
    hidden=ms['SSTidalLowerDeck']['bg_events'][0]
    assert hidden['type']=='hidden_item' and hidden['item']=='ITEM_LEFTOVERS' and (hidden['x'],hidden['y'])==(0,2)
    beds=[e for e in ms['SSTidalRooms']['bg_events'] if e['script']=='SSTidalRooms_EventScript_Bed']
    assert {(e['x'],e['y']) for e in beds}=={(15,11),(15,12)}
    report={'status':'PASS','base_commit':BASE,'protected_existing_files':len(c['protected_hashes']),
        'protected_fixes':FIXES,'historical_contracts':historical,'layouts_preserved':len(c['layout_ids']),
        'redrawn_ids':len(art['redrawn_ids']),'native_layer_masks_checked':masks,
        'unchanged_pixel_identical_metatiles':unchanged,'maps':states,
        'door_animation':{'preserved_ids':[hex(i) for i in DOOR_IDS],'stacks':stacks,
            'frames_palette7_source_and_field_door':'byte-identical; closed top/bottom preserved in all eight animated doorways'},
        'journey_logic':'Scott invitation, dynamic destinations, voyage steps, portholes, party healing, Snatch TM, Leftovers and trainer state protected byte-for-byte',
        'verification_scope':'source hashes, native 4bpp assets, attributes and door stacks; no simulated voyage or battles',
        'rom_build':'pending; ARM toolchain unavailable','mgba':'pending for new 08C; previous 08B3 acceptance recorded in INTEGRACAO_08B3.md'}
    dump(OUT/'validation.json',report);print(json.dumps(report,indent=2))


if __name__=='__main__':main()
