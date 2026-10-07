#!/usr/bin/env python3
"""Actual-C selectors, full data invariants, RGB cache and animation audit."""
import argparse,ctypes,hashlib,json,subprocess,tempfile,struct
from pathlib import Path
from PIL import Image
from native_visuals_v2 import ROOT,BASE,dump,callback
from bancos_nativos import resolve_bank,bank_words
from render_native_map import Renderer,words,indexed_tiles
from host_visual_selector_v2 import compile_selector,compile_caves
from validate_border_visuals_119_118 import compile_connections
from build_border_priority_v2 import NAMES,CODES
ANIMS=((432,30,'water'),(464,10,'sand_water_edge'),(480,10,'land_water_edge'),(496,6,'waterfall'),(508,4,'flower'))
def animated(r,repo,frame):
 raw=r._tile
 def tile(t):
  for start,count,slug in ANIMS:
   if start<=t<start+count:
    files=sorted((repo/'data/tilesets/primary/general/anim'/slug).glob('*.png'));im,row,_=indexed_tiles(files[frame%len(files)]);i=t-start;return im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8))
  return raw(t)
 r._tile=tile;return r
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);ap.add_argument('--output',type=Path,default=ROOT/'review/grutas_bordas_v2/validation.json');a=ap.parse_args();base=a.base.resolve();assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
 ls=[json.loads((p/'data/layouts/layouts.json').read_text())['layouts'] for p in (base,ROOT)];assert [l['id'] for l in ls[0]]==[l['id'] for l in ls[1]];layouts=[{l['id']:l for l in ll} for ll in ls];ms={m['id']:m for p in (ROOT/'data/maps').glob('*/map.json') for m in [json.loads(p.read_text())]};byname={m['name']:m for m in ms.values()};gr=json.loads((ROOT/'review/grutas_bordas_v2/grutas_build.json').read_text());br=json.loads((ROOT/'review/grutas_bordas_v2/borders_build.json').read_text());banks={};pixelcache={}
 def rr(which,l,frame=0):
  repo=(base,ROOT)[which];key=(which,l['primary_tileset'],l['secondary_tileset'],frame)
  if key not in banks:
   r=Renderer(*[resolve_bank(repo,l[k]) for k in ('primary_tileset','secondary_tileset')]);banks[key]=animated(r,repo,frame) if frame>=0 else r
  return banks[key]
 def pix(r,mid):
  key=id(r),mid
  if key not in pixelcache:
   try:pixelcache[key]=r.metatile(mid).tobytes()
   except (IndexError,ValueError):pixelcache[key]=None
  return pixelcache[key]
 unchanged=0
 for name in subprocess.check_output(['git','ls-files','data/maps','data/layouts','src/tileset_anims.c'],cwd=base,text=True).splitlines():
  if name=='data/layouts/layouts.json':continue
  assert (ROOT/name).read_bytes()==(base/name).read_bytes(),('native gameplay changed',name);unchanged+=1
 for before,after in zip(ls[0],ls[1]):
  if before['id'] in {byname[n]['layout'] for n in NAMES}:
   assert {k:v for k,v in before.items() if k not in ('primary_tileset','secondary_tileset')}=={k:v for k,v in after.items() if k not in ('primary_tileset','secondary_tileset')}
  else:assert before==after
 own_cells=alias_cells=fallbacks=0;own={};connections=[];cave={}
 with tempfile.TemporaryDirectory() as tmp:
  folder=Path(tmp);selector=compile_selector(folder);copier=compile_connections(folder);csel=compile_caves(folder)
  # Validate all 528 native grids against unchanged behavior/attrs, including
  # all other users of Lanette's shared secondary bank.
  for m in ms.values():
   if m['name'] not in NAMES and layouts[1][m['layout']]['secondary_tileset'] not in gr['banks']:continue
   l0,l1=[ll[m['layout']] for ll in layouts];r0,r1=rr(0,l0),rr(1,l1);g=words(ROOT/l1['blockdata_filepath'])
   for mid in {v&1023 for v in g}|set(br['maps'].get(m['name'],{}).get('runtime_visual_ids',[])):
    assert bank_words(r0,mid,True)==bank_words(r1,mid,True),(m['name'],'attribute',mid)
    if m['name'] not in gr['maps']:assert pix(r0,mid)==pix(r1,mid),(m['name'],'own native RGB',mid)
   if m['name'] in NAMES:assert r0.palettes[0][0]==r1.palettes[0][0],(m['name'],'background palette zero')
   for q in br['maps'].get(m['name'],{}).get('protected_door_palette_rows',[]):assert r0.palettes[q]==r1.palettes[q],(m['name'],'fixed door palette',q)
   if m['name'] in NAMES:own[m['name']]={'cells':len(g),'native_rgb_and_attributes_identical':True};own_cells+=len(g)
  for index,(n,d) in enumerate(gr['maps'].items()):
   l=ls[1][d['layout_index']];g=words(ROOT/l['blockdata_filepath']);visual=words(ROOT/'review/grutas_bordas_v2/visual_grids'/f'{n}.bin');r=rr(1,l)
   for j,(v,alias) in enumerate(zip(g,visual)):
    mid=v&1023;x,y=j%l['width']+7,j//l['width']+7;assert csel(index,x,y,mid)==alias;assert bank_words(r,mid,True)==bank_words(r,alias,True),(n,'alias attributes',mid,alias);alias_cells+=alias!=mid
    assert csel(index,x,y,mid^1)==mid^1;fallbacks+=1
    # Every visible alias has an opaque lower layer under the object.
    if alias!=mid:
     for e in bank_words(r,alias)[:4]:assert 0 not in r._tile(e&1023).tobytes(),(n,'transparent floor',j,alias)
   for mid in range(1024):assert csel(index,0,0,mid)==mid;fallbacks+=1
   if n=='Route114_LanettesHouse':
    m=byname[n];doors={(int(e['x']),int(e['y'])) for e in m['warp_events']};floor=pix(r,0x202)
    for j,v in enumerate(g):
     if not v&0xc00 and (j%l['width'],j//l['width']) not in doors:assert pix(r,visual[j])==floor,(n,'nonuniform floor',j)
   cave[n]={'cells':len(g),'alias_cells':sum((v&1023)!=a for v,a in zip(g,visual)),'all_native_attributes_identical':True,'script_changed_IDs_fall_back':True}
  target={(r['receiver'],r['source']):r for r in br['regions']};cache_cells=animated_cells=0
  for m in ms.values():
   l0,l1=[ll[m['layout']] for ll in layouts];receiver=CODES.get(m['name'],119 if m['name']=='Route119' else 118 if m['name']=='Route118' else 0)
   for c in m['connections'] or []:
    if c['direction'] not in ('up','down','left','right'):continue
    src=ms[c['map']];s0,s1=[ll[src['layout']] for ll in layouts];sg=words(ROOT/s1['blockdata_filepath']);buf=(ctypes.c_int*50000)();count=copier(['up','down','left','right'].index(c['direction']),l1['width'],l1['height'],s1['width'],s1['height'],c['offset'],buf);istarget=(m['name'],src['name']) in target;different=after=changes=0
    for i in range(count):
     sx,sy,x,y=buf[i*4:i*4+4];mid=sg[sy*s1['width']+sx]&1023;newid=selector(receiver,x,y,mid)
     oldid=selector(receiver if m['name'] not in NAMES else 0,x,y,mid)
     before,actual,wanted=pix(rr(0,l0),oldid),pix(rr(1,l1),newid),pix(rr(1,s1),mid)
     if istarget:
      assert actual==wanted,(m['name'],src['name'],'static',sx,sy,mid,newid)
      assert bank_words(rr(1,l1),newid,True)==bank_words(rr(1,s1),mid,True)
      for frame in range(8):
       assert pix(rr(1,l1,frame),newid)==pix(rr(1,s1,frame),mid),(m['name'],src['name'],'animated',frame,sx,sy,mid,newid)
       animated_cells+=1
     else:assert actual==before,(m['name'],src['name'],'unrelated cache RGB',sx,sy,mid,newid)
     different+=before!=wanted;after+=actual!=wanted;changes+=before!=actual;cache_cells+=1
    connections.append({'receiver':m['name'],'source':src['name'],'cells':count,'different_before':different,'different_after':after,'changed_cells':changes,'target':istarget})
  for n in NAMES:
   l=layouts[1][byname[n]['layout']];code=CODES[n]
   for x,y in ((7,7),(l['width']+6,l['height']+6),(-1,-1),(l['width']+15,l['height']+14)):
    for mid in range(1024):assert selector(code,x,y,mid)==mid;fallbacks+=1
 for d in list(gr['banks'].values())+list(br['maps'].values()):
  slots=d.get('new_static_slots',d.get('new_static_graphics_slots',[]));assert not any(432<=i<512 or 992<=i<1024 for i in slots)
 newpaths=[p for d in br['maps'].values() for p in d['paths']]+[d['secondary'] for d in gr['banks'].values()]
 for path in newpaths:
  p=ROOT/path;im=Image.open(p/'tiles.png');assert im.mode=='P' and max(im.getdata())<=15
  for q in range(13):
   raw=(p/f'palettes/{q:02}.pal').read_bytes();assert b'\n' not in raw.replace(b'\r\n',b''),('palette CRLF',p,q)
 assert '|| gMapHeader.mapLayout->primaryTileset == &gTileset_AraunaBorderRoute103BaseV2)' in (ROOT/'src/fldeff_cut.c').read_text()
 report={'status':'PASS','base_commit':BASE,'unchanged_map_script_grid_and_animation_files':unchanged,'layout_ID_order_preserved':True,'own_maps':own,'caves_and_lanette':cave,'cave_alias_cells':alias_cells,'script_and_scope_fallback_checks':fallbacks,'all_directed_connections':len(connections),'cache_cells_checked':cache_cells,'eight_animation_frames_target_cells_checked':animated_cells,'target_directions':len(target),'target_differences_after':sum(c['different_after'] for c in connections if c['target']),'other_directions_changed':sum(c['changed_cells']>0 for c in connections if not c['target']),'connections':connections};dump(a.output,report);print(json.dumps({k:v for k,v in report.items() if k not in ('connections','own_maps','caves_and_lanette')},indent=2))
if __name__=='__main__':main()
