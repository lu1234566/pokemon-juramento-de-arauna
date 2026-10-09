#!/usr/bin/env python3
"""Quiet refuge interiors: timber, sandstone, woven seats and copper thresholds."""
import argparse,json
from functools import lru_cache
from pathlib import Path
from PIL import Image,ImageDraw
from native_visuals_v2 import Pair,dump,marked,declarations
from frontier_07g_common import BASE,ROOT,OUT,NAMES,inventory,require_base
from trainer_hill_06a_art import native_layers
from render_native_map import words

MATERIAL=[(0,0,0),(32,24,24),(64,48,32),(104,72,48),(128,96,64),(176,136,88),(48,72,64),(48,104,80),(80,144,96),(152,184,104),(88,48,32),(144,80,40),(208,144,64),(80,56,72),(144,88,104),(232,216,168)]
RUGS={0x3ac,0x3ad,0x3ae,0x3b5,0x3b6}
FRIEZE={0x395,0x3c3,0x3c4,0x3c5,0x3c7}
WALLS={0x38d,0x3a4,0x3bb,0x3bc,0x3bd,0x3be,0x3bf}

@lru_cache(None)
def floor(kind,mid):
    im=Image.new('L',(16,16),3);d=ImageDraw.Draw(im)
    if kind=='wide':
        # Restrained limestone paving, without the original blue checkerboard.
        d.line((0,15,15,15),fill=2);d.line((15,0,15,14),fill=2)
        d.line((1,0,14,0),fill=4);d.point((2,1),fill=4)
    else:
        # Two timber boards per metatile; stagger the joints across both floor IDs.
        d.line((0,7,15,7),fill=2);d.line((0,15,15,15),fill=2)
        seam=3 if mid in (0x3c8,0x3ca,0x3d0,0x3d2) else 11
        d.line((seam,0,seam,6),fill=2);d.line(((seam+8)%16,8,(seam+8)%16,14),fill=2)
        d.line((6,3,10,3),fill=4);d.line((1,11,4,11),fill=4)
    return im

def material(rgb,x,y,mid,kind,layer):
    r,g,b=rgb;lum=(r+g+b)/3
    # Pixel silhouettes and alpha are copied from the native two planes.
    # Original blue is the floor and its footprint shadow, never a new walkable prop.
    if b>r*1.2 and b>g*1.12:
        return 2 if lum<65 else floor(kind,mid).getpixel((x,y))
    if mid in WALLS:
        if y<4:return 15
        if y<8:return 5 if x%8 not in (0,7) else 4
        if y==8:return 2
        if y==9:return 11
        if y==10:return 12
        return 3 if x%8 else 2
    if mid in FRIEZE and y<8:
        # Woven leaf/diamond band replaces the checker wallpaper.
        v=7 if (x+y)%8 in (3,4) or (x-y)%8 in (3,4) else 15
        return 12 if y in (0,7) else v
    if mid in RUGS and (r>g*1.3 and r>b*1.4):
        if r<110:return 6
        if g>125:return 12
        return 8 if (x+y)%4==0 else 7
    if g>r*1.07 and g>b*1.08:
        return 6 if lum<85 else 7 if lum<125 else 8 if lum<180 else 9
    if r>g*1.18 and r>b*1.18:
        # Chairs retain the original seat, arm, back and wood-leg silhouettes.
        if mid>=0x3da:
            if lum<75:return 10
            if lum<110:return 11
            if kind=='narrow':return 8 if (x+y)%4==0 else 7
            return 14 if (x+y)%4==0 else 13
        return 10 if lum<95 else 11 if lum<145 else 12 if lum<205 else 15
    if r>125 and g>b*1.2:
        return 4 if lum<120 else 5 if lum<175 else 12 if lum<215 else 15
    return 1 if lum<45 else 2 if lum<90 else 4 if lum<135 else 5 if lum<185 else 15

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,ls,maps=inventory(base);headers={k:'' for k in ('graphics.h','metatiles.h','headers.h')};records={};banks=[]
    groups=[('wide','BattleFrontier_Lounge2','LoungeWide'),('narrow','BattleFrontier_Lounge1','LoungeNarrow'),('house','BattleFrontier_ScottsHouse','BentoHouse')]
    for kind,representative,suffix in groups:
        layout=ls[maps[representative]['layout']];members=[n for n in NAMES if maps[n]['layout']==layout['id']]
        pair=Pair(base,layout,repack=False);assert not any(e>>12==12 for entries in pair.meta for e in entries)
        pal=list(MATERIAL)
        if kind=='wide':pal[2]=(72,72,64);pal[3]=(112,112,96);pal[4]=(136,136,112)
        if kind=='house':pal[3]=(88,56,40);pal[4]=(112,80,56)
        pair.pals[12]=pal
        used={v&1023 for f in ('blockdata_filepath','border_filepath') for v in words(base/layout[f])};redrawn=[]
        for mid in sorted(used):
            if mid<512:continue
            planes=[]
            for layer,native in enumerate(native_layers(pair.reader,mid)):
                values=[]
                for i,(r,g,b,a) in enumerate(native.getdata()):
                    rgb=tuple(c>>3<<3 for c in (r,g,b));values.append(material(rgb,i%16,i//16,mid,kind,layer) if a else 0)
                im=Image.new('L',(16,16));im.putdata(values);planes.append(im)
            pair.put(mid,planes[0],12,(planes[1],12));redrawn.append(mid)
        paths=[ROOT/f'data/tilesets/{k}/arauna_frontier07g_{kind}' for k in ('primary','secondary')];symbols=['AraunaFrontier07G'+suffix+'Base','AraunaFrontier07G'+suffix+'Art'];pair.write(paths)
        for k,v in declarations(paths,symbols,pair.callbacks).items():headers[k]+=v
        banks.append({'kind':kind,'layout':layout['id'],'maps':members,'paths':[p.relative_to(ROOT).as_posix() for p in paths],'source_paths':[p.relative_to(base).as_posix() for p in pair.paths],'symbols':symbols,'callbacks':pair.callbacks,'redrawn_ids':redrawn,'allocated_tiles':sorted(pair.touched),'free_slots':len(pair.free),'material_palette':12,'all_other_palettes_exact':True,'attributes_and_layer_masks_exact':True})
        layout['primary_tileset']='gTileset_'+symbols[0];layout['secondary_tileset']='gTileset_'+symbols[1]
        for n in members:records[n]={'layout':layout['id'],'layout_index':node['layouts'].index(layout),'cells':layout['width']*layout['height'],'bank_kind':kind}
    for k,v in headers.items():marked(ROOT/'src/data/tilesets'/k,'FRONTIER_07G',v)
    dump(ROOT/'data/layouts/layouts.json',node)
    dump(OUT/'build.json',{'base_commit':BASE,'maps':records,'banks':banks,'unique_layouts':3,'unique_cells':242,'native_ids_and_sharing_unchanged':True})
    print(json.dumps({'maps':len(records),'shared_layouts':3,'cells':sum(r['cells'] for r in records.values()),'redrawn_metatiles':sum(len(b['redrawn_ids']) for b in banks),'allocated_tiles':sum(len(b['allocated_tiles']) for b in banks),'callbacks':[b['callbacks'] for b in banks]}))

if __name__=='__main__':main()
