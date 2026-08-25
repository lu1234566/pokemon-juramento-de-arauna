import unittest
from dataclasses import replace

from arauna_qa.state import AraunaState
from arauna_qa.watchdog import StateWatchdog


def state(frame=0, **changes):
    base = AraunaState(
        frame=frame,
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
        script_ptr=0x08001234,
        in_battle=False,
        held_keys=0,
        new_keys=0,
        callback1=0,
        callback2=0x08005678,
    )
    return replace(base, **changes)


class StateWatchdogTests(unittest.TestCase):
    def test_detects_semantic_no_progress_after_frame_span(self):
        watch = StateWatchdog(stall_frames=60, stall_samples=4)
        event = None
        for frame in (0, 20, 40, 60):
            event = watch.observe(state(frame=frame))
        self.assertIsNotNone(event)
        self.assertEqual(event.kind, "no_progress")
        self.assertEqual(event.frame_span, 60)

    def test_movement_breaks_stall_sequence(self):
        watch = StateWatchdog(stall_frames=60, stall_samples=4)
        self.assertIsNone(watch.observe(state(frame=0)))
        self.assertIsNone(watch.observe(state(frame=20)))
        self.assertIsNone(watch.observe(state(frame=40, player_x=6)))
        self.assertIsNone(watch.observe(state(frame=60, player_x=6)))
        self.assertIsNone(watch.observe(state(frame=80, player_x=6)))

    def test_detects_short_repeating_cycle(self):
        watch = StateWatchdog(
            stall_frames=999,
            stall_samples=10,
            max_cycle_length=4,
            cycle_repeats=3,
        )
        event = None
        for index in range(6):
            x = 5 if index % 2 == 0 else 6
            event = watch.observe(state(frame=index * 10, player_x=x))
        self.assertIsNotNone(event)
        self.assertEqual(event.kind, "cycle")
        self.assertEqual(event.cycle_length, 2)

    def test_idle_observation_can_be_marked_not_expecting_progress(self):
        watch = StateWatchdog(stall_frames=20, stall_samples=2)
        self.assertIsNone(watch.observe(state(frame=0), expecting_progress=False))
        self.assertIsNone(watch.observe(state(frame=40), expecting_progress=False))

    def test_duplicate_candidate_is_not_emitted_repeatedly(self):
        watch = StateWatchdog(stall_frames=20, stall_samples=2)
        self.assertIsNone(watch.observe(state(frame=0)))
        first = watch.observe(state(frame=20))
        second = watch.observe(state(frame=40))
        self.assertIsNotNone(first)
        self.assertIsNone(second)


if __name__ == "__main__":
    unittest.main()
