"""Checkpoint 04 configuration and native underwater rendering."""
import json,re
from pathlib import Path
from PIL import Image
from native_visuals_v2 import ROOT,Pair
from bancos_nativos import resolve_bank
from render_native_map import words,indexed_tiles,Renderer
from validate_grutas_bordas_v2 import animated

BASE='802d01c3417a9384f8de54050c469e0c5de29399'
OUT=ROOT/'review/dive_04'
GROUPS={
 'costa':('Underwater_Route105',),
 'arquipelago':('Underwater_Route124','Underwater_Route126','Underwater_SootopolisCity'),
 'mare':('Underwater_Route125','Underwater_MarineCave'),
 'oceano':('Underwater_Route127','Underwater_Route128','Underwater_Route129'),
 'arquivo':('Underwater_Route134','Underwater_SealedChamber'),
 'horizonte':('Underwater_SeafloorCavern',),
}
NAMES=tuple(n for group in GROUPS.values() for n in group)
REGISTRIES={'data/layouts/layouts.json','src/data/arauna_cave_visuals_v2.h','src/data/tilesets/graphics.h','src/data/tilesets/metatiles.h','src/data/tilesets/headers.h'}
SURFACE_FILES={
 'data/tilesets/primary/arauna_border_route103_uivo_v1/metatiles.bin',
 'data/tilesets/secondary/arauna_border_route103_uivo_v1/tiles.png',
 'data/tilesets/secondary/arauna_border_route111_uivo_v1/tiles.png',
 'data/tilesets/secondary/arauna_border_route111_uivo_v1/metatiles.bin',
 'data/tilesets/secondary/arauna_border_route111_uivo_v1/metatile_attributes.bin',
}
MUTABLE=REGISTRIES|SURFACE_FILES|{'src/arauna_cave_visuals.c','src/field_weather_effect.c'}

def inventory(repo):
 node=json.loads((repo/'data/layouts/layouts.json').read_text())
 maps={m['name']:m for p in (repo/'data/maps').glob('*/map.json') for m in [json.loads(p.read_text())]}
 return node,{l['id']:l for l in node['layouts']},maps

def safe(pair):
 pair.free=[i for i in pair.free if i>=512 and i not in pair.dynamic]
 pair.tile_cache={raw:i for i,raw in pair.tiles.items() if i>=512 and i not in pair.dynamic and i not in pair.free}
 assert pair.reader._tile(0).tobytes()==bytes(64)
 pair.tile_cache[bytes(64)]=0

def renderer(repo,layout,frame=0):
 r=animated(Renderer(*[resolve_bank(repo,layout[k]) for k in ('primary_tileset','secondary_tileset')]),repo,frame)
 original=r._tile
 files=sorted((repo/'data/tilesets/secondary/underwater/anim/seaweed').glob('*.png'))
 im,row,_=indexed_tiles(files[(0,1,2,1)[frame%4]])
 def tile(t):
  if 1008<=t<1012:
   i=t-1008;return im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8))
  return original(t)
 r._tile=tile
 r.palettes=[[tuple(c>>3<<3 for c in rgb) for rgb in pal] for pal in r.palettes]
 return r

def render(repo,layout,visual=None,frame=0):
 r=renderer(repo,layout,frame);g=visual if visual is not None else [v&1023 for v in words(repo/layout['blockdata_filepath'])]
 out=Image.new('RGBA',(layout['width']*16,layout['height']*16));cache={}
 for i,mid in enumerate(g):
  if mid not in cache:cache[mid]=r.metatile(mid)
  out.alpha_composite(cache[mid],(i%layout['width']*16,i//layout['width']*16))
 return out.convert('RGB')

def strip_landmark_hook(text):
 return re.sub(r'\n*    // DIVE_04_LANDMARKS_BEGIN\n.*?    // DIVE_04_LANDMARKS_END\n','\n',text,flags=re.S)
