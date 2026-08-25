import unittest

from arauna_qa.party import PARTY_SIZE, POKEMON_SIZE, PartyReader, SUBSTRUCT_ORDERS


def build_mon(personality=1, ot_id=0x11223344):
    growth = bytearray(12)
    growth[0:2] = (25).to_bytes(2, "little")
    growth[2:4] = (100).to_bytes(2, "little")
    growth[4:8] = (12345).to_bytes(4, "little")
    growth[9] = 200

    attacks = bytearray(12)
    for i, move in enumerate((10, 20, 30, 40)):
        attacks[i*2:i*2+2] = move.to_bytes(2, "little")
    attacks[8:12] = bytes((5, 6, 7, 8))

    evs = bytearray(12)
    misc = bytearray(12)
    misc[4:8] = ((1 << 31) | (1 << 30)).to_bytes(4, "little")

    source = {"G": growth, "A": attacks, "E": evs, "M": misc}
    order = SUBSTRUCT_ORDERS[personality % 24]
    decrypted = b"".join(source[label] for label in order)
    checksum = sum(
        int.from_bytes(decrypted[i:i+2], "little")
        for i in range(0, 48, 2)
    ) & 0xFFFF

    raw = bytearray(POKEMON_SIZE)
    raw[0:4] = personality.to_bytes(4, "little")
    raw[4:8] = ot_id.to_bytes(4, "little")
    raw[0x13] = 0x02
    raw[0x1C:0x1E] = checksum.to_bytes(2, "little")
    key = personality ^ ot_id
    for i in range(0, 48, 4):
        word = int.from_bytes(decrypted[i:i+4], "little") ^ key
        raw[0x20+i:0x24+i] = word.to_bytes(4, "little")

    raw[0x50:0x54] = (0x1234).to_bytes(4, "little")
    raw[0x54] = 12
    for offset, value in ((0x56, 30), (0x58, 40), (0x5A, 50), (0x5C, 60), (0x5E, 70), (0x60, 80), (0x62, 90)):
        raw[offset:offset+2] = value.to_bytes(2, "little")
    return bytes(raw)


class Symbols:
    def __init__(self):
        self.addresses = {"gPlayerParty": 0x1000, "gPlayerPartyCount": 0x2000}
    def address(self, name):
        return self.addresses[name]


class Bridge:
    def __init__(self):
        self.party = build_mon() + bytes((PARTY_SIZE - 1) * POKEMON_SIZE)
    def read8(self, address):
        return 1
    def read_range(self, address, length):
        return self.party[:length]


class PartyTests(unittest.TestCase):
    def test_decrypts_shuffled_secure_substructs(self):
        mon = PartyReader.decode_mon(0, build_mon())
        self.assertTrue(mon.present)
        self.assertTrue(mon.checksum_ok)
        self.assertEqual(mon.species, 25)
        self.assertEqual(mon.moves, (10, 20, 30, 40))
        self.assertEqual(mon.pp, (5, 6, 7, 8))
        self.assertTrue(mon.is_egg)
        self.assertEqual(mon.ability_num, 1)
        self.assertEqual((mon.level, mon.hp, mon.max_hp), (12, 30, 40))

    def test_reads_player_party_count(self):
        snap = PartyReader(Bridge(), Symbols()).player()
        self.assertEqual(snap.count, 1)
        self.assertEqual(snap.mons[0].species, 25)


if __name__ == "__main__":
    unittest.main()
