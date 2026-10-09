#!/usr/bin/env python3
"""Freeze the cumulative checkpoint and all external Secret Power entrances."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from secret_06c2_common import BASE,GITHUB_BASE,ROOT,OUT,NAMES,MUTABLE,inventory,require_base

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve();require_base(base)
    node,layouts,maps=inventory(base);protected={};dependencies={}
    for rel in subprocess.check_output(['git','ls-files','-z'],cwd=base).decode().rstrip('\0').split('\0'):
        if rel in MUTABLE:continue
        table=protected if rel.split('/')[0] in ('data','src','include','graphics') else dependencies
        table[rel]=hashlib.sha256((base/rel).read_bytes()).hexdigest()
    entrances=[{'map':n,'event':e} for n,m in maps.items() for e in m.get('bg_events',[]) if e.get('type')=='secret_base' or e.get('kind')=='BG_EVENT_SECRET_BASE' or 'secret_base_id' in e]
    contract={'base_commit':BASE,'github_base':GITHUB_BASE,'protected_hashes':protected,'dependency_hashes':dependencies,'original_layout_count':len(node['layouts']),'maps':{n:{'map':maps[n],'layout':layouts[maps[n]['layout']]} for n in NAMES},'external_entrances':entrances,'scope':'8 Tree/Shrub interiors only; 754 existing layout IDs and all map/script/grid/event bytes retained. Two private secondary banks; canonical decoration banks and UI pointers untouched.'}
    OUT.mkdir(parents=True,exist_ok=True);raw=json.dumps(contract,indent=2,sort_keys=True)+'\n';p=OUT/'functional_contract.json'
    if p.exists():assert p.read_text()==raw
    else:p.write_text(raw)
    print(json.dumps({'gameplay_files':len(protected),'other_tracked_dependencies':len(dependencies),'maps':len(NAMES),'external_base_entrances':len(entrances)}))

if __name__=='__main__':main()
