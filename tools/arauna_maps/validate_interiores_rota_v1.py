#!/usr/bin/env python3
"""Independent identity, state coverage and native artwork checks."""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
from PIL import Image
from bancos_nativos import resolve_bank, bank_words
from render_native_map import Renderer, words
from check_interiors_native_encoding_v1 import pack_tiles, unpack_tiles

ROOT=Path(__file__).resolve().parents[2]
BASE='14e56ecd6e9653c67f2ca8a111c8fabdeddd3e2f'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True)
 ap.add_argument('--output',type=Path,default=ROOT/'review/interiores_rota_v1/validation.json');args=ap.parse_args();base=args.base.resolve()
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
 build=json.loads((ROOT/'review/interiores_rota_v1/build.json').read_text());names=set(build['maps'])
 before=json.loads((base/'data/layouts/layouts.json').read_text())['layouts'];after=json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts'];assert len(before)==len(after)
 old={l['id']:l for l in before};new={l['id']:l for l in after}
 owned={r['layout'] for r in build['maps'].values()}
 assert [l['id'] for l in before]==[l['id'] for l in after],'layout IDs reordered'
 for a,b in zip(before,after):
  if a['id'] in owned:
   assert {k:v for k,v in a.items() if k not in ('primary_tileset','secondary_tileset')}=={k:v for k,v in b.items() if k not in ('primary_tileset','secondary_tileset')}
  else:assert a==b,a['id']
 accepted={'data/layouts/layouts.json'}|{f'src/data/tilesets/{n}.h' for n in ('graphics','metatiles','headers')}
 report={'status':'PASS','base_commit':BASE,'active_maps':len(names),'existing_layout_count':len(old),'layout_ids_and_order_preserved':True,'protected_files_unchanged':0,'maps':{},'banks':{}}
 for rel in subprocess.check_output(['git','ls-files','data','src','include','graphics'],cwd=base,text=True).splitlines():
  if rel in accepted:continue
  assert (ROOT/rel).read_bytes()==(base/rel).read_bytes(),rel
  report['protected_files_unchanged']+=1
 # All event/map JSONs and engine sources are protected above. Original
 # banks are untouched; the three C tables only append this registration.
 for filename in ('graphics.h','metatiles.h','headers.h'):
  rel='src/data/tilesets/'+filename;text=(ROOT/rel).read_text();text=re.sub(r'\n*// INTERIORES_ROTA_V1_BEGIN\n.*?// INTERIORES_ROTA_V1_END\n','',text,flags=re.S)
  assert text.rstrip()==(base/rel).read_text().rstrip(),rel
 banks=set();total=0;script_ids=set();labels=dict((n,int(v,16)) for n,v in re.findall(r'#define (METATILE_\w+)\s+(0x[0-9a-fA-F]+)',(ROOT/'include/constants/metatile_labels.h').read_text()))
 for name in sorted(names):
  m=json.loads((ROOT/'data/maps'/name/'map.json').read_text());l=new[m['layout']];o=old[m['layout']]
  assert not m['connections'],name
  r=Renderer(resolve_bank(ROOT,l['primary_tileset']),resolve_bank(ROOT,l['secondary_tileset']));br=Renderer(resolve_bank(base,o['primary_tileset']),resolve_bank(base,o['secondary_tileset']))
  pa=words(r.primary/'metatile_attributes.bin');opa=words(br.primary/'metatile_attributes.bin');sa=words(r.secondary/'metatile_attributes.bin');osa=words(br.secondary/'metatile_attributes.bin');assert sa==osa,name
  assert pa[:len(opa)]==opa,name
  grid=words(ROOT/l['blockdata_filepath']);border=words(ROOT/l['border_filepath']);assert grid==words(base/o['blockdata_filepath']) and border==words(base/o['border_filepath'])
  for raw in grid+border:
   mid=raw&1023;assert bank_words(r,mid,True)==bank_words(br,mid,True),(name,mid)
   entries=bank_words(r,mid)
   # Every lower layer is opaque; upper index zero is intentional transparency.
   for entry in entries[:4]:
    tile=r._tile(entry&1023);assert tile is not None and min(tile.getdata())>0,(name,hex(mid),'transparent floor')
   assert r.metatile(mid).getextrema()[3]==(255,255),(name,hex(mid),'alpha hole')
  required=set()
  script=(ROOT/'data/maps'/name/'scripts.inc').read_text()
  for token in re.findall(r'^\s*setmetatile\s+[^,]+,\s*[^,]+,\s*(METATILE_\w+|0x[0-9a-fA-F]+|\d+)\s*,',script,re.M):
   mid=labels[token] if token.startswith('METATILE_') else int(token,0);required.add(mid)
   assert bank_words(r,mid,True)==bank_words(br,mid,True),(name,'script state behavior',token)
   assert any(r.metatile(mid).getchannel('A').getdata()),(name,'blank script state',token)
   if mid>=512:assert mid in build['banks'][build['maps'][name]['bank']]['drawn_ids'],(name,'unmapped state',token)
  script_ids.update(required);total+=len(grid)
  banks.add(r.secondary)
  if l['primary_tileset']=='gTileset_AraunaRotaBaseV1':banks.add(r.primary)
  report['maps'][name]={'cells':len(grid),'script_state_ids':sorted(required),'grid_border_collision_elevation_behavior_identical':True,'events_warps_scripts_weather_encounters_identical':True,'all_grid_bottom_layers_opaque':True}
 for path in sorted(banks):
  im=Image.open(path/'tiles.png');assert im.mode=='P' and max(im.getdata())<=15
  raw=pack_tiles(im);assert unpack_tiles(raw,im.size)==im.tobytes()
  entries=words(path/'metatiles.bin');attrs=words(path/'metatile_attributes.bin');assert len(entries)==8*len(attrs) and len(attrs)<=512
  for entry in entries:
   tid=entry&1023
   assert entry>>12<=12,(path,entry)
   if path.parent.name=='secondary':assert 512<=tid<992 and tid-512<len(raw)//32,(path,entry)
   else:assert tid<432 and tid<len(raw)//32,(path,entry)
  report['banks'][str(path.relative_to(ROOT))]={'4bpp_roundtrip':True,'tiles_with_padding':len(raw)//32,'attributes_preserved':True,'safe_static_slots_and_palettes':True}
 assert len(banks)==15 and len(names)==25
 primary=ROOT/'data/tilesets/primary/arauna_rota_base_v1'
 assert words(primary/'metatile_attributes.bin')==words(base/'data/tilesets/primary/building/metatile_attributes.bin')
 pc=Renderer(primary,ROOT/'data/tilesets/secondary/arauna_rota_safari_v1')
 for a,b in ((2,3),(4,5)):assert pc.metatile(a).tobytes()!=pc.metatile(b).tobytes(),('PC/TV states',a,b)
 # Explicit runtime pairs must remain visibly distinct after quantization.
 puzzle=next(r for r in build['maps'].values() if r['bank']=='enigmas');l=new[puzzle['layout']];r=Renderer(resolve_bank(ROOT,l['primary_tileset']),resolve_bank(ROOT,l['secondary_tileset']))
 pairs=[(0x258,0x259),(0x23e,0x23f),(0x238,0x248),(0x23b,0x24b),(0x260,0x261),(0x262,0x263)]
 for a,b in pairs:assert r.metatile(a).tobytes()!=r.metatile(b).tobytes(),(a,b,'states look equal')
 report.update(cells_checked=total,unique_script_state_ids_checked=len(script_ids),distinct_runtime_pairs=len(pairs),save_continue_warp_code_unchanged=True,all_original_tilesets_unchanged=True,all_exterior_grids_banks_and_connections_unchanged=True,prototype_flower_shop_untouched=True)
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('maps','banks')},indent=2))

if __name__=='__main__':main()
