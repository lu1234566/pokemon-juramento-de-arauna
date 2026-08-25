import unittest
from types import SimpleNamespace

from arauna_qa.scenario import ScenarioRunner
from arauna_qa.state import AraunaState


def state(map_num=0, x=1, y=2, battle=False, script=False):
    return AraunaState(
        frame=1, map_group=0, map_num=map_num, map_layout_id=1, region_map_section_id=1,
        map_type=1, weather=0, music=1, player_valid=True, player_x=x, player_y=y,
        player_x_internal=x+7, player_y_internal=y+7, facing=1, movement_direction=1,
        elevation=3, metatile_behavior=0, avatar_flags=1, running_state=0,
        tile_transition_state=0, field_controls_locked=False, script_enabled=script,
        script_mode=0, script_ptr=0, in_battle=battle, held_keys=0, new_keys=0,
        callback1=0, callback2=0,
    )


class Reader:
    def __init__(self):
        self.value = state()
    def snapshot(self):
        return self.value


class Bridge:
    def __init__(self):
        self.presses = []
        self.shots = []
    def press(self, key, frames=2):
        self.presses.append((key, frames))
    def screenshot(self, path):
        self.shots.append(path)


class Navigator:
    def __init__(self):
        self.reader = Reader()
        self.bridge = Bridge()
    def walk_to(self, x, y, max_steps=256):
        self.reader.value = state(x=x, y=y)
        s = self.reader.value
        return SimpleNamespace(reached=True, reason="reached", final_state=s, to_dict=lambda: {"reached": True})


class WorldNav:
    def __init__(self, nav):
        self.nav = nav
    def route_to(self, target):
        s = self.nav.reader.snapshot()
        return SimpleNamespace(reached=True, reason="already_there", final_state=s, to_dict=lambda: {"reached": True})


class Npc:
    def __init__(self, nav):
        self.nav = nav
        self.calls = []
    def interact(self, **kwargs):
        self.calls.append(kwargs)
        s = self.nav.reader.snapshot()
        return SimpleNamespace(success=True, reason="script_started", final_state=s, to_dict=lambda: {"success": True})


class BattleAutoplayer:
    def __init__(self, nav):
        self.nav = nav
        self.calls = []
    def run(self, **kwargs):
        self.calls.append(kwargs)
        self.nav.reader.value = state(battle=False)
        s = self.nav.reader.value
        return SimpleNamespace(
            success=True,
            reason="battle_ended",
            final_state=s,
            to_dict=lambda: {"success": True, "reason": "battle_ended"},
        )


class MapDef:
    id = "MAP_A"


class Index:
    def from_runtime(self, group, num):
        return MapDef() if (group, num) == (0, 0) else None
    def require(self, key):
        if key not in {"MAP_A", "A"}:
            raise KeyError(key)
        return MapDef()


class ScenarioTests(unittest.TestCase):
    def test_runs_press_wait_talk_and_assert(self):
        nav = Navigator()
        npc = Npc(nav)
        runner = ScenarioRunner(nav, WorldNav(nav), npc, Index())
        result = runner.run({
            "name": "intro",
            "steps": [
                {"action": "press", "key": "A"},
                {"action": "wait", "frames": 3},
                {"action": "talk", "local_id": 7},
                {"action": "assert", "map": "MAP_A", "in_battle": False},
            ],
        })
        self.assertTrue(result.success)
        self.assertEqual(nav.bridge.presses, [("A", 2), (0, 3)])
        self.assertEqual(npc.calls, [{"local_id": 7}])

    def test_runs_bounded_battle_step(self):
        nav = Navigator()
        nav.reader.value = state(battle=True)
        autoplay = BattleAutoplayer(nav)
        runner = ScenarioRunner(
            nav, WorldNav(nav), Npc(nav), Index(), battle_autoplayer=autoplay
        )
        result = runner.run({
            "name": "battle",
            "steps": [
                {"action": "assert", "in_battle": True},
                {"action": "play_battle", "max_turns": 12, "stall_cycles": 9},
                {"action": "assert", "in_battle": False},
            ],
        })
        self.assertTrue(result.success)
        self.assertEqual(autoplay.calls, [{
            "max_turns": 12,
            "max_cycles": 1024,
            "wait_frames": 4,
            "stall_cycles": 9,
        }])

    def test_battle_step_requires_autoplayer(self):
        nav = Navigator()
        nav.reader.value = state(battle=True)
        runner = ScenarioRunner(nav, WorldNav(nav), Npc(nav), Index())
        result = runner.run({"steps": [{"action": "play_battle"}]})
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "battle_autoplayer_unavailable")

    def test_stops_on_failed_assert(self):
        nav = Navigator()
        runner = ScenarioRunner(nav, WorldNav(nav), Npc(nav), Index())
        result = runner.run({
            "steps": [
                {"action": "assert", "player_x": 99},
                {"action": "press", "key": "A"},
            ]
        })
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "player_x_mismatch")
        self.assertEqual(nav.bridge.presses, [])


if __name__ == "__main__":
    unittest.main()
