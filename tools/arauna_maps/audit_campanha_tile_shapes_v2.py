#!/usr/bin/env python3
"""Exact colour-invariant tile-shape matches, with both mirrored variants.

This is a reuse detector, not a Brazilian-identity score. Plain surfaces can
match incidentally. It reports stored nonblank tiles and composited map blocks
separately; it never counts invisible padding as new art.
"""
import argparse,json,struct,subprocess,hashlib
from pathlib import Path
from PIL import Image
from render_native_map import indexed_tiles,Renderer,render_map,words
from bancos_nativos import resolve_bank
from build_campanha_interiores_v1 import MAPS
ROOT=Path(__file__).resolve().parents[2]
ORIGINAL='ad0fd4d17f546ca6fd8d785c8724f9382e6e9382'

def canon(values):
 mapping={0:0};out=[]
 for value in values:
  if value not in mapping:mapping[value]=len(mapping)
  out.append(mapping[value])
 return bytes(out)

def shape(raw):
 im=Image.frombytes('L',(8,8),raw)
 return min(canon(t.tobytes()) for t in (im,im.transpose(Image.Transpose.FLIP_LEFT_RIGHT),im.transpose(Image.Transpose.FLIP_TOP_BOTTOM),im.transpose(Image.Transpose.ROTATE_180)))

def native_tiles(path):
 im,_,_=indexed_tiles(path)
 return [im.crop((x,y,x+8,y+8)).tobytes() for y in range(0,im.height,8) for x in range(0,im.width,8)]

def rgba_indices(im):
 mapping={};out=[]
 for r,g,b,a in im.convert('RGBA').getdata():
  key=(r,g,b)
  if not a:out.append(0);continue
  if key not in mapping:mapping[key]=len(mapping)+1
  out.append(mapping[key])
 return bytes(out)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--original',type=Path,required=True);ap.add_argument('--base',type=Path,required=True);ap.add_argument('--output',type=Path,default=ROOT/'review/campanha_interiores_v2/tile_shapes.json');a=ap.parse_args()
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.original,text=True).strip()==ORIGINAL
 corpus=set();original_tiles=0
 for p in sorted((a.original/'data/tilesets').glob('*/**/tiles.png')):
  for raw in native_tiles(p):
   original_tiles+=1
   if any(raw):corpus.add(shape(raw))
 node=lambda root:{l['id']:l for l in json.loads((root/'data/layouts/layouts.json').read_text())['layouts']}
 before=node(a.base);after=node(ROOT)
 report={'original_commit':ORIGINAL,'original_tiles':original_tiles,'canonical_nonblank_shapes':len(corpus),'method':'Exact equality of colour classes, transparency, and horizontal/vertical mirrors; blank tiles excluded. Incidental matches on simple shapes possible. Not a perceptual originality or cultural-identity score.','banks':{},'maps':{}}
 banks={}
 for label,root,ls in (('V1',a.base,before),('V2',ROOT,after)):
  for name in MAPS:
   m=json.loads((root/'data/maps'/name/'map.json').read_text());l=ls[m['layout']]
   p=resolve_bank(root,l['primary_tileset']);s=resolve_bank(root,l['secondary_tileset'])
   for bank in (s,)+( (p,) if label=='V2' and l['primary_tileset'].endswith('BaseV2') else () ):
    key=label+':'+str(bank.relative_to(root))
    if key not in report['banks']:
     raw=[t for t in native_tiles(bank/'tiles.png') if any(t)]
     matched=sum(shape(t) in corpus for t in raw)
     report['banks'][key]={'nonblank_stored_tiles':len(raw),'matching_hoenn_shape':matched,'match_percent':round(100*matched/len(raw),2) if raw else 0}
   r=Renderer(p,s);cells=words(root/l['blockdata_filepath']);observed=[];objects=[]
   for cell in cells:
    mid=cell&1023;im=r.metatile(mid)
    for y in (0,8):
     for x in (0,8):
      raw=rgba_indices(im.crop((x,y,x+8,y+8)))
      if any(raw):observed.append(shape(raw) in corpus)
    table=r.primary_metatiles if mid<512 else r.secondary_metatiles;local=mid if mid<512 else mid-512
    for entry in table[local*8+4:local*8+8]:
     t=r._tile(entry&1023)
     if t is not None and any(t.tobytes()):objects.append(shape(t.tobytes()) in corpus)
   report['maps'].setdefault(name,{})[label]={'opaque_composited_map_blocks':len(observed),'matching_hoenn_shape':sum(observed),'match_percent':round(100*sum(observed)/len(observed),2),'nonblank_upper_object_references':len(objects),'upper_object_matching_shape':sum(objects),'upper_object_match_percent':round(100*sum(objects)/len(objects),2) if objects else 0}
 assert all(v['match_percent']<=50 for k,v in report['banks'].items() if k.startswith('V2:')),'More than half the stored nonblank tiles match Hoenn'
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'banks':report['banks'],'maps':report['maps']},indent=2))

if __name__=='__main__':main()
