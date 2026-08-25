import unittest
from dataclasses import replace

from arauna_qa.navigation import Navigator
from arauna_qa.repo_map import CollisionGrid, MapDefinition
from arauna_qa.state import AraunaState


def state(**changes):
    base = AraunaState(
        frame=1,
        map_group=0,
        map_num=9,
        map_layout_id=1,
        region_map_section_id=1,
        map_type=1,
        weather=0,
        music=1,
        player_valid=True,
        player_x=5,
        player_y=5,
        player_x_internal=12,
        player_y_internal=12,
        facing=1,
        movement_direction=1,
        elevation=3,
        metatile_behavior=0,
        avatar_flags=1,
        running_state=0,
        tile_transition_state=0,
        field_controls_locked=False,
        script_enabled=False,
        script_mode=0,
        script_ptr=0,
        in_battle=False,
        held_keys=0,
        new_keys=0,
        callback1=0,
        callback2=0,
    )
    return replace(base, **changes)


class FakeBridge:
    def __init__(self):
        self.presses = []

    def press(self, direction, frames=1):
        self.presses.append((direction, frames))


class FakeReader:
    def __init__(self, states):
        self.states = list(states)
        self.last = self.states[-1]

    def snapshot(self):
        if self.states:
            self.last = self.states.pop(0)
        return self.last


def make_grid(width, height, blocked=()):
    blocked = set(blocked)
    cells = []
    for y in range(height):
        for x in range(width):
            collision = 1 if (x, y) in blocked else 0
            cells.append((collision << 10) | (3 << 12))
    return CollisionGrid(width, height, tuple(cells))


class FakeWorld:
    def __init__(self, x=0, y=1, dynamic=(), warp=None):
        self.x = x
        self.y = y
        self.dynamic = set(dynamic)
        self.warp = warp
        self.frame = 1
        self.group = 0
        self.number = 0

    def snapshot(self):
        return state(
            frame=self.frame,
            map_group=self.group,
            map_num=self.number,
            player_x=self.x,
            player_y=self.y,
            player_x_internal=self.x + 7,
            player_y_internal=self.y + 7,
        )

    def move(self, direction):
        dx, dy = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}[direction]
        nxt = (self.x + dx, self.y + dy)
        self.frame += 1
        if nxt in self.dynamic:
            return
        self.x, self.y = nxt
        if self.warp is not None and nxt == self.warp:
            self.group = 1
            self.number = 0
            self.x = 0
            self.y = 0


class WorldBridge:
    def __init__(self, world):
        self.world = world
        self.presses = []

    def press(self, direction, frames=1):
        self.presses.append((direction, frames))
        self.world.move(direction)


class WorldReader:
    def __init__(self, world):
        self.world = world

    def snapshot(self):
        return self.world.snapshot()


class FakeMapIndex:
    def __init__(self, grid):
        self.grid = grid

    def from_runtime(self, group, number):
        if (group, number) != (0, 0):
            return None
        return MapDefinition("MAP_TEST", "Test", "LAYOUT_TEST", "Test", 0, 0, (), (), (), (), ())

    def load_collision_grid(self, map_def):
        return self.grid


class NavigationTests(unittest.TestCase):
    def test_step_confirms_tile_move_after_transition_settles(self):
        before = state()
        moving = state(frame=2, player_y=4, player_y_internal=11, tile_transition_state=1)
        settled = state(frame=3, player_y=4, player_y_internal=11, tile_transition_state=0)
        bridge = FakeBridge()
        nav = Navigator(bridge, FakeReader([before, moving, settled]))
        result = nav.step("up")
        self.assertTrue(result.moved)
        self.assertFalse(result.blocked)
        self.assertEqual(result.position_after, (5, 4))
        self.assertEqual(bridge.presses, [("UP", 1)])

    def test_step_marks_unchanged_position_as_blocked(self):
        before = state()
        bridge = FakeBridge()
        nav = Navigator(bridge, FakeReader([before] + [state(frame=i + 2) for i in range(8)]))
        result = nav.step("LEFT")
        self.assertFalse(result.moved)
        self.assertTrue(result.blocked)

    def test_step_detects_warp_as_map_change(self):
        before = state()
        warped = state(frame=2, map_group=1, map_num=4, player_x=2, player_y=3)
        nav = Navigator(FakeBridge(), FakeReader([before, warped]))
        result = nav.step("DOWN")
        self.assertTrue(result.moved)
        self.assertTrue(result.map_changed)

    def test_rejects_navigation_in_battle(self):
        nav = Navigator(FakeBridge(), FakeReader([state(in_battle=True)]))
        with self.assertRaisesRegex(RuntimeError, "battle"):
            nav.step("UP")

    def test_plan_path_avoids_static_collision(self):
        grid = make_grid(5, 3, {(2, 1)})
        path = Navigator.plan_path(grid, (0, 1), (4, 1))
        self.assertIsNotNone(path)
        pos = (0, 1)
        for direction in path:
            dx, dy = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}[direction]
            pos = (pos[0] + dx, pos[1] + dy)
            self.assertNotEqual(pos, (2, 1))
        self.assertEqual(pos, (4, 1))

    def test_walk_to_replans_around_dynamic_blocker(self):
        grid = make_grid(5, 3)
        world = FakeWorld(dynamic={(2, 1)})
        nav = Navigator(WorldBridge(world), WorldReader(world), max_polls=2, map_index=FakeMapIndex(grid))
        result = nav.walk_to(4, 1, max_steps=20)
        self.assertTrue(result.reached)
        self.assertEqual((result.final_state.player_x, result.final_state.player_y), (4, 1))
        self.assertIn((2, 1), result.blocked_tiles)
        self.assertGreaterEqual(result.replans, 1)

    def test_walk_to_stops_when_a_warp_changes_map(self):
        grid = make_grid(5, 3)
        world = FakeWorld(warp=(1, 1))
        nav = Navigator(WorldBridge(world), WorldReader(world), max_polls=2, map_index=FakeMapIndex(grid))
        result = nav.walk_to(4, 1, max_steps=20)
        self.assertFalse(result.reached)
        self.assertTrue(result.map_changed)
        self.assertEqual(result.reason, "map_changed")

    def test_walk_to_rejects_out_of_bounds_target(self):
        grid = make_grid(5, 3)
        world = FakeWorld()
        nav = Navigator(WorldBridge(world), WorldReader(world), map_index=FakeMapIndex(grid))
        with self.assertRaises(ValueError):
            nav.walk_to(9, 9)


if __name__ == "__main__":
    unittest.main()
