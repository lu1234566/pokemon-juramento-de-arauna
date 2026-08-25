import unittest

from arauna_qa.state import AraunaStateReader, MAP_OFFSET, OBJECT_EVENT_SIZE
from arauna_qa.symbols import Symbol, SymbolTable


class FakeBridge:
    def __init__(self):
        self.memory = bytearray(0x2000)
        self.base = 0x02000000

    def put(self, address, data):
        start = address - self.base
        self.memory[start : start + len(data)] = data

    def read8(self, address):
        return self.memory[address - self.base]

    def read_range(self, address, length):
        start = address - self.base
        return bytes(self.memory[start : start + length])


class StateReaderTests(unittest.TestCase):
    def test_snapshot_decodes_player_map_script_and_battle_state(self):
        base = 0x02000000
        addresses = {
            "gMain": base + 0x000,
            "gPlayerAvatar": base + 0x500,
            "gObjectEvents": base + 0x600,
            "gMapHeader": base + 0xA00,
            "sGlobalScriptContextStatus": base + 0xB00,
            "sGlobalScriptContext": base + 0xB10,
            "sLockFieldControls": base + 0xB90,
        }
        symbols = SymbolTable(
            {name: Symbol(name=name, address=address) for name, address in addresses.items()}
        )
        bridge = FakeBridge()

        main = bytearray(0x43A)
        main[0x20:0x24] = (1234).to_bytes(4, "little")
        main[0x2C:0x2E] = (0x40).to_bytes(2, "little")
        main[0x2E:0x30] = (0x01).to_bytes(2, "little")
        main[0x439] = 0x02
        main[0:4] = (0x08001234).to_bytes(4, "little")
        main[4:8] = (0x08005678).to_bytes(4, "little")
        bridge.put(addresses["gMain"], main)

        avatar = bytearray(0x24)
        avatar[0] = 0x21
        avatar[2] = 2
        avatar[3] = 1
        avatar[5] = 3
        bridge.put(addresses["gPlayerAvatar"], avatar)

        obj = bytearray(OBJECT_EVENT_SIZE)
        obj[0] = 0x01
        obj[2] = 0x01
        obj[9] = 7
        obj[10] = 2
        obj[11] = 3
        obj[0x10:0x12] = (18 + MAP_OFFSET).to_bytes(2, "little", signed=True)
        obj[0x12:0x14] = (27 + MAP_OFFSET).to_bytes(2, "little", signed=True)
        obj[0x18:0x1A] = (2 | (3 << 4)).to_bytes(2, "little")
        obj[0x1E] = 0x44
        bridge.put(addresses["gObjectEvents"] + 3 * OBJECT_EVENT_SIZE, obj)

        header = bytearray(0x1C)
        header[0x10:0x12] = (321).to_bytes(2, "little")
        header[0x12:0x14] = (99).to_bytes(2, "little")
        header[0x14] = 12
        header[0x16] = 5
        header[0x17] = 3
        bridge.put(addresses["gMapHeader"], header)

        bridge.put(addresses["sGlobalScriptContextStatus"], bytes([1]))
        bridge.put(addresses["sLockFieldControls"], bytes([1]))
        script = bytearray(12)
        script[1] = 1
        script[8:12] = (0x08123456).to_bytes(4, "little")
        bridge.put(addresses["sGlobalScriptContext"], script)

        state = AraunaStateReader(bridge, symbols).snapshot()
        self.assertEqual((state.map_group, state.map_num), (2, 7))
        self.assertEqual((state.player_x, state.player_y), (18, 27))
        self.assertEqual((state.facing, state.movement_direction), (2, 3))
        self.assertTrue(state.script_enabled)
        self.assertTrue(state.field_controls_locked)
        self.assertEqual(state.script_ptr, 0x08123456)
        self.assertTrue(state.in_battle)
        self.assertEqual(state.map_layout_id, 99)


if __name__ == "__main__":
    unittest.main()
