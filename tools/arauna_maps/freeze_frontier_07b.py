#!/usr/bin/env python3
"""Freeze every tracked dependency, including both requested engine fixes."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from frontier_07b_common import BASE,PREVIOUS,ROOT,OUT,NAMES,MUTABLE,inventory,door_records,require_base
from native_visuals_v2 import dump

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,ls,maps=inventory(base);files=subprocess.check_output(['git','ls-files','-z'],cwd=base).decode().rstrip('\0').split('\0')
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    # All existing review assets, tools and concepts are dependencies as well.
    frozen={n:sha(base/n) for n in files if n not in MUTABLE}
    assert subprocess.run(['git','merge-base','--is-ancestor',PREVIOUS,BASE],cwd=base).returncode==0
    data={'base_commit':BASE,'previous_checkpoint':PREVIOUS,'protected_hashes':frozen,'dependency_hashes':{},'layout_count':len(node['layouts']),'maps':{n:{'map':maps[n],'layout':ls[maps[n]['layout']]} for n in NAMES},'doors':door_records(base),'explicit_engine_protection':{n:frozen[n] for n in ('src/field_door.c','src/overworld.c')},'scope':'Four Battle Dome maps; four existing layouts only change the bank pair. No appended layout, map header, grid, border, collision, script, event, warp, trainer, reward, Dome tournament or engine changes.'}
    p=OUT/'functional_contract.json'
    if p.exists():assert json.loads(p.read_text())==data,'Contract differs'
    else:dump(p,data)
    print(json.dumps({'protected_files':len(frozen),'maps':len(NAMES),'layouts':len(node['layouts']),'engine':data['explicit_engine_protection']}))

if __name__=='__main__':main()
