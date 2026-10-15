"""Revisit Ademar after loading the privately retained actual victory SAVE."""
import subprocess
import sys
from campaign_controller import *

source = 'ademar_first_result_20261015'
expected = json.loads((Q / ('campaign_' + source + '_receipt.json')).read_text())
assert expected['fixture_setup'] is False and expected['normal_save_menu'] is True
assert expected['rom_sha256'] == metadata()['rom_sha256']
boot()
restore(Q / ('campaign_' + source + '.sav'))
assert party_sha256() == expected['party_sha256']
assert flag('FLAG_BADGE02_GET') and flag('FLAG_RECEIVED_TM_BULK_UP')
assert flag('FLAG_ENABLE_BRAWLY_MATCH_CALL')
assert quantity('ITEM_TM_BULK_UP') == 1
assert var('VAR_PETALBURG_GYM_STATE') == 4
assert read(read('gSaveBlock1Ptr') + 0x30, 1) == 0
talk(1)
assert not BATTLES
assert quantity('ITEM_TM_BULK_UP') == 1
assert var('VAR_PETALBURG_GYM_STATE') == 4
assert overworld() and not read('sLockFieldControls', 1)
normal_save('badge02_revisit_20261015')
subprocess.run([sys.executable, str(Q / 'test_campaign_checkpoint.py'), 'badge02_revisit_20261015'], check=True)
print('Actual second badge, leader revisit, one TM, lights and CONTINUE: PASS', flush=True)
