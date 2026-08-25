import unittest

from arauna_qa.battle import BattleMonState, BattleSnapshot
from arauna_qa.battle_advisor import BattleAdvisor, BattleMetadataReader, TYPE_EFFECT_TABLE_SIZE


class Symbols:
    def address(self, name):
        return {"gBattleMoves": 0x1000, "gTypeEffectiveness": 0x2000}[name]


class Bridge:
    def __init__(self):
        self.moves = {
            10: bytes((1, 50, 3, 100, 20, 0, 0, 0, 0)),
            20: bytes((1, 70, 4, 80, 15, 0, 0, 0, 0)),
        }
        table = bytearray(TYPE_EFFECT_TABLE_SIZE)
        table[0:3] = bytes((3, 5, 20))
        table[3:6] = bytes((4, 5, 5))
        table[6:9] = bytes((0xFF, 0, 0))
        self.table = bytes(table)

    def read_range(self, address, length):
        if address == 0x2000:
            return self.table[:length]
        move_id = (address - 0x1000) // 9
        return self.moves[move_id][:length]


class BattleReader:
    def snapshot(self):
        player = BattleMonState(
            battler=0, side="player", species=1, level=10, hp=30, max_hp=40,
            status1=0, status2=0, ability=0, types=(3, 3), item=0,
            moves=(10, 20, 0, 0), pp=(5, 5, 0, 0), attack=20, defense=20,
            speed=20, sp_attack=20, sp_defense=20, stat_stages=(6,) * 8,
        )
        foe = BattleMonState(
            battler=1, side="opponent", species=2, level=10, hp=30, max_hp=40,
            status1=0, status2=0, ability=0, types=(5, 5), item=0,
            moves=(0, 0, 0, 0), pp=(0, 0, 0, 0), attack=20, defense=20,
            speed=20, sp_attack=20, sp_defense=20, stat_stages=(6,) * 8,
        )
        return BattleSnapshot(2, (player, foe))


class AdvisorTests(unittest.TestCase):
    def test_reads_move_and_type_multiplier(self):
        metadata = BattleMetadataReader(Bridge(), Symbols())
        move = metadata.move(10)
        self.assertEqual((move.power, move.type, move.accuracy), (50, 3, 100))
        self.assertEqual(metadata.type_multiplier(3, (5, 5)), 2.0)
        self.assertEqual(metadata.type_multiplier(4, (5, 5)), 0.5)

    def test_recommends_higher_effective_stab_score(self):
        metadata = BattleMetadataReader(Bridge(), Symbols())
        advice = BattleAdvisor(BattleReader(), metadata).recommend()
        self.assertTrue(advice.available)
        self.assertEqual(advice.recommendations[0].move.move_id, 10)
        self.assertGreater(advice.recommendations[0].score, advice.recommendations[1].score)


if __name__ == "__main__":
    unittest.main()
