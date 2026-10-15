"""Read-only choices for the native Olivia campaign journey."""
from campaign_controller import *


def enemy_species():
    e = SYMS['gBattleMons'] + 88
    if read(e + 40, 2):
        return read(e, 2)
    # The switch prompt announces the incoming species before loading it.
    slot = read(read('gBattleStruct') + 0x5C + 1, 1)
    assert slot < 6
    p = SYMS['gEnemyParty'] + 100 * slot
    personality, ot = read(p), read(p + 4)
    growth = ORDERS[personality % 24][0] * 12
    return (read(p + 32 + growth) ^ personality ^ ot) & 65535


def preferences():
    kind = enemy_species()
    if kind == constant('SPECIES_PILOSWINE'):
        names = ['ABSOL', 'NIDORAN_F', 'ILLUMISE', 'COMBUSKEN']
    elif kind == constant('SPECIES_SMEARGLE'):
        names = ['ABSOL', 'ILLUMISE', 'COMBUSKEN', 'NIDORAN_F']
    else:
        names = ['ILLUMISE', 'COMBUSKEN', 'FARFETCHD', 'NIDORAN_F', 'ABSOL']
    return [constant('SPECIES_' + name) for name in names]


def switch_prompt():
    mons = party()
    desired = next((species for species in preferences()
                    if any(mon['species'] == species and mon['hp'] for mon in mons)), None)
    if enemy_species() == constant('SPECIES_SMEARGLE') and read('gBattleMons', 2) == constant('SPECIES_ABSOL'):
        if read(SYMS['gBattleMons'] + 80) & constant('STATUS2_DESTINY_BOND'):
            return False
        return any(mon['species'] == desired and mon['hp'] > read(SYMS['gBattleMons'] + 40, 2) for mon in mons)
    return desired is not None and read('gBattleMons', 2) != desired


def replacement(alive):
    mons = party()
    for species in preferences():
        matches = [index for index in alive if mons[index]['species'] == species]
        if matches:
            return max(matches, key=lambda index: mons[index]['hp'])
    return alive[0]

def action(battler):
    p = SYMS['gBattleMons'] + 88 * battler
    # Olivia may switch voluntarily to her Bug counter before Arraia faints.
    if enemy_species() == constant('SPECIES_TAUROS') and read(p, 2) in (constant('SPECIES_ABSOL'), constant('SPECIES_NIDORAN_F')):
        if any(mon['species'] in (constant('SPECIES_ILLUMISE'), constant('SPECIES_COMBUSKEN')) and mon['hp'] for mon in party()):
            return 2
    return None

def items(battler):
    p = SYMS['gBattleMons'] + 88 * battler
    kind = enemy_species()
    if read(p + 76) & constant('STATUS1_PARALYSIS') and quantity('ITEM_PARALYZE_HEAL'):
        return ('ITEM_PARALYZE_HEAL', read(p + 72))
    counter = next((mon for mon in party() if mon['species'] == constant('SPECIES_ILLUMISE')), None)
    if not counter or not counter['hp']:
        return None
    if kind == constant('SPECIES_PILOSWINE') and counter['max_hp'] - counter['hp'] >= 25 and quantity('ITEM_SUPER_POTION'):
        return ('ITEM_SUPER_POTION', counter['personality'])
    if read(p, 2) == constant('SPECIES_ILLUMISE'):
        if read(p + 40, 2) < 38 and quantity('ITEM_SUPER_POTION'):
            return ('ITEM_SUPER_POTION', counter['personality'])
        if kind == constant('SPECIES_TAUROS') and read(p + 27, 1) == 6 and quantity('ITEM_X_SPEED'):
            return ('ITEM_X_SPEED', None)
    return None


def moves(battler):
    p = SYMS['gBattleMons'] + 88 * battler
    enemy = living_enemy()
    e = SYMS['gBattleMons'] + 88 * enemy
    available = {read(p + 12 + 2 * i, 2): i for i in range(4) if read(p + 36 + i, 1)}
    def slot(name):
        return available.get(constant(name))
    if read(e, 2) == constant('SPECIES_SMEARGLE') and slot('MOVE_DESTINY_BOND') is not None:
        return slot('MOVE_DESTINY_BOND')
    if (read(e, 2) == constant('SPECIES_PILOSWINE') and read(e + 40, 2) <= 20
            and read(SYMS['gStatuses3'] + 4 * enemy) & constant('STATUS3_LEECHSEED')
            and slot('MOVE_DESTINY_BOND') is not None):
        return slot('MOVE_DESTINY_BOND')
    if read(p + 40, 2) * 2 < read(p + 44, 2) and slot('MOVE_SYNTHESIS') is not None:
        return slot('MOVE_SYNTHESIS')
    if (slot('MOVE_LEECH_SEED') is not None
            and constant('TYPE_GRASS') not in {read(e + 33, 1), read(e + 34, 1)}
            and not read(SYMS['gStatuses3'] + 4 * enemy) & constant('STATUS3_LEECHSEED')):
        return slot('MOVE_LEECH_SEED')
    if read(e + 40, 2) > 20 and slot('MOVE_CONFUSE_RAY') is not None and not read(e + 80) & constant('STATUS2_CONFUSION'):
        return slot('MOVE_CONFUSE_RAY')
    return None
