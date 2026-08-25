import unittest

from arauna_qa.objects import MAP_OFFSET, OBJECT_EVENT_COUNT, OBJECT_EVENT_SIZE, ObjectEventReader


class Symbols:
    def address(self, name):
        return 0x02000000


class Bridge:
    def __init__(self, raw):
        self.raw = raw

    def read_range(self, address, length):
        return bytes(self.raw[:length])


class ObjectReaderTests(unittest.TestCase):
    def test_decodes_runtime_object_coordinates_and_flags(self):
        raw = bytearray(OBJECT_EVENT_COUNT * OBJECT_EVENT_SIZE)
        off = 3 * OBJECT_EVENT_SIZE
        raw[off + 0x00] = 0x01
        raw[off + 0x05] = 44
        raw[off + 0x06] = 7
        raw[off + 0x07] = 2
        raw[off + 0x08] = 9
        raw[off + 0x09] = 5
        raw[off + 0x0A] = 1
        raw[off + 0x0B] = 3
        for pos, value in ((0x0C, 10), (0x0E, 11), (0x10, 12), (0x12, 13), (0x14, 11), (0x16, 13)):
            raw[off + pos: off + pos + 2] = int(value + MAP_OFFSET).to_bytes(2, "little", signed=True)
        raw[off + 0x18:off + 0x1A] = (2 | (4 << 4)).to_bytes(2, "little")
        raw[off + 0x1E] = 0x55

        reader = ObjectEventReader(Bridge(raw), Symbols())
        obj = reader.snapshot()[3]
        self.assertTrue(obj.active)
        self.assertFalse(obj.is_player)
        self.assertEqual(obj.local_id, 9)
        self.assertEqual(obj.position, (12, 13))
        self.assertEqual(obj.initial_x, 10)
        self.assertEqual(obj.previous_x, 11)
        self.assertEqual(obj.facing_direction, 2)
        self.assertEqual(obj.movement_direction, 4)
        self.assertEqual(obj.current_metatile_behavior, 0x55)

    def test_active_on_map_filters_player_and_other_maps(self):
        raw = bytearray(OBJECT_EVENT_COUNT * OBJECT_EVENT_SIZE)
        for index, (is_player, group, num) in enumerate(((False, 0, 1), (True, 0, 1), (False, 2, 1))):
            off = index * OBJECT_EVENT_SIZE
            raw[off] = 1
            raw[off + 2] = 1 if is_player else 0
            raw[off + 9] = num
            raw[off + 10] = group
        reader = ObjectEventReader(Bridge(raw), Symbols())
        objs = reader.active_on_map(0, 1)
        self.assertEqual([obj.index for obj in objs], [0])


if __name__ == "__main__":
    unittest.main()
