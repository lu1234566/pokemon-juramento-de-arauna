#!/usr/bin/env python3
"""Native Battle Tower wood, stone and bronze, keeping door footprints exact."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw
from native_visuals_v2 import Pair,dump,marked,declarations
from frontier_07a_common import BASE,ROOT,OUT,NAMES,MATERIAL,inventory,protected_ids,require_base
from trainer_hill_06a_art import native_layers
from render_native_map import words

def wood(medallion=False):
    im=Image.new('L',(16,16),5);d=ImageDraw.Draw(im)
    for y in (0,8):d.line((0,y,15,y),fill=6)
    for y in (7,15):d.line((0,y,15,y),fill=3)
    d.line((5,1,5,6),fill=4);d.line((13,9,13,14),fill=4)
    d.line((1,3,3,3),fill=6);d.line((8,11,10,11),fill=4)
    if medallion:
        d.polygon(((8,3),(12,8),(8,12),(3,8)),fill=3)
        d.polygon(((8,4),(11,8),(8,11),(4,8)),outline=7)
        d.rectangle((7,7,8,8),fill=6)
    return im

def stone():
    im=Image.new('L',(16,16),13);d=ImageDraw.Draw(im)
    d.line((0,0,15,0),fill=14);d.line((0,15,15,15),fill=12)
    d.line((11,1,11,7),fill=12);d.line((0,8,15,8),fill=14);d.line((3,9,3,14),fill=12)
    d.line((6,12,8,12),fill=14)
    return im

def planes(reader,mid):
    out=[];floor=wood(mid==0x229);rock=stone()
    for native in native_layers(reader,mid):
        im=Image.new('L',(16,16));pixels=[]
        for i,(r,g,b,a) in enumerate(native.getdata()):
            if not a:pixels.append(0);continue
            x,y=i%16,i//16;lum=(r+g+b)//3
            # Cyan floor planes become wood, including the visible support
            # beneath furniture and wall corners. Equipment screens stay native.
            if b>r*1.6 and g>r*1.4 and b>145:
                value=floor.getpixel((x,y));value=max(2,value-1) if lum<110 else value
            elif mid in (0x23a,0x23b,0x23c,0x25c,0x25d,0x264,0x265) and a and lum>115:
                value=rock.getpixel((x,y))
            elif r>g*1.15 and r>b*1.4:
                target=(r*.70,g*.80,b*.85);value=min(range(1,16),key=lambda k:sum((MATERIAL[k][j]-target[j])**2 for j in range(3)))
            elif max(r,g,b)-min(r,g,b)<40 and lum>105:
                # Sandstone wall faces, with restrained joints inside flat areas.
                value=12 if lum<145 else 13 if lum<190 else 14
                if lum>145 and y in (4,12):value-=1
            else:
                target=(r*.82,g*.79,b*.66);value=min(range(1,16),key=lambda k:sum((MATERIAL[k][j]-target[j])**2 for j in range(3)))
            pixels.append(value)
        im.putdata(pixels);out.append(im)
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,ls,maps=inventory(base);first=ls[maps[NAMES[0]]['layout']];pair=Pair(base,first,repack=True)
    assert not any(e>>12==12 for a in pair.meta for e in a)
    pair.pals[12]=MATERIAL;keep=protected_ids(base)
    # Primary art and all animation colors remain exact. A single private pair
    # retains source callbacks and metatile attributes, including unused states.
    used={v&1023 for n in NAMES for k in ('blockdata_filepath','border_filepath') for v in words(base/ls[maps[n]['layout']][k])}
    used|={0x207,0x20f};redrawn=[]
    for mid in sorted(used-keep):
        if mid<512:continue # animated PC stays in the exact primary bank
        bottom,top=planes(pair.reader,mid)
        pair.put(mid,bottom,12,(top,12));redrawn.append(mid)
    paths=[ROOT/f'data/tilesets/{kind}/arauna_frontier07a_tower' for kind in ('primary','secondary')]
    symbols=['AraunaFrontier07ATower'+suffix for suffix in ('Base','Art')]
    pair.write(paths)
    for k,v in declarations(paths,symbols,pair.callbacks).items():marked(ROOT/'src/data/tilesets'/k,'FRONTIER_07A',v)
    records={}
    for n in NAMES:
        l=ls[maps[n]['layout']];l['primary_tileset']='gTileset_'+symbols[0];l['secondary_tileset']='gTileset_'+symbols[1]
        records[n]={'layout':l['id'],'layout_index':node['layouts'].index(l),'cells':l['width']*l['height']}
    dump(ROOT/'data/layouts/layouts.json',node)
    dump(OUT/'build.json',{'base_commit':BASE,'maps':records,'banks':{'tower':{'paths':[p.relative_to(ROOT).as_posix() for p in paths],'source_paths':[p.relative_to(base).as_posix() for p in pair.paths],'symbols':symbols,'callbacks':pair.callbacks,'redrawn_ids':redrawn,'protected_door_ids':sorted(keep),'allocated_tiles':sorted(pair.touched),'material_palette':12,'all_other_palettes_exact':True}}})
    print(json.dumps({'maps':len(NAMES),'layouts':len({maps[n]['layout'] for n in NAMES}),'redrawn_ids':len(redrawn),'allocated_tiles':len(pair.touched),'protected_door_ids':sorted(keep)}))

if __name__=='__main__':main()
