"""Normal letter delivery from the private pre-delivery campaign SAVE."""
import subprocess
import sys
from campaign_controller import *

source = 'bento_before_letter_20261015'
expected = json.loads((Q / ('campaign_' + source + '_receipt.json')).read_text())
assert expected['fixture_setup'] is False and expected['normal_save_menu'] is True
assert expected['rom_sha256'] == metadata()['rom_sha256']
boot()
restore(Q / ('campaign_' + source + '.sav'))
assert list(position()) == expected['position']
assert party_sha256() == expected['party_sha256']
assert quantity('ITEM_LETTER') == 1
assert not flag('FLAG_DELIVERED_STEVEN_LETTER')
step(0, 1)
assert position()[0] == 'GraniteCave_StevensRoom'
talk(1)
assert quantity('ITEM_LETTER') == 0 and quantity('ITEM_TM_STEEL_WING') == 1
assert flag('FLAG_DELIVERED_STEVEN_LETTER')
assert flag('FLAG_REGISTERED_STEVEN_POKENAV')
assert flag('FLAG_HIDE_GRANITE_CAVE_STEVEN')
assert all(o[0] != 1 for o in objects())
go(7, 3)
assert position()[0] == 'GraniteCave_1F'
step(0, -1)
go(5, 10)
step(0, 1)
assert position()[0] == 'GraniteCave_StevensRoom'
assert all(o[0] != 1 for o in objects())
assert quantity('ITEM_TM_STEEL_WING') == 1
normal_save('bento_replay_20261015')
subprocess.run([sys.executable, str(Q / 'test_campaign_checkpoint.py'), 'bento_replay_20261015'], check=True)
print('Normal letter delivery, room revisit and separate-process CONTINUE: PASS', flush=True)
