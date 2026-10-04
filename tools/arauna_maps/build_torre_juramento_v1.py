#!/usr/bin/env python3
"""Adapt Sky Pillar as a blue-sea ancient tower with progressive erosion."""
import json,shutil,struct,subprocess
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
MAPS=tuple(p.parent.name for p in sorted((ROOT/'data/maps').glob('SkyPillar*/map.json')))
PRIMARY=ROOT/'data/tilesets/primary/arauna_torre_mar'
SECONDARY={k:ROOT/'data/tilesets/secondary'/('arauna_torre_'+k)
           for k in ('costa','pisos_baixos','pisos_altos','topo','entrada')}
BASE=512+203

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
def layout_id(name):return 'LAYOUT_ARAUNA_TORRE_'+name.split('_',1)[1].upper()+'_V1'
def state(name):
    if name=='SkyPillar_Entrance':return 'entrada'
    if name=='SkyPillar_Outside':return 'costa'
    if name=='SkyPillar_Top':return 'topo'
    return 'pisos_altos' if name in ('SkyPillar_4F','SkyPillar_5F') else 'pisos_baixos'

def assets():
    clone(ROOT/'data/tilesets/primary/general',PRIMARY)
    palette(PRIMARY/'palettes/03.pal',{
        8:(42,50,62),9:(191,195,188),10:(159,171,171),
        11:(129,147,157),12:(101,123,142),13:(74,97,122),14:(48,70,101)})
    palette(PRIMARY/'palettes/04.pal',{
        6:(112,162,199),7:(36,113,182),8:(25,97,167),9:(20,80,149),
        10:(17,62,132),11:(124,190,219),12:(88,163,209),
        13:(60,139,193),14:(39,115,176)})
    palette(PRIMARY/'palettes/05.pal',{
        11:(192,184,159),12:(162,158,142),13:(130,135,133),14:(94,107,120)})
    source=ROOT/'data/tilesets/secondary/pacifidlog'
    variations={'costa':((60,78,105),(199,205,196)),
                'pisos_baixos':((67,79,103),(190,199,195)),
                'pisos_altos':((49,66,94),(159,176,181)),
                'topo':((65,88,119),(197,218,224))}
    for k,(dark,bright) in variations.items():
        target=SECONDARY[k];clone(source,target)
        colors={0:dark,1:bright,
                2:tuple(round((2*a+b)/3) for a,b in zip(bright,dark)),
                3:tuple(round((a+b)/2) for a,b in zip(bright,dark)),
                4:tuple(round((a+2*b)/3) for a,b in zip(bright,dark)),
                5:(107,130,157),6:(77,103,139),7:(50,73,109),8:(31,53,85),
                9:(169,149,119),10:(151,128,100),11:(181,152,104),
                12:(188,207,222),13:(96,125,162),14:(132,158,183)}
        palette(target/'palettes/06.pal',colors)
        palette(target/'palettes/07.pal',{
            1:(215,215,192),2:(181,190,177),3:(150,164,162),
            4:(118,137,148),5:(93,113,131),6:(63,85,111),
            7:(39,60,90),9:(188,222,237),10:(138,192,223),
            11:(96,165,211),12:(63,137,194),13:(37,110,178),14:(20,88,157)})
        palette(target/'palettes/11.pal',{
            1:(188,212,223),2:(127,175,206),3:(78,135,183),
            4:(46,102,154),5:(109,127,157),6:(75,96,128)})
        image=Image.open(target/'tiles.png');assert image.mode=='P' and image.size==(128,256)
        meta=words(target/'metatiles.bin');attrs=words(target/'metatile_attributes.bin')
        assert len(attrs)==203 and not {x&1023 for x in meta}.intersection(range(0x3f8,0x400))
        rune=Image.new('P',(16,16),0);d=ImageDraw.Draw(rune)
        d.line((2,3,7,5,11,2,13,7,9,11,4,12),fill=5,width=1)
        d.arc((4,4,11,12),30,260,fill=3,width=1)
        for x,y in ((3,4),(10,9),(6,13)):d.point((x,y),fill=2)
        fracture=Image.new('P',(16,16),0);d=ImageDraw.Draw(fracture)
        d.line((2,3,6,7,4,11,9,10,13,14),fill=5,width=1)
        d.line((6,7,11,5,13,3),fill=3,width=1)
        d.point((9,10),fill=2)
        for kind,art in enumerate((rune,fracture)):
            start=0x3f8+kind*4
            for i,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):
                index=start+i
                image.paste(art.crop((x,y,x+8,y+8)),((index-512)%16*8,(index-512)//16*8))
        image.save(target/'tiles.png')
        for kind,src in enumerate((701,564)):
            meta.extend(meta[(src-512)*8:(src-512)*8+4]+[(0x3f8+kind*4+i)|(11<<12) for i in range(4)])
            attrs.append(attrs[src-512])
        (target/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(meta),*meta))
        (target/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(attrs),*attrs))
    target=SECONDARY['entrada'];clone(ROOT/'data/tilesets/secondary/cave',target)
    palette(target/'palettes/06.pal',{
        0:(68,83,105),1:(209,216,215),2:(180,193,198),3:(151,171,184),
        4:(119,145,168),5:(91,119,146),6:(63,89,121),7:(39,62,97),
        8:(231,239,240),9:(170,204,223),10:(96,162,211),11:(39,111,181)})

