"""Revisit Nara from a real victory SAVE; no fixture progression."""
import subprocess
import sys
import campaign_controller as c
import campaign_fourth as fourth

source = 'badge04_nara_won_20261016'
expected = c.json.loads((c.Q / ('campaign_' + source + '_receipt.json')).read_text())
assert expected['fixture_setup'] is False and expected['normal_save_menu'] is True
assert expected['rom_sha256'] == c.metadata()['rom_sha256']
c.boot()
c.restore(c.Q / ('campaign_' + source + '.sav'))
assert c.party_sha256() == expected['party_sha256']
for flag in ('FLAG_BADGE04_GET', 'FLAG_DEFEATED_LAVARIDGE_GYM',
             'FLAG_RECEIVED_TM_OVERHEAT', 'FLAG_ENABLE_FLANNERY_MATCH_CALL',
             'FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY'):
    assert c.flag(flag), flag
assert c.quantity('ITEM_TM_OVERHEAT') == 1
assert c.var('VAR_PETALBURG_GYM_STATE') == 6
assert c.var('VAR_LAVARIDGE_TOWN_STATE') == 1
before = c.party_sha256()
c.talk(1)
assert not c.BATTLES and c.party_sha256() == before
assert c.quantity('ITEM_TM_OVERHEAT') == 1
assert c.var('VAR_PETALBURG_GYM_STATE') == 6
assert c.path_to((12, 12)) is not None
fourth.SOURCE = source
fourth.save('badge04_nara_revisit_20261016')
subprocess.run([sys.executable, str(c.Q / 'test_campaign_checkpoint.py'),
                'badge04_nara_revisit_20261016'], check=True)
print('Actual fourth badge, Nara revisit, one TM and CONTINUE: PASS', flush=True)
