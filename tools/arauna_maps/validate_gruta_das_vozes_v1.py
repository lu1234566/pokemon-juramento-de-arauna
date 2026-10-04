#!/usr/bin/env python3
"""Check four Granite Cave layouts against HEAD and native GBA constraints."""
import json
import struct
import subprocess
from pathlib import Path

from PIL import Image

from build_gruta_das_vozes_v1 import ROOT,NAMES,SUFFIX,SIZE,OLD,NEW,BASE


def words(path):
    raw=path.read_bytes();return struct.unpack('<%dH'%(len(raw)//2),raw)


def head(path):
    return subprocess.check_output(['git','show','HEAD:'+str(path)],cwd=ROOT)


def main():
    layouts=json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']
    cave=ROOT/'data/tilesets/secondary/cave'
    baseline_meta=words(cave/'metatiles.bin')
    baseline_attrs=words(cave/'metatile_attributes.bin')
    results={}
    for level,(name,suffix,(w,h),old_id,new_id) in enumerate(zip(NAMES,SUFFIX,SIZE,OLD,NEW)):
        p=Path('data/maps')/name/'map.json'
        current=json.loads((ROOT/p).read_text());before=json.loads(head(p))
        assert current=={**before,'layout':new_id}
        record=next(item for item in layouts if item['id']==new_id)
        original=next(item for item in layouts if item['id']==old_id)
        assert (record['width'],record['height'])==(w,h)
        assert record['primary_tileset']==original['primary_tileset']=='gTileset_General'
        assert record['secondary_tileset']=='gTileset_AraunaGrutaVozes'+suffix
        old=words(ROOT/original['blockdata_filepath'])
        new=words(ROOT/record['blockdata_filepath'])
        assert len(old)==len(new)==w*h
        change=[]
        for i,(a,b) in enumerate(zip(old,new)):
            if a==b:continue
            x,y=i%w,i//w
            src,dest=a&1023,b&1023
            assert (a^b)&~1023==0, (name,x,y,'collision/elevation changed')
            assert BASE<=dest<=BASE+7
            assert (src,dest-BASE) in ((529,0),(513,1),(529,2),(513,3),
                                       (529,4),(529,5),(529,6),(529,7)),(name,x,y,src,dest)
            change.append((x,y))
        occupied={(int(obj['x']),int(obj['y']))
                  for group in ('warp_events','object_events','coord_events','bg_events')
                  for obj in current[group]}
        assert not occupied.intersection(change), (name,'event metatile replaced')
        assert len(current['warp_events'])==len(before['warp_events'])
        assert (ROOT/record['border_filepath']).read_bytes()==(ROOT/original['border_filepath']).read_bytes()
        assert 5<=len(change)<=30 or level==3 and len(change)==1, (name,len(change))
        if level==3:assert new[9*w+7]&1023==BASE+3
        else:
            px,py=((25,3),(13,5),(20,3))[level]
            assert [new[(py+dy)*w+px+dx]&1023 for dy in (0,1) for dx in (0,1)]==list(range(BASE+4,BASE+8))
        secondary=ROOT/'data/tilesets/secondary'/('arauna_gruta_vozes_'+suffix.lower())
        assert Image.open(secondary/'tiles.png').size==(128,256)
        meta=words(secondary/'metatiles.bin');attrs=words(secondary/'metatile_attributes.bin')
        assert meta[:len(baseline_meta)]==baseline_meta
        assert attrs[:len(baseline_attrs)]==baseline_attrs
        assert len(attrs)==422 and len(meta)==422*8
        for part in range(8):
            src=(529,513,529,513,529,529,529,529)[part]
            assert attrs[414+part]==baseline_attrs[src-512]
            entries=meta[(414+part)*8:(415+part)*8]
            assert entries[:4]==baseline_meta[(src-512)*8:(src-512)*8+4]
            start=(0x3e0+part*4) if part<4 else (0x3f0+(part-4)*4)
            assert [x&1023 for x in entries[4:]]==list(range(start,start+4))
            assert all(x>>12==11 for x in entries[4:])
        results[name]={'cells_changed':len(change),'warps':len(current['warp_events']),
                       'objects':len(current['object_events']),'background_events':len(current['bg_events'])}
    print(json.dumps({'status':'PASS','levels':results,'collision_and_events_preserved':True},indent=2))


if __name__=='__main__':main()
