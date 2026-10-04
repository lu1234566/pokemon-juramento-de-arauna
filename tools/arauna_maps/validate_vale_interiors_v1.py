#!/usr/bin/env python3
"""Validate six rustic rooms and their retained services/event graph."""
import collections,json,re,subprocess
from PIL import Image
from build_vale_interiors_v1 import ROOT,BANK,NAMES,SYMBOL,MARK,words,layout_id,TENT_BANK,TENT_SYMBOL

def reachable(grid,w,h,start,objects):
    blocked={(i%w,i//w) for i,v in enumerate(grid) if v&0x400}|objects
    assert start not in blocked,('blocked entry',start)
    seen={start};queue=collections.deque([start])
    while queue:
        x,y=queue.popleft()
        for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=p[0]<w and 0<=p[1]<h and p not in blocked and p not in seen:
                seen.add(p);queue.append(p)
    return seen

def main():
    layouts={r['id']:r for r in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
    attr=words(BANK/'metatile_attributes.bin');meta=words(BANK/'metatiles.bin')
    original=words(ROOT/'data/tilesets/secondary/pokemon_center/metatile_attributes.bin')
    assert len(meta)==len(attr)*8 and len(attr)<=512
    sheet=Image.open(BANK/'tiles.png');assert sheet.size==(128,256) and sheet.mode=='P'
    used={v&1023 for v in meta};used.discard(0)
    assert all(512<=v<992 for v in used)
    for mid in (0x280,0x281,0x288,0x289,0x290,0x291,0x298,0x299,0x2a0,0x2a1,0x2a8,0x2a9):
        assert attr[mid-512]==original[mid-512]
    assert attr[0x264-512]&255==0x69
    tent_attr=words(TENT_BANK/'metatile_attributes.bin')
    original_tent=ROOT/'data/tilesets/secondary/battle_tent'
    original_tent_attr=words(original_tent/'metatile_attributes.bin')
    original_tent_meta=words(original_tent/'metatiles.bin')
    assert words(TENT_BANK/'metatiles.bin')[:len(original_tent_meta)]==original_tent_meta
    assert tent_attr[:len(original_tent_attr)]==original_tent_attr
    assert Image.open(TENT_BANK/'tiles.png').crop((0,0,128,128)).tobytes()==Image.open(original_tent/'tiles.png').tobytes()
    assert (TENT_BANK/'palettes/09.pal').read_bytes()==(original_tent/'palettes/09.pal').read_bytes()
    report={};warps=objects_count=0
    for name in NAMES:
        rel='data/maps/'+name+'/map.json'
        baseline=json.loads(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT))
        event=json.loads((ROOT/rel).read_text())
        assert event['layout']==layout_id(name)
        for key in baseline:
            if key not in ('layout','object_events','warp_events'):assert event[key]==baseline[key]
        for key in ('object_events','warp_events'):
            assert len(event[key])==len(baseline[key])
            for a,b in zip(event[key],baseline[key]):
                assert {k:v for k,v in a.items() if k not in ('x','y','elevation')}=={k:v for k,v in b.items() if k not in ('x','y','elevation')}
        script='data/maps/'+name+'/scripts.inc'
        current=(ROOT/script).read_text()
        original_script=subprocess.check_output(['git','show','HEAD:'+script],cwd=ROOT).decode()
        # Existing English text revisions are independent from this map package.
        mask=lambda s:re.sub(r'^\s*\.string[^\n]*\n','',s,flags=re.M)
        assert mask(current)==mask(original_script)
        l=layouts[event['layout']];old=layouts[baseline['layout']];w,h=l['width'],l['height']
        if 'BattleTent' in name:
            assert event=={**baseline,'layout':layout_id(name)}
            assert l['secondary_tileset']=='gTileset_'+TENT_SYMBOL and l['primary_tileset']==old['primary_tileset']
            assert (w,h)==(old['width'],old['height'])
            a=words(ROOT/old['blockdata_filepath']);b=words(ROOT/l['blockdata_filepath'])
            assert len(a)==len(b)==w*h
            primary=words(ROOT/'data/tilesets/primary/general/metatile_attributes.bin')
            for before,after in zip(a,b):
                assert (before^after)&~1023==0
                v,t=before&1023,after&1023
                expected=original_tent_attr[v-512] if v>=512 else primary[v]
                actual=tent_attr[t-512] if t>=512 else primary[t]
                assert expected==actual
                if v in (610,611,612,618,619,620):assert v==t
            if name.endswith('Lobby'):
                paths=[[(6,y) for y in range(5,0,-1)],[(6,y) for y in range(6,0,-1)]]
            elif name.endswith('Corridor'):
                paths=[[(2,y) for y in range(6,0,-1)],[(2,y) for y in range(7,0,-1)]]
            else:paths=[[(2,y) for y in range(8,4,-1)],[(11,y) for y in range(1,6)],[(3,4),(3,5)]]
            assert all(not b[y*w+x]&0x400 for path in paths for x,y in path)
            assert (ROOT/l['border_filepath']).read_bytes()==(ROOT/old['border_filepath']).read_bytes()
            warps+=len(event['warp_events']);objects_count+=len(event['object_events'])
            report[name]={'size':[w,h],'scripted_paths':len(paths),'warps':len(event['warp_events']),'objects':len(event['object_events'])}
            continue
        assert l['primary_tileset']==old['primary_tileset'] and l['secondary_tileset']=='gTileset_'+SYMBOL
        assert (ROOT/l['border_filepath']).read_bytes()==(ROOT/old['border_filepath']).read_bytes()
        grid=words(ROOT/l['blockdata_filepath']);assert len(grid)==w*h
        assert all(512<=v&1023<512+len(attr) for v in grid)
        npcs={(e['x'],e['y']) for e in event['object_events']}
        assert len(npcs)==len(event['object_events'])
        assert all(not grid[y*w+x]&0x400 for x,y in npcs),(name,'NPC inside furniture')
        entry=event['warp_events'][0];start=(entry['x'],entry['y']-1)
        seen=reachable(grid,w,h,start,npcs)
        for e in event['object_events']:
            x,y=e['x'],e['y'];near=False
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                p=(x+dx,y+dy)
                if p in seen:near=True
                elif 0<=p[0]<w and 0<=p[1]<h and attr[(grid[p[1]*w+p[0]]&1023)-512]&255==0x80:
                    near|=(x+2*dx,y+2*dy) in seen
            assert near,(name,'unreachable NPC',x,y)
            if e['movement_type']=='MOVEMENT_TYPE_WANDER_AROUND':
                rx,ry=e['movement_range_x'],e['movement_range_y']
                for px in range(x-rx,x+rx+1):
                    for py in range(y-ry,y+ry+1):
                        assert 0<=px<w and 0<=py<h and not grid[py*w+px]&0x400,(name,'wander area',px,py)
        for e in event['warp_events']:
            p=(e['x'],e['y'])
            if name.endswith('2F') and p in ((5,1),(9,1)):
                opened=list(grid)
                for y in (2,3):opened[y*w+p[0]]&=~0x400
                later=reachable(opened,w,h,start,npcs)
                assert p in later
            else:assert p in seen,(name,'unreachable warp',p)
        if name.endswith('Mart'):
            assert all(attr[(grid[4*w+x]&1023)-512]&255==0x80 for x in (2,3,4))
        if name.endswith('1F'):
            assert attr[(grid[5*w+11]&1023)-512]&255==0x83
            assert (10,5) in seen
        warps+=len(event['warp_events']);objects_count+=len(event['object_events'])
        report[name]={'size':[w,h],'reachable':len(seen),'warps':len(event['warp_events']),'objects':len(event['object_events'])}
    for filename in ('graphics.h','metatiles.h','headers.h'):
        text=(ROOT/'src/data/tilesets'/filename).read_text()
        assert text.count('// '+MARK+'_BEGIN')==text.count('// '+MARK+'_END')==1
    assert warps==16 and objects_count==31
    print(json.dumps({'status':'PASS','maps':report,'warps':warps,'objects':objects_count,
                      'script_commands_and_event_identity_preserved':True,'shop_counter_and_pc':True,
                      'stairs_and_link_doors':True},indent=2))

if __name__=='__main__':main()
