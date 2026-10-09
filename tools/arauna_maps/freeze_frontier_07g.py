#!/usr/bin/env python3
"""Freeze official 07F integration before changing three shared interior banks."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from frontier_07g_common import BASE,PREVIOUS,ROOT,OUT,NAMES,MUTABLE,inventory,require_base
from native_visuals_v2 import dump

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,ls,maps=inventory(base)
    files=subprocess.check_output(['git','ls-files','-z'],cwd=base).decode().rstrip('\0').split('\0')
    frozen={n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in files if n not in MUTABLE}
    assert subprocess.check_output(['git','rev-parse',BASE+'^'],cwd=base,text=True).strip()==PREVIOUS
    protected=('src/field_door.c','src/overworld.c','src/battle_pyramid.c','src/battle_pyramid_bag.c','src/frontier_util.c','src/fieldmap.c','src/tileset_anims.c','src/field_specials.c','src/apprentice.c','src/trade.c','src/record_mixing.c','src/graphics.c','include/global.h','graphics/battle_frontier/pyramid_floor.pal','include/constants/metatile_labels.h','docs/INTEGRACAO_07F.md','tools/arauna_maps/corrige_agua_palace_07c.py','data/tilesets/secondary/arauna_frontier07c_palace_garden/metatiles.bin')
    data={'base_commit':BASE,'previous_checkpoint':PREVIOUS,'protected_hashes':frozen,'dependency_hashes':{},'layout_count':len(node['layouts']),'maps':{n:{'map':maps[n],'layout':ls[maps[n]['layout']]} for n in NAMES},'explicit_engine_protection':{n:frozen[n] for n in protected},'scope':'Ten maps retain three shared layouts, every grid, border, object, warp, script, condition, price, reward, dialogue, save and progression. Only three layout bank pairs change. All earlier 29 Frontier maps, Tower doors, Palace water and Pyramid runtime remain frozen.'}
    path=OUT/'functional_contract.json'
    if path.exists():assert json.loads(path.read_text())==data
    else:dump(path,data)
    plan=json.loads((base/'review/frontier_07f/checkpoint_plan.json').read_text());plan.update(base_commit=BASE,completed=39,remaining=8)
    for step in plan['checkpoints']:
        if step['id']=='07G':step['state']='completed'
    plan['notes'].append('07G: ten maps retain three shared layouts; private 4bpp banks preserve original Building TV animation, services, apprentice, Scott rewards and all earlier maps.')
    dump(OUT/'checkpoint_plan.json',plan)
    print(json.dumps({'protected_files':len(frozen),'frontier_maps':10,'shared_layouts':3,'layouts':len(node['layouts'])}))

if __name__=='__main__':main()
