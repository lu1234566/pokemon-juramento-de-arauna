#!/usr/bin/env python3
"""Five whole-map pairs, entry cameras and cable floor replacement states."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from native_visuals_v2 import dump
from frontier_07h_common import ROOT,OUT,NAMES,ROLES,inventory,render,renderer,require_base
BG=(24,28,32);INK='#eed6a8';FONT=ImageFont.truetype('DejaVuSans.ttf',19);SMALL=ImageFont.truetype('DejaVuSans.ttf',14)
def label(im,x,y,s,big=False):ImageDraw.Draw(im).text((x,y),s,font=FONT if big else SMALL,fill=INK)
def camera(im,x=None,y=None):
    if x is None:x=im.width//2
    if y is None:y=im.height-80
    out=Image.new('RGB',(240,160),BG);out.paste(im,(120-x,80-y));return out
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    _,bl,bm=inventory(base);_,ls,ms=inventory(ROOT);full={};before={};cameras=Image.new('RGB',(1010,1850),BG);label(cameras,16,12,'07H — 240×160 — ORIGINAL À ESQUERDA / NOVO À DIREITA',True)
    rows=[]
    for i,(n,role) in enumerate(zip(NAMES,ROLES)):
        a=render(base,bl[bm[n]['layout']]);b=render(ROOT,ls[ms[n]['layout']]);full[n]=b;before[n]=a
        for im,suffix in ((a,'Before'),(b,'After')):im.save(OUT/(n+'_'+suffix+'.png'));camera(im).save(OUT/(n+'_Camera_'+suffix+'.png'))
        y=52+i*350;label(cameras,16,y,role)
        for im,x in ((a,16),(b,520)):cameras.paste(camera(im).resize((480,320),Image.Resampling.NEAREST),(x,y+24))
        rows.append((n,role,a,b))
    label(cameras,16,1820,'Bancos 4bpp em RGB555, sem atores. Recortes nativos; não são fotos do mGBA.');cameras.save(OUT/'BattleFrontier_07H_Cameras_240x160.png')
    height=100+sum(a.height*(4 if a.width<300 else 2)+65 for n,role,a,b in rows)
    board=Image.new('RGB',(1770,height),BG);label(board,16,12,'ARAUNA — 07H — SERVIÇOS — MAPAS COMPLETOS',True)
    y=58
    for n,role,a,b in rows:
        label(board,16,y,role+' — original em cima / novo embaixo')
        scale=2 if a.width<300 else 1
        for im,yy in ((a,y+25),(b,y+30+a.height*scale)):board.paste(im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST),(16,yy))
        y+=a.height*scale*2+65
    board=board.crop((0,0,1770,y+38));label(board,16,y+6,'44/47. Madeira, cerâmica verde, pedra clara e bronze. IDs, atributos e planos preservados.');board.save(OUT/'BattleFrontier_07H_Antes_Depois.png')
    states=Image.new('RGB',(1010,430),BG);label(states,16,12,'07H — COMUNICAÇÃO — BALCÃO FECHADO / PASSAGEM ABERTA',True)
    l=ls[ms[NAMES[3]]['layout']]
    from render_native_map import words
    from frontier_07h_common import render_grid
    grid=words(ROOT/l['blockdata_filepath']);opened=list(grid)
    for x in (5,9):opened[2*14+x]=(opened[2*14+x]&~1023)|0x2dc;opened[3*14+x]=(opened[3*14+x]&~1023)|0x2e4
    for im,x in ((full[NAMES[3]],16),(render_grid(ROOT,l,opened,14,10),520)):states.paste(camera(im,112,80).resize((480,320),Image.Resampling.NEAREST),(x,58))
    label(states,16,398,'IDs 0x21E / 0x25D ↔ 0x2DC / 0x2E4. Scripts de cable_club.inc preservados.');states.save(OUT/'BattleFrontier_07H_Comunicacao_Estados.png')
    dump(OUT/'renders.json',{'whole_map_pairs':5,'camera_pairs':5,'cable_script_states':2,'native_rgb555':True,'sprites':False,'emulator_screenshots':False})
    print('07H: five native pairs and cable-room states rendered.')
if __name__=='__main__':main()
