"""Actual normal save: lab exit must finish the farewell and Running Shoes."""
import argparse
import subprocess
import sys
from campaign_controller import *
parser = argparse.ArgumentParser()
parser.add_argument('--expect', choices=('bypass', 'received'), required=True)
parser.add_argument('--cold', action='store_true')
args = parser.parse_args()
boot()
if args.cold:
    restore(Q / 'campaign_shoes_received.sav')
    assert flag('FLAG_RECEIVED_RUNNING_SHOES')
    assert flag('FLAG_SYS_B_DASH')
    assert var('VAR_LITTLEROOT_TOWN_STATE') == 4
    assert not read('sLockFieldControls', 1)
    # Re-enter and exit the relocated lab: no repeated farewell or lock.
    go(20, 22)
    go(6, 12)
    step(0, 1)
    assert position() == ('LittlerootTown', 20, 23)
    assert not read('sLockFieldControls', 1)
    assert flag('FLAG_HIDE_LITTLEROOT_TOWN_MOM_OUTSIDE')
    snap('shoes_cold_continue')
    (Q / 'campaign_shoes_cold_receipt.json').write_text(json.dumps(metadata() | {
        'fixture_setup': False, 'game_ram_or_rom_writes': False, 'cold_continue': True,
        'new_process': True, 'received_running_shoes': True, 'b_dash': True,
        'town_state': 4, 'repeated_lab_exit_unlocked': True}, indent=2) + '\n')
    print('Running Shoes, separate-process CONTINUE and lab re-entry: PASS', flush=True)
    raise SystemExit(0)
restore(Q / 'campaign_pokedex_received.sav')
assert flag('FLAG_SYS_POKEDEX_GET')
assert var('VAR_LITTLEROOT_TOWN_STATE') == 3
assert not flag('FLAG_RECEIVED_RUNNING_SHOES')
go(6, 12)
step(0, 1)
if args.expect == 'received':
    assert flag('FLAG_RECEIVED_RUNNING_SHOES')
    assert flag('FLAG_SYS_B_DASH')
    assert var('VAR_LITTLEROOT_TOWN_STATE') == 4
    normal_save('shoes_received')
    subprocess.run([sys.executable, str(Path(__file__)), '--expect', 'received', '--cold'], check=True)
cross('Route101')
cross('OldaleTown')
cross('Route102')
assert flag('FLAG_RECEIVED_RUNNING_SHOES') == (args.expect == 'received')
assert flag('FLAG_SYS_B_DASH') == (args.expect == 'received')
snap('shoes_' + args.expect)
if args.expect == 'received':
    normal_save('pampa_with_shoes')
receipt = metadata() | {'fixture_setup': False, 'game_ram_or_rom_writes': False,
                       'source': 'normal journey save after winning CIRO and receiving the dex',
                       'expect': args.expect, 'position': position(),
                       'received_running_shoes': flag('FLAG_RECEIVED_RUNNING_SHOES'),
                       'b_dash': flag('FLAG_SYS_B_DASH'), 'town_state': var('VAR_LITTLEROOT_TOWN_STATE')}
(Q / ('campaign_shoes_' + args.expect + '_receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
print('Normal lab exit and Pampa entry:', args.expect, 'PASS', flush=True)
