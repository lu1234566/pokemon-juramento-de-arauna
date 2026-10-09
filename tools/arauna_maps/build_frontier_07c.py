#!/usr/bin/env python3
"""Terracotta water garden and timber training rooms; native masks and IDs."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw
from native_visuals_v2 import Pair,dump,marked,declarations
from frontier_07c_common import BASE,ROOT,OUT,GROUPS,ARENA,PALACE,inventory,protected_ids,require_base
from trainer_hill_06a_art import native_layers
from render_native_map import words

def texture(theme,mid):
    im=Image.new('L',(16,16),5 if theme=='arena' else 13);d=ImageDraw.Draw(im)
    if theme=='arena':
        for y in (0,8):d.line((0,y,15,y),fill=6)
        for y in (7,15):d.line((0,y,15,y),fill=3)
        d.line((5,1,5,6),fill=4);d.line((13,9,13,14),fill=4);d.line((1,3,3,3),fill=6)
    else:
        d.rectangle((0,0,15,15),outline=11);d.line((1,1,14,1),fill=14);d.line((1,1,1,14),fill=14)
        d.rectangle((3,3,12,12),outline=12)
        if mid in (0x205,0x206,0x221,0x237):d.polygon(((8,4),(11,8),(8,11),(4,8)),outline=7)
        else:d.line((7,7,8,8),fill=14)
    return im

def planes(reader,mid,theme):
    material=ARENA if theme=='arena' else PALACE;floor=texture(theme,mid);out=[]
    for native in native_layers(reader,mid):
        im=Image.new('L',(16,16));values=[]
        for i,(r,g,b,a) in enumerate(native.getdata()):
            if not a:values.append(0);continue
            x,y=i%16,i//16;lum=(r+g+b)//3
            green=g>r*1.12 and g>b*1.10
            if mid<512 and green:
                v=8 if lum<100 else 9 if lum<160 else 10
                if x in (3,11) and y in (5,13):v=max(8,v-1)
            elif theme=='arena' and 0x228<=mid<=0x24f:
                if r>g*1.35 and r>b*1.8:v=8
                elif green:v=6 if lum<155 else 7
                else:v=11
            elif theme=='arena' and r>155 and g>135 and b<130 and r<g*1.45:
                v=floor.getpixel((x,y))
                if lum<130:v=max(2,v-1)
            elif theme!='arena' and r>95 and b>g*1.05 and r>b*.75:
                v=floor.getpixel((x,y))
                if lum<110:v=max(11,v-2)
            elif green:
                v=8 if lum<100 else 9 if lum<175 else 10
                if theme=='arena' and 0x229<=mid<=0x24d and y%4==0:v=max(8,v-1)
            elif r>g*1.30 and r>b*1.70:
                v=3 if lum<90 else 4 if lum<135 else 5
                if theme!='arena' and y in (4,12):v=max(2,v-1)
            elif max(r,g,b)-min(r,g,b)<40 and lum>120:
                v=12 if lum<155 else 13 if lum<200 else 15
                if y in (4,12) and lum<225:v=max(11,v-1)
            else:
                target=(r*.88,g*.82,b*.70) if theme!='arena' else (r*.82,g*.83,b*.72)
                v=min(range(1,16),key=lambda k:sum((material[k][j]-target[j])**2 for j in range(3)))
            values.append(v)
        im.putdata(values);out.append(im)
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,ls,maps=inventory(base);build={};records={};decls={k:'' for k in ('graphics.h','metatiles.h','headers.h')}
    for group,names in GROUPS.items():
        first=ls[maps[names[0]]['layout']];pair=Pair(base,first,repack=True);assert not any(e>>12==12 for entries in pair.meta for e in entries)
        theme='arena' if group=='arena' else 'palace';pair.pals[12]=ARENA if theme=='arena' else PALACE;keep=protected_ids(base,names)
        used={v&1023 for n in names for field in ('blockdata_filepath','border_filepath') for v in words(base/ls[maps[n]['layout']][field])};redrawn=[];animated=[]
        for mid in sorted(used-keep):
            entries=(pair.reader.primary_metatiles if mid<512 else pair.reader.secondary_metatiles)[mid%512*8:mid%512*8+8]
            if mid<512:
                if group!='palace_garden':continue
                if any((e&1023) in pair.dynamic for e in entries):animated.append(mid);continue
            bottom,top=planes(pair.reader,mid,theme);pair.put(mid,bottom,12,(top,12));redrawn.append(mid)
        paths=[ROOT/f'data/tilesets/{kind}/arauna_frontier07c_{group}' for kind in ('primary','secondary')];stem='AraunaFrontier07C'+''.join(v.title() for v in group.split('_'));symbols=[stem+'Base',stem+'Art'];pair.write(paths)
        for k,v in declarations(paths,symbols,pair.callbacks).items():decls[k]+=v
        for n in names:
            l=ls[maps[n]['layout']];assert all(ls[maps[other]['layout']][key]==first[key] for other in names for key in ('primary_tileset','secondary_tileset')) if n==names[0] else True
            l['primary_tileset']='gTileset_'+symbols[0];l['secondary_tileset']='gTileset_'+symbols[1];records[n]={'layout':l['id'],'layout_index':node['layouts'].index(l),'cells':l['width']*l['height'],'group':group}
        build[group]={'paths':[p.relative_to(ROOT).as_posix() for p in paths],'source_paths':[p.relative_to(base).as_posix() for p in pair.paths],'symbols':symbols,'callbacks':pair.callbacks,'redrawn_ids':redrawn,'protected_door_ids':sorted(keep),'allocated_tiles':sorted(pair.touched),'preserved_animated_primary_ids':animated,'material_palette':12,'all_other_palettes_exact':True}
    for k,v in decls.items():marked(ROOT/'src/data/tilesets'/k,'FRONTIER_07C',v)
    dump(ROOT/'data/layouts/layouts.json',node);dump(OUT/'build.json',{'base_commit':BASE,'maps':records,'banks':build})
    print(json.dumps({'maps':len(records),'banks':{k:{'redrawn_ids':len(v['redrawn_ids']),'allocated_tiles':len(v['allocated_tiles']),'animated_primary_ids':v['preserved_animated_primary_ids']} for k,v in build.items()}}))

if __name__=='__main__':main()
