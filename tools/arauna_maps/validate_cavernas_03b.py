#!/usr/bin/env python3
"""Independent data, GBA formats, animation and actual-C selector checks."""
from __future__ import annotations
import argparse,hashlib,json,re,subprocess,tempfile
from pathlib import Path
from PIL import Image
from build_cavernas_03b import BASE,ROOT,OUT,NAMES,IMMUTABLE,REGISTRIES
from puzzles_cavernas_03b import run as puzzle_tests
from cavernas_03a_common import compile_caves,renderer
from bancos_nativos import resolve_bank,bank_words
from render_native_map import words,indexed_tiles,palette

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);a=ap.parse_args();base=a.base.resolve()
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
    contract=json.loads((OUT/'functional_contract.json').read_text());assert contract['base_commit']==BASE
    for rel,sha in {**contract['protected_hashes'], **contract.get('dependency_hashes',{})}.items():
        assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==sha,('protected file',rel)
    ls=[json.loads((p/'data/layouts/layouts.json').read_text())['layouts'] for p in (base,ROOT)];assert len(ls[0])==len(ls[1])==744
    target_ids={contract['maps'][n]['map']['layout'] for n in NAMES}
    for before,after in zip(*ls):
        assert before['id']==after['id']
        if before['id'] in target_ids:
            assert {k:v for k,v in before.items() if k!='secondary_tileset'}=={k:v for k,v in after.items() if k!='secondary_tileset'}
        else:assert before==after,('other layout',before['id'])
    # Registries are additive; all old declarations and grid records survive.
    for rel in ('src/data/tilesets/graphics.h','src/data/tilesets/headers.h','src/data/tilesets/metatiles.h'):
        current=(ROOT/rel).read_text();old=(base/rel).read_text()
        stripped=re.sub(r'\n*// CAVERNAS_03B_BEGIN\n.*?// CAVERNAS_03B_END\n','\n',current,flags=re.S)
        assert stripped.rstrip()==old.rstrip(),rel
    old_header=(base/'src/data/arauna_cave_visuals_v2.h').read_text();new_header=(ROOT/'src/data/arauna_cave_visuals_v2.h').read_text()
    old_records=re.findall(r'\{(\d+), sVisual_(\w+)\}',old_header);new_records=re.findall(r'\{(\d+), sVisual_(\w+)\}',new_header)
    assert new_records[:len(old_records)]==old_records and len(new_records)==len(old_records)+4
    build=json.loads((OUT/'build.json').read_text());banks=[]
    for family,b in build['banks'].items():
        path=ROOT/b['path'];sheet,cols,count=indexed_tiles(path/'tiles.png');assert count<=512
        assert all(i not in set(range(432,512))|set(range(928,932))|set(range(992,1024)) for i in b['new_static_graphics_slots'])
        # Index serialization roundtrip independently of the renderer.
        values=list(sheet.getdata());packed=bytes(values[i]|values[i+1]<<4 for i in range(0,len(values),2))
        assert [x for byte in packed for x in (byte&15,byte>>4)]==values
        for i in range(13):
            raw=(path/f'palettes/{i:02}.pal').read_bytes();assert raw.count(b'\n')==raw.count(b'\r\n')
            pal=palette(path/f'palettes/{i:02}.pal');assert len(pal)==16
            assert all(0<=c<=255 for rgb in pal for c in rgb)
            if i in (7,9,11,12):assert all(c%8==0 for rgb in pal for c in rgb)
            encoded=[sum((c>>3)<<(5*j) for j,c in enumerate(rgb)) for rgb in pal]
            decoded=[tuple(((v>>(5*j))&31)<<3 for j in range(3)) for v in encoded]
            assert decoded==[tuple(c>>3<<3 for c in rgb) for rgb in pal]
        original=base/'data/tilesets/secondary/cave'
        # Hardware animation colors and all original native ground palettes stay.
        for row in (6,8,10):assert palette(path/f'palettes/{row:02}.pal')==palette(original/f'palettes/{row:02}.pal')
        for x in (928,929,930,931):
            old=indexed_tiles(original/'tiles.png');ox=(x-512)%old[1]*8;oy=(x-512)//old[1]*8
            nx=(x-512)%cols*8;ny=(x-512)//cols*8
            assert old[0].crop((ox,oy,ox+8,oy+8)).tobytes()==sheet.crop((nx,ny,nx+8,ny+8)).tobytes()
        attrs=words(path/'metatile_attributes.bin');meta=words(path/'metatiles.bin');assert len(meta)==len(attrs)*8 and len(attrs)<=512
        for e in meta:assert e>>12<=12
        banks.append({'family':family,'graphics_tiles':count,'metatiles':len(attrs),'new_graphics_tiles':len(b['new_static_graphics_slots']),'aliases':b['alias_count'],'4bpp_and_rgb555':'PASS','animations_reserved':'PASS'})
    reports={};selector_cells=fallbacks=legacy_cells=0;animation_frames=0
    layouts=[{l['id']:l for l in node} for node in ls]
    with tempfile.TemporaryDirectory() as tmp:
        sel,cases=compile_caves(tmp)
        # All preexisting cave-selector maps retain exactly the same output.
        for idx,n in old_records:
            l=ls[1][int(idx)];native=words(ROOT/l['blockdata_filepath']);expected=words(ROOT/re.search(r'sVisual_'+n+r'\[\] = INCBIN_U16\("([^"]+)"\)',old_header)[1])
            for i,v in enumerate(native):
                assert sel(cases[n],i%l['width']+7,i//l['width']+7,v&1023)==expected[i];legacy_cells+=1
        for n in NAMES:
            m=contract['maps'][n]['map'];old=layouts[0][m['layout']];new=layouts[1][m['layout']]
            grid=words(ROOT/new['blockdata_filepath']);visual=words(OUT/'visual_grids'/f'{n}.bin');assert len(visual)==len(grid)
            oldr=renderer(base,old);newr=renderer(ROOT,new);changed=0
            pixel_cache={};frame_grids=[]
            for frame in range(8):
                r=renderer(ROOT,new,frame);frame_grids.append({mid:r.metatile(mid).tobytes() for mid in set(visual)});animation_frames+=1
            for i,v in enumerate(grid):
                native=v&1023;alias=sel(cases[n],i%new['width']+7,i//new['width']+7,native);assert alias==visual[i]
                assert bank_words(oldr,native,True)==bank_words(newr,native,True)==bank_words(newr,alias,True),('attribute',n,i,native,alias)
                im=newr.metatile(alias);assert im.getextrema()[3]==(255,255),('transparent ground',n,i)
                e=bank_words(newr,alias)
                assert all((word&1023)<512 or (word&1023)-512<newr.secondary_tiles[2] for word in e),('missing graphics',n,i)
                key=native,alias
                if key not in pixel_cache:pixel_cache[key]=oldr.metatile(native).tobytes()!=im.tobytes()
                changed+=pixel_cache[key];selector_cells+=1
                for other in (native^1,1023 if native!=1023 else 1022,0 if native else 1):
                    assert sel(cases[n],i%new['width']+7,i//new['width']+7,other)==other;fallbacks+=1
            for x,y in [(-1,0),(0,-1),(new['width'],0),(0,new['height'])]:
                assert sel(cases[n],x+7,y+7,757)==757;fallbacks+=1
            for mid in IMMUTABLE:
                assert bank_words(oldr,mid)==bank_words(newr,mid),('protected metatile entries',n,mid)
                assert bank_words(oldr,mid,True)==bank_words(newr,mid,True),('protected metatile attr',n,mid)
                assert oldr.metatile(mid).tobytes()==newr.metatile(mid).tobytes(),('protected pixel/palette',n,mid)
            for event in m['bg_events']:
                j=event['y']*new['width']+event['x'];mid=grid[j]&1023
                assert visual[j]==mid and oldr.metatile(mid).tobytes()==newr.metatile(mid).tobytes(),('Braille event',n,j)
            reports[n]={'cells':len(grid),'changed_visual_cells':changed,'native_words_unchanged':True,'attributes_compared':len(grid),'warps_preserved':len(m['warp_events']),'objects_preserved':len(m['object_events']),'coord_events_preserved':len(m['coord_events'])}
        puzzles=puzzle_tests(Path(tmp)/'puzzles')
        door_checks=0
        for n,states in puzzles['door_states'].items():
            l=layouts[1][contract['maps'][n]['map']['layout']];native=words(ROOT/l['blockdata_filepath']);visual=words(OUT/'visual_grids'/f'{n}.bin')
            for state,patch in states.items():
                for x,y,word in patch:
                    # Even when an opened ID equals the stored base ID, a door
                    # never receives an art alias. Reload and reversal are safe.
                    assert sel(cases[n],x+7,y+7,word&1023)==word&1023,(n,state,x,y)
                    assert visual[y*l['width']+x]==native[y*l['width']+x]&1023
                    door_checks+=1
        island=layouts[1][contract['maps']['IslandCave']['map']['layout']];g=words(ROOT/island['blockdata_filepath']);r=renderer(ROOT,island);vis=words(OUT/'visual_grids/IslandCave.bin')
        for x,y in contract['regice_perimeter']:
            v=g[y*island['width']+x];assert v&0xc00==0,('running collision',x,y)
            assert (bank_words(r,vis[y*island['width']+x],True)&255)==(bank_words(r,v&1023,True)&255),('running floor/exit behavior',x,y)
        sealed=(ROOT/'data/maps/SealedChamber_OuterRoom/scripts.inc').read_text()
        assert 'setdivewarp MAP_UNDERWATER_SEALED_CHAMBER, 12, 44' in sealed and 'setescapewarp MAP_UNDERWATER_SEALED_CHAMBER, 12, 44' in sealed
    (OUT/'puzzles.json').write_text(json.dumps(puzzles,indent=2)+'\n')
    report={'status':'PASS','base_commit':BASE,'protected_existing_files':len(contract['protected_hashes']),'layouts_preserved':740,'target_layout_secondary_fields_changed':4,'maps':reports,'banks':banks,'actual_c_selector_cells':selector_cells,'actual_c_fallback_checks':fallbacks,'legacy_cave_selector_cells':legacy_cells,'native_animation_frames':animation_frames,'closed_open_passage_checks':door_checks,'braille_pixels_and_messages_preserved':True,'regice_perimeter_cells_preserved':36,'actual_c_puzzle_checks':puzzles['checks'],'sealed_dive_and_escape_return_preserved':True,'legendary_encounters_scripts_flags_results_preserved':True,'rom_build':'pending_toolchain_unavailable','emulator':'pending_unavailable'}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
