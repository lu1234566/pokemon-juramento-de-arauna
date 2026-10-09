#!/usr/bin/env python3
"""Freeze every existing dependency including the integrated Palace water fix."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from frontier_07d_common import BASE,PREVIOUS,ROOT,OUT,NAMES,MUTABLE,inventory,door_records,require_base
from native_visuals_v2 import dump

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,ls,maps=inventory(base);files=subprocess.check_output(['git','ls-files','-z'],cwd=base).decode().rstrip('\0').split('\0')
    frozen={n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in files if n not in MUTABLE}
    assert subprocess.run(['git','merge-base','--is-ancestor',PREVIOUS,BASE],cwd=base).returncode==0
    protected=('src/field_door.c','src/overworld.c','src/battle_factory.c','src/battle_factory_screen.c','data/tilesets/secondary/arauna_frontier07c_palace_garden/metatiles.bin','docs/INTEGRACAO_07C.md','tools/arauna_maps/corrige_agua_palace_07c.py')
    data={'base_commit':BASE,'previous_checkpoint':PREVIOUS,'protected_hashes':frozen,'dependency_hashes':{},'layout_count':len(node['layouts']),'maps':{n:{'map':maps[n],'layout':ls[maps[n]['layout']]} for n in NAMES},'doors':door_records(base),'explicit_engine_protection':{n:frozen[n] for n in protected},'scope':'Three Battle Factory rooms; only private bank references change in three existing layouts. Rental selection, swapping, level modes, trainer generation, battles, Noland, saves, rewards, scripts, objects, warps and collision remain exact. Official 07C water fix and previous door fixes are protected.'}
    p=OUT/'functional_contract.json'
    if p.exists():assert json.loads(p.read_text())==data,'Contract differs'
    else:dump(p,data)
    print(json.dumps({'protected_files':len(frozen),'maps':len(NAMES),'layouts':len(node['layouts']),'explicit_protection':data['explicit_engine_protection']}))

if __name__=='__main__':main()
