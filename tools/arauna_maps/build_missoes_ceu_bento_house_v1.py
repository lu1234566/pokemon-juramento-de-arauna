#!/usr/bin/env python3
"""Adapt Bento's fixed-script home with the native Missões do Céu art bank."""
import json, shutil, struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAME = 'MossdeepCity_StevensHouse'
ID = 'LAYOUT_ARAUNA_MISSOES_CEU_BENTO_HOUSE'
SYMBOL = 'AraunaMissoesCeuBentoHouseV1'
MARK = 'MISSOES_CEU_BENTO_HOUSE_V1'
SOURCE = ROOT/'data/tilesets/secondary/arauna_missoes_ceu_interiors_v1'
BANK = ROOT/'data/tilesets/secondary/arauna_missoes_ceu_bento_house_v1'

def words(path):
    raw=path.read_bytes()
    return list(struct.unpack('<%dH'%(len(raw)//2),raw))

def pack(values):
    return struct.pack('<%dH'%len(values),*values)

def dump(path, value):
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def main():
    assert SOURCE.is_dir(), 'Instale os interiores V1 primeiro'
    if BANK.exists(): shutil.rmtree(BANK)
    shutil.copytree(SOURCE,BANK)
    source_meta=words(SOURCE/'metatiles.bin')
    source_attrs=words(SOURCE/'metatile_attributes.bin')
    # The unchanged story command sets tile 0x2f1 at (6,4). Give that slot
    # a coastal table-edge graphic and the original table-edge attributes.
    edge=0x2f1-0x200
    while len(source_attrs)<=edge:
        source_attrs.append(source_attrs[0])
        source_meta.extend(source_meta[8:16])
    source_meta[edge*8:edge*8+8]=source_meta[(0x22e-0x200)*8:(0x22e-0x200)*8+8]
    source_attrs[edge]=0x1000
    (BANK/'metatiles.bin').write_bytes(pack(source_meta))
    (BANK/'metatile_attributes.bin').write_bytes(pack(source_attrs))

    old=words(ROOT/'data/layouts'/NAME/'map.bin')
    house=words(ROOT/'data/layouts/MossdeepCity_House1_Arauna/map.bin')
    assert len(old)==11*8 and len(house)==12*11
    def h(x,y): return house[y*12+x]&0x3ff
    grid=[]
    for y in range(8):
        for x in range(11):
            if y<2: mid=h(x,y)
            elif x==0: mid=h(0,3)
            elif x==10: mid=h(11,3)
            else: mid=h(2+(x+y)%2,6)
            grid.append((old[y*11+x]&~0x3ff)|mid)
    def put(x,y,mid):
        i=y*11+x;grid[i]=(grid[i]&~0x3ff)|mid
    # Existing blocked 4x2 table remains at its exact coordinates. The gift
    # and hidden letter retain their original object positions.
    for dy in range(2):
        for dx in range(4): put(4+dx,3+dy,h(2+min(dx,2),3+dy))
    put(6,4,h(4,4))  # post-game letter surface before the script hides it
    for x in (3,4): put(x,7,0x266)  # two existing exit cells
    # Display cases occupy only cells already blocked in the original room.
    put(10,4,h(10,3));put(10,6,h(10,3))
    assert all((a&~0x3ff)==(b&~0x3ff) for a,b in zip(old,grid))
    assert all(0<=v&0x3ff<0x200+len(source_attrs) for v in grid)
    dest=ROOT/'data/layouts/MossdeepCity_StevensHouse_Arauna';dest.mkdir(exist_ok=True)
    (dest/'map.bin').write_bytes(pack(grid))
    shutil.copy2(ROOT/'data/layouts'/NAME/'border.bin',dest/'border.bin')
    layouts=ROOT/'data/layouts/layouts.json';data=json.loads(layouts.read_text())
    template=next(r for r in data['layouts'] if r['id']=='LAYOUT_MOSSDEEP_CITY_STEVENS_HOUSE')
    record=dict(template,id=ID,name='MossdeepCity_BentoHouse_Arauna_Layout',
                secondary_tileset='gTileset_'+SYMBOL,
                border_filepath='data/layouts/MossdeepCity_StevensHouse_Arauna/border.bin',
                blockdata_filepath='data/layouts/MossdeepCity_StevensHouse_Arauna/map.bin')
    existing=next((r for r in data['layouts'] if r['id']==ID),None)
    if existing: existing.update(record)
    else: data['layouts'].append(record)
    dump(layouts,data)
    p=ROOT/'data/maps'/NAME/'map.json';event=json.loads(p.read_text())
    assert event['layout'] in (template['id'],ID)
    event['layout']=ID;dump(p,event)
    base='data/tilesets/secondary/arauna_missoes_ceu_bento_house_v1'
    bodies={
      'graphics.h':f'const u32 gTilesetTiles_{SYMBOL}[] = INCGFX_U32("{base}/tiles.png", ".4bpp.lz");\n'
         +f'const u16 gTilesetPalettes_{SYMBOL}[][16] =\n{{\n'
         +''.join(f'    INCGFX_U16("{base}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n',
      'metatiles.h':f'const u16 gMetatiles_{SYMBOL}[] = INCBIN_U16("{base}/metatiles.bin");\n'
         +f'const u16 gMetatileAttributes_{SYMBOL}[] = INCBIN_U16("{base}/metatile_attributes.bin");\n',
      'headers.h':f'const struct Tileset gTileset_{SYMBOL} =\n{{\n'
         +f'    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n    .tiles = gTilesetTiles_{SYMBOL},\n'
         +f'    .palettes = gTilesetPalettes_{SYMBOL},\n    .metatiles = gMetatiles_{SYMBOL},\n'
         +f'    .metatileAttributes = gMetatileAttributes_{SYMBOL},\n    .callback = NULL,\n}};\n'}
    import re
    for file,body in bodies.items():
        p=ROOT/'src/data/tilesets'/file
        clean=re.sub(r'\n*// '+MARK+r'_BEGIN\n.*?// '+MARK+r'_END\n','',p.read_text(),flags=re.S)
        p.write_text(clean.rstrip()+'\n\n// '+MARK+'_BEGIN\n'+body+'// '+MARK+'_END\n')
    print(json.dumps({'map':NAME,'metatiles':len(source_attrs),'script_tile':hex(0x2f1),'collision_preserved':True}))

if __name__=='__main__':main()
