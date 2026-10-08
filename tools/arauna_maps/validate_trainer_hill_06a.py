#!/usr/bin/env python3
"""Cumulative protection, native banks, live floor C and unchanged door colors."""
import argparse,hashlib,json,re,subprocess,tempfile
from pathlib import Path
from PIL import Image
from trainer_hill_06a_common import BASE,ROOT,OUT,NAMES,ELEVATOR_ID,inventory,renderer,floors,runtime_words
from trainer_hill_06a_art import PLINTHS,DOORS_STAIRS,native_layers
from trainer_hill_06a_c_checks import checks
from native_visuals_v2 import dump,callback
from render_native_map import words,palette,indexed_tiles
from bancos_nativos import bank_words
import safari_05_c_checks as previous

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve()
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
    contract=json.loads((OUT/'functional_contract.json').read_text());build=json.loads((OUT/'build.json').read_text())
    for rel,h in {**contract['protected_hashes'],**contract['dependency_hashes']}.items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,('protected',rel)
    before,bl,bm=inventory(base);node,ls,maps=inventory(ROOT);assert len(before['layouts'])==744 and len(node['layouts'])==745
    targets={bm[n]['layout'] for n in NAMES if n!='TrainerHill_Elevator'}
    for old,new in zip(before['layouts'],node['layouts']):
        if old['id'] in targets:assert {k:v for k,v in old.items() if k not in ('primary_tileset','secondary_tileset')}=={k:v for k,v in new.items() if k not in ('primary_tileset','secondary_tileset')}
        else:assert old==new,old['id']
    elevator=node['layouts'][-1];original=bl[bm['TrainerHill_Elevator']['layout']]
    assert elevator['id']==ELEVATOR_ID and maps['TrainerHill_Elevator']['layout']==ELEVATOR_ID
    assert {k:v for k,v in elevator.items() if k not in ('id','name','primary_tileset','secondary_tileset')}=={k:v for k,v in original.items() if k not in ('id','name','primary_tileset','secondary_tileset')}
    assert {k:v for k,v in maps['TrainerHill_Elevator'].items() if k!='layout'}=={k:v for k,v in bm['TrainerHill_Elevator'].items() if k!='layout'}
    for rel in ('graphics.h','metatiles.h','headers.h'):
        new=(ROOT/'src/data/tilesets'/rel).read_text();stripped=re.sub(r'\n*// TRAINER_HILL_06A_BEGIN\n.*?// TRAINER_HILL_06A_END\n','\n',new,flags=re.S)
        assert stripped.rstrip()==(base/'src/data/tilesets'/rel).read_text().rstrip(),rel
    assert json.loads(json.dumps(floors(ROOT)))==json.loads(json.dumps(floors(base)))==contract['runtime_floors']
    cells=runtime_cells=fallbacks=legacy=attributes=plain_cells=barrier_cells=plane_masks=0;reports={};cache={}
    def rr(repo,l):
        key=str(repo),l['primary_tileset'],l['secondary_tileset']
        if key not in cache:cache[key]=renderer(repo,l)
        return cache[key]
    with tempfile.TemporaryDirectory() as temp:
        previous.NAMES=NAMES+('BattleFrontier_BattleTowerElevator',)
        selector,_=previous.selector(Path(temp)/'selector');native_c=checks(Path(temp)/'hill')
        header=(base/'src/data/arauna_cave_visuals_v2.h').read_text()
        for idx,n in re.findall(r'\{(\d+), sVisual_(\w+)\}',header):
            l=node['layouts'][int(idx)];g=words(ROOT/l['blockdata_filepath']);path=re.search(r'sVisual_'+n+r'\[\] = INCBIN_U16\("([^"]+)"\)',header)[1];expected=words(base/path)
            for i,v in enumerate(g):assert selector.probe(int(idx),i%l['width']+7,i//l['width']+7,v&1023)==expected[i];legacy+=1
        for n in NAMES:
            l=ls[maps[n]['layout']];old=bl[bm[n]['layout']];r=rr(ROOT,l);br=rr(base,old);g=words(ROOT/l['blockdata_filepath']);assert g==words(base/old['blockdata_filepath'])
            idx=node['layouts'].index(l);changed={}
            for mid in {v&1023 for v in g}|{v&1023 for v in words(ROOT/l['border_filepath'])}:
                assert bank_words(r,mid,True)==bank_words(br,mid,True),(n,hex(mid),'full attribute')
                changed[mid]=r.metatile(mid).tobytes()!=br.metatile(mid).tobytes()
            for i,v in enumerate(g):assert selector.probe(idx,i%l['width']+7,i//l['width']+7,v&1023)==v&1023;cells+=1
            for x,y in ((7,7),(6,7),(7,6),(l['width']+7,7),(7,l['height']+7)):
                for mid in range(1024):assert selector.probe(idx,x,y,mid)==mid;fallbacks+=1
            count=sum(changed[v&1023] for v in g);assert count>0,n
            reports[n]={'cells':len(g),'changed_visual_cells':count,'warps':len(maps[n]['warp_events']),'objects':len(maps[n]['object_events']),'layout':l['id']}
        runtime={}
        for key,f in floors(ROOT).items():
            l,g=runtime_words(ROOT,f);old,oldg=runtime_words(base,f);assert g==oldg
            r=rr(ROOT,l);br=rr(base,old);idx=node['layouts'].index(l);changed=0
            plain=set(build['banks']['pavilion']['plain_ids'])
            for i,v in enumerate(g):
                mid=v&1023;assert selector.probe(idx,i%16+7,i//16+7,mid)==mid
                assert bank_words(r,mid,True)==bank_words(br,mid,True)
                if mid in plain:assert not v&0xc00,(key,hex(mid),'plain ground blocks');plain_cells+=1
                if mid in PLINTHS|{0x221,0x246}:assert v&0xc00,(key,hex(mid),'barrier is traversable');barrier_cells+=1
                changed+=r.metatile(mid).tobytes()!=br.metatile(mid).tobytes();runtime_cells+=1
            assert changed>0;runtime[key]={'cells':len(g),'changed_visual_cells':changed,'trainer_coordinates':f['trainers']}
    banks=[]
    for theme,entry in build['banks'].items():
        l=ls[maps[NAMES[0] if theme=='pavilion' else NAMES[-1]]['layout']];old=bl[bm[NAMES[0] if theme=='pavilion' else NAMES[-1]]['layout']];r=rr(ROOT,l);br=rr(base,old)
        for mid in entry['material_plane_ids']:
            if mid==0x380:continue
            for a,b in zip(native_layers(br,mid),native_layers(r,mid)):
                assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes(),(theme,hex(mid),'layer footprint');plane_masks+=1
        for kind,(rel,source) in enumerate(zip(entry['paths'],entry['source_paths'])):
            p=ROOT/rel;oldbank=base/source;aa=words(p/'metatile_attributes.bin');assert aa==words(oldbank/'metatile_attributes.bin');attributes+=len(aa)
            im,row,count=indexed_tiles(p/'tiles.png');assert count<=512
            meta=words(p/'metatiles.bin');assert len(meta)==len(aa)*8 and all(e>>12<13 for e in meta)
            for e in meta:
                actual=e&1023;bank=r.primary_tiles if actual<512 else r.secondary_tiles;assert actual%512<bank[2],(rel,actual,'missing graphics')
            for i in range(count):
                pixels=list(im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8)).getdata());packed=bytes(pixels[j]|pixels[j+1]<<4 for j in range(0,64,2));assert [v for b in packed for v in (b&15,b>>4)]==pixels
            for q in range(13):
                raw=(p/f'palettes/{q:02}.pal').read_bytes();assert raw.count(b'\r\n')==raw.count(b'\n')
                palette(p/f'palettes/{q:02}.pal')
            assert not set(entry['allocated_tiles'])&(set(range(432,512))|set(range(992,1024)))
            assert callback(ROOT,'gTileset_'+entry['symbols'][kind])==entry['callbacks'][kind]
            banks.append({'path':rel,'tiles':count,'original_attribute_words':len(aa),'callback':entry['callbacks'][kind]})
        for q in (7,9):assert r.palettes[q]==br.palettes[q],(theme,q,'door palette')
        for tile in tuple(range(432,512))+tuple(range(992,1024)):
            a,b=r._tile(tile),br._tile(tile)
            assert (a.tobytes() if a is not None else None)==(b.tobytes() if b is not None else None),(theme,tile,'animation tile')
    first=ls[maps[NAMES[0]]['layout']];old=bl[bm[NAMES[0]]['layout']]
    after=rr(ROOT,first);before_r=rr(base,old)
    for mid in (0x32c,0x383):assert after.metatile(mid).tobytes()==before_r.metatile(mid).tobytes(),('elevator door',hex(mid))
    companion='BattleFrontier_BattleTowerElevator';l=ls[maps[companion]['layout']];old=bl[bm[companion]['layout']];g=words(ROOT/l['blockdata_filepath']);r=rr(ROOT,l);br=rr(base,old)
    assert l==old and maps[companion]==bm[companion]
    for v in g:assert r.metatile(v&1023).tobytes()==br.metatile(v&1023).tobytes() and bank_words(r,v&1023,True)==bank_words(br,v&1023,True)
    endpoints={n:{'warps':maps[n]['warp_events'],'script_metatiles':re.findall(r'^\s*setmetatile\s+(.+)',(ROOT/f'data/maps/{n}/scripts.inc').read_text(),re.M)} for n in NAMES}
    dump(OUT/'endpoints.json',endpoints)
    report={'status':'PASS','base_commit':BASE,'protected_gameplay_files':len(contract['protected_hashes']),'protected_dependencies':len(contract['dependency_hashes']),'maps':reports,'runtime':runtime,'banks':banks,'full_native_attributes_preserved':attributes,'actual_c_static_selector_cells':cells,'actual_c_runtime_selector_cells':runtime_cells,'actual_c_fallback_cases':fallbacks,'previous_cavern_dive_selector_cells':legacy,'plain_cells_checked':plain_cells,'barrier_cells_checked':barrier_cells,'architectural_layer_masks_preserved':plane_masks,'battle_tower_elevator_unchanged_cells':len(g),'door_palettes_preserved':[7,9],'native_elevator_closed_door_ids_unchanged':[0x32c,0x383],'native_c':native_c,'rom_build':'pending: ARM compiler unavailable','emulator':'pending: mGBA unavailable'}
    dump(OUT/'validation.json',report)
    print(json.dumps({k:v for k,v in report.items() if k not in ('maps','runtime','banks')},indent=2))

if __name__=='__main__':main()
