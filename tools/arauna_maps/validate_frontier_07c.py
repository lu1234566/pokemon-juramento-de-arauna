#!/usr/bin/env python3
"""Six native map invariants, water frames and reconciled engine protection."""
import argparse,hashlib,json,re,tempfile
from pathlib import Path
from native_visuals_v2 import dump,callback
from frontier_07c_common import BASE,ROOT,OUT,NAMES,GROUPS,inventory,renderer,render,protected_ids,require_base,door_records
from trainer_hill_06a_art import native_layers
from render_native_map import words,indexed_tiles
import safari_05_c_checks as selectors
from frontier_07c_c_checks import checks as door_checks
from frontier_07c_animation_checks import checks as animation_checks
from frontier_07b_animation_checks import animation_checks as dome_animation_checks

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    contract=json.loads((OUT/'functional_contract.json').read_text());build=json.loads((OUT/'build.json').read_text())
    for rel,h in contract['protected_hashes'].items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,('frozen',rel)
    old,bl,bm=inventory(base);node,ls,maps=inventory(ROOT);assert len(node['layouts'])==len(old['layouts'])==754
    targets={bm[n]['layout'] for n in NAMES}
    for a,b in zip(old['layouts'],node['layouts']):
        fields={'primary_tileset','secondary_tileset'} if a['id'] in targets else set();assert {k:v for k,v in a.items() if k not in fields}=={k:v for k,v in b.items() if k not in fields},a['id']
    for k in ('graphics.h','metatiles.h','headers.h'):
        raw=(ROOT/'src/data/tilesets'/k).read_text();stripped=re.sub(r'\n*// FRONTIER_07C_BEGIN\n.*?// FRONTIER_07C_END\n','\n',raw,flags=re.S);assert stripped.rstrip()==(base/'src/data/tilesets'/k).read_text().rstrip(),k
    attrs=masks=animated=0;readers={}
    for group,names in GROUPS.items():
        entry=build['banks'][group];l=ls[maps[names[0]]['layout']];r=renderer(ROOT,l);br=renderer(base,bl[bm[names[0]]['layout']]);readers[group]=(r,br)
        for kind,rel in enumerate(entry['paths']):
            p=ROOT/rel;source=base/entry['source_paths'][kind];assert (p/'metatile_attributes.bin').read_bytes()==(source/'metatile_attributes.bin').read_bytes();attrs+=len(words(p/'metatile_attributes.bin'))
            im,row,count=indexed_tiles(p/'tiles.png');assert count<=512 and max(im.getdata())<=15
            assert callback(ROOT,l[('primary_tileset','secondary_tileset')[kind]])==entry['callbacks'][kind]
            for e in words(p/'metatiles.bin'):assert e>>12<=12 and r._tile(e&1023) is not None
        for q in range(12):assert r.palettes[q]==br.palettes[q],('palette',group,q)
        assert not set(entry['allocated_tiles'])&(set(range(432,512))|set(range(992,1024)))
        for mids in (range(len(r.primary_metatiles)//8),range(512,512+len(r.secondary_metatiles)//8)):
            for mid in mids:
                for a,b in zip(native_layers(br,mid),native_layers(r,mid)):assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes(),('mask',group,mid);masks+=1
                if mid not in entry['redrawn_ids']:assert r.metatile(mid).tobytes()==br.metatile(mid).tobytes(),('untouched',group,mid)
        for mid in protected_ids(base,names):assert r.metatile(mid).tobytes()==br.metatile(mid).tobytes(),('door',group,mid)
        for frame in range(8):
            ar=renderer(ROOT,l,frame);abr=renderer(base,bl[bm[names[0]]['layout']],frame)
            for mid in entry['preserved_animated_primary_ids']:assert ar.metatile(mid).tobytes()==abr.metatile(mid).tobytes(),('animated',frame,mid);animated+=1
    from frontier_07a_common import NAMES as TOWER
    from frontier_07b_common import NAMES as DOME,render as dome_render
    for n in TOWER+DOME:
        draw=dome_render if n in DOME else render
        assert draw(ROOT,ls[maps[n]['layout']],0).tobytes()==draw(base,bl[bm[n]['layout']],0).tobytes(),('previous Frontier',n)
    assert door_records(ROOT)==contract['doors']==door_records(base)
    cells=fallbacks=legacy=door_cells=0;details={}
    with tempfile.TemporaryDirectory(prefix='arauna07c-c-',dir='/tmp') as tmp:
        native_doors=door_checks(Path(tmp)/'doors');native_animation=animation_checks(Path(tmp)/'animation');dome_animation=dome_animation_checks(Path(tmp)/'dome')
        selectors.NAMES=NAMES;dll,_=selectors.selector(Path(tmp)/'selector')
        for n in NAMES:
            l=ls[maps[n]['layout']];before=bl[bm[n]['layout']];g=words(ROOT/l['blockdata_filepath']);r,br=readers[build['maps'][n]['group']]
            assert maps[n]==bm[n] and g==words(base/before['blockdata_filepath']) and words(ROOT/l['border_filepath'])==words(base/before['border_filepath']);idx=node['layouts'].index(l);changed=0
            for i,v in enumerate(g):assert dll.probe(idx,i%l['width']+7,i//l['width']+7,v&1023)==v&1023;cells+=1;changed+=r.metatile(v&1023).tobytes()!=br.metatile(v&1023).tobytes()
            assert changed>0,n
            for x,y in ((7,7),(6,7),(7,6),(l['width']+7,7),(7,l['height']+7)):
                for mid in range(1024):assert dll.probe(idx,x,y,mid)==mid;fallbacks+=1
            door_cells+=len(contract['doors'][n]);details[n]={'cells':len(g),'changed_visual_cells':changed,'objects':len(maps[n]['object_events']),'warps':len(maps[n]['warp_events']),'layout':l['id']}
        header=(ROOT/'src/data/arauna_cave_visuals_v2.h').read_text()
        for idx,n in re.findall(r'\{(\d+), sVisual_(\w+)\}',header):
            l=node['layouts'][int(idx)];g=words(ROOT/l['blockdata_filepath']);path=re.search(r'sVisual_'+n+r'\[\] = INCBIN_U16\("([^"]+)"\)',header)[1];expected=words(base/path)
            for i,v in enumerate(g):assert dll.probe(int(idx),i%l['width']+7,i//l['width']+7,v&1023)==expected[i];legacy+=1
    report={'status':'PASS','base_commit':BASE,'maps':details,'native_cells':cells,'protected_files':len(contract['protected_hashes']),'explicit_engine_protection':contract['explicit_engine_protection'],'layout_count':754,'appended_layouts':0,'native_attributes':attrs,'layer_masks':masks,'animated_metatile_frame_cases':animated,'previous_frontier_maps':11,'door_footprint_cells':door_cells,'production_c_selector_cells':cells,'production_c_selector_fallbacks':fallbacks,'previous_cavern_dive_selector_cells':legacy,'native_doors':native_doors,'native_garden_animation':native_animation,'previous_dome_animation':dome_animation,'scope':'Production C doors, selectors, General animation queue and previous Dome fade execute on host. Palace autonomy, Arena judging, scripts, saves and progression are byte-preserved; battle/script interpreter and ROM are not executed. Official GitHub 9f integration, including 07B and the 52e Tower door repair, is the frozen baseline.','rom_build':'pending: ARM compiler unavailable','emulator':'pending: mGBA unavailable'}
    dump(OUT/'validation.json',report);print(json.dumps(report,indent=2))

if __name__=='__main__':main()
