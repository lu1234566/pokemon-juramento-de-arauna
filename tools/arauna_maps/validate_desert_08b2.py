#!/usr/bin/env python3
"""Verify the corrected base, native art footprints, water and item access."""
import json
import re
import subprocess
from desert_08b2 import BASE, PARTY_HASH, NAMES, OUT, ROOT, MUTABLE, TAG, inventory, sha
from native_visuals_v2 import Pair, dump
from trainer_hill_06a_art import native_layers
from render_native_map import words, indexed_tiles
from cavernas_03a_common import renderer


def flood(grid, width, height, pair, start, surf):
    seen={start};todo=[start]
    while todo:
        x,y=todo.pop()
        for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if not 0<=nx<width or not 0<=ny<height or (nx,ny) in seen:continue
            v=grid[ny*width+nx];mid=v&1023
            behavior=pair.attrs[mid>=512][mid%512]&255
            if v&0xc00 or (not surf and behavior in (0x10,0x11,0x12,0x13,0x14,0x15,0x17,0x19)):continue
            seen.add((nx,ny));todo.append((nx,ny))
    return seen


def main():
    c=json.loads((OUT/'functional_contract.json').read_text())
    assert c['base_commit']==BASE
    assert c['protected_hashes']['src/party_menu.c']==PARTY_HASH==sha((ROOT/'src/party_menu.c').read_bytes()), 'party_menu.c must retain the corrected 08B1 hash: '+PARTY_HASH
    for rel,h in c['protected_hashes'].items():
        assert (ROOT/rel).is_file() and sha((ROOT/rel).read_bytes())==h,('protected file',rel)
    node,ls,ms=inventory()
    original=json.loads(subprocess.check_output(['git','show',BASE+':data/layouts/layouts.json'],cwd=ROOT))
    restored=json.loads(json.dumps(node))
    for l in restored['layouts']:
        if l['id'] in {ms[n]['layout'] for n in NAMES}:
            old=next(c['maps'][n]['layout'] for n in NAMES if ms[n]['layout']==l['id'])
            l['primary_tileset'],l['secondary_tileset']=old['primary_tileset'],old['secondary_tileset']
    assert restored==original
    assert [l['id'] for l in node['layouts']]==c['layout_ids']
    for rel in MUTABLE-{'data/layouts/layouts.json'}:
        text=(ROOT/rel).read_text()
        stripped=re.sub(r'\n*// '+TAG+r'_BEGIN\n.*?// '+TAG+r'_END\n','\n',text,flags=re.S)
        expected=subprocess.check_output(['git','show',BASE+':'+rel],cwd=ROOT,text=True)
        assert stripped.rstrip()==expected.rstrip(),('registry',rel)
        assert text.count('// '+TAG+'_BEGIN')==1
    historical=json.loads((ROOT/'review/desert_08b1/functional_contract.json').read_text())
    assert historical['protected_hashes']['src/party_menu.c']!=PARTY_HASH
    for rel,h in historical['protected_hashes'].items():
        if rel!='src/party_menu.c':assert sha((ROOT/rel).read_bytes())==h,('08B1 historical dependency',rel)
    build=json.loads((OUT/'build.json').read_text());reports={}
    for name in NAMES:
        before=c['maps'][name]['layout'];after=ls[ms[name]['layout']]
        old,new=Pair(ROOT,before),Pair(ROOT,after);art=build['maps'][name]
        assert old.attrs==new.attrs
        assert old.callbacks==new.callbacks
        assert old.pals[:12]==new.pals[:12]
        assert not set(art['new_graphics_slots']) & (old.dynamic|set(range(928,932)))
        for t in old.dynamic|set(range(928,932)):
            a,b=old.reader._tile(t),new.reader._tile(t)
            if a is not None:assert b is not None and a.tobytes()==b.tobytes(),('DMA source',name,t)
        for path in new.paths:
            im,_,count=indexed_tiles(path/'tiles.png');assert count<=512 and max(im.getdata())<=15
            entries,attrs=words(path/'metatiles.bin'),words(path/'metatile_attributes.bin')
            assert len(entries)==8*len(attrs) and len(attrs)<=512
            for e in entries:assert e>>12<=12 and (new.reader._tile(e&1023) is not None or e&1023 in old.dynamic|set(range(928,932)))
        assert all(v%8==0 for rgb in new.pals[12] for v in rgb)
        masks=unchanged=waterpixels=dynamicwords=0
        for mid in art['active_ids']:
            for a,b in zip(native_layers(old.reader,mid),native_layers(new.reader,mid)):
                assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes(),('native layer footprint',name,hex(mid));masks+=1
            ae=old.meta[mid>=512][mid%512*8:mid%512*8+8];be=new.meta[mid>=512][mid%512*8:mid%512*8+8]
            for a,b in zip(ae,be):
                if a&1023 in old.dynamic|set(range(928,932)):assert a==b;dynamicwords+=1
            assert new.reader.metatile(mid).getextrema()[3]==(255,255),('opaque map',name,mid)
        for kind,attrs in enumerate(old.attrs):
            for local in range(len(attrs)):
                mid=local+kind*512
                if mid not in art['redrawn_ids']:
                    assert old.reader.metatile(mid).tobytes()==new.reader.metatile(mid).tobytes(),('unredrawn ID',name,hex(mid));unchanged+=1
        if name=='ScorchedSlab':
            for frame in range(8):
                a,b=renderer(ROOT,before,frame),renderer(ROOT,after,frame)
                for mid in art['active_ids']:
                    original_pixels=a.metatile(mid);new_pixels=b.metatile(mid)
                    for y in range(16):
                        for x in range(16):
                            r,g,blue,alpha=original_pixels.getpixel((x,y))
                            if alpha and blue>r*1.3 and blue>g*1.1:
                                assert new_pixels.getpixel((x,y))==(r,g,blue,alpha),('water frame',frame,hex(mid),x,y);waterpixels+=1
        grid=words(ROOT/before['blockdata_filepath']);w,h=before['width'],before['height']
        warp=ms[name]['warp_events'][0];start=(warp['x'],warp['y'])
        reachable={}
        for surf in (False,True):
            old_seen=flood(grid,w,h,old,start,surf);new_seen=flood(grid,w,h,new,start,surf)
            assert old_seen==new_seen
            reachable['surf' if surf else 'walk']=len(new_seen)
            if surf or name=='DesertUnderpass':
                for e in ms[name]['object_events']:
                    assert any((e['x']+dx,e['y']+dy) in new_seen for dx,dy in ((0,-1),(0,1),(-1,0),(1,0))),('item not reachable',name,e)
        reports[name]={'cells':len(grid),'redrawn_ids':len(art['redrawn_ids']),
            'native_layer_masks_checked':masks,'unchanged_pixel_identical_metatiles':unchanged,
            'preserved_dynamic_tile_words':dynamicwords,'water_pixels_compared_over_8_frames':waterpixels,
            'reachable_cells_ignoring_elevation':reachable,'events_warps_elevations_and_scripts':'byte-identical'}
    report={'status':'PASS','base_commit':BASE,'protected_existing_files':len(c['protected_hashes']),
        'corrected_party_menu_sha256':PARTY_HASH,'historical_08B1_contract':'unchanged; documented old party-menu hash remains historical',
        'layouts_preserved':len(c['layout_ids']),'maps':reports,
        'source_item_logic':'fossil choices, common finditem, flags and TM scripts protected byte-for-byte',
        'rom_build':'pending; ARM toolchain unavailable','mgba_and_save':'pending; emulator unavailable',
        'navigation_test_scope':'native collision/behavior flood without elevation or event actors; not a gameplay run'}
    dump(OUT/'validation.json',report);print(json.dumps(report,indent=2))


if __name__=='__main__':main()
