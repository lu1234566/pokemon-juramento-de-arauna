#!/usr/bin/env python3
"""Recolor Meteor Falls as ancient slate ruins with deep water and glyphs."""
import json
import shutil
import struct
from pathlib import Path

from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
NAMES=('MeteorFalls_1F_1R','MeteorFalls_1F_2R','MeteorFalls_B1F_1R',
       'MeteorFalls_B1F_2R','MeteorFalls_StevensCave')
OLD=('LAYOUT_METEOR_FALLS_1F_1R','LAYOUT_METEOR_FALLS_1F_2R',
     'LAYOUT_METEOR_FALLS_B1F_1R','LAYOUT_METEOR_FALLS_B1F_2R',
     'LAYOUT_METEOR_FALLS_STEVENS_CAVE')
SUFFIX=('SalaMaior','Cascatas','PonteFunda','CamaraAntiga','CaminhoFinal')
NEW=tuple('LAYOUT_ARAUNA_RUINAS_QUEDA_'+s.upper()+'_V1' for s in SUFFIX)
PRIMARY=ROOT/'data/tilesets/primary/arauna_rocha_queda'
SECONDARY=ROOT/'data/tilesets/secondary/arauna_ruinas_queda'
BASE=512+159


def words(path):
    raw=path.read_bytes();return list(struct.unpack('<%dH'%(len(raw)//2),raw))
def write_words(path,values):path.write_bytes(struct.pack('<%dH'%len(values),*values))
def dump(path,node):path.write_text(json.dumps(node,indent=2,ensure_ascii=False)+'\n')


def clone(src,dst):
    dst.mkdir(parents=True,exist_ok=True)
    for name in ('tiles.png','metatiles.bin','metatile_attributes.bin'):
        shutil.copyfile(src/name,dst/name)
    (dst/'palettes').mkdir(exist_ok=True)
    for i in range(16):shutil.copyfile(src/'palettes'/f'{i:02}.pal',dst/'palettes'/f'{i:02}.pal')


def palette(path,changes):
    lines=path.read_text().splitlines()
    assert lines[:3]==['JASC-PAL','0100','16'] and len(lines)==19
    for i,rgb in changes.items():lines[i+3]=' '.join(map(str,rgb))
    path.write_text('\n'.join(lines)+'\n')


def insert(path,anchor,block,marker):
    text=path.read_text()
    if marker not in text:
        assert text.count(anchor)==1,(path,anchor)
        path.write_text(text.replace(anchor,block+anchor))


def assets():
    clone(ROOT/'data/tilesets/primary/general',PRIMARY)
    clone(ROOT/'data/tilesets/secondary/meteor_falls',SECONDARY)
    # Primary palette 4 controls the water. Preserve white foam and transparency.
    palette(PRIMARY/'palettes/04.pal',{
        6:(132,166,195),7:(44,121,178),8:(31,102,164),9:(25,86,144),
        10:(18,69,127),11:(118,171,206),12:(91,148,193),
        13:(66,126,176),14:(44,105,157)})
    palette(PRIMARY/'palettes/03.pal',{
        8:(43,59,78),9:(205,216,219),10:(177,193,200),
        11:(148,170,182),12:(117,142,161),13:(88,115,137),
        14:(62,85,110)})
    rock={0:(61,78,94),1:(186,198,203),2:(162,178,187),3:(134,154,167),
          4:(109,132,148),5:(84,108,127),6:(58,84,108),7:(36,57,83),
          8:(215,222,219),9:(181,192,187),10:(153,169,171),
          11:(125,147,154),12:(99,123,139),13:(72,97,118),
          14:(44,66,91),15:(24,42,64)}
    palette(SECONDARY/'palettes/06.pal',rock)
    waterfall={i:rock[i] for i in range(8)}
    waterfall.update({8:(192,220,231),9:(147,199,219),10:(109,178,209),
                      11:(75,152,198),12:(51,129,183),13:(32,105,164),
                      14:(20,80,141)})
    palette(SECONDARY/'palettes/07.pal',waterfall)
    palette(SECONDARY/'palettes/08.pal',{
        10:(202,215,219),11:(179,194,201),12:(151,171,184),
        13:(120,145,163),14:(89,115,139),15:(61,85,112)})
    palette(SECONDARY/'palettes/11.pal',{
        1:(210,220,213),2:(175,195,191),3:(141,172,174),
        4:(112,153,165),5:(82,130,155),6:(54,102,132),7:(33,75,107)})
    source=Image.open(SECONDARY/'tiles.png')
    assert source.mode=='P' and source.size==(128,232)
    expanded=Image.new('P',(128,256),0)
    expanded.putpalette(source.getpalette());expanded.paste(source,(0,0))
    meta=words(SECONDARY/'metatiles.bin');attrs=words(SECONDARY/'metatile_attributes.bin')
    assert len(attrs)==159 and not {value&1023 for value in meta}.intersection(range(0x3f8,0x400))
    artworks=[]
    for kind in range(2):
        tile=Image.new('P',(16,16),0);draw=ImageDraw.Draw(tile)
        if kind==0:  # square stone inscription
            draw.line((3,4,11,4,12,11,5,12,3,4),fill=6,width=1)
            draw.line((5,7,8,5,10,8,7,10),fill=3,width=1)
            draw.point((8,7),fill=2)
        else:  # four worn stones arranged as an older shrine
            draw.arc((2,2,13,13),35,285,fill=5,width=1)
            draw.line((4,10,7,7,9,10,12,6),fill=4,width=1)
            for x,y in ((3,3),(11,3),(12,12)):draw.point((x,y),fill=2)
        artworks.append(tile)
    for kind,tile in enumerate(artworks):
        start=0x3f8+kind*4
        for quadrant,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):
            index=start+quadrant
            expanded.paste(tile.crop((x,y,x+8,y+8)),((index-512)%16*8,(index-512)//16*8))
        src=513
        meta.extend(meta[(src-512)*8:(src-512)*8+4]+[(start+i)|(11<<12) for i in range(4)])
        attrs.append(attrs[src-512])
    expanded.save(SECONDARY/'tiles.png')
    write_words(SECONDARY/'metatiles.bin',meta)
    write_words(SECONDARY/'metatile_attributes.bin',attrs)


def register():
    p=ROOT/'src/graphics.c'
    refs='\n'.join(f'    INCGFX_U16("data/tilesets/primary/arauna_rocha_queda/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
    insert(p,'// trade/egg hatch',
           'const u16 gTilesetPalettes_AraunaRochaQueda[][16] =\n{\n'+refs+'\n};\n'
           'const u32 gTilesetTiles_AraunaRochaQueda[] = INCGFX_U32("data/tilesets/primary/arauna_rocha_queda/tiles.png", ".4bpp.lz");\n\n',
           'const u32 gTilesetTiles_AraunaRochaQueda[]')
    p=ROOT/'src/data/tilesets/metatiles.h'
    insert(p,'const u16 gMetatiles_Petalburg[]',
           'const u16 gMetatiles_AraunaRochaQueda[] = INCBIN_U16("data/tilesets/primary/arauna_rocha_queda/metatiles.bin");\n'
           'const u16 gMetatileAttributes_AraunaRochaQueda[] = INCBIN_U16("data/tilesets/primary/arauna_rocha_queda/metatile_attributes.bin");\n\n',
           'const u16 gMetatiles_AraunaRochaQueda[]')
    p=ROOT/'src/data/tilesets/headers.h'
    insert(p,'const struct Tileset gTileset_Petalburg =',
           'const struct Tileset gTileset_AraunaRochaQueda =\n{\n    .isCompressed = TRUE,\n    .isSecondary = FALSE,\n'
           '    .tiles = gTilesetTiles_AraunaRochaQueda,\n    .palettes = gTilesetPalettes_AraunaRochaQueda,\n'
           '    .metatiles = gMetatiles_AraunaRochaQueda,\n    .metatileAttributes = gMetatileAttributes_AraunaRochaQueda,\n'
           '    .callback = InitTilesetAnim_General,\n};\n\n',
           'const struct Tileset gTileset_AraunaRochaQueda =')
    p=ROOT/'src/data/tilesets/graphics.h'
    refs='\n'.join(f'    INCGFX_U16("data/tilesets/secondary/arauna_ruinas_queda/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
    insert(p,'const u32 gTilesetTiles_AraunaAmanhecer[]',
           'const u32 gTilesetTiles_AraunaRuinasQueda[] = INCGFX_U32("data/tilesets/secondary/arauna_ruinas_queda/tiles.png", ".4bpp.lz");\n'
           'const u16 gTilesetPalettes_AraunaRuinasQueda[][16] =\n{\n'+refs+'\n};\n\n',
           'const u32 gTilesetTiles_AraunaRuinasQueda[]')
    p=ROOT/'src/data/tilesets/metatiles.h'
    insert(p,'const u16 gMetatiles_AraunaAmanhecer[]',
           'const u16 gMetatiles_AraunaRuinasQueda[] = INCBIN_U16("data/tilesets/secondary/arauna_ruinas_queda/metatiles.bin");\n'
           'const u16 gMetatileAttributes_AraunaRuinasQueda[] = INCBIN_U16("data/tilesets/secondary/arauna_ruinas_queda/metatile_attributes.bin");\n\n',
           'const u16 gMetatiles_AraunaRuinasQueda[]')
    p=ROOT/'src/data/tilesets/headers.h'
    insert(p,'const struct Tileset gTileset_AraunaAmanhecer =',
           'const struct Tileset gTileset_AraunaRuinasQueda =\n{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n'
           '    .tiles = gTilesetTiles_AraunaRuinasQueda,\n    .palettes = gTilesetPalettes_AraunaRuinasQueda,\n'
           '    .metatiles = gMetatiles_AraunaRuinasQueda,\n    .metatileAttributes = gMetatileAttributes_AraunaRuinasQueda,\n'
           '    .callback = NULL,\n};\n\n',
           'const struct Tileset gTileset_AraunaRuinasQueda =')


def main():
    assets();register()
    layouts_path=ROOT/'data/layouts/layouts.json'
    node=json.loads(layouts_path.read_text());report={}
    for level,(name,old_id,new_id,suffix) in enumerate(zip(NAMES,OLD,NEW,SUFFIX)):
        original=next(r for r in node['layouts'] if r['id']==old_id)
        width,height=original['width'],original['height']
        raw=words(ROOT/original['blockdata_filepath']);assert len(raw)==width*height
        event_path=ROOT/'data/maps'/name/'map.json';event=json.loads(event_path.read_text())
        assert event['layout'] in (old_id,new_id)
        occupied={(int(e['x']),int(e['y'])) for group in ('warp_events','object_events','coord_events','bg_events') for e in event[group]}
        new=list(raw);marks=[]
        for y in range(2,height-2):
            for x in range(2,width-2):
                i=y*width+x
                if raw[i]&1023!=513 or (x,y) in occupied:continue
                if any(abs(x-a)+abs(y-b)<2 for a,b in occupied):continue
                salt=(x*17+y*19+x*y*3+level*11)%83
                if salt not in (5,37):continue
                kind=0 if salt==5 else 1
                new[i]=(raw[i]&~1023)|(BASE+kind);marks.append((x,y))
        assert 1<=len(marks)<=25,(name,marks)
        folder=ROOT/'data/layouts'/('AraunaRuinasQueda_'+suffix)
        folder.mkdir(exist_ok=True)
        write_words(folder/'map.bin',new)
        shutil.copyfile(ROOT/original['border_filepath'],folder/'border.bin')
        record=dict(original,id=new_id,name='AraunaRuinasQueda_'+suffix+'_Layout',
                    primary_tileset='gTileset_AraunaRochaQueda',
                    secondary_tileset='gTileset_AraunaRuinasQueda',
                    blockdata_filepath=str((folder/'map.bin').relative_to(ROOT)),
                    border_filepath=str((folder/'border.bin').relative_to(ROOT)))
        current=next((r for r in node['layouts'] if r['id']==new_id),None)
        if current:current.update(record)
        else:node['layouts'].append(record)
        event['layout']=new_id;dump(event_path,event)
        report[name]={'size':[width,height],'ancient_marks':len(marks),'warps':len(event['warp_events'])}
    dump(layouts_path,node)
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
