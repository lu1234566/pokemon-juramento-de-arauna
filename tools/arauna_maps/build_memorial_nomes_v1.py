#!/usr/bin/env python3
"""Adapt the eight Mt. Pyre maps to a quiet stone and violet memorial."""
import json,shutil,struct,subprocess
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
MAPS=tuple(p.parent.name for p in sorted((ROOT/'data/maps').glob('MtPyre*/map.json')))
PRIMARY_SOURCE=ROOT/'data/tilesets/primary/general'
PRIMARY=ROOT/'data/tilesets/primary/arauna_memorial_exterior'
SECONDARY_SOURCE=ROOT/'data/tilesets/secondary/facility'
SECONDARY=ROOT/'data/tilesets/secondary/arauna_memorial_nomes'
CRYSTAL=1023

def words(path):
    b=path.read_bytes();return list(struct.unpack('<%dH'%(len(b)//2),b))
def dump(path,node):path.write_text(json.dumps(node,indent=2,ensure_ascii=False)+'\n')
def palette(path,changes):
    lines=path.read_text().splitlines();assert lines[:3]==['JASC-PAL','0100','16'] and len(lines)==19
    for i,rgb in changes.items():lines[i+3]=' '.join(map(str,rgb))
    path.write_text('\n'.join(lines)+'\n')
def clone(src,dst):
    dst.mkdir(parents=True,exist_ok=True)
    for n in ('tiles.png','metatiles.bin','metatile_attributes.bin'):shutil.copyfile(src/n,dst/n)
    (dst/'palettes').mkdir(exist_ok=True)
    for i in range(16):shutil.copyfile(src/'palettes'/f'{i:02}.pal',dst/'palettes'/f'{i:02}.pal')
def insert(path,anchor,block,marker):
    s=path.read_text()
    if marker not in s:
        assert s.count(anchor)==1,(path,anchor)
        path.write_text(s.replace(anchor,block+anchor))
def layout_id(name):return 'LAYOUT_ARAUNA_MEMORIAL_'+name.split('_',1)[1].upper()+'_V1'

def assets():
    clone(PRIMARY_SOURCE,PRIMARY);clone(SECONDARY_SOURCE,SECONDARY)
    palette(PRIMARY/'palettes/01.pal',{
        1:(197,202,216),2:(147,159,184),3:(104,119,153),4:(72,88,126),
        5:(72,80,111),6:(57,63,97),7:(42,48,82),8:(30,34,65),
        9:(155,128,211),10:(121,91,184),11:(199,161,142),
        12:(161,123,130),13:(128,87,115),14:(96,65,101),15:(100,154,140)})
    palette(PRIMARY/'palettes/02.pal',{
        1:(162,196,144),2:(113,155,113),3:(67,115,92),4:(41,71,62),
        5:(182,154,137),6:(93,82,91),7:(145,107,116),8:(60,54,68),
        9:(215,188,165),10:(182,125,130),11:(142,81,101),
        12:(139,183,163),13:(95,153,135),14:(66,133,112),15:(40,112,91)})
    palette(PRIMARY/'palettes/03.pal',{
        1:(220,222,224),2:(183,190,199),3:(150,159,174),4:(117,127,145),
        5:(86,98,119),6:(82,148,131),7:(126,183,159),8:(37,40,62),
        9:(185,184,190),10:(153,147,167),11:(122,113,145),
        12:(95,83,119),13:(75,63,103),14:(54,46,81),15:(107,158,140)})
    palette(PRIMARY/'palettes/04.pal',{
        1:(194,204,217),2:(164,180,203),6:(125,144,176),
        7:(88,112,161),8:(67,91,148),9:(53,75,127),10:(38,56,102),
        11:(147,168,202),12:(118,143,189),13:(91,120,174),
        14:(67,98,160),15:(98,145,132)})
    palette(SECONDARY/'palettes/09.pal',{
        1:(209,207,226),2:(160,162,192),3:(110,113,158),4:(76,79,128),
        5:(58,65,112),6:(91,90,125),7:(62,62,100),8:(97,94,143),
        9:(36,38,73),10:(228,193,251),11:(184,130,224),12:(142,91,192),
        13:(99,65,151),14:(179,215,216),15:(119,162,181)})
    palette(SECONDARY/'palettes/11.pal',{
        1:(60,58,85),2:(102,98,130),5:(105,92,130),
        6:(150,128,170),7:(206,184,214)})
    palette(SECONDARY/'palettes/08.pal',{
        1:(227,223,235),2:(188,191,208),3:(125,134,156),4:(87,99,132),
        5:(54,67,106),6:(167,188,182),7:(128,158,156),8:(90,127,134),
        9:(59,100,114)})
    tile=Image.open(SECONDARY/'tiles.png');assert tile.mode=='P' and tile.size==(128,256)
    art=Image.new('P',(16,16),0);d=ImageDraw.Draw(art)
    d.polygon([(7,0),(10,4),(13,10),(9,15),(4,13),(2,8)],fill=12,outline=13)
    d.polygon([(7,1),(9,5),(9,13),(5,11),(4,7)],fill=11)
    d.polygon([(7,2),(8,5),(7,9),(5,8)],fill=10)
    d.line((1,13,5,14,12,14,15,12),fill=14)
    meta=words(SECONDARY/'metatiles.bin');attrs=words(SECONDARY/'metatile_attributes.bin')
    assert len(attrs)==511 and not {v&1023 for v in meta}.intersection(range(1015,1019))
    for i,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):
        idx=1015+i;tile.paste(art.crop((x,y,x+8,y+8)),((idx-512)%16*8,(idx-512)//16*8))
    primary_meta=words(PRIMARY/'metatiles.bin');primary_attrs=words(PRIMARY/'metatile_attributes.bin')
    meta.extend(primary_meta[8:12]+[(1015+i)|(9<<12) for i in range(4)])
    attrs.append(primary_attrs[1]);tile.save(SECONDARY/'tiles.png')
    (SECONDARY/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(meta),*meta))
    (SECONDARY/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(attrs),*attrs))

def register():
    refs='\n'.join(f'    INCGFX_U16("data/tilesets/primary/arauna_memorial_exterior/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
    insert(ROOT/'src/graphics.c','// trade/egg hatch',
           'const u16 gTilesetPalettes_AraunaMemorialExterior[][16] =\n{\n'+refs+'\n};\n'
           'const u32 gTilesetTiles_AraunaMemorialExterior[] = INCGFX_U32("data/tilesets/primary/arauna_memorial_exterior/tiles.png", ".4bpp.lz");\n\n',
           'const u32 gTilesetTiles_AraunaMemorialExterior[]')
    insert(ROOT/'src/data/tilesets/metatiles.h','const u16 gMetatiles_Petalburg[]',
           'const u16 gMetatiles_AraunaMemorialExterior[] = INCBIN_U16("data/tilesets/primary/arauna_memorial_exterior/metatiles.bin");\n'
           'const u16 gMetatileAttributes_AraunaMemorialExterior[] = INCBIN_U16("data/tilesets/primary/arauna_memorial_exterior/metatile_attributes.bin");\n\n',
           'const u16 gMetatiles_AraunaMemorialExterior[]')
    insert(ROOT/'src/data/tilesets/headers.h','const struct Tileset gTileset_Petalburg =',
           'const struct Tileset gTileset_AraunaMemorialExterior =\n{\n    .isCompressed = TRUE,\n    .isSecondary = FALSE,\n'
           '    .tiles = gTilesetTiles_AraunaMemorialExterior,\n    .palettes = gTilesetPalettes_AraunaMemorialExterior,\n'
           '    .metatiles = gMetatiles_AraunaMemorialExterior,\n    .metatileAttributes = gMetatileAttributes_AraunaMemorialExterior,\n'
           '    .callback = InitTilesetAnim_General,\n};\n\n',
           'const struct Tileset gTileset_AraunaMemorialExterior =')
    refs='\n'.join(f'    INCGFX_U16("data/tilesets/secondary/arauna_memorial_nomes/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
    insert(ROOT/'src/data/tilesets/graphics.h','const u32 gTilesetTiles_AraunaAmanhecer[]',
           'const u32 gTilesetTiles_AraunaMemorialNomes[] = INCGFX_U32("data/tilesets/secondary/arauna_memorial_nomes/tiles.png", ".4bpp.lz");\n'
           'const u16 gTilesetPalettes_AraunaMemorialNomes[][16] =\n{\n'+refs+'\n};\n\n',
           'const u32 gTilesetTiles_AraunaMemorialNomes[]')
    insert(ROOT/'src/data/tilesets/metatiles.h','const u16 gMetatiles_AraunaAmanhecer[]',
           'const u16 gMetatiles_AraunaMemorialNomes[] = INCBIN_U16("data/tilesets/secondary/arauna_memorial_nomes/metatiles.bin");\n'
           'const u16 gMetatileAttributes_AraunaMemorialNomes[] = INCBIN_U16("data/tilesets/secondary/arauna_memorial_nomes/metatile_attributes.bin");\n\n',
           'const u16 gMetatiles_AraunaMemorialNomes[]')
    insert(ROOT/'src/data/tilesets/headers.h','const struct Tileset gTileset_AraunaAmanhecer =',
           'const struct Tileset gTileset_AraunaMemorialNomes =\n{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n'
           '    .tiles = gTilesetTiles_AraunaMemorialNomes,\n    .palettes = gTilesetPalettes_AraunaMemorialNomes,\n'
           '    .metatiles = gMetatiles_AraunaMemorialNomes,\n    .metatileAttributes = gMetatileAttributes_AraunaMemorialNomes,\n'
           '    .callback = NULL,\n};\n\n',
           'const struct Tileset gTileset_AraunaMemorialNomes =')

def main():
    assets();register();path=ROOT/'data/layouts/layouts.json';node=json.loads(path.read_text());report={}
    for name in MAPS:
        map_path=ROOT/'data/maps'/name/'map.json';event=json.loads(map_path.read_text())
        if event['layout'].startswith('LAYOUT_ARAUNA_MEMORIAL_'):
            old_event=json.loads(subprocess.check_output(['git','show',f'HEAD:data/maps/{name}/map.json'],cwd=ROOT))
            original=next(r for r in node['layouts'] if r['id']==old_event['layout'])
        else:original=next(r for r in node['layouts'] if r['id']==event['layout'])
        new_id=layout_id(name);w,h=original['width'],original['height'];old=words(ROOT/original['blockdata_filepath']);assert len(old)==w*h
        new=list(old);crystals=0
        if name=='MtPyre_Summit':
            occupied={(int(e['x']),int(e['y'])) for group in ('warp_events','object_events','coord_events','bg_events') for e in event[group]}
            for x,y in ((20,3),(26,3),(20,5),(26,5),(11,13),(37,13),(21,20),(29,20)):
                assert old[y*w+x]&1023==1 and (x,y) not in occupied,(x,y,old[y*w+x]&1023)
                new[y*w+x]=(old[y*w+x]&~1023)|CRYSTAL;crystals+=1
        folder=ROOT/'data/layouts'/('AraunaMemorial_'+name.split('_',1)[1]);folder.mkdir(exist_ok=True)
        (folder/'map.bin').write_bytes(struct.pack('<%dH'%len(new),*new))
        shutil.copyfile(ROOT/original['border_filepath'],folder/'border.bin')
        record=dict(original,id=new_id,name=folder.name+'_Layout',
                    primary_tileset='gTileset_AraunaMemorialExterior',
                    secondary_tileset='gTileset_AraunaMemorialNomes',
                    blockdata_filepath=str((folder/'map.bin').relative_to(ROOT)),border_filepath=str((folder/'border.bin').relative_to(ROOT)))
        current=next((r for r in node['layouts'] if r['id']==new_id),None)
        if current:current.update(record)
        else:node['layouts'].append(record)
        event['layout']=new_id;dump(map_path,event)
        report[name]={'size':[w,h],'crystals':crystals,'warps':len(event['warp_events'])}
    dump(path,node);print(json.dumps(report,indent=2))

if __name__=='__main__':main()
