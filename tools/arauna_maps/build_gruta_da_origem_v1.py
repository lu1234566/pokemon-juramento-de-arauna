#!/usr/bin/env python3
"""Adapt Cave of Origin to dark primordial stone and green mineral life."""
import json,shutil,struct,subprocess
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
MAPS=tuple(p.parent.name for p in sorted((ROOT/'data/maps').glob('CaveOfOrigin*/map.json')))
SOURCE=ROOT/'data/tilesets/secondary/cave'
TARGET=ROOT/'data/tilesets/secondary/arauna_gruta_origem'
BASE=512+414

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
def layout_id(name):return 'LAYOUT_ARAUNA_ORIGEM_'+name.split('_',1)[1].upper()+'_V1'

def assets():
    TARGET.mkdir(parents=True,exist_ok=True)
    for n in ('tiles.png','metatiles.bin','metatile_attributes.bin'):shutil.copyfile(SOURCE/n,TARGET/n)
    (TARGET/'palettes').mkdir(exist_ok=True)
    for i in range(16):shutil.copyfile(SOURCE/'palettes'/f'{i:02}.pal',TARGET/'palettes'/f'{i:02}.pal')
    palette(TARGET/'palettes/07.pal',{
        0:(39,63,69),1:(210,218,196),2:(176,189,175),3:(144,164,156),
        4:(109,135,133),5:(80,111,118),6:(55,84,99),7:(33,58,78),
        8:(224,239,205),9:(150,218,172),10:(87,188,146),11:(40,142,120),
        12:(188,230,132),13:(102,198,97),14:(47,145,83),15:(25,66,61)})
    palette(TARGET/'palettes/11.pal',{
        1:(34,87,68),2:(51,125,74),3:(77,158,84),4:(112,188,102),
        5:(155,214,138),6:(87,162,148),7:(45,121,134),
        8:(222,242,195),9:(154,224,155)})
    image=Image.open(TARGET/'tiles.png');assert image.mode=='P' and image.size==(128,216)
    sheet=Image.new('P',(128,256),0);sheet.putpalette(image.getpalette());sheet.paste(image,(0,0))
    meta=words(TARGET/'metatiles.bin');attrs=words(TARGET/'metatile_attributes.bin')
    assert len(attrs)==414 and not {x&1023 for x in meta}.intersection(range(0x3f8,0x400))
    moss=Image.new('P',(16,16),0);d=ImageDraw.Draw(moss)
    d.polygon(((2,10),(5,7),(8,10),(11,7),(14,10),(11,13),(5,12)),fill=2)
    d.line((4,9,7,7,10,9,13,8),fill=4,width=1)
    for x,y in ((2,6),(7,4),(12,4),(14,12)):d.point((x,y),fill=5)
    roots=Image.new('P',(16,16),0);d=ImageDraw.Draw(roots)
    d.line((8,1,7,5,4,8,3,14),fill=2,width=1)
    d.line((7,5,12,8,13,13),fill=3,width=1)
    d.line((5,8,9,11,9,15),fill=4,width=1)
    for x,y in ((4,10),(12,11),(9,14)):d.point((x,y),fill=5)
    for kind,art in enumerate((moss,roots)):
        start=0x3f8+kind*4
        for i,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):
            index=start+i
            sheet.paste(art.crop((x,y,x+8,y+8)),((index-512)%16*8,(index-512)//16*8))
        src=(819,795)[kind]
        meta.extend(meta[(src-512)*8:(src-512)*8+4]+[(start+i)|(11<<12) for i in range(4)])
        attrs.append(attrs[src-512])
    sheet.save(TARGET/'tiles.png')
    (TARGET/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(meta),*meta))
    (TARGET/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(attrs),*attrs))

