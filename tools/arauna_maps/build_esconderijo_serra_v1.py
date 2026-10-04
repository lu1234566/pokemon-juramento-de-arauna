#!/usr/bin/env python3
"""Turn Magma Hideout into a mined mountain with increasing industry."""
import json,shutil,struct,subprocess
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
MAPS=tuple(p.parent.name for p in sorted((ROOT/'data/maps').glob('MagmaHideout*/map.json')))
SOURCE=ROOT/'data/tilesets/secondary/lavaridge'
TARGET=ROOT/'data/tilesets/secondary/arauna_esconderijo_serra'
BASE=512+441

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
def layout_id(name):return 'LAYOUT_ARAUNA_ESCONDERIJO_'+name.split('_',1)[1].upper()+'_V1'

def assets():
    TARGET.mkdir(parents=True,exist_ok=True)
    for n in ('tiles.png','metatiles.bin','metatile_attributes.bin'):shutil.copyfile(SOURCE/n,TARGET/n)
    (TARGET/'palettes').mkdir(exist_ok=True)
    for i in range(16):shutil.copyfile(SOURCE/'palettes'/f'{i:02}.pal',TARGET/'palettes'/f'{i:02}.pal')
    palette(TARGET/'palettes/10.pal',{
        0:(48,43,44),1:(196,171,137),2:(167,143,113),3:(138,116,99),
        4:(107,91,81),5:(77,68,69),8:(42,41,46),
        9:(183,136,95),10:(154,110,82),11:(127,85,69),
        12:(98,67,61),13:(72,51,53),14:(46,39,46)})
    palette(TARGET/'palettes/11.pal',{
        0:(48,43,44),1:(228,204,168),2:(207,183,148),3:(181,158,129),
        4:(153,134,115),6:(120,107,101),8:(82,76,76),
        9:(235,207,155),10:(211,178,129),11:(185,149,110),
        12:(156,118,95),13:(124,88,79),14:(87,64,64),15:(70,63,57)})
    palette(TARGET/'palettes/09.pal',{
        1:(50,57,65),2:(75,87,96),3:(111,117,115),4:(152,143,119),
        5:(191,156,95),6:(226,184,83),7:(246,212,111)})
    palette(TARGET/'palettes/06.pal',{
        1:(61,69,80),2:(180,165,72),3:(225,224,205),
        7:(153,87,60),8:(119,63,54),9:(224,78,24),10:(177,57,28),
        11:(246,110,27),12:(249,165,48),14:(105,117,127)})
    palette(TARGET/'palettes/07.pal',{
        5:(104,91,78),6:(83,79,78),7:(59,64,68),8:(42,47,55),
        9:(167,143,98),10:(197,167,106),11:(241,220,162),
        12:(219,194,137),13:(180,153,94),14:(151,122,72),15:(108,159,133)})
    palette(TARGET/'palettes/08.pal',{
        1:(244,225,166),4:(192,172,124),5:(149,137,111),
        6:(91,88,85),7:(65,69,70),8:(43,49,55),
        9:(214,179,100),10:(182,144,76),11:(249,215,118),
        12:(222,177,85),13:(176,133,68),14:(134,99,48),15:(97,72,46)})
    original=Image.open(TARGET/'tiles.png');assert original.mode=='P' and original.size==(128,232)
    sheet=Image.new('P',(128,256),0);sheet.putpalette(original.getpalette());sheet.paste(original,(0,0))
    meta=words(TARGET/'metatiles.bin');attrs=words(TARGET/'metatile_attributes.bin')
    assert len(attrs)==441 and not {v&1023 for v in meta}.intersection(range(0x3f8,0x400))
    duct=Image.new('P',(16,16),0);d=ImageDraw.Draw(duct)
    d.rectangle((1,5,14,10),fill=3,outline=2,width=1)
    d.line((3,6,3,9),fill=6,width=1);d.line((12,6,12,9),fill=6,width=1)
    d.point((7,7),fill=7);d.point((9,8),fill=5)
    cable=Image.new('P',(16,16),0);d=ImageDraw.Draw(cable)
    d.line((0,11,4,9,8,11,11,7,15,8),fill=2,width=2)
    d.line((4,9,8,11,11,7),fill=4,width=1)
    for x,y in ((3,9),(11,7)):d.ellipse((x-1,y-1,x+1,y+1),fill=6)
    for kind,art in enumerate((duct,cable)):
        start=0x3f8+kind*4
        for i,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):
            idx=start+i;sheet.paste(art.crop((x,y,x+8,y+8)),((idx-512)%16*8,(idx-512)//16*8))
        src=(625,776)[kind]
        meta.extend(meta[(src-512)*8:(src-512)*8+4]+[(start+i)|(9<<12) for i in range(4)])
        attrs.append(attrs[src-512])
    sheet.save(TARGET/'tiles.png')
    (TARGET/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(meta),*meta))
    (TARGET/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(attrs),*attrs))

