import unittest

from arauna_qa.interaction import NpcInteractor
from arauna_qa.navigation import MoveResult
from arauna_qa.objects import ObjectEventState
from arauna_qa.repo_map import CollisionGrid, MapDefinition
from arauna_qa.state import AraunaState


def state(x=0, y=1, script=False, locked=False, battle=False, frame=1):
    return AraunaState(
        frame=frame, map_group=0, map_num=0, map_layout_id=1, region_map_section_id=1,
        map_type=1, weather=0, music=1, player_valid=True, player_x=x, player_y=y,
        player_x_internal=x+7, player_y_internal=y+7, facing=4, movement_direction=4,
        elevation=3, metatile_behavior=0, avatar_flags=1, running_state=0,
        tile_transition_state=0, field_controls_locked=locked, script_enabled=script,
        script_mode=0, script_ptr=0, in_battle=battle, held_keys=0, new_keys=0,
        callback1=0, callback2=0,
    )


def npc(x=2, y=1):
    return ObjectEventState(
        index=3, active=True, is_player=False, frozen=False, invisible=False, local_id=7,
        map_num=0, map_group=0, graphics_id=10, movement_type=0, trainer_type=0,
        elevation=3, initial_x=2, initial_y=1, current_x=x, current_y=y,
        previous_x=x, previous_y=y, facing_direction=3, movement_direction=3,
        current_metatile_behavior=0,
    )


class World:
    def __init__(self):
        self.x = 0
        self.y = 1
        self.script = False
        self.frame = 1

    def snapshot(self):
        return state(self.x, self.y, script=self.script, locked=self.script, frame=self.frame)


class Bridge:
    def __init__(self, world):
        self.world = world
        self.presses = []

    def press(self, key, frames=1):
        self.presses.append((key, frames))
        if key == "A":
            self.world.script = True
            self.world.frame += 1


class Reader:
    def __init__(self, world):
        self.world = world

    def snapshot(self):
        return self.world.snapshot()


class Nav:
    def __init__(self, world):
        self.world = world
        self.reader = Reader(world)
        self.bridge = Bridge(world)

    def step(self, direction, press_frames=1):
        before = self.reader.snapshot()
        moved = False
        if direction == "RIGHT" and self.world.x < 1:
            self.world.x += 1
            moved = True
        self.world.frame += 1
        after = self.reader.snapshot()
        return MoveResult(direction, before, after, moved, False, not moved, 1)


class Symbols:
    def get(self, name):
        return None


class Objects:
    def __init__(self, bridge):
        self.bridge = bridge
        self.symbols = Symbols()

    def active_on_map(self, group, num, **kwargs):
        return (npc(),)

    def find_index(self, index):
        return npc() if index == 3 else None

    def find_local_id(self, local_id, group, num):
        return npc() if local_id == 7 else None


class Index:
    def __init__(self):
        self.map = MapDefinition("MAP_A", "A", "LAYOUT_A", "A", 0, 0, (), (), (), (), ())

    def from_runtime(self, group, num):
        return self.map if (group, num) == (0, 0) else None

    def load_collision_grid(self, map_def):
        return CollisionGrid(4, 3, tuple(3 << 12 for _ in range(12)))


class InteractionTests(unittest.TestCase):
    def test_approaches_faces_and_starts_script(self):
        world = World()
        nav = Nav(world)
        interactor = NpcInteractor(nav, Objects(nav.bridge), Index())
        result = interactor.interact(object_index=3)
        self.assertTrue(result.success)
        self.assertIn(result.reason, {"script_started", "controls_locked"})
        self.assertEqual((world.x, world.y), (1, 1))
        self.assertIn(("A", 2), nav.bridge.presses)

    def test_lists_current_runtime_objects(self):
        world = World()
        nav = Nav(world)
        interactor = NpcInteractor(nav, Objects(nav.bridge), Index())
        objs = interactor.list_current()
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].local_id, 7)


if __name__ == "__main__":
    unittest.main()
