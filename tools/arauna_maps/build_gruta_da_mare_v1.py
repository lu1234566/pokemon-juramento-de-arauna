#!/usr/bin/env python3
"""Give Shoal Cave paired tidal palettes and visible waterline inscriptions."""
import json,shutil,struct,subprocess
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
MAPS=tuple(p.parent.name for p in sorted((ROOT/'data/maps').glob('ShoalCave*/map.json')))
PRIMARY_HIGH=ROOT/'data/tilesets/primary/arauna_mare_alta'
PRIMARY_LOW=ROOT/'data/tilesets/primary/arauna_mare_baixa'
SECONDARY={k:ROOT/'data/tilesets/secondary'/('arauna_mare_rocha_'+k if k!='gelo' else 'arauna_mare_gelo')
           for k in ('alta','baixa','gelo')}
BASE=512+414

def words(path):
    b=path.read_bytes();return list(struct.unpack('<%dH'%(len(b)//2),b))
def dump(path,node):path.write_text(json.dumps(node,indent=2,ensure_ascii=False)+'\n')
def clone(src,dst):
    dst.mkdir(parents=True,exist_ok=True)
    for n in ('tiles.png','metatiles.bin','metatile_attributes.bin'):shutil.copyfile(src/n,dst/n)
    (dst/'palettes').mkdir(exist_ok=True)
    for i in range(16):shutil.copyfile(src/'palettes'/f'{i:02}.pal',dst/'palettes'/f'{i:02}.pal')
def palette(path,changes):
    lines=path.read_text().splitlines();assert lines[:3]==['JASC-PAL','0100','16'] and len(lines)==19
    for i,rgb in changes.items():lines[i+3]=' '.join(map(str,rgb))
    path.write_text('\n'.join(lines)+'\n')
def insert(path,anchor,block,marker):
    s=path.read_text()
    if marker not in s:
        assert s.count(anchor)==1,(path,anchor)
        path.write_text(s.replace(anchor,block+anchor))
def state(name):return 'gelo' if 'IceRoom' in name else ('alta' if 'HighTide' in name else 'baixa')
def layout_id(name):return 'LAYOUT_ARAUNA_MARE_'+name.split('_',1)[1].upper()+'_V1'

def assets():
    source=ROOT/'data/tilesets/primary/general'
    for target in (PRIMARY_HIGH,PRIMARY_LOW):clone(source,target)
    palette(PRIMARY_HIGH/'palettes/04.pal',{
        6:(179,204,228),7:(87,152,210),8:(68,133,197),9:(55,116,181),
        10:(40,96,165),11:(192,225,238),12:(162,211,233),
        13:(130,190,224),14:(94,163,207)})
    palette(PRIMARY_LOW/'palettes/04.pal',{
        6:(101,149,190),7:(26,104,168),8:(19,84,151),9:(18,70,134),
        10:(15,54,116),11:(115,180,212),12:(83,151,199),
        13:(56,127,184),14:(36,103,163)})
    palette(PRIMARY_HIGH/'palettes/05.pal',{
        11:(221,234,233),12:(191,215,220),13:(154,190,204),14:(121,166,185)})
    palette(PRIMARY_LOW/'palettes/05.pal',{
        11:(190,175,144),12:(160,145,119),13:(130,116,99),14:(99,90,82)})
    source=ROOT/'data/tilesets/secondary/cave'
    for target in SECONDARY.values():clone(source,target)
    colors={
        'alta':((83,104,132),(212,226,231)),
        'baixa':((65,68,72),(187,177,151)),
        'gelo':((82,126,171),(223,241,247)),
    }
    for k,target in SECONDARY.items():
        dark,bright=colors[k]
        values={0:dark,1:bright,2:tuple(round((2*a+b)/3) for a,b in zip(bright,dark)),
                3:tuple(round((a+b)/2) for a,b in zip(bright,dark)),
                4:tuple(round((a+2*b)/3) for a,b in zip(bright,dark)),
                5:tuple(round((a+3*b)/4) for a,b in zip(bright,dark)),
                6:tuple(round(v*.68) for v in dark),7:tuple(round(v*.47) for v in dark),
                8:(237,244,245),9:(192,220,230),10:(119,179,211),11:(51,122,179)}
        palette(target/'palettes/06.pal',values)
        if k!='gelo':
            palette(target/'palettes/09.pal',values)
            palette(target/'palettes/10.pal',values)
            palette(target/'palettes/11.pal',{
                1:(199,227,230),2:(146,201,215),3:(94,171,202),
                4:(57,137,190),5:(39,105,165),6:(22,77,135),7:(14,52,104)})
            image=Image.open(target/'tiles.png')
            assert image.mode=='P' and image.size==(128,216)
            sheet=Image.new('P',(128,256),0);sheet.putpalette(image.getpalette());sheet.paste(image,(0,0))
            meta=words(target/'metatiles.bin');attrs=words(target/'metatile_attributes.bin')
            assert len(attrs)==414 and not {v&1023 for v in meta}.intersection(range(0x3f8,0x3fc))
            mark=Image.new('P',(16,16),0);d=ImageDraw.Draw(mark)
            d.arc((2,3,13,12),25,265,fill=3,width=1)
            d.line((3,11,6,8,9,10,12,7),fill=5,width=1)
            for point in ((4,4),(10,4),(12,12)):d.point(point,fill=2)
            for i,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):
                idx=0x3f8+i
                sheet.paste(mark.crop((x,y,x+8,y+8)),((idx-512)%16*8,(idx-512)//16*8))
            sheet.save(target/'tiles.png')
            src=529
            meta.extend(meta[(src-512)*8:(src-512)*8+4]+[(0x3f8+i)|(11<<12) for i in range(4)])
            attrs.append(attrs[src-512])
            (target/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(meta),*meta))
            (target/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(attrs),*attrs))

def register():
    p_refs=[];p_metas=[];p_headers=[]
    for k,name in (('alta','AraunaMareAlta'),('baixa','AraunaMareBaixa')):
        slug='arauna_mare_'+k
        refs='\n'.join(f'    INCGFX_U16("data/tilesets/primary/{slug}/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
        p_refs.append(f'const u16 gTilesetPalettes_{name}[][16] =\n{{\n'+refs+'\n};\n'
                      f'const u32 gTilesetTiles_{name}[] = INCGFX_U32("data/tilesets/primary/{slug}/tiles.png", ".4bpp.lz");\n')
        p_metas.append(f'const u16 gMetatiles_{name}[] = INCBIN_U16("data/tilesets/primary/{slug}/metatiles.bin");\n'
                       f'const u16 gMetatileAttributes_{name}[] = INCBIN_U16("data/tilesets/primary/{slug}/metatile_attributes.bin");\n')
        p_headers.append(f'const struct Tileset gTileset_{name} =\n{{\n    .isCompressed = TRUE,\n    .isSecondary = FALSE,\n'
                         f'    .tiles = gTilesetTiles_{name},\n    .palettes = gTilesetPalettes_{name},\n'
                         f'    .metatiles = gMetatiles_{name},\n    .metatileAttributes = gMetatileAttributes_{name},\n'
                         '    .callback = InitTilesetAnim_General,\n};\n')
    insert(ROOT/'src/graphics.c','// trade/egg hatch','\n'.join(p_refs)+'\n','const u16 gTilesetPalettes_AraunaMareAlta[][16] =')
    insert(ROOT/'src/data/tilesets/metatiles.h','const u16 gMetatiles_Petalburg[]','\n'.join(p_metas)+'\n','const u16 gMetatiles_AraunaMareAlta[] =')
    insert(ROOT/'src/data/tilesets/headers.h','const struct Tileset gTileset_Petalburg =','\n'.join(p_headers)+'\n','const struct Tileset gTileset_AraunaMareAlta =')
    refs=[];metas=[];headers=[]
    for k,name in (('alta','AraunaMareRochaAlta'),('baixa','AraunaMareRochaBaixa'),('gelo','AraunaMareGelo')):
        slug='arauna_mare_rocha_'+k if k!='gelo' else 'arauna_mare_gelo'
        refs.append(f'const u32 gTilesetTiles_{name}[] = INCGFX_U32("data/tilesets/secondary/{slug}/tiles.png", ".4bpp.lz");\n'
                    f'const u16 gTilesetPalettes_{name}[][16] =\n{{\n'+
                    '\n'.join(f'    INCGFX_U16("data/tilesets/secondary/{slug}/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))+'\n};\n')
        metas.append(f'const u16 gMetatiles_{name}[] = INCBIN_U16("data/tilesets/secondary/{slug}/metatiles.bin");\n'
                     f'const u16 gMetatileAttributes_{name}[] = INCBIN_U16("data/tilesets/secondary/{slug}/metatile_attributes.bin");\n')
        headers.append(f'const struct Tileset gTileset_{name} =\n{{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n'
                       f'    .tiles = gTilesetTiles_{name},\n    .palettes = gTilesetPalettes_{name},\n'
                       f'    .metatiles = gMetatiles_{name},\n    .metatileAttributes = gMetatileAttributes_{name},\n'
                       '    .callback = NULL,\n};\n')
    insert(ROOT/'src/data/tilesets/graphics.h','const u32 gTilesetTiles_AraunaAmanhecer[]',
           '\n'.join(refs)+'\n','const u32 gTilesetTiles_AraunaMareRochaAlta[]')
    insert(ROOT/'src/data/tilesets/metatiles.h','const u16 gMetatiles_AraunaAmanhecer[]',
           '\n'.join(metas)+'\n','const u16 gMetatiles_AraunaMareRochaAlta[]')
    insert(ROOT/'src/data/tilesets/headers.h','const struct Tileset gTileset_AraunaAmanhecer =',
           '\n'.join(headers)+'\n','const struct Tileset gTileset_AraunaMareRochaAlta =')

def main():
    assets();register()
    path=ROOT/'data/layouts/layouts.json';node=json.loads(path.read_text());report={}
    for name in MAPS:
        map_path=ROOT/'data/maps'/name/'map.json';event=json.loads(map_path.read_text())
        if event['layout'].startswith('LAYOUT_ARAUNA_MARE_'):
            old_event=json.loads(subprocess.check_output(['git','show',f'HEAD:data/maps/{name}/map.json'],cwd=ROOT))
            original=next(r for r in node['layouts'] if r['id']==old_event['layout'])
        else:original=next(r for r in node['layouts'] if r['id']==event['layout'])
        new_id=layout_id(name);assert event['layout'] in (original['id'],new_id)
        w,h=original['width'],original['height']
        old=words(ROOT/original['blockdata_filepath']);assert len(old)==w*h
        new=list(old);kind=state(name);marks=0
        if kind!='gelo':
            occupied={(int(e['x']),int(e['y'])) for group in ('warp_events','object_events','coord_events','bg_events') for e in event[group]}
            for y in range(2,h-2):
                for x in range(2,w-2):
                    i=y*w+x
                    if old[i]&1023!=529 or (x,y) in occupied:continue
                    if (x*13+y*19+x*y*3)%71==4:
                        new[i]=(old[i]&~1023)|BASE;marks+=1
        folder=ROOT/'data/layouts'/('AraunaMare_'+name.split('_',1)[1]);folder.mkdir(exist_ok=True)
        (folder/'map.bin').write_bytes(struct.pack('<%dH'%len(new),*new))
        shutil.copyfile(ROOT/original['border_filepath'],folder/'border.bin')
        record=dict(original,id=new_id,name='AraunaMare_'+name.split('_',1)[1]+'_Layout',
                    primary_tileset='gTileset_AraunaMareAlta' if kind in ('alta','gelo') else 'gTileset_AraunaMareBaixa',
                    secondary_tileset={'alta':'gTileset_AraunaMareRochaAlta',
                                       'baixa':'gTileset_AraunaMareRochaBaixa',
                                       'gelo':'gTileset_AraunaMareGelo'}[kind],
                    blockdata_filepath=str((folder/'map.bin').relative_to(ROOT)),
                    border_filepath=str((folder/'border.bin').relative_to(ROOT)))
        found=next((r for r in node['layouts'] if r['id']==new_id),None)
        if found:found.update(record)
        else:node['layouts'].append(record)
        event['layout']=new_id;dump(map_path,event)
        report[name]={'state':kind,'size':[w,h],'waterline_marks':marks,'warps':len(event['warp_events'])}
    dump(path,node);print(json.dumps(report,indent=2))

if __name__=='__main__':main()
