#!/usr/bin/env python3
"""Five native services and all 39 prior Frontier maps."""
import argparse,hashlib,json,re,tempfile
from pathlib import Path
from native_visuals_v2 import dump,callback
from frontier_07h_common import BASE,ROOT,OUT,NAMES,ROLES,inventory,renderer,render,render_grid,require_base
from trainer_hill_06a_art import native_layers
from render_native_map import words,indexed_tiles
import safari_05_c_checks as selectors
from frontier_07c_c_checks import checks as door_checks
from frontier_07d_animation_checks import checks as building_checks
from frontier_07c_animation_checks import checks as general_checks
from frontier_07b_animation_checks import animation_checks as dome_checks
from frontier_07e_c_checks import checks as curtain_checks
from frontier_07f_c_checks import checks as generator_checks,animation_checks as pyramid_checks

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    contract=json.loads((OUT/'functional_contract.json').read_text());build=json.loads((OUT/'build.json').read_text())
    assert contract['base_commit']==build['base_commit']==BASE
    for rel,h in contract['protected_hashes'].items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,('frozen',rel)
    old,bl,bm=inventory(base);node,ls,maps=inventory(ROOT);assert len(node['layouts'])==len(old['layouts'])==754
    targets={bm[n]['layout'] for n in NAMES};assert len(targets)==5
    for a,b in zip(old['layouts'],node['layouts']):
        fields={'primary_tileset','secondary_tileset'} if a['id'] in targets else set()
        assert {k:v for k,v in a.items() if k not in fields}=={k:v for k,v in b.items() if k not in fields},a['id']
    # No other map may silently inherit a new private pair.
    assert {n for n,m in maps.items() if m['layout'] in targets}==set(NAMES)
    for k in ('graphics.h','metatiles.h','headers.h'):
        raw=(ROOT/'src/data/tilesets'/k).read_text();stripped=re.sub(r'\n*// FRONTIER_07H_BEGIN\n.*?// FRONTIER_07H_END\n','\n',raw,flags=re.S)
        assert stripped.rstrip()==(base/'src/data/tilesets'/k).read_text().rstrip(),k
    attrs=masks=frame_masks=0
    for entry in build['banks']:
        layout=ls[entry['layout']];original=bl[entry['layout']];r=renderer(ROOT,layout);br=renderer(base,original)
        assert entry['maps']==[n for n in NAMES if bm[n]['layout'] in entry['layouts']]
        assert entry['callbacks']==['InitTilesetAnim_Building','NULL']
        for kind,rel in enumerate(entry['paths']):
            p=ROOT/rel;source=base/entry['source_paths'][kind]
            assert (p/'metatile_attributes.bin').read_bytes()==(source/'metatile_attributes.bin').read_bytes();attrs+=len(words(p/'metatile_attributes.bin'))
            im,row,count=indexed_tiles(p/'tiles.png');assert count<=512 and max(im.getdata())<=15
            assert callback(ROOT,layout[('primary_tileset','secondary_tileset')[kind]])==entry['callbacks'][kind]
            for e in words(p/'metatiles.bin'):assert e>>12<=12 and r._tile(e&1023) is not None
        for q in range(12):assert r.palettes[q]==br.palettes[q],('palette',entry['kind'],q)
        assert r.primary_metatiles==br.primary_metatiles
        assert not set(entry['allocated_tiles'])&(set(range(432,512))|set(range(992,1024)))
        for mid in list(range(len(r.primary_metatiles)//8))+list(range(512,512+len(r.secondary_metatiles)//8)):
            for a,b in zip(native_layers(br,mid),native_layers(r,mid)):
                assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes(),('mask',entry['kind'],mid);masks+=1
            if mid not in entry['redrawn_ids']:assert r.metatile(mid).tobytes()==br.metatile(mid).tobytes(),('untouched',entry['kind'],mid)
        for frame in range(3):
            ar=renderer(ROOT,layout,frame);abr=renderer(base,original,frame)
            for mid in entry['redrawn_ids']:
                for a,b in zip(native_layers(abr,mid),native_layers(ar,mid)):
                    assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes(),('frame mask',entry['kind'],frame,mid);frame_masks+=1
            for i in range(496,500):assert ar._tile(i).tobytes()==abr._tile(i).tobytes(),('Building TV VRAM',entry['kind'],frame,i)
            assert ar.metatile(2).tobytes()==abr.metatile(2).tobytes()
    from frontier_07a_common import NAMES as TOWER
    from frontier_07b_common import NAMES as DOME,render as dome_render
    from frontier_07c_common import NAMES as PALACE_ARENA
    from frontier_07d_common import NAMES as FACTORY
    from frontier_07e_common import NAMES as PIKE
    from frontier_07f_common import NAMES as PYRAMID
    from frontier_07g_common import NAMES as LOUNGES
    previous=TOWER+DOME+PALACE_ARENA+FACTORY+PIKE+PYRAMID+LOUNGES;assert len(previous)==39
    for n in previous:
        draw=dome_render if n in DOME else render
        for frame in (0,7):assert draw(ROOT,ls[maps[n]['layout']],frame).tobytes()==draw(base,bl[bm[n]['layout']],frame).tobytes(),('previous Frontier',n,frame)
    palace='BattleFrontier_BattlePalaceBattleRoom'
    for frame in range(8):
        rr=renderer(ROOT,ls[maps[palace]['layout']],frame);assert rr.metatile(0x226).tobytes()==rr.metatile(0x190).tobytes()
    cells=fallbacks=legacy=objects=warps=0;details={}
    with tempfile.TemporaryDirectory(prefix='arauna07h-c-',dir='/tmp') as tmp:
        native_doors=door_checks(Path(tmp)/'doors');native_building=building_checks(Path(tmp)/'building');native_general=general_checks(Path(tmp)/'general');native_dome=dome_checks(Path(tmp)/'dome');native_curtain=curtain_checks(Path(tmp)/'curtain')
        native_generator=generator_checks(base,Path(tmp)/'generator');native_pyramid=pyramid_checks(Path(tmp)/'pyramid')
        runtime_cases=0
        for g in native_generator['snapshots']:
            for frame in (0,7):
                assert render_grid(ROOT,ls[maps[PYRAMID[1]]['layout']],g['grid'],32,32,frame,g['floor']).tobytes()==render_grid(base,bl[bm[PYRAMID[1]]['layout']],g['grid'],32,32,frame,g['floor']).tobytes()
                runtime_cases+=1
        selectors.NAMES=NAMES;dll,_=selectors.selector(Path(tmp)/'selector')
        for n,role in zip(NAMES,ROLES):
            l=ls[maps[n]['layout']];before=bl[bm[n]['layout']];g=words(ROOT/l['blockdata_filepath']);idx=node['layouts'].index(l);changed=0;r=renderer(ROOT,l);br=renderer(base,before)
            assert maps[n]==bm[n] and g==words(base/before['blockdata_filepath']) and words(ROOT/l['border_filepath'])==words(base/before['border_filepath'])
            for i,v in enumerate(g):
                assert dll.probe(idx,i%l['width']+7,i//l['width']+7,v&1023)==v&1023;cells+=1
                changed+=r.metatile(v&1023).tobytes()!=br.metatile(v&1023).tobytes()
            assert changed>0,n
            for x,y in ((7,7),(6,7),(7,6),(l['width']+7,7),(7,l['height']+7)):
                for mid in range(1024):assert dll.probe(idx,x,y,mid)==mid;fallbacks+=1
            for event in maps[n]['warp_events']:
                assert 0<=event['x']<l['width'] and 0<=event['y']<l['height']
                assert event in bm[n]['warp_events']
            scripts=(ROOT/'data/maps'/n/'scripts.inc').read_bytes();assert scripts==(base/'data/maps'/n/'scripts.inc').read_bytes()
            objects+=len(maps[n]['object_events']);warps+=len(maps[n]['warp_events'])
            details[n]={'role':role,'cells':len(g),'changed_visual_cells':changed,'objects':len(maps[n]['object_events']),'warps':len(maps[n]['warp_events']),'layout':l['id'],'scripts_sha256':hashlib.sha256(scripts).hexdigest()}
        header=(ROOT/'src/data/arauna_cave_visuals_v2.h').read_text()
        for idx,n in re.findall(r'\{(\d+), sVisual_(\w+)\}',header):
            l=node['layouts'][int(idx)];g=words(ROOT/l['blockdata_filepath']);path=re.search(r'sVisual_'+n+r'\[\] = INCBIN_U16\("([^"]+)"\)',header)[1];expected=words(base/path)
            for i,v in enumerate(g):assert dll.probe(int(idx),i%l['width']+7,i//l['width']+7,v&1023)==expected[i];legacy+=1
    assert objects==25 and warps==13 and cells==1314
    report={'status':'PASS','base_commit':BASE,'maps':details,'native_cells':cells,'unique_layouts':5,'unique_cells':1314,'object_events':objects,'warp_events':warps,'protected_files':len(contract['protected_hashes']),'explicit_engine_protection':contract['explicit_engine_protection'],'layout_count':754,'changed_layout_bank_references':5,'appended_layouts':0,'native_attributes':attrs,'layer_masks':masks,'animated_layer_masks':frame_masks,'previous_frontier_maps':39,'previous_frontier_frame_cases':78,'previous_pyramid_runtime_floor_frame_cases':runtime_cases,'palace_corrected_water_edge_frames':8,'production_c_selector_cells':cells,'production_c_selector_fallbacks':fallbacks,'previous_cavern_dive_selector_cells':legacy,'native_doors':native_doors,'native_building_animation':native_building,'previous_garden_animation':native_general,'previous_dome_animation':native_dome,'previous_pike_curtain':native_curtain,'pyramid_generator':{k:v for k,v in native_generator.items() if k!='snapshots'},'pyramid_animation':native_pyramid,'scope':'Native renders and selected original C execute on host with explicit fixtures; all service scripts and engine logic remain byte-preserved. No GBA ROM or emulator execution.','rom_build':'pending: ARM compiler unavailable','emulator':'pending: mGBA unavailable'}
    dump(OUT/'validation.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ('maps','explicit_engine_protection')},indent=2))

if __name__=='__main__':main()
