import unittest

from arauna_qa.dialogue import (
    DialogueAdvancer,
    DialogueReader,
    FIELD_MESSAGE_BOX_AUTO_SCROLL,
    FIELD_MESSAGE_BOX_HIDDEN,
    FIELD_MESSAGE_BOX_NORMAL,
    RENDER_STATE_CLEAR,
    RENDER_STATE_HANDLE_CHAR,
    RENDER_STATE_WAIT_SE,
    TEXT_PRINTER_ACTIVE_OFFSET,
    TEXT_PRINTER_DELAY_OFFSET,
    TEXT_PRINTER_SIZE,
    TEXT_PRINTER_STATE_OFFSET,
)
from arauna_qa.state import AraunaState
from arauna_qa.symbols import Symbol, SymbolTable


MODE_ADDR = 0x02000010
PRINTER_ADDR = 0x02000100


def game_state(in_battle=False):
    return AraunaState(
        frame=1, map_group=0, map_num=0, map_layout_id=1, region_map_section_id=1,
        map_type=1, weather=0, music=1, player_valid=True, player_x=1, player_y=2,
        player_x_internal=8, player_y_internal=9, facing=1, movement_direction=1,
        elevation=3, metatile_behavior=0, avatar_flags=1, running_state=0,
        tile_transition_state=0, field_controls_locked=True, script_enabled=True,
        script_mode=0, script_ptr=0x08100000, in_battle=in_battle, held_keys=0,
        new_keys=0, callback1=0, callback2=0,
    )


class StateReader:
    def __init__(self, in_battle=False):
        self.value = game_state(in_battle)
    def snapshot(self):
        return self.value


class Bridge:
    def __init__(self, mode=FIELD_MESSAGE_BOX_NORMAL, active=True,
                 printer_state=RENDER_STATE_HANDLE_CHAR, current_char=0x08100000):
        self.mode = mode
        self.raw = bytearray(TEXT_PRINTER_SIZE)
        self.raw[0:4] = current_char.to_bytes(4, "little")
        self.raw[TEXT_PRINTER_ACTIVE_OFFSET] = int(active)
        self.raw[TEXT_PRINTER_STATE_OFFSET] = printer_state
        self.raw[TEXT_PRINTER_DELAY_OFFSET] = 0
        self.presses = []
        self.on_press = None

    def read8(self, address):
        if address != MODE_ADDR:
            raise AssertionError(address)
        return self.mode

    def read_range(self, address, length):
        if address != PRINTER_ADDR or length != TEXT_PRINTER_SIZE:
            raise AssertionError((address, length))
        return bytes(self.raw)

    def press(self, keys, frames=2):
        self.presses.append((keys, frames))
        if self.on_press is not None:
            self.on_press(self, keys, frames)


class DialogueTests(unittest.TestCase):
    def symbols(self):
        return SymbolTable({
            "sFieldMessageBoxMode": Symbol("sFieldMessageBoxMode", MODE_ADDR, 1, "l"),
            "sTextPrinters": Symbol("sTextPrinters", PRINTER_ADDR, TEXT_PRINTER_SIZE * 32, "l"),
        })

    def test_normal_clear_prompt_is_safe_to_advance(self):
        bridge = Bridge(printer_state=RENDER_STATE_CLEAR)
        snap = DialogueReader(bridge, self.symbols()).snapshot()
        self.assertEqual(snap.message_mode_name, "normal")
        self.assertEqual(snap.wait_kind, "prompt_clear")
        self.assertTrue(snap.waiting_for_input)
        self.assertTrue(snap.safe_to_advance)
        self.assertEqual(snap.current_char, 0x08100000)

    def test_auto_scroll_prompt_is_never_safe_to_advance(self):
        bridge = Bridge(mode=FIELD_MESSAGE_BOX_AUTO_SCROLL, printer_state=RENDER_STATE_CLEAR)
        snap = DialogueReader(bridge, self.symbols()).snapshot()
        self.assertTrue(snap.waiting_for_input)
        self.assertFalse(snap.safe_to_advance)

    def test_advance_once_never_presses_without_verified_wait(self):
        bridge = Bridge(mode=FIELD_MESSAGE_BOX_HIDDEN, active=False)
        advancer = DialogueAdvancer(bridge, StateReader(), DialogueReader(bridge, self.symbols()))
        result = advancer.advance_once()
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "no_verified_dialogue_wait")
        self.assertEqual(bridge.presses, [])

    def test_run_waits_for_printing_then_advances_and_stops_before_followup_menu(self):
        bridge = Bridge(printer_state=RENDER_STATE_HANDLE_CHAR)
        phase = {"value": 0}

        def on_press(obj, keys, frames):
            if phase["value"] == 0 and keys == 0:
                # Simulate text printing forward until a \p / clear prompt.
                obj.raw[0:4] = (0x08100001).to_bytes(4, "little")
                obj.raw[TEXT_PRINTER_STATE_OFFSET] = RENDER_STATE_CLEAR
                phase["value"] = 1
            elif phase["value"] == 1 and keys == "A":
                # A verified prompt is accepted and text resumes.
                obj.raw[0:4] = (0x08100002).to_bytes(4, "little")
                obj.raw[TEXT_PRINTER_STATE_OFFSET] = RENDER_STATE_HANDLE_CHAR
                phase["value"] = 2
            elif phase["value"] == 2 and keys == 0:
                # Printer reaches EOS. A later script menu could now appear; the
                # advancer must stop rather than inject another A.
                obj.raw[TEXT_PRINTER_ACTIVE_OFFSET] = 0
                obj.mode = FIELD_MESSAGE_BOX_HIDDEN
                phase["value"] = 3

        bridge.on_press = on_press
        advancer = DialogueAdvancer(bridge, StateReader(), DialogueReader(bridge, self.symbols()))
        result = advancer.run(max_cycles=10, stall_cycles=3)
        self.assertTrue(result.success)
        self.assertEqual(result.reason, "dialogue_finished")
        self.assertEqual(result.advances, 1)
        self.assertEqual(bridge.presses, [(0, 2), ("A", 2), (0, 2)])

    def test_auto_scroll_uses_no_confirmation_input(self):
        bridge = Bridge(mode=FIELD_MESSAGE_BOX_AUTO_SCROLL, printer_state=RENDER_STATE_CLEAR)

        def on_press(obj, keys, frames):
            if keys == 0:
                obj.raw[TEXT_PRINTER_ACTIVE_OFFSET] = 0
                obj.mode = FIELD_MESSAGE_BOX_HIDDEN

        bridge.on_press = on_press
        advancer = DialogueAdvancer(bridge, StateReader(), DialogueReader(bridge, self.symbols()))
        result = advancer.run(max_cycles=5)
        self.assertTrue(result.success)
        self.assertEqual(result.reason, "dialogue_finished")
        self.assertTrue(bridge.presses)
        self.assertTrue(all(keys == 0 for keys, _ in bridge.presses))

    def test_unknown_active_wait_stalls_without_a_or_b(self):
        bridge = Bridge(mode=FIELD_MESSAGE_BOX_NORMAL, printer_state=RENDER_STATE_WAIT_SE)
        advancer = DialogueAdvancer(bridge, StateReader(), DialogueReader(bridge, self.symbols()))
        result = advancer.run(max_cycles=10, stall_cycles=2, wait_frames=3)
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "stalled_without_verified_input_wait")
        self.assertTrue(all(keys == 0 for keys, _ in bridge.presses))


if __name__ == "__main__":
    unittest.main()
