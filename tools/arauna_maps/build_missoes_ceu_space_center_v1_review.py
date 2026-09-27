#!/usr/bin/env python3
"""Comparison rendered from actual source and replacement native metatiles."""
import json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent))
import render_native_map as native
native.ROOT=ROOT
layouts={x['id']:x for x in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
canvas=Image.new('RGB',(1700,1150),'#112436');d=ImageDraw.Draw(canvas)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',25)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19)
d.text((34,25),'MISSÕES DO CÉU • CENTRO ESPACIAL',font=font,fill='#f2f1dc')
d.text((34,67),'2 pisos • render nativo dos metatiles • geometria de eventos preservada',font=small,fill='#9ec8d4')
d.text((34,114),'Antes • Facility / Emerald',font=small,fill='white')
d.text((870,114),'Depois • observação e preparo',font=small,fill='white')
for row,floor in enumerate(('1F','2F')):
 l=layouts['LAYOUT_MOSSDEEP_CITY_SPACE_CENTER_'+floor]
 old=native.Renderer(native.resolve_tileset(l['primary_tileset']),native.resolve_tileset('gTileset_Facility'))
 new=native.Renderer(native.resolve_tileset(l['primary_tileset']),native.resolve_tileset(l['secondary_tileset']))
 src=ROOT/'data/layouts'/('MossdeepCity_SpaceCenter_'+floor)/'map.bin'
 panels=[native.render_map(old,src,16,10),native.render_map(new,ROOT/l['blockdata_filepath'],16,10)]
 for col,im in enumerate(panels):canvas.paste(im.resize((768,480),Image.Resampling.NEAREST),(34+col*836,145+row*490))
d.text((34,1133),'1F: hall e consoles • 2F: observação e plataforma • sprites de NPC não incluídos no render',font=small,fill='#9ec8d4',anchor='ls')
out=ROOT.parent/'output/missoes_ceu_space_center_v1_comparison.png';out.parent.mkdir(exist_ok=True);canvas.save(out)
print(out)
