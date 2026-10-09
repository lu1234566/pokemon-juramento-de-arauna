#!/usr/bin/env python3
"""Preservation, native geometry, door footprints and production selectors."""
import argparse,hashlib,json,re,tempfile
from pathlib import Path
from native_visuals_v2 import dump,callback
from frontier_07b_common import BASE,ROOT,OUT,NAMES,inventory,renderer,protected_ids,require_base,door_records
from trainer_hill_06a_art import native_layers
from render_native_map import words,indexed_tiles
from bancos_nativos import resolve_bank
import safari_05_c_checks as selectors
from frontier_07b_c_checks import checks
from frontier_07b_animation_checks import animation_checks
from build_frontier_07b import indexed_quadrant

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    contract=json.loads((OUT/'functional_contract.json').read_text());build=json.loads((OUT/'build.json').read_text());entry=build['banks']['dome']
    for rel,h in contract['protected_hashes'].items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,('frozen',rel)
    old,bl,bm=inventory(base);node,ls,maps=inventory(ROOT);assert len(node['layouts'])==len(old['layouts'])==754
    targets={bm[n]['layout'] for n in NAMES}
    for a,b in zip(old['layouts'],node['layouts']):
        fields={'primary_tileset','secondary_tileset'} if a['id'] in targets else set()
        assert {k:v for k,v in a.items() if k not in fields}=={k:v for k,v in b.items() if k not in fields},a['id']
    for k in ('graphics.h','metatiles.h','headers.h'):
        raw=(ROOT/'src/data/tilesets'/k).read_text();stripped=re.sub(r'\n*// FRONTIER_07B_BEGIN\n.*?// FRONTIER_07B_END\n','\n',raw,flags=re.S)
        assert stripped.rstrip()==(base/'src/data/tilesets'/k).read_text().rstrip(),k
    l=ls[maps[NAMES[0]]['layout']];r=renderer(ROOT,l,-1);br=renderer(base,bl[bm[NAMES[0]]['layout']],-1)
    attrs=masks=0
    for kind,rel in enumerate(entry['paths']):
        p=ROOT/rel;source=base/entry['source_paths'][kind]
        assert (p/'metatile_attributes.bin').read_bytes()==(source/'metatile_attributes.bin').read_bytes();attrs+=len(words(p/'metatile_attributes.bin'))
        im,row,count=indexed_tiles(p/'tiles.png');assert count<=512 and max(im.getdata())<=15
        assert callback(ROOT,l[('primary_tileset','secondary_tileset')[kind]])==entry['callbacks'][kind]
        for e in words(p/'metatiles.bin'):assert e>>12<=12 and r._tile(e&1023) is not None
    for q in range(12):assert r.palettes[q]==br.palettes[q],('palette',q)
    assert not set(entry['allocated_tiles']) & (set(range(432,512))|set(range(992,1024)))
    # Every attribute and both alpha masks, including script-only open states.
    for mid in range(len(r.primary_metatiles)//8):assert r.metatile(mid).tobytes()==br.metatile(mid).tobytes(),('primary',mid)
    for mid in range(512,512+len(r.secondary_metatiles)//8):
        for a,b in zip(native_layers(br,mid),native_layers(r,mid)):
            assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes(),('mask',mid);masks+=1
        if mid not in entry['redrawn_ids']:assert r.metatile(mid).tobytes()==br.metatile(mid).tobytes(),('untouched',mid)
    animated_masks=0
    for mid in range(512,512+len(r.secondary_metatiles)//8):
        old_entries=br.secondary_metatiles[(mid-512)*8:(mid-512+1)*8]
        new_entries=r.secondary_metatiles[(mid-512)*8:(mid-512+1)*8]
        for j,(e,f) in enumerate(zip(old_entries,new_entries)):
            if e>>12==8:
                assert f>>12==8,('animated bank',mid,j)
                a=indexed_quadrant(br,e);b=indexed_quadrant(r,f)
                for v in (13,15):
                    assert bytes(x==v for x in a.getdata())==bytes(x==v for x in b.getdata()),('animated footprint',mid,j,v);animated_masks+=1
            else:
                assert f>>12!=8,('new animated quadrant',mid,j)
    # All seven already completed Tower maps retain exact native renders.
    from frontier_07a_common import NAMES as TOWER
    from navel_06b_common import render
    for n in TOWER:assert render(ROOT,ls[maps[n]['layout']],-1).tobytes()==render(base,bl[bm[n]['layout']],-1).tobytes(),('previous Tower',n)
    assert door_records(ROOT)==contract['doors']==door_records(base)
    for mid in protected_ids(base):assert r.metatile(mid).tobytes()==br.metatile(mid).tobytes(),('door',mid)
    cells=fallbacks=legacy=door_cells=0;details={}
    with tempfile.TemporaryDirectory(prefix='frontier07a-c-') as tmp:
        native_doors=checks(Path(tmp)/'doors');native_animation=animation_checks(Path(tmp)/'animation')
        selectors.NAMES=NAMES;dll,_=selectors.selector(Path(tmp)/'selector')
        for n in NAMES:
            l=ls[maps[n]['layout']];before=bl[bm[n]['layout']];g=words(ROOT/l['blockdata_filepath'])
            assert maps[n]==bm[n] and g==words(base/before['blockdata_filepath'])
            assert words(ROOT/l['border_filepath'])==words(base/before['border_filepath'])
            idx=node['layouts'].index(l);changed=0
            for i,v in enumerate(g):
                assert dll.probe(idx,i%l['width']+7,i//l['width']+7,v&1023)==v&1023;cells+=1
                changed+=r.metatile(v&1023).tobytes()!=br.metatile(v&1023).tobytes()
            assert changed>0,n
            for x,y in ((7,7),(6,7),(7,6),(l['width']+7,7),(7,l['height']+7)):
                for mid in range(1024):assert dll.probe(idx,x,y,mid)==mid;fallbacks+=1
            door_cells+=len(contract['doors'][n]);details[n]={'cells':len(g),'changed_visual_cells':changed,'objects':len(maps[n]['object_events']),'warps':len(maps[n]['warp_events']),'layout':l['id']}
        header=(ROOT/'src/data/arauna_cave_visuals_v2.h').read_text()
        for idx,n in re.findall(r'\{(\d+), sVisual_(\w+)\}',header):
            l=node['layouts'][int(idx)];g=words(ROOT/l['blockdata_filepath']);path=re.search(r'sVisual_'+n+r'\[\] = INCBIN_U16\("([^"]+)"\)',header)[1];expected=words(base/path)
            for i,v in enumerate(g):assert dll.probe(int(idx),i%l['width']+7,i//l['width']+7,v&1023)==expected[i];legacy+=1
    report={'status':'PASS','base_commit':BASE,'maps':details,'native_cells':cells,'protected_files':len(contract['protected_hashes']),'explicit_engine_protection':contract['explicit_engine_protection'],'layout_count':754,'appended_layouts':0,'native_attributes':attrs,'secondary_layer_masks':masks,'animated_color_masks':animated_masks,'previous_tower_maps':7,'door_footprint_cells':door_cells,'animated_palette':8,'animated_indices':[13,15],'native_animation':native_animation,'production_c_selector_cells':cells,'production_c_selector_fallbacks':fallbacks,'previous_cavern_dive_selector_cells':legacy,'native_doors':native_doors,'scope':'Production visual selectors and door functions execute on host. Scripts, battle logic, trainers, saves and Dome tournament code are byte-preserved; script/battle interpreter and link sessions are not executed. All door footprint pixels and source animation palettes remain exact.','rom_build':'pending: ARM compiler unavailable','emulator':'pending: mGBA unavailable'}
    dump(OUT/'validation.json',report);print(json.dumps(report,indent=2))

if __name__=='__main__':main()
