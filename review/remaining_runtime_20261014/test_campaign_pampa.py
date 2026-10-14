"""Normal Pampa journey, Val's tutorial and Mata da Espera rescue.

The origin is produced by the normal NEW GAME → starter → dex → shoes tests.
LEVEL and REST are selected through the installed in-game ARAUNA menu.
"""
import argparse
import subprocess
import sys
from campaign_controller import *

parser = argparse.ArgumentParser()
parser.add_argument('--cold', choices=('val', 'mata'))
args = parser.parse_args()
boot()
if args.cold:
    stage = 'pampa_val' if args.cold == 'val' else 'pampa_mata'
    restore(Q / ('campaign_' + stage + '.sav'))
    expected = json.loads((Q / ('campaign_' + stage + '_receipt.json')).read_text())
    assert list(position()) == expected['position']
    assert party() == expected['party']
    assert party_sha256() == expected['party_sha256']
    assert var('VAR_PETALBURG_GYM_STATE') == 2
    assert var('VAR_PETALBURG_CITY_STATE') == 3
    assert flag('FLAG_RECEIVED_RUNNING_SHOES')
    assert not read('sLockFieldControls', 1)
    if args.cold == 'mata':
        assert var('VAR_PETALBURG_WOODS_STATE') == 1
        assert flag('FLAG_HIDE_PETALBURG_WOODS_AQUA_GRUNT')
        assert flag('FLAG_HIDE_PETALBURG_WOODS_DEVON_EMPLOYEE')
        assert quantity('ITEM_GREAT_BALL') == 1
    snap(stage + '_cold')
    (Q / ('campaign_' + stage + '_cold_receipt.json')).write_text(json.dumps(metadata() | {
        'fixture_setup': False, 'game_ram_or_rom_writes': False, 'new_process': True,
        'cold_continue': True, 'party_exact': True, 'position': position(),
        'gym_state': 2, 'city_state': 3, 'stage': args.cold}, indent=2) + '\n')
    print('Pampa', args.cold, 'separate-process CONTINUE: PASS', flush=True)
    raise SystemExit(0)

restore(Q / 'campaign_pampa_with_shoes.sav')
assert position()[0] == 'Route102'
heal()
cross('PetalburgCity')
go(15, 8)
assert position()[0] == 'PetalburgCity_Gym'
before = party()
before_digest = party_sha256()
balls = quantity('ITEM_POKE_BALL')
talk('LOCALID_PETALBURG_GYM_NORMAN')
assert position() == ('PetalburgCity_Gym', 4, 108)
assert party() == before, 'Val tutorial must restore the actual player party'
assert party_sha256() == before_digest, 'Val must restore all bytes of the active party'
assert quantity('ITEM_POKE_BALL') == balls, 'Val uses the tutorial ball'
assert var('VAR_PETALBURG_GYM_STATE') == 2
assert var('VAR_PETALBURG_CITY_STATE') == 3
normal_save('pampa_val')
subprocess.run([sys.executable, str(Path(__file__)), '--cold', 'val'], check=True)
go(4, 111)
step(0, 1)
cross('Route104')
go(10, 38)
assert position()[0] == 'PetalburgWoods'
level_to(15)
heal()
go(26, 23)
settle()
assert var('VAR_PETALBURG_WOODS_STATE') == 1
assert flag('FLAG_HIDE_PETALBURG_WOODS_AQUA_GRUNT')
assert flag('FLAG_HIDE_PETALBURG_WOODS_DEVON_EMPLOYEE')
assert quantity('ITEM_GREAT_BALL') == 1
assert read('gBattleOutcome', 1) == constant('B_OUTCOME_WON')
normal_save('pampa_mata')
subprocess.run([sys.executable, str(Path(__file__)), '--cold', 'mata'], check=True)
print('Normal Elias/Val tutorial and Mata da Espera rescue: PASS', flush=True)
