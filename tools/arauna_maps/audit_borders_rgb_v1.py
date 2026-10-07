#!/usr/bin/env python3
"""Audit native RGB along the engine's actual connection rectangles."""
from pathlib import Path
import argparse,sys,json,tempfile,ctypes
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/arauna_maps'))
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--output',type=Path,default=ROOT/'review/interiores_rota_v1/borders_current.json')
args=ap.parse_args()
from render_native_map import Renderer,words
from bancos_nativos import resolve_bank,bank_words
from validate_border_visuals_119_118 import compile_selector,compile_connections
ls={l['id']:l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']};ms={m['id']:m for p in (ROOT/'data/maps').glob('*/map.json') for m in [json.loads(p.read_text())]};banks={};cache={};rows=[]
def renderer(l):
 k=l['primary_tileset'],l['secondary_tileset']
 if k not in banks:banks[k]=Renderer(resolve_bank(ROOT,k[0]),resolve_bank(ROOT,k[1]))
 return banks[k]
def pixels(r,mid):
 k=str(r.primary),str(r.secondary),mid
 if k not in cache:
  try:cache[k]=r.metatile(mid).convert('RGB').tobytes()
  except (IndexError,ValueError):cache[k]=None
 return cache[k]
with tempfile.TemporaryDirectory() as temp:
 sel=compile_selector(Path(temp));copier=compile_connections(Path(temp))
 for m in sorted(ms.values(),key=lambda x:x['name']):
  if not any(c['direction'] in ['up','down','left','right'] for c in m['connections'] or []):continue
  l=ls[m['layout']];r=renderer(l)
  for c in m['connections'] or []:
   if c['direction'] not in ['up','down','left','right']:continue
   source=ms[c['map']];other=ls[source['layout']];sr=renderer(other);grid=words(ROOT/other['blockdata_filepath']);buf=(ctypes.c_int*50000)();n=copier(['up','down','left','right'].index(c['direction']),l['width'],l['height'],other['width'],other['height'],c['offset'],buf);exact=wrong=undefined=0;ids=set()
   receiver=119 if l['secondary_tileset']=='gTileset_AraunaRoute119BorderV1' else 118 if l['secondary_tileset']=='gTileset_AraunaRoute118BorderV1' else 0
   new_report=ROOT/'review/grutas_bordas_v2/borders_build.json'
   if new_report.exists():receiver=json.loads(new_report.read_text())['maps'].get(m['name'],{}).get('code',receiver)
   for i in range(n):
    x,y,gx,gy=buf[i*4:i*4+4];mid=grid[y*other['width']+x]&1023;alias=sel(receiver,gx,gy,mid);a=pixels(r,alias);b=pixels(sr,mid)
    if a!=b:exact+=1
    if a is None or b is None:undefined+=1;wrong+=1;ids.add(mid);continue
    if max(abs(u-v) for u,v in zip(a,b))>48:wrong+=1;ids.add(mid)
   rows.append({'receiver':m['name'],'source':source['name'],'direction':c['direction'],'cells':n,'exact_rgb_different':exact,'rgb_different_over_48':wrong,'undefined_metatile_cells':undefined,'source_ids_with_errors':sorted(ids)})
result={'base_commit':json.loads((ROOT/'review/grutas_bordas_v2/borders_build.json').read_text())['base_commit'] if (ROOT/'review/grutas_bordas_v2/borders_build.json').exists() else '14e56ecd6e9653c67f2ca8a111c8fabdeddd3e2f','method':'Actual C connection rectangles and scoped C border selector; repository native bank resolver; exact RGB and maximum-channel difference >48 separately. Static graphics only; VRAM water animations are not synthesized. These criteria may differ from the earlier external 55/6015 audit.','directed_connections':len(rows),'exact_rgb_different_connections':sum(x['exact_rgb_different']>0 for x in rows),'exact_rgb_different_cells':sum(x['exact_rgb_different'] for x in rows),'over_48_connections':sum(x['rgb_different_over_48']>0 for x in rows),'over_48_cells':sum(x['rgb_different_over_48'] for x in rows),'connections':rows}
p=args.output;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='connections'}));print(json.dumps(sorted(rows,key=lambda x:x['rgb_different_over_48'],reverse=True)[:12],indent=2))
