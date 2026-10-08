#!/usr/bin/env python3
"""Freeze every existing tracked dependency before editing Navel Rock art."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from navel_06b_common import BASE,GITHUB_BASE,ROOT,OUT,NAMES,MUTABLE,inventory

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve()
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
    node,ls,maps=inventory(base);files=subprocess.check_output(['git','ls-files','-z'],cwd=base).decode().rstrip('\0').split('\0');protected={};deps={}
    for rel in files:
        if rel in MUTABLE:continue
        table=protected if rel.split('/')[0] in ('data','src','include','graphics') else deps
        table[rel]=hashlib.sha256((base/rel).read_bytes()).hexdigest()
    data={'base_commit':BASE,'github_base':GITHUB_BASE,'protected_hashes':protected,'dependency_hashes':deps,'maps':{n:{'map':maps[n],'layout':ls[maps[n]['layout']]} for n in (*NAMES,'BirthIsland_Harbor')},'original_layout_count':len(node['layouts']),'native_warps':sum(len(maps[n]['warp_events']) for n in NAMES),'scope':'21 Navel Rock maps and one dependent harbor. All prior tracked files protected except bank declarations, eight native layout bank assignments and 14 layout-only map references. Nine layouts appended without shifting old IDs; all grid/border paths and bytes retained.'}
    raw=json.dumps(data,indent=2,sort_keys=True)+'\n';OUT.mkdir(parents=True,exist_ok=True);p=OUT/'functional_contract.json'
    if p.exists():assert p.read_text()==raw,'Frozen contract differs'
    else:p.write_text(raw)
    print(json.dumps({'gameplay_files':len(protected),'other_tracked_dependencies':len(deps),'maps':len(NAMES),'warps':data['native_warps']}))
if __name__=='__main__':main()
