#!/usr/bin/env python3
"""Private Trainer Hill native banks, immutable dynamic floor input and IDs."""
import argparse,copy,json,subprocess
from pathlib import Path
from native_visuals_v2 import Pair,dump,marked,declarations
from trainer_hill_06a_common import BASE,ROOT,OUT,NAMES,ELEVATOR_ID,inventory,floors,runtime_words
from trainer_hill_06a_art import PLAIN,PLINTHS,DOORS_STAIRS,recolor,slab,canvas,barrier,material_planes,family
from render_native_map import words

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve()
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
    node,ls,maps=inventory(base);groups={'pavilion':NAMES[:-1],'elevator':NAMES[-1:]}
    report={'base_commit':BASE,'banks':{},'maps':{},'live_runtime_combinations':16};decl={k:'' for k in ('graphics.h','metatiles.h','headers.h')}
    full_grids={n:words(base/ls[maps[n]['layout']]['blockdata_filepath']) for n in NAMES}
    dynamic=floors(base)
    for key,f in dynamic.items():_,g=runtime_words(base,f);full_grids[key]=g
    for theme,names in groups.items():
        first=ls[maps[names[0]]['layout']];pair=Pair(base,first,repack=True);pair.pals=recolor(pair.pals);redrawn=[];plain=[];planes=[]
        if theme=='pavilion':
            usage={mid:set() for mid in PLAIN|{0x301,0x307,0x330,0x331}}
            for n,g in full_grids.items():
                if n=='TrainerHill_Elevator':continue
                for v in g:
                    if v&1023 in usage:usage[v&1023].add(bool(v&0xc00))
            for mid,status in sorted(usage.items()):
                if status and status=={False}:
                    art=canvas() if mid==0x307 else slab(mid%2,'sand' if mid>=0x301 else family(mid))
                    pair.put(mid,art,12);redrawn.append(mid);plain.append(mid)
            for mid in sorted(PLINTHS|{0x221,0x246}):pair.put(mid,barrier(),12);redrawn.append(mid)
            architectural=set(range(0x301,0x357))|set(range(0x357,0x3d0))
            # Leave programmable counter, stairs and elevator door pixels/palettes
            # exactly native. Black void 0x208 and every puzzle glyph also remain.
            architectural-=set(redrawn)|DOORS_STAIRS
            for mid in sorted(architectural):
                bottom,top=material_planes(pair.reader,mid,roof=mid>=0x357)
                pair.put(mid,bottom,12,(top,12));redrawn.append(mid);planes.append(mid)
            # The inherited outside background is a sky plane, not a wall.
            from PIL import Image
            pair.put(0x380,Image.new('L',(16,16),15),12)
        else:
            used={v&1023 for v in full_grids['TrainerHill_Elevator']}
            for mid in sorted(used):
                if mid in (0x24f,0x257):continue # exit/warp silhouettes
                if mid in (0x25c,0x25d,0x264,0x265):pair.put(mid,slab(mid%2),12);plain.append(mid)
                else:
                    bottom,top=material_planes(pair.reader,mid)
                    pair.put(mid,bottom,12,(top,12));planes.append(mid)
                redrawn.append(mid)
        paths=[ROOT/f'data/tilesets/{kind}/arauna_trainerhill06a_{theme}' for kind in ('primary','secondary')]
        symbols=['AraunaTrainerHill06A'+theme.title()+suffix for suffix in ('Base','Art')]
        pair.write(paths);d=declarations(paths,symbols,pair.callbacks)
        for k,v in d.items():decl[k]+=v
        for n in names:
            before=ls[maps[n]['layout']]
            if n=='TrainerHill_Elevator':
                l=copy.deepcopy(before);l['id']=ELEVATOR_ID;l['name']='AraunaTrainerHill06AElevator_Layout';node['layouts'].append(l)
                m=copy.deepcopy(maps[n]);m['layout']=ELEVATOR_ID;dump(ROOT/f'data/maps/{n}/map.json',m)
            else:l=before
            l['primary_tileset']='gTileset_'+symbols[0];l['secondary_tileset']='gTileset_'+symbols[1]
            report['maps'][n]={'layout':l['id'],'layout_index':node['layouts'].index(l),'theme':theme,'cells':l['width']*l['height'],'immutable_native_word_grid':l['blockdata_filepath']}
        report['banks'][theme]={'paths':[str(p.relative_to(ROOT)) for p in paths],'source_paths':[str(p.relative_to(base)) for p in pair.paths],'symbols':symbols,'callbacks':pair.callbacks,'allocated_tiles':sorted(pair.touched),'redrawn_ids':sorted(set(redrawn)),'plain_ids':plain,'material_plane_ids':planes,'attribute_counts':list(map(len,pair.attrs)),'animation_palettes_unchanged':[7,9]}
    for k,v in decl.items():marked(ROOT/'src/data/tilesets'/k,'TRAINER_HILL_06A',v)
    dump(ROOT/'data/layouts/layouts.json',node);dump(OUT/'build.json',report)
    print(json.dumps({'maps':len(report['maps']),'total_layouts':len(node['layouts']),'banks':{k:{'allocated_tiles':len(v['allocated_tiles']),'redrawn_ids':len(v['redrawn_ids'])} for k,v in report['banks'].items()}}))

if __name__=='__main__':main()
