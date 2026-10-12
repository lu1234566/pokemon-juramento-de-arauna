#!/usr/bin/env python3
"""Generate the canonical mapjson data required by checks on a clean checkout.

This builds only the host mapjson utility; no ARM code, ROM or debug warp is
generated. The same JSON inputs and converter are used by the regular build.
"""
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def main():
    subprocess.run(['make','-C','tools/mapjson'],cwd=ROOT,check=True)
    tool=str(ROOT/'tools/mapjson/mapjson')
    def run(*args):subprocess.run([tool,*map(str,args)],cwd=ROOT,check=True)
    maps=ROOT/'data/maps';layouts=ROOT/'data/layouts';constants=ROOT/'include/constants'
    run('groups','emerald',maps/'map_groups.json',maps,constants)
    run('layouts','emerald',layouts/'layouts.json',layouts,constants)
    inputs=sorted(maps.glob('*/map.json'))
    run('event_constants','emerald',*inputs,constants/'map_event_ids.h')
    for p in inputs:run('map','emerald',p,layouts/'layouts.json',p.parent)
    print(f'Static map data: {len(inputs)} canonical maps generated; no ARM execution.')
if __name__=='__main__':main()
