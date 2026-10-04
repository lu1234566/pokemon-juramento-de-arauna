#!/usr/bin/env python3
"""Adapt Fiery Path as a dark volcanic tube with hot pockets."""
import json,shutil,struct
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'data/tilesets/secondary/lavaridge'
TARGET=ROOT/'data/tilesets/secondary/arauna_trilha_brasa'
ID='LAYOUT_ARAUNA_TRILHA_BRASA_V1'
W,H=35,38
BASE=512+441

def words(path):
    raw=path.read_bytes();return list(struct.unpack('<%dH'%(len(raw)//2),raw))
def dump(path,node):path.write_text(json.dumps(node,indent=2,ensure_ascii=False)+'\n')
def palette(path,changes):
    lines=path.read_text().splitlines()
    assert lines[:3]==['JASC-PAL','0100','16'] and len(lines)==19
    for i,rgb in changes.items():lines[i+3]=' '.join(map(str,rgb))
    path.write_text('\n'.join(lines)+'\n')
def insert(path,anchor,block,marker):
    s=path.read_text()
    if marker not in s:
        assert s.count(anchor)==1
        path.write_text(s.replace(anchor,block+anchor))

def assets():
    TARGET.mkdir(parents=True,exist_ok=True)
    for name in ('tiles.png','metatiles.bin','metatile_attributes.bin'):
        shutil.copyfile(SOURCE/name,TARGET/name)
    (TARGET/'palettes').mkdir(exist_ok=True)
    for i in range(16):shutil.copyfile(SOURCE/'palettes'/f'{i:02}.pal',TARGET/'palettes'/f'{i:02}.pal')
    palette(TARGET/'palettes/10.pal',{
        0:(45,51,59),1:(145,154,155),2:(117,127,134),3:(91,105,116),
        4:(67,84,100),5:(45,63,83),8:(32,40,55),
        9:(132,128,120),10:(107,105,105),11:(83,86,93),
        12:(63,70,83),13:(43,52,69),14:(26,37,55)})
    palette(TARGET/'palettes/11.pal',{
        0:(45,51,59),1:(225,211,181),2:(205,191,165),3:(183,171,151),
        4:(155,151,141),6:(122,126,127),8:(87,91,97),
        9:(240,219,178),10:(216,194,154),11:(188,162,128),
        12:(153,127,107),13:(119,97,86),14:(83,70,70),15:(70,68,63)})
    # Embers retain orange and yellow, but their surrounding rock loses red.
    palette(TARGET/'palettes/06.pal',{
        1:(48,61,78),7:(137,81,63),8:(109,59,55),9:(219,77,24),
        10:(175,58,27),11:(245,104,25),12:(246,164,51)})
    source=Image.open(TARGET/'tiles.png');assert source.mode=='P' and source.size==(128,232)
    raw=Image.new('P',(128,256),0);raw.putpalette(source.getpalette());raw.paste(source,(0,0))
    meta=words(TARGET/'metatiles.bin');attrs=words(TARGET/'metatile_attributes.bin')
    assert len(attrs)==441 and not {v&1023 for v in meta}.intersection(range(0x3e0,0x400))
    artworks=[]
    ember=Image.new('P',(16,16),0);d=ImageDraw.Draw(ember)
    d.line((1,10,4,8,7,10,9,6,13,4),fill=10,width=2)
    d.line((4,8,7,10,9,6),fill=11,width=1)
    for x,y in ((3,4),(12,11),(10,12)):d.point((x,y),fill=12)
    artworks.append(ember)
    vent=Image.new('P',(16,16),0);d=ImageDraw.Draw(vent)
    d.ellipse((2,7,13,13),fill=10,outline=8,width=1)
    d.arc((4,2,8,9),190,345,fill=3,width=1)
    d.arc((9,1,13,8),195,345,fill=4,width=1)
    d.point((7,10),fill=12);d.point((10,11),fill=11)
    artworks.append(vent)
    for kind,art in enumerate(artworks):
        start=0x3f8+kind*4
        for i,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):
            index=start+i
            raw.paste(art.crop((x,y,x+8,y+8)),((index-512)%16*8,(index-512)//16*8))
        src=(625,776)[kind]
        meta.extend(meta[(src-512)*8:(src-512)*8+4]+[(start+i)|(6<<12) for i in range(4)])
        attrs.append(attrs[src-512])
    magma=Image.new('P',(32,32),0);d=ImageDraw.Draw(magma)
    d.polygon(((2,12),(5,5),(13,4),(17,2),(26,6),(29,13),
               (26,18),(30,24),(23,29),(14,27),(7,30),(2,23)),fill=8)
    d.polygon(((5,12),(9,7),(18,6),(25,11),(23,18),(27,23),
               (18,25),(10,23),(5,20)),fill=10)
    d.polygon(((9,11),(17,8),(24,13),(20,18),(24,21),(16,23),(8,18)),fill=11)
    d.line((8,15,14,12,20,15,23,13),fill=12,width=2)
    d.line((10,21,15,19,20,21),fill=9,width=1)
    for part in range(4):
        bx,by=(part%2)*16,(part//2)*16
        for i,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):
            index=0x3e0+part*4+i
            raw.paste(magma.crop((bx+x,by+y,bx+x+8,by+y+8)),
                      ((index-512)%16*8,(index-512)//16*8))
        src=625
        meta.extend(meta[(src-512)*8:(src-512)*8+4]+[(0x3e0+part*4+i)|(6<<12) for i in range(4)])
        attrs.append(attrs[src-512])
    raw.save(TARGET/'tiles.png')
    (TARGET/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(meta),*meta))
    (TARGET/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(attrs),*attrs))

def register():
    refs='\n'.join(f'    INCGFX_U16("data/tilesets/secondary/arauna_trilha_brasa/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
    insert(ROOT/'src/data/tilesets/graphics.h','const u32 gTilesetTiles_AraunaAmanhecer[]',
           'const u32 gTilesetTiles_AraunaTrilhaBrasa[] = INCGFX_U32("data/tilesets/secondary/arauna_trilha_brasa/tiles.png", ".4bpp.lz");\n'
           'const u16 gTilesetPalettes_AraunaTrilhaBrasa[][16] =\n{\n'+refs+'\n};\n\n',
           'const u32 gTilesetTiles_AraunaTrilhaBrasa[]')
    insert(ROOT/'src/data/tilesets/metatiles.h','const u16 gMetatiles_AraunaAmanhecer[]',
           'const u16 gMetatiles_AraunaTrilhaBrasa[] = INCBIN_U16("data/tilesets/secondary/arauna_trilha_brasa/metatiles.bin");\n'
           'const u16 gMetatileAttributes_AraunaTrilhaBrasa[] = INCBIN_U16("data/tilesets/secondary/arauna_trilha_brasa/metatile_attributes.bin");\n\n',
           'const u16 gMetatiles_AraunaTrilhaBrasa[]')
    insert(ROOT/'src/data/tilesets/headers.h','const struct Tileset gTileset_AraunaAmanhecer =',
           'const struct Tileset gTileset_AraunaTrilhaBrasa =\n{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n'
           '    .tiles = gTilesetTiles_AraunaTrilhaBrasa,\n    .palettes = gTilesetPalettes_AraunaTrilhaBrasa,\n'
           '    .metatiles = gMetatiles_AraunaTrilhaBrasa,\n    .metatileAttributes = gMetatileAttributes_AraunaTrilhaBrasa,\n'
           '    .callback = NULL,\n};\n\n',
           'const struct Tileset gTileset_AraunaTrilhaBrasa =')

def main():
    assets();register()
    event_path=ROOT/'data/maps/FieryPath/map.json';event=json.loads(event_path.read_text())
    assert event['layout'] in ('LAYOUT_FIERY_PATH',ID)
    old=words(ROOT/'data/layouts/FieryPath/map.bin');assert len(old)==W*H
    occupied={(int(v['x']),int(v['y'])) for key in ('warp_events','object_events','coord_events','bg_events') for v in event[key]}
    modified=list(old);counts=[0,0]
    for y in range(2,H-2):
        for x in range(2,W-2):
            i=y*W+x;tile=old[i]&1023
            if (x,y) in occupied or any(abs(x-a)+abs(y-b)<2 for a,b in occupied):continue
            salt=(x*17+y*29+x*y*3)%97
            kind=0 if tile==625 and salt in (2,41) else (1 if tile==776 and salt in (17,63) else None)
            if kind is not None:
                modified[i]=(old[i]&~1023)|(BASE+kind);counts[kind]+=1
    assert 5<=counts[0]<=30 and 2<=counts[1]<=20,counts
    for px,py in ((24,11),(13,26)):
        for part in range(4):
            x,y=px+part%2,py+part//2;i=y*W+x
            assert old[i]&1023==625 and (x,y) not in occupied
            if modified[i]!=old[i]:counts[0]-=1
            modified[i]=(old[i]&~1023)|(BASE+2+part)
    layout_folder=ROOT/'data/layouts/FieryPath_AraunaTrilhaBrasa';layout_folder.mkdir(exist_ok=True)
    (layout_folder/'map.bin').write_bytes(struct.pack('<%dH'%len(modified),*modified))
    shutil.copyfile(ROOT/'data/layouts/FieryPath/border.bin',layout_folder/'border.bin')
    path=ROOT/'data/layouts/layouts.json';node=json.loads(path.read_text())
    base=next(v for v in node['layouts'] if v['id']=='LAYOUT_FIERY_PATH')
    record=dict(base,id=ID,name='FieryPath_AraunaTrilhaBrasa_Layout',
                secondary_tileset='gTileset_AraunaTrilhaBrasa',
                blockdata_filepath='data/layouts/FieryPath_AraunaTrilhaBrasa/map.bin',
                border_filepath='data/layouts/FieryPath_AraunaTrilhaBrasa/border.bin')
    found=next((v for v in node['layouts'] if v['id']==ID),None)
    if found:found.update(record)
    else:node['layouts'].append(record)
    dump(path,node);event['layout']=ID;dump(event_path,event)
    print(json.dumps({'size':[W,H],'ember_cracks':counts[0],'hot_vents':counts[1],'magma_pockets':2,
                      'warps':len(event['warp_events']),'objects':len(event['object_events'])}))

if __name__=='__main__':main()
