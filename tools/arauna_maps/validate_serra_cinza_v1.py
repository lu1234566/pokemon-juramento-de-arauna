#!/usr/bin/env python3
"""Validate the volcanic summit and cable car station."""
import json,struct,subprocess
from PIL import Image
from build_serra_cinza_v1 import ROOT,MAPS,SOURCE,TARGET,STATION_SOURCE,STATION_TARGET,BASE,layout_id

def words(path):
    b=path.read_bytes();return struct.unpack('<%dH'%(len(b)//2),b)

def main():
    layouts={r['id']:r for r in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
    original_meta=words(SOURCE/'metatiles.bin');original_attrs=words(SOURCE/'metatile_attributes.bin')
    meta=words(TARGET/'metatiles.bin');attrs=words(TARGET/'metatile_attributes.bin')
    assert meta[:len(original_meta)]==original_meta and attrs[:len(original_attrs)]==original_attrs
    assert len(meta)==443*8 and len(attrs)==443
    assert Image.open(TARGET/'tiles.png').size==(128,256)
    for kind,src in enumerate((625,626)):
        assert attrs[441+kind]==original_attrs[src-512]
        entries=meta[(441+kind)*8:(442+kind)*8]
        assert entries[:4]==original_meta[(src-512)*8:(src-512)*8+4]
        assert [v&1023 for v in entries[4:]]==list(range(0x3f8+kind*4,0x3fc+kind*4))
    for filename in ('tiles.png','metatiles.bin','metatile_attributes.bin'):
        assert (STATION_SOURCE/filename).read_bytes()==(STATION_TARGET/filename).read_bytes()
    report={};warps=objects=0
    for name in MAPS:
        rel=f'data/maps/{name}/map.json';baseline=json.loads(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT))
        event=json.loads((ROOT/rel).read_text());new_id=layout_id(name)
        assert event=={**baseline,'layout':new_id}
        old=layouts[baseline['layout']];new=layouts[new_id]
        w,h=old['width'],old['height'];assert (new['width'],new['height'])==(w,h)
        assert new['primary_tileset']=='gTileset_General'
        assert new['secondary_tileset']==('gTileset_AraunaSerraCinzaEstacao' if name.endswith('CableCarStation') else 'gTileset_AraunaSerraCinza')
        a=words(ROOT/old['blockdata_filepath']);b=words(ROOT/new['blockdata_filepath']);assert len(a)==len(b)==w*h
        changed=[];counts=[0,0]
        for i,(v,t) in enumerate(zip(a,b)):
            if v==t:continue
            x,y=i%w,i//w;src,dst=v&1023,t&1023
            assert (src,dst) in ((625,BASE),(626,BASE+1)),(name,x,y,src,dst)
            assert (v^t)&~1023==0,(name,x,y,'collision/elevation changed')
            counts[dst-BASE]+=1;changed.append((x,y))
        occupied={(int(e['x']),int(e['y'])) for key in ('warp_events','object_events','coord_events','bg_events') for e in event[key]}
        assert not occupied.intersection(changed)
        assert (ROOT/old['border_filepath']).read_bytes()==(ROOT/new['border_filepath']).read_bytes()
        warps+=len(event['warp_events']);objects+=len(event['object_events'])
        report[name]={'maintenance_marks':counts,'warps':len(event['warp_events'])}
    assert warps==6 and objects==32
    print(json.dumps({'status':'PASS','maps':report,'warps':warps,'objects':objects,
                      'collision_and_events_preserved':True},indent=2))

if __name__=='__main__':main()
