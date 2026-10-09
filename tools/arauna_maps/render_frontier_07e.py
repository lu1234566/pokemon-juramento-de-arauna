#!/usr/bin/env python3
"""Render six native maps, cameras, full comparisons and all curtain stages."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from frontier_07e_common import ROOT,OUT,NAMES,inventory,render,renderer,require_base
from native_visuals_v2 import dump
from render_frontier_07c import camera

BG=(24,28,32)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',required=True,type=Path);base=ap.parse_args().base.resolve();require_base(base)
    _,bl,bm=inventory(base);_,ls,maps=inventory(ROOT);font=ImageFont.truetype('DejaVuSans.ttf',19);small=ImageFont.truetype('DejaVuSans.ttf',15)
    full={};before={}
    for n in NAMES:
        full[n]=render(ROOT,ls[maps[n]['layout']]);before[n]=render(base,bl[bm[n]['layout']]);full[n].save(OUT/(n+'_After.png'));before[n].save(OUT/(n+'_Before.png'))
    board=Image.new('RGB',(1536,1220),BG);d=ImageDraw.Draw(board);d.text((16,12),'ARAUNA — 07E — BATTLE PIKE — SEIS MAPAS',font=font,fill='#eed6a8')
    for i,n in enumerate(NAMES):
        x=16+i%3*508;y=50 if i<3 else 530;l=ls[maps[n]['layout']]
        d.text((x,y),n.removeprefix('BattleFrontier_Battle')+f' — {l["width"]}×{l["height"]}',font=font,fill='#eed6a8')
        im=full[n];board.paste(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),(x,y+28))
    d.text((16,1190),'Pedra, cobre, tecido vinho e jade. Renders RGB555 nativos, sem atores.',font=small,fill='#d8c9af');board.save(OUT/'BattleFrontier_07E_Seis_Mapas.png')
    paired=Image.new('RGB',(1536,2380),BG);d=ImageDraw.Draw(paired);d.text((16,12),'07E — ORIGINAL EM CIMA / NOVO EMBAIXO — MAPAS COMPLETOS',font=font,fill='#eed6a8')
    for i,n in enumerate(NAMES):
        x=16+i%3*508;y=50 if i<3 else 970;im=full[n]
        d.text((x,y),n.removeprefix('BattleFrontier_Battle'),font=font,fill='#eed6a8')
        for pic,py,tag in ((before[n],y+45,'Original'),(im,y+75+max(full[k].height*2 for k in (NAMES[:3] if i<3 else NAMES[3:])),'07E')):
            d.text((x,py-18),tag,font=small,fill='#d8c9af');paired.paste(pic.resize((pic.width*2,pic.height*2),Image.Resampling.NEAREST),(x,py))
    d.text((16,2355),'Os seis mapas mantêm grids, IDs, eventos e warps. RoomUnused mantém o banco anterior.',font=small,fill='#d8c9af');paired.save(OUT/'BattleFrontier_07E_Antes_Depois.png')
    cams=Image.new('RGB',(1000,2260),BG);d=ImageDraw.Draw(cams);d.text((12,8),'07E — CÂMERA NATIVA 240×160 — ORIGINAL / NOVO',font=font,fill='white')
    for i,n in enumerate(NAMES):
        y=48+i*360;d.text((12,y),n.removeprefix('BattleFrontier_'),font=font,fill='#eed6a8')
        for tag,im,x in [('Before',before[n],12),('After',full[n],508)]:
            crop=camera(im);crop.save(OUT/(n+'_Camera_'+tag+'.png'));cams.paste(crop.resize((480,320),Image.Resampling.NEAREST),(x,y+28))
    d.text((12,2220),'Sem sprites; capturas no emulador e execução de desafios ficam para a integração.',font=small,fill='#d8c9af');cams.save(OUT/'BattleFrontier_07E_Cameras_240x160.png')
    curtain=Image.new('RGB',(1000,670),BG);d=ImageDraw.Draw(curtain);d.text((16,10),'07E — CORTINA — ORIGINAL EM CIMA / NOVO EMBAIXO',font=font,fill='#eed6a8')
    r=renderer(ROOT,ls[maps[NAMES[0]]['layout']]);br=renderer(base,bl[bm[NAMES[0]]['layout']]);states=[]
    lobby=ls[maps[NAMES[0]]['layout']]
    from render_native_map import words
    grid=words(ROOT/lobby['blockdata_filepath'])
    initial=[grid[y*lobby['width']+x]&1023 for y in range(4) for x in range(4,7)]
    for frame in range(4):
        x=20+frame*245;ids=initial if frame==0 else [0x201+xx+yy*8+(frame-1)*32 for yy in range(4) for xx in range(3)];states.append(ids)
        d.text((x,42),'Aberta' if frame==0 else f'Quadro {frame} — tick {frame*4}',font=small,fill='#eed6a8')
        for rr,y in ((br,68),(r,365)):
            patch=Image.new('RGBA',(48,64))
            for i,mid in enumerate(ids):patch.alpha_composite(rr.metatile(mid),(i%3*16,i//3*16))
            curtain.paste(patch.convert('RGB').resize((192,256),Image.Resampling.NEAREST),(x,y))
    d.text((16,638),'Mesmos 36 IDs dinâmicos, três redraws e retomada do script no tick 12. C original validado no host.',font=small,fill='#d8c9af');curtain.save(OUT/'BattleFrontier_07E_Cortina.png')
    dump(OUT/'renders.json',{'maps':6,'whole_map_pairs':6,'camera_pairs':6,'curtain_states':states,'native_rgb555':True,'sprites':False,'emulator_screenshots':False})
    print('Six maps, whole-map pairs, six cameras and original/new curtain states rendered.')

if __name__=='__main__':main()
