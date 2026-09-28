#!/usr/bin/env python3
"""Render seven native maps and selected original/converted comparisons."""
import json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent))
import render_native_map as native
native.ROOT=ROOT
layouts={r['id']:r for r in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
names=[f'MossdeepCity_House{i}' for i in range(1,5)]+['MossdeepCity_Mart','MossdeepCity_PokemonCenter_1F','MossdeepCity_PokemonCenter_2F']
sources={name:ref for name,ref in zip(names,['LAYOUT_HOUSE2','LAYOUT_HOUSE1','LAYOUT_HOUSE2','LAYOUT_HOUSE_WITH_BED',
                                              'LAYOUT_MART','LAYOUT_POKEMON_CENTER_1F','LAYOUT_POKEMON_CENTER_2F'])}
def render(layout):
 r=native.Renderer(native.resolve_tileset(layout['primary_tileset']),native.resolve_tileset(layout['secondary_tileset']))
 return native.render_map(r,ROOT/layout['blockdata_filepath'],layout['width'],layout['height'])
def current(name):
 d=json.loads((ROOT/'data/maps'/name/'map.json').read_text());return layouts[d['layout']]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
bg='#172a33';out=ROOT.parent/'output';out.mkdir(exist_ok=True)
board=Image.new('RGB',(1600,990),bg);draw=ImageDraw.Draw(board)
draw.text((28,24),'MISSÕES DO CÉU • MORADIAS E SERVIÇOS',font=font,fill='#f6f1e4')
draw.text((28,65),'Sete mapas nativos • quatro casas, loja e Centro Pokémon',font=small,fill='#a8d2d5')
for i,name in enumerate(names):
 x=28+(i%4)*390;y=108+(i//4)*430
 label=name.removeprefix('MossdeepCity_').replace('PokemonCenter_','Centro ').replace('House','Casa ')
 draw.text((x,y),label,font=small,fill='#f4c875')
 img=render(current(name));scale=1.6
 resized=img.resize((round(img.width*scale),round(img.height*scale)),Image.Resampling.NEAREST)
 board.paste(resized,(x,y+30))
draw.text((28,970),'Arte derivada do concept e ajustada ao banco 4bpp • personagens ocultos no render.',font=small,fill='#a8d2d5',anchor='ls')
path=out/'missoes_ceu_interiors_v1_7_ambientes.png';board.save(path)
compare=Image.new('RGB',(1510,1050),bg);draw=ImageDraw.Draw(compare)
draw.text((28,24),'MISSÕES DO CÉU • ANTES E DEPOIS',font=font,fill='#f6f1e4')
draw.text((28,64),'Casa 1 e Centro Pokémon • metatiles nativos',font=small,fill='#a8d2d5')
for row,name in enumerate(('MossdeepCity_House1','MossdeepCity_PokemonCenter_1F')):
 for col,layout in enumerate((layouts[sources[name]],current(name))):
  x=28+col*740;y=110+row*462
  draw.text((x,y),('Antes • Emerald' if col==0 else 'Depois • Missões do Céu')+' • '+('Casa' if row==0 else 'Centro'),font=small,fill='#f4c875')
  img=render(layout).resize((layout['width']*40,layout['height']*40),Image.Resampling.NEAREST)
  compare.paste(img,(x,y+32))
draw.text((28,1028),'Colisão, elevação, warps e scripts conferidos; teste em ROM pendente.',font=small,fill='#a8d2d5',anchor='ls')
path2=out/'missoes_ceu_interiors_v1_comparison.png';compare.save(path2)
print(path);print(path2)
