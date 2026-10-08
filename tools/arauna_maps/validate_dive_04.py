#!/usr/bin/env python3
"""Production-C draw/warp checks and complete preservation audit."""
import argparse,hashlib,json,re,subprocess,tempfile
from pathlib import Path
from PIL import Image
from dive_04_common import BASE,ROOT,OUT,NAMES,inventory,renderer,strip_landmark_hook,SURFACE_FILES
from dive_04_c_checks import selector,dive,fog
from bancos_nativos import resolve_bank,bank_words
from render_native_map import words,indexed_tiles,palette
import puzzles_cavernas_03b as puzzles

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);a=ap.parse_args();base=a.base.resolve()
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
 contract=json.loads((OUT/'functional_contract.json').read_text());build=json.loads((OUT/'build.json').read_text())
 for rel,sha in {**contract['protected_hashes'],**contract['dependency_hashes']}.items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==sha,('protected',rel)
 oldnode,oldls,maps=inventory(base);node,ls,_=inventory(ROOT);assert len(node['layouts'])==len(oldnode['layouts'])==744
 targets={maps[n]['layout'] for n in NAMES}
 for old,new in zip(oldnode['layouts'],node['layouts']):
  if old['id'] in targets:assert {k:v for k,v in old.items() if k!='secondary_tileset'}=={k:v for k,v in new.items() if k!='secondary_tileset'}
  else:assert old==new
 for rel in ('src/data/tilesets/graphics.h','src/data/tilesets/metatiles.h','src/data/tilesets/headers.h'):
  stripped=re.sub(r'\n*// DIVE_04_BEGIN\n.*?// DIVE_04_END\n','\n',(ROOT/rel).read_text(),flags=re.S);assert stripped.rstrip()==(base/rel).read_text().rstrip()
 assert strip_landmark_hook((ROOT/'src/arauna_cave_visuals.c').read_text())==(base/'src/arauna_cave_visuals.c').read_text()
 # Reverse only the tightly scoped fog rendering change, then compare whole file.
 oldfog=(base/'src/field_weather_effect.c').read_text();newfog=(ROOT/'src/field_weather_effect.c').read_text()
 newfog=newfog.replace('#include "constants/maps.h"\n','')
 match=re.search(r'        if \(gWeatherPtr->currWeather == WEATHER_FOG_HORIZONTAL\)\n        \{\n            // Arauna:.*?\n        \}',newfog,re.S);assert match
 newfog=newfog[:match.start()]+'        if (gWeatherPtr->currWeather == WEATHER_FOG_HORIZONTAL)\n            Weather_SetTargetBlendCoeffs(12, 8, 3);'+newfog[match.end():]
 assert newfog==oldfog,'Unrelated weather lifecycle change'
 oldh=(base/'src/data/arauna_cave_visuals_v2.h').read_text();newh=(ROOT/'src/data/arauna_cave_visuals_v2.h').read_text()
 stripped=re.sub(r'^static const u16 sVisual_Underwater_.*?\n','',newh,flags=re.M);stripped=re.sub(r'^    \{\d+, sVisual_Underwater_.*?\n','',stripped,flags=re.M);assert stripped==oldh
 reports={};cells=fallbacks=legacy=transitions=animations=0;bankreports=[]
 with tempfile.TemporaryDirectory() as tmp:
  compiled,indices=selector(Path(tmp)/'selector');dispatcher,divechecks=dive(Path(tmp)/'dive');fogchecks=fog(Path(tmp)/'fog')
  puzzlechecks=puzzles.run(Path(tmp)/'puzzles')
  for idx,name in re.findall(r'\{(\d+), sVisual_(\w+)\}',oldh):
   l=node['layouts'][int(idx)];g=words(ROOT/l['blockdata_filepath']);expected=words(base/re.search(r'sVisual_'+name+r'\[\] = INCBIN_U16\("([^"]+)"\)',oldh)[1])
   for i,v in enumerate(g):assert compiled.probe(int(idx),i%l['width']+7,i//l['width']+7,v&1023)==expected[i];legacy+=1
  for n in NAMES:
   l=ls[maps[n]['layout']];old=oldls[l['id']];g=words(ROOT/l['blockdata_filepath']);vis=words(ROOT/build['maps'][n]['visual_grid']);idx=build['maps'][n]['layout_index'];before=renderer(base,old);after=renderer(ROOT,l);cache={};changed=0;opaque={}
   assert len(g)==len(vis)==l['width']*l['height']
   for i,v in enumerate(g):
    mid=v&1023;alias=compiled.probe(idx,i%l['width']+7,i//l['width']+7,mid);assert alias==vis[i]
    originalattr=bank_words(before,mid,True);assert bank_words(after,mid,True)==originalattr==bank_words(after,alias,True),(n,i,'full attributes')
    if alias not in opaque:
     im=after.metatile(alias);assert im.getextrema()[3]==(255,255),(n,i,'opacity');opaque[alias]=True
     assert all((e&1023)<512+after.secondary_tiles[2] or 1008<=e&1023<1012 for e in bank_words(after,alias)),(n,i,'tile range')
    pair=(mid,alias)
    if pair not in cache:cache[pair]=before.metatile(mid).tobytes()!=after.metatile(alias).tobytes()
    changed+=cache[pair];cells+=1
    for other in (mid^1,1023 if mid!=1023 else 1022):assert compiled.probe(idx,i%l['width']+7,i//l['width']+7,other)==other;fallbacks+=1
    behavior=originalattr&255;actual=bank_words(after,alias,True)&255;via=any(c['direction']=='emerge' for c in maps[n]['connections'] or [])
    want=dispatcher.probe(1,behavior,via,not via,i%l['width'],i//l['width']);dest=[dispatcher.destination(j) for j in range(4)]
    assert dispatcher.probe(1,actual,via,not via,i%l['width'],i//l['width'])==want and [dispatcher.destination(j) for j in range(4)]==dest;transitions+=1
   for x,y in ((-1,0),(0,-1),(l['width'],0),(0,l['height'])):assert compiled.probe(idx,x+7,y+7,530)==530;fallbacks+=1
   for e in maps[n]['warp_events']:assert (g[e['y']*l['width']+e['x']]&0xc00)==0,(n,'warp collision')
   reports[n]={'cells':len(g),'changed_visual_cells':changed,'warps':len(maps[n]['warp_events']),'connections':len(maps[n]['connections'] or []),'hidden_items':len([e for e in maps[n]['bg_events'] if e['type']=='hidden_item']),'native_words_events_scripts_preserved':True}
  for theme,b in build['banks'].items():
   path=ROOT/b['path'];original=base/b['source_secondary'];attrs=words(path/'metatile_attributes.bin');oldattrs=words(original/'metatile_attributes.bin');assert attrs[:len(oldattrs)]==oldattrs,'All old native metatile attributes'
   im,cols,count=indexed_tiles(path/'tiles.png');assert count<=512 and len(attrs)<=512
   meta=words(path/'metatiles.bin');assert len(meta)==len(attrs)*8 and all(e>>12<13 for e in meta)
   assert not set(b['new_tiles'])&(set(range(432,512))|set(range(992,1024)))
   pixels=list(im.getdata());packed=bytes(pixels[i]|pixels[i+1]<<4 for i in range(0,len(pixels),2));assert [v for x in packed for v in (x&15,x>>4)]==pixels
   for q in range(13):
    raw=(path/f'palettes/{q:02}.pal').read_bytes();assert raw.count(b'\n')==raw.count(b'\r\n')
    pal=palette(path/f'palettes/{q:02}.pal');assert all(c%8==0 for rgb in pal for c in rgb)
   l=next(ls[maps[n]['layout']] for n in NAMES if build['maps'][n]['theme']==theme)
   for mid in b['native_dynamic_ids']:
    frames=[renderer(ROOT,l,frame).metatile(mid).tobytes() for frame in range(4)];assert len(set(frames))>1,('kelp static',theme,mid);animations+=1
   if theme=='arquivo':assert words(path/'metatiles.bin')[(624-512)*8:(625-512)*8]==words(original/'metatiles.bin')[(624-512)*8:(625-512)*8],'Braille glyph entries'
   bankreports.append({'theme':theme,'tiles':count,'aliases':b['aliases'],'native_attributes_preserved':len(oldattrs)})
  # Surface landmarks: old attributes and every old unrelated entry/graphic stay.
  for n,key in (('Route103','altering'),('Route111','mirage')):
   l=ls[maps[n]['layout']];old=oldls[l['id']];before=renderer(base,old);after=renderer(ROOT,l);info=build['landmarks'][key]
   for kind in (0,1):
    oldpath=resolve_bank(base,old[('primary_tileset','secondary_tileset')[kind]]);newpath=resolve_bank(ROOT,l[('primary_tileset','secondary_tileset')[kind]])
    a,b=words(oldpath/'metatiles.bin'),words(newpath/'metatiles.bin');aa,bb=words(oldpath/'metatile_attributes.bin'),words(newpath/'metatile_attributes.bin')
    allowed=set(info['native_ids'] if key=='altering' and kind==0 else info.get('visual_ids',[]) if kind==1 else [])
    for mid in range(len(aa)):
     native=mid+kind*512
     if native not in allowed:assert a[mid*8:mid*8+8]==b[mid*8:mid*8+8] and aa[mid]==bb[mid],(n,native,'unrelated entry')
    oldim,oc,ot=indexed_tiles(oldpath/'tiles.png');newim,nc,nt=indexed_tiles(newpath/'tiles.png')
    for t in range(ot):
     if t+kind*512 not in info['new_tiles']:assert oldim.crop((t%oc*8,t//oc*8,t%oc*8+8,t//oc*8+8)).tobytes()==newim.crop((t%nc*8,t//nc*8,t%nc*8+8,t//nc*8+8)).tobytes(),(n,t,'existing graphic')
   g=words(ROOT/l['blockdata_filepath'])
   for i,v in enumerate(g):
    native=v&1023;alias=compiled.probe(node['layouts'].index(l),i%l['width']+7,i//l['width']+7,native)
    allowed=key=='mirage' and [i%l['width'],i//l['width']] in info['positions'] and native in info['native_ids']
    if not allowed:assert alias==native
    if key=='mirage' and not allowed:assert after.metatile(alias).tobytes()==before.metatile(native).tobytes(),(n,i,'terrain changed')
    assert bank_words(after,alias,True)==bank_words(before,native,True)
   if key=='altering':
    for mid in info['native_ids']:assert bank_words(before,mid,True)==bank_words(after,mid,True) and before.metatile(mid).tobytes()!=after.metatile(mid).tobytes()
   else:
    for idx in info['layout_indices']:
     for col,(mid,alias) in enumerate(zip(info['native_ids'],info['visual_ids'])):
      assert compiled.probe(idx,18+col+7,56+7,mid)==alias
      assert compiled.probe(idx,18+col+7,55+7,mid)==mid
      assert compiled.probe(idx,18+col+7,56+7,mid^1)==mid^1
      # Vanishing tower restores a sand ID; it must never show the new base.
      assert compiled.probe(idx,18+col+7,56+7,555)==555
  for mid in range(1024):assert compiled.unknown(7,7,mid)==mid
  # The actual tower-absent layout is all ground at these coordinates. Check
  # the whole variant, not merely a hypothetical sand replacement.
  l=node['layouts'][711];g=words(ROOT/l['blockdata_filepath']);before=renderer(base,oldnode['layouts'][711]);after=renderer(ROOT,l)
  for i,v in enumerate(g):
   mid=v&1023;alias=compiled.probe(711,i%l['width']+7,i//l['width']+7,mid);assert alias==mid
   assert before.metatile(mid).tobytes()==after.metatile(alias).tobytes(),('Mirage absent',i)
 # Every installed script endpoint is retained and listed for runtime review.
 endpoints={}
 for n in NAMES+('MarineCave_Entrance','SealedChamber_OuterRoom','Route134'):
  text=(ROOT/f'data/maps/{n}/scripts.inc').read_text()
  endpoints[n]={'fixed_commands':[line.strip() for line in text.splitlines() if re.match(r'\s*(?:setdivewarp|setdynamicwarp|setescapewarp|setwarp)\b',line)],'coordinate_conditions':[line.strip() for line in text.splitlines() if re.match(r'\s*goto_if_ne VAR_0x800[45]',line)]}
 # Exercise the 12 submarine-removal writes through the actual draw selector.
 with tempfile.TemporaryDirectory() as tmp:
  compiled,_=selector(Path(tmp));l=ls[maps['Underwater_SeafloorCavern']['layout']];idx=build['maps']['Underwater_SeafloorCavern']['layout_index'];r=renderer(ROOT,l)
  for y,mid in ((3,542),(4,552),(5,552)):
   for x in (5,6,7,8):assert compiled.probe(idx,x+7,y+7,mid)==mid and r.metatile(mid).getextrema()[3]==(255,255)
 (OUT/'endpoints.json').write_text(json.dumps(endpoints,indent=2)+'\n')
 (OUT/'puzzle_regressions.json').write_text(json.dumps(puzzlechecks,indent=2)+'\n')
 report={'status':'PASS','base_commit':BASE,'protected_gameplay_files':len(contract['protected_hashes']),'protected_dependencies':len(contract['dependency_hashes']),'maps':reports,'banks':bankreports,'actual_c_selector_cells':cells,'actual_c_fallback_cases':fallbacks,'previous_selector_cells_preserved':legacy,'actual_c_native_alias_dive_comparisons':transitions,'live_kelp_metatiles_checked':animations,'hidden_items_preserved':len(contract['items']),'surface_landmarks':build['landmarks'],'dive_c':divechecks,'fog_c':fogchecks,'real_c_puzzle_regressions':puzzlechecks['checks'],'submarine_gone_script_cells':12,'mirage_absent_layout_cells_preserved':5600,'rom_build':'pending ARM toolchain unavailable','emulator':'pending mGBA unavailable'}
 (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
