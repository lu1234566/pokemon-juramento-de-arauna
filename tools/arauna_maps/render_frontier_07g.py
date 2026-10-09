#!/usr/bin/env python3
"""All ten whole-map pairs and three shared-layout native RGB555 camera pairs."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from frontier_07g_common import ROOT,OUT,NAMES,ROLES,inventory,render,require_base
from native_visuals_v2 import dump
BG=(24,28,32);INK='#eed6a8'
FONT=ImageFont.truetype('DejaVuSans.ttf',20);SMALL=ImageFont.truetype('DejaVuSans.ttf',14)
def title(im,text):ImageDraw.Draw(im).text((16,12),text,font=FONT,fill=INK)
def label(im,x,y,text):ImageDraw.Draw(im).text((x,y),text,font=SMALL,fill=INK)
def camera(im):
    canvas=Image.new('RGB',(240,160),BG);canvas.paste(im,((240-im.width)//2,(160-im.height)//2));return canvas

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    _,bl,bm=inventory(base);_,ls,maps=inventory(ROOT);full={};before={}
    for n in NAMES:
        full[n]=render(ROOT,ls[maps[n]['layout']]);before[n]=render(base,bl[bm[n]['layout']])
        full[n].save(OUT/(n+'_After.png'));before[n].save(OUT/(n+'_Before.png'))
        camera(full[n]).save(OUT/(n+'_Camera_After.png'));camera(before[n]).save(OUT/(n+'_Camera_Before.png'))
    unique=[NAMES[0],NAMES[1],NAMES[-1]];captions=['Lounge estreito — 7 mapas / 9×10','Lounge largo — 2 mapas / 13×8','Casa de Bento — 1 mapa / 6×8'];xs=[16,480,1120]
    board=Image.new('RGB',(1435,625),BG);title(board,'ARAUNA — 07G — LOUNGES E CASA DE BENTO — TRÊS LAYOUTS')
    for n,x,caption in zip(unique,xs,captions):
        label(board,x,52,caption);board.paste(full[n].resize((full[n].width*3,full[n].height*3),Image.Resampling.NEAREST),(x,82))
    label(board,16,588,'Madeira, pedra, tecido e cobre. Dez mapas; compartilhamento original mantido. Frontier: 39/47.');board.save(OUT/'BattleFrontier_07G_Tres_Layouts.png')
    pairs=Image.new('RGB',(1435,1190),BG);title(pairs,'07G — MAPAS COMPLETOS — ORIGINAL EM CIMA / NOVO EMBAIXO')
    for row,pics in enumerate((before,full)):
        y=52+row*550
        for n,x,caption in zip(unique,xs,captions):
            label(pairs,x,y,caption);im=pics[n];pairs.paste(im.resize((im.width*3,im.height*3),Image.Resampling.NEAREST),(x,y+28))
    label(pairs,16,1158,'886 células nos dez mapas; 242 células únicas. Mesmos IDs, atributos, eventos, saídas e serviços.');pairs.save(OUT/'BattleFrontier_07G_Antes_Depois.png')
    ten=Image.new('RGB',(2160,1080),BG);title(ten,'07G — DEZ MAPAS — FUNÇÕES PRESERVADAS')
    for i,(n,role) in enumerate(zip(NAMES,ROLES)):
        x=16+i%5*430;y=54+i//5*485;label(ten,x,y,'Casa de Bento (ScottsHouse)' if i==9 else 'Lounge '+str(i+1));label(ten,x,y+22,role)
        im=full[n];im=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST);ten.paste(im,(x,y+54))
        label(ten,x,y+390,f"{len(maps[n]['object_events'])} objetos · {len(maps[n]['warp_events'])} warps · {ls[maps[n]['layout']]['width']}×{ls[maps[n]['layout']]['height']}")
    label(ten,16,1048,'Renders dos bancos 4bpp em RGB555, sem atores. Os mapas compartilham três layouts; não são fotos do mGBA.');ten.save(OUT/'BattleFrontier_07G_Dez_Mapas.png')
    cameras=Image.new('RGB',(1010,1160),BG);title(cameras,'07G — QUADRO 240×160 — ORIGINAL À ESQUERDA / NOVO À DIREITA')
    for i,n in enumerate(unique):
        y=52+i*355;label(cameras,16,y,captions[i])
        for im,x in ((before[n],16),(full[n],520)):cameras.paste(camera(im).resize((480,320),Image.Resampling.NEAREST),(x,y+24))
    label(cameras,16,1132,'Salas menores que a tela são centralizadas. Sem sprites, sem enquadramento do motor e sem emulação.');cameras.save(OUT/'BattleFrontier_07G_Cameras_240x160.png')
    anim=Image.new('RGB',(980,650),BG);title(anim,'07G — TV BUILDING — TRÊS QUADROS NATIVOS PRESERVADOS')
    for frame in range(3):
        x=16+frame*320;label(anim,x,52,f'Quadro {frame}')
        for repo,layout,y in ((base,bl[bm[NAMES[0]]['layout']],82),(ROOT,ls[maps[NAMES[0]]['layout']],350)):
            im=render(repo,layout,frame);im=im.crop((48,0,96,64)).resize((192,256),Image.Resampling.NEAREST);anim.paste(im,(x,y))
    label(anim,16,620,'Original em cima / novo embaixo. Metatile 0x002 e slots VRAM 496–499 continuam nativos.');anim.save(OUT/'BattleFrontier_07G_Animacao_TV.png')
    dump(OUT/'renders.json',{'frontier_maps':10,'unique_layouts':3,'whole_map_pairs':10,'camera_pairs':10,'displayed_unique_camera_pairs':3,'tv_frames':3,'native_rgb555':True,'sprites':False,'emulator_screenshots':False,'camera_padding':'Centered 240×160 field, not engine viewport.'})
    print('Ten native whole-map and camera pairs, three shared layouts and TV frames rendered.')

if __name__=='__main__':main()
