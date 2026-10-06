#!/usr/bin/env python3
"""Colour-invariant reuse detector against the untouched expansion corpus."""
import argparse,json,subprocess
from pathlib import Path
from audit_campanha_tile_shapes_v2 import shape,native_tiles,rgba_indices
from bancos_nativos import resolve_bank
from render_native_map import Renderer,words
ROOT=Path(__file__).resolve().parents[2]
ORIGINAL='ad0fd4d17f546ca6fd8d785c8724f9382e6e9382'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--original',type=Path,required=True);ap.add_argument('--output',type=Path,default=ROOT/'review/interiores_rota_v1/tile_shapes.json');a=ap.parse_args()
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.original,text=True).strip()==ORIGINAL
 corpus=set();total=0;nonblank=0;memo={}
 def sig(raw):
  if raw not in memo:memo[raw]=shape(raw)
  return memo[raw]
 for p in sorted((a.original/'data/tilesets').glob('*/**/tiles.png')):
  for raw in native_tiles(p):
   total+=1
   if any(raw):corpus.add(sig(raw));nonblank+=1
 node=json.loads((ROOT/'review/interiores_rota_v1/build.json').read_text());ls={l['id']:l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']};banks={};report={'original_commit':ORIGINAL,'original_stored_tiles':total,'original_nonblank_tiles':nonblank,'canonical_patterns':len(corpus),'method':'Exact equality of colour classes and transparency, including both flips. Blank/padding tiles excluded. Measures exact reuse, not cultural identity, quality or authorship. Corpus is expansion 1.16.2; percentages from different corpora are not directly interchangeable.','banks':{},'maps':{}}
 for name,row in sorted(node['maps'].items()):
  l=ls[row['layout']];p=resolve_bank(ROOT,l['primary_tileset']);s=resolve_bank(ROOT,l['secondary_tileset']);r=Renderer(p,s)
  for bank in (s,)+( (p,) if l['primary_tileset']=='gTileset_AraunaRotaBaseV1' else () ):
   key=str(bank.relative_to(ROOT))
   if key not in report['banks']:
    raw=[x for x in native_tiles(bank/'tiles.png') if any(x)];matched=sum(sig(x) in corpus for x in raw)
    report['banks'][key]={'nonblank_stored_tiles':len(raw),'matching_hoenn_shape':matched,'match_percent':round(100*matched/len(raw),2)}
  observed=[];upper=[]
  for cell in words(ROOT/l['blockdata_filepath']):
   mid=cell&1023;im=r.metatile(mid)
   for y in (0,8):
    for x in (0,8):
     raw=rgba_indices(im.crop((x,y,x+8,y+8)))
     if any(raw):observed.append(sig(raw) in corpus)
   table=r.primary_metatiles if mid<512 else r.secondary_metatiles
   for entry in table[(mid%512)*8+4:(mid%512)*8+8]:
    raw=r._tile(entry&1023).tobytes()
    if any(raw):upper.append(sig(raw) in corpus)
  report['maps'][name]={'drawn_composited_blocks':len(observed),'composited_match_percent':round(100*sum(observed)/len(observed),2),'nonblank_upper_references':len(upper),'upper_match_percent':round(100*sum(upper)/len(upper),2) if upper else 0}
 assert all(v['match_percent']<=50 for v in report['banks'].values()),'More than half of the stored nonblank art matches the reference'
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['banks'],indent=2))

if __name__=='__main__':main()
