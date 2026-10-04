#!/usr/bin/env python3
"""Validate eight Mt. Pyre maps and all preserved native connections."""
import json,struct,subprocess
from PIL import Image
from build_memorial_nomes_v1 import ROOT,MAPS,PRIMARY_SOURCE,PRIMARY,SECONDARY_SOURCE,SECONDARY,CRYSTAL,layout_id

def words(path):
    b=path.read_bytes();return struct.unpack('<%dH'%(len(b)//2),b)

def main():
    layouts={r['id']:r for r in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
    for src,dst in ((PRIMARY_SOURCE,PRIMARY),(SECONDARY_SOURCE,SECONDARY)):
        original_meta=words(src/'metatiles.bin');original_attrs=words(src/'metatile_attributes.bin')
        meta=words(dst/'metatiles.bin');attrs=words(dst/'metatile_attributes.bin')
        assert meta[:len(original_meta)]==original_meta and attrs[:len(original_attrs)]==original_attrs
        assert Image.open(dst/'tiles.png').size==Image.open(src/'tiles.png').size
    primary_meta=words(PRIMARY/'metatiles.bin');primary_attrs=words(PRIMARY/'metatile_attributes.bin')
    meta=words(SECONDARY/'metatiles.bin');attrs=words(SECONDARY/'metatile_attributes.bin')
    assert len(attrs)==512 and len(meta)==512*8
    assert attrs[511]==primary_attrs[1]
    assert meta[511*8:511*8+4]==primary_meta[8:12]
    assert [x&1023 for x in meta[511*8+4:512*8]]==list(range(1015,1019))
    assert all(x>>12==9 for x in meta[511*8+4:512*8])
    report={};warps=objects=0;total=0
    for name in MAPS:
        rel=f'data/maps/{name}/map.json';baseline=json.loads(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT))
        event=json.loads((ROOT/rel).read_text());new_id=layout_id(name)
        assert event=={**baseline,'layout':new_id}
        old=layouts[baseline['layout']];new=layouts[new_id]
        w,h=old['width'],old['height'];assert (new['width'],new['height'])==(w,h)
        assert new['primary_tileset']=='gTileset_AraunaMemorialExterior'
        assert new['secondary_tileset']=='gTileset_AraunaMemorialNomes'
        a=words(ROOT/old['blockdata_filepath']);b=words(ROOT/new['blockdata_filepath']);assert len(a)==len(b)==w*h
        changed=[]
        for i,(v,t) in enumerate(zip(a,b)):
            if v==t:continue
            x,y=i%w,i//w;assert name=='MtPyre_Summit' and (v&1023,t&1023)==(1,CRYSTAL),(name,x,y)
            assert (v^t)&~1023==0,(name,x,y,'collision/elevation changed')
            changed.append((x,y))
        occupied={(int(e['x']),int(e['y'])) for key in ('warp_events','object_events','coord_events','bg_events') for e in event[key]}
        assert not occupied.intersection(changed)
        assert (ROOT/old['border_filepath']).read_bytes()==(ROOT/new['border_filepath']).read_bytes()
        total+=len(changed);warps+=len(event['warp_events']);objects+=len(event['object_events'])
        report[name]={'crystals':len(changed),'warps':len(event['warp_events'])}
    assert total==8 and warps==36 and objects==38
    print(json.dumps({'status':'PASS','maps':report,'warps':warps,'objects':objects,
                      'collision_and_events_preserved':True},indent=2))

if __name__=='__main__':main()