def register():
    refs='\n'.join(f'    INCGFX_U16("data/tilesets/primary/arauna_torre_mar/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
    insert(ROOT/'src/graphics.c','// trade/egg hatch',
           'const u16 gTilesetPalettes_AraunaTorreMar[][16] =\n{\n'+refs+'\n};\n'
           'const u32 gTilesetTiles_AraunaTorreMar[] = INCGFX_U32("data/tilesets/primary/arauna_torre_mar/tiles.png", ".4bpp.lz");\n\n',
           'const u32 gTilesetTiles_AraunaTorreMar[]')
    insert(ROOT/'src/data/tilesets/metatiles.h','const u16 gMetatiles_Petalburg[]',
           'const u16 gMetatiles_AraunaTorreMar[] = INCBIN_U16("data/tilesets/primary/arauna_torre_mar/metatiles.bin");\n'
           'const u16 gMetatileAttributes_AraunaTorreMar[] = INCBIN_U16("data/tilesets/primary/arauna_torre_mar/metatile_attributes.bin");\n\n',
           'const u16 gMetatiles_AraunaTorreMar[]')
    insert(ROOT/'src/data/tilesets/headers.h','const struct Tileset gTileset_Petalburg =',
           'const struct Tileset gTileset_AraunaTorreMar =\n{\n    .isCompressed = TRUE,\n    .isSecondary = FALSE,\n'
           '    .tiles = gTilesetTiles_AraunaTorreMar,\n    .palettes = gTilesetPalettes_AraunaTorreMar,\n'
           '    .metatiles = gMetatiles_AraunaTorreMar,\n    .metatileAttributes = gMetatileAttributes_AraunaTorreMar,\n'
           '    .callback = InitTilesetAnim_General,\n};\n\n',
           'const struct Tileset gTileset_AraunaTorreMar =')
    refs=[];metas=[];headers=[]
    labels=(('costa','AraunaTorreCosta'),('pisos_baixos','AraunaTorrePisosBaixos'),
            ('pisos_altos','AraunaTorrePisosAltos'),('topo','AraunaTorreTopo'),
            ('entrada','AraunaTorreEntrada'))
    for k,name in labels:
        slug='arauna_torre_'+k
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
           '\n'.join(refs)+'\n','const u32 gTilesetTiles_AraunaTorreCosta[]')
    insert(ROOT/'src/data/tilesets/metatiles.h','const u16 gMetatiles_AraunaAmanhecer[]',
           '\n'.join(metas)+'\n','const u16 gMetatiles_AraunaTorreCosta[]')
    insert(ROOT/'src/data/tilesets/headers.h','const struct Tileset gTileset_AraunaAmanhecer =',
           '\n'.join(headers)+'\n','const struct Tileset gTileset_AraunaTorreCosta =')

def main():
    assets();register()
    path=ROOT/'data/layouts/layouts.json';node=json.loads(path.read_text());report={}
    for name in MAPS:
        map_path=ROOT/'data/maps'/name/'map.json';event=json.loads(map_path.read_text())
        if event['layout'].startswith('LAYOUT_ARAUNA_TORRE_'):
            base_event=json.loads(subprocess.check_output(['git','show',f'HEAD:data/maps/{name}/map.json'],cwd=ROOT))
            original=next(r for r in node['layouts'] if r['id']==base_event['layout'])
        else:original=next(r for r in node['layouts'] if r['id']==event['layout'])
        new_id=layout_id(name);assert event['layout'] in (original['id'],new_id)
        w,h=original['width'],original['height'];old=words(ROOT/original['blockdata_filepath']);assert len(old)==w*h
        new=list(old);marks=0;kind=state(name)
        if kind!='entrada':
            occupied={(int(e['x']),int(e['y'])) for group in ('warp_events','object_events','coord_events','bg_events') for e in event[group]}
            for y in range(1,h-1):
                for x in range(1,w-1):
                    i=y*w+x
                    tile=old[i]&1023
                    if tile not in (701,564) or (x,y) in occupied:continue
                    salt=(x*13+y*19+x*y*3+len(name))%31
                    if salt in ((3,11,19) if kind=='pisos_altos' else (3,)):
                        new[i]=(old[i]&~1023)|(BASE+(tile==564));marks+=1
        folder=ROOT/'data/layouts'/('AraunaTorre_'+name.split('_',1)[1]);folder.mkdir(exist_ok=True)
        (folder/'map.bin').write_bytes(struct.pack('<%dH'%len(new),*new))
        shutil.copyfile(ROOT/original['border_filepath'],folder/'border.bin')
        symbol={'costa':'AraunaTorreCosta','pisos_baixos':'AraunaTorrePisosBaixos',
                'pisos_altos':'AraunaTorrePisosAltos','topo':'AraunaTorreTopo',
                'entrada':'AraunaTorreEntrada'}[kind]
        record=dict(original,id=new_id,name='AraunaTorre_'+name.split('_',1)[1]+'_Layout',
                    primary_tileset='gTileset_AraunaTorreMar',secondary_tileset='gTileset_'+symbol,
                    blockdata_filepath=str((folder/'map.bin').relative_to(ROOT)),
                    border_filepath=str((folder/'border.bin').relative_to(ROOT)))
        current=next((r for r in node['layouts'] if r['id']==new_id),None)
        if current:current.update(record)
        else:node['layouts'].append(record)
        event['layout']=new_id;dump(map_path,event)
        report[name]={'level':kind,'size':[w,h],'ancient_marks':marks,'warps':len(event['warp_events'])}
    dump(path,node);print(json.dumps(report,indent=2))

if __name__=='__main__':main()
