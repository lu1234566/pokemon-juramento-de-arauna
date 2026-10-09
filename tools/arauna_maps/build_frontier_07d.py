#!/usr/bin/env python3
"""Stone workshop, copper infrastructure and jade consoles in native 4bpp banks."""
import argparse,math,json
from pathlib import Path
from PIL import Image,ImageDraw
from native_visuals_v2 import Pair,dump,marked,declarations
from frontier_07d_common import BASE,ROOT,OUT,NAMES,MATERIAL,inventory,door_records,require_base
from trainer_hill_06a_art import native_layers
from render_native_map import words

FLOOR_IDS={0x201,0x202,0x203,0x204}

def plate(mid):
    im=Image.new('L',(16,16),3);d=ImageDraw.Draw(im)
    d.line((0,15,15,15),fill=2);d.line((15,0,15,15),fill=2)
    d.line((0,0,14,0),fill=4);d.line((0,0,0,14),fill=4)
    d.point((2,2),fill=5);d.point((13,13),fill=2)
    if mid in (0x202,0x204):d.line((5,5,10,5),fill=4);d.line((10,5,10,8),fill=4)
    return im

def stage():
    im=Image.new('L',(208,192),3);d=ImageDraw.Draw(im)
    for x in range(0,208,16):d.line((x,0,x,191),fill=2);d.line((x+1,0,x+1,191),fill=4)
    for y in range(0,192,16):d.line((0,y,207,y),fill=2);d.line((0,y+1,207,y+1),fill=4)
    d.rounded_rectangle((49,81,158,142),radius=9,outline=10,width=2)
    d.line((58,83,148,83),fill=11);d.line((51,91,51,131),fill=11)
    # Calibration emblem: a copper gear, not a new gameplay marker or trigger.
    cx,cy=104,112
    points=[]
    for i in range(8):
        a=2*math.pi*i/8
        for r,t in ((22,-5),(28,-5),(28,5),(22,5)):
            points.append((round(cx+math.cos(a)*r-math.sin(a)*t),round(cy+math.sin(a)*r+math.cos(a)*t)))
    d.polygon(points,fill=9,outline=11);d.ellipse((84,92,124,132),fill=3,outline=10,width=2)
    d.line((79,112,129,112),fill=5);d.line((104,87,104,137),fill=5)
    d.polygon(((104,102),(114,112),(104,122),(94,112)),fill=12,outline=14)
    d.rectangle((101,109,107,115),fill=13);d.point((103,111),fill=15)
    return im

def material_pixel(rgb,x,y,role):
    r,g,b=rgb;lum=(r+g+b)/3
    if g>r*1.10 and g>b*1.06:return 12 if lum<110 else 13 if lum<180 else 14
    if r>160 and g>120 and b<115 and r<g*1.65:return 9 if lum<125 else 10 if lum<175 else 11
    if r>g*1.35 and r>b*1.50:return 8 if lum<100 else 9 if lum<155 else 10
    if b>r*1.10 and g>r*.80:return 12 if lum<110 else 13 if lum<170 else 15
    # Retain bright architectural profiles, dark recesses and legible machine silhouettes.
    if lum>224:return 7
    if lum>186:return 6
    if lum>150:return 5
    if lum>114:return 4
    if lum>78:return 3
    if lum>46:return 2
    return 1

