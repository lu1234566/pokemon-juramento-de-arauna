"""Normal-joypad combat choices for the prepared second-gym campaign team."""
import campaign_controller as c


def is_ademar():
    return bool(c.read('gBattleTypeFlags') & 8) and c.read('gTrainerBattleOpponent_A', 2) == c.constant('TRAINER_BRAWLY_1')


def move_policy(battler):
    if not is_ademar():
        return None
    p, e = c.SYMS['gBattleMons'] + 88 * battler, c.SYMS['gBattleMons'] + 88
    available = {c.read(p + 12 + 2 * i, 2): i for i in range(4) if c.read(p + 36 + i, 1)}
    enemy, hp, maximum = c.read(e, 2), c.read(p + 40, 2), c.read(p + 44, 2)
    bond = c.constant('MOVE_DESTINY_BOND')
    if enemy in (c.constant('SPECIES_KINGDRA'), c.constant('SPECIES_LARVITAR')) and bond in available:
        return available[bond]
    seed, synthesis, confuse = [c.constant('MOVE_' + n) for n in ('LEECH_SEED', 'SYNTHESIS', 'CONFUSE_RAY')]
    if synthesis in available and hp * 5 < maximum * 3:
        return available[synthesis]
    if seed in available and not c.read(c.SYMS['gStatuses3'] + 4) & c.constant('STATUS3_LEECHSEED'):
        return available[seed]
    if confuse in available and not c.read(e + 80) & c.constant('STATUS2_CONFUSION') and hp * 2 > maximum and c.read(e + 40, 2) * 2 > c.read(e + 44, 2):
        return available[confuse]
    return None


def party_policy(alive):
    if not is_ademar():
        return alive[0]
    enemy, mons = c.read(c.SYMS['gBattleMons'] + 88, 2), c.party()
    if enemy == c.constant('SPECIES_DROWZEE'):
        candidates = [i for i in alive if mons[i]['species'] == c.constant('SPECIES_NIDORAN_F')]
    elif enemy == c.constant('SPECIES_LARVITAR'):
        candidates = [i for i in alive if c.constant('MOVE_DESTINY_BOND') in mons[i]['moves']]
    else:
        candidates = [i for i in alive if mons[i]['species'] == c.constant('SPECIES_FARFETCHD')]
    return max(candidates or alive, key=lambda i: mons[i]['hp'])
