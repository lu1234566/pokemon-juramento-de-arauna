#!/usr/bin/env python3
"""Validate Fiery Path's thermal landmarks and preserved event footprint."""
import json,struct,subprocess
from pathlib import Path
from PIL import Image
from build_trilha_de_brasa_v1 import ROOT,SOURCE,TARGET,ID,W,H,BASE

def words(path):
    raw=path.read_bytes();return struct.unpack('<%dH'%(len(raw)//2),raw)

def main():
    before=json.loads(subprocess.check_output(['git','show','HEAD:data/maps/FieryPath/map.json'],cwd=ROOT))
    event=json.loads((ROOT/'data/maps/FieryPath/map.json').read_text())
    assert event=={**before,'layout':ID}
    layouts=json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']
    old=next(r for r in layouts if r['id']=='LAYOUT_FIERY_PATH')
    new=next(r for r in layouts if r['id']==ID)
    assert (new['width'],new['height'])==(W,H)
    assert (new['primary_tileset'],new['secondary_tileset'])==('gTileset_General','gTileset_AraunaTrilhaBrasa')
    a=words(ROOT/old['blockdata_filepath']);b=words(ROOT/new['blockdata_filepath'])
    assert len(a)==len(b)==W*H
    changes=[];counts={n:0 for n in range(6)}
    for i,(v,t) in enumerate(zip(a,b)):
        if v==t:continue
        x,y=i%W,i//W;src,dest=v&1023,t&1023
        assert (v^t)&~1023==0,(x,y,'collision/elevation changed')
        assert BASE<=dest<BASE+6 and src==(776 if dest-BASE==1 else 625),(x,y,src,dest)
        changes.append((x,y));counts[dest-BASE]+=1
    assert counts[0]==8 and counts[1]==3 and [counts[i] for i in range(2,6)]==[2]*4,counts
    for px,py in ((24,11),(13,26)):
        assert [b[(py+dy)*W+px+dx]&1023 for dy in (0,1) for dx in (0,1)]==list(range(BASE+2,BASE+6))
    occupied={(int(e['x']),int(e['y'])) for key in ('warp_events','object_events','coord_events','bg_events') for e in event[key]}
    assert not occupied.intersection(changes)
    assert (ROOT/old['border_filepath']).read_bytes()==(ROOT/new['border_filepath']).read_bytes()
    original_meta=words(SOURCE/'metatiles.bin');original_attrs=words(SOURCE/'metatile_attributes.bin')
    meta=words(TARGET/'metatiles.bin');attrs=words(TARGET/'metatile_attributes.bin')
    assert len(meta)==447*8 and len(attrs)==447
    assert meta[:len(original_meta)]==original_meta and attrs[:len(original_attrs)]==original_attrs
    for part,src in enumerate((625,776,625,625,625,625)):
        assert attrs[441+part]==original_attrs[src-512]
        entries=meta[(441+part)*8:(442+part)*8]
        assert entries[:4]==original_meta[(src-512)*8:(src-512)*8+4]
        start=(0x3f8+part*4) if part<2 else (0x3e0+(part-2)*4)
        assert [v&1023 for v in entries[4:]]==list(range(start,start+4))
        assert all(v>>12==6 for v in entries[4:])
    assert Image.open(TARGET/'tiles.png').size==(128,256)
    assert len(event['warp_events'])==2 and len(event['object_events'])==10
    print(json.dumps({'status':'PASS','embers':8,'vents':3,'magma_pockets':2,
                      'warps_objects_and_collision_preserved':True},indent=2))

if __name__=='__main__':main()
