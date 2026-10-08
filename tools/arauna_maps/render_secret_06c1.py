#!/usr/bin/env python3
"""Native RGB555 map previews and production-C decoration fixtures."""
import argparse,json,tempfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from secret_06c1_common import *
from secret_06c1_c_checks import compile_native,load

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    _,bl,bm=inventory(base);_,ls,ms=inventory(ROOT);old={};new={};fixtures={};records={}
    font=ImageFont.truetype('DejaVuSans.ttf',17);small=ImageFont.truetype('DejaVuSans.ttf',13)
    for n in NAMES:
        old[n]=render(base,bl[bm[n]['layout']]);new[n]=render(ROOT,ls[ms[n]['layout']])
        for tag,data in (('Before',old),('After',new)):data[n].save(OUT/(n+'_'+tag+'.png'))
    board=Image.new('RGB',(1320,1410),(22,27,32));d=ImageDraw.Draw(board)
    d.text((16,12),'ARAUNA 06C1 — 16 BASES EM CAVERNAS',font=font,fill='white')
    labels={'Red':'Laterita','Brown':'Arenito','Blue':'Basalto','Yellow':'Calcário'}
    for i,n in enumerate(NAMES):
        x=16+i%4*326;y=50+i//4*326;im=new[n];scale=min(304//im.width,278//im.height);scale=max(1,scale)
        d.text((x,y),n.removeprefix('SecretBase_')+' / '+labels[COLORS[i//4]],font=small,fill='#eddfc6');board.paste(im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST),(x,y+24))
    d.text((16,1380),'RGB555 nativo. Sem atores, clima ou captura de emulador. Geometrias e dados preservados.',font=small,fill='#bfd0d0');board.save(OUT/'SecretBases_06C1_16_Mapas.png')
    compare=Image.new('RGB',(1060,1490),(22,27,32));d=ImageDraw.Draw(compare);d.text((16,10),'ANTES / DEPOIS — quatro materiais de Arauna',font=font,fill='white')
    for i,c in enumerate(COLORS):
        n=f'SecretBase_{c}Cave1';y=46+i*352;d.text((16,y),labels[c]+' — '+n,font=font,fill='#eddfc6')
        for x,im in ((16,old[n]),(540,new[n])):
            scale=min(496//im.width,304//im.height);compare.paste(im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST),(x,y+27))
    d.text((16,1460),'A arte muda em bancos privados. Paletas das decorações e computador mantidas.',font=small,fill='#bfd0d0');compare.save(OUT/'SecretBases_06C1_Antes_Depois.png')
    with tempfile.TemporaryDirectory() as temp:
        dll,_=compile_native(Path(temp))
        for c in COLORS:
            n=f'SecretBase_{c}Cave4';l=ls[ms[n]['layout']];load(dll,ROOT,l);placed=[]
            # Existing native catalog: desk, chair, plant, mat and wall poster.
            for deco in (1,10,19,48,66):
                candidates=[(x,y) for y in range(1,l['height']-1) for x in range(1,l['width']-1) if dll.can_place(deco,x,y,0)]
                if not candidates:continue
                x,y=candidates[len(candidates)//2];dll.show(deco,x,y);placed.append({'decoration':deco,'x':x,'y':y})
            grid=[dll.cell(x,y) for y in range(l['height']) for x in range(l['width'])];fixtures[c]=render(ROOT,l,grid);fixtures[c].save(OUT/(n+'_Decoration_Fixture.png'));records[n]=placed
    board=Image.new('RGB',(1110,970),(22,27,32));d=ImageDraw.Draw(board);d.text((16,12),'DECORAÇÕES NATIVAS — cenas de teste, não instaladas',font=font,fill='white')
    for i,c in enumerate(COLORS):
        x=16+i%2*550;y=52+i//2*420;im=fixtures[c];scale=min(520//im.width,360//im.height);d.text((x,y),labels[c]+' — '+str(len(records[f'SecretBase_{c}Cave4']))+' itens',font=font,fill='#eddfc6');board.paste(im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST),(x,y+28))
    d.text((16,923),'Itens escolhidos por CanPlaceDecoration e escritos por ShowDecorationOnMap, funções C do jogo.',font=small,fill='#bfd0d0');d.text((16,947),'Os saves e os grids instalados permanecem intactos. Dolls e NPCs dependem do motor de sprites.',font=small,fill='#bfd0d0');board.save(OUT/'SecretBases_06C1_Decoracoes.png')
    (OUT/'renders.json').write_text(json.dumps({'map_pairs':16,'boards':3,'decoration_fixtures':records,'scope':'Native RGB555. Decoration fixtures use production C; they are previews only, never installed into grids or saves. No engine actors/weather or emulator.'},indent=2)+'\n')
    print(json.dumps({'map_pairs':16,'decoration_fixtures':len(records),'boards':3}))
if __name__=='__main__':main()
