import unittest
from types import SimpleNamespace

from arauna_qa.battle_loop import BattleAutoplayer
from arauna_qa.state import AraunaState


def state(in_battle=True):
    return AraunaState(
        frame=1, map_group=0, map_num=0, map_layout_id=1, region_map_section_id=1,
        map_type=1, weather=0, music=1, player_valid=True, player_x=1, player_y=1,
        player_x_internal=8, player_y_internal=8, facing=1, movement_direction=1,
        elevation=3, metatile_behavior=0, avatar_flags=1, running_state=0,
        tile_transition_state=0, field_controls_locked=False, script_enabled=False,
        script_mode=0, script_ptr=0, in_battle=in_battle, held_keys=0, new_keys=0,
        callback1=0, callback2=0,
    )


class StateReader:
    def __init__(self):
        self.in_battle = True
    def snapshot(self):
        return state(self.in_battle)


class Menu:
    def __init__(self, reader, has_prompt=True, raw_prompts=()):
        self.reader = reader
        self.has_prompt = has_prompt
        self.raw_prompts = tuple(raw_prompts)
    def player_prompt(self):
        if self.reader.in_battle and self.has_prompt:
            return SimpleNamespace()
        return None
    def prompts(self):
        return self.raw_prompts


class Input:
    def __init__(self, reader):
        self.reader = reader
        self.calls = 0
    def choose_recommended(self):
        self.calls += 1
        self.reader.in_battle = False
        return SimpleNamespace(success=True, reason="move_submitted", to_dict=lambda: {"success": True})


class BattleReader:
    def snapshot(self):
        return SimpleNamespace(mons=())


class Bridge:
    def __init__(self):
        self.waits = []
    def press(self, keys, frames=2):
        self.waits.append((keys, frames))


def raw_prompt(command):
    return SimpleNamespace(
        battler=0,
        side="player",
        controller_active=True,
        command=command,
        action_cursor=0,
        move_cursor=0,
        to_dict=lambda: {"battler": 0, "side": "player", "command": command},
    )


class BattleLoopTests(unittest.TestCase):
    def test_submits_known_prompt_then_observes_battle_end(self):
        reader = StateReader()
        menu = Menu(reader, True)
        inp = Input(reader)
        loop = BattleAutoplayer(Bridge(), reader, BattleReader(), menu, inp)
        result = loop.run(max_turns=3, max_cycles=5)
        self.assertTrue(result.success)
        self.assertEqual(result.reason, "battle_ended")
        self.assertEqual(result.turns_submitted, 1)
        self.assertEqual(inp.calls, 1)

    def test_final_allowed_turn_can_end_battle(self):
        reader = StateReader()
        menu = Menu(reader, True)
        inp = Input(reader)
        loop = BattleAutoplayer(Bridge(), reader, BattleReader(), menu, inp)
        result = loop.run(max_turns=1, max_cycles=5)
        self.assertTrue(result.success)
        self.assertEqual(result.reason, "battle_ended")
        self.assertEqual(result.turns_submitted, 1)
        self.assertEqual(inp.calls, 1)

    def test_stalls_without_blind_a_press(self):
        reader = StateReader()
        menu = Menu(reader, False)
        bridge = Bridge()
        loop = BattleAutoplayer(bridge, reader, BattleReader(), menu, Input(reader))
        result = loop.run(max_cycles=10, stall_cycles=2, wait_frames=3)
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "stalled_without_known_prompt")
        self.assertTrue(all(keys == 0 for keys, _ in bridge.waits))
        self.assertEqual(bridge.waits, [(0, 3), (0, 3)])

    def test_reports_mandatory_party_selection_without_guessing(self):
        reader = StateReader()
        bridge = Bridge()
        menu = Menu(reader, False, (raw_prompt(22),))
        loop = BattleAutoplayer(bridge, reader, BattleReader(), menu, Input(reader))
        result = loop.run(max_cycles=10, stall_cycles=2, wait_frames=3)
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "party_selection_not_supported")
        self.assertEqual(bridge.waits, [])
        self.assertEqual(result.events[-1].kind, "unsupported_player_decision")

    def test_reports_yes_no_prompt_without_guessing(self):
        reader = StateReader()
        bridge = Bridge()
        menu = Menu(reader, False, (raw_prompt(19),))
        loop = BattleAutoplayer(bridge, reader, BattleReader(), menu, Input(reader))
        result = loop.run(max_cycles=10)
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "yes_no_prompt_not_supported")
        self.assertEqual(bridge.waits, [])


if __name__ == "__main__":
    unittest.main()
