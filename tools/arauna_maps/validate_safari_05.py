#!/usr/bin/env python3
"""Complete native invariants, actual-C camera/caches and Safari mechanics."""
import argparse,ctypes,hashlib,json,re,subprocess,tempfile
from pathlib import Path
from safari_05_common import BASE,ROOT,OUT,NAMES,EXTERIORS,inventory,renderer
from safari_05_c_checks import selector,safari,behavior
from native_visuals_v2 import dump,callback
from bancos_nativos import resolve_bank,bank_words
from render_native_map import words,indexed_tiles,palette
from validate_border_visuals_119_118 import compile_connections

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve()
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
 contract=json.loads((OUT/'functional_contract.json').read_text());build=json.loads((OUT/'build.json').read_text())
 for rel,h in {**contract['protected_hashes'],**contract['dependency_hashes']}.items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,('protected',rel)
 oldnode,oldls,maps=inventory(base);node,ls,_=inventory(ROOT);assert len(node['layouts'])==len(oldnode['layouts'])==744
 targets={maps[n]['layout'] for n in NAMES}
 for before,after in zip(oldnode['layouts'],node['layouts']):
  if before['id'] in targets:assert {k:v for k,v in before.items() if k not in ('primary_tileset','secondary_tileset')}=={k:v for k,v in after.items() if k not in ('primary_tileset','secondary_tileset')}
  else:assert before==after
 for rel in ('src/data/tilesets/graphics.h','src/data/tilesets/metatiles.h','src/data/tilesets/headers.h'):
  stripped=re.sub(r'\n*// SAFARI_05_BEGIN\n.*?// SAFARI_05_END\n','\n',(ROOT/rel).read_text(),flags=re.S);assert stripped.rstrip()==(base/rel).read_text().rstrip()
 reports={};cells=fallbacks=legacy=attrs=anim=predicate_comparisons=0;connections=[];hidden_dynamic=[];shape_entries=0
 bank_cache={};pixel_cache={}
 def rr(l,frame=0):
  key=l['primary_tileset'],l['secondary_tileset'],frame
  if key not in bank_cache:bank_cache[key]=renderer(ROOT,l,frame)
  return bank_cache[key]
 def pix(r,mid):
  key=id(r),mid
  if key not in pixel_cache:pixel_cache[key]=r.metatile(mid).tobytes()
  return pixel_cache[key]
 with tempfile.TemporaryDirectory() as tmp:
  folder=Path(tmp);sel,_=selector(folder/'selector');copier=compile_connections(folder/'selector');b,behavior_report=behavior(folder/'behavior');safari_report=safari(folder/'safari')
  header=(base/'src/data/arauna_cave_visuals_v2.h').read_text()
  for idx,n in re.findall(r'\{(\d+), sVisual_(\w+)\}',header):
   l=node['layouts'][int(idx)];g=words(ROOT/l['blockdata_filepath']);expected=words(base/re.search(r'sVisual_'+n+r'\[\] = INCBIN_U16\("([^"]+)"\)',header)[1])
   for i,v in enumerate(g):assert sel.probe(int(idx),i%l['width']+7,i//l['width']+7,v&1023)==expected[i];legacy+=1
  for n in NAMES:
   l=ls[maps[n]['layout']];old=oldls[l['id']];g=words(ROOT/l['blockdata_filepath']);r=rr(l);before=renderer(base,old);idx=build['maps'][n]['layout_index'];changed=0;cache={}
   assert g==words(base/old['blockdata_filepath']) and len(g)==l['width']*l['height']
   for mid in set(v&1023 for v in g)|set(v&1023 for v in words(ROOT/l['border_filepath'])):
    a=bank_words(before,mid,True);assert a==bank_words(r,mid,True),(n,mid,'full attribute')
    for j in range(7):assert b.probe(j,a&255)==b.probe(j,bank_words(r,mid,True)&255);predicate_comparisons+=1
    cache[mid]=pix(r,mid)!=before.metatile(mid).tobytes()
    if mid in build['banks'][build['maps'][n]['theme']]['redrawn_native_ids']:assert r.metatile(mid).getextrema()[3]==(255,255),(n,mid,'opacity')
    else:
     # Repacking may change tile addresses; every inherited silhouette,
     # transparency mask, flip, palette reference and layer stays identical.
     for a,z in zip(bank_words(before,mid),bank_words(r,mid)):
      assert a&~1023==z&~1023,(n,mid,'entry flags')
      ai,zi=before._tile(a&1023),r._tile(z&1023)
      assert (ai.tobytes() if ai is not None else None)==(zi.tobytes() if zi is not None else None),(n,mid,'inherited shape')
      shape_entries+=1
   for i,v in enumerate(g):
    mid=v&1023;assert sel.probe(idx,i%l['width']+7,i//l['width']+7,mid)==mid;cells+=1;changed+=cache[mid]
   for x,y in ((7,7),(6,7),(7,6),(l['width']+7,7),(7,l['height']+7)):
    for mid in range(1024):assert sel.probe(idx,x,y,mid)==mid;fallbacks+=1
   reports[n]={'cells':len(g),'changed_visual_cells':changed,'warps':len(maps[n]['warp_events']),'connections':len(maps[n]['connections'] or []),'objects':len(maps[n]['object_events']),'hidden_items':len([e for e in maps[n]['bg_events'] if e['type']=='hidden_item']),'visible_items':len([e for e in maps[n]['object_events'] if e['graphics_id']=='OBJ_EVENT_GFX_ITEM_BALL'])}
   assert changed>0,(n,'no visual change')
  # The actual engine cache functions determine donor and receiver coordinates.
  for n in EXTERIORS:
   l=ls[maps[n]['layout']]
   for c in maps[n]['connections']:
    source=next(m for m in maps.values() if m['id']==c['map']);assert source['name'] in EXTERIORS
    sl=ls[source['layout']];assert [l[k] for k in ('primary_tileset','secondary_tileset')]==[sl[k] for k in ('primary_tileset','secondary_tileset')]
    sg=words(ROOT/sl['blockdata_filepath']);buf=(ctypes.c_int*40000)();count=copier(['up','down','left','right'].index(c['direction']),l['width'],l['height'],sl['width'],sl['height'],c['offset'],buf)
    for i in range(count):
     sx,sy,rx,ry=buf[i*4:i*4+4];mid=sg[sy*sl['width']+sx]&1023
     alias=sel.probe(build['maps'][n]['layout_index'],rx,ry,mid);assert alias==mid
     for f in range(8):assert pix(rr(l,f),alias)==pix(rr(sl,f),mid);anim+=1
     assert bank_words(rr(l),alias,True)==bank_words(rr(sl),mid,True)
    connections.append({'receiver':n,'source':source['name'],'direction':c['direction'],'native_engine_cache_cells':count,'pixel_attribute_mismatches':0,'frames':8})
 bank_reports=[];animated_ids=set()
 for theme,info in build['banks'].items():
  for kind,(rel,src) in enumerate(zip(info['paths'],info['source_paths'])):
   p=ROOT/rel;old=base/src;aa=words(p/'metatile_attributes.bin');assert aa==words(old/'metatile_attributes.bin');attrs+=len(aa)
   im,row,count=indexed_tiles(p/'tiles.png');assert count<=512;meta=words(p/'metatiles.bin');assert len(meta)==len(aa)*8 and all(e>>12<13 for e in meta)
   # Independently roundtrip each 8x8 tile through GBA 4bpp byte packing.
   for i in range(count):
    pixels=list(im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8)).getdata());packed=bytes(pixels[j]|pixels[j+1]<<4 for j in range(0,64,2));assert [v for x in packed for v in (x&15,x>>4)]==pixels
   for q in range(13):
    raw=(p/f'palettes/{q:02}.pal').read_bytes();assert raw.count(b'\n')==raw.count(b'\r\n');colors=palette(p/f'palettes/{q:02}.pal');assert all(c%8==0 for rgb in colors for c in rgb)
    for rgb in colors:
     value=sum((c>>3)<<(5*j) for j,c in enumerate(rgb));assert tuple((value>>(5*j)&31)<<3 for j in range(3))==rgb
   assert not set(info['allocated_static_tiles'])&(set(range(432,512))|set(range(992,1024)))
   assert callback(ROOT,'gTileset_'+info['symbols'][kind])==info['callbacks'][kind]
   bank_reports.append({'path':rel,'tiles':count,'native_attributes_preserved':len(aa),'callback':info['callbacks'][kind]})
 if True:
  l=ls[maps[EXTERIORS[0]]['layout']];old=oldls[l['id']];before=renderer(base,old);after=rr(l)
  used={v&1023 for n in EXTERIORS for v in words(ROOT/ls[maps[n]['layout']]['blockdata_filepath'])}
  for mid in used:
   olde=bank_words(before,mid);newe=bank_words(after,mid)
   dynamic=lambda e:432<=e&1023<512 or 992<=e&1023<1024
   for a,z in zip(olde,newe):
    if dynamic(a):assert a==z,(mid,'live animation reference changed')
   if any(dynamic(e) for e in olde):
    oldframes=[renderer(base,old,f).metatile(mid).tobytes() for f in range(8)]
    frames=[pix(rr(l,f),mid) for f in range(8)]
    if len(set(oldframes))>1:assert len(set(frames))>1,(mid,'frozen animation');animated_ids.add(mid)
    else:hidden_dynamic.append(mid)
 # Endpoint data and scripts are SHA-protected; this inventory is for ROM review.
 endpoints={n:{'warps':maps[n]['warp_events'],'script_commands':[s.strip() for s in (ROOT/f'data/maps/{n}/scripts.inc').read_text().splitlines() if re.match(r'\s*(?:warp\w*|setwarp|checkmoney|removemoney|checkitem|setvar|clearflag|setflag|setobjectxyperm)\b',s)]} for n in NAMES}
 dump(OUT/'endpoints.json',endpoints)
 # Artist-authored plain ground must never replace blocked jump ledges.
 plain={1,0xd3,0xd4,0x1ce,0x1cf,0x121};trees={0x1d4,0x1d5,0x1d6,0x1d7,0x1dc,0x1dd,0x1de,0x1df,0x1e4,0x1e5,0x1e6,0x1e7}
 semantic=0
 for n in EXTERIORS:
  l=ls[maps[n]['layout']];r=rr(l)
  for v in words(ROOT/l['blockdata_filepath']):
   mid=v&1023
   if mid in plain:assert not v&0xc00 and bank_words(r,mid,True)&255==0;semantic+=1
   elif mid in trees:assert v&0xc00;semantic+=1
   elif mid==13:assert not v&0xc00 and bank_words(r,mid,True)&255==2;semantic+=1
   elif mid==0xb1:assert bank_words(r,mid,True)&255==0x10;semantic+=1
   elif mid in (0xc9,0xd1):assert bank_words(r,mid,True)&255==0x16;semantic+=1
 assert 0xd6 not in build['banks']['mata']['redrawn_native_ids'],'Jump ledge must keep its original silhouette'
 report={'status':'PASS','base_commit':BASE,'protected_gameplay_files':len(contract['protected_hashes']),'protected_dependencies':len(contract['dependency_hashes']),'maps':reports,'banks':bank_reports,'full_native_attributes_preserved':attrs,'actual_c_camera_cells':cells,'actual_c_fallback_cases':fallbacks,'prior_cavern_dive_selector_cells':legacy,'actual_c_native_behavior_comparisons':predicate_comparisons,'connections':connections,'animated_connection_cell_frames':anim,'live_animated_native_metatile_ids':sorted(animated_ids),'native_dynamic_refs_without_visible_change':hidden_dynamic,'semantic_art_collision_cells':semantic,'inherited_shape_entries_preserved':shape_entries,'safari_c':safari_report,'behavior_c':behavior_report,'rom_build':'pending: ARM compiler unavailable','emulator':'pending: mGBA unavailable'}
 dump(OUT/'validation.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ('maps','banks','connections')},indent=2))

if __name__=='__main__':main()
