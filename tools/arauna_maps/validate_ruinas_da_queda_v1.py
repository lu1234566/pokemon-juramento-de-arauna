#!/usr/bin/env python3
"""Validate native Meteor Falls adaptation without moving story events."""
import json
import struct
import subprocess

from PIL import Image
from build_ruinas_da_queda_v1 import ROOT,NAMES,OLD,NEW,BASE,PRIMARY,SECONDARY


def words(path):
    raw=path.read_bytes();return struct.unpack('<%dH'%(len(raw)//2),raw)


def main():
    layouts=json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']
    original_secondary=ROOT/'data/tilesets/secondary/meteor_falls'
    original_primary=ROOT/'data/tilesets/primary/general'
    meta=words(SECONDARY/'metatiles.bin');attrs=words(SECONDARY/'metatile_attributes.bin')
    old_meta=words(original_secondary/'metatiles.bin')
    old_attrs=words(original_secondary/'metatile_attributes.bin')
    assert len(meta)==161*8 and len(attrs)==161
    assert meta[:len(old_meta)]==old_meta and attrs[:len(old_attrs)]==old_attrs
    for kind in range(2):
        assert attrs[159+kind]==old_attrs[513-512]
        entries=meta[(159+kind)*8:(160+kind)*8]
        assert entries[:4]==old_meta[(513-512)*8:(513-512)*8+4]
        assert [x&1023 for x in entries[4:]]==list(range(0x3f8+4*kind,0x3fc+4*kind))
        assert all(x>>12==11 for x in entries[4:])
    assert Image.open(SECONDARY/'tiles.png').size==(128,256)
    assert words(PRIMARY/'metatiles.bin')==words(original_primary/'metatiles.bin')
    assert words(PRIMARY/'metatile_attributes.bin')==words(original_primary/'metatile_attributes.bin')
    report={}
    for name,old_id,new_id in zip(NAMES,OLD,NEW):
        rel=f'data/maps/{name}/map.json'
        baseline=json.loads(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT))
        event=json.loads((ROOT/rel).read_text())
        assert event=={**baseline,'layout':new_id}
        old=next(r for r in layouts if r['id']==old_id)
        new=next(r for r in layouts if r['id']==new_id)
        w,h=old['width'],old['height']
        assert (w,h)==(new['width'],new['height'])
        assert (new['primary_tileset'],new['secondary_tileset'])==('gTileset_AraunaRochaQueda','gTileset_AraunaRuinasQueda')
        a=words(ROOT/old['blockdata_filepath']);b=words(ROOT/new['blockdata_filepath'])
        assert len(a)==len(b)==w*h
        changes=[]
        for i,(v,t) in enumerate(zip(a,b)):
            if v==t:continue
            x,y=i%w,i//w
            assert v&1023==513 and t&1023 in (BASE,BASE+1),(name,x,y,v,t)
            assert (v^t)&~1023==0,(name,x,y,'collision/elevation changed')
            changes.append((x,y))
        occupied={(int(obj['x']),int(obj['y'])) for key in ('warp_events','object_events','coord_events','bg_events') for obj in event[key]}
        assert not occupied.intersection(changes)
        assert 1<=len(changes)<=25
        assert (ROOT/old['border_filepath']).read_bytes()==(ROOT/new['border_filepath']).read_bytes()
        report[name]={'stone_marks':len(changes),'warps':len(event['warp_events']),
                      'objects':len(event['object_events'])}
    print(json.dumps({'status':'PASS','maps':report,'collision_and_events_preserved':True},indent=2))


if __name__=='__main__':main()
