#!/usr/bin/env python3
"""Galerias Serra abandoned mine at Rusturf Tunnel."""
import json,shutil,struct
from pathlib import Path
from PIL import Image,ImageDraw
def words(p):
    b=p.read_bytes();return list(struct.unpack('<%dH'%(len(b)//2),b))
def dump(p,node):p.write_text(json.dumps(node,indent=2,ensure_ascii=False)+'\n')
def insert(path,anchor,content,marker):
    s=path.read_text()
    if marker not in s:
        assert s.count(anchor)==1,(path,anchor)
        path.write_text(s.replace(anchor,content+anchor))
def palette(path,changes):
    s=path.read_text().splitlines();assert s[:3]==['JASC-PAL','0100','16'] and len(s)==19
    for i,rgb in changes.items():s[i+3]=' '.join(map(str,rgb))
    path.write_text('\n'.join(s)+'\n')
def clone(src,dst):
    dst.mkdir(parents=True,exist_ok=True)
    for n in ('tiles.png','metatiles.bin','metatile_attributes.bin'):shutil.copyfile(src/n,dst/n)
    (dst/'palettes').mkdir(exist_ok=True)
    for i in range(16):shutil.copyfile(src/'palettes'/f'{i:02}.pal',dst/'palettes'/f'{i:02}.pal')

ROOT=Path(__file__).resolve().parents[2]
ID='LAYOUT_ARAUNA_GALERIAS_SERRA_V1';W,H=36,24
PRIMARY=ROOT/'data/tilesets/primary/arauna_rocha_mina'
SECONDARY=ROOT/'data/tilesets/secondary/arauna_galerias_serra'

def register():
    p=ROOT/'src/graphics.c';refs='\n'.join(f'    INCGFX_U16("data/tilesets/primary/arauna_rocha_mina/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
    insert(p,'// trade/egg hatch','const u16 gTilesetPalettes_AraunaRochaMina[][16] =\n{\n'+refs+'\n};\nconst u32 gTilesetTiles_AraunaRochaMina[] = INCGFX_U32("data/tilesets/primary/arauna_rocha_mina/tiles.png", ".4bpp.lz");\n\n','const u32 gTilesetTiles_AraunaRochaMina[]')
    p=ROOT/'src/data/tilesets/metatiles.h'
    insert(p,'const u16 gMetatiles_Petalburg[]','const u16 gMetatiles_AraunaRochaMina[] = INCBIN_U16("data/tilesets/primary/arauna_rocha_mina/metatiles.bin");\nconst u16 gMetatileAttributes_AraunaRochaMina[] = INCBIN_U16("data/tilesets/primary/arauna_rocha_mina/metatile_attributes.bin");\n\n','const u16 gMetatiles_AraunaRochaMina[]')
    p=ROOT/'src/data/tilesets/headers.h'
    insert(p,'const struct Tileset gTileset_Petalburg =','const struct Tileset gTileset_AraunaRochaMina =\n{\n    .isCompressed = TRUE,\n    .isSecondary = FALSE,\n    .tiles = gTilesetTiles_AraunaRochaMina,\n    .palettes = gTilesetPalettes_AraunaRochaMina,\n    .metatiles = gMetatiles_AraunaRochaMina,\n    .metatileAttributes = gMetatileAttributes_AraunaRochaMina,\n    .callback = InitTilesetAnim_General,\n};\n\n','const struct Tileset gTileset_AraunaRochaMina =')
    p=ROOT/'src/data/tilesets/graphics.h';refs='\n'.join(f'    INCGFX_U16("data/tilesets/secondary/arauna_galerias_serra/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))
    insert(p,'const u32 gTilesetTiles_AraunaAmanhecer[]','const u32 gTilesetTiles_AraunaGaleriasSerra[] = INCGFX_U32("data/tilesets/secondary/arauna_galerias_serra/tiles.png", ".4bpp.lz");\nconst u16 gTilesetPalettes_AraunaGaleriasSerra[][16] =\n{\n'+refs+'\n};\n\n','const u32 gTilesetTiles_AraunaGaleriasSerra[]')
    p=ROOT/'src/data/tilesets/metatiles.h'
    insert(p,'const u16 gMetatiles_AraunaAmanhecer[]','const u16 gMetatiles_AraunaGaleriasSerra[] = INCBIN_U16("data/tilesets/secondary/arauna_galerias_serra/metatiles.bin");\nconst u16 gMetatileAttributes_AraunaGaleriasSerra[] = INCBIN_U16("data/tilesets/secondary/arauna_galerias_serra/metatile_attributes.bin");\n\n','const u16 gMetatiles_AraunaGaleriasSerra[]')
    p=ROOT/'src/data/tilesets/headers.h'
    insert(p,'const struct Tileset gTileset_AraunaAmanhecer =','const struct Tileset gTileset_AraunaGaleriasSerra =\n{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n    .tiles = gTilesetTiles_AraunaGaleriasSerra,\n    .palettes = gTilesetPalettes_AraunaGaleriasSerra,\n    .metatiles = gMetatiles_AraunaGaleriasSerra,\n    .metatileAttributes = gMetatileAttributes_AraunaGaleriasSerra,\n    .callback = NULL,\n};\n\n','const struct Tileset gTileset_AraunaGaleriasSerra =')

def main():
    clone(ROOT/'data/tilesets/primary/general',PRIMARY)
    clone(ROOT/'data/tilesets/secondary/rusturf_tunnel',SECONDARY)
    palette(SECONDARY/'palettes/06.pal',{0:(88,62,48),1:(222,191,143),2:(192,158,111),3:(165,132,91),4:(136,104,72),5:(107,79,55),6:(83,58,44),7:(61,43,34),8:(214,198,166),9:(183,162,131),10:(153,133,107),11:(123,104,83),12:(95,78,64),13:(74,61,52),14:(53,43,39),15:(34,28,30)})
    palette(SECONDARY/'palettes/09.pal',{1:(221,180,124),2:(179,126,78),3:(133,83,52),4:(94,57,40),5:(57,39,34),6:(183,170,138),7:(121,126,116)})
    source_image=Image.open(SECONDARY/'tiles.png');assert source_image.mode=='P' and source_image.size==(128,72)
    raw=Image.new('P',(128,256),0);raw.putpalette(source_image.getpalette());raw.paste(source_image,(0,0))
    used={v&1023 for v in words(SECONDARY/'metatiles.bin')};assert all(i not in used for i in range(0x3f8,0x400))
    beam=Image.new('P',(16,16),0);d=ImageDraw.Draw(beam)
    d.rectangle((1,1,14,3),fill=3,outline=2,width=1)
    d.rectangle((2,4,4,15),fill=4,outline=2,width=1)
    d.rectangle((11,4,13,15),fill=4,outline=2,width=1)
    d.line((5,4,9,8),fill=3,width=1);d.line((10,4,6,8),fill=3,width=1)
    rails=Image.new('P',(16,16),0);d=ImageDraw.Draw(rails)
    for y in (2,7,12):d.rectangle((2,y,13,y+1),fill=3)
    d.line((5,0,5,15),fill=6,width=1);d.line((11,0,11,15),fill=6,width=1)
    for art,start in ((beam,0x3f8),(rails,0x3fc)):
        for i,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):
            idx=start+i;raw.paste(art.crop((x,y,x+8,y+8)),((idx-512)%16*8,(idx-512)//16*8))
    raw.save(SECONDARY/'tiles.png')
    meta=words(SECONDARY/'metatiles.bin');attrs=words(SECONDARY/'metatile_attributes.bin')
    assert len(attrs)==83
    mid=512+len(attrs)
    for src,start in ((0x211,0x3f8),(0x219,0x3fc),(0x201,0x3fc)):
        meta.extend(meta[(src-512)*8:(src-512)*8+4]+[(start+i)|(9<<12) for i in range(4)])
        attrs.append(attrs[src-512])
    (SECONDARY/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(meta),*meta))
    (SECONDARY/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(attrs),*attrs))
    register()
    old=words(ROOT/'data/layouts/RusturfTunnel/map.bin');assert len(old)==W*H
    new=list(old)
    event=json.loads((ROOT/'data/maps/RusturfTunnel/map.json').read_text())
    occupied={(v['x'],v['y']) for key in ('warp_events','object_events','coord_events','bg_events') for v in event[key]}
    beams=[];rails_cells=[]
    for y in range(2,H-2):
        for x in range(3,W-3):
            i=y*W+x;tile=old[i]&1023
            if (x,y) in occupied:continue
            if tile==0x211 and x in (8,14,20,26) and y in (7,8,13,18):
                new[i]=(old[i]&~1023)|mid;beams.append((x,y))
            elif tile==0x219 and y==3 and 9<=x<=26:
                new[i]=(old[i]&~1023)|(mid+1);rails_cells.append((x,y))
    for x in range(4,8):
        y=9;i=y*W+x
        assert old[i]&1023==0x201 and (x,y) not in occupied
        new[i]=(old[i]&~1023)|(mid+2);rails_cells.append((x,y))
    assert 4<=len(beams)<=25 and 16<=len(rails_cells)<=30,(len(beams),len(rails_cells))
    assert all((a^b)&~1023==0 for a,b in zip(old,new))
    path=ROOT/'data/layouts/layouts.json';node=json.loads(path.read_text());base=next(v for v in node['layouts'] if v['id']=='LAYOUT_RUSTURF_TUNNEL')
    record=dict(base,id=ID,name='RusturfTunnel_AraunaGaleriasSerra_Layout',primary_tileset='gTileset_AraunaRochaMina',secondary_tileset='gTileset_AraunaGaleriasSerra',blockdata_filepath='data/layouts/RusturfTunnel_AraunaGaleriasSerra/map.bin',border_filepath='data/layouts/RusturfTunnel_AraunaGaleriasSerra/border.bin')
    found=next((v for v in node['layouts'] if v['id']==ID),None)
    if found:found.update(record)
    else:node['layouts'].append(record)
    dump(path,node)
    assert event['layout'] in ('LAYOUT_RUSTURF_TUNNEL',ID);event['layout']=ID;dump(ROOT/'data/maps/RusturfTunnel/map.json',event)
    target=ROOT/'data/layouts/RusturfTunnel_AraunaGaleriasSerra';target.mkdir(exist_ok=True)
    (target/'map.bin').write_bytes(struct.pack('<%dH'%len(new),*new))
    shutil.copyfile(ROOT/base['border_filepath'],target/'border.bin')
    print(json.dumps({'size':[W,H],'wooden_supports':len(beams),'rail_segments':len(rails_cells),'warps':len(event['warp_events'])}))
if __name__=='__main__':main()
