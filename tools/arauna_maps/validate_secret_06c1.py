#!/usr/bin/env python3
"""Exact preservation contract, native bank layers and production C checks."""
import argparse,hashlib,json,re,tempfile
from pathlib import Path
from secret_06c1_common import *
from render_native_map import indexed_tiles,words
from trainer_hill_06a_art import native_layers
from secret_06c1_c_checks import checks
from validate_navel_06b import reachable
import safari_05_c_checks as selector_source

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    contract=json.loads((OUT/'functional_contract.json').read_text());build=json.loads((OUT/'build.json').read_text())
    for p,h in {**contract['protected_hashes'],**contract['dependency_hashes']}.items():
        assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,('frozen',p)
    before,bl,bm=inventory(base);node,ls,ms=inventory(ROOT);assert len(node['layouts'])==len(before['layouts'])==754
    target={bm[n]['layout'] for n in NAMES}
    for a,b in zip(before['layouts'],node['layouts']):
        if a['id'] in target:
            assert {k:v for k,v in a.items() if k!='secondary_tileset'}=={k:v for k,v in b.items() if k!='secondary_tileset'}
        else:assert a==b,a['id']
    for f in ('graphics.h','metatiles.h','headers.h'):
        raw=(ROOT/'src/data/tilesets'/f).read_text();raw=re.sub(r'\n*// SECRET_BASES_06C1_BEGIN\n.*?// SECRET_BASES_06C1_END\n','\n',raw,flags=re.S)
        assert raw.rstrip()==(base/'src/data/tilesets'/f).read_text().rstrip()
    masks=attrs=foreground_entries=palettes=tiles=changed_cells=selector_cells=legacy=0;details={}
    for color in COLORS:
        n=next(n for n in NAMES if '_'+color+'Cave' in n);l=ls[ms[n]['layout']];old=bl[bm[n]['layout']]
        p,op=parts(ROOT,l['secondary_tileset']),parts(base,old['secondary_tileset']);r,br=SecretRenderer(ROOT,l),SecretRenderer(base,old)
        am,bmwords=words(p['metatiles']),words(op['metatiles']);aa=words(p['attributes']);assert aa==words(op['attributes']);attrs+=len(aa)
        assert p['callback']==op['callback']=='NULL' and p['compressed'] and len(aa)==324
        assert 12 not in {v>>12 for v in bmwords+words(parts(base,old['primary_tileset'])['metatiles'])}
        for a,b in zip(am,bmwords):
            if b&1023<512:assert a==b;foreground_entries+=1
            elif a!=b:assert b>>12==6 and a>>12==12 and (a&0xc00)==(b&0xc00)
        for q in range(12):assert p['palettes'][q].read_bytes()==op['palettes'][q].read_bytes();palettes+=1
        im,row,count=indexed_tiles(p['tiles']);oi,orow,_=indexed_tiles(op['tiles']);assert count==build['banks'][color]['static_tile_count']<=512
        for i in range(83):
            assert im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8)).tobytes()==oi.crop((i%orow*8,i//orow*8,i%orow*8+8,i//orow*8+8)).tobytes();tiles+=1
        for mid in range(512,836):
            for a,b in zip(native_layers(r,mid),native_layers(br,mid)):
                assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes(),(color,mid,'alpha');masks+=1
        for e in am:
            assert e>>12<13
            assert e&1023<512 or (e&1023)-512<count
        for i in range(count):
            px=list(im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8)).getdata());packed=bytes(px[j]|px[j+1]<<4 for j in range(0,64,2));assert [v for b in packed for v in (b&15,b>>4)]==px
    with tempfile.TemporaryDirectory() as temp:
        folder=Path(temp);_,c=checks(folder/'native',base);selector_source.NAMES=NAMES
        selector,_=selector_source.selector(folder/'selector')
        for n in NAMES:
            m=ms[n];assert m==contract['maps'][n]['map'];l=ls[m['layout']];old=bl[m['layout']];g=words(ROOT/l['blockdata_filepath']);assert g==words(base/old['blockdata_filepath'])
            r,br=SecretRenderer(ROOT,l),SecretRenderer(base,old);count=0;idx=node['layouts'].index(l)
            for i,v in enumerate(g):
                assert selector.probe(idx,i%l['width']+7,i//l['width']+7,v&1023)==v&1023;selector_cells+=1
                count+=r.metatile(v&1023).tobytes()!=br.metatile(v&1023).tobytes()
            assert count>0;changed_cells+=count
            warp=m['warp_events'];assert len(warp)==1 and warp[0]['dest_map']=='MAP_DYNAMIC' and warp[0]['dest_warp_id']=='WARP_ID_SECRET_BASE'
            seen=reachable(l,g,(warp[0]['x'],warp[0]['y']));assert seen==reachable(old,g,(warp[0]['x'],warp[0]['y']))
            pc=c['maps'][n]['pc'];assert (pc[0],pc[1]+1) in seen,(n,'PC access')
            details[n]={'cells':len(g),'changed_visual_cells':count,'reachable_cells':len(seen),'layout':l['id'],'theme':build['maps'][n]['theme']}
        header=(ROOT/'src/data/arauna_cave_visuals_v2.h').read_text()
        for idx,n in re.findall(r'\{(\d+), sVisual_(\w+)\}',header):
            l=node['layouts'][int(idx)];g=words(ROOT/l['blockdata_filepath']);p=re.search(r'sVisual_'+n+r'\[\] = INCBIN_U16\("([^"]+)"\)',header)[1];visual=words(ROOT/p)
            for i,v in enumerate(g):assert selector.probe(int(idx),i%l['width']+7,i//l['width']+7,v&1023)==visual[i];legacy+=1
    for n in ms:
        if n.startswith('SecretBase_') and n not in NAMES:
            l=ls[ms[n]['layout']];old=bl[ms[n]['layout']];assert render(ROOT,l).tobytes()==render(base,old).tobytes(),n
    report={'status':'PASS','base_commit':BASE,'github_base':GITHUB_BASE,'maps':details,'cave_maps':16,'cells':selector_cells,'changed_visual_cells':changed_cells,'native_attributes':attrs,'native_layer_masks':masks,'preserved_primary_foreground_entries':foreground_entries,'preserved_palette_files':palettes,'preserved_original_graphic_tiles':tiles,'layout_count':754,'appended_layouts':0,'external_entrances_unchanged':len(contract['external_entrances']),'protected_gameplay_files':len(contract['protected_hashes']),'other_tracked_dependencies':len(contract['dependency_hashes']),'previous_cavern_dive_selector_cells':legacy,'native_c':c,'rom_build':'pending: ARM compiler unavailable','emulator':'pending: mGBA unavailable'}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('maps','native_c')},indent=2))
if __name__=='__main__':main()
