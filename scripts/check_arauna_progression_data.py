#!/usr/bin/env python3
"""Check learnset consumer bounds and the Safari Rock Smash contract."""
from pathlib import Path
import re,json,csv
ROOT=Path(__file__).resolve().parents[1]
def main():
 limit=int(re.search(r'#define MAX_LEVEL_UP_MOVES\s+(\d+)',(ROOT/'include/constants/pokemon.h').read_text())[1]);errors=[]
 lists=re.findall(r'static const u16 (\w+)\[\] = \{(.*?)\};',(ROOT/'src/data/pokemon/arauna_complete_learnsets.h').read_text(),re.S)
 for name,body in lists:
  moves=re.findall(r'LEVEL_UP_MOVE\(\s*(\d+),\s*(MOVE_\w+)\)',body)
  if len(moves)>limit:errors.append(f'{name}: {len(moves)} exceeds {limit}')
  if 'CACTURNE' in name and ('70','MOVE_UPROAR') not in moves:errors.append('Iarau lost level-70 UPROAR')
 mapping={r['species_constant']:r for r in csv.DictReader((ROOT/'docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv').open())};slots=0
 for group in json.loads((ROOT/'src/data/wild_encounters.json').read_text())['wild_encounter_groups']:
  for enc in group['encounters']:
   if not enc.get('map','').startswith('MAP_SAFARI_ZONE_'):continue
   for mon in enc.get('rock_smash_mons',{}).get('mons',[]):
    slots+=1
    if 'rock' not in mapping[mon['species']]['types'].split('/'):errors.append('Safari rock habitat drift: '+mon['species'])
 if errors:print('\n'.join(errors));return 1
 print(f'Progression data PASS: {len(lists)} learnsets within {limit}; {slots} Safari rock slots.');return 0
if __name__=='__main__':raise SystemExit(main())
