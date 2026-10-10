#!/usr/bin/env python3
"""Weathered stone terraces, terracotta and bronze facades, olive greenery."""
import argparse,json
from functools import lru_cache
from pathlib import Path
from PIL import Image
from native_visuals_v2 import Pair,dump,marked,declarations
from frontier_07i_common import ROOT,BASE,OUT,NAMES,inventory,require_base,door_records
from trainer_hill_06a_art import native_layers
from render_native_map import words
PATHS={0x23,0x100,0x101,0x102,0x108,0x109,0x10a,0x110,0x111,0x112}
@lru_cache(None)
def nearest(rgb,colors):
    k=min(range(1,16),key=lambda k:sum((rgb[c]-colors[k][c])**2 for c in range(3)))
    return k,sum((rgb[c]-colors[k][c])**2 for c in range(3))
def entry(pair,im,pal):
    variants=[(im,0),(im.transpose(Image.Transpose.FLIP_LEFT_RIGHT),0x400),(im.transpose(Image.Transpose.FLIP_TOP_BOTTOM),0x800),(im.transpose(Image.Transpose.FLIP_LEFT_RIGHT).transpose(Image.Transpose.FLIP_TOP_BOTTOM),0xc00)]
    for shape,flag in variants:
        if shape.tobytes() in pair.tile_cache:return pair.tile_cache[shape.tobytes()]|flag|pal<<12
    shape,flag=min(variants,key=lambda p:p[0].tobytes());return pair.tile(shape)|flag|pal<<12
def desired(rgb,x,y,mid):
    r,g,b=rgb;lum=(r+g+b)/3
    if g>r*1.08 and g>b*.95:
        if mid==1:
            return (144,216,152) if (x,y) in ((2,3),(3,2),(11,10),(12,9)) else (112,192,144)
        return (int(r*.96),int(g*.98),int(b*.92))
    if 0x70<=mid<=0xaf and r>=g*.94:
        return (min(248,r+32),min(240,g+24),min(216,b+16))
    if mid in PATHS or 0x3b0<=mid<=0x3df:
        if lum>105 and b>=r*.92:
            q=185 if y in (0,8) else 142 if y in (7,15) or x==(3 if y<8 else 11) else 172
            return (q,int(q*.91),int(q*.76))
    if r>g*1.2 and r>b*1.16:return (int(lum*1.12),int(lum*.68),int(lum*.40))
    if b>r*1.1 and b>g*1.04:return (int(lum*.67),int(lum*.84),int(lum*.61))
    if r>130 and g>b*1.2:return (int(lum*1.10),int(lum*.81),int(lum*.49))
    return (int(lum*.99),int(lum*.91),int(lum*.77))
def replace(pair,mid):
    entries=[]
    for native in native_layers(pair.reader,mid):
        for x,y in ((0,0),(8,0),(0,8),(8,8)):
            cells=list(native.crop((x,y,x+8,y+8)).get_flattened_data());targets=[desired(tuple(c>>3<<3 for c in (r,g,b)),x+i%8,y+i//8,mid) if a else None for i,(r,g,b,a) in enumerate(cells)]
            # Per-quadrant choice keeps vegetation in its native green palette.
            candidates=[]
            for pal in (2,12):
                values=[];cost=0
                for rgb in targets:
                    if rgb is None:values.append(0);continue
                    best,error=nearest(rgb,tuple(tuple(c>>3<<3 for c in color) for color in pair.pals[pal]));values.append(best);cost+=error
                candidates.append((cost,pal,values))
            _,pal,values=min(candidates,key=lambda d:d[0]);im=Image.new('L',(8,8));im.putdata(values);entries.append(entry(pair,im,pal))
    pair.meta[mid>=512][mid%512*8:mid%512*8+8]=entries
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,ls,ms=inventory(base);doors=door_records(base);records={};banks=[];headers={k:'' for k in ('graphics.h','metatiles.h','headers.h')}
    common_primary={v&1023 for n in NAMES[:2] for f in ('blockdata_filepath','border_filepath') for v in words(base/ls[ms[n]['layout']][f]) if v&1023<512}
    source_pal12=Pair(base,ls[ms[NAMES[0]]['layout']]).pals[12]
    for kind,n in zip(('east','west','gate'),NAMES):
        l=ls[ms[n]['layout']];pair=Pair(base,l);pair.dynamic.update(range(730,736));pair.pals[12]=source_pal12
        used={v&1023 for f in ('blockdata_filepath','border_filepath') for v in words(base/l[f])};used|=common_primary if kind!='gate' else set()
        protected={d[k] for d in doors if d['map']==n for k in ('id','upper_id')}
        protected|={d[k] for d in doors for k in ('id','upper_id') if d[k]<512}
        animated={mid for mid in used if any((e&1023) in pair.dynamic for e in pair.meta[mid>=512][mid%512*8:mid%512*8+8])}
        redraw=used-protected-animated-{0}
        # Reclaim only static tiles referenced exclusively by the redrawn IDs.
        retained=set(pair.dynamic)|{0}
        for bank,entries in enumerate(pair.meta):
            for j,e in enumerate(entries):
                mid=bank*512+j//8
                if mid not in redraw:retained.add(e&1023)
        reclaim={i for i in pair.tiles if i not in retained and i not in pair.dynamic};pair.free=sorted((set(pair.free)|reclaim)-pair.dynamic)
        for i in reclaim:pair.tiles.pop(i)
        pair.tile_cache={raw:i for i,raw in pair.tiles.items() if i not in pair.dynamic}
        for mid in sorted(redraw):
            try:replace(pair,mid)
            except AssertionError as exc:raise AssertionError((kind,hex(mid),'allocated',len(pair.touched),'reclaimed',len(reclaim))) from exc
        paths=[ROOT/f'data/tilesets/{k}/arauna_frontier07i_{kind}' for k in ('primary','secondary')];suffix=kind.title();symbols=['AraunaFrontier07I'+suffix+'Base','AraunaFrontier07I'+suffix+'Art'];pair.write(paths)
        for k,v in declarations(paths,symbols,pair.callbacks).items():headers[k]+=v
        banks.append({'kind':kind,'layout':l['id'],'layouts':[l['id']],'maps':[n],'paths':[p.relative_to(ROOT).as_posix() for p in paths],'source_paths':[p.relative_to(base).as_posix() for p in pair.paths],'symbols':symbols,'callbacks':pair.callbacks,'redrawn_ids':sorted(redraw),'protected_door_ids':sorted(protected),'animated_ids':sorted(animated),'allocated_tiles':sorted(pair.touched),'free_slots':len(pair.free),'material_palette':12,'source_palettes_exact':kind!='gate','reclaimed_static_slots':len(reclaim)})
        l['primary_tileset']='gTileset_'+symbols[0];l['secondary_tileset']='gTileset_'+symbols[1];records[n]={'layout':l['id'],'layout_index':node['layouts'].index(l),'cells':l['width']*l['height'],'bank_kind':kind}
        print(kind,'redrawn',len(redraw),'allocated',len(pair.touched),'free',len(pair.free),flush=True)
    for k,v in headers.items():marked(ROOT/'src/data/tilesets'/k,'FRONTIER_07I',v)
    dump(ROOT/'data/layouts/layouts.json',node);dump(OUT/'build.json',{'base_commit':BASE,'maps':records,'banks':banks,'unique_layouts':3,'unique_cells':9342,'doors':doors,'native_ids_and_sharing_unchanged':True})
if __name__=='__main__':main()