def planes(reader,mid,scene_position=None,floor_tiles=()):
    slab=plate(mid);calibration=stage() if scene_position else None;out=[]
    source=reader.secondary_metatiles[(mid-512)*8:(mid-512)*8+8]
    for layer,native in enumerate(native_layers(reader,mid)):
        values=[]
        for i,(r,g,b,a) in enumerate(native.getdata()):
            if not a:values.append(0);continue
            x,y=i%16,i//16
            floor_component=(source[(y//8)*2+x//8]&1023) in floor_tiles and source[(y//8)*2+x//8]>>12==6
            if mid in FLOOR_IDS:v=slab.getpixel((x,y))
            elif scene_position:
                sx,sy=scene_position;gx,gy=sx*16+x,sy*16+y
                if 48<=gx<160 and 80<=gy<144:v=calibration.getpixel((gx,gy))
                else:
                    # Native edge shading identifies the lit platform and the shaded corners.
                    lum=(r+g+b)/3;v=slab.getpixel((x,y))
                    if lum<150:v=max(1,v-1)
                    if r>g*1.35 and r>b*1.50:v=9
                    if 180<lum<235 and x in (0,15):v=max(2,v-1)
            elif layer==0 and (floor_component or (0x280<=mid<=0x287 and (r,g,b) in ((208,208,192),(248,248,248),(168,168,136)))):
                # Only native floor components below furniture change material.
                # The foreground silhouettes, shadow masks and architectural components stay legible.
                v=slab.getpixel((x,y))
            else:
                v=material_pixel((r,g,b),x,y,'architecture')
                # Sparse masonry joints and copper highlights preserve the source outline.
                if v in (5,6,7) and y==7 and mid in (0x222,0x223,0x224,0x225,0x228,0x229,0x270,0x271,0x272):v=max(4,v-1)
            values.append(v)
        im=Image.new('L',(16,16));im.putdata(values);out.append(im)
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,ls,maps=inventory(base);first=ls[maps[NAMES[0]]['layout']];pair=Pair(base,first,repack=True)
    assert not any(e>>12==12 for entries in pair.meta for e in entries);pair.pals[12]=MATERIAL
    assert all(ls[maps[n]['layout']][k]==first[k] for n in NAMES for k in ('primary_tileset','secondary_tileset'))
    keep={c['id'] for cells in door_records(base).values() for c in cells}
    used={v&1023 for n in NAMES for f in ('blockdata_filepath','border_filepath') for v in words(base/ls[maps[n]['layout']][f])}
    battle=ls[maps[NAMES[2]]['layout']];g=words(base/battle['blockdata_filepath']);other={v&1023 for n in NAMES[:2] for v in words(base/ls[maps[n]['layout']]['blockdata_filepath'])}
    positions={}
    for i,v in enumerate(g):
        mid=v&1023;x,y=i%battle['width'],i//battle['width']
        if y>=3:
            assert mid not in other and mid not in positions,('calibration geometry is not exclusive',mid)
            positions[mid]=(x,y)
    floor_sources=FLOOR_IDS|{0x333,0x334,0x335,0x337,0x33b}
    floor_tiles={e&1023 for mid in floor_sources for e in pair.reader.secondary_metatiles[(mid-512)*8:(mid-512)*8+4] if e>>12==6}
    redrawn=[]
    for mid in sorted(used-keep):
        if mid<512:continue
        bottom,top=planes(pair.reader,mid,positions.get(mid),floor_tiles);pair.put(mid,bottom,12,(top,12));redrawn.append(mid)
    paths=[ROOT/f'data/tilesets/{k}/arauna_frontier07d_factory' for k in ('primary','secondary')];symbols=['AraunaFrontier07DFactoryBase','AraunaFrontier07DFactoryArt'];pair.write(paths)
    for k,v in declarations(paths,symbols,pair.callbacks).items():marked(ROOT/'src/data/tilesets'/k,'FRONTIER_07D',v)
    records={}
    for n in NAMES:
        l=ls[maps[n]['layout']];l['primary_tileset']='gTileset_'+symbols[0];l['secondary_tileset']='gTileset_'+symbols[1]
        records[n]={'layout':l['id'],'layout_index':node['layouts'].index(l),'cells':l['width']*l['height']}
    dump(ROOT/'data/layouts/layouts.json',node)
    dump(OUT/'build.json',{'base_commit':BASE,'maps':records,'bank':{'paths':[p.relative_to(ROOT).as_posix() for p in paths],'source_paths':[p.relative_to(base).as_posix() for p in pair.paths],'symbols':symbols,'callbacks':pair.callbacks,'redrawn_ids':redrawn,'protected_door_ids':sorted(keep),'allocated_tiles':sorted(pair.touched),'material_palette':12,'native_floor_component_tiles':sorted(floor_tiles),'calibration_cells':{str(k):list(v) for k,v in sorted(positions.items())},'all_other_palettes_exact':True,'attributes_and_layer_masks_exact':True}})
    print(json.dumps({'maps':3,'cells':sum(r['cells'] for r in records.values()),'redrawn_metatiles':len(redrawn),'allocated_tiles':len(pair.touched),'free_slots':len(pair.free),'callbacks':pair.callbacks}))

if __name__=='__main__':main()
