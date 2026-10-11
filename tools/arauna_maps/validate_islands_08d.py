#!/usr/bin/env python3
"""Verify six native islands, their runtime states and integrated fixes."""
import json
import re
import subprocess
from islands_08d import BASE,FIXES,NAMES,OUT,ROOT,MUTABLE,TAG,GROUPS,CHECKPOINTS,inventory,sha,reserve_dma,renderer
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
    assert restored==original and [l['id'] for l in node['layouts']]==c['layout_ids']
    for rel in MUTABLE-{'data/layouts/layouts.json'}:
        text=(ROOT/rel).read_text();stripped=re.sub(r'\n*// '+TAG+r'_BEGIN\n.*?// '+TAG+r'_END\n','\n',text,flags=re.S)
        expected=subprocess.check_output(['git','show',BASE+':'+rel],cwd=ROOT,text=True);assert stripped.rstrip()==expected.rstrip() and text.count('// '+TAG+'_BEGIN')==1,rel
    historical={};scripts={n for n in FIXES if n.endswith('.inc')}
    for folder,exceptions in [('desert_08b1',set(FIXES)),('desert_08b2',set(FIXES)-{'src/party_menu.c'}),('mirage_08b3',scripts),('sstidal_08c',scripts)]:
        old=json.loads((ROOT/'review'/folder/'functional_contract.json').read_text());diff={n for n,h in old['protected_hashes'].items() if sha((ROOT/n).read_bytes())!=h}
        assert diff==exceptions,(folder,diff,exceptions);historical[folder]={'contract':'unchanged','documented_integration_exceptions':sorted(diff)}
    build=json.loads((OUT/'build.json').read_text());groups={};masks=unchanged=waterquarters=waterframes=0
    for key,g in GROUPS.items():
        old=reserve_dma(Pair(ROOT,c['maps'][g['names'][0]]['layout']));new=reserve_dma(Pair(ROOT,ls[ms[g['names'][0]]['layout']]));art=build['groups'][key]
        assert old.attrs==new.attrs and old.callbacks==new.callbacks==art['callbacks']
        assert old.pals[:12]==new.pals[:12] and all(v%8==0 for rgb in new.pals[12] for v in rgb)
        assert not set(art['new_graphics_slots'])&old.dynamic and set(art['reserved_dma_slots'])==old.dynamic
        for quarter in art['preserved_static_sea_quarters']:
            mid=quarter['mid'];index=mid%512*8+quarter['quarter'];assert old.meta[mid>=512][index]==new.meta[mid>=512][index]==quarter['word']
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
                if a&1023 in old.dynamic:assert a==b,('animated quarter word',key,hex(mid));waterquarters+=1
        for kind,attrs in enumerate(old.attrs):
            for local in range(len(attrs)):
                mid=local+kind*512
                if mid not in art['redrawn_ids']:
                    assert old.reader.metatile(mid).tobytes()==new.reader.metatile(mid).tobytes(),('unredrawn RGB',key,hex(mid));unchanged+=1
        # Compare actual animated images, with source callback ranges decoded.
        # Rustboro's staggered lanes share a phase here; word preservation also
        # proves equivalence for every independently staggered native lane.
        aquatic=[mid for mid in art['active_and_runtime_ids'] if old.attrs[mid>=512][mid%512]&255 in (0x15,0x16)]
        for frame in range(8):
            a=renderer(c['maps'][g['names'][0]]['layout'],frame);b=renderer(ls[ms[g['names'][0]]['layout']],frame)
            for mid in aquatic:assert a.metatile(mid).tobytes()==b.metatile(mid).tobytes(),('water animation',key,hex(mid),frame);waterframes+=1
        groups[key]={'redrawn_ids':len(art['redrawn_ids']),'new_static_slots':len(art['new_graphics_slots']),
            'static_sea_quarters_preserved':len(art['preserved_static_sea_quarters']),
            'callbacks_preserved':old.callbacks,'complete_attributes':'identical','palettes_0_through_11':'identical',
            'runtime_ids_checked':[hex(i) for i in art['runtime_ids']]}
    states={}
    for n in NAMES:
        m=ms[n];assert m==c['maps'][n]['map'];l=ls[m['layout']];grid=words(ROOT/l['blockdata_filepath'])
        assert len(grid)==l['width']*l['height'];states[n]={'cells':len(grid),'warps':len(m['warp_events']),
            'objects':len(m['object_events']),'coord_events':len(m['coord_events']),'bg_events':len(m['bg_events']),
            'scripts_grid_border_collision_elevation':'byte-identical to 72b72497ac'}
    # These literal coordinates come from production C and remain obstacles,
    # not decorative floor. The AI for Mew depends on all four positions.
    mew_l=ls[ms['FarawayIsland_Interior']['layout']];grid=words(ROOT/mew_l['blockdata_filepath']);rocks=[]
    source=(ROOT/'src/faraway_island.c').read_text()
    for x,y in [(14,9),(18,9),(9,10),(13,13)]:
        assert re.search(r'\{\s*'+str(x)+r'\s*\+ MAP_OFFSET,\s*'+str(y)+r'\s*\+ MAP_OFFSET\s*\}',source)
        v=grid[y*mew_l['width']+x];assert v&0xc00 and v&1023==0xe0;rocks.append({'x':x,'y':y,'cell':hex(v)})
    assert ms['FarawayIsland_Interior']['object_events'][0]['movement_type']=='MOVEMENT_TYPE_COPY_PLAYER_OPPOSITE_IN_GRASS'
    assert 'case METATILE_General_LongGrass:' in (ROOT/'src/fldeff_cut.c').read_text()
    deoxys=(ROOT/'src/field_specials.c').read_text();coords=re.search(r'sDeoxysRockCoords\[DEOXYS_ROCK_LEVELS\]\[2\] = \{(.*?)\};',deoxys,re.S)[1]
    points=[tuple(map(int,m)) for m in re.findall(r'\{\s*(\d+),\s*(\d+)\s*\}',coords)];assert len(points)==11
    l=ls[ms['BirthIsland_Exterior']['layout']];grid=words(ROOT/l['blockdata_filepath'])
    for x,y in points:assert not grid[y*l['width']+x]&0xc00,('Deoxys landing blocked',x,y)
    assert '4, 8, 8, 8, 4, 4, 4, 6, 3, 3' in deoxys
    assert ms['BirthIsland_Harbor']['layout']=='LAYOUT_ISLAND_HARBOR'
    users=[json.loads(p.read_text())['name'] for p in (ROOT/'data/maps').glob('*/map.json') if json.loads(p.read_text())['layout']=='LAYOUT_ISLAND_HARBOR'];assert users==['BirthIsland_Harbor'],users
    report={'status':'PASS','base_commit':BASE,'protected_existing_files':len(c['protected_hashes']),
        'protected_fixes':FIXES,'historical_contracts':historical,'layouts_preserved':len(c['layout_ids']),
        'groups':groups,'redrawn_id_instances':sum(g['redrawn_ids'] for g in groups.values()),'native_layer_masks_checked':masks,
        'unredrawn_pixel_identical_metatiles':unchanged,'animated_quarters_preserved':waterquarters,'water_state_frame_comparisons':waterframes,
        'maps':states,'mew_rocks':rocks,'deoxys_11_positions':points,
        'mechanics':'tickets, ferry returns, Lati encounter/Soul Dew, Deoxys coordinates/step limits/11 sprite palettes, Mew pursuit/Cut/grass effects and capture/defeat/flee flags frozen',
        'verification_scope':'source hashes, exact native grids and attributes, runtime state artwork, DMA words and renders; no simulated gameplay or battles',
        'rom_build':'pending; ARM compiler unavailable','mgba':'pending for new 08D; 08C acceptance is in INTEGRACAO_08C.md'}
    dump(OUT/'validation.json',report)
    for checkpoint,names in CHECKPOINTS.items():dump(OUT/(checkpoint+'.json'),{'status':'PASS_STATIC','maps':list(names),'base_commit':BASE,'validation':'review/islands_08d/validation.json','runtime_acceptance':'pending mGBA'})
    print(json.dumps({k:v for k,v in report.items() if k not in ('maps','groups','protected_fixes','historical_contracts')},indent=2))


if __name__=='__main__':main()
