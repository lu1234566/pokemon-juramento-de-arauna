import json
import tempfile
import unittest
from pathlib import Path

from arauna_qa.reporting import ScenarioReporter, safe_artifact_name
from arauna_qa.scenario import ScenarioResult
from arauna_qa.state import AraunaState


def state():
    return AraunaState(
        frame=1, map_group=0, map_num=0, map_layout_id=1, region_map_section_id=1,
        map_type=1, weather=0, music=1, player_valid=True, player_x=1, player_y=2,
        player_x_internal=8, player_y_internal=9, facing=1, movement_direction=1,
        elevation=3, metatile_behavior=0, avatar_flags=1, running_state=0,
        tile_transition_state=0, field_controls_locked=False, script_enabled=False,
        script_mode=0, script_ptr=0, in_battle=False, held_keys=0, new_keys=0,
        callback1=0, callback2=0,
    )


class Bridge:
    def __init__(self):
        self.screenshots = []
        self.states = []
    def screenshot(self, path):
        self.screenshots.append(path)
        Path(path).write_bytes(b"png")
    def save_state(self, path):
        self.states.append(path)
        Path(path).write_bytes(b"state")


class ReportingTests(unittest.TestCase):
    def test_safe_artifact_name(self):
        self.assertEqual(safe_artifact_name("  NPC battle / smoke  "), "NPC_battle_smoke")
        self.assertEqual(safe_artifact_name("..."), "scenario")

    def test_failure_bundle_captures_trace_screenshot_and_state(self):
        bridge = Bridge()
        result = ScenarioResult("NPC battle / smoke", False, "stalled", (), state())
        with tempfile.TemporaryDirectory() as tmp:
            bundle = ScenarioReporter(bridge).write(result, tmp)
            self.assertTrue(Path(bundle.result_json).is_file())
            self.assertTrue(Path(bundle.screenshot).is_file())
            self.assertTrue(Path(bundle.save_state).is_file())
            manifest = Path(tmp) / "NPC_battle_smoke.bundle.json"
            self.assertTrue(manifest.is_file())
            payload = json.loads(Path(bundle.result_json).read_text(encoding="utf-8"))
            self.assertEqual(payload["reason"], "stalled")
            self.assertEqual(len(bridge.screenshots), 1)
            self.assertEqual(len(bridge.states), 1)

    def test_success_bundle_writes_trace_without_failure_capture(self):
        bridge = Bridge()
        result = ScenarioResult("ok", True, "completed", (), state())
        with tempfile.TemporaryDirectory() as tmp:
            bundle = ScenarioReporter(bridge).write(result, tmp)
            self.assertTrue(Path(bundle.result_json).is_file())
            self.assertIsNone(bundle.screenshot)
            self.assertIsNone(bundle.save_state)
            self.assertEqual(bridge.screenshots, [])
            self.assertEqual(bridge.states, [])


if __name__ == "__main__":
    unittest.main()
