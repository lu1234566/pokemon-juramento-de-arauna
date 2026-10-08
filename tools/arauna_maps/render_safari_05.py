#!/usr/bin/env python3
"""Full maps, connected reserve and native 240x160 before/after viewports."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from safari_05_common import ROOT,OUT,NAMES,EXTERIORS,inventory,render
from native_visuals_v2 import dump

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve()
 _,oldls,maps=inventory(base);_,ls,_=inventory(ROOT);font=ImageFont.truetype('DejaVuSans.ttf',17)
 names={'SafariZone_Northwest':'Noroeste — platôs e lago','SafariZone_North':'Norte — encosta e comedouros','SafariZone_Northeast':'Nordeste — expansão da mata','SafariZone_Southwest':'Sudoeste — margem e pouso','SafariZone_South':'Sul — trilha de entrada','SafariZone_Southeast':'Sudeste — lagos e capinzal','SafariZone_RestHouse':'Casa de descanso','Route121_SafariZoneEntrance':'Recepção da Rota 121'}
 targets={'SafariZone_Northwest':(18,0),'SafariZone_North':(0,22),'SafariZone_Northeast':(4,5),'SafariZone_Southwest':(23,2),'SafariZone_South':(10,23),'SafariZone_Southeast':(23,9),'SafariZone_RestHouse':(0,0),'Route121_SafariZoneEntrance':(4,1)}
 full={};before={};records=[]
 for n in NAMES:
  l=ls[maps[n]['layout']];full[n]=render(ROOT,l);before[n]=render(base,oldls[l['id']])
  full[n].save(OUT/(n+'_After.png'));before[n].save(OUT/(n+'_Before.png'))
 overview=Image.new('RGB',(1296,1492),(19,28,35));d=ImageDraw.Draw(overview)
 for i,n in enumerate(NAMES):
  x=16+(i%3)*432;y=16+(i//3)*490;d.text((x,y),names[n],font=font,fill='white');im=full[n];ratio=min(400/im.width,440/im.height);size=(int(im.width*ratio),int(im.height*ratio));overview.paste(im.resize(size,Image.Resampling.NEAREST),(x,y+30))
 overview.save(OUT/'Safari_05_Oito_Mapas.png')
 joined=Image.new('RGB',(1920,1280))
 for i,n in enumerate(EXTERIORS):joined.paste(full[n],(i%3*640,i//3*640))
 joined.save(OUT/'Safari_05_Reserva_Conectada.png')
 # Two review boards with eight exact camera windows, enlarged only for display.
 boards=[]
 for part in range(2):
  sheet=Image.new('RGB',(1016,1532),(19,28,35));d=ImageDraw.Draw(sheet);d.text((16,8),'SAFARI V1 — ANTES / DEPOIS — dados nativos, sem sprites',font=font,fill='white')
  for k,n in enumerate(NAMES[part*4:(part+1)*4]):
   x,y=targets[n];yy=42+k*365;d.text((16,yy),names[n],font=font,fill='#bdd0c4')
   for tag,im,xx in [('Before',before[n],16),('After',full[n],516)]:
    if im.width<240 or im.height<160:
     canvas=Image.new('RGB',(240,160));canvas.paste(im,((240-im.width)//2,(160-im.height)//2));crop=canvas
    else:crop=im.crop((x*16,y*16,x*16+240,y*16+160))
    crop.save(OUT/(n+'_Camera_'+tag+'.png'));sheet.paste(crop.resize((480,320),Image.Resampling.NEAREST),(xx,yy+27))
   records.append({'map':n,'origin':[x,y],'size':[240,160],'small_interior_centered':n=='SafariZone_RestHouse'})
  sheet.save(OUT/f'Safari_05_Cameras_{part+1}.png')
  boards.append(sheet)
 combined=Image.new('RGB',(1016,3064),(19,28,35))
 for i,sheet in enumerate(boards):combined.paste(sheet,(0,i*1532))
 combined.save(OUT/'Safari_05_Cameras_Completas.png')
 dump(OUT/'renders.json',{'kind':'native host renderer, RGB555, no actor sprites, not emulator screenshots','maps':8,'connected_exterior_maps':6,'camera_pairs':records})
 print('8 before/after maps; connected 6-sector reserve; 8 native camera pairs.')

if __name__=='__main__':main()
