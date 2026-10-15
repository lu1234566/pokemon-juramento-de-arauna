"""Revisit Olivia from the private victory SAVE; no fixture progression."""
import subprocess
import sys
from campaign_controller import *

source = 'badge03_olivia_won_20261015'
expected = json.loads((Q / ('campaign_' + source + '_receipt.json')).read_text())
assert expected['fixture_setup'] is False and expected['normal_save_menu'] is True
assert expected['rom_sha256'] == metadata()['rom_sha256']
boot()
restore(Q / ('campaign_' + source + '.sav'))
assert party_sha256() == expected['party_sha256']
assert flag('FLAG_BADGE03_GET') and flag('FLAG_DEFEATED_MAUVILLE_GYM')
assert flag('FLAG_RECEIVED_TM_SHOCK_WAVE') and flag('FLAG_ENABLE_WATTSON_MATCH_CALL')
assert quantity('ITEM_TM_SHOCK_WAVE') == 1
assert var('VAR_PETALBURG_GYM_STATE') == 5
assert var('VAR_SLATEPORT_OUTSIDE_MUSEUM_STATE') == 3
before = party_sha256()
talk(1)
assert not BATTLES and party_sha256() == before
assert quantity('ITEM_TM_SHOCK_WAVE') == 1
assert var('VAR_PETALBURG_GYM_STATE') == 5
assert path_to((4, 20)) is not None
normal_save('badge03_olivia_revisit_20261015')
subprocess.run([sys.executable, str(Q / 'test_campaign_checkpoint.py'), 'badge03_olivia_revisit_20261015'], check=True)
print('Actual third badge, Olivia revisit, one TM, open exit and CONTINUE: PASS', flush=True)
