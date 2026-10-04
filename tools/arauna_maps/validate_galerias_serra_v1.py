#!/usr/bin/env python3
"""Validate the Rusturf Tunnel mining conversion and story events."""
import json,struct,subprocess
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
W,H=36,24;ID='LAYOUT_ARAUNA_GALERIAS_SERRA_V1'
def words(path):
    b=path.read_bytes();return struct.unpack('<%dH'%(len(b)//2),b)
def main():
    baseline=json.loads(subprocess.check_output(['git','show','HEAD:data/maps/RusturfTunnel/map.json'],cwd=ROOT))
    event=json.loads((ROOT/'data/maps/RusturfTunnel/map.json').read_text())
    assert {**event,'layout':baseline['layout']}==baseline and event['layout']==ID
    layout=next(v for v in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts'] if v['id']==ID)
    assert (layout['width'],layout['height'])==(W,H)
    assert (layout['primary_tileset'],layout['secondary_tileset'])==('gTileset_AraunaRochaMina','gTileset_AraunaGaleriasSerra')
    old=words(ROOT/'data/layouts/RusturfTunnel/map.bin');new=words(ROOT/layout['blockdata_filepath']);assert len(old)==len(new)==W*H
    change={}
    for i,(a,b) in enumerate(zip(old,new)):
        if a==b:continue
        x,y=i%W,i//W;assert (a^b)&~1023==0
        pair=(a&1023,b&1023)
        assert pair in ((0x211,0x253),(0x219,0x254),(0x201,0x255)),(x,y,pair)
        change.setdefault(pair,[]).append((x,y))
    assert tuple(len(change.get(pair,[])) for pair in ((0x211,0x253),(0x219,0x254),(0x201,0x255)))==(5,18,4)
    assert change[(0x201,0x255)]==[(x,9) for x in range(4,8)]
    for key in ('warp_events','object_events','coord_events','bg_events'):
        for obj in event[key]:
            i=obj['y']*W+obj['x'];assert old[i]==new[i]
    assert len(event['warp_events'])==3 and len(event['coord_events'])==5
    assert new[:2*W]==old[:2*W] and new[-2*W:]==old[-2*W:]
    assert all(new[y*W:y*W+3]==old[y*W:y*W+3] and new[y*W+W-3:y*W+W]==old[y*W+W-3:y*W+W] for y in range(H))
    assert (ROOT/layout['border_filepath']).read_bytes()==(ROOT/'data/layouts/RusturfTunnel/border.bin').read_bytes()
    secondary=ROOT/'data/tilesets/secondary/arauna_galerias_serra'
    attrs=words(secondary/'metatile_attributes.bin');original_attrs=words(ROOT/'data/tilesets/secondary/rusturf_tunnel/metatile_attributes.bin')
    assert attrs[:len(original_attrs)]==original_attrs and attrs[-3:]==tuple(original_attrs[i-512] for i in (0x211,0x219,0x201))
    meta=words(secondary/'metatiles.bin');original=words(ROOT/'data/tilesets/secondary/rusturf_tunnel/metatiles.bin')
    assert meta[:len(original)]==original
    for k,start in enumerate((0x3f8,0x3fc,0x3fc)):
        entries=meta[(0x253+k-512)*8:(0x254+k-512)*8]
        assert [v&1023 for v in entries[4:]]==list(range(start,start+4))
        assert all(v>>12==9 for v in entries[4:])
    assert Image.open(secondary/'tiles.png').size==(128,256)
    print(json.dumps({'status':'PASS','wooden_supports':5,'rail_cells':22,'warps_objects_triggers_preserved':True},indent=2))
if __name__=='__main__':main()
