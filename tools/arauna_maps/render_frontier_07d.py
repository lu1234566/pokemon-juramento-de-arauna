#!/usr/bin/env python3
"""Native whole-map and 240x160 before/after boards for the three Factory rooms."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from frontier_07d_common import ROOT,OUT,NAMES,inventory,render,require_base
from native_visuals_v2 import dump
from render_frontier_07c import camera

BG=(24,28,32)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',required=True,type=Path);base=ap.parse_args().base.resolve();require_base(base)
    _,bl,bm=inventory(base);_,ls,maps=inventory(ROOT);font=ImageFont.truetype('DejaVuSans.ttf',20);small=ImageFont.truetype('DejaVuSans.ttf',16)
    full={};before={}
    for n in NAMES:
        l=ls[maps[n]['layout']];full[n]=render(ROOT,l);before[n]=render(base,bl[bm[n]['layout']]);full[n].save(OUT/(n+'_After.png'));before[n].save(OUT/(n+'_Before.png'))
    board=Image.new('RGB',(1984,590),BG);d=ImageDraw.Draw(board);d.text((16,12),'ARAUNA — 07D — BATTLE FACTORY — TRÊS MAPAS',font=font,fill='#eed6a8')
    for i,n in enumerate(NAMES):
        x=16+i*656;l=ls[maps[n]['layout']];d.text((x,48),n.removeprefix('BattleFrontier_Battle')+f' — {l["width"]}×{l["height"]}',font=font,fill='#eed6a8');im=full[n]
        board.paste(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),(x,82))
    d.text((16,552),'Pedra escura, cobre, painéis jade e marca de calibração. Bancos RGB555 nativos. Sem atores.',font=small,fill='#d8c9af');board.save(OUT/'BattleFrontier_07D_Tres_Mapas.png')
    paired=Image.new('RGB',(1984,1100),BG);d=ImageDraw.Draw(paired);d.text((16,12),'07D — MAPAS COMPLETOS — ORIGINAL EM CIMA / NOVO EMBAIXO',font=font,fill='#eed6a8')
    for i,n in enumerate(NAMES):
        x=16+i*656;d.text((x,48),n.removeprefix('BattleFrontier_Battle'),font=font,fill='#eed6a8')
        for im,y,tag in ((before[n],96,'Original'),(full[n],600,'07D')):
            d.text((x,y-24),tag,font=small,fill='#d8c9af');paired.paste(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),(x,y))
    d.text((16,1070),'Mesmos layouts, grids, atributos e máscaras; apenas três pares de referências trocam para o banco privado.',font=small,fill='#d8c9af');paired.save(OUT/'BattleFrontier_07D_Antes_Depois.png')
    cameras=Image.new('RGB',(1000,1160),BG);d=ImageDraw.Draw(cameras);d.text((12,8),'07D — CÂMERA NATIVA 240×160 — ORIGINAL / NOVO',font=font,fill='white')
    for i,n in enumerate(NAMES):
        y=48+i*360;d.text((12,y),n.removeprefix('BattleFrontier_'),font=font,fill='#eed6a8')
        for tag,im,x in [('Before',before[n],12),('After',full[n],508)]:
            crop=camera(im);crop.save(OUT/(n+'_Camera_'+tag+'.png'));cameras.paste(crop.resize((480,320),Image.Resampling.NEAREST),(x,y+28))
    d.text((12,1130),'Renders RGB555 sem sprites. Execução de partidas e captura no mGBA ficam para a integração.',font=small,fill='#d8c9af');cameras.save(OUT/'BattleFrontier_07D_Cameras_240x160.png')
    dump(OUT/'renders.json',{'maps':3,'whole_map_pairs':3,'camera_pairs':3,'native_rgb555':True,'sprites':False,'emulator_screenshots':False,'whole_maps_original_above_new_below':True})
    print('Three native maps, three whole-map comparisons and three 240x160 camera pairs rendered.')

if __name__=='__main__':main()
