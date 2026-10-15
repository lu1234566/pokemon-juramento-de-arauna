"""Explicit normal-input strategy for Dalva; never changes game state directly."""
import campaign_controller as c


def move_policy(battler):
    if c.read('gTrainerBattleOpponent_A', 2) != c.constant('TRAINER_ROXANNE_1') or not c.read('gBattleTypeFlags') & 8:
        return None
    player, enemy = c.SYMS['gBattleMons'] + 88 * battler, c.SYMS['gBattleMons'] + 88
    moves = [c.read(player + 12 + 2 * i, 2) for i in range(4)]
    available = {move: i for i, move in enumerate(moves) if c.read(player + 36 + i, 1)}
    species = c.read(enemy, 2)
    bond = c.constant('MOVE_DESTINY_BOND')
    if species in (c.constant('SPECIES_WOBBUFFET'), c.constant('SPECIES_DUNSPARCE')) and bond in available:
        return available[bond]
    burn, growth = c.constant('MOVE_WILL_O_WISP'), c.constant('MOVE_GROWTH')
    hp, maximum = c.read(player + 40, 2), c.read(player + 44, 2)
    if burn in available and not c.read(enemy + 76) & 16 and hp * 5 > maximum * 3:
        return available[burn]
    target_stage = 8 if species == c.constant('SPECIES_HOPPIP') else 12
    if growth in available and c.read(player + 28, 1) < target_stage and hp * 5 > maximum * 3:
        return available[growth]
    return None


def party_policy(alive):
    enemy = c.read(c.SYMS['gBattleMons'] + 88, 2)
    if enemy in (c.constant('SPECIES_WOBBUFFET'), c.constant('SPECIES_DUNSPARCE')):
        candidates = [i for i in alive if c.constant('MOVE_DESTINY_BOND') in c.party()[i]['moves']]
        if candidates:
            return candidates[0]
    return alive[0]
