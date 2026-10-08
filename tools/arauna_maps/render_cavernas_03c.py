#!/usr/bin/env python3
"""Native, actual-selector review sheets for 03C and 03B V1.1."""
import argparse,json,re,tempfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from build_cavernas_03c import ROOT,OUT,NAMES,BNAMES,ALLNAMES
from cavernas_03a_common import compile_caves,render
from render_native_map import words
import puzzles_cavernas_03b as puzzles


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);a=ap.parse_args();base=a.base.resolve()
    ls=[{l['id']:l for l in json.loads((r/'data/layouts/layouts.json').read_text())['layouts']} for r in (base,ROOT)]
    maps={n:json.loads((ROOT/f'data/maps/{n}/map.json').read_text()) for n in ALLNAMES}
    oldh=(base/'src/data/arauna_cave_visuals_v2.h').read_text();build=json.loads((OUT/'build.json').read_text());OUT.mkdir(exist_ok=True)
    font=ImageFont.truetype('DejaVuSans.ttf',16)
    targets={'AlteringCave':[(2,2),(13,11),(11,14)],'ArtisanCave_B1F':[(1,0),(25,24),(1,42)],'ArtisanCave_1F':[(0,1),(5,7),(3,12)],'SealedChamber_OuterRoom':[(3,0),(2,5),(5,13)],'SealedChamber_InnerRoom':[(3,1),(1,7),(5,13)],'AncientTomb':[(1,2),(1,17),(1,23)],'IslandCave':[(1,2),(1,17),(1,23)]}
    before={};after={};records=[]
    with tempfile.TemporaryDirectory() as tmp:
        sel,cases=compile_caves(tmp);puzzles.OUT=OUT;puzzle_report=puzzles.run(Path(tmp)/'puzzles');(OUT/'puzzles.json').write_text(json.dumps(puzzle_report,indent=2)+'\n')
        for n in ALLNAMES:
            old,new=[ls[i][maps[n]['layout']] for i in (0,1)];native=words(ROOT/new['blockdata_filepath']);vis=[sel(cases[n],i%new['width']+7,i//new['width']+7,v&1023) for i,v in enumerate(native)]
            assert vis==words(ROOT/build['maps'][n]['visual_grid'])
            match=re.search(r'sVisual_'+n+r'\[\] = INCBIN_U16\("([^"]+)"\)',oldh)
            bvis=words(base/match[1]) if match else [v&1023 for v in native]
            before[n]=render(base,old,bvis);after[n]=render(ROOT,new,vis)
            for label,im in [('antes',before[n]),('depois',after[n])]:im.save(OUT/f'{n}_{label}.png')
            sheet=Image.new('RGB',(1016,1110),(19,28,35));d=ImageDraw.Draw(sheet);d.text((16,8),n+' — pixels nativos ampliados 2×',font=font,fill='white')
            for j,(x,y) in enumerate(targets[n]):
                yy=40+j*355
                for label,im,xx in [('antes',before[n],16),('depois',after[n],516)]:
                    crop=im.crop((x*16,y*16,x*16+240,y*16+160));crop.save(OUT/f'{n}_recorte{j+1}_{label}.png');d.text((xx,yy),label.upper(),font=font,fill=(167,197,204));sheet.paste(crop.resize((480,320),Image.Resampling.NEAREST),(xx,yy+24))
                records.append({'map':n,'crop':j+1,'origin':[x,y],'native_size':[240,160]})
            sheet.save(OUT/f'{n}_comparacao.png')
        door_sheet=Image.new('RGB',(1016,1110),(19,28,35));d=ImageDraw.Draw(door_sheet);d.text((16,8),'03B V1.1 — FECHADA / ABERTA',font=font,fill='white')
        for k,(n,patches) in enumerate(puzzle_report['door_states'].items()):
            l=ls[1][maps[n]['layout']];native=words(ROOT/l['blockdata_filepath']);x0,y0=(3,0) if n.startswith('Sealed') else (1,17);yy=40+k*355;d.text((16,yy),n,font=font,fill='white')
            for state,xx in [('closed',16),('open',516)]:
                g=list(native)
                for x,y,v in patches[state]:g[y*l['width']+x]=(g[y*l['width']+x]&0xf000)|v
                vis=[sel(cases[n],i%l['width']+7,i//l['width']+7,v&1023) for i,v in enumerate(g)];im=render(ROOT,l,vis)
                crop=im.crop((x0*16,y0*16,x0*16+240,y0*16+160));crop.save(OUT/f'{n}_porta_{state}.png');door_sheet.paste(crop.resize((480,320),Image.Resampling.NEAREST),(xx,yy+24))
        door_sheet.save(OUT/'03B_V11_Portas_Fechadas_Abertas.png')
    sheet=Image.new('RGB',(1632,930),(19,28,35));d=ImageDraw.Draw(sheet)
    for n,x in zip(NAMES,(16,544,1296)):
        d.text((x,8),n,font=font,fill='white');sheet.paste(after[n],(x,38))
    sheet.save(OUT/'Tres_Mapas_03C.png')
    sheet=Image.new('RGB',(936,1150),(19,28,35));d=ImageDraw.Draw(sheet)
    for k,n in enumerate(BNAMES):
        x=16+k%2*468;y=8+k//2*550;d.text((x,y),n,font=font,fill='white');sheet.paste(after[n],(x,y+30))
    sheet.save(OUT/'03B_V11_Quatro_Mapas.png')
    sheet=Image.new('RGB',(1016,1110),(19,28,35));d=ImageDraw.Draw(sheet);d.text((16,8),'03B V1.1 — SAÍDAS: BASE INSTALADA / ESTILO NOVO',font=font,fill='white')
    for k,n in enumerate(['SealedChamber_InnerRoom','AncientTomb','IslandCave']):
        l=ls[1][maps[n]['layout']];x,y=(3,13) if n.startswith('Sealed') else (1,23);yy=40+k*355;d.text((16,yy),n,font=font,fill='white')
        for im,xx in [(before[n],16),(after[n],516)]:sheet.paste(im.crop((x*16,y*16,x*16+240,y*16+160)).resize((480,320),Image.Resampling.NEAREST),(xx,yy+24))
    sheet.save(OUT/'03B_V11_Saidas_Antes_Depois.png')
    (OUT/'renders.json').write_text(json.dumps({'kind':'native_render_not_emulator','full_maps':7,'before_after_viewports':21,'door_state_pairs':3,'south_exit_pairs':3,'before_03b_uses_installed_corrected_selector_grids':True,'records':records},indent=2)+'\n')
    print('7 full maps, 21 before/after native viewports, 3 door and 3 exit pairs.')
if __name__=='__main__':main()
