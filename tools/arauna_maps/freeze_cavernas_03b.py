#!/usr/bin/env python3
"""Freeze the base explicitly; never regenerate the historical checkpoint 01."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from build_cavernas_03b import BASE,ROOT,OUT,NAMES,REGISTRIES



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
    source=(base/'src/braille_puzzles.c').read_text()
    import re
    data['regice_perimeter']=[[int(x),int(y)] for x,y in re.findall(r'{(\d+),\s*(\d+)}',source.split('sRegicePathCoords')[1].split('};')[0])]
    data['immutable_metatiles']=[553,554,555,556,562,563,564,565,566,567,519]
    data['doors']={'SealedChamber_OuterRoom':{'top':[9,1],'bottom':[9,2],'flag':'FLAG_SYS_BRAILLE_DIG'},'AncientTomb':{'top':[7,19],'bottom':[7,20],'flag':'FLAG_SYS_REGISTEEL_PUZZLE_COMPLETED'},'IslandCave':{'top':[7,19],'bottom':[7,20],'flag':'FLAG_SYS_BRAILLE_REGICE_COMPLETED'}}
    data['braille_message_labels']=re.findall(r'^(\w+Braille_\w+):',(base/'data/text/braille.inc').read_text(),re.M)
    data['sealed_surface_return']='MAP_UNDERWATER_SEALED_CHAMBER, 12, 44'
    data['shared_puzzle_dependency']='DesertRuins and original field-move hooks are included in protected_hashes.'
    extra=set()
    for path in (base/'src').rglob('*.h'):
        for rel in re.findall(r'INCBIN_\w+\("([^"]+)"\)',path.read_text(errors='ignore')):
            if rel.startswith('review/') and (base/rel).is_file():extra.add(rel)
    extra.add('art/cavernas_03a/minerais_atlas.png')
    data['dependency_hashes']={rel:hashlib.sha256((base/rel).read_bytes()).hexdigest() for rel in sorted(extra)}
    data['preservation_scope']='All preexisting tracked game sources/assets except additive graphic registries and the four secondary-tileset fields.'
    raw=json.dumps(data,indent=2,sort_keys=True)+'\n'
    if target.exists():assert target.read_text()==raw,'Refusing to replace a different frozen contract'
    else:target.write_text(raw)
    print('Frozen:',len(data['protected_hashes']),'protected files, 4 maps, 36 Regice perimeter cells.')
if __name__=='__main__':main()
