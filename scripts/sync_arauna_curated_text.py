#!/usr/bin/env python3
"""Install reviewed English contracts explicitly, or check source equivalence."""
from pathlib import Path
import argparse,os,tempfile
import render_pokenav_named_calls_en_checked as calls
import render_remaining_story_en_checked as remaining
import render_main_readiness_residue_en_checked as ready
import render_casa_da_cinza_nara_en_checked as casa
import render_route102_pampa_en_checked as pampa
import render_route120_bento_en as route120
import render_ruins_memorial_en as memorial
import render_remembrancers_core_en as remembrance
ROOT=Path(__file__).resolve().parents[1]
def outputs():
 result={}
 def add(path,targets):
  targets={label:[c.replace('SEU BENTO','MR. BENTO').replace('DONA CELINA','MS. CELINA').replace('DOS NOMES','NOMES') for c in chunks] for label,chunks in targets.items()}
  source=result.get(path,path.read_text());rendered=calls.render_asm(source,targets)
  assert calls.mask_asm(source,targets)==calls.mask_asm(rendered,targets),path
  for chunks in targets.values():calls.payload_line_width(''.join(chunks))
  result[path]=rendered
 add(calls.MATCH_CALL_PATH,calls.build_targets(calls.load_bank()))
 source=calls.STRINGS_PATH.read_text();rendered=calls.render_c_strings(source);calls.validate_c_strings(source,rendered)
 result[calls.STRINGS_PATH]=rendered.replace('_("SEU BENTO")','_("MR. BENTO")')
 targets=remaining.load_targets()
 for section,path in remaining.FILES.items():add(ROOT/path,targets[section])
 bank=ready.load_bank()
 for section,path in ready.FILES.items():
  add(path,bank[section]);ready.validate_asm(section,path.read_text(),result[path],ready.EXPECTED[section])
 result[ready.MENU_PATH]=ready.render_menu(ready.MENU_PATH.read_text())
 result[ready.LANDMARK_PATH]=ready.render_landmarks(ready.LANDMARK_PATH.read_text())
 ready.validate_landmarks(ready.LANDMARK_PATH.read_text(),result[ready.LANDMARK_PATH])
 bank=casa.load_bank();casa.validate_widths(bank);casa.validate_identity(bank)
 for section,path in casa.FILES.items():add(path,bank[section])
 for path,targets in [(pampa.base.CITY,pampa.base.CITY_TARGETS),(pampa.base.ROUTE,pampa.base.ROUTE_TARGETS),(route120.MAP_PATH,route120.TARGETS),(memorial.base.MEMORIAL_PATH,memorial.base.MEMORIAL_TARGETS)]:add(path,{k:v[1] for k,v in targets.items()})
 b=remembrance.base
 for path,targets in [(b.PATH_3F1,b.TARGETS_3F1),(b.PATH_3F2,b.TARGETS_3F2),(b.PATH_4F,b.TARGETS_4F)]:add(path,targets)
 add(ROOT/'data/maps/GraniteCave_StevensRoom/scripts.inc',{'GraniteCave_StevensRoom_Text_ThankYouTakeThis':['MR. BENTO: Thank you for the\\n','LETTER. These names matter.\\p','Take this move for the road.$']})
 return result
def main():
 p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--check',action='store_true');g.add_argument('--write',action='store_true');args=p.parse_args()
 out=outputs();changed=[f for f,s in out.items() if f.read_text()!=s]
 if args.check and changed:
  print('\n'.join('Curated source is stale: '+str(f.relative_to(ROOT)) for f in changed));return 1
 if args.write:
  backup={f:f.read_bytes() for f in changed};staged={}
  try:
   for f in changed:
    with tempfile.NamedTemporaryFile(dir=f.parent,prefix='.curated-',delete=False) as t:t.write(out[f].encode());staged[f]=Path(t.name)
    staged[f].chmod(f.stat().st_mode)
   for f,t in staged.items():os.replace(t,f)
  except BaseException:
   for f,b in backup.items():f.write_bytes(b)
   raise
  finally:
   for t in staged.values():t.unlink(missing_ok=True)
 print(f'Curated English contracts: {len(out)} sources verified; {len(changed)} updated.');return 0
if __name__=='__main__':raise SystemExit(main())
