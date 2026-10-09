#!/usr/bin/env python3
"""Native RGB555 six-map board, paired cameras, water cycles and doors."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from frontier_07c_common import ROOT,OUT,NAMES,inventory,render,door_records,require_base
from native_visuals_v2 import dump
BG=(24,28,32)

def camera(im):
    crop=Image.new('RGB',(240,160));ox=max(0,(im.width-240)//2);oy=max(0,(im.height-160)//2);part=im.crop((ox,oy,min(im.width,ox+240),min(im.height,oy+160)));crop.paste(part,((240-part.width)//2,(160-part.height)//2));return crop

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',required=True,type=Path);base=ap.parse_args().base.resolve();require_base(base)
    _,bl,bm=inventory(base);_,ls,maps=inventory(ROOT);font=ImageFont.truetype('DejaVuSans.ttf',18);small=ImageFont.truetype('DejaVuSans.ttf',14)
    board=Image.new('RGB',(1216,1120),BG);d=ImageDraw.Draw(board);full={};before={};d.text((12,12),'ARAUNA — 07C — PALACE / ARENA — SEIS MAPAS',font=font,fill='#eed6a8')
    for i,n in enumerate(NAMES):
        l=ls[maps[n]['layout']];full[n]=render(ROOT,l);before[n]=render(base,bl[bm[n]['layout']]);full[n].save(OUT/(n+'_After.png'));before[n].save(OUT/(n+'_Before.png'))
        x=12+(i//3)*604;y=52+(i%3)*346;d.text((x,y),n.removeprefix('BattleFrontier_Battle')+f' — {l["width"]}×{l["height"]}',font=font,fill='#eed6a8');im=full[n];scale=min(580/im.width,300/im.height);board.paste(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST),(x,y+28))
    d.text((12,1092),'Bancos nativos RGB555: jardim de água e terracota; madeira e tapete de fibra. Sem atores.',font=small,fill='#d8c9af');board.save(OUT/'BattleFrontier_07C_Seis_Mapas.png')
    cameras=Image.new('RGB',(1000,2240),BG);d=ImageDraw.Draw(cameras);d.text((12,8),'07C — ANTES / DEPOIS — câmera nativa 240×160',font=font,fill='white')
    for i,n in enumerate(NAMES):
        y=46+i*360;d.text((12,y),n.removeprefix('BattleFrontier_'),font=font,fill='#eed6a8')
        for tag,im,x in [('Before',before[n],12),('After',full[n],508)]:
            crop=camera(im);crop.save(OUT/(n+'_Camera_'+tag+'.png'));cameras.paste(crop.resize((480,320),Image.Resampling.NEAREST),(x,y+26))
    cameras.save(OUT/'BattleFrontier_07C_Antes_Depois.png')
    water=Image.new('RGB',(1970,1070),BG);d=ImageDraw.Draw(water);d.text((12,12),'PALACE — OITO CICLOS NATIVOS DA ÁGUA / SEQUÊNCIA DE FLORES 0, 1, 0, 2',font=font,fill='white');room=NAMES[2];l=ls[maps[room]['layout']]
    for frame in range(8):
        im=render(ROOT,l,frame);im.save(OUT/(room+f'_Water_Frame_{frame}.png'));x=12+(frame%4)*490;y=50+(frame//4)*360;d.text((x,y),f'Ciclo {frame}',font=font,fill='#eed6a8');water.paste(im.resize((480,320),Image.Resampling.NEAREST),(x,y+26))
    d.text((12,780),'PORTAS — duas células verticais originais; materiais novos ao redor',font=font,fill='white');doors=door_records(ROOT)
    for i,n in enumerate((NAMES[0],NAMES[1],NAMES[3])):
        x=12+i*650;x0=doors[n][0]['x'];y0=doors[n][0]['y'];d.text((x,815),n.removeprefix('BattleFrontier_Battle'),font=font,fill='#eed6a8')
        for im,xx in ((before[n],x),(full[n],x+180)):
            crop=im.crop((max(0,x0*16-32),max(0,y0*16-16),(x0+3)*16,(y0+3)*16));water.paste(crop.resize((160,128),Image.Resampling.NEAREST),(xx,845))
        d.text((x,982),'Antes                            Depois',font=small,fill='#d8c9af')
    d.text((12,1020),'C do host: fila de animação General, gráficos de portas e correção Tower do GitHub preservados.',font=small,fill='#d8c9af');water.save(OUT/'BattleFrontier_07C_Agua_e_Portas.png')
    dump(OUT/'renders.json',{'maps':6,'camera_pairs':6,'water_cycles':8,'flower_sequence':[0,1,0,2],'native_rgb555':True,'sprites':False,'emulator_screenshots':False,'native_door_footprints':True})
    print('Six native maps, six camera pairs, eight water cycles and three door comparisons rendered.')

if __name__=='__main__':main()
