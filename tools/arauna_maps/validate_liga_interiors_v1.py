#!/usr/bin/env python3
"""Validate native League art, events, dynamic doors and animation slots."""
import json,subprocess
from PIL import Image
from build_liga_interiors_v1 import ROOT,MAPS,SPECS,ROOMS,ELITE_BASE,HALL_BASE,TABLET_BASE,words,source,target,layout_id

def main():
 layouts={r['id']:r for r in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
 changed_art={v+48*k for k in range(4) for v in (537,538,539,545,546,547,553,554,555,561,562,563)}
 for symbol in SPECS:
  src,dst=source(symbol),target(symbol);old_meta=words(src/'metatiles.bin');meta=words(dst/'metatiles.bin');old_attr=words(src/'metatile_attributes.bin');attrs=words(dst/'metatile_attributes.bin')
  assert attrs[:len(old_attr)]==old_attr
  count={'AraunaLigaPedra':len(old_attr),'AraunaLigaVozes':434,'AraunaLigaHall':248,'AraunaLigaMemoria':256}[symbol]
  assert len(attrs)==count and len(meta)==8*count
  for i in range(len(old_attr)):
   if symbol=='AraunaLigaVozes' and i+512 in changed_art:continue
   assert meta[i*8:i*8+8]==old_meta[i*8:i*8+8],(symbol,i+512)
  assert Image.open(dst/'tiles.png').width==128 and Image.open(dst/'tiles.png').height<=256
  original_used={x&1023 for x in old_meta}
  custom_entries=[]
  if symbol=='AraunaLigaVozes':
   for id in changed_art:custom_entries+=meta[(id-512)*8+4:(id-512)*8+8]
   for i in range(len(old_attr),count):custom_entries+=meta[i*8+4:i*8+8]
  if symbol=='AraunaLigaHall':
   for i in range(len(old_attr),count):custom_entries+=meta[i*8+4:i*8+8]
  custom={x&1023 for x in custom_entries}
  assert not custom.intersection(original_used)
  assert not custom.intersection({992,993,994,995,1016})
  if symbol in ('AraunaLigaPedra','AraunaLigaMemoria'):
   assert (src/'tiles.png').read_bytes()==(dst/'tiles.png').read_bytes()
 report={};warps=objects=changed_total=0
 for name in MAPS:
  rel=f'data/maps/{name}/map.json';baseline=json.loads(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT));event=json.loads((ROOT/rel).read_text())
  assert event=={**baseline,'layout':layout_id(name)}
  old,new=layouts[baseline['layout']],layouts[layout_id(name)]
  assert (new['width'],new['height'])==(old['width'],old['height'])
  assert new['primary_tileset']=='gTileset_AraunaLigaPedra'
  symbol=new['secondary_tileset'].removeprefix('gTileset_');assert symbol in SPECS
  a,b=words(ROOT/old['blockdata_filepath']),words(ROOT/new['blockdata_filepath']);assert len(a)==len(b)==old['width']*old['height']
  old_attrs=words(source(symbol)/'metatile_attributes.bin');new_attrs=words(target(symbol)/'metatile_attributes.bin');w=old['width'];changed=[]
  for i,(v,t) in enumerate(zip(a,b)):
   if v==t:continue
   x,y=i%w,i//w;assert (v^t)&~1023==0
   src,dst=v&1023,t&1023
   assert old_attrs[src-512]==new_attrs[dst-512],(name,x,y,'behavior changed')
   if name=='EverGrandeCity_PokemonLeague_1F':assert dst==HALL_BASE+(y-5)*4+x-8 and 8<=x<12 and 5<=y<9
   elif name=='EverGrandeCity_ChampionsRoom':assert dst==ELITE_BASE+(y-6)*3+x-5 and 5<=x<8 and 6<=y<8
   else:
    assert name in ROOMS and x in (0,1,11,12) and 4<=y<10
    k=ROOMS.index(name);side=int(x>=11);assert dst==TABLET_BASE+k*24+side*12+(y-4)*2+x-(11 if side else 0)
   changed.append((x,y))
  occupied={(int(e['x']),int(e['y'])) for group in ('warp_events','object_events','coord_events','bg_events') for e in event[group]};assert not occupied.intersection(changed)
  assert (ROOT/old['border_filepath']).read_bytes()==(ROOT/new['border_filepath']).read_bytes()
  scripts=f'data/maps/{name}/scripts.inc';assert (ROOT/scripts).read_bytes()==subprocess.check_output(['git','show','HEAD:'+scripts],cwd=ROOT)
  warps+=len(event['warp_events']);objects+=len(event['object_events']);changed_total+=len(changed)
  report[name]={'changed_cells':len(changed),'warps':len(event['warp_events'])}
 assert warps==43 and objects==24 and changed_total==118
 print(json.dumps({'status':'PASS','maps':report,'warps':warps,'objects':objects,'events_behaviors_scripts_preserved':True,'animation_slots_preserved':True},indent=2))

if __name__=='__main__':main()
