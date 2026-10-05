#!/usr/bin/env python3
"""Render all sixteen native before/after pairs and stage the package manifest."""
import json,subprocess,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import build_porto_interiors_v1 as b
import render_porto_interiors_native as r
ROOT=b.ROOT;OUT=ROOT.parent/'output'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
LABELS=('Pavilhão — arena','Pavilhão — corredor','Pavilhão — recepção','Cais e embarque',
        'Casa residencial','Venda local','Casa dos nomes','Museu — recepção','Museu — exposição',
        'Centro — térreo','Centro — conexão','Clube comunitário','Estaleiro — oficina','Estaleiro — superior')

def main():
    OUT.mkdir(exist_ok=True)
    layouts={v['id']:v for v in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
    canvas=Image.new('RGB',(2400,1880),'#202b30');draw=ImageDraw.Draw(canvas)
    def text(x,y,s,size=20,color='#e8e2d2'):
        draw.multiline_text((x,y),s,font=ImageFont.truetype(FONT,size),fill=color,spacing=12)
    text(30,22,'PORTO DO SAL • QUATORZE INTERIORES V1',36)
    concept=Image.open(b.OUT/'Porto_do_Sal_concept.png').convert('RGB');concept.thumbnail((270,285));canvas.paste(concept,(30,84))
    text(335,100,'Referência de materiais: concept externo de Porto do Sal e Bíblia p. 6.',27)
    text(335,160,'Madeira envelhecida, reboco claro, tecidos azuis e mapas marítimos.\nEstaleiro: casco de madeira, caixotes, pranchas e guarda-corpos.\nMuseu: painéis emoldurados e exposição; serviços funcionais preservados.',24)
    text(335,285,'Não há concept individual destes interiores no pacote recuperado.\nCenas de embarque e museu mantêm comandos, coordenadas e colisão.',20)
    for i,(name,label) in enumerate(zip(b.NAMES,LABELS)):
        event=json.loads((ROOT/'data/maps'/name/'map.json').read_text())
        baseline=json.loads(subprocess.check_output(['git','show','HEAD:data/maps/'+name+'/map.json'],cwd=ROOT))
        x=20+(i%4)*595;y=395+(i//4)*340
        draw.rounded_rectangle((x,y,x+578,y+324),radius=10,fill='#2b373a')
        text(x+12,y+8,label,22);text(x+12,y+45,'Antes',17);text(x+300,y+45,'Depois',17)
        for shift,mapdata,before in ((12,baseline,True),(300,event,False)):
            l=layouts[mapdata['layout']]
            image=r.render_map(r.Renderer(r.resolve_tileset(l['primary_tileset']),r.resolve_tileset(l['secondary_tileset'])),ROOT/l['blockdata_filepath'],l['width'],l['height'])
            if not before:
                image.save(b.OUT/(name+'_native.png'));r.add_event_overlay(image,event).save(b.OUT/(name+'_events.png'))
            factor=min(265/image.width,230/image.height)
            image=image.resize((round(image.width*factor),round(image.height*factor)),Image.Resampling.NEAREST)
            canvas.paste(image,(x+shift,y+80))
    text(30,1785,'28 warps • 67 objetos • geometria e comportamentos idênticos ao original.',25)
    text(30,1832,'Renders dos assets nativos. Compilação de ROM e testes em emulador pendentes.',20)
    canvas.save(OUT/'porto_interiors_v1_14_ambientes.png')
    new=[]
    for symbol in b.SPECS:
        new.extend(str(p.relative_to(ROOT)) for p in b.target(symbol).rglob('*') if p.is_file())
    for name in b.NAMES:
        new.extend(str(p.relative_to(ROOT)) for p in (ROOT/'data/layouts'/(name+'_Arauna')).rglob('*') if p.is_file())
    new+=['docs/PORTO_INTERIORS_V1.md',
          'docs/ADAPTACAO_INTERIORES_STATUS_PORTO_2026_10_04.md',
          'review/porto_interiors_v1/manifest.json','review/porto_interiors_v1/geometry.json',
          'review/porto_interiors_v1/Porto_do_Sal_concept.png',
          'tools/arauna_maps/build_porto_interiors_review_v1.py','tools/arauna_maps/render_porto_interiors_native.py']
    new += [f'tools/arauna_maps/{a}_porto_interiors_v1.py' for a in ('apply','build','validate','package')]
    meta={'new_files':sorted(new),'map_baselines':{'data/maps/'+name+'/map.json':hashlib.sha256(subprocess.check_output(['git','show','HEAD:data/maps/'+name+'/map.json'],cwd=ROOT)).hexdigest() for name in b.NAMES},'new_layout_ids':[b.layout_id(name) for name in b.NAMES]}
    b.dump(b.OUT/'manifest.json',meta)

if __name__=='__main__':main()
