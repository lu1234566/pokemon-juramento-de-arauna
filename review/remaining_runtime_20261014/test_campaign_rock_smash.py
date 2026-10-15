"""Native badge-granted Rock Smash, from the actual private approach SAVE."""
import subprocess
import sys
from campaign_controller import *

source = 'rock_smash_before_field_use_20261015'
expected = json.loads((Q / ('campaign_' + source + '_receipt.json')).read_text())
assert expected['fixture_setup'] is False and expected['normal_save_menu'] is True
assert expected['rom_sha256'] == metadata()['rom_sha256']
boot()
restore(Q / ('campaign_' + source + '.sav'))
assert party_sha256() == expected['party_sha256']
assert position() == ('Route111', 18, 102)
assert flag('FLAG_BADGE03_GET') and quantity('ITEM_HM_ROCK_SMASH') == 1
before = [(m['moves'], m['pp']) for m in party()]
assert not any(constant('MOVE_ROCK_SMASH') in m['moves'] for m in party())
stat_before = game_stat('GAME_STAT_USED_ROCK_SMASH')
act(64, 1, 8)
start_action(1)
for _ in range(30):
    if active_task('Task_HandleSelectionMenuInput') is not None:
        break
    choose_party(0)
else:
    raise RuntimeError('Party context menu did not open')
act(0, 1, 30)
internal = read('sPartyMenuInternal')
actions = [read(internal + 15 + i, 1) for i in range(read(internal + 23, 1))]
# src/party_menu.c: MENU_FIELD_MOVES (19) + FIELD_MOVE_ROCK_SMASH (2).
assert 21 in actions
snap('rock_smash_replay_menu_20261015')
for _ in range(actions.index(21)):
    act(128, 2, 25)
act(1, 2, 80)
settle()
assert not BATTLES
assert [(m['moves'], m['pp']) for m in party()] == before
assert game_stat('GAME_STAT_USED_ROCK_SMASH') == stat_before + 1
assert not any(local == 15 for local, _, _ in objects())
go(18, 100)
normal_save('rock_smash_replay_20261015')
subprocess.run([sys.executable, str(Q / 'test_campaign_checkpoint.py'), 'rock_smash_replay_20261015'], check=True)
print('Normal Rock Smash menu, no learned HM or PP cost, cleared passage and CONTINUE: PASS', flush=True)
