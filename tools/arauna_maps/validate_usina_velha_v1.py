#!/usr/bin/env python3
"""Check New Mauville's two adapted maps and electrical events."""
import json,struct,subprocess
from PIL import Image
from build_usina_velha_v1 import ROOT,PRIMARY,SECONDARY,MAPS,OLD,NEW,SIZES,BASE

def words(path):
    b=path.read_bytes();return struct.unpack('<%dH'%(len(b)//2),b)

def main():
    layouts=json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']
    baseline_meta=words(ROOT/'data/tilesets/secondary/bike_shop/metatiles.bin')
    baseline_attrs=words(ROOT/'data/tilesets/secondary/bike_shop/metatile_attributes.bin')
    meta=words(SECONDARY/'metatiles.bin');attrs=words(SECONDARY/'metatile_attributes.bin')
    assert meta[:len(baseline_meta)]==baseline_meta and attrs[:len(baseline_attrs)]==baseline_attrs
    assert len(meta)==254*8 and len(attrs)==254
    assert Image.open(SECONDARY/'tiles.png').size==(128,256)
    assert words(PRIMARY/'metatiles.bin')==words(ROOT/'data/tilesets/primary/general/metatiles.bin')
    report={}
    for level,(name,old_id,new_id,(w,h)) in enumerate(zip(MAPS,OLD,NEW,SIZES)):
        rel=f'data/maps/{name}/map.json'
        before=json.loads(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT))
        event=json.loads((ROOT/rel).read_text());assert event=={**before,'layout':new_id}
        old=next(r for r in layouts if r['id']==old_id)
        new=next(r for r in layouts if r['id']==new_id)
        assert (new['width'],new['height'])==(w,h)
        assert new['primary_tileset']=='gTileset_AraunaUsinaRocha'
        assert new['secondary_tileset']==('gTileset_Facility' if level==0 else 'gTileset_AraunaUsinaMaquinas')
        a=words(ROOT/old['blockdata_filepath']);b=words(ROOT/new['blockdata_filepath'])
        assert len(a)==len(b)==w*h
        counts=[0]*6;changed=set()
        for i,(v,t) in enumerate(zip(a,b)):
            if v==t:continue
            x,y=i%w,i//w
            assert level==1 and v&1023==528 and BASE<=t&1023<BASE+6,(name,x,y)
            assert (v^t)&~1023==0,(name,x,y,'collision/elevation changed')
            changed.add((x,y));counts[(t&1023)-BASE]+=1
        if level==0:assert counts==[0]*6
        else:
            assert counts[:2]==[6,8] and counts[2:]==[3]*4,counts
            for px,py in ((29,6),(21,27),(6,18)):
                assert [b[(py+dy)*w+px+dx]&1023 for dy in (0,1) for dx in (0,1)]==list(range(BASE+2,BASE+6))
        occupied={(int(obj['x']),int(obj['y'])) for key in ('warp_events','object_events','coord_events','bg_events') for obj in event[key]}
        assert not occupied.intersection(changed)
        assert (ROOT/old['border_filepath']).read_bytes()==(ROOT/new['border_filepath']).read_bytes()
        report[name]={'changed':len(changed),'warps':len(event['warp_events']),
                      'coord_events':len(event['coord_events']),'bg_events':len(event['bg_events'])}
    for part in range(6):
        assert attrs[248+part]==baseline_attrs[528-512]
        entries=meta[(248+part)*8:(249+part)*8]
        assert entries[:4]==baseline_meta[(528-512)*8:(528-512)*8+4]
        start=(0x3d0+part*4) if part<2 else (0x268+(part-2)*4)
        assert [v&1023 for v in entries[4:]]==list(range(start,start+4))
        assert all(v>>12==(6 if part<2 else 11) for v in entries[4:])
    print(json.dumps({'status':'PASS','maps':report,'events_and_collision_preserved':True},indent=2))

if __name__=='__main__':main()
