#!/usr/bin/env python3
"""Every Navel map plus stage board and native RGB555 camera comparisons."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from native_visuals_v2 import dump
from navel_06b_common import BASE,ROOT,OUT,NAMES,inventory,render

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',required=True,type=Path);base=ap.parse_args().base.resolve()
    _,bl,bm=inventory(base);_,ls,maps=inventory(ROOT);OUT.mkdir(parents=True,exist_ok=True);font=ImageFont.truetype('DejaVuSans.ttf',16);small=ImageFont.truetype('DejaVuSans.ttf',13)
    new={};old={}
    for n in NAMES:
        new[n]=render(ROOT,ls[maps[n]['layout']]);old[n]=render(base,bl[bm[n]['layout']])
        new[n].save(OUT/(n+'_After.png'));old[n].save(OUT/(n+'_Before.png'))
    board=Image.new('RGB',(1256,1900),(21,26,31));d=ImageDraw.Draw(board)
    names=('NavelRock_Exterior','NavelRock_Harbor','NavelRock_Entrance','NavelRock_B1F','NavelRock_Top','NavelRock_Bottom')
    for i,n in enumerate(names):
        x=12+i%2*416;y=12+i//2*616;im=new[n];ratio=min(396/im.width,570/im.height)
        d.text((x,y),n.removeprefix('NavelRock_'),font=font,fill='#e7dfc8');board.paste(im.resize((round(im.width*ratio),round(im.height*ratio)),Image.Resampling.NEAREST),(x,y+28))
    n='NavelRock_Fork';im=new[n];ratio=min(396/im.width,1780/im.height);d.text((844,12),'Fork — planta completa',font=font,fill='#e7dfc8');board.paste(im.resize((round(im.width*ratio),round(im.height*ratio)),Image.Resampling.NEAREST),(844,40))
    d.text((12,1870),'Dados nativos RGB555, sem atores ou iluminação do motor; não é captura de emulador.',font=small,fill='#bbc9c9');board.save(OUT/'NavelRock_06B_Locais_Chave.png')
    stairs=Image.new('RGB',(1220,1190),(21,26,31));d=ImageDraw.Draw(stairs)
    order=[*(f'NavelRock_Up{i}' for i in range(1,5)),*(f'NavelRock_Down{i:02}' for i in range(1,12))]
    for i,n in enumerate(order):
        x=12+i%4*304;y=12+i//4*292;d.text((x,y),n.removeprefix('NavelRock_'),font=font,fill='#e7dfc8');stairs.paste(new[n].resize((288,256),Image.Resampling.NEAREST),(x,y+24))
    d.text((12,1170),'4 salas de subida e 11 de descida; geometrias e escadas nativas preservadas.',font=small,fill='#bbc9c9');stairs.save(OUT/'NavelRock_06B_Subida_e_Descida.png')
    def camera(im,x,y):
        if im.width<240 or im.height<160:
            crop=Image.new('RGB',(240,160));crop.paste(im,((240-im.width)//2,(160-im.height)//2));return crop
        return im.crop((x*16,y*16,x*16+240,y*16+160))
    crops={};records=[]
    explicit={'NavelRock_Exterior':(3,5),'NavelRock_Harbor':(1,1),'NavelRock_Top':(5,4),'NavelRock_Bottom':(4,10)}
    for n in NAMES:
        l=ls[maps[n]['layout']];w=maps[n]['warp_events'][0];x,y=explicit.get(n,(max(0,min(l['width']-15,w['x']-7)),max(0,min(l['height']-10,w['y']-5))))
        for tag,source in (('Before',old),('After',new)):
            crop=camera(source[n],x,y);crops[n+'_'+tag]=crop;crop.save(OUT/(n+'_Camera_'+tag+'.png'))
        records.append({'map':n,'origin':[x,y],'size':[240,160],'small_map_centered':l['width']<15 or l['height']<10})
    for suffix,x in (('ForkWest',0),('ForkEast',12)):
        for tag,source in (('Before',old),('After',new)):
            crop=camera(source['NavelRock_Fork'],x,0);crops[suffix+'_'+tag]=crop;crop.save(OUT/(suffix+'_Camera_'+tag+'.png'))
        records.append({'map':'NavelRock_Fork','detail':suffix,'origin':[x,0],'size':[240,160]})
    camera_names=('NavelRock_Exterior','NavelRock_Harbor','NavelRock_Entrance','ForkWest','ForkEast','NavelRock_Up4','NavelRock_Down11','NavelRock_Top','NavelRock_Bottom')
    cameras=Image.new('RGB',(1000,3320),(21,26,31));d=ImageDraw.Draw(cameras);d.text((12,8),'NAVEL ROCK 06B — ANTES / DEPOIS — recortes 240×160',font=font,fill='white')
    for i,n in enumerate(camera_names):
        yy=42+i*362;d.text((12,yy),n,font=font,fill='#e7dfc8')
        for tag,xx in (('Before',12),('After',508)):cameras.paste(crops[n+'_'+tag].resize((480,320),Image.Resampling.NEAREST),(xx,yy+24))
    cameras.save(OUT/'NavelRock_06B_Cameras.png');dump(OUT/'renders.json',{'kind':'Native RGB555, no actors or engine weather; not emulator screenshots. Small maps centered with black padding in camera previews.','map_pairs':22,'core_maps':21,'dependent_harbor':1,'camera_pairs':records,'concept_is_material_reference_only':True})
    print(json.dumps({'map_pairs':22,'camera_pairs':len(records),'boards':3}))
if __name__=='__main__':main()
