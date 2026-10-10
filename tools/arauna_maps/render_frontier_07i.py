#!/usr/bin/env python3
"""Whole exterior pairs, nine landmark cameras and all sixteen native door frames."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from native_visuals_v2 import dump
from frontier_07i_common import ROOT,OUT,NAMES,ROLES,inventory,render,require_base,door_records
from frontier_07i_c_checks import door_frame,door_table
from render_native_map import words
BG=(24,28,32);INK='#eed6a8';FONT=ImageFont.truetype('DejaVuSans.ttf',19);SMALL=ImageFont.truetype('DejaVuSans.ttf',14)
def label(im,x,y,s,big=False):ImageDraw.Draw(im).text((x,y),s,font=FONT if big else SMALL,fill=INK)
def save(im,path):
    # Lossless indexed previews where all RGB555 colors fit in one PNG palette.
    if im.getcolors(maxcolors=256) is not None:
        indexed=im.convert('P',palette=Image.Palette.ADAPTIVE,colors=256)
        assert indexed.convert('RGB').tobytes()==im.convert('RGB').tobytes()
        indexed.save(path,optimize=True,compress_level=9)
    else:im.save(path,optimize=True,compress_level=9)
def camera(im,x,y):
    out=Image.new('RGB',(240,160),BG);out.paste(im,(120-x*16-8,80-y*16-8));return out
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    _,bl,bm=inventory(base);_,ls,ms=inventory(ROOT);full={};before={}
    for n in NAMES:
        a=render(base,bl[bm[n]['layout']]);b=render(ROOT,ls[ms[n]['layout']]);full[n]=b;before[n]=a
        for im,s in ((a,'Before'),(b,'After')):save(im,OUT/(n+'_'+s+'.png'))
        board=Image.new('RGB',(a.width*2+48,a.height+95),BG);label(board,16,12,n+' — ORIGINAL À ESQUERDA / NOVO À DIREITA',True);board.paste(a,(16,52));board.paste(b,(a.width+32,52));label(board,16,a.height+65,'Arte nativa RGB555 sem atores. Mesmas dimensões, células, atributos, eventos e destinos.');save(board,OUT/(n+'_Antes_Depois.png'))
    joined=Image.new('RGB',(2048,1250),BG);label(joined,16,12,'ARAUNA — FRONTIER 47/47 — WEST + EAST — CONEXÃO ORIGINAL',True);joined.paste(full[NAMES[1]],(0,52));joined.paste(full[NAMES[0]],(896,52));label(joined,16,1218,'Terraços de pedra, cerâmica, bronze, vegetação, canais. Portas, água e bandeiras nativas preservadas.');save(joined,OUT/'BattleFrontier_07I_Exteriores_Conectados.png')
    landmarks=[(0,16,14,'Torre'),(0,39,29,'Arena'),(0,45,56,'Palace'),(0,58,14,'Pyramid'),(1,19,17,'Dome'),(1,11,38,'Factory'),(1,42,27,'Pike'),(2,4,7,'Recepção — centro'),(2,4,12,'Recepção — entrada')]
    cameras=Image.new('RGB',(1010,len(landmarks)*350+90),BG);label(cameras,16,12,'07I — 240×160 — ORIGINAL À ESQUERDA / NOVO À DIREITA',True)
    for i,(idx,x,y,role) in enumerate(landmarks):
        n=NAMES[idx];yy=52+i*350;label(cameras,16,yy,role)
        for pic,xx in ((before[n],16),(full[n],520)):cameras.paste(camera(pic,x,y).resize((480,320),Image.Resampling.NEAREST),(xx,yy+24))
    label(cameras,16,cameras.height-28,'Recortes dos bancos 4bpp sem sprites; não são screenshots de emulador.');save(cameras,OUT/'BattleFrontier_07I_Cameras_240x160.png')
    records=door_records(base);lookup=door_table(ROOT);gallery=Image.new('RGB',(1160,len(records)*200+100),BG);label(gallery,16,12,'07I — AS 16 PORTAS ANIMADAS — PIXELS E PALETAS NATIVOS',True)
    captions=['Original fechado','Novo fechado','Novo — quadro 0','Novo — quadro 1','Novo — quadro 2']
    for c,t in enumerate(captions):label(gallery,16+c*228,42,t)
    for i,d in enumerate(records):
        n=d['map'];y=68+i*200;label(gallery,16,y,n.removeprefix('BattleFrontier_')+f" ({d['x']},{d['y']}) / 0x{d['id']:03X} → "+d['destination'].removeprefix('MAP_BATTLE_FRONTIER_'))
        rect=((d['x']-3)*16,(d['y']-3)*16,(d['x']+4)*16,(d['y']+2)*16)
        pictures=[before[n],full[n]]
        for frame in range(3):
            pic=full[n].copy();pic.paste(door_frame(ROOT,d,frame,lookup),(d['x']*16,(d['y']-1)*16));pictures.append(pic)
        for c,pic in enumerate(pictures):gallery.paste(pic.crop(rect).resize((224,160),Image.Resampling.NEAREST),(16+c*228,y+22))
    label(gallery,16,gallery.height-28,'Quadros reais 4bpp com paletas originais. Composição nativa; tarefas e sprites do GBA não foram executados.');save(gallery,OUT/'BattleFrontier_07I_Portas_16.png')
    animations=Image.new('RGB',(1040,580),BG);label(animations,16,12,'07I — QUATRO QUADROS ORIGINAIS DAS BANDEIRAS',True)
    for row,n in enumerate(NAMES[:2]):
        l=ls[ms[n]['layout']];g=words(ROOT/l['blockdata_filepath']);b=__import__('json').loads((OUT/'build.json').read_text())['banks'][row]
        from frontier_07i_common import renderer
        r=renderer(ROOT,l,-1);flagids={mid for mid in b['animated_ids'] if any(730<=e&1023<736 for e in r.secondary_metatiles[(mid-512)*8:(mid-512)*8+8]) if mid>=512};index=next(i for i,v in enumerate(g) if v&1023 in flagids);x=index%l['width'];y=index//l['width'];label(animations,16,52+row*250,n)
        for f in range(4):
            im=render(ROOT,l,f).crop((x*16,(y-1)*16,(x+3)*16,(y+2)*16));animations.paste(im.resize((192,192),Image.Resampling.NEAREST),(16+f*250,78+row*250))
    label(animations,16,552,'Callbacks e slots 730–735 preservados; água General conserva os oito quadros.');save(animations,OUT/'BattleFrontier_07I_Bandeiras.png')
    dump(OUT/'renders.json',{'whole_map_pairs':3,'landmark_camera_pairs':9,'animated_doors':16,'closed_and_three_open_frames':64,'flag_frames_per_side':4,'native_rgb555':True,'sprites':False,'emulator_screenshots':False,'door_task_playback':False})
    print('07I: whole-map pairs, connected exterior, nine cameras, all door and flag frames.')
if __name__=='__main__':main()
