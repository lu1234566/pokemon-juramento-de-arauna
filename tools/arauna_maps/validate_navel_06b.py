#!/usr/bin/env python3
"""Exact cumulative dependencies, attributes, selectors, warp graph and events."""
import argparse,hashlib,json,re,subprocess,tempfile
from collections import deque
from pathlib import Path
from navel_06b_common import BASE,ROOT,OUT,CORE,NAMES,GROUPS,COPIES,inventory,renderer
from native_visuals_v2 import dump,callback
from render_native_map import words,indexed_tiles,palette
from bancos_nativos import bank_words
from trainer_hill_06a_art import native_layers
from trainer_hill_06a_common import floors,runtime_words
from navel_06b_c_checks import checks as c_checks
from navel_06b_script_checks import checks as script_checks
import safari_05_c_checks as selector_source

def reachable(l,g,start):
    todo=deque([start]);seen=set()
    while todo:
        x,y=todo.popleft()
        if (x,y) in seen or not (0<=x<l['width'] and 0<=y<l['height']) or g[y*l['width']+x]&0xc00:continue
        seen.add((x,y));todo.extend(((x-1,y),(x+1,y),(x,y-1),(x,y+1)))
    return seen

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve()
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
    contract=json.loads((OUT/'functional_contract.json').read_text());build=json.loads((OUT/'build.json').read_text())
    for rel,h in {**contract['protected_hashes'],**contract['dependency_hashes']}.items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,('protected',rel)
    before,bl,bm=inventory(base);node,ls,maps=inventory(ROOT);assert len(before['layouts'])==745 and len(node['layouts'])==754
    targets={bm[n]['layout'] for n in CORE};assert len(targets)==8
    for old,new in zip(before['layouts'],node['layouts']):
        if old['id'] in targets:assert {k:v for k,v in old.items() if k not in ('primary_tileset','secondary_tileset')}=={k:v for k,v in new.items() if k not in ('primary_tileset','secondary_tileset')}
        else:assert old==new,old['id']
    assert {l['id'] for l in node['layouts'][745:]}==set(COPIES.values())
    for n in NAMES:
        old,new=bm[n],maps[n]
        assert {k:v for k,v in old.items() if k!='layout'}=={k:v for k,v in new.items() if k!='layout'},n
        assert new['layout']==COPIES.get(n,old['layout'])
        a,b=bl[old['layout']],ls[new['layout']]
        assert {k:v for k,v in a.items() if k not in ('id','name','primary_tileset','secondary_tileset')}=={k:v for k,v in b.items() if k not in ('id','name','primary_tileset','secondary_tileset')}
    for file in ('graphics.h','metatiles.h','headers.h'):
        s=(ROOT/'src/data/tilesets'/file).read_text();s=re.sub(r'\n*// NAVEL_ROCK_06B_BEGIN\n.*?// NAVEL_ROCK_06B_END\n','\n',s,flags=re.S)
        assert s.rstrip()==(base/'src/data/tilesets'/file).read_text().rstrip()
    # The game has no C dispatch keyed to a native Navel Rock layout ID.
    engine=''.join(p.read_text(errors='ignore') for p in (base/'src').glob('*.c'))
    assert not re.search(r'LAYOUT_(?:NAVEL_ROCK|ISLAND_HARBOR)\w*',engine)
    cache={}
    def rr(repo,l,frame=0):
        key=str(repo),l['primary_tileset'],l['secondary_tileset'],frame
        if key not in cache:cache[key]=renderer(repo,l,frame)
        return cache[key]
    cells=fallbacks=legacy=trainer_cells=plain_cells=rim_cells=layer_masks=attributes=warp_cells=sky_pixels=0;reports={};routes={};all_edges=[]
    with tempfile.TemporaryDirectory() as temp:
        folder=Path(temp);selector_source.NAMES=NAMES+tuple(n for n in bm if n.startswith('TrainerHill_'))
        selector,_=selector_source.selector(folder/'selector');behavior,c_report=c_checks(folder/'native')
        header=(ROOT/'src/data/arauna_cave_visuals_v2.h').read_text()
        for idx,n in re.findall(r'\{(\d+), sVisual_(\w+)\}',header):
            l=node['layouts'][int(idx)];g=words(ROOT/l['blockdata_filepath']);path=re.search(r'sVisual_'+n+r'\[\] = INCBIN_U16\("([^"]+)"\)',header)[1];visual=words(base/path)
            for i,v in enumerate(g):assert selector.probe(int(idx),i%l['width']+7,i//l['width']+7,v&1023)==visual[i];legacy+=1
        for f in floors(ROOT).values():
            l,g=runtime_words(ROOT,f);idx=node['layouts'].index(l)
            for i,v in enumerate(g):assert selector.probe(idx,i%16+7,i//16+7,v&1023)==v&1023;trainer_cells+=1
        by_id={m['id']:n for n,m in maps.items()}
        for n in NAMES:
            l=ls[maps[n]['layout']];old=bl[bm[n]['layout']];g=words(ROOT/l['blockdata_filepath']);assert g==words(base/old['blockdata_filepath'])
            r,br=rr(ROOT,l),rr(base,old);idx=node['layouts'].index(l);changed={}
            for mid in {v&1023 for v in g}|{v&1023 for v in words(ROOT/l['border_filepath'])}:
                assert bank_words(r,mid,True)==bank_words(br,mid,True),(n,hex(mid),'attribute')
                changed[mid]=r.metatile(mid).tobytes()!=br.metatile(mid).tobytes()
            theme=build['maps'][n]['theme'];plain=set(build['banks'][theme]['plain_floor_ids'])
            if n=='NavelRock_Top':
                sky_masks={}
                for mid in changed:
                    a=tuple(p[:3]==(112,184,240) for p in br.metatile(mid).getdata())
                    b=tuple(p[:3]==(112,184,240) for p in r.metatile(mid).getdata())
                    assert a==b,('native summit sky silhouette',hex(mid));sky_masks[mid]=sum(a)
                sky_pixels=sum(sky_masks[v&1023] for v in g)
            for i,v in enumerate(g):
                assert selector.probe(idx,i%l['width']+7,i//l['width']+7,v&1023)==v&1023;cells+=1
                if v&1023 in plain:assert not v&0xc00;plain_cells+=1
                if v&1023==0x247:assert v&0xc00;rim_cells+=1
            for x,y in ((7,7),(6,7),(7,6),(l['width']+7,7),(7,l['height']+7)):
                for mid in range(1024):assert selector.probe(idx,x,y,mid)==mid;fallbacks+=1
            warps=maps[n]['warp_events'];seen=reachable(l,g,(warps[0]['x'],warps[0]['y']))
            seen_before=reachable(old,words(base/old['blockdata_filepath']),(warps[0]['x'],warps[0]['y']));assert seen==seen_before
            for i,w in enumerate(warps):
                assert (w['x'],w['y']) in seen,(n,i,'unreachable warp')
                target=maps[by_id[w['dest_map']]];wi=int(w['dest_warp_id']);assert 0<=wi<len(target['warp_events'])
                other=target['warp_events'][wi];assert other['dest_map']==maps[n]['id'],(n,'nonreciprocal')
                all_edges.append({'map':n,'warp':i,'x':w['x'],'y':w['y'],'dest_map':target['name'],'dest_warp':wi})
                attr=bank_words(r,g[w['y']*l['width']+w['x']]&1023,True)&255
                assert [behavior.probe(j,attr) for j in range(3)]==[behavior.expected(j,attr) for j in range(3)];warp_cells+=1
            count=sum(changed[v&1023] for v in g);assert count>0,n
            reports[n]={'cells':len(g),'changed_visual_cells':count,'theme':theme,'warps':len(warps),'walkable_component_cells':len(seen),'layout':l['id']}
    # A directed warp graph proves both sanctuary branches and their returns.
    graph={n:set() for n in NAMES}
    for e in all_edges:graph[e['map']].add(e['dest_map'])
    def route(a,b):
        todo=deque([(a,[a])]);seen=set()
        while todo:
            n,path=todo.popleft()
            if n==b:return path
            if n in seen:continue
            seen.add(n);todo.extend((d,path+[d]) for d in sorted(graph[n]))
        raise AssertionError((a,b,'no route'))
    for a,b in (('NavelRock_Harbor','NavelRock_Top'),('NavelRock_Top','NavelRock_Harbor'),('NavelRock_Harbor','NavelRock_Bottom'),('NavelRock_Bottom','NavelRock_Harbor')):routes[a+' -> '+b]=route(a,b)
    banks=[]
    for theme,entry in build['banks'].items():
        n=GROUPS[theme][0];r,br=rr(ROOT,ls[maps[n]['layout']]),rr(base,bl[bm[n]['layout']])
        for mid in entry['layer_mask_ids']:
            for a,b in zip(native_layers(br,mid),native_layers(r,mid)):assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes(),(theme,hex(mid),'layer mask');layer_masks+=1
        for kind,(rel,source) in enumerate(zip(entry['paths'],entry['source_paths'])):
            p=ROOT/rel;aa=words(p/'metatile_attributes.bin');assert aa==words(base/source/'metatile_attributes.bin');attributes+=len(aa)
            im,row,count=indexed_tiles(p/'tiles.png');assert count<=512
            meta=words(p/'metatiles.bin');assert len(meta)==len(aa)*8
            for e in meta:
                assert e>>12<13
                t=e&1023;bank=r.primary_tiles if t<512 else r.secondary_tiles;assert t%512<bank[2],(rel,t,'missing tile')
            for i in range(count):
                pixels=list(im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8)).getdata());packed=bytes(pixels[j]|pixels[j+1]<<4 for j in range(0,64,2));assert [v for b in packed for v in (b&15,b>>4)]==pixels
            for q in range(13):
                raw=(p/f'palettes/{q:02}.pal').read_bytes();assert raw.count(b'\r\n')==raw.count(b'\n');palette(p/f'palettes/{q:02}.pal')
            assert callback(ROOT,'gTileset_'+entry['symbols'][kind])==entry['callbacks'][kind]
            banks.append({'path':rel,'tiles':count,'attribute_words':len(aa),'callback':entry['callbacks'][kind]})
        reserved=set(range(432,512))|set(range(992,1024))
        if theme=='coast':reserved.update(range(682,688))
        assert set(entry['reserved_animation_tiles'])==reserved
        assert not set(entry['allocated_tiles'])&reserved
        # Stored reserved bytes plus four live frames: animation slots cannot
        # overwrite any newly allocated graphic or change their silhouettes.
        stored,stored_before=rr(ROOT,ls[maps[n]['layout']],-1),rr(base,bl[bm[n]['layout']],-1)
        for tile in sorted(reserved):
            a,b=stored._tile(tile),stored_before._tile(tile);assert (a.tobytes() if a else None)==(b.tobytes() if b else None)
        for frame in range(4):
            ar,brr=rr(ROOT,ls[maps[n]['layout']],frame),rr(base,bl[bm[n]['layout']],frame)
            for tile in sorted(reserved):
                a,b=ar._tile(tile),brr._tile(tile);assert (a.tobytes() if a else None)==(b.tobytes() if b else None)
    companion='BirthIsland_Harbor';l=ls[maps[companion]['layout']];old=bl[bm[companion]['layout']];assert l==old and maps[companion]==bm[companion]
    for frame in range(4):
        a,b=rr(ROOT,l,frame),rr(base,old,frame)
        for v in words(ROOT/l['blockdata_filepath']):assert a.metatile(v&1023).tobytes()==b.metatile(v&1023).tobytes()
    # Reach the trigger, hidden ash and an adjacent interaction cell on the
    # unchanged landing surfaces; these are not new placement coordinates.
    for n in ('NavelRock_Top','NavelRock_Bottom','NavelRock_Harbor'):
        m=maps[n];l=ls[m['layout']];g=words(ROOT/l['blockdata_filepath']);seen=reachable(l,g,(m['warp_events'][0]['x'],m['warp_events'][0]['y']))
        for e in m['coord_events']+m['bg_events']:assert (e['x'],e['y']) in seen,(n,e)
        for e in m['object_events']:
            if e['script']=='0x0':continue
            assert any((e['x']+dx,e['y']+dy) in seen for dx,dy in ((-1,0),(1,0),(0,-1),(0,1))),(n,e['local_id'],'interaction')
    scripts=script_checks();dump(OUT/'navigation.json',{'warps':all_edges,'routes':routes,'ferry':{'arrival':['NavelRock_Harbor',8,4],'return':['LilycoveCity_Harbor',8,11]}})
    report={'status':'PASS','base_commit':BASE,'protected_gameplay_files':len(contract['protected_hashes']),'other_tracked_dependencies':len(contract['dependency_hashes']),'maps':reports,'banks':banks,'core_maps':21,'dependent_harbor':1,'native_warps':warp_cells,'appended_private_layouts':9,'full_native_attributes':attributes,'native_layer_masks':layer_masks,'plain_cells_checked':plain_cells,'blocked_rim_cells_checked':rim_cells,'actual_c_selector_cells':cells,'actual_c_fallback_cases':fallbacks,'previous_cavern_dive_cells':legacy,'previous_trainer_hill_generated_cells':trainer_cells,'birth_island_harbor_unchanged_cells':221,'native_c':c_report,'event_fragments':scripts,'rom_build':'pending: ARM compiler unavailable','emulator':'pending: mGBA unavailable'}
    report['native_summit_sky_pixels_preserved']=sky_pixels
    dump(OUT/'validation.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ('maps','banks')},indent=2))
if __name__=='__main__':main()
