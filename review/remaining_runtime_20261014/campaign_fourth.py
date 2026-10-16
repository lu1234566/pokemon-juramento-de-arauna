"""Evidence helpers for the natural journey from badge three to badge four.

The campaign controller issues only ordinary joypad inputs. This module adds
read-only story observations and compressed input journals to native SAVE files.
"""
import gzip
import campaign_controller as c

SOURCE = 'badge03_route111_north_ready_20261015'
FLAGS = (
    'FLAG_BADGE04_GET', 'FLAG_DEFEATED_LAVARIDGE_GYM',
    'FLAG_RECEIVED_TM_OVERHEAT', 'FLAG_ENABLE_FLANNERY_MATCH_CALL',
    'FLAG_HIDE_ROUTE_112_TEAM_MAGMA', 'FLAG_MET_ARCHIE_METEOR_FALLS',
    'FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY', 'FLAG_RECEIVED_METEORITE',
    'FLAG_RECEIVED_GO_GOGGLES', 'FLAG_RECEIVED_HM_STRENGTH',
    'FLAG_HIDE_MT_CHIMNEY_TEAM_MAGMA', 'FLAG_HIDE_MT_CHIMNEY_TEAM_AQUA',
)
VARS = ('VAR_METEOR_FALLS_STATE', 'VAR_LAVARIDGE_TOWN_STATE',
        'VAR_JAGGED_PASS_ASH_WEATHER', 'VAR_CABLE_CAR_STATION_STATE')
ITEMS = ('ITEM_TM_OVERHEAT', 'ITEM_METEORITE', 'ITEM_GO_GOGGLES',
         'ITEM_HM_STRENGTH', 'ITEM_SUPER_POTION', 'ITEM_ENERGY_ROOT',
         'ITEM_LAVA_COOKIE', 'ITEM_X_SPEED')


def monitor():
    """Show read-only emulator telemetry during long navigation attempts."""
    original = c.act

    def observed(*args, **kwargs):
        result = original(*args, **kwargs)
        if len(c.INPUTS) % 200 == 0:
            print('JOY', len(c.INPUTS), c.position(),
                  'field', c.overworld(), 'lock', c.read('sLockFieldControls', 1),
                  'battles', len(c.BATTLES), flush=True)
        return result

    c.act = observed


def field_action(action, slot=0):
    """Select a field action actually offered by the ordinary party menu."""
    before = [(m['moves'], m['pp']) for m in c.party()]
    c.start_action(1)
    for _ in range(40):
        if c.active_task('Task_HandleSelectionMenuInput') is not None:
            break
        c.choose_party(slot)
    else:
        raise RuntimeError('Party field-action menu did not open')
    c.act(0, 1, 30)
    internal = c.read('sPartyMenuInternal')
    actions = [c.read(internal + 15 + i, 1) for i in range(c.read(internal + 23, 1))]
    assert action in actions, (action, actions)
    c.snap('field_action_' + str(action) + '_menu_20261016')
    for _ in range(actions.index(action)):
        c.act(128, 2, 25)
    c.act(1, 2, 80)
    c.settle()
    assert [(m['moves'], m['pp']) for m in c.party()] == before
    return {'offered_actions': actions, 'selected_action': action,
            'moves_pp_before': before, 'moves_pp_after': [(m['moves'], m['pp']) for m in c.party()]}


def save(name):
    path = c.normal_save(name)
    receipt_path = c.Q / ('campaign_' + name + '_receipt.json')
    receipt = c.json.loads(receipt_path.read_text())
    receipt['source_checkpoint'] = SOURCE
    receipt['story_flags'].update({n: c.flag(n) for n in FLAGS})
    receipt['story_vars'].update({n: c.var(n) for n in VARS})
    receipt['inventory_checks'].update({n: c.quantity(n) for n in ITEMS})
    receipt['game_stats']['GAME_STAT_RODE_CABLE_CAR'] = c.game_stat('GAME_STAT_RODE_CABLE_CAR')
    for key, suffix, count_key, data in (
        ('input_journal', '_inputs.json.gz', 'rows', receipt.pop('input_runs')),
        ('battle_trace', '_battles.json.gz', 'battles', receipt.pop('battles')),
    ):
        target = c.Q / ('campaign_' + name + suffix)
        target.write_bytes(gzip.compress(c.json.dumps(data).encode(), mtime=0))
        receipt[key] = {'file': target.name, count_key: len(data),
                        'sha256': c.hashlib.sha256(target.read_bytes()).hexdigest()}
    receipt_path.write_text(c.json.dumps(receipt, indent=2) + '\n')
    print('SAVED', name, c.position(), flush=True)
    return path
