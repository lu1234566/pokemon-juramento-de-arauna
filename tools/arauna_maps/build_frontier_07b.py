#!/usr/bin/env python3
"""Native Dome stone/wood art, with exact animated index-13/15 footprints."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw
from native_visuals_v2 import Pair,dump,marked,declarations
from frontier_07b_common import BASE,ROOT,OUT,NAMES,MATERIAL,inventory,protected_ids,require_base
from trainer_hill_06a_art import native_layers
from render_native_map import words
from build_frontier_07a import wood,stone

GLYPHS={
'A':['01110','10001','10001','11111','10001','10001','10001'],
'R':['11110','10001','10001','11110','10100','10010','10001'],
'U':['10001','10001','10001','10001','10001','10001','01110'],
'N':['10001','11001','11001','10101','10011','10011','10001'],
'C':['01111','10000','10000','10000','10000','10000','01111'],
'I':['11111','00100','00100','00100','00100','00100','11111'],
'T':['11111','00100','00100','00100','00100','00100','00100'],
' ':['00000']*7}

def banner():
    im=Image.new('L',(96,16),1);d=ImageDraw.Draw(im)
    d.line((0,0,95,0),fill=14);d.line((0,15,95,15),fill=7)
    text='ARAUNA CIRCUIT';x=(96-(len(text)*6-1))//2
    for ch in text:
        for y,row in enumerate(GLYPHS[ch]):
            for xx,v in enumerate(row):
                if v=='1':d.point((x+xx,y+4),fill=5)
        x+=6
    return im

BANNER=banner()

def material_planes(reader,mid):
    out=[];floor=stone();timber=wood()
    for native in native_layers(reader,mid):
        im=Image.new('L',(16,16));pixels=[]
        for i,(r,g,b,a) in enumerate(native.getdata()):
            if not a:pixels.append(0);continue
            x,y=i%16,i//16;lum=(r+g+b)//3
            if g>r*1.10 and b>r*1.05 and g>b*.80:
                # Mint lobby floors become stone; dark planes become timber.
                v=floor.getpixel((x,y)) if lum>135 else timber.getpixel((x,y))
                if lum>205:v=min(14,v+1)
            elif max(r,g,b)-min(r,g,b)<42 and lum>110:
                v=12 if lum<145 else 13 if lum<195 else 14
                if y in (4,12) and lum<220:v=max(11,v-1)
            elif r>g*1.12 and r>b*1.25:
                target=(r*.74,g*.80,b*.84);v=min(range(1,16),key=lambda k:sum((MATERIAL[k][j]-target[j])**2 for j in range(3)))
            else:
                target=(r*.75,g*.77,b*.74);v=min(range(1,16),key=lambda k:sum((MATERIAL[k][j]-target[j])**2 for j in range(3)))
            pixels.append(v)
        im.putdata(pixels);out.append(im)
    return out

def indexed_quadrant(reader,e):
    im=reader._tile(e&1023).copy()
    if e&0x400:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if e&0x800:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return im

def lights_plane(reader,mid,j,e):
    im=indexed_quadrant(reader,e);out=[];dx=(j%4%2)*8;dy=(j%4//2)*8
    for i,v in enumerate(im.getdata()):
        x,y=dx+i%8,dy+i//8
        if v in (0,13,15):nv=v # transparent and animated pixels remain exact
        elif 0x2d5<=mid<=0x2da and j<4:nv=BANNER.getpixel(((mid-0x2d5)*16+x,y))
        elif mid in (0x2d0,0x2d1):
            nv={9:7,10:12,11:14}.get(v,v)
            if v in (10,11) and y in (4,12):nv=7
        elif v in (9,10,11):nv={9:1,10:2,11:4}[v]
        elif 0x2e0<=mid<=0x33f and v in (6,8):nv=2 if v==6 else 4
        elif v in (12,14):
            nv=2 if v==12 else 3
            if mid==0x309:
                nv=3
                if y in (0,8):nv=4
                elif y in (7,15) or x==(11 if y<8 else 3):nv=2
        else:nv=v
        assert (nv==0)==(v==0) and (nv in (13,15))==(v in (13,15))
        out.append(nv)
    result=Image.new('L',(8,8));result.putdata(out);return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,ls,maps=inventory(base);first=ls[maps[NAMES[0]]['layout']];pair=Pair(base,first,repack=True)
    assert not any(e>>12==12 for a in pair.meta for e in a)
    pair.pals[12]=MATERIAL;keep=protected_ids(base)
    used={v&1023 for n in NAMES for k in ('blockdata_filepath','border_filepath') for v in words(base/ls[maps[n]['layout']][k])};redrawn=[];lights=[]
    for mid in sorted(used-keep):
        if mid<512:continue
        original=pair.reader.secondary_metatiles[(mid-512)*8:(mid-512+1)*8]
        bottom,top=material_planes(pair.reader,mid);entries=pair.put(mid,bottom,12,(top,12))
        for j,e in enumerate(original):
            if e>>12==8:
                entries[j]=pair.tile(lights_plane(pair.reader,mid,j,e))|(8<<12);lights.append([mid,j])
        pair.meta[1][(mid-512)*8:(mid-512+1)*8]=entries;redrawn.append(mid)
    paths=[ROOT/f'data/tilesets/{kind}/arauna_frontier07b_dome' for kind in ('primary','secondary')];symbols=['AraunaFrontier07BDome'+suffix for suffix in ('Base','Art')]
    pair.write(paths)
    for k,v in declarations(paths,symbols,pair.callbacks).items():marked(ROOT/'src/data/tilesets'/k,'FRONTIER_07B',v)
    records={}
    for n in NAMES:
        l=ls[maps[n]['layout']];l['primary_tileset']='gTileset_'+symbols[0];l['secondary_tileset']='gTileset_'+symbols[1]
        records[n]={'layout':l['id'],'layout_index':node['layouts'].index(l),'cells':l['width']*l['height']}
    dump(ROOT/'data/layouts/layouts.json',node)
    dump(OUT/'build.json',{'base_commit':BASE,'maps':records,'banks':{'dome':{'paths':[p.relative_to(ROOT).as_posix() for p in paths],'source_paths':[p.relative_to(base).as_posix() for p in pair.paths],'symbols':symbols,'callbacks':pair.callbacks,'redrawn_ids':redrawn,'protected_door_ids':sorted(keep),'allocated_tiles':sorted(pair.touched),'material_palette':12,'all_other_palettes_exact':True,'palette8_quadrants':lights,'animated_indices':[13,15],'banner':'ARAUNA CIRCUIT'}}})
    print(json.dumps({'maps':len(NAMES),'layouts':4,'redrawn_ids':len(redrawn),'allocated_tiles':len(pair.touched),'palette8_quadrants':len(lights)}))

if __name__=='__main__':main()
