#!/usr/bin/env python3
"""Four full native maps, twelve 240x160 before/after viewport pairs."""
import argparse,json,tempfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from build_cavernas_03a import ROOT,OUT,NAMES
from render_native_map import words
from cavernas_03a_common import compile_caves,render

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);a=ap.parse_args();base=a.base.resolve()
    nodes=[json.loads((p/'data/layouts/layouts.json').read_text())['layouts'] for p in (base,ROOT)]
    maps={n:json.loads((ROOT/f'data/maps/{n}/map.json').read_text()) for n in NAMES}
    ls=[{l['id']:l for l in node} for node in nodes]
    targets={'TerraCave_Entrance':[(5,0),(4,5),(1,10)],'MarineCave_Entrance':[(5,0),(4,5),(1,10)],'TerraCave_End':[(0,0),(5,9),(10,18)],'MarineCave_End':[(12,0),(5,9),(2,18)]}
    try:font=ImageFont.truetype('DejaVuSans.ttf',16)
    except OSError:font=ImageFont.load_default(size=16)
    OUT.mkdir(parents=True,exist_ok=True);record=[]
    with tempfile.TemporaryDirectory() as tmp:
        selector,cases=compile_caves(tmp)
        for k,n in enumerate(NAMES):
            l=ls[1][maps[n]['layout']];native=words(ROOT/l['blockdata_filepath']);grid=[selector(cases[n],i%l['width']+7,i//l['width']+7,v&1023) for i,v in enumerate(native)]
            expected=words(OUT/'visual_grids'/f'{n}.bin');assert grid==expected
            before=render(base,ls[0][maps[n]['layout']]);after=render(ROOT,l,grid)
            for label,im in [('antes',before),('depois',after)]:im.save(OUT/f'{n}_{label}.png')
            for j,(x0,y0) in enumerate(targets[n]):
                for label,im,x in [('antes',before,16),('depois',after,516)]:
                    crop=im.crop((x0*16,y0*16,x0*16+240,y0*16+160));crop.save(OUT/f'{n}_recorte{j+1}_{label}.png')
                record.append({'map':n,'crop':j+1,'origin':[x0,y0],'native_size':[240,160]})
    # Keep full comparison separate from the readable viewport-only contact sheets.
    # Each map sheet has three rows; no downsampling of native pixels is used.
    for k,n in enumerate(NAMES):
        sheet=Image.new('RGB',(1016,1110),(19,28,35));sd=ImageDraw.Draw(sheet)
        sd.text((16,8),n+' — recortes nativos 240×160 (ampliados 2×)',font=font,fill='white')
        for j in range(3):
            yy=38+j*355;sd.text((16,yy),'ANTES',font=font,fill=(167,197,204));sd.text((516,yy),'DEPOIS',font=font,fill=(167,197,204))
            for label,x in [('antes',16),('depois',516)]:
                crop=Image.open(OUT/f'{n}_recorte{j+1}_{label}.png');sheet.paste(crop.resize((480,320),Image.Resampling.NEAREST),(x,yy+24))
        sheet.save(OUT/f'{n}_comparacao.png')
    full=Image.new('RGB',(936,1150),(19,28,35));fd=ImageDraw.Draw(full)
    for k,n in enumerate(NAMES):
        x=16+(k%2)*468;y=8+(k//2)*550;fd.text((x,y),n,font=font,fill='white');im=Image.open(OUT/f'{n}_depois.png');full.paste(im,(x,y+30))
    full.save(OUT/'Quatro_Mapas_03A.png')
    (OUT/'renders.json').write_text(json.dumps({'kind':'native_render_not_emulator','full_maps':4,'before_after_viewports':12,'records':record},indent=2)+'\n')
    print('4 mapas integrais e 12 pares 240x160 renderizados pelo seletor C real.')
if __name__=='__main__':main()