def register():
    refs='\n'.join(f'    INCGFX_U16("data/tilesets/secondary/arauna_esconderijo_serra/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
    insert(ROOT/'src/data/tilesets/graphics.h','const u32 gTilesetTiles_AraunaAmanhecer[]',
           'const u32 gTilesetTiles_AraunaEsconderijoSerra[] = INCGFX_U32("data/tilesets/secondary/arauna_esconderijo_serra/tiles.png", ".4bpp.lz");\n'
           'const u16 gTilesetPalettes_AraunaEsconderijoSerra[][16] =\n{\n'+refs+'\n};\n\n',
           'const u32 gTilesetTiles_AraunaEsconderijoSerra[]')
    insert(ROOT/'src/data/tilesets/metatiles.h','const u16 gMetatiles_AraunaAmanhecer[]',
           'const u16 gMetatiles_AraunaEsconderijoSerra[] = INCBIN_U16("data/tilesets/secondary/arauna_esconderijo_serra/metatiles.bin");\n'
           'const u16 gMetatileAttributes_AraunaEsconderijoSerra[] = INCBIN_U16("data/tilesets/secondary/arauna_esconderijo_serra/metatile_attributes.bin");\n\n',
           'const u16 gMetatiles_AraunaEsconderijoSerra[]')
    insert(ROOT/'src/data/tilesets/headers.h','const struct Tileset gTileset_AraunaAmanhecer =',
           'const struct Tileset gTileset_AraunaEsconderijoSerra =\n{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n'
           '    .tiles = gTilesetTiles_AraunaEsconderijoSerra,\n    .palettes = gTilesetPalettes_AraunaEsconderijoSerra,\n'
           '    .metatiles = gMetatiles_AraunaEsconderijoSerra,\n    .metatileAttributes = gMetatileAttributes_AraunaEsconderijoSerra,\n'
           '    .callback = NULL,\n};\n\n',
           'const struct Tileset gTileset_AraunaEsconderijoSerra =')

def main():
    assets();register()
    path=ROOT/'data/layouts/layouts.json';node=json.loads(path.read_text());report={}
    for name in MAPS:
        map_path=ROOT/'data/maps'/name/'map.json';event=json.loads(map_path.read_text())
        if event['layout'].startswith('LAYOUT_ARAUNA_ESCONDERIJO_'):
            old_event=json.loads(subprocess.check_output(['git','show',f'HEAD:data/maps/{name}/map.json'],cwd=ROOT))
            original=next(r for r in node['layouts'] if r['id']==old_event['layout'])
        else:original=next(r for r in node['layouts'] if r['id']==event['layout'])
        new_id=layout_id(name);assert event['layout'] in (original['id'],new_id)
        w,h=original['width'],original['height'];old=words(ROOT/original['blockdata_filepath']);assert len(old)==w*h
        occupied={(int(e['x']),int(e['y'])) for group in ('warp_events','object_events','coord_events','bg_events') for e in event[group]}
        new=list(old);counts=[0,0]
        level=int(name.split('_')[1][0])
        for y in range(2,h-2):
            for x in range(2,w-2):
                i=y*w+x;tile=old[i]&1023
                if (x,y) in occupied or any(abs(x-a)+abs(y-b)<2 for a,b in occupied):continue
                salt=(x*19+y*23+x*y*3+len(name))%83
                kind=0 if tile==625 and salt in ((2,41) if level>=3 else (2,)) else (
                     1 if tile==776 and salt in ((7,35,63) if level>=3 else (7,)) else None)
                if kind is not None:
                    new[i]=(old[i]&~1023)|(BASE+kind);counts[kind]+=1
        folder=ROOT/'data/layouts'/('AraunaEsconderijo_'+name.split('_',1)[1]);folder.mkdir(exist_ok=True)
        (folder/'map.bin').write_bytes(struct.pack('<%dH'%len(new),*new))
        shutil.copyfile(ROOT/original['border_filepath'],folder/'border.bin')
        record=dict(original,id=new_id,name='AraunaEsconderijo_'+name.split('_',1)[1]+'_Layout',
                    secondary_tileset='gTileset_AraunaEsconderijoSerra',
                    blockdata_filepath=str((folder/'map.bin').relative_to(ROOT)),
                    border_filepath=str((folder/'border.bin').relative_to(ROOT)))
        current=next((r for r in node['layouts'] if r['id']==new_id),None)
        if current:current.update(record)
        else:node['layouts'].append(record)
        event['layout']=new_id;dump(map_path,event)
        report[name]={'size':[w,h],'depth':level,'ducts_and_cables':counts,'warps':len(event['warp_events'])}
    dump(path,node);print(json.dumps(report,indent=2))

if __name__=='__main__':main()
