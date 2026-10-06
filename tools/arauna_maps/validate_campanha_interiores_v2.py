#!/usr/bin/env python3
"""Independent functional identity and compact bank validation against V1."""
import argparse,json,subprocess,re
from pathlib import Path
from PIL import Image
from bancos_nativos import resolve_bank
from render_native_map import words,Renderer
from check_interiors_native_encoding_v1 import pack_tiles,unpack_tiles
from build_campanha_interiores_v1 import MAPS,SPECS
ROOT=Path(__file__).resolve().parents[2]
BASE='d561ab72aeb1c98ac72b0dd6661510effaa7362d'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);ap.add_argument('--output',type=Path,default=ROOT/'review/campanha_interiores_v2/validation.json');a=ap.parse_args();base=a.base.resolve()
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
 before={l['id']:l for l in json.loads((base/'data/layouts/layouts.json').read_text())['layouts']};after={l['id']:l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
 assert all(after[k]==v for k,v in before.items()) and len(after)==len(before)+7
 accepted={f'data/maps/{n}/map.json' for n in MAPS}|{'data/layouts/layouts.json'}|{f'src/data/tilesets/{n}.h' for n in ('graphics','metatiles','headers')}|{'graphics/object_events/pics/misc/moving_box.png','graphics/object_events/palettes/moving_box.pal'}
 report={'status':'PASS','base_commit':BASE,'maps':{},'banks':{},'protected_files_unchanged':0}
 files=subprocess.check_output(['git','ls-files','data','src','include','graphics'],cwd=base,text=True).splitlines()
 for p in files:
  if p not in accepted:
   assert (base/p).read_bytes()==(ROOT/p).read_bytes(),p
   report['protected_files_unchanged']+=1
 banks=set()
 for name in MAPS:
  path=Path('data/maps')/name/'map.json';m=json.loads((ROOT/path).read_text());old=json.loads((base/path).read_text());l=after[m.pop('layout')];o=before[old.pop('layout')];assert m==old,name
  assert (l['width'],l['height'])==(o['width'],o['height']) and m['connections'] is None
  for field in ('blockdata_filepath','border_filepath'):assert (ROOT/l[field]).read_bytes()==(base/o[field]).read_bytes()
  p=resolve_bank(ROOT,l['primary_tileset']);s=resolve_bank(ROOT,l['secondary_tileset']);r=Renderer(p,s)
  op=resolve_bank(base,o['primary_tileset']);os=resolve_bank(base,o['secondary_tileset']);oldr=Renderer(op,os)
  pa=words(p/'metatile_attributes.bin');sa=words(s/'metatile_attributes.bin');opa=words(op/'metatile_attributes.bin');osa=words(os/'metatile_attributes.bin')
  cells=words(ROOT/l['blockdata_filepath'])+words(ROOT/l['border_filepath'])
  for raw in cells:
   mid=raw&1023;assert (pa[mid] if mid<512 else sa[mid-512])==(opa[mid] if mid<512 else osa[mid-512])
   table=r.primary_metatiles if mid<512 else r.secondary_metatiles;local=mid if mid<512 else mid-512
   for entry in table[local*8:local*8+8]:assert r._tile(entry&1023) is not None,(name,mid,entry)
  assert sa==osa,name
  for raw in words(ROOT/l['border_filepath']):assert r.metatile(raw&1023).tobytes()==oldr.metatile(raw&1023).tobytes(),(name,'outside backdrop changed')
  report['maps'][name]={'grid_cells':l['width']*l['height'],'grid_border_collision_elevation_behavior_identical':True,'events_scripts_connections_weather_identical':True}
  banks.add(s)
  if name!='InsideOfTruck':banks.add(p)
 for bank in sorted(banks):
  im=Image.open(bank/'tiles.png');assert im.mode=='P' and max(im.getdata())<=15
  raw=pack_tiles(im);assert unpack_tiles(raw,im.size)==im.tobytes() and len(raw)<=512*32
  meta=words(bank/'metatiles.bin');attrs=words(bank/'metatile_attributes.bin');assert len(meta)==len(attrs)*8 and len(attrs)<=512
  assert max(e>>12 for e in meta)<=12
  for e in meta:
   tid=e&1023
   if bank.parent.name=='secondary':assert 512<=tid<992 and tid-512<len(raw)//32
   else:assert tid<len(raw)//32
  report['banks'][str(bank.relative_to(ROOT))]={'4bpp_roundtrip':True,'tiles_with_padding':len(raw)//32,'max_palette':max(e>>12 for e in meta),'safe_static_slots':True}
 # PC animation is implemented by the shared field special using IDs 4 and 5.
 primary=ROOT/'data/tilesets/primary/arauna_campanha_base_v2'
 assert words(primary/'metatile_attributes.bin')[:8]==words(base/'data/tilesets/primary/building/metatile_attributes.bin')[:8]
 meta=words(primary/'metatiles.bin');assert meta[4*8:5*8]!=meta[5*8:6*8]
 truck=resolve_bank(ROOT,after[json.loads((ROOT/'data/maps/InsideOfTruck/map.json').read_text())['layout']]['secondary_tileset']);attrs=words(truck/'metatile_attributes.bin');old=words(base/'data/tilesets/secondary/inside_of_truck/metatile_attributes.bin')
 for mid in (0x20d,0x215,0x21d,0x208,0x210,0x218):assert attrs[mid-512]==old[mid-512]
 sprite=Image.open(ROOT/'graphics/object_events/pics/misc/moving_box.png');assert sprite.size==(16,16) and sprite.mode=='P' and max(sprite.getdata())<=15
 users=[p.parent.name for p in (ROOT/'data/maps').glob('*/map.json') if 'OBJ_EVENT_GFX_MOVING_BOX' in p.read_text()];assert users==['InsideOfTruck']
 report['truck_door_ids_pc_states_and_box_geometry_preserved']=True;report['cells_checked']=sum(m['grid_cells'] for m in report['maps'].values())
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
