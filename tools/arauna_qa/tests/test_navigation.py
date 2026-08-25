import unittest
from dataclasses import replace

from arauna_qa.navigation import Navigator
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


if __name__ == "__main__":
    unittest.main()
