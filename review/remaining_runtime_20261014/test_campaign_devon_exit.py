"""Continue the real Devon checkpoint through the mandatory PokéNav tutorial.

Requires the privately retained normal campaign save, not a fixture. No game
function injection, RAM/ROM writes or artificial progression is used.
"""
import subprocess
import sys
from campaign_controller import *

source = 'devon_return_20261015'
expected = json.loads((Q / ('campaign_' + source + '_receipt.json')).read_text())
assert expected['fixture_setup'] is False
assert expected['rom_sha256'] == metadata()['rom_sha256']
boot()
restore(Q / ('campaign_' + source + '.sav'))
assert party_sha256() == expected['party_sha256']
assert var('VAR_RUSTBORO_CITY_STATE') == 6
assert flag('FLAG_RETURNED_DEVON_GOODS') and flag('FLAG_SYS_POKENAV_GET')
assert quantity('ITEM_LETTER') == 1
go(2, 1)
assert position()[0] == 'RustboroCity_DevonCorp_2F'
go(14, 1)
assert position()[0] == 'RustboroCity_DevonCorp_1F'
go(5, 8)
step(0, 1)
assert position()[0] == 'RustboroCity'
assert var('VAR_RUSTBORO_CITY_STATE') == 7
assert flag('FLAG_HAS_MATCH_CALL')
assert overworld() and not read('sLockFieldControls', 1)
normal_save('devon_exit_20261015')
subprocess.run([sys.executable, str(Q / 'test_campaign_checkpoint.py'), 'devon_exit_20261015'], check=True)
print('Normal Devon exit, forced PokéNav tutorial and separate-process CONTINUE: PASS', flush=True)
