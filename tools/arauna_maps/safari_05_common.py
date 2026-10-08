"""Base-specific Safari V1 configuration and native rendering."""
import json
from pathlib import Path
from PIL import Image
from native_visuals_v2 import ROOT
from bancos_nativos import resolve_bank
from render_native_map import Renderer,words
from validate_grutas_bordas_v2 import animated

BASE='5d0b14e46e98f099ef4807af71d5e9be60f88d66'
OUT=ROOT/'review/safari_05'
EXTERIORS=('SafariZone_Northwest','SafariZone_North','SafariZone_Northeast','SafariZone_Southwest','SafariZone_South','SafariZone_Southeast')
GROUPS={'mata':EXTERIORS,'pouso':('SafariZone_RestHouse',),'recepcao':('Route121_SafariZoneEntrance',)}
NAMES=tuple(n for group in GROUPS.values() for n in group)
MUTABLE={'data/layouts/layouts.json',*('src/data/tilesets/'+k for k in ('graphics.h','metatiles.h','headers.h'))}

def inventory(repo):
 node=json.loads((repo/'data/layouts/layouts.json').read_text())
 maps={m['name']:m for p in (repo/'data/maps').glob('*/map.json') for m in [json.loads(p.read_text())]}
 return node,{l['id']:l for l in node['layouts']},maps

def renderer(repo,layout,frame=0):
 r=Renderer(*[resolve_bank(repo,layout[k]) for k in ('primary_tileset','secondary_tileset')])
 if 'Mata' in layout['primary_tileset'] or layout['primary_tileset']=='gTileset_General':r=animated(r,repo,frame)
 r.palettes=[[tuple(c>>3<<3 for c in rgb) for rgb in pal] for pal in r.palettes]
 return r

def render(repo,layout,frame=0):
 r=renderer(repo,layout,frame);cache={};g=words(repo/layout['blockdata_filepath']);out=Image.new('RGBA',(layout['width']*16,layout['height']*16))
 for i,v in enumerate(g):
  mid=v&1023
  if mid not in cache:cache[mid]=r.metatile(mid)
  out.alpha_composite(cache[mid],(i%layout['width']*16,i//layout['width']*16))
 return out.convert('RGB')
