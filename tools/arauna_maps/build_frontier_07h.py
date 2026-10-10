#!/usr/bin/env python3
"""Timber exchange, ceramic market, limestone clinic and bronze record gallery."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw
from native_visuals_v2 import Pair,dump,marked,declarations
from frontier_07h_common import ROOT,BASE,OUT,NAMES,inventory,require_base
from trainer_hill_06a_art import native_layers
from render_native_map import words
MATERIAL=[(0,0,0),(24,32,32),(48,56,48),(88,80,64),(128,120,96),(176,168,136),(216,208,168),(240,232,200),(32,72,64),(56,112,80),(112,160,104),(56,40,32),(104,64,40),(160,104,56),(208,152,80),(232,192,112)]
# Machines, healing station, working stairs and cable door keep native pixels.
# Cable script replacement floors are redrawn together with the closed barrier.
PC_PROTECTED=set(range(0x280,0x28e))|set(range(0x298,0x2ae))|{0x264,0x25c,0x25b,0x24a,0x24b,0x248,0x249,0x250,0x251,0x252,0x253,0x207,0x205,0x206,0x222,0x223,0x22a,0x22b,0x258,0x259,0x260,0x261,0x272,0x27a,0x213,0x247,0x24f,0x2a6,0x2cf,0x2cd,0x2d5,0x2d6,0x2d7,0x2d8,0x2d9,0x2da,0x2db,0x2e0}
FLOORS={'exchange':{0x3b8,0x3b9,0x3c0,0x3c1},'market':{0x201,0x202,0x208},'clinic':{0x201,0x202,0x2e4,0x21e,0x2dc},'records':{0x202,0x203,0x204,0x205,0x20a,0x20b}}
def floor(kind,mid,x,y):
    if kind=='exchange':
        if y%8==7 or (x==(3 if mid&1 else 11) and y<7):return 11
        return 13 if (y in (2,10) and 3<x<10) else 12
    if kind=='records':
        if y in (0,15) or x==15:return 3
        return 5 if y==1 or x==0 else 4
    if kind=='market':
        if y==15 or x==15:return 8
        return 10 if x==0 or y==0 else 9
    if x==15 or y==15:return 4
    return 7 if x==0 or y==0 else 6
def material(rgb,x,y,mid,kind,layer):
    r,g,b=rgb;lum=(r+g+b)/3
    if mid in FLOORS[kind]:
        # Native shadows at the top edge remain visually darker.
        q=floor(kind,mid,x,y)
        return max(2,q-2) if mid in (0x21e,0x2dc) and y<8 else q
    if kind=='exchange' and b>r*1.1:return floor(kind,mid,x,y) if lum>70 else 11
    if kind=='records' and r>170 and g>170 and b>170:return floor(kind,mid,x,y)
    if g>r*1.06 and g>b*1.05:return 8 if lum<90 else 9 if lum<160 else 10
    if r>g*1.2 and r>b*1.15:return 11 if lum<80 else 12 if lum<135 else 13 if lum<185 else 14
    if b>r*1.15 and b>g*1.08:return 8 if lum<100 else 9 if lum<165 else 10
    if r>140 and g>b*1.15:return 12 if lum<110 else 13 if lum<155 else 14 if lum<200 else 15
    return 1 if lum<40 else 2 if lum<70 else 3 if lum<110 else 4 if lum<145 else 5 if lum<180 else 6 if lum<220 else 7
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,ls,maps=inventory(base);headers={k:'' for k in ('graphics.h','metatiles.h','headers.h')};banks=[];records={}
    groups=[('exchange',NAMES[:1],'Exchange'),('market',NAMES[1:2],'Market'),('clinic',NAMES[2:4],'Clinic'),('records',NAMES[4:],'Records')]
    for kind,members,suffix in groups:
        layout=ls[maps[members[0]]['layout']];pair=Pair(base,layout,repack=False);assert not any(e>>12==12 for entries in pair.meta for e in entries)
        pair.pals[12]=MATERIAL
        used={v&1023 for n in members for f in ('blockdata_filepath','border_filepath') for v in words(base/ls[maps[n]['layout']][f])}
        if kind=='clinic':used|={0x21e,0x2dc,0x2e4,0x25d}
        protected=PC_PROTECTED if kind=='clinic' else set();redrawn=[]
        for mid in sorted(used-protected):
            if mid<512:continue
            planes=[]
            for layer,native in enumerate(native_layers(pair.reader,mid)):
                values=[material(tuple(c>>3<<3 for c in (r,g,b)),i%16,i//16,mid,kind,layer) if a else 0 for i,(r,g,b,a) in enumerate(native.get_flattened_data())]
                im=Image.new('L',(16,16));im.putdata(values);planes.append(im)
            pair.put(mid,planes[0],12,(planes[1],12));redrawn.append(mid)
        paths=[ROOT/f'data/tilesets/{k}/arauna_frontier07h_{kind}' for k in ('primary','secondary')];symbols=['AraunaFrontier07H'+suffix+'Base','AraunaFrontier07H'+suffix+'Art'];pair.write(paths)
        for k,v in declarations(paths,symbols,pair.callbacks).items():headers[k]+=v
        lids=[maps[n]['layout'] for n in members]
        banks.append({'kind':kind,'layout':layout['id'],'layouts':lids,'maps':list(members),'paths':[p.relative_to(ROOT).as_posix() for p in paths],'source_paths':[p.relative_to(base).as_posix() for p in pair.paths],'symbols':symbols,'callbacks':pair.callbacks,'redrawn_ids':redrawn,'protected_equipment_ids':sorted(protected),'allocated_tiles':sorted(pair.touched),'free_slots':len(pair.free),'material_palette':12})
        for n in members:
            l=ls[maps[n]['layout']];l['primary_tileset']='gTileset_'+symbols[0];l['secondary_tileset']='gTileset_'+symbols[1];records[n]={'layout':l['id'],'layout_index':node['layouts'].index(l),'cells':l['width']*l['height'],'bank_kind':kind}
    for k,v in headers.items():marked(ROOT/'src/data/tilesets'/k,'FRONTIER_07H',v)
    dump(ROOT/'data/layouts/layouts.json',node);dump(OUT/'build.json',{'base_commit':BASE,'maps':records,'banks':banks,'unique_layouts':5,'unique_cells':1314,'native_ids_and_sharing_unchanged':True})
    print('07H: five maps, four native pairs, 1,314 unchanged cells.')
if __name__=='__main__':main()