def register():
    refs='\n'.join(f'    INCGFX_U16("data/tilesets/secondary/arauna_gruta_origem/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
    insert(ROOT/'src/data/tilesets/graphics.h','const u32 gTilesetTiles_AraunaAmanhecer[]',
           'const u32 gTilesetTiles_AraunaGrutaOrigem[] = INCGFX_U32("data/tilesets/secondary/arauna_gruta_origem/tiles.png", ".4bpp.lz");\n'
           'const u16 gTilesetPalettes_AraunaGrutaOrigem[][16] =\n{\n'+refs+'\n};\n\n',
           'const u32 gTilesetTiles_AraunaGrutaOrigem[]')
    insert(ROOT/'src/data/tilesets/metatiles.h','const u16 gMetatiles_AraunaAmanhecer[]',
           'const u16 gMetatiles_AraunaGrutaOrigem[] = INCBIN_U16("data/tilesets/secondary/arauna_gruta_origem/metatiles.bin");\n'
           'const u16 gMetatileAttributes_AraunaGrutaOrigem[] = INCBIN_U16("data/tilesets/secondary/arauna_gruta_origem/metatile_attributes.bin");\n\n',
           'const u16 gMetatiles_AraunaGrutaOrigem[]')
    insert(ROOT/'src/data/tilesets/headers.h','const struct Tileset gTileset_AraunaAmanhecer =',
           'const struct Tileset gTileset_AraunaGrutaOrigem =\n{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n'
           '    .tiles = gTilesetTiles_AraunaGrutaOrigem,\n    .palettes = gTilesetPalettes_AraunaGrutaOrigem,\n'
           '    .metatiles = gMetatiles_AraunaGrutaOrigem,\n    .metatileAttributes = gMetatileAttributes_AraunaGrutaOrigem,\n'
           '    .callback = NULL,\n};\n\n',
           'const struct Tileset gTileset_AraunaGrutaOrigem =')

def main():
    assets();register()
    path=ROOT/'data/layouts/layouts.json';node=json.loads(path.read_text());report={}
    for name in MAPS:
        map_path=ROOT/'data/maps'/name/'map.json';event=json.loads(map_path.read_text())
        if event['layout'].startswith('LAYOUT_ARAUNA_ORIGEM_'):
            old_event=json.loads(subprocess.check_output(['git','show',f'HEAD:data/maps/{name}/map.json'],cwd=ROOT))
            original=next(r for r in node['layouts'] if r['id']==old_event['layout'])
        else:original=next(r for r in node['layouts'] if r['id']==event['layout'])
        new_id=layout_id(name);assert event['layout'] in (original['id'],new_id)
        w,h=original['width'],original['height'];old=words(ROOT/original['blockdata_filepath']);assert len(old)==w*h
        occupied={(int(e['x']),int(e['y'])) for group in ('warp_events','object_events','coord_events','bg_events') for e in event[group]}
        new=list(old);counts=[0,0]
        for y in range(2,h-2):
            for x in range(2,w-2):
                i=y*w+x;tile=old[i]&1023
                if (x,y) in occupied or any(abs(x-a)+abs(y-b)<2 for a,b in occupied):continue
                salt=(x*13+y*17+x*y*3+len(name))%47
                kind=0 if tile==819 and salt in (2,19) else (1 if tile==795 and salt==11 else None)
                if kind is not None:
                    new[i]=(old[i]&~1023)|(BASE+kind);counts[kind]+=1
        folder=ROOT/'data/layouts'/('AraunaOrigem_'+name.split('_',1)[1]);folder.mkdir(exist_ok=True)
        (folder/'map.bin').write_bytes(struct.pack('<%dH'%len(new),*new))
        shutil.copyfile(ROOT/original['border_filepath'],folder/'border.bin')
        record=dict(original,id=new_id,name='AraunaOrigem_'+name.split('_',1)[1]+'_Layout',
                    secondary_tileset='gTileset_AraunaGrutaOrigem',
                    blockdata_filepath=str((folder/'map.bin').relative_to(ROOT)),
                    border_filepath=str((folder/'border.bin').relative_to(ROOT)))
        found=next((r for r in node['layouts'] if r['id']==new_id),None)
        if found:found.update(record)
        else:node['layouts'].append(record)
        event['layout']=new_id;dump(map_path,event)
        report[name]={'size':[w,h],'moss_and_roots':counts,'warps':len(event['warp_events'])}
    dump(path,node);print(json.dumps(report,indent=2))

if __name__=='__main__':main()
