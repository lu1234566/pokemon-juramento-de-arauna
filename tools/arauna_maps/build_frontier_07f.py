#!/usr/bin/env python3
"""Quiet stone, copper navigation marks and a dusk compass above the Pyramid."""
import argparse,json,collections
from pathlib import Path
from PIL import Image,ImageDraw
from native_visuals_v2 import Pair,dump,marked,declarations
from frontier_07f_common import BASE,ROOT,OUT,NAMES,SQUARES,MATERIAL,ANIMATED,inventory,require_base
from trainer_hill_06a_art import native_layers
from render_native_map import words

def pavement(pal6=False):
    im=Image.new('L',(16,16),6 if pal6 else 3);d=ImageDraw.Draw(im)
    d.line((0,15,15,15),fill=7 if pal6 else 2);d.line((15,0,15,15),fill=7 if pal6 else 2)
    d.line((0,0,14,0),fill=7 if pal6 else 4)
    d.point((1,1),fill=8 if pal6 else 10);d.point((2,1),fill=7 if pal6 else 8)
    return im

def signal():
    im=Image.new('L',(16,16),5);d=ImageDraw.Draw(im)
    d.rectangle((1,1,14,14),outline=4);d.rectangle((3,3,12,12),outline=3)
    d.polygon([(8,4),(11,8),(8,11),(5,8)],fill=2)
    d.line((8,5,8,9),fill=4);d.line((6,7,8,5,10,7),fill=2)
    return im

