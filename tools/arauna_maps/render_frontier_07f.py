#!/usr/bin/env python3
"""Whole native maps, original-C generated floors, all modules and actual 240x160 crops."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from frontier_07f_common import ROOT,OUT,NAMES,SQUARES,inventory,render,render_grid,renderer,require_base
from native_visuals_v2 import dump
from render_native_map import words

BG=(24,28,32);INK='#eed6a8'
FONT=ImageFont.truetype('DejaVuSans.ttf',20);SMALL=ImageFont.truetype('DejaVuSans.ttf',15)

def title(im,text):ImageDraw.Draw(im).text((16,12),text,font=FONT,fill=INK)
def label(im,x,y,text):ImageDraw.Draw(im).text((x,y),text,font=SMALL,fill=INK)
def camera(im,x,y):
    cx=max(0,min(x*16+8-120,im.width-240));cy=max(0,min(y*16+8-80,im.height-160))
    if im.width<240 or im.height<160:
        canvas=Image.new('RGB',(240,160),BG);canvas.paste(im,((240-im.width)//2,(160-im.height)//2));return canvas
    return im.crop((cx,cy,cx+240,cy+160))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    _,bl,bm=inventory(base);_,ls,maps=inventory(ROOT);generated=json.loads((OUT/'generator.json').read_text())['snapshots'];full={};before={}
    for n in NAMES:
        full[n]=render(ROOT,ls[maps[n]['layout']]);before[n]=render(base,bl[bm[n]['layout']])
        full[n].save(OUT/(n+'_After.png'));before[n].save(OUT/(n+'_Before.png'))
    floor=ls[maps[NAMES[1]]['layout']];bfloor=bl[bm[NAMES[1]]['layout']]
    after_floors=[render_grid(ROOT,floor,g['grid'],32,32,floor=g['floor']) for g in generated]
    before_floors=[render_grid(base,bfloor,g['grid'],32,32,floor=g['floor']) for g in generated]
    display=[full[NAMES[0]].resize((480,576),Image.Resampling.NEAREST),after_floors[0],full[NAMES[2]]]
    old=[before[NAMES[0]].resize((480,576),Image.Resampling.NEAREST),before_floors[0],before[NAMES[2]]]
    names=['Saguão — 15×18 (ampliado 2×)','Andar montado pelo C — 32×32','Topo — 34×23']
    xs=[16,520,1060]
    board=Image.new('RGB',(1620,710),BG);title(board,'ARAUNA — 07F — BATTLE PYRAMID — TRÊS MAPAS')
    for x,im,text in zip(xs,display,names):label(board,x,50,text);board.paste(im,(x,78))
    label(board,16,677,'Pedra e cobre; rosa dos ventos ao crepúsculo. RGB555 nativo, sem sprites. Frontier: 29/47.');board.save(OUT/'BattleFrontier_07F_Tres_Mapas.png')
    pairs=Image.new('RGB',(1620,1400),BG);title(pairs,'07F — MAPAS COMPLETOS — ORIGINAL EM CIMA / NOVO EMBAIXO')
    for row,pics in enumerate((old,display)):
        y=55+row*660
        for x,im,text in zip(xs,pics,names):label(pairs,x,y,text);pairs.paste(im,(x,y+30))
    label(pairs,16,1370,'Mesmo andar, mesmos módulos, mesma saída; apenas os bancos gráficos dos três layouts mudam.');pairs.save(OUT/'BattleFrontier_07F_Antes_Depois.png')
    cameras=Image.new('RGB',(1010,1170),BG);title(cameras,'07F — CÂMERA 240×160 — ORIGINAL / NOVO')
    coords=[(7,6),tuple(generated[0]['entrance']),(16,14)]
    for i,(n,point) in enumerate(zip(NAMES,coords)):
        y=55+i*360;label(cameras,16,y,n.removeprefix('BattleFrontier_')+(' — entrada procedural' if i==1 else ''))
        for tag,im,x in [('Before',old[i] if i!=0 else before[n],16),('After',display[i] if i!=0 else full[n],520)]:
            crop=camera(im,*point);crop.save(OUT/(n+'_Camera_'+tag+'.png'));cameras.paste(crop.resize((480,320),Image.Resampling.NEAREST),(x,y+25))
    label(cameras,16,1135,'Crops de mapas nativos sem atores e sem simulação da luz. Não são fotos do mGBA.');cameras.save(OUT/'BattleFrontier_07F_Cameras_240x160.png')
    palettes=Image.new('RGB',(2128,1190),BG);title(palettes,'07F — SETE ANDARES MONTADOS PELO C — PALETAS NATIVAS PRESERVADAS')
    for i,(im,g) in enumerate(zip(after_floors,generated)):
        x=16+i%4*528;y=52+i//4*550;label(palettes,x,y,f'Piso {i+1} — entrada {tuple(g["entrance"])} / saída {tuple(g["exit"])}');palettes.paste(im,(x,y+26));im.save(OUT/f'Pyramid_Floor_{i+1}_Generated.png')
    x=16+3*528;y=52+550
    for dy,text in enumerate(('16 módulos de 8×8','16 modelos de distribuição','1.848 casos do gerador original','Dois modos de posição inicial','Itens/treinadores conferidos','Mesmas sete paletas BG6','Sem sprites e sem luz simulada')):label(palettes,x,y+40+dy*34,text)
    label(palettes,16,1160,'As cores vêm da tarefa original do jogo; saída 0x28E e piso 0x28D mantêm IDs e atributos.');palettes.save(OUT/'BattleFrontier_07F_Sete_Pisos.png')
    modules=Image.new('RGB',(1120,790),BG);title(modules,'07F — 16 MÓDULOS — ORIGINAL À ESQUERDA / NOVO À DIREITA')
    for i,n in enumerate(SQUARES):
        x=16+i%4*276;y=52+i//4*174;l=ls[maps[n]['layout']];g=words(ROOT/l['blockdata_filepath']);label(modules,x,y,n)
        for repo,layout,dx in ((base,bfloor,0),(ROOT,floor,132)):
            im=render_grid(repo,layout,g,8,8,floor=0);modules.paste(im,(x+dx,y+26))
    label(modules,16,760,'Todos são exibidos pelo banco ativo do Floor, como ocorre no runtime. Grids e eventos permanecem exatos.');modules.save(OUT/'BattleFrontier_07F_Dezesseis_Modulos.png')
    anim=Image.new('RGB',(1040,720),BG);title(anim,'07F — TOCHAS E SOMBRAS — TRÊS QUADROS NATIVOS')
    for frame in range(3):
        x=16+frame*342;label(anim,x,52,f'Quadro {frame} — atualização a cada 8 ticks')
        for repo,layout,y in ((base,bl[bm[NAMES[0]]['layout']],80),(ROOT,ls[maps[NAMES[0]]['layout']],370)):
            im=render(repo,layout,frame);patch=im.crop((32,32,160,160)).resize((256,256),Image.Resampling.NEAREST);anim.paste(patch,(x,y))
    label(anim,16,685,'Original em cima, novo embaixo. Slots 647–654 e 663–670, índices, flips e paletas animadas preservados.');anim.save(OUT/'BattleFrontier_07F_Animacao.png')
    dump(OUT/'renders.json',{'frontier_maps':3,'whole_map_pairs':3,'camera_pairs':3,'generated_floors':7,'source_modules':16,'animation_frames':3,'native_rgb555':True,'sprites':False,'light_simulated':False,'emulator_screenshots':False,'floor_data_from_original_c':True})
    print('Three maps, original-C floors, all sixteen modules, cameras and three animation frames rendered.')

if __name__=='__main__':main()
