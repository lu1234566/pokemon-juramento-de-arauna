#!/usr/bin/env python3
"""Build a coherent naval-ruin treatment for all Abandoned Ship maps."""
import json,shutil,struct
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
MAPS=tuple(p.parent.name for p in sorted((ROOT/'data/maps').glob('AbandonedShip*/map.json')))
PRIMARY=ROOT/'data/tilesets/primary/arauna_navio_mar'
FACILITY=ROOT/'data/tilesets/secondary/arauna_navio_conves'
SHIP=ROOT/'data/tilesets/secondary/arauna_navio_interior'
FLOODED=ROOT/'data/tilesets/secondary/arauna_navio_alagado'
FLOODED_MAPS={'AbandonedShip_HiddenFloorCorridors','AbandonedShip_HiddenFloorRooms',
              'AbandonedShip_Underwater1','AbandonedShip_Underwater2'}
BASE=512+252

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
def layout_id(name):return 'LAYOUT_ARAUNA_NAVIO_'+name.split('_',1)[1].upper()+'_V1'

def assets():
    clone(ROOT/'data/tilesets/primary/general',PRIMARY)
    clone(ROOT/'data/tilesets/secondary/facility',FACILITY)
    clone(ROOT/'data/tilesets/secondary/inside_ship',SHIP)
    palette(PRIMARY/'palettes/04.pal',{
        6:(129,160,194),7:(39,110,179),8:(27,94,162),9:(24,76,143),
        10:(18,61,124),11:(133,185,218),12:(96,157,206),
        13:(69,134,190),14:(42,107,167)})
    palette(PRIMARY/'palettes/03.pal',{
        8:(42,53,65),9:(206,195,164),10:(179,163,132),11:(151,132,105),
        12:(117,99,85),13:(85,71,69),14:(57,54,63)})
    palette(FACILITY/'palettes/06.pal',{
        2:(180,197,207),3:(140,165,183),4:(86,112,140),5:(51,74,105),
        6:(216,201,170),7:(185,155,120),8:(150,117,90),9:(114,83,69),
        10:(196,209,211),11:(159,178,187),12:(118,148,167),13:(78,112,139),
        14:(182,91,51)})
    palette(FACILITY/'palettes/07.pal',{
        2:(217,192,144),3:(188,148,102),4:(151,99,68),5:(48,68,93),
        6:(91,111,129),7:(118,81,57),8:(84,61,52),9:(52,54,62),
        10:(192,161,119),11:(149,116,82),12:(109,83,65),
        13:(96,121,116),14:(114,178,198)})
    palette(FACILITY/'palettes/08.pal',{
        2:(187,203,211),3:(127,151,170),4:(81,108,136),5:(51,77,111),
        6:(120,160,151),7:(95,134,127),8:(78,111,105),9:(56,85,88),
        10:(179,166,153),11:(144,123,113),12:(172,97,62),
        13:(147,71,47),14:(109,53,44)})
    palette(FACILITY/'palettes/09.pal',{
        2:(191,214,226),3:(132,178,204),4:(76,128,174),5:(39,89,142),
        8:(74,105,144),9:(30,55,92),10:(177,224,200),
        11:(98,194,162),12:(64,160,136),13:(43,117,109)})
    palette(SHIP/'palettes/06.pal',{
        1:(44,62,83),2:(96,112,124),3:(159,177,180),4:(224,224,205),
        5:(91,110,137),6:(124,146,158),7:(161,184,198),8:(194,213,222),
        9:(86,107,137),10:(104,136,169),11:(130,165,192),
        12:(139,159,182),13:(89,153,199),14:(97,161,141)})
    palette(SHIP/'palettes/07.pal',{
        1:(43,59,78),2:(89,105,116),3:(168,182,178),4:(224,222,196),
        5:(144,100,67),6:(178,129,76),7:(199,170,111),8:(112,74,55),
        9:(129,71,55),10:(151,85,62),11:(137,103,82),12:(174,132,99),
        13:(129,161,184),14:(137,135,61),15:(225,199,101)})
    palette(SHIP/'palettes/08.pal',{
        1:(43,59,78),2:(104,121,130),3:(168,181,177),4:(222,222,202),
        5:(90,112,79),6:(124,139,100),7:(172,181,123),8:(207,207,160),
        9:(82,137,126),10:(107,167,129),11:(149,192,143),
        12:(184,113,57),13:(217,149,71),14:(220,126,85),15:(172,65,33)})
    palette(SHIP/'palettes/09.pal',{
        1:(42,61,80),2:(93,112,124),3:(162,180,180),4:(220,222,207),
        5:(112,104,70),6:(151,140,91),7:(189,179,110),8:(190,213,225),
        9:(76,111,151),10:(99,143,181),11:(128,172,202),
        12:(161,117,79),13:(71,132,177),14:(88,153,141)})
    palette(SHIP/'palettes/10.pal',{
        1:(43,59,83),2:(80,110,133),3:(143,176,189),4:(190,216,222),
        5:(41,78,124),6:(57,100,149),7:(97,145,184),8:(174,210,225),
        9:(63,101,153),10:(88,131,177),11:(117,160,198),
        12:(108,142,177),13:(68,135,194),14:(85,151,142)})
    palette(SHIP/'palettes/11.pal',{
        1:(34,65,88),2:(51,106,133),3:(86,152,170),4:(138,190,190),
        5:(107,66,47),6:(153,84,50),7:(202,119,64),8:(237,160,81)})
    image=Image.open(SHIP/'tiles.png');assert image.mode=='P' and image.size==(128,176)
    expanded=Image.new('P',(128,256),0);expanded.putpalette(image.getpalette());expanded.paste(image,(0,0))
    meta=words(SHIP/'metatiles.bin');attrs=words(SHIP/'metatile_attributes.bin')
    assert len(attrs)==252 and not {v&1023 for v in meta}.intersection(range(0x3f8,0x400))
    rust=Image.new('P',(16,16),0);d=ImageDraw.Draw(rust)
    d.polygon(((2,3),(8,2),(12,6),(10,11),(4,12),(2,8)),fill=5)
    d.line((3,5,8,4,11,7),fill=7,width=1)
    d.point((6,9),fill=8);d.point((10,11),fill=6)
    seep=Image.new('P',(16,16),0);d=ImageDraw.Draw(seep)
    d.polygon(((2,9),(5,7),(9,8),(13,6),(14,11),(10,13),(5,12)),fill=2)
    d.line((4,9,8,9,12,8),fill=4,width=1)
    d.point((6,12),fill=3)
    for kind,art in enumerate((rust,seep)):
        start=0x3f8+kind*4
        for i,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):
            idx=start+i;expanded.paste(art.crop((x,y,x+8,y+8)),((idx-512)%16*8,(idx-512)//16*8))
        src=(568,514)[kind]
        meta.extend(meta[(src-512)*8:(src-512)*8+4]+[(start+i)|(11<<12) for i in range(4)])
        attrs.append(attrs[src-512])
    expanded.save(SHIP/'tiles.png')
    (SHIP/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(meta),*meta))
    (SHIP/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(attrs),*attrs))
    clone(SHIP,FLOODED)
    palette(FLOODED/'palettes/07.pal',{
        9:(117,74,58),10:(144,91,66),11:(37,100,153),12:(65,132,177)})

