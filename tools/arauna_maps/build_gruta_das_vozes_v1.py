#!/usr/bin/env python3
"""Give Granite Cave four native GBA depth palettes and ancient landmarks."""
import json
import shutil
import struct
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'data/tilesets/secondary/cave'
NAMES = ('GraniteCave_1F', 'GraniteCave_B1F', 'GraniteCave_B2F', 'GraniteCave_StevensRoom')
SUFFIX = ('Entrada', 'Paredes', 'Profundezas', 'Memoria')
SIZE = ((42, 15), (32, 26), (32, 26), (15, 14))
TINT = ((102, 116, 137), (76, 93, 117), (53, 71, 98), (65, 84, 113))
LIGHT = ((205, 213, 223), (178, 192, 211), (145, 166, 196), (185, 206, 224))
OLD = ('LAYOUT_GRANITE_CAVE_1F', 'LAYOUT_GRANITE_CAVE_B1F',
       'LAYOUT_GRANITE_CAVE_B2F', 'LAYOUT_GRANITE_CAVE_STEVENS_ROOM')
NEW = tuple('LAYOUT_ARAUNA_GRUTA_VOZES_' + s.upper() + '_V1' for s in SUFFIX)
BASE = 512 + 414  # Cave has 414 secondary metatiles.


def words(path):
    raw = path.read_bytes()
    return list(struct.unpack('<%dH' % (len(raw) // 2), raw))


def write_words(path, entries):
    path.write_bytes(struct.pack('<%dH' % len(entries), *entries))


def insert(path, anchor, block, marker):
    source = path.read_text()
    if marker not in source:
        assert source.count(anchor) == 1, (path, anchor)
        path.write_text(source.replace(anchor, block + anchor))


def tint_palette(path, dark, bright):
    lines = path.read_text().splitlines()
    assert lines[:3] == ['JASC-PAL', '0100', '16'] and len(lines) == 19
    # Keep hue and contrast fixed across all four levels; lower levels lose light.
    stops = (dark, bright, tuple(round((2*a+b)/3) for a,b in zip(bright,dark)),
             tuple(round((a+b)/2) for a,b in zip(bright,dark)),
             tuple(round((a+2*b)/3) for a,b in zip(bright,dark)),
             tuple(round((a+3*b)/4) for a,b in zip(bright,dark)),
             tuple(round(a*.63) for a in dark), tuple(round(a*.43) for a in dark))
    for i, rgb in enumerate(stops):
        lines[3+i] = ' '.join(map(str, rgb))
    # Cave sprites use 8..11 for small reflections, now cold instead of red.
    for i, rgb in enumerate(((233,240,247),(164,206,240),(92,160,217),(39,105,169)), 8):
        lines[3+i] = ' '.join(map(str, rgb))
    path.write_text('\n'.join(lines) + '\n')


def art():
    result=[]
    for kind in range(4):
        im=Image.new('P',(16,16),0)
        d=ImageDraw.Draw(im)
        if kind == 0:  # a weathered ring of runes, barely lit
            d.arc((2,2,13,13),15,295,fill=3,width=1)
            d.line((4,10,7,5,9,8,12,4),fill=4,width=1)
            for xy in ((2,7),(12,12),(8,2)):d.point(xy,fill=2)
        elif kind == 1:  # narrow, eroded blue markings on the old walls
            d.line((3,2,6,4,5,8,9,9,12,13),fill=4,width=1)
            d.line((10,1,8,5,11,7),fill=3,width=1)
            d.point((4,3),fill=6);d.point((9,9),fill=5)
        elif kind == 2:  # a small blue mineral pool, deliberately walkable
            d.polygon(((3,8),(5,5),(9,4),(13,7),(12,11),(8,13),(4,11)),fill=4)
            d.line((4,8,7,6,11,7),fill=2,width=1)
            d.line((6,10,9,11,12,9),fill=5,width=1)
            for xy in ((1,6),(13,4),(3,12)):d.point(xy,fill=3)
        else:  # the memory chamber's quiet circular focus
            d.ellipse((1,1,14,14),outline=4,width=1)
            d.arc((4,4,11,11),40,310,fill=3,width=1)
            d.line((8,3,8,6),fill=5,width=1)
            d.point((8,8),fill=2)
        result.append(im)
    return result


def clone_and_draw(target, dark, bright):
    target.mkdir(parents=True,exist_ok=True)
    for name in ('tiles.png','metatiles.bin','metatile_attributes.bin'):
        shutil.copyfile(SOURCE/name,target/name)
    (target/'palettes').mkdir(exist_ok=True)
    for i in range(16):shutil.copyfile(SOURCE/'palettes'/f'{i:02}.pal',target/'palettes'/f'{i:02}.pal')
    for i in (6,9,10):tint_palette(target/'palettes'/f'{i:02}.pal',dark,bright)
    cold=("0 0 0", "210 228 240", "142 194 226", "88 156 210",
          "38 120 190", "23 91 166", "16 67 133", "11 48 106")
    pal=target/'palettes/11.pal';lines=pal.read_text().splitlines()
    for i,rgb in enumerate(cold):lines[i+3]=rgb
    pal.write_text('\n'.join(lines)+'\n')
    raw=Image.open(target/'tiles.png')
    assert raw.mode == 'P' and raw.size == (128,216)
    expanded=Image.new('P',(128,256),0);expanded.putpalette(raw.getpalette());expanded.paste(raw,(0,0))
    original=words(target/'metatiles.bin')
    assert len(original)==414*8
    used={entry&1023 for entry in original}
    assert not used.intersection(range(0x3e0,0x3f0))
    for kind, im in enumerate(art()):
        for quadrant,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):
            index=0x3e0+kind*4+quadrant
            expanded.paste(im.crop((x,y,x+8,y+8)),((index-512)%16*8,(index-512)//16*8))
    basin=Image.new('P',(32,32),0);d=ImageDraw.Draw(basin)
    d.polygon(((2,13),(5,7),(13,5),(17,2),(26,5),(29,12),(26,17),(30,21),
               (25,28),(16,27),(9,30),(3,24)),fill=4)
    d.polygon(((5,14),(10,8),(18,7),(25,10),(23,17),(27,22),(20,25),(11,24),(6,20)),fill=5)
    d.line((7,13,14,10,19,11,24,13),fill=2,width=1)
    d.line((9,21,16,19,22,21),fill=3,width=1)
    for x,y in ((3,9),(4,26),(13,3),(27,7),(29,25),(18,28)):
        d.point((x,y),fill=2)
    for part in range(4):
        bx,by=(part%2)*16,(part//2)*16
        for quadrant,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):
            index=0x3f0+part*4+quadrant
            expanded.paste(basin.crop((bx+x,by+y,bx+x+8,by+y+8)),
                           ((index-512)%16*8,(index-512)//16*8))
    expanded.save(target/'tiles.png')
    attrs=words(target/'metatile_attributes.bin')
    for kind, src in enumerate((529,513,529,513)):
        start=(src-512)*8
        original.extend(original[start:start+4]+[(0x3e0+kind*4+i)|(11<<12) for i in range(4)])
        attrs.append(attrs[src-512])
    for part in range(4):
        start=(529-512)*8
        original.extend(original[start:start+4]+[(0x3f0+part*4+i)|(11<<12) for i in range(4)])
        attrs.append(attrs[529-512])
    write_words(target/'metatiles.bin',original)
    write_words(target/'metatile_attributes.bin',attrs)


def register():
    refs=[]; metas=[]; headers=[]
    for suffix in SUFFIX:
        slug='arauna_gruta_vozes_'+suffix.lower()
        name='AraunaGrutaVozes'+suffix
        refs.append(f'const u32 gTilesetTiles_{name}[] = INCGFX_U32("data/tilesets/secondary/{slug}/tiles.png", ".4bpp.lz");\n'
                    f'const u16 gTilesetPalettes_{name}[][16] =\n{{\n'+
                    '\n'.join(f'    INCGFX_U16("data/tilesets/secondary/{slug}/palettes/{i:02}.pal", ".gbapal"),' for i in range(16))+'\n};\n')
        metas.append(f'const u16 gMetatiles_{name}[] = INCBIN_U16("data/tilesets/secondary/{slug}/metatiles.bin");\n'
                     f'const u16 gMetatileAttributes_{name}[] = INCBIN_U16("data/tilesets/secondary/{slug}/metatile_attributes.bin");\n')
        headers.append(f'const struct Tileset gTileset_{name} =\n{{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n'
                       f'    .tiles = gTilesetTiles_{name},\n    .palettes = gTilesetPalettes_{name},\n'
                       f'    .metatiles = gMetatiles_{name},\n    .metatileAttributes = gMetatileAttributes_{name},\n'
                       '    .callback = NULL,\n};\n')
    blocks=(('src/data/tilesets/graphics.h','const u32 gTilesetTiles_AraunaAmanhecer[]','\n'.join(refs),'const u32 gTilesetTiles_AraunaGrutaVozesEntrada[]'),
            ('src/data/tilesets/metatiles.h','const u16 gMetatiles_AraunaAmanhecer[]','\n'.join(metas),'const u16 gMetatiles_AraunaGrutaVozesEntrada[]'),
            ('src/data/tilesets/headers.h','const struct Tileset gTileset_AraunaAmanhecer =','\n'.join(headers),'const struct Tileset gTileset_AraunaGrutaVozesEntrada ='))
    for path,anchor,block,marker in blocks:insert(ROOT/path,anchor,block+'\n',marker)


def decorate(original,w,h,events,level):
    modified=list(original)
    occupied={(int(item['x']),int(item['y']))
              for group in ('warp_events','object_events','coord_events','bg_events')
              for item in events[group]}
    counts=[0,0,0,0]
    # Sparse land­marks, away from the structural edge and game events.
    for y in range(2,h-2):
        for x in range(2,w-2):
            i=y*w+x; tile=original[i]&1023
            if (x,y) in occupied or any(abs(x-a)+abs(y-b)<=2 for a,b in occupied):continue
            kind=None
            if tile==513 and (x*7+y*11+level*17)%43==0:kind=1
            elif tile==529:
                salt=(x*17+y*23+x*y*3+level*13)%67
                if salt==0:kind=2
                elif salt in (9,31):kind=0
            if level==3 and (x,y)==(7,10) and tile==513:kind=3
            if kind is not None:
                modified[i]=(original[i]&~1023)|(BASE+kind)
                counts[kind]+=1
    if level==3 and counts[3]==0:
        for x,y in ((7,10),(7,9),(6,9)):
            i=y*w+x
            if original[i]&1023==513 and (x,y) not in occupied:
                modified[i]=(original[i]&~1023)|(BASE+3);counts[3]+=1;break
    if level<3:
        px,py=((25,3),(13,5),(20,3))[level]
        for part in range(4):
            x,y=px+part%2,py+part//2;i=y*w+x
            assert original[i]&1023==529 and (x,y) not in occupied
            oldkind=(modified[i]&1023)-BASE
            if modified[i]!=original[i] and 0<=oldkind<4:counts[oldkind]-=1
            modified[i]=(original[i]&~1023)|(BASE+4+part)
        counts.append(4)
    else:counts.append(0)
    return modified,counts


def main():
    layouts_path=ROOT/'data/layouts/layouts.json'
    all_layouts=json.loads(layouts_path.read_text())
    summary={}
    for level,(mapname,suffix,(w,h),dark,bright,old_id,new_id) in enumerate(zip(NAMES,SUFFIX,SIZE,TINT,LIGHT,OLD,NEW)):
        target=ROOT/'data/tilesets/secondary'/('arauna_gruta_vozes_'+suffix.lower())
        clone_and_draw(target,dark,bright)
        baseline=next(r for r in all_layouts['layouts'] if r['id']==old_id)
        assert (baseline['width'],baseline['height'])==(w,h)
        source=words(ROOT/baseline['blockdata_filepath'])
        map_path=ROOT/'data/maps'/mapname/'map.json'
        event=json.loads(map_path.read_text())
        assert event['layout'] in (old_id,new_id)
        result,counts=decorate(source,w,h,event,level)
        layout_folder=ROOT/'data/layouts'/('AraunaGrutaVozes_'+suffix)
        layout_folder.mkdir(exist_ok=True)
        write_words(layout_folder/'map.bin',result)
        shutil.copyfile(ROOT/baseline['border_filepath'],layout_folder/'border.bin')
        record=dict(baseline,id=new_id,name='AraunaGrutaVozes_'+suffix+'_Layout',
                    secondary_tileset='gTileset_AraunaGrutaVozes'+suffix,
                    blockdata_filepath=str((layout_folder/'map.bin').relative_to(ROOT)),
                    border_filepath=str((layout_folder/'border.bin').relative_to(ROOT)))
        found=next((r for r in all_layouts['layouts'] if r['id']==new_id),None)
        if found:found.update(record)
        else:all_layouts['layouts'].append(record)
        event['layout']=new_id
        map_path.write_text(json.dumps(event,indent=2,ensure_ascii=False)+'\n')
        summary[mapname]={'size':[w,h],'runes_wall_pool_altar':counts,'warps':len(event['warp_events'])}
    layouts_path.write_text(json.dumps(all_layouts,indent=2,ensure_ascii=False)+'\n')
    register()
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
