#!/usr/bin/env python3
"""Validate six Cave of Origin maps and primordial mineral art."""
import json,struct,subprocess
from PIL import Image
from build_gruta_da_origem_v1 import ROOT,MAPS,SOURCE,TARGET,BASE,layout_id

def words(path):
    b=path.read_bytes();return struct.unpack('<%dH'%(len(b)//2),b)

def main():
    layouts={r['id']:r for r in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
    original_meta=words(SOURCE/'metatiles.bin');original_attrs=words(SOURCE/'metatile_attributes.bin')
    meta=words(TARGET/'metatiles.bin');attrs=words(TARGET/'metatile_attributes.bin')
    assert meta[:len(original_meta)]==original_meta and attrs[:len(original_attrs)]==original_attrs
    assert len(meta)==416*8 and len(attrs)==416
    assert Image.open(TARGET/'tiles.png').size==(128,256)
    for kind,src in enumerate((819,795)):
        assert attrs[414+kind]==original_attrs[src-512]
        entries=meta[(414+kind)*8:(415+kind)*8]
        assert entries[:4]==original_meta[(src-512)*8:(src-512)*8+4]
        assert [v&1023 for v in entries[4:]]==list(range(0x3f8+kind*4,0x3fc+kind*4))
        assert all(v>>12==11 for v in entries[4:])
    report={};warps=objects=0
    for name in MAPS:
        rel=f'data/maps/{name}/map.json';baseline=json.loads(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT))
        event=json.loads((ROOT/rel).read_text());new_id=layout_id(name)
        assert event=={**baseline,'layout':new_id}
        old=layouts[baseline['layout']];new=layouts[new_id]
        w,h=old['width'],old['height'];assert (new['width'],new['height'])==(w,h)
        assert new['primary_tileset']=='gTileset_General'
        assert new['secondary_tileset']=='gTileset_AraunaGrutaOrigem'
        a=words(ROOT/old['blockdata_filepath']);b=words(ROOT/new['blockdata_filepath']);assert len(a)==len(b)==w*h
        counts=[0,0];changed=[]
        for i,(v,t) in enumerate(zip(a,b)):
            if v==t:continue
            x,y=i%w,i//w;src,dst=v&1023,t&1023
            assert (src,dst) in ((819,BASE),(795,BASE+1)),(name,x,y,src,dst)
            assert (v^t)&~1023==0,(name,x,y,'collision/elevation changed')
            counts[dst-BASE]+=1;changed.append((x,y))
        occupied={(int(e['x']),int(e['y'])) for key in ('warp_events','object_events','coord_events','bg_events') for e in event[key]}
        assert not occupied.intersection(changed)
        assert (ROOT/old['border_filepath']).read_bytes()==(ROOT/new['border_filepath']).read_bytes()
        warps+=len(event['warp_events']);objects+=len(event['object_events'])
        report[name]={'moss_and_roots':counts,'warps':len(event['warp_events'])}
    assert warps==11 and objects==1
    assert sum(sum(x['moss_and_roots']) for x in report.values())==20
    print(json.dumps({'status':'PASS','maps':report,'warps':warps,'objects':objects,
                      'collision_and_events_preserved':True},indent=2))

if __name__=='__main__':main()
