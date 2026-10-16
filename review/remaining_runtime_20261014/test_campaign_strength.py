"""Use badge-granted Strength from the actual private approach SAVE."""
import subprocess
import sys
import campaign_controller as c
import campaign_fourth as fourth

source = 'badge04_strength_before_field_use_20261016'
expected = c.json.loads((c.Q / ('campaign_' + source + '_receipt.json')).read_text())
assert expected['fixture_setup'] is False and expected['normal_save_menu'] is True
assert expected['rom_sha256'] == c.metadata()['rom_sha256']
c.boot()
c.restore(c.Q / ('campaign_' + source + '.sav'))
assert c.party_sha256() == expected['party_sha256']
assert c.position() == ('FieryPath', 18, 15)
assert c.flag('FLAG_BADGE04_GET')
assert c.quantity('ITEM_HM_STRENGTH') == 0
assert not any(c.constant('MOVE_STRENGTH') in m['moves'] for m in c.party())
before = [(m['moves'], m['pp']) for m in c.party()]
assert (3, 17, 15) in c.objects()
c.act(32, 1, 8)
observed = fourth.field_action(22)
assert c.flag('FLAG_SYS_USE_STRENGTH')
c.step(-1, 0)
c.act(0, 1, 60)
assert (3, 16, 15) in c.objects() and (3, 17, 15) not in c.objects()
c.go(17, 15)
assert c.position() == ('FieryPath', 17, 15)
assert [(m['moves'], m['pp']) for m in c.party()] == before
assert not c.BATTLES
fourth.SOURCE = source
tag = 'badge04_strength_replay_20261016'
fourth.save(tag)
receipt_path = c.Q / ('campaign_' + tag + '_receipt.json')
receipt = c.json.loads(receipt_path.read_text())
receipt['field_observation'] = observed | {'boulder_local_id': 3,
    'boulder_before': [17, 15], 'boulder_after': [16, 15],
    'vacated_tile_walked': [17, 15], 'hm_strength_quantity': 0}
receipt_path.write_text(c.json.dumps(receipt, indent=2) + '\n')
subprocess.run([sys.executable, str(c.Q / 'test_campaign_checkpoint.py'), tag], check=True)
print('Native Strength menu, no learned HM or PP cost, boulder push and CONTINUE: PASS', flush=True)
