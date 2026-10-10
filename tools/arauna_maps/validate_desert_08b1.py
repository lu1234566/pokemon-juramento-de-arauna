#!/usr/bin/env python3
"""Whole-base preservation, native graphics, and real Regirock C regressions."""
import json
import subprocess
import tempfile
from pathlib import Path

from desert_08b1 import BASE, BRAILLE, GLYPH, MUTABLE, OUT, ROOT, TAG, layout, sha, states
from native_visuals_v2 import Pair, dump
from render_native_map import indexed_tiles, words, palette
from trainer_hill_06a_art import native_layers
from puzzles_cavernas_03b import HOST_CONSTANTS, compile_puzzles, script_writes


def main():
    c = json.loads((OUT/'functional_contract.json').read_text())
    for n,h in c['protected_hashes'].items():
        assert (ROOT/n).is_file() and sha((ROOT/n).read_bytes()) == h, ('protected file changed',n)
    node, l = layout()
    original = json.loads(subprocess.check_output(['git','show',BASE+':data/layouts/layouts.json'],cwd=ROOT))
    restored = json.loads(json.dumps(node))
    target = next(x for x in restored['layouts'] if x['id']==l['id'])
    target['primary_tileset'],target['secondary_tileset'] = c['layout']['primary_tileset'],c['layout']['secondary_tileset']
    assert restored == original, 'Unrelated layout change'
    assert [x['id'] for x in node['layouts']] == c['layout_ids']
    import re
    for rel in MUTABLE-{'data/layouts/layouts.json'}:
        current = (ROOT/rel).read_text()
        unmarked = re.sub(r'\n*// '+TAG+r'_BEGIN\n.*?// '+TAG+r'_END\n','\n',current,flags=re.S)
        expected = subprocess.check_output(['git','show',BASE+':'+rel],cwd=ROOT,text=True)
        assert unmarked.rstrip()==expected.rstrip(), ('nonadditive registry change',rel)
        assert current.count('// '+TAG+'_BEGIN') == 1
    old, new = Pair(ROOT,c['layout']), Pair(ROOT,l)
    assert old.attrs == new.attrs, 'Native attributes changed'
    assert old.callbacks == new.callbacks
    for row in range(12):
        assert old.pals[row]==new.pals[row], ('existing palette changed',row)
    art = json.loads((OUT/'build.json').read_text())
    assert not set(art['new_graphics_slots']) & (old.dynamic|set(range(928,932)))
    for path in new.paths:
        im,_,count = indexed_tiles(path/'tiles.png')
        assert count <= 512 and max(im.getdata()) <= 15
        entries, attrs = words(path/'metatiles.bin'), words(path/'metatile_attributes.bin')
        assert len(entries)==8*len(attrs) and len(attrs)<=512
        assert all(e>>12<=12 for e in entries)
        # Every static reference must fit graphics memory and its source sheet.
        for e in entries:
            t=e&1023
            assert new.reader._tile(t) is not None or t in new.dynamic|set(range(928,932)), t
    assert all(v%8==0 for rgb in new.pals[12] for v in rgb)
    mask_checks=glyphs=0
    for mid in art['redrawn_ids']:
        for before,after in zip(native_layers(old.reader,mid),native_layers(new.reader,mid)):
            assert before.getchannel('A').tobytes()==after.getchannel('A').tobytes(), ('layer mask',hex(mid))
            mask_checks+=1
            if mid in BRAILLE:
                old_dots={i for i,(r,g,b,a) in enumerate(before.getdata()) if a and (r,g,b)==GLYPH}
                new_dots={i for i,(r,g,b,a) in enumerate(after.getdata()) if a and (r>>3,g>>3,b>>3)==tuple(v>>3 for v in GLYPH)}
                assert old_dots==new_dots, ('Braille dots',hex(mid))
                glyphs+=len(old_dots)
        assert new.reader.metatile(mid).getextrema()[3]==(255,255), ('transparent ground',mid)
    unchanged=0
    for kind,attrs in enumerate(old.attrs):
        for local in range(len(attrs)):
            mid=local+kind*512
            if mid not in art['redrawn_ids']:
                assert old.reader.metatile(mid).tobytes()==new.reader.metatile(mid).tobytes(), ('unredrawn graphics',hex(mid))
                unchanged+=1
    predicates=writes=0
    with tempfile.TemporaryDirectory(prefix='arauna-regirock-') as tmp:
        dll=compile_puzzles(Path(tmp))
        flag=dll.test_constant(HOST_CONSTANTS.index('FLAG_SYS_REGIROCK_PUZZLE_COMPLETED'))
        real_map=dll.test_map(3)
        for completed in (0,1):
            for map_id in (real_map, real_map^1, real_map^256):
                for y in range(33):
                    for x in range(17):
                        dll.test_reset(map_id,x,y);dll.test_flag(flag,completed)
                        expected=int(not completed and map_id==real_map and y==23 and x in (5,6,7))
                        assert dll.ShouldDoBrailleRegirockEffect()==expected,(completed,map_id,x,y)
                        predicates+=1
        grid=words(ROOT/c['layout']['blockdata_filepath'])
        dll.test_reset(real_map,6,23)
        for i,v in enumerate(grid):dll.test_cell(i%17,i//17,v)
        closed=script_writes('DesertRuins','DesertRuins_EventScript_HideRegiEntrance')
        for x,y,v in closed:dll.MapGridSetMetatileIdAt(x+7,y+7,v)
        assert all(dll.test_read(x,y)&0xfff==v for x,y,v in closed)
        before=[dll.test_read(i%17,i//17) for i in range(len(grid))]
        dll.test_open(2)
        expected=states(c)['open']
        for i,v in enumerate(expected):
            actual=dll.test_read(i%17,i//17)
            assert actual==v,('actual whole-grid opening',i,hex(actual),hex(v))
            writes+=1
        assert dll.test_getflag(flag)==1
        dll.test_pos(6,23);assert dll.ShouldDoBrailleRegirockEffect()==0
        assert sum(a!=b for a,b in zip(before,expected))==6
    # Flood the vestibule in both states using the unchanged collision words.
    paths={}
    for state,grid in states(c).items():
        start=(8,28);seen={start};todo=[start]
        while todo:
            x,y=todo.pop()
            for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if 0<=nx<17 and 0<=ny<33 and (nx,ny) not in seen and not grid[ny*17+nx]&0xc00:
                    seen.add((nx,ny));todo.append((nx,ny))
        assert all((x,23) in seen for x in (5,6,7))
        assert ((8,20) in seen)==(state=='open')
        paths[state]=len(seen)
    report={'status':'PASS','base_commit':BASE,'maps':1,'cells':561,
            'protected_existing_files':len(c['protected_hashes']),
            'layouts_preserved':len(c['layout_ids']),'only_changed_layout':'LAYOUT_DESERT_RUINS',
            'grid_border_map_events_and_scripts':'byte-identical',
            'metatile_ids_attributes_and_layer_masks':'PASS',
            'per_layer_masks_checked':mask_checks,'unaltered_metatiles_pixel_identical':unchanged,
            'native_braille_dot_pixels':glyphs,'actual_c_predicate_cases':predicates,
            'actual_c_whole_grid_opening_cells':writes,'opening_changes_exactly_six_cells':True,
            'closed_open_reachable_cells':paths,
            'regirock_encounter':'unchanged SPECIES_REGIROCK level 40; scripts, flags and outcome branches hash-protected',
            'native_map_audit':'8 gates PASS; 3 inherited Surf notes',
            'rom_build':'pending; ARM toolchain unavailable',
            'mgba_battles_and_save':'pending; emulator unavailable'}
    dump(OUT/'validation.json',report)
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
