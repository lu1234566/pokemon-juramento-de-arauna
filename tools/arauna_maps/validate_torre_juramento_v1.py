#!/usr/bin/env python3
"""Validate eight Sky Pillar layouts and progressive wear."""
import json,struct,subprocess
from PIL import Image
from build_torre_juramento_v1 import ROOT,MAPS,PRIMARY,SECONDARY,BASE,state,layout_id

def words(path):
    b=path.read_bytes();return struct.unpack('<%dH'%(len(b)//2),b)

def main():
    layouts={r['id']:r for r in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
    old_tiles=ROOT/'data/tilesets/secondary/pacifidlog'
    old_meta=words(old_tiles/'metatiles.bin');old_attrs=words(old_tiles/'metatile_attributes.bin')
    for k,target in SECONDARY.items():
        meta=words(target/'metatiles.bin');attrs=words(target/'metatile_attributes.bin')
        source=ROOT/'data/tilesets/secondary'/('cave' if k=='entrada' else 'pacifidlog')
        baseline=words(source/'metatiles.bin');baseline_attrs=words(source/'metatile_attributes.bin')
        assert meta[:len(baseline)]==baseline and attrs[:len(baseline_attrs)]==baseline_attrs
        if k=='entrada':assert len(attrs)==414
        else:
            assert len(attrs)==205 and Image.open(target/'tiles.png').size==(128,256)
            for kind,src in enumerate((701,564)):
                assert attrs[203+kind]==old_attrs[src-512]
                entries=meta[(203+kind)*8:(204+kind)*8]
                assert entries[:4]==old_meta[(src-512)*8:(src-512)*8+4]
                assert [v&1023 for v in entries[4:]]==list(range(0x3f8+kind*4,0x3fc+kind*4))
                assert all(v>>12==11 for v in entries[4:])
    assert words(PRIMARY/'metatiles.bin')==words(ROOT/'data/tilesets/primary/general/metatiles.bin')
    report={};total_warps=total_objects=0
    for name in MAPS:
        rel=f'data/maps/{name}/map.json'
        before=json.loads(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT))
        after=json.loads((ROOT/rel).read_text());new_id=layout_id(name)
        assert after=={**before,'layout':new_id}
        old=layouts[before['layout']];new=layouts[new_id]
        w,h=old['width'],old['height'];k=state(name)
        assert (new['width'],new['height'])==(w,h)
        assert new['primary_tileset']=='gTileset_AraunaTorreMar'
        expected={'costa':'AraunaTorreCosta','pisos_baixos':'AraunaTorrePisosBaixos',
                  'pisos_altos':'AraunaTorrePisosAltos','topo':'AraunaTorreTopo',
                  'entrada':'AraunaTorreEntrada'}[k]
        assert new['secondary_tileset']=='gTileset_'+expected
        a=words(ROOT/old['blockdata_filepath']);b=words(ROOT/new['blockdata_filepath'])
        assert len(a)==len(b)==w*h
        counts=[0,0];changed=[]
        for i,(v,t) in enumerate(zip(a,b)):
            if v==t:continue
            x,y=i%w,i//w;src,dst=v&1023,t&1023
            assert (src,dst) in ((701,BASE),(564,BASE+1)),(name,x,y,src,dst)
            assert (v^t)&~1023==0,(name,x,y,'collision/elevation changed')
            counts[dst-BASE]+=1;changed.append((x,y))
        occupied={(int(e['x']),int(e['y'])) for group in ('warp_events','object_events','coord_events','bg_events') for e in after[group]}
        assert not occupied.intersection(changed)
        assert (ROOT/old['border_filepath']).read_bytes()==(ROOT/new['border_filepath']).read_bytes()
        total_warps+=len(after['warp_events']);total_objects+=len(after['object_events'])
        report[name]={'level':k,'marks':counts,'warps':len(after['warp_events'])}
    assert total_warps==18 and total_objects==3,(total_warps,total_objects)
    assert sum(sum(x['marks']) for x in report.values())==28
    assert sum(report[f'SkyPillar_{n}']['marks'][0]+report[f'SkyPillar_{n}']['marks'][1] for n in ('4F','5F'))>sum(report[f'SkyPillar_{n}']['marks'][0]+report[f'SkyPillar_{n}']['marks'][1] for n in ('1F','2F'))
    print(json.dumps({'status':'PASS','maps':report,'warps':total_warps,'objects':total_objects,
                      'collision_and_events_preserved':True},indent=2))

if __name__=='__main__':main()
