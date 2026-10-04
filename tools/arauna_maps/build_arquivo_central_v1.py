#!/usr/bin/env python3
"""Give Aqua Hideout a damp, technical archive identity."""
import json,shutil,struct,subprocess
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
MAPS=tuple(p.parent.name for p in sorted((ROOT/'data/maps').glob('AquaHideout*/map.json')))
SOURCE=ROOT/'data/tilesets/secondary/facility'
TARGET=ROOT/'data/tilesets/secondary/arauna_arquivo_central'
BASE=1023

def words(path):
    b=path.read_bytes();return list(struct.unpack('<%dH'%(len(b)//2),b))
def dump(path,node):path.write_text(json.dumps(node,indent=2,ensure_ascii=False)+'\n')
def palette(path,changes):
    lines=path.read_text().splitlines();assert lines[:3]==['JASC-PAL','0100','16'] and len(lines)==19
    for i,rgb in changes.items():lines[i+3]=' '.join(map(str,rgb))
    path.write_text('\n'.join(lines)+'\n')
def insert(path,anchor,block,marker):
    s=path.read_text()
    if marker not in s:
        assert s.count(anchor)==1,(path,anchor)
        path.write_text(s.replace(anchor,block+anchor))
def layout_id(name):return 'LAYOUT_ARAUNA_ARQUIVO_'+name.split('_',1)[1].upper()+'_V1'

def assets():
    TARGET.mkdir(parents=True,exist_ok=True)
    for n in ('tiles.png','metatiles.bin','metatile_attributes.bin'):shutil.copyfile(SOURCE/n,TARGET/n)
    (TARGET/'palettes').mkdir(exist_ok=True)
    for i in range(16):shutil.copyfile(SOURCE/'palettes'/f'{i:02}.pal',TARGET/'palettes'/f'{i:02}.pal')
    palette(TARGET/'palettes/06.pal',{
        1:(223,234,220),2:(183,210,203),3:(133,172,174),4:(74,102,119),
        5:(38,65,82),6:(205,207,178),7:(170,174,148),8:(131,146,132),
        9:(103,115,104),10:(143,164,155),11:(100,133,137),12:(70,106,115),
        13:(51,86,91),14:(188,132,82),15:(203,193,106)})
    palette(TARGET/'palettes/07.pal',{
        1:(225,235,217),2:(198,213,181),3:(161,184,154),4:(108,150,129),
        5:(40,72,87),6:(75,104,107),7:(107,91,66),8:(73,68,57),
        9:(39,55,55),10:(210,220,191),11:(174,196,162),12:(133,170,139),
        13:(91,139,114),14:(105,194,211),15:(142,168,154)})
    palette(TARGET/'palettes/08.pal',{
        1:(227,238,213),2:(188,212,213),3:(101,126,137),4:(61,92,112),
        5:(34,59,80),6:(161,198,171),7:(122,167,149),8:(83,139,123),
        9:(52,109,106),10:(140,170,151),11:(104,138,130),
        12:(190,153,87),13:(145,109,65),14:(102,76,53)})
    palette(TARGET/'palettes/09.pal',{
        1:(223,242,223),2:(185,213,221),3:(125,170,202),4:(67,112,158),
        5:(31,67,111),6:(64,86,119),7:(42,66,98),8:(75,127,154),
        9:(33,55,88),10:(173,223,171),11:(100,209,148),12:(67,172,116),
        13:(45,122,91),14:(105,191,218),15:(66,143,177)})
    palette(TARGET/'palettes/11.pal',{
        1:(61,72,67),2:(92,102,78),5:(108,112,72),6:(150,154,93),7:(188,188,125)})
    tile=Image.open(TARGET/'tiles.png');assert tile.mode=='P' and tile.size==(128,256)
    art=Image.new('P',(16,16),0);d=ImageDraw.Draw(art)
    d.ellipse((2,2,13,13),outline=11,width=1)
    d.line((3,10,6,7,9,9,12,4),fill=14,width=2)
    d.line((4,5,7,8,11,7),fill=12,width=1)
    for x,y in ((4,4),(11,4),(5,12),(12,11)):d.point((x,y),fill=10)
    meta=words(TARGET/'metatiles.bin');attrs=words(TARGET/'metatile_attributes.bin')
    assert len(attrs)==511 and not {v&1023 for v in meta}.intersection(range(1015,1019))
    for i,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):
        idx=1015+i;tile.paste(art.crop((x,y,x+8,y+8)),((idx-512)%16*8,(idx-512)//16*8))
    src=552;meta.extend(meta[(src-512)*8:(src-512)*8+4]+[(1015+i)|(9<<12) for i in range(4)])
    attrs.append(attrs[src-512]);tile.save(TARGET/'tiles.png')
    (TARGET/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(meta),*meta))
    (TARGET/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(attrs),*attrs))

def register():
    refs='\n'.join(f'    INCGFX_U16("data/tilesets/secondary/arauna_arquivo_central/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
    insert(ROOT/'src/data/tilesets/graphics.h','const u32 gTilesetTiles_AraunaAmanhecer[]',
           'const u32 gTilesetTiles_AraunaArquivoCentral[] = INCGFX_U32("data/tilesets/secondary/arauna_arquivo_central/tiles.png", ".4bpp.lz");\n'
           'const u16 gTilesetPalettes_AraunaArquivoCentral[][16] =\n{\n'+refs+'\n};\n\n',
           'const u32 gTilesetTiles_AraunaArquivoCentral[]')
    insert(ROOT/'src/data/tilesets/metatiles.h','const u16 gMetatiles_AraunaAmanhecer[]',
           'const u16 gMetatiles_AraunaArquivoCentral[] = INCBIN_U16("data/tilesets/secondary/arauna_arquivo_central/metatiles.bin");\n'
           'const u16 gMetatileAttributes_AraunaArquivoCentral[] = INCBIN_U16("data/tilesets/secondary/arauna_arquivo_central/metatile_attributes.bin");\n\n',
           'const u16 gMetatiles_AraunaArquivoCentral[]')
    insert(ROOT/'src/data/tilesets/headers.h','const struct Tileset gTileset_AraunaAmanhecer =',
           'const struct Tileset gTileset_AraunaArquivoCentral =\n{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n'
           '    .tiles = gTilesetTiles_AraunaArquivoCentral,\n    .palettes = gTilesetPalettes_AraunaArquivoCentral,\n'
           '    .metatiles = gMetatiles_AraunaArquivoCentral,\n    .metatileAttributes = gMetatileAttributes_AraunaArquivoCentral,\n'
           '    .callback = NULL,\n};\n\n',
           'const struct Tileset gTileset_AraunaArquivoCentral =')

def main():
    assets();register();path=ROOT/'data/layouts/layouts.json';node=json.loads(path.read_text());report={}
    for name in MAPS:
        map_path=ROOT/'data/maps'/name/'map.json';event=json.loads(map_path.read_text())
        if event['layout'].startswith('LAYOUT_ARAUNA_ARQUIVO_'):
            old_event=json.loads(subprocess.check_output(['git','show',f'HEAD:data/maps/{name}/map.json'],cwd=ROOT))
            original=next(r for r in node['layouts'] if r['id']==old_event['layout'])
        else:original=next(r for r in node['layouts'] if r['id']==event['layout'])
        new_id=layout_id(name);w,h=original['width'],original['height']
        old=words(ROOT/original['blockdata_filepath']);assert len(old)==w*h
        occupied={(int(e['x']),int(e['y'])) for group in ('warp_events','object_events','coord_events','bg_events') for e in event[group]}
        new=list(old);count=0
        for y in range(2,h-2):
            for x in range(2,w-2):
                i=y*w+x
                if old[i]&1023!=552 or (x,y) in occupied:continue
                if any(abs(x-a)+abs(y-b)<2 for a,b in occupied):continue
                if (x*31+y*17+x*y+len(name))%37==7:
                    new[i]=(old[i]&~1023)|BASE;count+=1
        folder=ROOT/'data/layouts'/('AraunaArquivo_'+name.split('_',1)[1]);folder.mkdir(exist_ok=True)
        (folder/'map.bin').write_bytes(struct.pack('<%dH'%len(new),*new))
        shutil.copyfile(ROOT/original['border_filepath'],folder/'border.bin')
        record=dict(original,id=new_id,name='AraunaArquivo_'+name.split('_',1)[1]+'_Layout',
                    secondary_tileset='gTileset_AraunaArquivoCentral',
                    blockdata_filepath=str((folder/'map.bin').relative_to(ROOT)),
                    border_filepath=str((folder/'border.bin').relative_to(ROOT)))
        current=next((r for r in node['layouts'] if r['id']==new_id),None)
        if current:current.update(record)
        else:node['layouts'].append(record)
        event['layout']=new_id;dump(map_path,event)
        report[name]={'size':[w,h],'archive_seals':count,'warps':len(event['warp_events'])}
    dump(path,node);print(json.dumps(report,indent=2))

if __name__=='__main__':main()
