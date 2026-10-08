#!/usr/bin/env python3
"""Seven map pairs and every live generated challenge, RGB555 without actors."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from trainer_hill_06a_common import BASE,ROOT,OUT,NAMES,MODES,inventory,renderer,render_words,floors,runtime_words
from render_native_map import words
from native_visuals_v2 import dump

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve()
    _,oldls,oldmaps=inventory(base);_,ls,maps=inventory(ROOT);OUT.mkdir(parents=True,exist_ok=True)
    font=ImageFont.truetype('DejaVuSans.ttf',16);small=ImageFont.truetype('DejaVuSans.ttf',13)
    new_floors=floors(ROOT);old_floors=floors(base);full={};before={}
    for n in NAMES:
        l=ls[maps[n]['layout']];old=oldls[oldmaps[n]['layout']]
        if n.endswith(('1F','2F','3F','4F')):
            key='normal_'+str(int(n[-2])-1);l,g=runtime_words(ROOT,new_floors[key]);old,oldg=runtime_words(base,old_floors[key])
        else:g=words(ROOT/l['blockdata_filepath']);oldg=words(base/old['blockdata_filepath'])
        full[n]=render_words(ROOT,l,g);before[n]=render_words(base,old,oldg)
        full[n].save(OUT/(n+'_After.png'));before[n].save(OUT/(n+'_Before.png'))
    overview=Image.new('RGB',(1256,1286),(23,27,30));d=ImageDraw.Draw(overview)
    for i,n in enumerate(NAMES):
        x=12+(i%3)*416;y=12+(i//3)*420;d.text((x,y),n.removeprefix('TrainerHill_'),font=font,fill='white');im=full[n]
        ratio=min(396/im.width,374/im.height);size=(round(im.width*ratio),round(im.height*ratio));overview.paste(im.resize(size,Image.Resampling.NEAREST),(x,y+28))
    d.text((12,1260),'Dados nativos RGB555; andares no modo Normal; sem sprites. Não é captura de emulador.',font=small,fill='#d1c5a4')
    overview.save(OUT/'TrainerHill_06A_Sete_Mapas.png')
    board=Image.new('RGB',(1136,1540),(23,27,30));d=ImageDraw.Draw(board)
    for mi,mode in enumerate(MODES):
        for floor in range(4):
            key=mode+'_'+str(floor);l,g=runtime_words(ROOT,new_floors[key]);old,oldg=runtime_words(base,old_floors[key]);a=render_words(ROOT,l,g);b=render_words(base,old,oldg)
            a.save(OUT/(key+'_After.png'));b.save(OUT/(key+'_Before.png'))
            x=12+floor*282;y=12+mi*382;d.text((x,y),mode.title()+' — '+str(floor+1)+'F',font=font,fill='#e9d8b4');board.paste(a,(x,y+26))
    d.text((12,1515),'16 combinações do desafio — grades confirmadas com o gerador C real; renders sem atores.',font=small,fill='#d1c5a4')
    board.save(OUT/'TrainerHill_06A_Dezesseis_Desafios.png')
    cameras=Image.new('RGB',(1000,2612),(23,27,30));d=ImageDraw.Draw(cameras)
    d.text((12,8),'TRAINER HILL 06A — ANTES / DEPOIS — recortes 240×160 sem sprites',font=font,fill='white')
    records=[]
    origins={'TrainerHill_Entrance':(2,7),'TrainerHill_Roof':(5,0),'TrainerHill_Elevator':(0,0)}
    for i,n in enumerate(NAMES):
        x,y=origins.get(n,(0,5));yy=42+i*364;d.text((12,yy),n,font=font,fill='#e9d8b4')
        for tag,im,xx in [('Before',before[n],12),('After',full[n],508)]:
            if im.width<240 or im.height<160:
                crop=Image.new('RGB',(240,160));crop.paste(im,((240-im.width)//2,(160-im.height)//2))
            else:crop=im.crop((x*16,y*16,x*16+240,y*16+160))
            crop.save(OUT/(n+'_Camera_'+tag+'.png'));cameras.paste(crop.resize((480,320),Image.Resampling.NEAREST),(xx,yy+24))
        records.append({'map':n,'origin':[x,y],'size':[240,160],'generated_mode':'normal' if n.endswith(('1F','2F','3F','4F')) else None,'small_elevator_centered':n.endswith('Elevator')})
    cameras.save(OUT/'TrainerHill_06A_Cameras.png')
    dump(OUT/'renders.json',{'kind':'native RGB555 renderer, without actors, not emulator screenshots','map_pairs':7,'generated_mode_floor_pairs':16,'camera_pairs':records,'source_layouts_private_elevator':True})
    print('7 before/after map pairs; 16 live generated challenges; 7 native 240x160 camera pairs.')

if __name__=='__main__':main()
