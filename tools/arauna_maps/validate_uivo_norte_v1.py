#!/usr/bin/env python3
"""Native data and actual C aliases, compared at GBA RGB555 precision."""
import argparse,ctypes,json,subprocess,tempfile,collections
from pathlib import Path
from PIL import Image
from native_visuals_v2 import ROOT,dump
from build_uivo_norte_v1 import BASE,TARGETS,FIXES,REDRAW
from bancos_nativos import resolve_bank,bank_words
from render_native_map import Renderer,words
from validate_grutas_bordas_v2 import animated
from validate_border_visuals_119_118 import compile_connections
import host_visual_selector_v2 as host

def rgb555(r):
 r.palettes=[[tuple(c>>3<<3 for c in color) for color in pal] for pal in r.palettes];return r

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);ap.add_argument('--output',type=Path,default=ROOT/'review/uivo_norte_v1/validation.json');a=ap.parse_args();base=a.base.resolve();assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
 nodes=[json.loads((p/'data/layouts/layouts.json').read_text())['layouts'] for p in (base,ROOT)];assert [l['id'] for l in nodes[0]]==[l['id'] for l in nodes[1]][:len(nodes[0])];assert len(nodes[1])==len(nodes[0])+3
 ls=[{l['id']:l for l in node} for node in nodes];maps=[{m['name']:m for p in (r/'data/maps').glob('*/map.json') for m in [json.loads(p.read_text())]} for r in (base,ROOT)];byid={m['id']:m for m in maps[1].values()};art=json.loads((ROOT/'review/uivo_norte_v1/art_build.json').read_text());border=json.loads((ROOT/'review/uivo_norte_v1/borders_build.json').read_text());oldborder=json.loads((base/'review/sul_pampa_v1/borders_build.json').read_text());cache={};pixels={}
 def render(which,n,frame=0):
  repo=(base,ROOT)[which];l=ls[which][maps[which][n]['layout']];key=(which,l['primary_tileset'],l['secondary_tileset'],frame)
  if key not in cache:cache[key]=rgb555(animated(Renderer(*[resolve_bank(repo,l[k]) for k in ('primary_tileset','secondary_tileset')]),repo,frame))
  return cache[key]
 def pix(r,mid):
  key=r,mid
  if key not in pixels:
   try:pixels[key]=r.metatile(mid).tobytes()
   except (IndexError,ValueError):pixels[key]=None
  return pixels[key]
 protected=0
 for path in subprocess.check_output(['git','ls-files','data/maps','src/tileset_anims.c'],cwd=base,text=True).splitlines():
  if path.endswith('/map.json') and path.split('/')[2] in TARGETS:continue
  assert (ROOT/path).read_bytes()==(base/path).read_bytes(),('game data changed',path);protected+=1
 for n,m in maps[1].items():
  if n in TARGETS:assert {k:v for k,v in m.items() if k!='layout'}=={k:v for k,v in maps[0][n].items() if k!='layout'}
 own={};attrs_checked=0
 for n in border['maps']:
  l0,l1=[ls[i][maps[i][n]['layout']] for i in range(2)];g0,g1=[words(p/l['blockdata_filepath']) for p,l in ((base,l0),(ROOT,l1))];assert [l0['width'],l0['height']]==[l1['width'],l1['height']];assert len(g0)==len(g1);r0,r1=render(0,n),render(1,n);geometry=[]
  for j,(v0,v1) in enumerate(zip(g0,g1)):
   assert v0>>12==v1>>12,(n,'elevation',j)
   assert bank_words(r0,v0&1023,True)==bank_words(r1,v1&1023,True),(n,'full attribute',j);attrs_checked+=1
   if (v0&0xc00)!=(v1&0xc00):geometry.append([j%l1['width'],j//l1['width']])
   if n not in TARGETS:assert v0==v1 and pix(r0,v0&1023)==pix(r1,v1&1023),(n,'own map changed',j)
   if n in FIXES and [j%l1['width'],j//l1['width']] not in art['maps'][n]['changed_cells']:assert pix(r0,v0&1023)==pix(r1,v1&1023),(n,'non-target own cell changed',j)
   if n in TARGETS and [j%l1['width'],j//l1['width']] in art['maps'][n]['changed_cells']:
    for e in bank_words(r1,v1&1023)[:4]:assert 0 not in r1._tile(e&1023).tobytes(),(n,'transparent object floor',j)
  assert geometry==art['maps'].get(n,{}).get('geometry_changed_cells',[])
  reach=[]
  if n in TARGETS:
   for surf in (False,True):
    def free(g,r,j):return not g[j]&0xc00 and (surf or bank_words(r,g[j]&1023,True)&255 not in (0x15,0x16,0x17,0x18))
    seed=next(j for j in range(len(g0)) if free(g0,r0,j) and free(g1,r1,j));seen=[]
    for g,r in ((g0,r0),(g1,r1)):
     done={seed};todo=collections.deque([seed]);w=l1['width'];h=l1['height']
     while todo:
      j=todo.popleft();x,y=j%w,j//w
      for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
       k=yy*w+xx
       if 0<=xx<w and 0<=yy<h and k not in done and free(g,r,k):done.add(k);todo.append(k)
     seen.append(done)
    for kind in ('object_events','warp_events','coord_events','bg_events'):
     for e in maps[1][n][kind]:
      x,y=int(e['x']),int(e['y']);around={yy*l1['width']+xx for xx,yy in ((x,y),(x-1,y),(x+1,y),(x,y-1),(x,y+1)) if 0<=xx<w and 0<=yy<h}
      assert bool(around&seen[0])==bool(around&seen[1]),(n,'event reach changed',kind,e,surf)
    reach.append({'surf':surf,'reachable_before':len(seen[0]),'reachable_after':len(seen[1])})
   expected=rgb555(animated(Renderer(*[ROOT/p for p in art['maps'][n]['paths']]),ROOT,0))
   for native in art['maps'][n]['engine_created_ids']:assert bank_words(r1,native,True)==bank_words(expected,native,True) and pix(r1,native)==pix(expected,native),(n,'engine-created ID',native)
   for runtime in art['maps'][n]['script_created_ids']:
    assert bank_words(r0,runtime,True)==bank_words(r1,runtime,True) and pix(r0,runtime)==pix(r1,runtime),(n,'shared script metatile changed',runtime)
   for source,target in art['maps'][n]['cut_outputs'].items():
    assert bank_words(r1,int(source),True)&255==2 and bank_words(r1,target,True)&255==0,(n,'Cut output')
    assert pix(r1,target)==pix(expected,target),(n,'Cut floor drawing',target)
  own[n]={'cells':len(g1),'same_own_RGB555':n not in TARGETS,'geometry_changed_cells':geometry,'reach':reach}
 # Preserve every pre-existing alternate layout, including Route111 without Mirage Tower.
 variants=0
 for oldlayout in nodes[0]:
  if oldlayout['id'] in {maps[0][n]['layout'] for n in border['maps']}:continue
  newlayout=ls[1][oldlayout['id']];assert newlayout==oldlayout
  for field in ('blockdata_filepath','border_filepath'):assert (base/oldlayout[field]).read_bytes()==(ROOT/newlayout[field]).read_bytes()
  variants+=1
 # Obstructing brush must differ from the encounter tuft, with behavior untouched.
 for n,count in (('Route102',104),('Route103',588)):
  d=art['maps'][n];assert len(d['changed_cells'])==count
  l=ls[1][maps[1][n]['layout']];grid=words(ROOT/l['blockdata_filepath']);r=render(1,n)
  encounter={pix(r,v&1023) for v in grid if not v&0xc00 and bank_words(r,v&1023,True)&255==2}
  for x,y in d['changed_cells']:
   v=grid[y*l['width']+x];assert v&0xc00 and bank_words(r,v&1023,True)&255==0 and pix(r,v&1023) not in encounter
 connections=[];frames_checked=0;fallbacks=0
 with tempfile.TemporaryDirectory() as tmp:
  folder=Path(tmp);p0=folder/'before';p1=folder/'after';p0.mkdir();p1.mkdir();host.ROOT=base;s0=host.compile_selector(p0);host.ROOT=ROOT;s1=host.compile_selector(p1);copier=compile_connections(p1)
  def code(which,n):
   table=oldborder if which==0 else border
   return table['maps'].get(n,{}).get('code',119 if n=='Route119' else 118 if n=='Route118' else 0)
  target={(r['receiver'],r['source']) for r in border['regions']}
  for n,m in maps[1].items():
   l0,l1=[ls[i][maps[i][n]['layout']] for i in range(2)]
   for c in m['connections'] or []:
    if c['direction'] not in ('up','down','left','right'):continue
    sn=byid[c['map']]['name'];sl0,sl1=[ls[i][maps[i][sn]['layout']] for i in range(2)];sg0=words(base/sl0['blockdata_filepath']);sg1=words(ROOT/sl1['blockdata_filepath']);buf=(ctypes.c_int*50000)();count=copier(['up','down','left','right'].index(c['direction']),l1['width'],l1['height'],sl1['width'],sl1['height'],c['offset'],buf);bad0=bad1=changed=0;is_target=(n,sn) in target
    for j in range(count):
     sx,sy,x,y=buf[j*4:j*4+4];mid0=sg0[sy*sl0['width']+sx]&1023;mid1=sg1[sy*sl1['width']+sx]&1023;alias0=s0(code(0,n),x,y,mid0);alias1=s1(code(1,n),x,y,mid1);before=pix(render(0,n),alias0);actual=pix(render(1,n),alias1);wanted=pix(render(1,sn),mid1)
     if is_target:
      assert actual==wanted,(n,sn,'RGB555',sx,sy,mid1,alias1)
      assert bank_words(render(1,n),alias1,True)==bank_words(render(1,sn),mid1,True)
      for frame in range(8):assert pix(render(1,n,frame),alias1)==pix(render(1,sn,frame),mid1),(n,sn,'animation',frame,sx,sy);frames_checked+=1
     else:assert actual==before,(n,sn,'unrelated border changed',sx,sy,mid0,mid1,alias0,alias1)
     bad0+=before!=pix(render(0,sn),mid0);bad1+=actual!=wanted;changed+=actual!=before
    connections.append({'receiver':n,'source':sn,'cells':count,'different_before':bad0,'different_after':bad1,'changed_cells':changed,'target':is_target})
  for n,d in border['maps'].items():
   l=ls[1][maps[1][n]['layout']]
   for x,y in ((7,7),(l['width']+6,l['height']+6),(-1,-1)):
    for mid in range(1024):assert s1(d['code'],x,y,mid)==mid;fallbacks+=1
 for d in border['maps'].values():
  assert not any(432<=i<512 or 992<=i<1024 for i in d['new_static_slots'])
  for p in d['paths']:
   im=Image.open(ROOT/p/'tiles.png');assert im.mode=='P' and max(im.getdata())<16
   assert all((e>>12)<13 for e in words(ROOT/p/'metatiles.bin')),(p,'unloaded palette row')
   for q in range(13):
    raw=(ROOT/p/f'palettes/{q:02}.pal').read_bytes();assert b'\n' not in raw.replace(b'\r\n',b'')
 report={'status':'PASS','base_commit':BASE,'protected_map_and_animation_files':protected,'alternate_layouts_preserved':variants,'appended_layouts':3,'all_native_attributes_checked':attrs_checked,'maps':own,'connections':connections,'target_directions':len(target),'target_errors_after':sum(c['different_after'] for c in connections if c['target']),'unrelated_connections_changed':sum(bool(c['changed_cells']) for c in connections if not c['target']),'eight_frame_border_cells_checked':frames_checked,'C_selector_fallback_checks':fallbacks};dump(a.output,report);print(json.dumps({k:v for k,v in report.items() if k not in ('maps','connections')},indent=2))
if __name__=='__main__':main()
