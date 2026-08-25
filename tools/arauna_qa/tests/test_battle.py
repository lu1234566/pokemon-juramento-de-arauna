import unittest

from arauna_qa.battle import BATTLE_MON_SIZE, MAX_BATTLERS, BattleReader


class Symbol:
    def __init__(self, address):
        self.address = address


class Symbols:
    def address(self, name):
        return {"gBattleMons": 0x1000}[name]
    def get(self, name):
        return {
            "gBattlersCount": Symbol(0x2000),
            "gBattlerPositions": Symbol(0x3000),
        }.get(name)


class Bridge:
    def __init__(self):
        self.raw = bytearray(MAX_BATTLERS * BATTLE_MON_SIZE)
        d = bytearray(BATTLE_MON_SIZE)
        d[0:2] = (25).to_bytes(2, "little")
        d[2:4] = (50).to_bytes(2, "little")
        d[0x0C:0x14] = b"".join(x.to_bytes(2, "little") for x in (10, 20, 30, 40))
        d[0x20] = 7
        d[0x21:0x23] = bytes((3, 4))
        d[0x24:0x28] = bytes((5, 6, 7, 8))
        d[0x28:0x2A] = (30).to_bytes(2, "little")
        d[0x2A] = 12
        d[0x2C:0x2E] = (40).to_bytes(2, "little")
        self.raw[:BATTLE_MON_SIZE] = d
    def read8(self, address):
        return 1
    def read_range(self, address, length):
        if address == 0x3000:
            return bytes((0, 1, 2, 3))[:length]
        return bytes(self.raw[:length])


class BattleTests(unittest.TestCase):
    def test_decodes_active_battle_mon(self):
        snap = BattleReader(Bridge(), Symbols()).snapshot()
        self.assertEqual(snap.battlers_count, 1)
        mon = snap.mons[0]
        self.assertEqual(mon.side, "player")
        self.assertEqual(mon.species, 25)
        self.assertEqual(mon.moves, (10, 20, 30, 40))
        self.assertEqual(mon.pp, (5, 6, 7, 8))
        self.assertEqual((mon.level, mon.hp, mon.max_hp), (12, 30, 40))


if __name__ == "__main__":
    unittest.main()
