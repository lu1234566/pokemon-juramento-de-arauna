#!/usr/bin/env python3
"""Private indexed banks and layout-only copies; native map words stay intact."""
import argparse,copy,json,subprocess
from pathlib import Path
from native_visuals_v2 import dump,marked,declarations
from render_native_map import words
from navel_06b_common import BASE,ROOT,OUT,NAMES,GROUPS,COPIES,inventory
from navel_06b_art import NavelPair,palettes,planes

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve()
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
    node,ls,maps=inventory(base);originals=copy.deepcopy(ls);copies={};decl={k:'' for k in ('graphics.h','metatiles.h','headers.h')};report={'base_commit':BASE,'banks':{},'maps':{},'appended_layouts':[]}
    for theme,names in GROUPS.items():
        first=originals[maps[names[0]]['layout']];pair=NavelPair(base,first);pair.pals=palettes(pair.pals,theme)
        used=sorted({v&1023 for n in names for f in ('blockdata_filepath','border_filepath') for v in words(base/originals[maps[n]['layout']][f])});redrawn=[];floors=[];layers=[];usage={}
        for n in names:
            for v in words(base/originals[maps[n]['layout']]['blockdata_filepath']):usage.setdefault(v&1023,set()).add(bool(v&0xc00))
        for mid in used:
            # Water and shore animation graphics retain their native references.
            # Shore/sea in General are recolored through the private palettes.
            if mid<512 and theme not in ('coast','dock'):continue
            if mid<512 and mid not in set(range(0x70,0xb0))|{0xbf,0xcf,0x121,0xe2,0x189}:continue
            if theme=='summit' and mid==0x33c:continue # open sky
            floor=mid in ({0x121} if theme=='coast' else {0x3a1,0x3a0} if theme=='dock' else {0x201,0x35c,0x364}) and usage.get(mid)=={False}
            wood=(theme=='dock' and mid in (0x3a0,0x3a1,0x3c1,0x3c5)) or (theme=='coast' and mid==0x189)
            ladder=mid in (0x204,0x207,0x20f,0x217,0x23f,0x2dc,0x373,0x37b,0x383,0x38b,0x3a3,0x3a4,0x3ab,0x3ac)
            if mid==0x201 and theme=='dock':continue # native black void
            bottom,top=planes(pair.reader,mid,theme,floor=floor,wood=wood,ladder=ladder,rim=mid==0x247)
            pair.put(mid,bottom,12,(top,12));redrawn.append(mid);layers.append(mid)
            if floor and not wood:floors.append(mid)
        paths=[ROOT/f'data/tilesets/{kind}/arauna_navel06b_{theme}' for kind in ('primary','secondary')];symbols=['AraunaNavel06B'+theme.title()+suffix for suffix in ('Base','Art')]
        pair.write(paths);d=declarations(paths,symbols,pair.callbacks)
        for k,v in d.items():decl[k]+=v
        for n in names:
            old=originals[maps[n]['layout']]
            if n in COPIES:
                lid=COPIES[n]
                if lid not in copies:
                    l=copy.deepcopy(old);l['id']=lid;l['name']=lid.removeprefix('LAYOUT_').title().replace('_','')+'_Layout';copies[lid]=l;node['layouts'].append(l);report['appended_layouts'].append(lid)
                l=copies[lid];m=copy.deepcopy(maps[n]);m['layout']=lid;dump(ROOT/f'data/maps/{n}/map.json',m)
            else:l=ls[maps[n]['layout']]
            l['primary_tileset']='gTileset_'+symbols[0];l['secondary_tileset']='gTileset_'+symbols[1]
            report['maps'][n]={'layout':l['id'],'source_layout':old['id'],'layout_index':node['layouts'].index(l),'theme':theme,'cells':l['width']*l['height'],'native_grid':old['blockdata_filepath']}
        report['banks'][theme]={'paths':[str(p.relative_to(ROOT)) for p in paths],'source_paths':[str(p.relative_to(base)) for p in pair.paths],'symbols':symbols,'callbacks':pair.callbacks,'reserved_animation_tiles':sorted(pair.dynamic),'allocated_tiles':sorted(pair.touched),'redrawn_ids':redrawn,'plain_floor_ids':floors,'layer_mask_ids':layers}
    for k,v in decl.items():marked(ROOT/'src/data/tilesets'/k,'NAVEL_ROCK_06B',v)
    dump(ROOT/'data/layouts/layouts.json',node);dump(OUT/'build.json',report)
    print(json.dumps({'maps':len(NAMES),'core_maps':21,'private_harbor':1,'banks':len(report['banks'])*2,'layouts':len(node['layouts']),'appended':len(copies)}))
if __name__=='__main__':main()
