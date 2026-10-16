"""Read-only choices used in the native second Nara attempt.

Only ordinary move, owned-item and party selections are requested. Activate
explicitly with install(); other trainers always use the controller defaults.
"""
import campaign_controller as c


def active():
    return bool(c.read('gBattleTypeFlags') & 8) and c.read('gTrainerBattleOpponent_A', 2) == c.constant('TRAINER_FLANNERY_1')


def items(battler):
    if not active():
        return None
    p = c.SYMS['gBattleMons'] + 88 * battler
    hp, maximum = c.read(p + 40, 2), c.read(p + 44, 2)
    if c.read(p, 2) == c.constant('SPECIES_ILLUMISE'):
        if hp < 42 and maximum - hp >= 40 and c.quantity('ITEM_SUPER_POTION'):
            return 'ITEM_SUPER_POTION', c.read(p + 72)
        if c.read(p + 76) & c.constant('STATUS1_BURN') and c.quantity('ITEM_LAVA_COOKIE'):
            return 'ITEM_LAVA_COOKIE', c.read(p + 72)
    return None


def moves(battler):
    if not active():
        return None
    p = c.SYMS['gBattleMons'] + 88 * battler
    enemy = c.living_enemy()
    e = c.SYMS['gBattleMons'] + 88 * enemy
    available = {c.read(p + 12 + 2 * slot, 2): slot for _, slot in c.move_options(battler)}
    def slot(name):
        return available.get(c.constant(name))
    if slot('MOVE_SYNTHESIS') is not None and c.read(p + 40, 2) * 2 < c.read(p + 44, 2):
        return slot('MOVE_SYNTHESIS')
    if slot('MOVE_LEECH_SEED') is not None and not c.read(c.SYMS['gStatuses3'] + 4 * enemy) & c.constant('STATUS3_LEECHSEED'):
        return slot('MOVE_LEECH_SEED')
    if slot('MOVE_CONFUSE_RAY') is not None and c.read(e + 40, 2) > 25 and not c.read(e + 80) & c.constant('STATUS2_CONFUSION'):
        return slot('MOVE_CONFUSE_RAY')
    return None


def replacement(alive):
    if active():
        mons = c.party()
        for species in ('ILLUMISE', 'FARFETCHD', 'COMBUSKEN', 'WYNAUT', 'NIDORAN_F'):
            choices = [i for i in alive if mons[i]['species'] == c.constant('SPECIES_' + species)]
            if choices:
                return max(choices, key=lambda i: mons[i]['hp'])
    return alive[0]


def install():
    c.ITEM_POLICY = items
    c.MOVE_POLICY = moves
    c.PARTY_POLICY = replacement
