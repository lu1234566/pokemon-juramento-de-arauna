"""Cold CONTINUE of an existing, normally generated campaign checkpoint.

This does not create progression or a save. Generate the checkpoint through
the normal UI first. No calls into game functions or RAM/ROM writes.
"""
import argparse
from campaign_controller import *

parser = argparse.ArgumentParser()
parser.add_argument('checkpoint')
args = parser.parse_args()
assert re.fullmatch(r'[a-z0-9_]+', args.checkpoint)
name = 'campaign_' + args.checkpoint
expected = json.loads((Q / (name + '_receipt.json')).read_text())
assert expected['fixture_setup'] is False
assert expected['game_ram_or_rom_writes'] is False
assert expected['normal_save_menu'] is True
assert expected['rom_sha256'] == metadata()['rom_sha256']
boot()
restore(Q / (name + '.sav'))
assert list(position()) == expected['position']
assert party() == expected['party']
assert party_sha256() == expected['party_sha256']
assert all(var(n) == value for n, value in expected['story_vars'].items())
assert all(flag(n) == value for n, value in expected['story_flags'].items())
assert overworld() and not read('sLockFieldControls', 1)
snap(args.checkpoint + '_cold')
receipt = metadata() | {'fixture_setup': False, 'game_ram_or_rom_writes': False,
                       'source_checkpoint': args.checkpoint, 'new_process': True,
                       'cold_continue': True, 'position': position(), 'party': party(),
                       'party_sha256': party_sha256(), 'story_vars': expected['story_vars'],
                       'story_flags': expected['story_flags']}
(Q / (name + '_cold_receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
print('Normal checkpoint', args.checkpoint, 'separate-process CONTINUE: PASS', flush=True)
