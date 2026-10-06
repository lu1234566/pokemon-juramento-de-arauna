#!/usr/bin/env python3
"""Audit event/grid identity against an explicit base and native bank limits."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from PIL import Image
from bancos_nativos import resolve_bank
from build_campanha_interiores_v1 import ROOT, BASE, MAPS, SPECS
from render_native_map import Renderer, render_map, words
from check_interiors_native_encoding_v1 import pack_tiles, unpack_tiles


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--base',type=Path,required=True,help='Clean checkout of 258195026b')
    ap.add_argument('--output',type=Path,default=ROOT/'review/campanha_interiores_v1/validation.json')
    args=ap.parse_args(); base=args.base.resolve()
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
    old_node=json.loads((base/'data/layouts/layouts.json').read_text())
    new_node=json.loads((ROOT/'data/layouts/layouts.json').read_text())
    old={l['id']:l for l in old_node['layouts']};new={l['id']:l for l in new_node['layouts']}
    assert all(new[k]==v for k,v in old.items()),'An existing layout changed'
    assert len(new)==len(old)+7
    headers=(ROOT/'src/data/tilesets/headers.h').read_text()
    report={'status':'PASS','base_commit':BASE,'maps':{},'banks':{},'unchanged_protected_files':0}
    accepted={f'data/maps/{name}/map.json' for name in MAPS}
    # Includes every old map/grid/script, all original graphics banks and
    # engine files. Only the explicitly scoped map JSONs and registrations
    # are permitted to differ. This covers shared-bank users by byte identity.
    tracked=subprocess.check_output(['git','ls-files','data/maps','data/layouts','data/tilesets','src','include'],cwd=base,text=True).splitlines()
    accepted |= {'data/layouts/layouts.json', 'src/data/tilesets/graphics.h','src/data/tilesets/metatiles.h','src/data/tilesets/headers.h'}
    for name in tracked:
        if name not in accepted:
            assert (base/name).read_bytes()==(ROOT/name).read_bytes(),name
            report['unchanged_protected_files']+=1
    assert old_node['layouts_table_label']==new_node['layouts_table_label']
    for name,(lid,key) in MAPS.items():
        p=Path('data/maps')/name/'map.json'
        before=json.loads((base/p).read_text()); after=json.loads((ROOT/p).read_text())
        lid_new=after.pop('layout'); before.pop('layout'); assert before==after,name
        a=old[lid];b=new[lid_new]
        assert (a['width'],a['height'],a['primary_tileset'])==(b['width'],b['height'],b['primary_tileset'])
        for field in ['blockdata_filepath','border_filepath']:
            assert (base/a[field]).read_bytes()==(ROOT/b[field]).read_bytes(),(name,field)
        ra=Renderer(resolve_bank(base,a['primary_tileset']),resolve_bank(base,a['secondary_tileset']))
        rb=Renderer(resolve_bank(ROOT,b['primary_tileset']),resolve_bank(ROOT,b['secondary_tileset']))
        assert words(ra.secondary/'metatile_attributes.bin')==words(rb.secondary/'metatile_attributes.bin')
        cells=words(ROOT/b['blockdata_filepath'])
        assert len(cells)==b['width']*b['height']
        assert not after['connections'],'This delivery must not affect a connection cache'
        changed=sum(ra.metatile(v&1023).tobytes()!=rb.metatile(v&1023).tobytes() for v in cells)
        assert changed>0,name
        report['maps'][name]={'cells':len(cells),'changed_visual_cells':changed,'grid_border_identical':True,'events_scripts_weather_identical':True,'behavior_collision_elevation_identical':True,'warps':len(after['warp_events']),'objects':len(after['object_events'])}
    for key,(source,symbol,style) in SPECS.items():
        original=base/'data/tilesets/secondary'/source
        target=resolve_bank(ROOT,'gTileset_'+symbol)
        im=Image.open(target/'tiles.png'); assert im.mode=='P' and max(im.getdata())<=15
        packed=pack_tiles(im);assert unpack_tiles(packed,im.size)==im.tobytes()
        assert len(packed)<=512*32
        entries=words(target/'metatiles.bin');attrs=words(target/'metatile_attributes.bin')
        assert len(entries)==len(attrs)*8 and len(attrs)<=512
        assert all(e>>12<=12 for e in entries)
        assert (target/'metatile_attributes.bin').read_bytes()==(original/'metatile_attributes.bin').read_bytes()
        definition=re.search(r'const struct Tileset gTileset_'+symbol+r' =\s*\{(.*?)\};',headers,re.S)[1]
        assert '.callback = NULL' in definition
        report['banks'][key]={'4bpp_roundtrip':True,'tiles':len(packed)//32,'metatiles':len(attrs),'max_palette':max(e>>12 for e in entries),'attributes_identical':True,'sha256_4bpp':hashlib.sha256(packed).hexdigest()}
    # These IDs are used by the native moving/opening truck sequence rather
    # than just the map.bin. Exact engine and script identity is checked above.
    bank=resolve_bank(ROOT,'gTileset_AraunaCargaV1')
    attrs=words(bank/'metatile_attributes.bin')
    old_attrs=words(base/'data/tilesets/secondary/inside_of_truck/metatile_attributes.bin')
    for mid in [0x20d,0x215,0x21d,0x208,0x210,0x218]: assert attrs[mid-512]==old_attrs[mid-512]
    report['truck_runtime_door_ids_preserved']=True
    report['cells_checked']=sum(m['cells'] for m in report['maps'].values())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
