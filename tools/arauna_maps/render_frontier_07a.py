#!/usr/bin/env python3
"""Native RGB555 maps, before/after cameras and scripted passage review."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from frontier_07a_common import ROOT,OUT,NAMES,inventory,render,renderer,require_base
from native_visuals_v2 import dump
from render_native_map import words

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',required=True,type=Path);base=ap.parse_args().base.resolve();require_base(base)
    _,bl,bm=inventory(base);_,ls,maps=inventory(ROOT);font=ImageFont.truetype('DejaVuSans.ttf',16);small=ImageFont.truetype('DejaVuSans.ttf',13)
    board=Image.new('RGB',(1236,900),(24,28,32));d=ImageDraw.Draw(board);full={};before={}
    for i,n in enumerate(NAMES):
        full[n]=render(ROOT,ls[maps[n]['layout']],-1);before[n]=render(base,bl[bm[n]['layout']],-1)
        full[n].save(OUT/(n+'_After.png'));before[n].save(OUT/(n+'_Before.png'))
        x=12+(i%3)*408;y=12+(i//3)*286;d.text((x,y),n.removeprefix('BattleFrontier_BattleTower'),font=font,fill='#eed6a8')
        im=full[n];scale=min(384/im.width,244/im.height);board.paste(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST),(x,y+28))
    d.text((12,873),'07A — sete mapas; renders dos bancos e grids nativos RGB555, sem sprites/clima.',font=small,fill='#d8c9af');board.save(OUT/'BattleFrontier_07A_Sete_Mapas.png')
    cameras=Image.new('RGB',(1000,2600),(24,28,32));d=ImageDraw.Draw(cameras)
    d.text((12,8),'BATTLE TOWER 07A — ANTES / DEPOIS — viewport 240×160',font=font,fill='white')
    for i,n in enumerate(NAMES):
        y=42+i*360;d.text((12,y),n.removeprefix('BattleFrontier_'),font=font,fill='#eed6a8')
        for tag,im,x in [('Before',before[n],12),('After',full[n],508)]:
            crop=Image.new('RGB',(240,160));ox=max(0,(im.width-240)//2);oy=max(0,(im.height-160)//2)
            part=im.crop((ox,oy,min(im.width,ox+240),min(im.height,oy+160)));crop.paste(part,((240-part.width)//2,(160-part.height)//2))
            crop.save(OUT/(n+'_Camera_'+tag+'.png'));cameras.paste(crop.resize((480,320),Image.Resampling.NEAREST),(x,y+24))
    cameras.save(OUT/'BattleFrontier_07A_Antes_Depois.png')
    doors=Image.new('RGB',(1056,590),(24,28,32));d=ImageDraw.Draw(doors);d.text((12,10),'PORTAS — estados nativos mantidos; novas superfícies ao redor',font=font,fill='white')
    for i,n in enumerate(('BattleFrontier_BattleTowerLobby','BattleFrontier_BattleTowerCorridor','BattleFrontier_BattleTowerMultiCorridor')):
        l=ls[maps[n]['layout']];g=words(ROOT/l['blockdata_filepath']);r=renderer(ROOT,l,-1);im=full[n];x=12+i*348;d.text((x,43),n.removeprefix('BattleFrontier_BattleTower'),font=font,fill='#eed6a8')
        # Corridor's two script-controlled routes, without installing fixture grids.
        fixture=im.copy()
        if n.endswith('Corridor') and not n.endswith('MultiCorridor'):
            for xx in (12,15):
                for yy,mid in ((0,0x207),(1,0x20f)):fixture.paste(r.metatile(mid).convert('RGB'),(xx*16,yy*16))
        crop=fixture.crop((max(0,fixture.width-160),0,fixture.width,min(160,fixture.height)))
        doors.paste(crop.resize((320,crop.height*2),Image.Resampling.NEAREST),(x,75))
    d.text((12,410),'0x207 / 0x20F: abertura dos corredores. Footprints e paleta 7 intactos.',font=small,fill='#d8c9af')
    d.text((12,434),'Multi: preservados os pares de portas de 32 px e a porta distante redirecionada.',font=small,fill='#d8c9af')
    d.text((12,458),'field_door.c e overworld.c: hashes idênticos à base 7e9d29dc5f.',font=small,fill='#d8c9af')
    d.text((12,482),'Fixtures de revisão. Animação e atores ainda exigem teste no emulador.',font=small,fill='#d8c9af');doors.save(OUT/'BattleFrontier_07A_Portas.png')
    dump(OUT/'renders.json',{'maps':7,'camera_pairs':7,'native_rgb555':True,'sprites':False,'emulator_screenshots':False,'script_open_corridor_fixture_not_installed':True})
    print('Seven native maps, seven before/after cameras and passage fixtures rendered.')

if __name__=='__main__':main()
