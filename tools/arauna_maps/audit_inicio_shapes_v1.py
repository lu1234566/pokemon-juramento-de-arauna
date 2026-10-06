#!/usr/bin/env python3
"""Report exact color-invariant matches; compatibility tiles are explicit."""
import argparse,json,subprocess
from pathlib import Path
from render_native_map import Renderer,words
from bancos_nativos import resolve_bank
from audit_campanha_tile_shapes_v2 import native_tiles,shape,rgba_indices,ORIGINAL
ROOT=Path(__file__).resolve().parents[2]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--original',type=Path,required=True);ap.add_argument('--base',type=Path,required=True);a=ap.parse_args()
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.original,text=True).strip()==ORIGINAL
 corpus=set();total=0
 for p in sorted((a.original/'data/tilesets').glob('*/**/tiles.png')):
  for raw in native_tiles(p):
   total+=1
   if any(raw):corpus.add(shape(raw))
 report={'original_commit':ORIGINAL,'original_stored_tiles':total,'canonical_shapes':len(corpus),'method':'Exact color-class equality with transparency and H/V mirrors; not a perceptual or Brazilian identity score. Flat areas can match incidentally. Compatibility banks retain original neighbor tiles deliberately.','banks':{},'maps':{}}
 ls={l['id']:l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
 m=json.loads((ROOT/'data/maps/LittlerootTown/map.json').read_text());l=ls[m['layout']];r=Renderer(resolve_bank(ROOT,l['primary_tileset']),resolve_bank(ROOT,l['secondary_tileset']))
 build=json.loads((ROOT/'review/inicio_geometria_v1/build.json').read_text())['bank'];raw=[r._tile(i).tobytes() for i in build['new_static_tile_slots']];matched=sum(shape(t) in corpus for t in raw)
 report['new_art_only']={'nonblank_tiles':len(raw),'matching_old_shape':matched,'percent':round(100*matched/len(raw),2)}
 assert report['new_art_only']['percent']<50,'new module shapes mostly inherited'
 for bank in (r.primary,r.secondary):
  ts=[t for t in native_tiles(bank/'tiles.png') if any(t)];n=sum(shape(t) in corpus for t in ts)
  report['banks'][str(bank.relative_to(ROOT))]={'nonblank_tiles':len(ts),'matching_old_shape':n,'percent':round(100*n/len(ts),2),'includes_neighbor_compatibility':True}
 for n in ('LittlerootTown','Route101','OldaleTown'):
  report['maps'][n]={}
  for label,root in [('before',a.base),('after',ROOT)]:
   node={l['id']:l for l in json.loads((root/'data/layouts/layouts.json').read_text())['layouts']};m=json.loads((root/f'data/maps/{n}/map.json').read_text());l=node[m['layout']];rr=Renderer(resolve_bank(root,l['primary_tileset']),resolve_bank(root,l['secondary_tileset']))
   samples=[]
   for v in words(root/l['blockdata_filepath']):
    im=rr.metatile(v&1023)
    for y in (0,8):
     for x in (0,8):samples.append(shape(rgba_indices(im.crop((x,y,x+8,y+8)))) in corpus)
   report['maps'][n][label]={'opaque_map_blocks':len(samples),'matching_shape':sum(samples),'percent':round(100*sum(samples)/len(samples),2)}
 p=ROOT/'review/inicio_geometria_v1/originality.json';p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
