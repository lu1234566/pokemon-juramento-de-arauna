#!/usr/bin/env python3
"""Freeze the base explicitly; never regenerate the historical checkpoint 01."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from build_cavernas_03a import BASE,ROOT,OUT,NAMES

REGISTRIES={'data/layouts/layouts.json','src/data/arauna_cave_visuals_v2.h','src/data/tilesets/graphics.h','src/data/tilesets/headers.h','src/data/tilesets/metatiles.h'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);a=ap.parse_args();base=a.base.resolve()
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
    target=OUT/'functional_contract.json'
    ls=json.loads((base/'data/layouts/layouts.json').read_text())['layouts'];layouts={l['id']:l for l in ls}
    names=subprocess.check_output(['git','ls-files','data','src','include','graphics'],cwd=base,text=True).splitlines()
    data={'base_commit':BASE,'protected_hashes':{n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in names if n not in REGISTRIES},
          'registry_hashes':{n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in sorted(REGISTRIES)},'maps':{}}
    for n in NAMES:
        m=json.loads((base/f'data/maps/{n}/map.json').read_text());data['maps'][n]={'map':m,'layout':layouts[m['layout']]}
    data['temporary_entries']=[{'route':r,'location':loc,'top':[x,y-1],'entrance':[x,y]} for r,loc,x,y in [('Route114','North',7,4),('Route114','South',6,46),('Route115','West',21,6),('Route115','East',36,10),('Route116','North',59,13),('Route116','South',79,6),('Route118','East',42,6),('Route118','West',9,6)]]
    data['marine_return']={'setdivewarp':'MAP_UNDERWATER_MARINE_CAVE, 9, 6','surface_routes':['Route105','Route125','Route127','Route129']}
    data['preservation_scope']='All preexisting tracked game sources/assets except additive graphic registries and the four secondary-tileset fields.'
    raw=json.dumps(data,indent=2,sort_keys=True)+'\n'
    if target.exists():assert target.read_text()==raw,'Refusing to replace a different frozen contract'
    else:target.write_text(raw)
    print('Frozen:',len(data['protected_hashes']),'protected files, 4 maps, 8 temporary Terra entrances.')
if __name__=='__main__':main()
