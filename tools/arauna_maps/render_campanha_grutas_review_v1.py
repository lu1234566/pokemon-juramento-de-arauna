#!/usr/bin/env python3
"""Render exact native assets and assemble existing mGBA captures, unretouched."""
import argparse,json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from render_native_map import Renderer,render_map
from bancos_nativos import resolve_bank
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'review/campanha_grutas_v1'
def board(names,title,filename):
 cols=min(3,len(names));cellw,cellh=500,370;im=Image.new('RGB',(cols*cellw,70+math.ceil(len(names)/cols)*cellh),(20,26,34));draw=ImageDraw.Draw(im);font=ImageFont.truetype('DejaVuSans.ttf',18);head=ImageFont.truetype('DejaVuSans.ttf',24);draw.text((18,16),title,font=head,fill='white')
 for i,n in enumerate(names):
  x,y=(i%cols)*cellw,70+(i//cols)*cellh;pic=Image.open(OUT/'screenshots'/f'{n}.png');assert pic.size==(240,160);im.paste(pic.resize((480,320),Image.Resampling.NEAREST),(x+10,y+35));label=n.replace('SeafloorCavern_','Seafloor ').replace('VictoryRoad_','Victory Road ').replace('Route110_TrickHousePuzzle','Trick House — desafio ').replace('Route114_','').replace('Route121_','');draw.text((x+10,y+6),label,font=font,fill='#e7d5b0')
 p=OUT/'boards'/filename;p.parent.mkdir(exist_ok=True);im.save(p)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path);a=ap.parse_args();build=json.loads((OUT/'build.json').read_text());extras=[f'Route110_TrickHousePuzzle{i}' for i in (2,4,6,7)]+['Route114_LanettesHouse','Route114_FossilManiacsTunnel','Route121_SafariZoneEntrance'];layouts={l['id']:l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
 for n in list(build['maps'])+extras:
  m=json.loads((ROOT/'data/maps'/n/'map.json').read_text());l=layouts[m['layout']];im=render_map(Renderer(resolve_bank(ROOT,l['primary_tileset']),resolve_bank(ROOT,l['secondary_tileset'])),ROOT/l['blockdata_filepath'],l['width'],l['height']);p=OUT/'static'/f'{n}.png';p.parent.mkdir(exist_ok=True);im.save(p)
 board(['VictoryRoad_1F','VictoryRoad_B1F','VictoryRoad_B2F'],'Victory Road — faixa ocre | mGBA 0.10.2','01_Victory_Road_mGBA.png')
 board(['SeafloorCavern_Entrance']+[f'SeafloorCavern_Room{i}' for i in range(1,5)],'Seafloor Cavern — basalto | mGBA 0.10.2','02_Seafloor_Entrada_Salas1_4_mGBA.png')
 board([f'SeafloorCavern_Room{i}' for i in range(5,10)],'Seafloor Cavern — basalto | mGBA 0.10.2','03_Seafloor_Salas5_9_mGBA.png')
 board(extras,'Interiores de Rota V1.1 — revisão | mGBA 0.10.2','04_Interiores_V11_mGBA.png')
 if (OUT/'interactions.json').exists():board(['VictoryRoad_1F_return','SeafloorCavern_Room1_return','Route110_TrickHousePuzzle2_collision','Route110_TrickHousePuzzle7_collision','Safari_PC','Seafloor_Surf'],'Passagens, colisão, PC e Surf | mGBA 0.10.2','05_Interacoes_mGBA.png')
 if a.base:
  old={l['id']:l for l in json.loads((a.base/'data/layouts/layouts.json').read_text())['layouts']};canvas=Image.new('RGB',(1040,90+len(extras)*290),(20,26,34));d=ImageDraw.Draw(canvas);font=ImageFont.truetype('DejaVuSans.ttf',20);d.text((20,15),'V1 → V1.1 | renders estáticos das grades completas',font=font,fill='white');d.text((20,45),'Antes (4439f99632)',font=font,fill='white');d.text((540,45),'Depois',font=font,fill='white')
  for i,n in enumerate(extras):
   m=json.loads((ROOT/'data/maps'/n/'map.json').read_text());l=old[m['layout']];before=render_map(Renderer(resolve_bank(a.base,l['primary_tileset']),resolve_bank(a.base,l['secondary_tileset'])),a.base/l['blockdata_filepath'],l['width'],l['height']);after=Image.open(OUT/'static'/f'{n}.png');y=90+i*290;d.text((20,y),n,font=font,fill='#e7d5b0')
   for x,pic in ((20,before),(540,after)):pic.thumbnail((480,250),Image.Resampling.NEAREST);canvas.paste(pic,(x,y+30))
  canvas.save(OUT/'boards/06_V11_Antes_Depois_Estatico.png')
 print('Static renders and native-capture boards generated.')
if __name__=='__main__':main()
