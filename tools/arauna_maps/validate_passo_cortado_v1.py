#!/usr/bin/env python3
"""Check volcanic art while preserving Jagged Pass gameplay."""
import json, subprocess
from PIL import Image
from build_passo_cortado_v1 import ROOT, SPECS, BASE, source, target, words, layout_id

def main():
    for symbol, (kind, _, _, _) in SPECS.items():
        original, adapted = source(symbol), target(symbol)
        old_meta, old_attrs = words(original/'metatiles.bin'), words(original/'metatile_attributes.bin')
        meta, attrs = words(adapted/'metatiles.bin'), words(adapted/'metatile_attributes.bin')
        assert meta[:len(old_meta)] == old_meta and attrs[:len(old_attrs)] == old_attrs
        if kind == 'primary':
            assert meta == old_meta and attrs == old_attrs
            assert (original/'tiles.png').read_bytes() == (adapted/'tiles.png').read_bytes()
            assert (original/'palettes/02.pal').read_bytes() == (adapted/'palettes/02.pal').read_bytes()
        else:
            assert len(meta) == 443*8 and len(attrs) == 443
            original_image, image = Image.open(original/'tiles.png'), Image.open(adapted/'tiles.png')
            assert image.mode == 'P' and image.size == (128,256)
            assert image.crop((0,0,128,232)).tobytes() == original_image.tobytes()
            assert not set(v&1023 for v in old_meta).intersection(range(1016,1024))
            for variant in range(2):
                entries = meta[(441+variant)*8:(442+variant)*8]
                assert entries[:4] == old_meta[(625-512)*8:(625-512)*8+4]
                assert [v&1023 for v in entries[4:]] == list(range(1016+variant*4,1020+variant*4))
                assert all(v>>12 == 12 for v in entries[4:])
                assert attrs[441+variant] == old_attrs[625-512] == 0x000c
    rel = 'data/maps/JaggedPass/map.json'
    baseline = json.loads(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT))
    event = json.loads((ROOT/rel).read_text())
    assert event == {**baseline,'layout':layout_id('JaggedPass')}
    layouts = {r['id']:r for r in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
    old, new = layouts[baseline['layout']], layouts[event['layout']]
    assert (new['width'],new['height']) == (old['width'],old['height']) == (30,46)
    assert new['primary_tileset'] == 'gTileset_AraunaPassoPedra'
    assert new['secondary_tileset'] == 'gTileset_AraunaPassoCortado'
    a, b = words(ROOT/old['blockdata_filepath']), words(ROOT/new['blockdata_filepath'])
    assert len(a) == len(b) == 30*46
    occupied = {(int(e['x']),int(e['y'])) for group in ('warp_events','object_events','coord_events','bg_events') for e in event[group]}
    counts = [0,0]
    for i,(before,after) in enumerate(zip(a,b)):
        if before == after: continue
        x,y = i%30,i//30
        assert before&1023 == 625 and after&1023 in (BASE,BASE+1)
        assert (before^after)&~1023 == 0
        assert all(abs(x-p)+abs(y-q) >= 3 for p,q in occupied)
        counts[(after&1023)-BASE] += 1
    assert counts == [14,11]
    for x,y in ((16,17),(16,18)): assert a[y*30+x] == b[y*30+x]
    assert (ROOT/old['border_filepath']).read_bytes() == (ROOT/new['border_filepath']).read_bytes()
    script = 'data/maps/JaggedPass/scripts.inc'
    assert (ROOT/script).read_bytes() == subprocess.check_output(['git','show','HEAD:'+script],cwd=ROOT)
    assert [len(event[k]) for k in ('warp_events','object_events','coord_events','bg_events')] == [5,7,10,2]
    print(json.dumps({'status':'PASS','maps':1,'ash_and_flat_fragments':counts,'warps':5,'objects':7,
                      'coord_events':10,'hidden_items':2,'collision_and_events_preserved':True,
                      'dynamic_hideout_entrance_preserved':True},indent=2))

if __name__ == '__main__': main()
