#!/usr/bin/env python3
"""Check preserved services, animated slots and narrative staging in Porto."""
import json,re,subprocess
from PIL import Image
from build_porto_interiors_v1 import ROOT,OUT,SPECS,NAMES,MARK,source,target,layout_id,words

def walk(script,label,start):
    match=re.search(r'^'+re.escape(label)+r':\n(.*?\tstep_end)',script,re.M|re.S)
    assert match,label
    x,y=start;path=[start]
    shifts={'walk_up':(0,-1),'walk_down':(0,1),'walk_left':(-1,0),'walk_right':(1,0)}
    for line in match.group(1).splitlines():
        command=line.strip()
        if command in shifts:
            dx,dy=shifts[command];x+=dx;y+=dy;path.append((x,y))
    return path

def main():
    layouts={r['id']:r for r in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
    geometry=json.loads((OUT/'geometry.json').read_text());banks={}
    for symbol in SPECS:
        src,dst=source(symbol),target(symbol)
        old_meta,new_meta=words(src/'metatiles.bin'),words(dst/'metatiles.bin')
        old_attr,new_attr=words(src/'metatile_attributes.bin'),words(dst/'metatile_attributes.bin')
        assert old_attr==new_attr and len(new_meta)==len(old_meta)==len(new_attr)*8
        original_used={v&1023 for v in old_meta if v&1023>=512}
        allocated=geometry['banks'][symbol]['allocated_tiles']
        assert len(allocated)==len(set(allocated)) and not original_used.intersection(allocated)
        assert all(512<=v<992 for v in allocated)
        before,after=Image.open(src/'tiles.png'),Image.open(dst/'tiles.png')
        assert after.mode=='P' and after.size==(128,256)
        for tile in original_used:
            local=tile-512;x=local%16*8;y=local//16*8
            assert before.crop((x,y,x+8,y+8)).tobytes()==after.crop((x,y,x+8,y+8)).tobytes()
        changed=[512+i for i in range(len(new_attr)) if old_meta[i*8:(i+1)*8]!=new_meta[i*8:(i+1)*8]]
        assert changed==geometry['banks'][symbol]['changed_metatiles']
        for slot in range(6):assert (src/f'palettes/{slot:02}.pal').read_bytes()==(dst/f'palettes/{slot:02}.pal').read_bytes()
        assert {v>>12 for v in old_meta}.isdisjoint({12,13,14,15})
        for slot in range(16):assert len((dst/f'palettes/{slot:02}.pal').read_text().splitlines())==19
        banks[symbol]=new_attr
    report={};warps=objects=0
    for name in NAMES:
        rel='data/maps/'+name+'/map.json'
        baseline=json.loads(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT))
        event=json.loads((ROOT/rel).read_text())
        assert event=={**baseline,'layout':layout_id(name)}
        old,new=layouts[baseline['layout']],layouts[event['layout']]
        for key in ('width','height','primary_tileset'):assert old[key]==new[key]
        for key in ('blockdata_filepath','border_filepath'):
            assert (ROOT/old[key]).read_bytes()==(ROOT/new[key]).read_bytes()
        script='data/maps/'+name+'/scripts.inc'
        current=(ROOT/script).read_text();original_script=subprocess.check_output(['git','show','HEAD:'+script],cwd=ROOT).decode()
        mask=lambda s:re.sub(r'^\s*\.string[^\n]*\n','',s,flags=re.M)
        assert mask(current)==mask(original_script)
        attr=banks[new['secondary_tileset'].removeprefix('gTileset_')]
        grid=words(ROOT/new['blockdata_filepath']);assert len(grid)==new['width']*new['height']
        assert all(v&1023<512+len(attr) for v in grid)
        # Geometry and every behavior word match the baseline. This includes
        # collision, stairs, boarding tiles and script-set numeric metatile IDs;
        # all executable commands and movement definitions also match HEAD.
        movements=re.findall(r'^'+re.escape(name)+r'_Movement_[^\n]+::?$',current,re.M)
        warps+=len(event['warp_events']);objects+=len(event['object_events'])
        report[name]={'size':[new['width'],new['height']],'warps':len(event['warp_events']),
                      'objects':len(event['object_events']),'movement_definitions_preserved':len(movements)}
    center=banks['AraunaPortoCentro'];original=words(source('AraunaPortoCentro')/'metatile_attributes.bin')
    for mid in (0x21e,0x25d,0x264,0x2dc,0x2e4,*range(0x280,0x28e),*range(0x298,0x29a),*range(0x2a0,0x2ae)):
        assert center[mid-512]==original[mid-512]
    for filename in ('graphics.h','metatiles.h','headers.h'):
        text=(ROOT/'src/data/tilesets'/filename).read_text()
        assert text.count('// '+MARK+'_BEGIN')==text.count('// '+MARK+'_END')==1
    assert len(NAMES)==14 and warps==28 and objects==67
    print(json.dumps({'status':'PASS','maps':report,'warps':warps,'objects':objects,
                      'geometry_and_events_preserved':True,'all_metatile_attributes_preserved':True,
                      'animated_vram_slots_preserved':True,'movement_definitions_preserved':sum(v['movement_definitions_preserved'] for v in report.values())},indent=2))

if __name__=='__main__':main()
