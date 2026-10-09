#!/usr/bin/env python3
"""Basalt, copper serpentine figures, wine curtains and jade thresholds in native GBA banks."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw
from native_visuals_v2 import Pair,dump,marked,declarations
from frontier_07e_common import BASE,ROOT,OUT,NAMES,MATERIAL,inventory,curtain_ids,require_base
from trainer_hill_06a_art import native_layers
from render_native_map import words

FLOOR_COLORS={(224,112,120),(248,152,160),(160,136,48),(200,168,48)}
SHADOW_COLORS={(176,80,64),(120,104,48)}

def stone(mid):
    im=Image.new('L',(16,16),3);d=ImageDraw.Draw(im)
    d.line((0,15,15,15),fill=2);d.line((15,0,15,15),fill=2)
    d.line((0,0,14,0),fill=4);d.line((0,0,0,14),fill=4)
    # Small copper inlay at tile junctions, leaving quiet stone for characters.
    d.point((1,1),fill=11);d.point((2,1),fill=10);d.point((1,2),fill=10)
    if mid==0x2c2:d.line((6,7,9,7),fill=4);d.line((7,6,7,9),fill=4)
    return im

def coil():
    im=Image.new('L',(48,48),3);d=ImageDraw.Draw(im)
    for x in (0,16,32):d.line((x,0,x,47),fill=2);d.line((x+1,0,x+1,47),fill=4)
    for y in (0,16,32):d.line((0,y,47,y),fill=2);d.line((0,y+1,47,y+1),fill=4)
    d.ellipse((5,5,42,42),outline=10,width=2)
    d.line([(12,33),(12,17),(18,11),(31,11),(36,17),(36,29),(31,35),(22,35),(18,31),(18,22),(23,18),(28,18),(30,21)],fill=11,width=3)
    d.line([(13,31),(13,18),(19,12),(30,12),(35,18)],fill=12,width=1)
    d.polygon([(28,20),(33,20),(34,23),(30,26),(27,23)],fill=13,outline=14)
    d.point((31,22),fill=15)
    return im

def material(rgb,x,y,mid,layer):
    rgb=tuple(c>>3<<3 for c in rgb)
    r,g,b=rgb;lum=(r+g+b)/3
    if layer==0 and rgb in FLOOR_COLORS:return stone(mid).getpixel((x,y))
    if layer==0 and rgb in SHADOW_COLORS:return 2
    # The wide red carpet becomes woven wine fabric with sparse copper stitches.
    if mid>=0x2de and (r>g*2.5 and r>b*2):
        return 8 if x%8 in (y%8,7-y%8) else 6 if y%8==7 else 7
    # Keep the native folds, tie-backs and upper rail, in muted wine/copper.
    if r>g*2 and r>b*2:
        return 6 if r<145 else 7 if r<220 else 8
    if r>g*1.4 and g>b*1.25:
        return 6 if lum<80 else 8 if lum<155 else 9
    if r>g*1.35 and b>g*1.05:return 7 if lum<135 else 8 if lum<190 else 9
    if r>150 and g>120 and b<110:return 10 if lum<125 else 11 if lum<170 else 12
    if r>g*1.20 and r>b*1.30:return 10 if lum<100 else 11 if lum<160 else 12
    if g>r*1.05 or b>r*1.12:return 13 if lum<125 else 14 if lum<190 else 15
    return 1 if lum<60 else 2 if lum<95 else 3 if lum<140 else 4 if lum<200 else 5

def planes(reader,mid,emblem_position=None):
    artwork=coil() if emblem_position else None;out=[]
    for layer,native in enumerate(native_layers(reader,mid)):
        values=[]
        for i,(r,g,b,a) in enumerate(native.getdata()):
            if not a:values.append(0);continue
            x,y=i%16,i//16
            if emblem_position and layer==0:
                sx,sy=emblem_position;v=artwork.getpixel((sx*16+x,sy*16+y))
            elif layer==0 and mid in (0x2c1,0x2c2):v=stone(mid).getpixel((x,y))
            else:v=material((r,g,b),x,y,mid,layer)
            values.append(v)
        im=Image.new('L',(16,16));im.putdata(values);out.append(im)
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,ls,maps=inventory(base);first=ls[maps[NAMES[0]]['layout']];pair=Pair(base,first,repack=True)
    assert not any(e>>12==12 for entries in pair.meta for e in entries);pair.pals[12]=MATERIAL
    assert all(ls[maps[n]['layout']][k]==first[k] for n in NAMES for k in ('primary_tileset','secondary_tileset'))
    used={v&1023 for n in NAMES for f in ('blockdata_filepath','border_filepath') for v in words(base/ls[maps[n]['layout']][f])}
    dynamic=set(curtain_ids(base));used|=dynamic
    final=ls[maps[NAMES[4]]['layout']];grid=words(base/final['blockdata_filepath']);other={v&1023 for n in NAMES if n!=NAMES[4] for v in words(base/ls[maps[n]['layout']]['blockdata_filepath'])}
    positions={}
    for y in range(4,7):
        for x in range(1,4):
            mid=grid[y*final['width']+x];mid&=1023
            assert mid not in other and mid not in dynamic and mid not in positions
            positions[mid]=(x-1,y-4)
    redrawn=[]
    for mid in sorted(used):
        if mid<512:continue
        bottom,top=planes(pair.reader,mid,positions.get(mid));pair.put(mid,bottom,12,(top,12));redrawn.append(mid)
    paths=[ROOT/f'data/tilesets/{k}/arauna_frontier07e_pike' for k in ('primary','secondary')];symbols=['AraunaFrontier07EPikeBase','AraunaFrontier07EPikeArt'];pair.write(paths)
    for k,v in declarations(paths,symbols,pair.callbacks).items():marked(ROOT/'src/data/tilesets'/k,'FRONTIER_07E',v)
    records={}
    for n in NAMES:
        l=ls[maps[n]['layout']];l['primary_tileset']='gTileset_'+symbols[0];l['secondary_tileset']='gTileset_'+symbols[1]
        records[n]={'layout':l['id'],'layout_index':node['layouts'].index(l),'cells':l['width']*l['height']}
    dump(ROOT/'data/layouts/layouts.json',node)
    dump(OUT/'build.json',{'base_commit':BASE,'maps':records,'bank':{'paths':[p.relative_to(ROOT).as_posix() for p in paths],'source_paths':[p.relative_to(base).as_posix() for p in pair.paths],'symbols':symbols,'callbacks':pair.callbacks,'redrawn_ids':redrawn,'curtain_ids':sorted(dynamic),'allocated_tiles':sorted(pair.touched),'material_palette':12,'coil_cells':{str(k):list(v) for k,v in sorted(positions.items())},'all_other_palettes_exact':True,'attributes_and_layer_masks_exact':True}})
    print(json.dumps({'maps':6,'cells':sum(r['cells'] for r in records.values()),'redrawn_metatiles':len(redrawn),'curtain_metatiles':len(dynamic),'allocated_tiles':len(pair.touched),'free_slots':len(pair.free),'callbacks':pair.callbacks}))

if __name__=='__main__':main()