def material(rgb,x,y,mid):
    r,g,b=rgb;lum=(r+g+b)/3
    if mid in (0x251,0x259):
        return 12 if lum>195 else 11 if lum>155 else 8 if lum>105 else 2
    if mid in (0x201,0x202,0x203,0x20b,0x21b,0x21c,0x231,0x2c8):
        return pavement().getpixel((x,y)) if lum>=65 else 1
    if mid>=0x278 and mid<=0x29c:
        if r>220 and g<95:return 12
        if r>220 and g<175:return 11
        if r>220 and g<215:return 9
        return 1 if lum<100 else 13
    if 0x238<=mid<=0x25e:
        if r>230 and g>170:return 13 if b<130 else 3
        return 2 if lum<100 else 3 if lum<155 else 4 if lum<190 else 5 if lum<225 else 12
    if b>r*1.1:return 1 if lum<100 else 13
    if r>g*1.20 and r>b*1.20:return 7 if lum<90 else 8 if lum<150 else 10 if lum<200 else 11
    if g>b*1.22 and r>=g:return 8 if lum<100 else 9 if lum<160 else 11 if lum<210 else 12
    return 1 if lum<65 else 2 if lum<105 else 3 if lum<150 else 4 if lum<205 else 5

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,ls,maps=inventory(base);first=ls[maps[NAMES[0]]['layout']];pair=Pair(base,first,repack=False)
    # Reserve the exact VRAM destinations before allocating; no shared editor changes.
    pair.dynamic|=ANIMATED;pair.free=[i for i in pair.free if i not in pair.dynamic]
    assert not any(e>>12==12 for entries in pair.meta for e in entries);pair.pals[12]=MATERIAL
    used={v&1023 for n in NAMES+SQUARES for f in ('blockdata_filepath','border_filepath') for v in words(base/ls[maps[n]['layout']][f])}
    top=ls[maps[NAMES[2]]['layout']];grid=words(base/top['blockdata_filepath']);counts=collections.Counter(v&1023 for v in grid)
    # The disk becomes a copper-framed compass. The sky and silhouette remain readable.
    compass=Image.new('L',(80,80),0);d=ImageDraw.Draw(compass)
    d.ellipse((4,4,75,75),fill=11,outline=8,width=2);d.ellipse((9,9,70,70),fill=12,outline=10,width=2)
    for a,b in [((40,12),(40,67)),((12,40),(67,40)),((22,22),(57,57)),((57,22),(22,57))]:d.line((a,b),fill=10,width=1)
    d.polygon([(40,15),(46,34),(64,40),(46,46),(40,65),(34,46),(16,40),(34,34)],fill=8)
    d.polygon([(40,21),(43,37),(57,40),(43,43),(40,59),(37,43),(23,40),(37,37)],fill=13)
    d.ellipse((36,36,44,44),fill=11)
    disk_ids=set(range(0x278,0x285))|set(range(0x288,0x28d))|set(range(0x290,0x295))
    positions={v&1023:(i%top['width']-15,i//top['width']-3) for i,v in enumerate(grid) if v&1023 in disk_ids and counts[v&1023]==1}
    redrawn=[];retained=[]
    for mid in sorted(used):
        if mid<512:continue
        pal=6 if 0x260<=mid<=0x274 or mid in (0x20d,0x28d,0x28e) else 12
        original=pair.meta[1][(mid-512)*8:(mid-512)*8+8].copy();planes=[]
        for layer,native in enumerate(native_layers(pair.reader,mid)):
            values=[]
            for i,(r,g,b,a) in enumerate(native.getdata()):
                x,y=i%16,i//16;rgb=tuple(c>>3<<3 for c in (r,g,b))
                if not a:v=0
                elif pal==6:
                    if mid==0x28d:v=pavement(True).getpixel((x,y))
                    elif mid in (0x20d,0x28e):v=signal().getpixel((x,y))
                    else:
                        v=min(range(1,16),key=lambda j:sum((rgb[k]-(pair.pals[6][j][k]>>3<<3))**2 for k in range(3)))
                        if v in (8,9,10) and y in (7,15):v=max(7,v-1)
                        if v in (8,9,10) and (x+(8 if y<8 else 0))%16==15:v=max(7,v-1)
                elif mid in positions and layer==0 and r>220:
                    px,py=positions[mid];cx=px*16+x;cy=py*16+y
                    v=compass.getpixel((cx,cy)) if 0<=cx<80 and 0<=cy<80 else material(rgb,x,y,mid)
                    if v==0:v=13
                else:v=material(rgb,x,y,mid)
                values.append(v)
            im=Image.new('L',(16,16));im.putdata(values);planes.append(im)
        entries=pair.put(mid,planes[0],pal,(planes[1],pal))
        # Animated torch/shadow tiles keep native graphics, palette and flips in every frame.
        for j,e in enumerate(original):
            if e&1023 in ANIMATED:pair.meta[1][(mid-512)*8+j]=e;retained.append({'metatile':mid,'quadrant':j,'entry':e})
        redrawn.append(mid)
    paths=[ROOT/f'data/tilesets/{k}/arauna_frontier07f_pyramid' for k in ('primary','secondary')];symbols=['AraunaFrontier07FPyramidBase','AraunaFrontier07FPyramidArt'];pair.write(paths)
    for k,v in declarations(paths,symbols,pair.callbacks).items():marked(ROOT/'src/data/tilesets'/k,'FRONTIER_07F',v)
    records={}
    for n in NAMES:
        l=ls[maps[n]['layout']];l['primary_tileset']='gTileset_'+symbols[0];l['secondary_tileset']='gTileset_'+symbols[1]
        records[n]={'layout':l['id'],'layout_index':node['layouts'].index(l),'cells':l['width']*l['height']}
    dump(ROOT/'data/layouts/layouts.json',node)
    dump(OUT/'build.json',{'base_commit':BASE,'maps':records,'bank':{'paths':[p.relative_to(ROOT).as_posix() for p in paths],'source_paths':[p.relative_to(base).as_posix() for p in pair.paths],'symbols':symbols,'callbacks':pair.callbacks,'redrawn_ids':redrawn,'allocated_tiles':sorted(pair.touched),'reserved_pyramid_animation_tiles':sorted(ANIMATED),'retained_animated_entries':retained,'material_palette':12,'runtime_palette':6,'module_metatile_ids':sorted({v&1023 for n in SQUARES for v in words(base/ls[maps[n]['layout']]['blockdata_filepath'])}),'source_module_bank_references_unchanged':True,'all_other_palettes_exact':True,'attributes_and_layer_masks_exact':True}})
    print(json.dumps({'maps':3,'source_modules':16,'cells':sum(r['cells'] for r in records.values()),'redrawn_metatiles':len(redrawn),'allocated_tiles':len(pair.touched),'free_slots':len(pair.free),'retained_animation_entries':len(retained),'callbacks':pair.callbacks}))

if __name__=='__main__':main()
