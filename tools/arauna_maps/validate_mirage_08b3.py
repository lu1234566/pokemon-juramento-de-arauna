#!/usr/bin/env python3
"""Verify Mirage Tower assets and every dependency of the integrated base."""
import json
import re
import subprocess
from mirage_08b3 import BASE,FIXES,NAMES,OUT,ROOT,MUTABLE,TAG,RUNTIME_IDS,inventory,sha
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
    for mid in art['redrawn_ids']:
        for a,b in zip(native_layers(old.reader,mid),native_layers(new.reader,mid)):
            assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes(),('native layer footprint',hex(mid));masks+=1
        assert new.reader.metatile(mid).getextrema()[3]==(255,255),('opaque state',hex(mid))
    for kind,attrs in enumerate(old.attrs):
        for local in range(len(attrs)):
            mid=local+kind*512
            if mid not in art['redrawn_ids']:
                assert old.reader.metatile(mid).tobytes()==new.reader.metatile(mid).tobytes(),('unredrawn ID',hex(mid));unchanged+=1
    labels=(ROOT/'include/constants/metatile_labels.h').read_text()
    assert re.search(r'#define METATILE_Cave_CrackedFloor\s+0x22F',labels)
    assert re.search(r'#define METATILE_Cave_CrackedFloor_Hole\s+0x206',labels)
    assert new.attrs[1][0x22f-512]==0x10d2 and new.attrs[1][0x206-512]==0x66
    assert all(mid in art['redrawn_ids'] for mid in RUNTIME_IDS)
    states={}
    for name in NAMES:
        l=ls[ms[name]['layout']];assert l['primary_tileset']==ls[ms[NAMES[0]]['layout']]['primary_tileset']
        assert l['secondary_tileset']==ls[ms[NAMES[0]]['layout']]['secondary_tileset']
        grid=words(ROOT/l['blockdata_filepath']);cracks=[(i%l['width'],i//l['width']) for i,v in enumerate(grid) if v&1023==0x22f]
        states[name]={'cells':len(grid),'cracked_cells':cracks,'warp_count':len(ms[name]['warp_events']),
            'object_count':len(ms[name]['object_events']),'scripts_events_collision_elevation':'byte-identical'}
    assert len(states[NAMES[1]]['cracked_cells'])==11 and len(states[NAMES[2]]['cracked_cells'])==3
    report={'status':'PASS','base_commit':BASE,'protected_existing_files':len(c['protected_hashes']),
        'protected_fixes':FIXES,'historical_contracts':historical,'layouts_preserved':len(c['layout_ids']),
        'redrawn_ids':len(art['redrawn_ids']),'native_layer_masks_checked':masks,
        'unchanged_pixel_identical_metatiles':unchanged,'maps':states,
        'runtime_states':{'crack':'0x22F, MB_CRACKED_FLOOR (0xD2)','hole':'0x206, MB_CRACKED_FLOOR_HOLE (0x66)',
            'timing_speed_fall_warps':'src/field_tasks.c and cave_hole.inc protected byte-for-byte'},
        'fossil_collapse_and_route111':'scripts, flags, object graphics, exterior animations and corrected tower base protected byte-for-byte',
        'verification_scope':'source hashes, native 4bpp assets, static data and rendered crack/hole states; no simulated gameplay',
        'rom_build':'pending; ARM toolchain unavailable','mgba':'pending for new 08B3; previous 08B2 acceptance supplied by integrator'}
    dump(OUT/'validation.json',report);print(json.dumps(report,indent=2))


if __name__=='__main__':main()
