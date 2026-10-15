"""Normal campaign: only joypad, reads and export of native flash saves.

No injected calls, fixtures, teleports, writes or forced battle outcomes.
"""
import collections
import hashlib
import re
import struct
from runtime import LIB, R, Q, SYMS, ADDRESSES, constant, read, boot, restore, press, metadata, json, Path, Image

INPUTS, BATTLES, BLOCKED = [], [], set()
CAPTURE_TYPES = set()
CAPTURE_PARTY_SIZE = 2
CAPTURE_WEAKEN = False
SCRIPT_YESNOBOX = re.findall(r'^\s*(B_SCR_OP_\w+)', (R / 'include/constants/battle_script_commands.h').read_text(), re.M).index('B_SCR_OP_YESNOBOX')
# Optional test driver policy: return a move slot, or None for the default.
# Policies inspect battle state and still act exclusively through the joypad.
MOVE_POLICY = None
PARTY_POLICY = None
ACTION_POLICY = None
ITEM_POLICY = None
SWITCH_POLICY = None
groups = json.loads((R / 'data/maps/map_groups.json').read_text())
MAP_NAMES = {(g, m): name for g, group in enumerate(groups['group_order']) for m, name in enumerate(groups[group])}
ORDERS = [tuple(map(int, row)) for row in re.findall(r'SUBSTRUCT_CASE\(\s*\d+,([0-3]),([0-3]),([0-3]),([0-3])\)', (R / 'src/pokemon.c').read_text())]

def position():
    sb = read('gSaveBlock1Ptr')
    return MAP_NAMES.get((read(sb + 4, 1), read(sb + 5, 1))), read(sb, 2), read(sb + 2, 2)

def var(name):
    return read(read('gSaveBlock1Ptr') + 0x139C + 2 * (constant(name) - constant('VARS_START')), 2)

