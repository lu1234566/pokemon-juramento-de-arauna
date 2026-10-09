#!/usr/bin/env python3
"""Freeze every tracked dependency before drawing, including curtain and gameplay code."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from frontier_07e_common import BASE,PREVIOUS,ROOT,OUT,NAMES,MUTABLE,inventory,door_records,curtain_ids,require_base
from native_visuals_v2 import dump

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,ls,maps=inventory(base)
    files=subprocess.check_output(['git','ls-files','-z'],cwd=base).decode().rstrip('\0').split('\0')
    frozen={n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in files if n not in MUTABLE}
    assert subprocess.check_output(['git','rev-parse',BASE+'^'],cwd=base,text=True).strip()==PREVIOUS
    protected=('src/field_door.c','src/overworld.c','src/field_specials.c','src/battle_pike.c','src/frontier_util.c','src/tileset_anims.c','include/constants/metatile_labels.h','include/constants/battle_pike.h','docs/INTEGRACAO_07D.md','docs/INTEGRACAO_07C.md','tools/arauna_maps/corrige_agua_palace_07c.py','data/tilesets/secondary/arauna_frontier07c_palace_garden/metatiles.bin')
    data={'base_commit':BASE,'previous_checkpoint':PREVIOUS,'protected_hashes':frozen,'dependency_hashes':{},'layout_count':len(node['layouts']),'maps':{n:{'map':maps[n],'layout':ls[maps[n]['layout']]} for n in NAMES},'doors':door_records(base),'curtain_ids':curtain_ids(base),'explicit_engine_protection':{n:frozen[n] for n in protected},'scope':'Six Pike maps only. Dynamic curtain metatile IDs/attributes, room RNG and hints, status, healing, wild encounters, party selection, level modes, battles, Lucy, saves, rewards, movements, scripts, events, warps, map grids and collision remain exact. Previous 20 Frontier maps, Tower doors, Palace water and official 07D integration are frozen.'}
    path=OUT/'functional_contract.json'
    if path.exists():assert json.loads(path.read_text())==data,'Contract differs'
    else:dump(path,data)
    print(json.dumps({'protected_files':len(frozen),'maps':len(NAMES),'layouts':len(node['layouts']),'curtain_metatiles':len(data['curtain_ids'])}))

if __name__=='__main__':main()
