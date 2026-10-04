#!/usr/bin/env python3
"""Adapt New Mauville to an overgrown, electrically alive old facility."""
import json,shutil,struct
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
PRIMARY=ROOT/'data/tilesets/primary/arauna_usina_rocha'
SECONDARY=ROOT/'data/tilesets/secondary/arauna_usina_maquinas'
MAPS=('NewMauville_Entrance','NewMauville_Inside')
OLD=('LAYOUT_NEW_MAUVILLE_ENTRANCE','LAYOUT_NEW_MAUVILLE_INSIDE')
NEW=('LAYOUT_ARAUNA_USINA_VELHA_ENTRADA_V1','LAYOUT_ARAUNA_USINA_VELHA_INTERIOR_V1')
SIZES=((9,9),(41,41))
BASE=512+248

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

def assets():
    clone(ROOT/'data/tilesets/primary/general',PRIMARY)
    clone(ROOT/'data/tilesets/secondary/bike_shop',SECONDARY)
    palette(PRIMARY/'palettes/03.pal',{
        8:(42,52,49),9:(210,206,174),10:(180,179,150),11:(148,151,127),
        12:(113,124,104),13:(79,98,78),14:(51,71,55)})
    palette(SECONDARY/'palettes/06.pal',{
        1:(40,62,67),2:(126,101,78),3:(119,139,110),4:(164,180,146),
        5:(211,219,184),6:(87,121,98),7:(132,163,124),
        8:(178,193,175),9:(195,208,184),10:(226,233,207),
        11:(108,171,133),12:(77,145,111),13:(158,219,188),
        14:(225,137,86),15:(177,82,60)})
    palette(SECONDARY/'palettes/07.pal',{
        1:(40,62,67),2:(105,125,118),3:(176,198,179),4:(222,232,211),
        5:(53,131,76),6:(94,171,92),7:(146,201,107),8:(179,221,138),
        10:(142,179,171),11:(88,151,161),12:(220,231,209)})
    palette(SECONDARY/'palettes/08.pal',{
        3:(58,154,164),4:(144,202,185),5:(96,180,180),
        6:(140,110,80),7:(205,154,88)})
    palette(SECONDARY/'palettes/10.pal',{
        1:(224,234,207),2:(187,207,176),3:(147,171,146),4:(96,127,114),
        5:(43,69,76),6:(172,218,174),7:(112,187,137)})
    palette(SECONDARY/'palettes/11.pal',{
        1:(44,82,66),2:(57,117,73),3:(80,151,91),4:(119,179,109),
        5:(35,109,115),6:(49,151,151),7:(94,192,164),
        8:(24,78,89),9:(55,134,136),10:(98,178,171),
        11:(138,199,174),12:(47,89,67),13:(72,123,80),14:(140,178,119)})
    image=Image.open(SECONDARY/'tiles.png');assert image.mode=='P' and image.size==(128,256)
    meta=words(SECONDARY/'metatiles.bin');attrs=words(SECONDARY/'metatile_attributes.bin')
    assert len(attrs)==248 and not {x&1023 for x in meta}.intersection(range(0x3d0,0x3d8))
    assert not {x&1023 for x in meta}.intersection(range(0x268,0x278))
    moss=Image.new('P',(16,16),0);d=ImageDraw.Draw(moss)
    for x,y in ((2,12),(4,11),(5,9),(10,13),(12,10),(13,8)):
        d.point((x,y),fill=6);d.line((x,y,x+(1 if x<7 else -1),y-2),fill=7,width=1)
    d.arc((1,5,14,15),35,150,fill=5,width=1)
    cable=Image.new('P',(16,16),0);d=ImageDraw.Draw(cable)
    d.line((1,11,4,10,7,12,10,9,14,10),fill=2,width=2)
    d.line((7,12,9,6,12,5),fill=5,width=1)
    for x,y in ((7,12),(12,5)):d.ellipse((x-1,y-1,x+1,y+1),fill=11)
    for kind,art in enumerate((moss,cable)):
        start=0x3d0+kind*4
        for i,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):
            index=start+i
            image.paste(art.crop((x,y,x+8,y+8)),((index-512)%16*8,(index-512)//16*8))
        src=528
        meta.extend(meta[(src-512)*8:(src-512)*8+4]+[(start+i)|(6<<12) for i in range(4)])
        attrs.append(attrs[src-512])
    growth=Image.new('P',(32,32),0);d=ImageDraw.Draw(growth)
    d.polygon(((2,9),(6,5),(15,7),(23,3),(29,10),(26,18),(30,23),
               (20,28),(12,25),(5,29),(2,20)),fill=1)
    d.polygon(((5,12),(13,9),(21,12),(26,9),(24,18),(27,23),
               (17,25),(9,21)),fill=2)
    d.polygon(((9,15),(15,11),(22,15),(19,21),(12,22)),fill=5)
    d.line((10,15,15,14,19,16),fill=7,width=1)
    for x,y in ((6,7),(14,7),(26,7),(4,23),(9,27),(22,25),(28,20)):
        d.line((x,y,x+1,y-3),fill=4,width=1)
        d.point((x-1,y-2),fill=3)
    for part in range(4):
        bx,by=(part%2)*16,(part//2)*16
        for i,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):
            index=0x268+part*4+i
            image.paste(growth.crop((bx+x,by+y,bx+x+8,by+y+8)),
                        ((index-512)%16*8,(index-512)//16*8))
        src=528
        meta.extend(meta[(src-512)*8:(src-512)*8+4]+[(0x268+part*4+i)|(11<<12) for i in range(4)])
        attrs.append(attrs[src-512])
    image.save(SECONDARY/'tiles.png')
    (SECONDARY/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(meta),*meta))
    (SECONDARY/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(attrs),*attrs))

def register():
    refs='\n'.join(f'    INCGFX_U16("data/tilesets/primary/arauna_usina_rocha/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
    insert(ROOT/'src/graphics.c','// trade/egg hatch',
           'const u16 gTilesetPalettes_AraunaUsinaRocha[][16] =\n{\n'+refs+'\n};\n'
           'const u32 gTilesetTiles_AraunaUsinaRocha[] = INCGFX_U32("data/tilesets/primary/arauna_usina_rocha/tiles.png", ".4bpp.lz");\n\n',
           'const u32 gTilesetTiles_AraunaUsinaRocha[]')
    insert(ROOT/'src/data/tilesets/metatiles.h','const u16 gMetatiles_Petalburg[]',
           'const u16 gMetatiles_AraunaUsinaRocha[] = INCBIN_U16("data/tilesets/primary/arauna_usina_rocha/metatiles.bin");\n'
           'const u16 gMetatileAttributes_AraunaUsinaRocha[] = INCBIN_U16("data/tilesets/primary/arauna_usina_rocha/metatile_attributes.bin");\n\n',
           'const u16 gMetatiles_AraunaUsinaRocha[]')
    insert(ROOT/'src/data/tilesets/headers.h','const struct Tileset gTileset_Petalburg =',
           'const struct Tileset gTileset_AraunaUsinaRocha =\n{\n    .isCompressed = TRUE,\n    .isSecondary = FALSE,\n'
           '    .tiles = gTilesetTiles_AraunaUsinaRocha,\n    .palettes = gTilesetPalettes_AraunaUsinaRocha,\n'
           '    .metatiles = gMetatiles_AraunaUsinaRocha,\n    .metatileAttributes = gMetatileAttributes_AraunaUsinaRocha,\n'
           '    .callback = InitTilesetAnim_General,\n};\n\n',
           'const struct Tileset gTileset_AraunaUsinaRocha =')
    refs='\n'.join(f'    INCGFX_U16("data/tilesets/secondary/arauna_usina_maquinas/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
    insert(ROOT/'src/data/tilesets/graphics.h','const u32 gTilesetTiles_AraunaAmanhecer[]',
           'const u32 gTilesetTiles_AraunaUsinaMaquinas[] = INCGFX_U32("data/tilesets/secondary/arauna_usina_maquinas/tiles.png", ".4bpp.lz");\n'
           'const u16 gTilesetPalettes_AraunaUsinaMaquinas[][16] =\n{\n'+refs+'\n};\n\n',
           'const u32 gTilesetTiles_AraunaUsinaMaquinas[]')
    insert(ROOT/'src/data/tilesets/metatiles.h','const u16 gMetatiles_AraunaAmanhecer[]',
           'const u16 gMetatiles_AraunaUsinaMaquinas[] = INCBIN_U16("data/tilesets/secondary/arauna_usina_maquinas/metatiles.bin");\n'
           'const u16 gMetatileAttributes_AraunaUsinaMaquinas[] = INCBIN_U16("data/tilesets/secondary/arauna_usina_maquinas/metatile_attributes.bin");\n\n',
           'const u16 gMetatiles_AraunaUsinaMaquinas[]')
    insert(ROOT/'src/data/tilesets/headers.h','const struct Tileset gTileset_AraunaAmanhecer =',
           'const struct Tileset gTileset_AraunaUsinaMaquinas =\n{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n'
           '    .tiles = gTilesetTiles_AraunaUsinaMaquinas,\n    .palettes = gTilesetPalettes_AraunaUsinaMaquinas,\n'
           '    .metatiles = gMetatiles_AraunaUsinaMaquinas,\n    .metatileAttributes = gMetatileAttributes_AraunaUsinaMaquinas,\n'
           '    .callback = NULL,\n};\n\n',
           'const struct Tileset gTileset_AraunaUsinaMaquinas =')

def main():
    assets();register()
    path=ROOT/'data/layouts/layouts.json';node=json.loads(path.read_text());report={}
    for level,(name,old_id,new_id,(w,h)) in enumerate(zip(MAPS,OLD,NEW,SIZES)):
        base=next(r for r in node['layouts'] if r['id']==old_id)
        assert (base['width'],base['height'])==(w,h)
        old=words(ROOT/base['blockdata_filepath']);assert len(old)==w*h
        event_path=ROOT/'data/maps'/name/'map.json';event=json.loads(event_path.read_text())
        assert event['layout'] in (old_id,new_id)
        new=list(old);counts=[0,0]
        if level==1:
            occupied={(int(e['x']),int(e['y'])) for group in ('warp_events','object_events','coord_events','bg_events') for e in event[group]}
            for y in range(2,h-2):
                for x in range(2,w-2):
                    i=y*w+x
                    if old[i]&1023!=528 or (x,y) in occupied:continue
                    if any(abs(x-a)+abs(y-b)<2 for a,b in occupied):continue
                    salt=(x*19+y*23+x*y*5)%61
                    kind=0 if salt in (3,27) else (1 if salt==49 else None)
                    if kind is not None:
                        new[i]=(old[i]&~1023)|(BASE+kind);counts[kind]+=1
            assert 4<=counts[0]<=20 and 2<=counts[1]<=12,counts
            for px,py in ((29,6),(21,27),(6,18)):
                for part in range(4):
                    x,y=px+part%2,py+part//2;i=y*w+x
                    assert old[i]&1023==528 and (x,y) not in occupied
                    prev=(new[i]&1023)-BASE
                    if new[i]!=old[i] and prev in (0,1):counts[prev]-=1
                    new[i]=(old[i]&~1023)|(BASE+2+part)
        suffix=('Entrada','Interior')[level]
        folder=ROOT/'data/layouts'/('AraunaUsinaVelha_'+suffix);folder.mkdir(exist_ok=True)
        (folder/'map.bin').write_bytes(struct.pack('<%dH'%len(new),*new))
        shutil.copyfile(ROOT/base['border_filepath'],folder/'border.bin')
        record=dict(base,id=new_id,name='AraunaUsinaVelha_'+suffix+'_Layout',
                    primary_tileset='gTileset_AraunaUsinaRocha',
                    secondary_tileset=('gTileset_Facility' if level==0 else 'gTileset_AraunaUsinaMaquinas'),
                    blockdata_filepath=str((folder/'map.bin').relative_to(ROOT)),
                    border_filepath=str((folder/'border.bin').relative_to(ROOT)))
        current=next((r for r in node['layouts'] if r['id']==new_id),None)
        if current:current.update(record)
        else:node['layouts'].append(record)
        event['layout']=new_id;dump(event_path,event)
        report[name]={'size':[w,h],'moss_and_cables':counts,
                      'infiltration_patches':3 if level else 0,'warps':len(event['warp_events'])}
    dump(path,node)
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