def flag(name):
    f = constant(name)
    return bool(read(read('gSaveBlock1Ptr') + 0x1270 + f // 8, 1) & (1 << (f % 8)))

def game_stat(name):
    return read(read('gSaveBlock1Ptr') + 0x159C + 4 * constant(name)) ^ read(read('gSaveBlock2Ptr') + 0xAC)

def act(keys=0, count=2, release=12):
    before = position()
    press(keys, count, release)
    INPUTS.append([keys, count, release])
    return before, position()

def snap(name):
    raw = Q / ('campaign_' + name + '.rgba')
    LIB.pixels(str(raw).encode())
    Image.frombytes('RGBA', (240, 160), raw.read_bytes()).save(Q / ('campaign_' + name + '.png'))
    raw.unlink()

def party():
    result = []
    for i in range(read('gPlayerPartyCount', 1)):
        p = SYMS['gPlayerParty'] + 100 * i
        personality, ot = read(p), read(p + 4)
        data = b''.join(struct.pack('<I', read(p + 32 + j * 4) ^ personality ^ ot) for j in range(12))
        growth, attacks = [ORDERS[personality % 24][n] * 12 for n in (0, 1)]
        result.append({'species': int.from_bytes(data[growth:growth+2], 'little'), 'personality': personality,
                       'level': read(p + 84, 1), 'hp': read(p + 86, 2), 'max_hp': read(p + 88, 2),
                       'moves': list(struct.unpack('<4H', data[attacks:attacks+8])), 'pp': list(data[attacks+8:attacks+12])})
    return result

def party_sha256():
    data = b''.join(struct.pack('<I', read(SYMS['gPlayerParty'] + offset))
                    for offset in range(0, 100 * read('gPlayerPartyCount', 1), 4))
    return hashlib.sha256(data).hexdigest()

def boxed_records():
    records = []
    storage = read('gPokemonStoragePtr')
    for index in range(14 * 30):
        address = storage + 4 + 80 * index
        if read(address) or read(address + 4):
            data = b''.join(struct.pack('<I', read(address + offset)) for offset in range(0, 80, 4))
            records.append({'box': index // 30, 'slot': index % 30,
                            'personality': read(address), 'sha256': hashlib.sha256(data).hexdigest()})
    return records

def overworld():
    return read(SYMS['gMain'] + 4) == SYMS['CB2_Overworld'] | 1

def controller(name, battler=0):
    return read(SYMS['gBattlerControllerFuncs'] + 4 * battler) in [a | 1 for a in ADDRESSES.get(name, [])]

def active_task(name):
    funcs = {a | 1 for a in ADDRESSES.get(name, [])}
    return next((i for i in range(16) if read(SYMS['gTasks'] + i * 40 + 4, 1) and read(SYMS['gTasks'] + i * 40) in funcs), None)

def quantity(item):
    target = constant(item)
    key = read(read('gSaveBlock2Ptr') + 0xAC) & 65535
    total = 0
    for pocket in range(5):
        base = SYMS['gBagPockets'] + pocket * 8
        slots, capacity = read(base), read(base + 4, 1)
        for i in range(capacity):
            if read(slots + i * 4, 2) == target:
                total += read(slots + i * 4 + 2, 2) ^ key
    return total

def living_enemy():
    return next((i for i in (1, 3) if i < read('gBattlersCount', 1)
                 and not (read('gAbsentBattlerFlags', 1) & (1 << i))
                 and read(SYMS['gBattleMons'] + 88 * i + 40, 2)), 1)

def move_score(move, battler=0):
    attr = SYMS['gBattleMoves'] + 12 * move
    power, kind, accuracy = read(attr + 1, 1), read(attr + 2, 1), read(attr + 3, 1)
    if not power:
        return 0
    p, e = SYMS['gBattleMons'] + 88 * battler, SYMS['gBattleMons'] + 88 * living_enemy()
    if move in (constant('MOVE_FLAIL'), constant('MOVE_REVERSAL')):
        fraction = read(p + 40, 2) * 48 // max(1, read(p + 44, 2))
        power = next(value for ceiling, value in ((1, 200), (4, 150), (9, 100), (16, 80), (32, 40), (48, 20)) if fraction <= ceiling)
    physical = kind < constant('TYPE_MYSTERY')
    def staged_stat(mon, offset, stage_index):
        stage = read(mon + 24 + stage_index, 1) - 6
        multiplier = (2 + stage) / 2 if stage >= 0 else 2 / (2 - stage)
        return read(mon + offset, 2) * multiplier
    ratio = staged_stat(p, 2 if physical else 8, 1 if physical else 4) / max(1, staged_stat(e, 4 if physical else 10, 2 if physical else 5))
    stab = 1.5 if kind in (read(p + 33, 1), read(p + 34, 1)) else 1
    effectiveness, types = 1, set((read(e + 33, 1), read(e + 34, 1)))
    table = SYMS['gTypeEffectiveness']
    for j in range(124):
        attack, defend, value = [read(table + j * 3 + k, 1) for k in range(3)]
        if attack == 255:
            break
        if attack == kind and defend in types:
            effectiveness *= value / 10
    return power * ratio * stab * effectiveness * (accuracy or 100) / 100

def choose_grid(cursor_symbol, target):
    act(0, 1, 25)
    cur = read(cursor_symbol, 1)
    if (cur & 1) != (target & 1):
        act(16 if target & 1 else 32, 2, 25)
    cur = read(cursor_symbol, 1)
    if (cur & 2) != (target & 2):
        act(128 if target & 2 else 64, 2, 25)
    act(1, 2, 25)

def choose_party(target):
    # This task exists during the fade-in too; wait for normal UI input.
    act(0, 1, 25)
    current = read(SYMS['gPartyMenu'] + 9, 1)
    if current == target:
        act(1, 2, 25)
    elif current == 0 and target > 0:
        act(16, 2, 25)
    elif 0 < current < 6 and target == 0:
        act(32, 2, 25)
    else:
        act(128 if current < target else 64, 2, 25)

def use_battle_item(item, personality=None, battler=0):
    """Choose BAG, an owned item and its recipient using ordinary input."""
    before = quantity(item)
    assert before > 0
    choose_grid(SYMS['gActionSelectionCursor'] + battler, 1)
    for _ in range(400):
        if quantity(item) < before and read(SYMS['gMain'] + 4) == SYMS['BattleMainCB2'] | 1:
            return
        if active_task('Task_BagMenu_HandleInput') is not None:
            pocket = read(SYMS['gBagPosition'] + 5, 1)
            if pocket:
                act(32, 2, 35)
                continue
            slots, capacity = read('gBagPockets'), read(SYMS['gBagPockets'] + 4, 1)
            items = [read(slots + 4 * i, 2) for i in range(capacity) if read(slots + 4 * i, 2)]
            target = items.index(constant(item))
            cursor = read(SYMS['gBagPosition'] + 8, 2) + read(SYMS['gBagPosition'] + 18, 2)
            act(128 if cursor < target else 64 if cursor > target else 1, 2, 30)
        elif active_task('Task_HandleChooseMonInput') is not None:
            target = next(i for i, mon in enumerate(party()) if mon['personality'] == personality)
            choose_party(target)
        else:
            act(1, 2, 25)
    snap('item_timeout')
    raise RuntimeError(('battle item timeout', item, personality))

def settle(limit=5000):
    battle = None
    capturing = False
    weakening = False
    weaken_turns = 0
    for _ in range(limit):
        action_battler = next((i for i in (0, 2) if controller('HandleInputChooseAction', i)), None)
        move_battler = next((i for i in (0, 2) if controller('HandleInputChooseMove', i)), None)
        if overworld() and not read('sLockFieldControls', 1):
            if battle is not None:
                battle |= {'outcome': read('gBattleOutcome', 1), 'end': position(), 'party_after': party()}
                BATTLES.append(battle)
                battle = None
                capturing = False
            act(0, 1, 30)
            if overworld() and not read('sLockFieldControls', 1):
                return
        elif action_battler is not None:
            if battle is None:
                battle = {'trainer': read('gTrainerBattleOpponent_A', 2) if read('gBattleTypeFlags') & 8 else 0, 'type_flags': read('gBattleTypeFlags'), 'start': position(), 'party_before': party(), 'move_choices': []}
                snap('battle_' + str(battle['trainer']) + '_start')
            selected_item = ITEM_POLICY(action_battler) if ITEM_POLICY else None
            if selected_item:
                battle.setdefault('item_choices', []).append(list(selected_item))
                use_battle_item(*selected_item, battler=action_battler)
                continue
            enemy_types = {read(SYMS['gBattleMons'] + 88 * living_enemy() + 33, 1), read(SYMS['gBattleMons'] + 88 * living_enemy() + 34, 1)}
            balls = sum(quantity(item) for item in ('ITEM_POKE_BALL', 'ITEM_GREAT_BALL', 'ITEM_PREMIER_BALL'))
            capturing = bool(CAPTURE_TYPES & enemy_types) and not (read('gBattleTypeFlags') & 8) and read('gPlayerPartyCount', 1) < CAPTURE_PARTY_SIZE and balls > 0
            e = SYMS['gBattleMons'] + 88 * living_enemy()
            # Drain moves can keep a grass-vs-grass encounter at full HP.
            # Bound preparation so the driver eventually throws a ball.
            weakening = capturing and CAPTURE_WEAKEN and weaken_turns < 4 and read(e + 40, 2) * 3 > read(e + 44, 2)
            selected_action = ACTION_POLICY(action_battler) if ACTION_POLICY and not capturing else None
            choose_grid(SYMS['gActionSelectionCursor'] + action_battler,
                        selected_action if selected_action is not None else 1 if capturing and not weakening else 0)
        elif move_battler is not None:
            p = SYMS['gBattleMons'] + 88 * move_battler
            options = [(move_score(read(p + 12 + j * 2, 2), move_battler), j) for j in range(4) if read(p + 12 + j * 2, 2) and read(p + 36 + j, 1)]
            selected = MOVE_POLICY(move_battler) if MOVE_POLICY and not weakening else None
            if selected is None:
                selected = (min if weakening else max)([o for o in options if o[0] > 0] or options or [(0, 0)])[1]
            assert not options or selected in [slot for _, slot in options], ('unavailable move', selected, options)
            if battle is not None:
                enemy = SYMS['gBattleMons'] + 88 * living_enemy()
                battle['move_choices'].append({'battler': move_battler, 'species': read(p, 2), 'hp': read(p + 40, 2), 'enemy_species': read(enemy, 2), 'enemy_hp': read(enemy + 40, 2), 'move': read(p + 12 + 2 * selected, 2)})
            choose_grid(SYMS['gMoveSelectionCursor'] + move_battler, selected)
            if weakening:
                weaken_turns += 1
        elif any(controller('HandleInputChooseTarget', i) for i in (0, 2)):
            # A selected move may default to the ally in a double battle.
            # Cycle the ordinary target cursor until it points at a live foe.
            if read('gMultiUsePlayerCursor', 1) == living_enemy():
                act(1, 2, 25)
            else:
                act(16, 2, 25)
        elif any(controller('PlayerHandleYesNoInput', i) for i in (0, 2)):
            # Keep the active Pokemon after a foe faints. Forced replacements
            # still go through the real party screen below.
            act(1 if SWITCH_POLICY and SWITCH_POLICY() else 2, 2, 25)
        elif (not overworld() and read(read('gBattlescriptCurrInstr'), 1) == SCRIPT_YESNOBOX
              and read('gBattleCommunication', 1) == 1):
            act(1 if SWITCH_POLICY and SWITCH_POLICY() else 2, 2, 25)
        elif capturing and read('gBattleOutcome', 1) == constant('B_OUTCOME_CAUGHT'):
            # B closes the new dex entry and declines a nickname normally.
            act(2, 2, 12)
        elif capturing and read(SYMS['gMain'] + 4) == SYMS['CB2_BagMenuRun'] | 1:
            if not any(quantity(item) for item in ('ITEM_POKE_BALL', 'ITEM_GREAT_BALL', 'ITEM_PREMIER_BALL')):
                act(2)
                capturing = False
            elif read(SYMS['gBagPosition'] + 5, 1) != 1:
                act(16, 2, 35)
            else:
                act(1, 2, 20)
        elif battle is not None and active_task('Task_HandleChooseMonInput') is not None:
            field = {read(SYMS['gBattlerPartyIndexes'] + 2 * i, 2) for i in ((0, 2) if read('gBattleTypeFlags') & 1 else (0,))}
            # The battle party screen temporarily reorders the visible party.
            # Its packed high/low nibbles map UI slots to battle party IDs.
            order = [read(SYMS['gBattlePartyCurrentOrder'] + i // 2, 1) >> (0 if i & 1 else 4) & 15 for i in range(6)]
            alive = [i for i, mon in enumerate(party()) if mon['hp'] > 0 and order[i] not in field]
            if alive:
                target = PARTY_POLICY(alive) if PARTY_POLICY else alive[0]
                assert target in alive, ('unavailable party slot', target, alive)
                choose_party(target)
            else:
                act(2, 2, 25)
        elif read(SYMS['gMain'] + 4) == SYMS['CB2_Pokenav'] | 1 and position()[0] == 'RustboroCity' and var('VAR_RUSTBORO_CITY_STATE') == 6:
            resources = read('gPokenavResources')
            mode = read(resources + 8, 2)
            # PokenavResources.substructPtrs[MAIN_MENU_HANDLER = 1].
            menu = read(resources + 20)
            if mode == 1 and menu and read(menu + 12) == SYMS['HandleMainMenuInputTutorial'] | 1:
                cursor = read(menu + 2, 2)
                act(128 if cursor < 2 else 64 if cursor > 2 else 1, 2, 25)
            else:
                # Ready: select Mr Stone and Call. After the call: close the
                # message, trainer list and main menu with ordinary B input.
                act(2 if mode == 2 else 1, 2, 25)
        elif (task := active_task('Task_HandleMultichoiceInput')) is not None and read(SYMS['gTasks'] + task * 40 + 8 + 2 * 7, 2) == constant('MULTI_ARAUNA_QOL'):
            act(2, 2, 25)
        elif (task := active_task('Task_HandleMultichoiceInput')) is not None and read(SYMS['gTasks'] + task * 40 + 8 + 2 * 7, 2) == constant('MULTI_FORCED_START_MENU'):
            # Devon's tutorial requires selecting POKENAV in its fixed menu.
            # Repeated A would continually reopen its explanatory dialogue.
            act(0, 1, 25)
            for _ in range(7):
                act(64, 2, 12)
            for _ in range(3):
                act(128, 2, 12)
            act(1, 2, 60)
        else:
            act(1, 2, 10)
    snap('settle_timeout')
    raise RuntimeError(('scene/battle timeout', position(), hex(read(SYMS['gMain'] + 4)), party()))

def start_action(action):
    assert overworld() and not read('sLockFieldControls', 1)
    act(8, 2, 40)
    cur, count = read('sStartMenuCursorPos', 1), read('sNumStartMenuActions', 1)
    actions = [read(SYMS['sCurrentStartMenuActions'] + i, 1) for i in range(count)]
    target = actions.index(action)
    for _ in range((target - cur) % count):
        act(128, 2, 8)
    act(1, 2, 80)

def heal():
    start_action(4)  # ARAUNA
    for _ in range(100):
        if active_task('Task_HandleMultichoiceInput') is not None:
            break
        act(1)
    act(0, 1, 20)
    for _ in range(4):
        act(128, 2, 8)
    act(1, 2, 90)
    for _ in range(400):
        if active_task('Task_HandleMultichoiceInput') is not None:
            break
        act(1)
    act(0, 1, 20)
    act(2, 2, 50)
    assert not read('sLockFieldControls', 1)
    assert all(p['hp'] == p['max_hp'] for p in party())

def level_to(level, slot=0, replace_slot=0):
    start_action(4)
    for _ in range(3000):
        # Finish the level's move-learning/evolution prompts before leaving.
        # A level value alone can be reached while a Yes/No prompt is active.
        if party()[slot]['level'] >= level and active_task('Task_HandleChooseMonInput') is not None:
            break
        if active_task('Task_HandleReplaceMoveInput') is not None:
            act(0, 1, 50)
            for _ in range(replace_slot):
                act(128, 2, 25)
            act(1, 2, 80)
        elif active_task('Task_HandleChooseMonInput') is not None:
            choose_party(slot)
        else:
            act(1, 2, 10)
    else:
        snap('level_timeout')
        raise RuntimeError(('LEVEL timeout', level, slot, party()))
    for _ in range(200):
        act(2, 2, 16)
        if overworld() and not read('sLockFieldControls', 1):
            return
    raise RuntimeError('LEVEL did not return to the overworld')

def objects():
    out = []
    for i in range(16):
        obj = SYMS['gObjectEvents'] + 36 * i
        if read(obj, 1) & 1 and not (read(obj + 2, 1) & 1):
            out.append((read(obj + 8, 1), read(obj + 16, 2) - 7, read(obj + 18, 2) - 7))
    return out

def grid():
    lay = read('gMapHeader')
    w, h = read(lay), read(lay + 4)
    bw, buf = read('gBackupMapLayout'), read(SYMS['gBackupMapLayout'] + 8)
    attrs = [read(read(lay + n) + 16) for n in (16, 20)]
    cells = {}
    for y in range(h):
        for x in range(w):
            block = read(buf + 2 * ((y + 7) * bw + x + 7), 2)
            tile = block & 1023
            behavior = read(attrs[tile // 512] + 2 * (tile % 512), 2) & 255
            cells[(x, y)] = block, behavior
    return w, h, cells

def path_to(target):
    name, sx, sy = position()
    _, _, cells = grid()
    occupied = {(x, y) for _, x, y in objects()}
    # 0x2B is reflection under a bridge, not surfable water. The installed
    # Route104 uses it on the walking bridge; retain its actual collision.
    water = set(range(0x10, 0x16)) | {0x18, 0x19, 0x1A, 0x2A}
    warps = set(range(0x60, 0x6F))
    queue = collections.deque([(sx, sy)])
    previous = {(sx, sy): None}
    while queue:
        here = queue.popleft()
        if here == target:
            break
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            nxt = here[0] + dx, here[1] + dy
            if nxt in previous or nxt not in cells or nxt in occupied or (name, here, nxt) in BLOCKED:
                continue
            block, behavior = cells[nxt]
            ledges = {0x38: (1, 0), 0x39: (-1, 0), 0x3A: (0, -1), 0x3B: (0, 1)}
            if behavior in ledges:
                if (dx, dy) != ledges[behavior]:
                    continue
                nxt = here[0] + 2 * dx, here[1] + 2 * dy
                if nxt in previous or nxt not in cells or nxt in occupied or (name, here, nxt) in BLOCKED:
                    continue
                block, behavior = cells[nxt]
            if (((block >> 10) & 3) and not (nxt == target and behavior in warps)) or behavior in water or (behavior in warps and nxt != target):
                continue
            previous[nxt] = here
            queue.append(nxt)
    if target not in previous:
        return None
    path, p = [], target
    while previous[p] is not None:
        path.append(p)
        p = previous[p]
    return list(reversed(path))

def step(dx, dy):
    key = {(0, -1): 64, (1, 0): 16, (0, 1): 128, (-1, 0): 32}[(dx, dy)]
    before = position()
    for _ in range(12):
        act(key, 2, 0)
        if position() != before or not overworld() or read('sLockFieldControls', 1):
            break
    act(0, 1, 20)
    if not overworld() or read('sLockFieldControls', 1):
        settle()
    return before, position()

def go(x, y, limit=400):
    name = position()[0]
    for _ in range(limit):
        current = position()
        if current[0] != name or current[1:] == (x, y):
            return current
        route = path_to((x, y))
        if not route:
            snap('no_path')
            raise RuntimeError(('no path', current, (x, y), objects()))
        nxt = route[0]
        dx, dy = nxt[0] - current[1], nxt[1] - current[2]
        before, after = step((dx > 0) - (dx < 0), (dy > 0) - (dy < 0))
        if after[0] != before[0] or abs(after[1] - nxt[0]) + abs(after[2] - nxt[1]) > 1:
            return after
        if after == before:
            # A transition or preceding movement can briefly reject input.
            # Confirm the obstruction after an idle interval before caching it.
            act(0, 1, 40)
            if position() != before or not overworld() or read('sLockFieldControls', 1):
                if not overworld() or read('sLockFieldControls', 1):
                    settle()
                return position()
            before, after = step((dx > 0) - (dx < 0), (dy > 0) - (dy < 0))
            if after[0] != name or abs(after[1] - nxt[0]) + abs(after[2] - nxt[1]) > 1:
                return after
            if after == before:
                BLOCKED.add((name, current[1:], nxt))
    raise RuntimeError(('walk limit', position(), (x, y)))

def talk(local_id):
    local = constant(local_id) if isinstance(local_id, str) else local_id
    map_name = position()[0]
    for _ in range(12):
        if position()[0] != map_name:
            raise RuntimeError(('map changed before talking', position(), map_name))
        event = next((o for o in objects() if o[0] == local), None)
        if event is None:
            # Object events spawn only within the camera view. Inspect the
            # saved templates to walk near a distant NPC, without spawning it.
            base = read('gSaveBlock1Ptr') + 0xC70
            template = next((base + 24 * i for i in range(64) if read(base + 24 * i, 1) == local), None)
            if template is None:
                raise RuntimeError(('NPC template missing', position(), local))
            x, y = read(template + 4, 2), read(template + 6, 2)
            neighbors = [(x, y + 1), (x - 1, y), (x, y - 1), (x + 1, y)]
            routes = [(len(path), cx, cy) for cx, cy in neighbors if (path := path_to((cx, cy))) is not None]
            if not routes:
                raise RuntimeError(('distant NPC unreachable', position(), local, (x, y)))
            _, cx, cy = min(routes)
            go(cx, cy)
            continue
        _, x, y = event
        options = [(x, y + 1, 64), (x - 1, y, 16), (x, y - 1, 128), (x + 1, y, 32)]
        _, _, cells = grid()
        # The engine permits talking across a counter from two tiles away.
        for cx, cy, key in list(options):
            if cells.get((cx, cy), (0, 0))[1] == 0x80:
                options.append((2 * cx - x, 2 * cy - y, key))
        routes = [(len(p), cx, cy, key) for cx, cy, key in options if (p := path_to((cx, cy))) is not None]
        if not routes:
            raise RuntimeError(('NPC unreachable', position(), event))
        _, cx, cy, key = min(routes)
        go(cx, cy)
        if next((o for o in objects() if o[0] == local), None) != event:
            continue
        act(key, 1, 8)
        act(1, 2, 30)
        settle()
        return
    raise RuntimeError('NPC kept moving')

def cross(next_map):
    name = position()[0]
    info = json.loads((R / 'data/maps' / name / 'map.json').read_text())
    destination = json.loads((R / 'data/maps' / next_map / 'map.json').read_text())
    connection = next((c for c in info['connections'] if c['map'] == destination['id']), None)
    if connection is None:
        raise RuntimeError(('not connected', name, next_map))
    w, h, _ = grid()
    direction, offset = connection['direction'], connection['offset']
    layouts = json.loads((R / 'data/layouts/layouts.json').read_text())['layouts']
    dest = next(l for l in layouts if l['id'] == destination['layout'])
    delta = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}[direction]
    tried = set()
    for _ in range(20):
        choices = []
        for coord in range(w if direction in ('up', 'down') else h):
            if not 0 <= coord - offset < (dest['width'] if direction in ('up', 'down') else dest['height']):
                continue
            edge = (coord, 0 if direction == 'up' else h - 1) if direction in ('up', 'down') else (0 if direction == 'left' else w - 1, coord)
            if edge not in tried and (p := path_to(edge)) is not None:
                choices.append((len(p), edge))
        if not choices:
            snap('connection_blocked')
            raise RuntimeError(('connection blocked', position(), next_map))
        _, edge = min(choices)
        try:
            go(*edge)
        except RuntimeError as error:
            if isinstance(error.args[0], tuple) and error.args[0][0] == 'no path':
                # An NPC may enter the camera view and occupy this boundary
                # after the route was chosen. Try another actual exit tile.
                tried.add(edge)
                continue
            raise
        if position()[0] == next_map:
            return position()
        if position()[1:] == edge:
            step(*delta)
            if position()[0] == next_map:
                return position()
        tried.add(edge)
    raise RuntimeError(('connection attempts', position(), next_map))

def normal_save(name):
    assert overworld() and not read('sLockFieldControls', 1)
    before = read('gSaveCounter')
    act(8, 2, 40)
    cur, count = read('sStartMenuCursorPos', 1), read('sNumStartMenuActions', 1)
    actions = [read(SYMS['sCurrentStartMenuActions'] + i, 1) for i in range(count)]
    target = actions.index(6)  # MENU_ACTION_SAVE
    for _ in range((target - cur) % count):
        act(128, 2, 8)
    act(1, 2, 80)
    for _ in range(300):
        act(1, 2, 16)
        if read('gSaveCounter') > before and overworld() and not read('sLockFieldControls', 1):
            break
    else:
        raise RuntimeError('normal SAVE failed')
    path = Q / ('campaign_' + name + '.sav')
    assert LIB.exportsave(str(path).encode())
    snap(name)
    runs = []
    for keys, count, release in INPUTS:
        if runs and runs[-1][:3] == [keys, count, release]:
            runs[-1][3] += 1
        else:
            runs.append([keys, count, release, 1])
    receipt = metadata() | {'fixture_setup': False, 'game_ram_or_rom_writes': False, 'normal_save_menu': True, 'position': position(), 'party': party(), 'party_sha256': party_sha256(), 'battles': BATTLES,
                            'joypad_actions': len(INPUTS), 'input_encoding': 'keys/count/release/repeats', 'input_runs': runs,
                            'story_vars': {n: var(n) for n in ('VAR_BIRCH_LAB_STATE', 'VAR_LITTLEROOT_TOWN_STATE', 'VAR_PETALBURG_GYM_STATE', 'VAR_PETALBURG_CITY_STATE', 'VAR_PETALBURG_WOODS_STATE', 'VAR_RUSTBORO_CITY_STATE', 'VAR_ROUTE116_STATE', 'VAR_RUSTURF_TUNNEL_STATE', 'VAR_DEVON_CORP_3F_STATE')},
                            'story_flags': {n: flag(n) for n in ('FLAG_DEFEATED_RIVAL_ROUTE103', 'FLAG_SYS_POKEDEX_GET', 'FLAG_RECEIVED_RUNNING_SHOES', 'FLAG_SYS_B_DASH', 'FLAG_BADGE01_GET', 'FLAG_RECEIVED_TM_ROCK_TOMB', 'FLAG_DEVON_GOODS_STOLEN', 'FLAG_RECOVERED_DEVON_GOODS', 'FLAG_RETURNED_DEVON_GOODS', 'FLAG_SYS_POKENAV_GET', 'FLAG_HAS_MATCH_CALL', 'FLAG_DELIVERED_STEVEN_LETTER', 'FLAG_REGISTERED_STEVEN_POKENAV', 'FLAG_RECEIVED_HM_FLASH', 'FLAG_BADGE02_GET', 'FLAG_RECEIVED_TM_BULK_UP')},
                            'inventory_checks': {n: quantity(n) for n in ('ITEM_TM_ROCK_TOMB', 'ITEM_DEVON_GOODS', 'ITEM_LETTER', 'ITEM_POKE_BALL', 'ITEM_HM_FLASH', 'ITEM_TM_STEEL_WING', 'ITEM_TM_BULK_UP')}}
    receipt['story_vars'].update({n: var(n) for n in ('VAR_MAUVILLE_GYM_STATE', 'VAR_SLATEPORT_OUTSIDE_MUSEUM_STATE')})
    receipt['story_flags'].update({n: flag(n) for n in ('FLAG_BADGE03_GET', 'FLAG_DEFEATED_MAUVILLE_GYM', 'FLAG_RECEIVED_TM_SHOCK_WAVE', 'FLAG_ENABLE_WATTSON_MATCH_CALL')})
    receipt['inventory_checks'].update({n: quantity(n) for n in ('ITEM_HM_ROCK_SMASH', 'ITEM_TM_SHOCK_WAVE')})
    receipt['boxed_mons'] = boxed_records()
    receipt['game_stats'] = {'GAME_STAT_USED_ROCK_SMASH': game_stat('GAME_STAT_USED_ROCK_SMASH')}
    (Q / ('campaign_' + name + '_receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    return path
