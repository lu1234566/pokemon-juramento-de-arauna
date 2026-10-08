#!/usr/bin/env python3
"""03B: draw-only mineral composition around immutable Braille/puzzle blocks."""
from __future__ import annotations
import argparse,collections,hashlib,json,re,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
from native_visuals_v2 import Pair,binary,declarations,dump,marked,ROOT
from render_native_map import words
from script_metatile_dependencies import collect
from build_cavernas_03a import pieces,quantize,ROCK,FLOOR

BASE='7cb02987e896535f8b445290883ff0022a989a52'
NAMES=('SealedChamber_OuterRoom','SealedChamber_InnerRoom','AncientTomb','IslandCave')
OUT=ROOT/'review/cavernas_03b'
REGISTRIES={'data/layouts/layouts.json','src/data/arauna_cave_visuals_v2.h','src/data/tilesets/graphics.h','src/data/tilesets/headers.h','src/data/tilesets/metatiles.h'}
# Closed wall, all six opening pieces, all three inscription blocks, exit stair.
IMMUTABLE={0x229,0x22a,0x22b,0x22c,0x232,0x233,0x234,0x235,0x236,0x237,519}
GROUPS=[('sealed',NAMES[:2],'marine','AraunaSealedChamber03B'),('ancient',(NAMES[2],),'terra','AraunaAncientTomb03B'),('island',(NAMES[3],),'marine','AraunaIslandCave03B')]

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--base',type=Path,required=True);a=ap.parse_args();base=a.base.resolve()
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
    node=json.loads((base/'data/layouts/layouts.json').read_text());layouts={l['id']:l for l in node['layouts']}
    maps={p.parent.name:json.loads(p.read_text()) for p in (base/'data/maps').glob('*/map.json')}
    target_ids={maps[n]['layout'] for n in NAMES}
    for rel in sorted(REGISTRIES):
        current=(ROOT/rel).read_text();original=(base/rel).read_text()
        if rel=='data/layouts/layouts.json':
            c=json.loads(current)
            for l in c['layouts']:
                if l['id'] in target_ids:l['secondary_tileset']='gTileset_Cave'
            assert c==node,('unrelated layout edit',rel)
        elif rel.endswith('arauna_cave_visuals_v2.h'):
            c=re.sub(r'^static const u16 sVisual_(?:'+ '|'.join(NAMES)+r')\[\].*\n','',current,flags=re.M)
            c=re.sub(r'^    \{\d+, sVisual_(?:'+ '|'.join(NAMES)+r')\}.*\n','',c,flags=re.M)
            assert c==original,('unrelated selector header edit',rel)
        else:
            c=re.sub(r'\n*// CAVERNAS_03B_BEGIN\n.*?// CAVERNAS_03B_END\n','\n',current,flags=re.S)
            assert c.rstrip()==original.rstrip(),('unrelated registry edit',rel)
    labels={k:int(v,16) for k,v in re.findall(r'#define (METATILE_\w+)\s+(0x[\da-fA-F]+)',(base/'include/constants/metatile_labels.h').read_text())}
    report={'base_commit':BASE,'maps':{},'banks':{},'art_source':'art/cavernas_03a/minerais_atlas.png','art_sha256':hashlib.sha256((ROOT/'art/cavernas_03a/minerais_atlas.png').read_bytes()).hexdigest(),'immutable_metatiles':sorted(IMMUTABLE)}
    tables=[];decl={k:'' for k in ('graphics.h','metatiles.h','headers.h')}
    for theme,group,family,symbol in GROUPS:
        pair=Pair(base,layouts[maps[group[0]]['layout']]);pair.dynamic.update(range(928,932))
        pair.free=[i for i in pair.free if i>=512 and i not in pair.dynamic]
        pair.tile_cache={raw:i for i,raw in pair.tiles.items() if i>=512 and i not in pair.dynamic and i not in pair.free}
        assert pair.reader._tile(0).tobytes()==bytes(64);pair.tile_cache[bytes(64)]=0
        pair.reserve(base,group,layouts,maps);pair.reserved.update(IMMUTABLE)
        for n in group:pair.reserved.update(collect(base,n,labels)[0])
        rock=list(ROCK[family]);floor=list(FLOOR[family])
        if theme=='ancient':
            rock=[(0,0,0),(24,24,32),(32,32,40),(48,48,56),(64,64,72),(80,80,88),(96,96,104),(120,120,128),(144,144,144),(176,176,168),(48,40,24),(72,56,32),(104,80,48),(144,112,64),(184,152,88),(224,200,128)]
            floor=[(0,0,0),(40,40,40),(56,56,56),(72,72,64),(88,88,80),(104,104,96),(120,120,112),(136,136,128),(152,152,144),(176,176,160),(96,88,64),(120,112,80),(144,136,96),(168,160,120),(192,184,144),(224,216,176)]
        elif theme=='sealed':
            floor=[(0,0,0),(32,48,56),(48,64,72),(64,80,88),(80,96,104),(96,112,120),(112,128,136),(128,144,152),(144,160,168),(168,184,184),(64,96,104),(80,120,128),(104,152,152),(136,184,176),(176,208,192),(224,240,216)]
        else:
            floor=[tuple(min(248,v+8) for v in rgb) if i else rgb for i,rgb in enumerate(floor)]
        pair.pals[7]=rock;pair.pals[9]=floor;pair.pals[12]=[tuple((v//16)*8 for v in rgb) for rgb in rock]
        pair.pals[11]=[(0,0,0),(16,24,32),(32,40,48),(48,56,64),(64,72,80),(88,96,104),(112,120,120),(144,152,144),(176,184,168),(208,216,192),(40,72,80),(64,104,112),(88,144,152),(144,184,184),(184,144,64),(232,208,128)]
        art=pieces(family);old_meta=[list(v) for v in pair.meta]
        entries=lambda mid:old_meta[mid>=512][mid%512*8:mid%512*8+8]
        behavior=lambda mid:pair.attrs[mid>=512][mid%512]&255
        liquid=lambda mid:behavior(mid) in (0x10,0x11,0x12,0x13,0x14,0x15,0x17,0x19)
        for n in group:
            l=layouts[maps[n]['layout']];grid=words(base/l['blockdata_filepath']);w,h=l['width'],l['height'];vis=[];roles=[]
            at=lambda x,y:grid[y*w+x] if 0<=x<w and 0<=y<h else None
            solid=lambda x,y:at(x,y) is not None and bool(at(x,y)&0xc00) and not liquid(at(x,y)&1023)
            event_cells={(e['x'],e['y']) for e in maps[n]['bg_events']}
            warps={(e['x'],e['y']) for e in maps[n]['warp_events']}
            for i,v in enumerate(grid):
                x,y=i%w,i//w;mid=v&1023;role='floor'
                if mid in IMMUTABLE or (x,y) in event_cells or liquid(mid):
                    alias=mid;role='native_braille_or_passage' if not liquid(mid) else 'native_dive_water'
                else:
                    floor_im=art[f'floor{(x//3+y//3)%3}'];out=None
                    if solid(x,y):
                        if not solid(x,y+1):piece='lower' if solid(x,y-1) else 'single'
                        elif not solid(x,y+2):piece='upper'
                        elif not solid(x-1,y):piece='left'
                        elif not solid(x+1,y):piece='right'
                        else:piece='cap'
                        if piece=='cap' and all(solid(x+dx,y+dy) for dx,dy in ((-2,0),(2,0),(0,-2),(0,2))):
                            under=Image.new('L',(16,16),2);d=ImageDraw.Draw(under);d.line((2,5,6,5),fill=3);d.line((6,5,8,7),fill=3);d.line((10,12,14,12),fill=3)
                            out=pair.entries(under,12)+[0]*4;role='bedrock'
                        else:
                            under=Image.new('L',(16,16),3 if piece=='cap' else 5)
                            top=art[piece].copy()
                            # Mineral pockets are confined to rock. They never
                            # occupy the 36 running cells or Flash's center.
                            if piece in ('upper','lower','single') and ((x+2*y)%7==0):
                                d=ImageDraw.Draw(top);d.line((10,5,12,7),fill=13 if theme!='ancient' else 14);d.point((12,8),fill=15)
                            out=pair.entries(under,7)+pair.entries(top,12 if piece=='cap' else 7);role='rock_'+piece
                    else:
                        overlay=Image.new('L',(16,16),0);d=ImageDraw.Draw(overlay)
                        if solid(x,y-1):d.line((0,0,15,1),fill=2)
                        # Broad interior seams establish an ancient stone hall,
                        # while clear center and perimeter remain walking floor.
                        if n=='SealedChamber_InnerRoom' and x in (8,12) and 6<=y<=17:
                            d.line((7,0,7,15),fill=4);role='archive_floor_seam'
                        if theme=='ancient' and y in (5,9,22,28):
                            d.line((0,14,15,14),fill=4);role='stone_course_floor'
                        if (x,y) in warps:
                            d.ellipse((3,10,12,14),fill=8);d.line((5,12,10,12),fill=9);role='exit_floor'
                        out=pair.entries(floor_im,9)+pair.entries(overlay,11)
                    alias=pair.alias(mid,out)
                vis.append(alias);roles.append(role)
            idx=node['layouts'].index(l);tables.append((n,idx,vis));binary(OUT/'visual_grids'/f'{n}.bin',vis)
            l['secondary_tileset']='gTileset_'+symbol
            report['maps'][n]={'layout_index':idx,'cells':len(grid),'visual_alias_cells':sum((v&1023)!=a for v,a in zip(grid,vis)),'roles':dict(collections.Counter(roles)),'role_grid':roles,'secondary':l['secondary_tileset']}
        borderids={v&1023 for n in group for v in words(base/layouts[maps[n]['layout']]['border_filepath'])}
        assert not borderids&IMMUTABLE
        for mid in borderids:pair.put(mid,Image.new('L',(16,16),2),12)
        path=ROOT/f'data/tilesets/secondary/arauna_{theme}_03b';pair.write([pair.paths[0],path],kinds=(1,))
        d=declarations([ROOT/pair.paths[0].relative_to(base),path],['General',symbol],pair.callbacks)
        for k,body in d.items():decl[k]+=body[body.index('const '+('u32 gTilesetTiles_' if k=='graphics.h' else 'u16 gMetatiles_' if k=='metatiles.h' else 'struct Tileset gTileset_')+symbol):]
        report['banks'][theme]={'path':path.relative_to(ROOT).as_posix(),'symbol':symbol,'alias_count':len(pair.alias_cache),'new_static_graphics_slots':sorted(pair.touched),'callbacks':pair.callbacks,'border_ids':sorted(borderids),'unchanged_palette_rows':[6,8,10]}
    for k,body in decl.items():marked(ROOT/'src/data/tilesets'/k,'CAVERNAS_03B',body)
    dump(ROOT/'data/layouts/layouts.json',node)
    header=(base/'src/data/arauna_cave_visuals_v2.h').read_text()
    definitions=''.join(f'static const u16 sVisual_{n}[] = INCBIN_U16("review/cavernas_03b/visual_grids/{n}.bin");\n' for n,idx,g in tables)
    header=header.replace('static const struct CaveVisualGrid sCaveVisualGrids[] =',definitions+'static const struct CaveVisualGrid sCaveVisualGrids[] =')
    pos=header.rfind('};');header=header[:pos]+''.join(f'    {{{idx}, sVisual_{n}}}, // {n} checkpoint 03B\n' for n,idx,g in tables)+header[pos:]
    (ROOT/'src/data/arauna_cave_visuals_v2.h').write_text(header);dump(OUT/'build.json',report)
    print(json.dumps({'maps':len(tables),'banks':{k:{f:v for f,v in b.items() if f in ('alias_count','new_static_graphics_slots')} for k,b in report['banks'].items()}},indent=2))
if __name__=='__main__':main()