def register():
    refs='\n'.join(f'    INCGFX_U16("data/tilesets/primary/arauna_navio_mar/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
    insert(ROOT/'src/graphics.c','// trade/egg hatch',
           'const u16 gTilesetPalettes_AraunaNavioMar[][16] =\n{\n'+refs+'\n};\n'
           'const u32 gTilesetTiles_AraunaNavioMar[] = INCGFX_U32("data/tilesets/primary/arauna_navio_mar/tiles.png", ".4bpp.lz");\n\n',
           'const u32 gTilesetTiles_AraunaNavioMar[]')
    insert(ROOT/'src/data/tilesets/metatiles.h','const u16 gMetatiles_Petalburg[]',
           'const u16 gMetatiles_AraunaNavioMar[] = INCBIN_U16("data/tilesets/primary/arauna_navio_mar/metatiles.bin");\n'
           'const u16 gMetatileAttributes_AraunaNavioMar[] = INCBIN_U16("data/tilesets/primary/arauna_navio_mar/metatile_attributes.bin");\n\n',
           'const u16 gMetatiles_AraunaNavioMar[]')
    insert(ROOT/'src/data/tilesets/headers.h','const struct Tileset gTileset_Petalburg =',
           'const struct Tileset gTileset_AraunaNavioMar =\n{\n    .isCompressed = TRUE,\n    .isSecondary = FALSE,\n'
           '    .tiles = gTilesetTiles_AraunaNavioMar,\n    .palettes = gTilesetPalettes_AraunaNavioMar,\n'
           '    .metatiles = gMetatiles_AraunaNavioMar,\n    .metatileAttributes = gMetatileAttributes_AraunaNavioMar,\n'
           '    .callback = InitTilesetAnim_General,\n};\n\n',
           'const struct Tileset gTileset_AraunaNavioMar =')
    refs=[];metas=[];headers=[]
    for name,slug in (('AraunaNavioConves','arauna_navio_conves'),
                      ('AraunaNavioInterior','arauna_navio_interior'),
                      ('AraunaNavioAlagado','arauna_navio_alagado')):
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
           '\n'.join(refs)+'\n','const u32 gTilesetTiles_AraunaNavioConves[]')
    insert(ROOT/'src/data/tilesets/metatiles.h','const u16 gMetatiles_AraunaAmanhecer[]',
           '\n'.join(metas)+'\n','const u16 gMetatiles_AraunaNavioConves[]')
    insert(ROOT/'src/data/tilesets/headers.h','const struct Tileset gTileset_AraunaAmanhecer =',
           '\n'.join(headers)+'\n','const struct Tileset gTileset_AraunaNavioConves =')

