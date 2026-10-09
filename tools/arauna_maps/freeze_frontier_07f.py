#!/usr/bin/env python3
"""Freeze the exact official Pike integration before changing Pyramid art."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from frontier_07f_common import BASE,PREVIOUS,ROOT,OUT,NAMES,SQUARES,MUTABLE,inventory,require_base
from native_visuals_v2 import dump

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,ls,maps=inventory(base)
    files=subprocess.check_output(['git','ls-files','-z'],cwd=base).decode().rstrip('\0').split('\0')
    frozen={n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in files if n not in MUTABLE}
    assert subprocess.check_output(['git','rev-parse',BASE+'^'],cwd=base,text=True).strip()==PREVIOUS
    protected=('src/field_door.c','src/overworld.c','src/battle_pyramid.c','src/battle_pyramid_bag.c','src/frontier_util.c','src/fieldmap.c','src/tileset_anims.c','src/graphics.c','graphics/battle_frontier/pyramid_floor.pal','include/constants/metatile_labels.h','include/constants/battle_pyramid.h','docs/INTEGRACAO_07E.md','tools/arauna_maps/corrige_agua_palace_07c.py','data/tilesets/secondary/arauna_frontier07c_palace_garden/metatiles.bin')
    data={'base_commit':BASE,'previous_checkpoint':PREVIOUS,'protected_hashes':frozen,'dependency_hashes':{},'layout_count':len(node['layouts']),'maps':{n:{'map':maps[n],'layout':ls[maps[n]['layout']]} for n in NAMES+SQUARES},'explicit_engine_protection':{n:frozen[n] for n in protected},'scope':'Three Frontier maps. All sixteen 8x8 source modules remain exact including their original bank references. Runtime Floor uses the private pair with the same metatile IDs. Generator, seeds, entrance/exit positions, items, trainers, light, seven palettes, bag, saves and progression are frozen, as are the previous 26 Frontier maps.'}
    path=OUT/'functional_contract.json'
    if path.exists():assert json.loads(path.read_text())==data
    else:dump(path,data)
    print(json.dumps({'protected_files':len(frozen),'frontier_maps':3,'source_modules':16,'layouts':len(node['layouts'])}))

if __name__=='__main__':main()
