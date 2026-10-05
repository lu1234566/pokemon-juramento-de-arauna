#!/usr/bin/env python3
"""Render all sixteen native before/after pairs and stage the package manifest."""
import json,subprocess,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import build_encruz_interiors_v1 as b
import render_encruz_interiors_native as r
ROOT=b.ROOT;OUT=ROOT.parent/'output'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
LABELS=('Oficina de bicicletas','Salão de jogos','Casa elétrica','Casa residencial 1',
        'Casa residencial 2','Venda local','Centro — térreo','Centro — conexão')

def main():
    OUT.mkdir(exist_ok=True)
    layouts={v['id']:v for v in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
    canvas=Image.new('RGB',(2400,1500),'#202b30');draw=ImageDraw.Draw(canvas)
    def text(x,y,s,size=20,color='#e8e2d2'):
        draw.multiline_text((x,y),s,font=ImageFont.truetype(FONT,size),fill=color,spacing=12)
    text(30,22,'ENCRUZILHADA CENTRAL • OITO INTERIORES V1',36)
    text(30,100,'Referência: arquitetura cívica e comércio da Bíblia, página 7.',27)
    text(30,160,'Calçamento claro, reboco e carpintaria local; casas com tábuas e tecidos azuis.\nOficina e jogos recebem bancadas próprias. Casa elétrica mantém portas, botões e animações.',24)
    text(30,270,'Não há concept individual identificado para estes interiores no conjunto recuperado.\nA Casa da Fogueira é um cenário separado, já adaptado nas rodadas anteriores.',20)
    for i,(name,label) in enumerate(zip(b.NAMES,LABELS)):
        event=json.loads((ROOT/'data/maps'/name/'map.json').read_text())
        baseline=json.loads(subprocess.check_output(['git','show','HEAD:data/maps/'+name+'/map.json'],cwd=ROOT))
        x=20+(i%4)*595;y=370+(i//4)*500
        draw.rounded_rectangle((x,y,x+578,y+482),radius=10,fill='#2b373a')
        text(x+12,y+8,label,22);text(x+12,y+45,'Antes',17);text(x+300,y+45,'Depois',17)
        for shift,mapdata,before in ((12,baseline,True),(300,event,False)):
            l=layouts[mapdata['layout']]
            image=r.render_map(r.Renderer(r.resolve_tileset(l['primary_tileset']),r.resolve_tileset(l['secondary_tileset'])),ROOT/l['blockdata_filepath'],l['width'],l['height'])
            if not before:
                image.save(b.OUT/(name+'_native.png'));r.add_event_overlay(image,event).save(b.OUT/(name+'_events.png'))
            factor=min(265/image.width,385/image.height)
            image=image.resize((round(image.width*factor),round(image.height*factor)),Image.Resampling.NEAREST)
            canvas.paste(image,(x+shift,y+80))
    text(30,1395,'18 warps • 36 objetos • geometria e comportamentos idênticos ao original.',25)
    text(30,1442,'Renders dos assets nativos. Compilação de ROM e testes em emulador pendentes.',20)
    canvas.save(OUT/'encruz_interiors_v1_8_ambientes.png')
    new=[]
    for symbol in b.SPECS:
        new.extend(str(p.relative_to(ROOT)) for p in b.target(symbol).rglob('*') if p.is_file())
    for name in b.NAMES:
        new.extend(str(p.relative_to(ROOT)) for p in (ROOT/'data/layouts'/(name+'_Arauna')).rglob('*') if p.is_file())
    new+=['docs/ENCRUZ_INTERIORS_V1.md',
          'docs/ADAPTACAO_INTERIORES_STATUS_ENCRUZ_2026_10_04.md',
          'review/encruz_interiors_v1/manifest.json','review/encruz_interiors_v1/geometry.json',
          'tools/arauna_maps/build_encruz_interiors_review_v1.py','tools/arauna_maps/render_encruz_interiors_native.py']
    new += [f'tools/arauna_maps/{a}_encruz_interiors_v1.py' for a in ('apply','build','validate','package')]
    meta={'new_files':sorted(new),'map_baselines':{'data/maps/'+name+'/map.json':hashlib.sha256(subprocess.check_output(['git','show','HEAD:data/maps/'+name+'/map.json'],cwd=ROOT)).hexdigest() for name in b.NAMES},'new_layout_ids':[b.layout_id(name) for name in b.NAMES]}
    b.dump(b.OUT/'manifest.json',meta)

if __name__=='__main__':main()
