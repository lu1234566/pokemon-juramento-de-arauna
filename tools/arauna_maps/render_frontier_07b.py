#!/usr/bin/env python3
"""Four native Dome maps, cameras, all four light frames and door footprints."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from frontier_07b_common import ROOT,OUT,NAMES,inventory,render,renderer,require_base,door_records
from native_visuals_v2 import dump

BG=(24,28,32)

def camera(im):
    crop=Image.new('RGB',(240,160));ox=max(0,(im.width-240)//2);oy=max(0,(im.height-160)//2)
    part=im.crop((ox,oy,min(im.width,ox+240),min(im.height,oy+160)));crop.paste(part,((240-part.width)//2,(160-part.height)//2));return crop

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',required=True,type=Path);base=ap.parse_args().base.resolve();require_base(base)
    _,bl,bm=inventory(base);_,ls,maps=inventory(ROOT);font=ImageFont.truetype('DejaVuSans.ttf',18);small=ImageFont.truetype('DejaVuSans.ttf',14)
    board=Image.new('RGB',(1216,850),BG);d=ImageDraw.Draw(board);full={};before={}
    positions=[(12,48,520,380),(548,48,650,240),(12,450,520,352),(548,330,650,450)]
    d.text((12,12),'ARAUNA — 07B — BATTLE DOME / QUATRO MAPAS',font=font,fill='#eed6a8')
    for n,(x,y,w,h) in zip(NAMES,positions):
        l=ls[maps[n]['layout']];full[n]=render(ROOT,l);before[n]=render(base,bl[bm[n]['layout']]);full[n].save(OUT/(n+'_After.png'));before[n].save(OUT/(n+'_Before.png'))
        d.text((x,y),n.removeprefix('BattleFrontier_BattleDome')+f' — {l["width"]}×{l["height"]}',font=font,fill='#eed6a8')
        im=full[n];scale=min(w/im.width,(h-32)/im.height);board.paste(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST),(x,y+32))
    d.text((12,821),'Bancos nativos RGB555. Pedra, madeira e bronze; sem atores ou captura de emulador.',font=small,fill='#d8c9af');board.save(OUT/'BattleFrontier_07B_Quatro_Mapas.png')
    cameras=Image.new('RGB',(1000,1500),BG);d=ImageDraw.Draw(cameras);d.text((12,8),'07B — ANTES / DEPOIS — câmera nativa 240×160',font=font,fill='white')
    for i,n in enumerate(NAMES):
        y=46+i*360;d.text((12,y),n.removeprefix('BattleFrontier_'),font=font,fill='#eed6a8')
        for tag,im,x in [('Before',before[n],12),('After',full[n],508)]:
            crop=camera(im);crop.save(OUT/(n+'_Camera_'+tag+'.png'));cameras.paste(crop.resize((480,320),Image.Resampling.NEAREST),(x,y+26))
    cameras.save(OUT/'BattleFrontier_07B_Antes_Depois.png')
    lights=Image.new('RGB',(1220,1080),BG);d=ImageDraw.Draw(lights);d.text((12,12),'LUZES ANIMADAS — quatro quadros da paleta nativa 8',font=font,fill='white')
    room=NAMES[3];l=ls[maps[room]['layout']]
    for frame in range(4):
        im=render(ROOT,l,frame);im.save(OUT/(room+f'_Light_Frame_{frame}.png'));x=12+(frame%2)*606;y=50+(frame//2)*350
        d.text((x,y),f'Quadro {frame} — índices 13 e 15, mesmas posições',font=small,fill='#eed6a8');lights.paste(im.resize((576,288),Image.Resampling.NEAREST),(x,y+24))
    d.text((12,762),'PORTAS — footprint original fechado, duas células verticais intactas',font=font,fill='white')
    doors=door_records(ROOT)
    for i,n in enumerate(NAMES[:3]):
        cells=doors[n];x0=cells[0]['x'];y0=cells[0]['y'];x=12+i*402;d.text((x,798),n.removeprefix('BattleFrontier_BattleDome'),font=font,fill='#eed6a8')
        for im,xx in [(before[n],x),(full[n],x+160)]:
            crop=im.crop((max(0,x0*16-32),max(0,y0*16-16),(x0+3)*16,(y0+3)*16));lights.paste(crop.resize((144,128),Image.Resampling.NEAREST),(xx,828))
        d.text((x,965),'Antes                         Depois',font=small,fill='#d8c9af')
    d.text((12,1000),'Paletas 7 e 9 e gráficos de portas preservados. Animação e fade executados no C do host.',font=small,fill='#d8c9af')
    d.text((12,1025),'Renders de revisão; batalha, sprites e execução no GBA permanecem pendentes.',font=small,fill='#d8c9af');lights.save(OUT/'BattleFrontier_07B_Luzes_e_Portas.png')
    dump(OUT/'renders.json',{'maps':4,'camera_pairs':4,'palette8_frames':4,'native_rgb555':True,'sprites':False,'emulator_screenshots':False,'native_door_footprints':True})
    print('Four native maps, four camera pairs, four light frames and three door-footprint comparisons rendered.')

if __name__=='__main__':main()