def main():
    assets();register()
    path=ROOT/'data/layouts/layouts.json';node=json.loads(path.read_text());report={}
    for name in MAPS:
        map_path=ROOT/'data/maps'/name/'map.json';event=json.loads(map_path.read_text())
        original=next(r for r in node['layouts'] if r['id']==event['layout']) if not event['layout'].startswith('LAYOUT_ARAUNA_NAVIO_') else None
        old_id='LAYOUT_ABANDONED_SHIP_'+name.split('_',1)[1].upper()
        # The original IDs use underscores in multiword room labels; resolve from HEAD once.
        if original is None:
            old_event=json.loads(__import__('subprocess').check_output(['git','show',f'HEAD:data/maps/{name}/map.json'],cwd=ROOT))
            original=next(r for r in node['layouts'] if r['id']==old_event['layout'])
        new_id=layout_id(name)
        assert event['layout'] in (original['id'],new_id)
        w,h=original['width'],original['height']
        old=words(ROOT/original['blockdata_filepath']);assert len(old)==w*h
        new=list(old);counts=[0,0]
        inside=original['secondary_tileset']=='gTileset_InsideShip'
        if inside:
            occupied={(int(e['x']),int(e['y'])) for key in ('warp_events','object_events','coord_events','bg_events') for e in event[key]}
            for y in range(1,h-1):
                for x in range(1,w-1):
                    i=y*w+x;tile=old[i]&1023
                    if (x,y) in occupied or any(abs(x-a)+abs(y-b)<2 for a,b in occupied):continue
                    salt=(x*17+y*29+x*y*3+len(name))%61
                    kind=0 if tile==568 and salt in (4,31) else (1 if tile==514 and salt==17 else None)
                    if kind is not None:
                        new[i]=(old[i]&~1023)|(BASE+kind);counts[kind]+=1
        folder=ROOT/'data/layouts'/('AraunaNavio_'+name.split('_',1)[1]);folder.mkdir(exist_ok=True)
        (folder/'map.bin').write_bytes(struct.pack('<%dH'%len(new),*new))
        shutil.copyfile(ROOT/original['border_filepath'],folder/'border.bin')
        record=dict(original,id=new_id,name='AraunaNavio_'+name.split('_',1)[1]+'_Layout',
                    primary_tileset='gTileset_AraunaNavioMar',
                    secondary_tileset=('gTileset_AraunaNavioAlagado' if name in FLOODED_MAPS else
                                       'gTileset_AraunaNavioInterior' if inside else 'gTileset_AraunaNavioConves'),
                    blockdata_filepath=str((folder/'map.bin').relative_to(ROOT)),
                    border_filepath=str((folder/'border.bin').relative_to(ROOT)))
        current=next((r for r in node['layouts'] if r['id']==new_id),None)
        if current:current.update(record)
        else:node['layouts'].append(record)
        event['layout']=new_id;dump(map_path,event)
        report[name]={'size':[w,h],'rust_and_seep':counts,'warps':len(event['warp_events'])}
    dump(path,node)
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
