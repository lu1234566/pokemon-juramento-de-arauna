#!/usr/bin/env python3
"""03C plus 03B V1.1 over the integrator's corrected base, draw-only."""
import argparse,collections,hashlib,json,re,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
from native_visuals_v2 import ROOT,Pair,binary,dump,declarations,marked
from build_cavernas_03a import pieces,ROCK,FLOOR
from render_native_map import words
from script_metatile_dependencies import collect
from cavernas_03c_art import safe_pair,install_landmarks,DOOR_IDS
BASE='4410ced6384b1d71dfa562d4bb5a2486ebc01e22'
NAMES=('AlteringCave','ArtisanCave_B1F','ArtisanCave_1F')
BNAMES=('SealedChamber_OuterRoom','SealedChamber_InnerRoom','AncientTomb','IslandCave')
ALLNAMES=NAMES+BNAMES
OUT=ROOT/'review/cavernas_03c'
REGISTRIES={'data/layouts/layouts.json','src/data/arauna_cave_visuals_v2.h','src/data/tilesets/graphics.h','src/data/tilesets/headers.h','src/data/tilesets/metatiles.h'}
GROUPS=[('altering',(NAMES[0],),'marine','AraunaAlteringCave03C'),('artisan',NAMES[1:],'terra','AraunaArtisanCave03C'),('sealed',BNAMES[:2],'marine','AraunaSealedChamber03BV11'),('ancient',(BNAMES[2],),'terra','AraunaAncientTomb03BV11'),('island',(BNAMES[3],),'marine','AraunaIslandCave03BV11')]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);a=ap.parse_args();base=a.base.resolve()
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
    node=json.loads((base/'data/layouts/layouts.json').read_text());ls={l['id']:l for l in node['layouts']}
    maps={n:json.loads((base/f'data/maps/{n}/map.json').read_text()) for n in ALLNAMES}
    for rel in REGISTRIES:
        old=(base/rel).read_text();now=(ROOT/rel).read_text()
        if rel.endswith('layouts.json'):
            current=json.loads(now)
            for l in current['layouts']:
                if l['id'] in {maps[n]['layout'] for n in ALLNAMES}:l['secondary_tileset']=ls[l['id']]['secondary_tileset']
            assert current==node,'Unrelated layout edits'
        elif rel.endswith('arauna_cave_visuals_v2.h'):
            stripped=now
            for name in BNAMES:stripped=stripped.replace(f'review/cavernas_03c/03b_v11_visual_grids/{name}.bin',f'review/cavernas_03b/visual_grids/{name}.bin')
            stripped=re.sub(r'^static const u16 sVisual_(?:'+ '|'.join(NAMES)+r')\[\].*\n','',stripped,flags=re.M)
            stripped=re.sub(r'^    \{\d+, sVisual_(?:'+ '|'.join(NAMES)+r')\}.*\n','',stripped,flags=re.M);assert stripped==old
        else:
            stripped=re.sub(r'\n*// CAVERNAS_03C_BEGIN\n.*?// CAVERNAS_03C_END\n','\n',now,flags=re.S);assert stripped.rstrip()==old.rstrip()
    labels={k:int(v,16) for k,v in re.findall(r'#define (METATILE_\w+)\s+(0x[\da-fA-F]+)',(base/'include/constants/metatile_labels.h').read_text())}
    report={'base_commit':BASE,'maps':{},'banks':{},'atlas_sha256':hashlib.sha256((base/'art/cavernas_03a/minerais_atlas.png').read_bytes()).hexdigest()};tables=[];decl={k:'' for k in ('graphics.h','metatiles.h','headers.h')}
    for theme,group,family,symbol in GROUPS:
        l=ls[maps[group[0]]['layout']];p=Pair(base,l);safe_pair(p);p.reserve(base,group,ls,maps)
        for n in group:p.reserved.update(collect(base,n,labels)[0])
        puzzle=group[0] in BNAMES
        if not puzzle:
            p.pals[7]=list(ROCK[family]);p.pals[9]=list(FLOOR[family]);p.pals[12]=[tuple((v//16)*8 for v in rgb) for rgb in ROCK[family]]
            p.pals[11]=[(0,0,0),(16,24,32),(32,40,48),(48,56,64),(64,72,80),(88,96,104),(112,120,120),(144,152,144),(176,184,168),(208,216,192),(40,72,80),(64,104,112),(88,144,152),(144,184,184),(184,144,64),(232,208,128)]
            if theme=='altering':
                p.pals[7]=[(0,0,0),(24,24,40),(32,32,48),(48,48,64),(64,64,80),(80,80,96),(104,104,120),(128,128,144),(152,152,168),(192,192,200),(40,48,72),(56,72,104),(80,104,144),(112,144,184),(168,192,224),(216,232,240)]
                p.pals[9]=[(0,0,0),(48,48,64),(64,64,80),(80,80,96),(96,96,112),(112,112,128),(128,128,144),(144,144,160),(160,160,176),(184,184,192),(64,88,104),(88,112,136),(120,152,176),(160,184,208),(192,216,232),(232,240,248)]
                p.pals[12]=[tuple((v//16)*8 for v in rgb) for rgb in p.pals[7]]
            else:
                p.pals[7]=[(0,0,0),(32,32,32),(48,48,48),(64,64,64),(80,80,80),(96,96,88),(120,120,104),(144,144,120),(168,168,144),(200,200,176),(64,48,32),(96,72,40),(128,104,64),(168,144,88),(200,184,128),(232,224,176)]
                p.pals[9]=[(0,0,0),(56,56,48),(72,72,64),(88,88,80),(104,104,96),(120,120,112),(136,136,120),(152,152,136),(176,176,152),(200,200,176),(104,88,64),(128,112,80),(152,136,96),(176,160,120),(208,192,152),(240,232,184)]
                p.pals[12]=[tuple((v//16)*8 for v in rgb) for rgb in p.pals[7]]
        exit_ids=(741,742,743) if theme=='sealed' else (600,601,602)
        targets=set(DOOR_IDS if puzzle else (572,535,575))|set(exit_ids);p.reserved.update(targets)
        landmarks=install_landmarks(p,family,exit_ids,puzzle);art=pieces(family)
        for n in group:
            l=ls[maps[n]['layout']];g=words(base/l['blockdata_filepath']);w,h=l['width'],l['height']
            if puzzle:
                vis=words(base/f'review/cavernas_03b/visual_grids/{n}.bin');roles=['existing_03b_visual']*len(g)
                for i,v in enumerate(g):
                    if v&1023 in exit_ids:vis[i]=v&1023;roles[i]='native_south_exit'
                binary(OUT/'03b_v11_visual_grids'/f'{n}.bin',vis)
            else:
                vis=[];roles=[];at=lambda x,y:g[y*w+x] if 0<=x<w and 0<=y<h else None
                solid=lambda x,y:at(x,y) is not None and bool(at(x,y)&0xc00)
                for i,v in enumerate(g):
                    x,y=i%w,i//w;mid=v&1023;role='floor';out=None
                    if mid in targets:alias=mid;role='native_exit_or_ladder'
                    elif mid==516:
                        top=Image.new('L',(16,16),0);d=ImageDraw.Draw(top)
                        for yy in (5,9,13):d.line((1,yy,14,yy),fill=7);d.line((1,yy+1,14,yy+1),fill=3)
                        out=p.entries(art['floor0'],9)+p.entries(top,11);role='ledge_steps';alias=p.alias(mid,out)
                    elif mid==515:
                        out=p.entries(art['floor0'],9)+p.entries(art['outcrop'],7);role='boulder';alias=p.alias(mid,out)
                    elif solid(x,y):
                        if not solid(x,y+1):piece='lower' if solid(x,y-1) else 'single'
                        elif not solid(x,y+2):piece='upper'
                        elif not solid(x-1,y):piece='left'
                        elif not solid(x+1,y):piece='right'
                        else:piece='cap'
                        if piece=='cap' and all(solid(x+dx,y+dy) for dx,dy in ((-2,0),(2,0),(0,-2),(0,2))):
                            im=Image.new('L',(16,16),2);d=ImageDraw.Draw(im);d.line((3,5,7,5,9,7),fill=3);d.line((10,12,14,12),fill=3);out=p.entries(im,12)+[0]*4;role='bedrock'
                        else:
                            out=p.entries(Image.new('L',(16,16),3 if piece=='cap' else 5),7)+p.entries(art[piece],12 if piece=='cap' else 7);role='rock_'+piece
                        alias=p.alias(mid,out)
                    else:
                        top=Image.new('L',(16,16),0);d=ImageDraw.Draw(top)
                        if solid(x,y-1):d.line((0,0,15,1),fill=2)
                        # Pigment seams stay on ground; raised ledge tops remain
                        # ground even when the native ID elsewhere is a wall.
                        if theme=='artisan' and x%9==4 and y%5==2:d.line((4,5,8,5),fill=14)
                        out=p.entries(art[f'floor{(x//3+y//3)%3}'],9)+p.entries(top,11);alias=p.alias(mid,out)
                    vis.append(alias);roles.append(role)
                idx=node['layouts'].index(l);tables.append((n,idx,vis));binary(OUT/'visual_grids'/f'{n}.bin',vis)
            l['secondary_tileset']='gTileset_'+symbol
            report['maps'][n]={'layout_index':node['layouts'].index(l),'cells':len(g),'secondary':l['secondary_tileset'],'visual_grid':f'review/cavernas_03c/03b_v11_visual_grids/{n}.bin' if puzzle else f'review/cavernas_03c/visual_grids/{n}.bin','roles':dict(collections.Counter(roles)),'role_grid':roles,'stage':'03B V1.1' if puzzle else '03C'}
        if not puzzle:
            for mid in {v&1023 for n in group for v in words(base/ls[maps[n]['layout']]['border_filepath'])}:p.put(mid,Image.new('L',(16,16),2),12)
        path=ROOT/f'data/tilesets/secondary/arauna_{theme}_03b_v11' if puzzle else ROOT/f'data/tilesets/secondary/arauna_{theme}_03c'
        p.write([p.paths[0],path],kinds=(1,));d=declarations([ROOT/p.paths[0].relative_to(base),path],['General',symbol],p.callbacks)
        for k,body in d.items():decl[k]+=body[body.index('const '+('u32 gTilesetTiles_' if k=='graphics.h' else 'u16 gMetatiles_' if k=='metatiles.h' else 'struct Tileset gTileset_')+symbol):]
        report['banks'][theme]={'path':path.relative_to(ROOT).as_posix(),'symbol':symbol,'source_secondary':p.paths[1].relative_to(base).as_posix(),'new_static_graphics_slots':sorted(p.touched),'alias_count':len(p.alias_cache),'callbacks':p.callbacks,'landmarks':landmarks,'stage':'03B V1.1' if puzzle else '03C'}
    for k,body in decl.items():marked(ROOT/'src/data/tilesets'/k,'CAVERNAS_03C',body)
    dump(ROOT/'data/layouts/layouts.json',node)
    header=(base/'src/data/arauna_cave_visuals_v2.h').read_text()
    for name in BNAMES:header=header.replace(f'review/cavernas_03b/visual_grids/{name}.bin',f'review/cavernas_03c/03b_v11_visual_grids/{name}.bin')
    defs=''.join(f'static const u16 sVisual_{n}[] = INCBIN_U16("review/cavernas_03c/visual_grids/{n}.bin");\n' for n,idx,g in tables)
    header=header.replace('static const struct CaveVisualGrid sCaveVisualGrids[] =',defs+'static const struct CaveVisualGrid sCaveVisualGrids[] =');pos=header.rfind('};');header=header[:pos]+''.join(f'    {{{idx}, sVisual_{n}}}, // {n} checkpoint 03C\n' for n,idx,g in tables)+header[pos:]
    (ROOT/'src/data/arauna_cave_visuals_v2.h').write_text(header);dump(OUT/'build.json',report)
    print(json.dumps({'maps':len(report['maps']),'new_selector_cases':len(tables),'banks':{k:{'new_tiles':len(v['new_static_graphics_slots']),'aliases':v['alias_count'],'stage':v['stage']} for k,v in report['banks'].items()}},indent=2))
if __name__=='__main__':main()
