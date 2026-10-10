#!/usr/bin/env python3
"""Freeze 07H checkpoint before changing three exterior bank pairs."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from frontier_07i_common import BASE,PREVIOUS,ROOT,OUT,NAMES,MUTABLE,inventory,require_base
from native_visuals_v2 import dump

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,ls,maps=inventory(base)
    files=subprocess.check_output(['git','ls-files','-z'],cwd=base).decode().rstrip('\0').split('\0')
    frozen={n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in files if n not in MUTABLE}
    assert subprocess.check_output(['git','rev-parse',BASE+'^'],cwd=base,text=True).strip()==PREVIOUS
    protected=('src/field_door.c','src/overworld.c','src/battle_pyramid.c','src/battle_pyramid_bag.c','src/frontier_util.c','src/fieldmap.c','src/tileset_anims.c','src/field_specials.c','src/apprentice.c','src/trade.c','src/record_mixing.c','src/graphics.c','include/global.h','graphics/battle_frontier/pyramid_floor.pal','include/constants/metatile_labels.h','docs/INTEGRACAO_07G.md','tools/arauna_maps/corrige_agua_palace_07c.py','data/tilesets/secondary/arauna_frontier07c_palace_garden/metatiles.bin')
    data={'base_commit':BASE,'previous_checkpoint':PREVIOUS,'protected_hashes':frozen,'dependency_hashes':{},'layout_count':len(node['layouts']),'maps':{n:{'map':maps[n],'layout':ls[maps[n]['layout']]} for n in NAMES},'explicit_engine_protection':{n:frozen[n] for n in protected},'scope':'Three maps retain three private layouts, every grid, border, object, warp, script, condition, price, reward, dialogue, save and progression. Only three layout bank pairs change. All earlier 44 Frontier maps, Tower doors, Palace water and Pyramid runtime remain frozen.'}
    path=OUT/'functional_contract.json'
    if path.exists():assert json.loads(path.read_text())==data
    else:dump(path,data)
    plan=json.loads((base/'review/frontier_07h/checkpoint_plan.json').read_text());plan.update(base_commit=BASE,completed=47,remaining=0)
    for step in plan['checkpoints']:
        if step['id']=='07I':step['state']='completed'
    plan['notes'].append('07I: three exteriors; doors, flag/water animations, reciprocal edge connections, all progression and earlier 44 maps preserved. Frontier 47/47 art complete; hardware acceptance remains pending.')
    dump(OUT/'checkpoint_plan.json',plan)
    print(json.dumps({'protected_files':len(frozen),'frontier_maps':3,'unique_layouts':3,'layouts':len(node['layouts'])}))

if __name__=='__main__':main()
