"""Normal campaign replay: clinic, CIRO defeat/retry and ANAHI's dex."""
from campaign_controller import *
boot()
restore(Q / 'natural_starter_complete.sav')
before = read('gSaveCounter')
go(6, 12)
step(0, 1)
cross('Route101')
cross('OldaleTown')
go(7, 19)
talk('LOCALID_OLDALE_NURSE')
go(7, 8)
step(0, 1)
for attempt in range(4):
    cross('Route103')
    level_to(10 + attempt)
    go(10, 4)
    heal()
    talk('LOCALID_ROUTE103_RIVAL')
    if flag('FLAG_DEFEATED_RIVAL_ROUTE103'):
        break
    assert var('VAR_BIRCH_LAB_STATE') == 3
    assert not read('sLockFieldControls', 1)
else:
    raise RuntimeError('CIRO could not be defeated through the normal UI')
normal_save('ciro_semantic_replay')
cross('OldaleTown')
cross('Route101')
cross('LittlerootTown')
go(20, 22)
settle()
normal_save('pokedex_received')
actions = len(INPUTS)
assert position()[0] == 'LittlerootTown_ProfessorBirchsLab'
assert var('VAR_BIRCH_LAB_STATE') == 5
assert var('VAR_LITTLEROOT_RIVAL_STATE') == 4
assert var('VAR_LITTLEROOT_TOWN_STATE') == 3
assert flag('FLAG_DEFEATED_RIVAL_ROUTE103')
assert flag('FLAG_SYS_POKEDEX_GET')
assert flag('FLAG_ADVENTURE_STARTED')
assert quantity('ITEM_POKE_BALL') == 5
assert not flag('FLAG_RECEIVED_RUNNING_SHOES')
assert not read('sLockFieldControls', 1)
assert read('gSaveCounter') > before
assert LIB.exportsave(str(Q / 'campaign_pokedex_received.sav').encode())
snap('dex_replay_complete')
receipt = metadata() | {'fixture_setup': False, 'game_ram_or_rom_writes': False,
                       'actions': actions, 'position': position(), 'party': party(),
                       'ciro_defeated': True, 'lab_state': 5, 'dex_received': True,
                       'adventure_started': True, 'poke_balls': 5, 'normal_save_menu': True}
(Q / 'campaign_dex_replay_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('Normal clinic, CIRO retry, dex and SAVE replay: PASS', flush=True)
