"""Use the badge-granted Flash entry through the actual party context menu."""
import subprocess
import sys
from campaign_controller import *

source = 'flash_before_field_use_20261015'
expected = json.loads((Q / ('campaign_' + source + '_receipt.json')).read_text())
assert expected['fixture_setup'] is False and expected['normal_save_menu'] is True
assert expected['rom_sha256'] == metadata()['rom_sha256']
boot()
restore(Q / ('campaign_' + source + '.sav'))
assert party_sha256() == expected['party_sha256']
assert flag('FLAG_BADGE02_GET') and quantity('ITEM_HM_FLASH') == 1
assert read(read('gSaveBlock1Ptr') + 0x30, 1) == 7
before = [(m['moves'], m['pp']) for m in party()]
assert not any(constant('MOVE_FLASH') in m['moves'] for m in party())
start_action(1)
choose_party(0)
act(128, 2, 25)  # SUMMARY -> FLASH
act(1, 2, 60)
settle()
assert flag('FLAG_SYS_USE_FLASH')
assert read(read('gSaveBlock1Ptr') + 0x30, 1) == 1
assert [(m['moves'], m['pp']) for m in party()] == before
normal_save('flash_replay_20261015')
p = Q / 'campaign_flash_replay_20261015_receipt.json'
receipt = json.loads(p.read_text())
receipt['story_flags']['FLAG_SYS_USE_FLASH'] = True
receipt['map_flash_level'] = 1
receipt['source_checkpoint'] = source
p.write_text(json.dumps(receipt, indent=2) + '\n')
subprocess.run([sys.executable, str(Q / 'test_campaign_checkpoint.py'), 'flash_replay_20261015'], check=True)
print('Normal Flash menu use without teaching, unchanged moves/PP and CONTINUE: PASS', flush=True)
