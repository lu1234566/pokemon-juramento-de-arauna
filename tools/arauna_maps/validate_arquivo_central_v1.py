#!/usr/bin/env python3
"""Validate the six technical Aqua Hideout maps and archive tileset."""
import json,struct,subprocess
from PIL import Image
from build_arquivo_central_v1 import ROOT,MAPS,SOURCE,TARGET,BASE,layout_id

def words(path):
    b=path.read_bytes();return struct.unpack('<%dH'%(len(b)//2),b)

def main():
    layouts={r['id']:r for r in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
    original_meta=words(SOURCE/'metatiles.bin');original_attrs=words(SOURCE/'metatile_attributes.bin')
    meta=words(TARGET/'metatiles.bin');attrs=words(TARGET/'metatile_attributes.bin')
    assert meta[:len(original_meta)]==original_meta and attrs[:len(original_attrs)]==original_attrs
    assert len(meta)==512*8 and len(attrs)==512
    assert Image.open(TARGET/'tiles.png').size==(128,256)
    assert attrs[511]==original_attrs[552-512]
    entries=meta[511*8:512*8]
    assert entries[:4]==original_meta[(552-512)*8:(552-512)*8+4]
    assert [v&1023 for v in entries[4:]]==list(range(1015,1019))
    assert all(v>>12==9 for v in entries[4:])
    report={};warps=objects=0
    for name in MAPS:
        rel=f'data/maps/{name}/map.json';baseline=json.loads(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT))
        event=json.loads((ROOT/rel).read_text());new_id=layout_id(name)
        assert event=={**baseline,'layout':new_id}
        old=layouts[baseline['layout']];new=layouts[new_id]
        w,h=old['width'],old['height'];assert (new['width'],new['height'])==(w,h)
        assert new['primary_tileset']=='gTileset_General'
        assert new['secondary_tileset']=='gTileset_AraunaArquivoCentral'
        a=words(ROOT/old['blockdata_filepath']);b=words(ROOT/new['blockdata_filepath']);assert len(a)==len(b)==w*h
        changed=[]
        for i,(v,t) in enumerate(zip(a,b)):
            if v==t:continue
            x,y=i%w,i//w;assert (v&1023,t&1023)==(552,BASE),(name,x,y,v&1023,t&1023)
            assert (v^t)&~1023==0,(name,x,y,'collision/elevation changed')
            changed.append((x,y))
        occupied={(int(e['x']),int(e['y'])) for key in ('warp_events','object_events','coord_events','bg_events') for e in event[key]}
        assert not occupied.intersection(changed)
        assert (ROOT/old['border_filepath']).read_bytes()==(ROOT/new['border_filepath']).read_bytes()
        warps+=len(event['warp_events']);objects+=len(event['object_events'])
        report[name]={'archive_seals':len(changed),'warps':len(event['warp_events'])}
    assert warps==38 and objects==20
    print(json.dumps({'status':'PASS','maps':report,'warps':warps,'objects':objects,
                      'collision_and_events_preserved':True},indent=2))

if __name__=='__main__':main()
