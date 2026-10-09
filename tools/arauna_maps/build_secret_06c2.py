#!/usr/bin/env python3
"""Private forest banks: preserve shared decoration graphics and every attribute."""
import argparse,json,struct
from pathlib import Path
from PIL import Image
from native_visuals_v2 import dump,binary,marked
from render_native_map import indexed_tiles,words,palette
from secret_06c2_common import BASE,ROOT,OUT,COLORS,NAMES,inventory,parts,require_base

MATERIALS={
 'Tree':{2:(104,160,128),3:(64,120,88),4:(40,80,56),5:(24,48,32),6:(192,152,104),7:(144,104,64),8:(112,72,48),9:(72,48,32)},
 'Shrub':{2:(152,176,104),3:(104,136,72),4:(64,96,48),5:(32,64,32),6:(168,144,96),7:(128,104,72),8:(96,72,48),9:(64,48,32)}}

def forest_floor(theme):
    floor=Image.new('L',(16,16),7)
    if theme=='Tree':
        # Wide worn planks, staggered end joints and a few short wood fibres.
        for x in range(16):
            for y in (0,8):floor.putpixel((x,y),6)
            for y in (7,15):floor.putpixel((x,y),8)
        for y in range(1,7):floor.putpixel((5,y),9)
        for y in range(9,15):floor.putpixel((13,y),9)
        for x in range(1,4):floor.putpixel((x,3),6)
        for x in range(7,10):floor.putpixel((x,11),8)
        for xy in ((11,3),(12,4),(11,5)):floor.putpixel(xy,8)
    else:
        # Packed forest soil, a short embedded root and sparse leaf litter.
        for x,y in ((3,3),(12,4),(4,12),(13,13)):floor.putpixel((x,y),6)
        for x,y in ((6,5),(7,5),(8,6),(9,6),(9,7)):floor.putpixel((x,y),8)
        for x,y in ((1,10),(2,11),(3,11)):floor.putpixel((x,y),9)
    return floor

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,layouts,maps=inventory(base);report={'base_commit':BASE,'banks':{},'maps':{}};decl={k:'' for k in ('graphics.h','metatiles.h','headers.h')}
    for color in COLORS:
        names=[n for n in NAMES if n.startswith('SecretBase_'+color)];layout=layouts[maps[names[0]]['layout']];bank=parts(base,layout['secondary_tileset']);prim=parts(base,layout['primary_tileset'])
        meta=words(bank['metatiles']);assert 12 not in {v>>12 for v in meta+words(prim['metatiles'])},'Material palette is already referenced'
        im,row,count=indexed_tiles(bank['tiles']);count=bank['tile_count'];assert count==83
        tiles={i:im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8)) for i in range(count)}
        # Native ground is also used underneath PCs, doors and decorations.
        # Remap these four subtiles everywhere, so interactive states match.
        native_floor=[v&1023 for v in meta[(0x20a-512)*8:(0x20a-512)*8+4]]
        floor=forest_floor(color)
        floors={gid-512:floor.crop((x,y,x+8,y+8)) for gid,(x,y) in zip(native_floor,((0,0),(8,0),(0,8),(8,8)))}
        referenced=sorted({v&1023 for v in meta if v>>12==6 and v&1023>=512});mapping={};new_tiles=[]
        for gid in referenced:
            local=gid-512;assert local<count
            native=tiles[local];new=floors.get(local,native.copy())
            if local not in floors:
                # Add a small leaf cluster inside the original opaque rock.
                new=native.copy()
                for x,y in ((2,3),(3,3),(4,4),(5,4)):
                    if new.getpixel((x,y)) in (2,3,4):new.putpixel((x,y),2 if y==3 else 4)
            assert bytes(v!=0 for v in native.getdata())==bytes(v!=0 for v in new.getdata()),('opacity',color,gid)
            target=count+len(new_tiles);mapping[gid]=512+target;new_tiles.append(new)
        changed=[]
        for j,e in enumerate(meta):
            if e>>12==6 and e&1023 in mapping:
                meta[j]=(e&0xc00)|mapping[e&1023]|(12<<12);changed.append(j//8+512)
        path=ROOT/f'data/tilesets/secondary/arauna_secret06c2_{color.lower()}';path.mkdir(parents=True,exist_ok=True);(path/'palettes').mkdir(exist_ok=True)
        total=(count+len(new_tiles)+15)//16*16;out=Image.new('P',(128,total//16*8));out.putpalette([c for i in range(256) for c in (i,i,i)])
        for i,tile in [*tiles.items(),*((count+i,tile) for i,tile in enumerate(new_tiles))]:out.paste(tile,(i%16*8,i//16*8))
        out.save(path/'tiles.png',bits=4);binary(path/'metatiles.bin',meta);(path/'metatile_attributes.bin').write_bytes(bank['attributes'].read_bytes())
        for q in range(13):
            raw=bank['palettes'][q].read_bytes()
            if q==12:
                colors=[tuple(c>>3<<3 for c in rgb) for rgb in palette(bank['palettes'][6])];colors[0]=(0,0,0);colors[1]=(24,24,32)
                for index,rgb in MATERIALS[color].items():colors[index]=rgb
                raw=('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in colors)).encode()
            (path/f'palettes/{q:02}.pal').write_bytes(raw)
        symbol='AraunaSecret06C2'+color;rel=path.relative_to(ROOT).as_posix()
        decl['graphics.h']+=f'const u32 gTilesetTiles_{symbol}[] = INCGFX_U32("{rel}/tiles.png", ".4bpp.lz");\nconst u16 gTilesetPalettes_{symbol}[][16] =\n{{\n'+''.join(f'    INCGFX_U16("{rel}/palettes/{q:02}.pal", ".gbapal"),\n' for q in range(13))+'};\n'
        decl['metatiles.h']+=f'const u16 gMetatiles_{symbol}[] = INCBIN_U16("{rel}/metatiles.bin");\nconst u16 gMetatileAttributes_{symbol}[] = INCBIN_U16("{rel}/metatile_attributes.bin");\n'
        decl['headers.h']+=f'const struct Tileset gTileset_{symbol} =\n{{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n    .tiles = gTilesetTiles_{symbol},\n    .palettes = gTilesetPalettes_{symbol},\n    .metatiles = gMetatiles_{symbol},\n    .metatileAttributes = gMetatileAttributes_{symbol},\n    .callback = NULL,\n}};\n'
        report['banks'][color]={'path':rel,'symbol':'gTileset_'+symbol,'source_symbol':layout['secondary_tileset'],'source_tile_count':count,'new_graphic_slots':sorted(mapping.values()),'remapped_native_slots':mapping,'changed_metatile_ids':sorted(set(changed)),'private_palette':12,'static_tile_count':total,'callback':'NULL'}
        for n in names:
            l=layouts[maps[n]['layout']];l['secondary_tileset']='gTileset_'+symbol
            report['maps'][n]={'layout':l['id'],'layout_index':node['layouts'].index(l),'theme':color,'cells':l['width']*l['height']}
    for name,body in decl.items():marked(ROOT/'src/data/tilesets'/name,'SECRET_BASES_06C2',body)
    dump(ROOT/'data/layouts/layouts.json',node);dump(OUT/'build.json',report)
    print(json.dumps({'maps':len(NAMES),'banks':2,'layouts':len(node['layouts']),'shared_primary_unchanged':True}))

if __name__=='__main__':main()
