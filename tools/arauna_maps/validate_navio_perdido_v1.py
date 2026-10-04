#!/usr/bin/env python3
"""Validate thirteen Abandoned Ship layouts, decorations and event links."""
import json,struct,subprocess
from PIL import Image
from build_navio_perdido_v1 import ROOT,MAPS,PRIMARY,FACILITY,SHIP,FLOODED,FLOODED_MAPS,BASE,layout_id

def words(path):
    b=path.read_bytes();return struct.unpack('<%dH'%(len(b)//2),b)

def main():
    layouts={r['id']:r for r in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
    original=ROOT/'data/tilesets/secondary/inside_ship'
    old_meta=words(original/'metatiles.bin');old_attrs=words(original/'metatile_attributes.bin')
    for target in (SHIP,FLOODED):
        meta=words(target/'metatiles.bin');attrs=words(target/'metatile_attributes.bin')
        assert meta[:len(old_meta)]==old_meta and attrs[:len(old_attrs)]==old_attrs
        assert len(meta)==254*8 and len(attrs)==254
        assert Image.open(target/'tiles.png').size==(128,256)
        for kind,src in enumerate((568,514)):
            assert attrs[252+kind]==old_attrs[src-512]
            entries=meta[(252+kind)*8:(253+kind)*8]
            assert entries[:4]==old_meta[(src-512)*8:(src-512)*8+4]
            assert [v&1023 for v in entries[4:]]==list(range(0x3f8+4*kind,0x3fc+4*kind))
            assert all(v>>12==11 for v in entries[4:])
    assert words(PRIMARY/'metatiles.bin')==words(ROOT/'data/tilesets/primary/general/metatiles.bin')
    assert words(FACILITY/'metatiles.bin')==words(ROOT/'data/tilesets/secondary/facility/metatiles.bin')
    assert words(FLOODED/'metatiles.bin')==words(SHIP/'metatiles.bin')
    report={};total_warps=0;total_objects=0
    for name in MAPS:
        rel=f'data/maps/{name}/map.json'
        before=json.loads(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT))
        after=json.loads((ROOT/rel).read_text())
        new_id=layout_id(name)
        assert after=={**before,'layout':new_id}
        old=layouts[before['layout']];new=layouts[new_id]
        w,h=old['width'],old['height']
        assert (new['width'],new['height'])==(w,h)
        assert new['primary_tileset']=='gTileset_AraunaNavioMar'
        inside=old['secondary_tileset']=='gTileset_InsideShip'
        expected=('gTileset_AraunaNavioAlagado' if name in FLOODED_MAPS else
                  'gTileset_AraunaNavioInterior' if inside else 'gTileset_AraunaNavioConves')
        assert new['secondary_tileset']==expected
        a=words(ROOT/old['blockdata_filepath']);b=words(ROOT/new['blockdata_filepath'])
        assert len(a)==len(b)==w*h
        counts=[0,0];changed=[]
        for i,(v,t) in enumerate(zip(a,b)):
            if v==t:continue
            x,y=i%w,i//w;src,dst=v&1023,t&1023
            assert inside and (src,dst) in ((568,BASE),(514,BASE+1)),(name,x,y,src,dst)
            assert (v^t)&~1023==0,(name,x,y,'collision/elevation changed')
            counts[dst-BASE]+=1;changed.append((x,y))
        occupied={(int(e['x']),int(e['y'])) for key in ('warp_events','object_events','coord_events','bg_events') for e in after[key]}
        assert not occupied.intersection(changed)
        assert (ROOT/old['border_filepath']).read_bytes()==(ROOT/new['border_filepath']).read_bytes()
        total_warps+=len(after['warp_events']);total_objects+=len(after['object_events'])
        report[name]={'marks':counts,'warps':len(after['warp_events'])}
    assert total_warps==63 and total_objects==24,(total_warps,total_objects)
    assert sum(sum(r['marks']) for r in report.values())>=8
    print(json.dumps({'status':'PASS','maps':report,'warps':total_warps,'objects':total_objects,
                      'collision_and_events_preserved':True},indent=2))

if __name__=='__main__':main()
