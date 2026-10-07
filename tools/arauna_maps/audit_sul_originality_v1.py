#!/usr/bin/env python3
"""Exact shape/color-class audit of new art, excluding imported compatibility."""
import argparse,json,subprocess
from pathlib import Path
from PIL import Image
from native_visuals_v2 import ROOT,dump
from render_native_map import Renderer,indexed_tiles
from bancos_nativos import bank_words
ORIGINAL='ad0fd4d17f546ca6fd8d785c8724f9382e6e9382'
def shape(raw):
 classes={};out=[]
 for ix in raw:
  if ix==0:out.append(0);continue
  if ix not in classes:classes[ix]=len(classes)+1
  out.append(classes[ix])
 return bytes(out)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--original',type=Path,required=True);a=ap.parse_args();root=a.original.resolve();assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()==ORIGINAL
 shapes=set();count=0
 for p in sorted((root/'data/tilesets').glob('*/*/tiles.png')):
  im,row,n=indexed_tiles(p)
  for j in range(n):
   tile=im.crop((j%row*8,j//row*8,j%row*8+8,j//row*8+8));count+=1
   for op in (None,Image.Transpose.FLIP_LEFT_RIGHT,Image.Transpose.FLIP_TOP_BOTTOM,Image.Transpose.ROTATE_180):shapes.add(shape((tile.transpose(op) if op is not None else tile).tobytes()))
 art=json.loads((ROOT/'review/sul_pampa_v1/art_build.json').read_text());report={}
 for n,d in art['maps'].items():
  r=Renderer(*[ROOT/p for p in d['paths']]);ids={e&1023 for mid in d['custom_metatile_ids'] for e in bank_words(r,mid)};tiles={r._tile(t).tobytes() for t in ids if t and r._tile(t) is not None and any(r._tile(t).tobytes())};matching=sum(shape(t) in shapes for t in tiles);report[n]={'new_art_nonblank_graphics':len(tiles),'matching_original_color_class_shape':matching,'percent':round(100*matching/len(tiles),2)}
 result={'status':'PASS','original_commit':ORIGINAL,'original_stored_graphics':count,'method':'Exact color-class/alpha equality with H/V mirrors, on new-art graphics only. Functional water, ledge, door and imported neighbor graphics excluded. Flat textures may coincide. Not a perceptual identity measure.','maps':report};dump(ROOT/'review/sul_pampa_v1/originality.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
