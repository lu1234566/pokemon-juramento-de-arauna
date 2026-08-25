from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .state import AraunaState, AraunaStateReader
from .symbols import SymbolTable


FIELD_MESSAGE_BOX_HIDDEN = 0
FIELD_MESSAGE_BOX_UNUSED = 1
FIELD_MESSAGE_BOX_NORMAL = 2
FIELD_MESSAGE_BOX_AUTO_SCROLL = 3

RENDER_STATE_HANDLE_CHAR = 0
RENDER_STATE_WAIT = 1
RENDER_STATE_CLEAR = 2
RENDER_STATE_SCROLL_START = 3
RENDER_STATE_SCROLL = 4
RENDER_STATE_WAIT_SE = 5
RENDER_STATE_PAUSE = 6

# Emerald struct TextPrinter layout (include/text.h):
# callback at 0x10, subStructFields at 0x14, active at 0x1B, state at 0x1C.
TEXT_PRINTER_SIZE = 0x24
TEXT_PRINTER_ACTIVE_OFFSET = 0x1B
TEXT_PRINTER_STATE_OFFSET = 0x1C
TEXT_PRINTER_SPEED_OFFSET = 0x1D
TEXT_PRINTER_DELAY_OFFSET = 0x1E

_WAIT_KIND = {
    RENDER_STATE_WAIT: "pause_until_press",
    RENDER_STATE_CLEAR: "prompt_clear",
    RENDER_STATE_SCROLL_START: "prompt_scroll",
}

_STATE_NAME = {
    RENDER_STATE_HANDLE_CHAR: "handle_char",
    RENDER_STATE_WAIT: "wait",
    RENDER_STATE_CLEAR: "clear",
    RENDER_STATE_SCROLL_START: "scroll_start",
    RENDER_STATE_SCROLL: "scroll",
    RENDER_STATE_WAIT_SE: "wait_se",
    RENDER_STATE_PAUSE: "pause",
}

_MODE_NAME = {
    FIELD_MESSAGE_BOX_HIDDEN: "hidden",
    FIELD_MESSAGE_BOX_UNUSED: "unused",
    FIELD_MESSAGE_BOX_NORMAL: "normal",
    FIELD_MESSAGE_BOX_AUTO_SCROLL: "auto_scroll",
}


@dataclass(frozen=True)
class DialogueState:
    message_mode: int
    message_mode_name: str
    printer_active: bool
    printer_state: int
    printer_state_name: str
    text_speed: int
    delay_counter: int
    waiting_for_input: bool
    wait_kind: str | None
    safe_to_advance: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DialogueAdvanceEvent:
    cycle: int
    action: str
    before: DialogueState
    after: DialogueState

    def to_dict(self) -> dict[str, Any]:
        return {
            "cycle": self.cycle,
            "action": self.action,
            "before": self.before.to_dict(),
            "after": self.after.to_dict(),
        }


@dataclass(frozen=True)
class DialogueAdvanceResult:
    success: bool
    reason: str
    advances: int
    cycles: int
    final_dialogue: DialogueState
    final_state: AraunaState
    events: tuple[DialogueAdvanceEvent, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "reason": self.reason,
            "advances": self.advances,
            "cycles": self.cycles,
            "final_dialogue": self.final_dialogue.to_dict(),
            "final_state": self.final_state.to_dict(),
            "events": [event.to_dict() for event in self.events],
        }


class DialogueReader:
    """Read the normal overworld field text printer without modifying RAM."""

    def __init__(self, bridge, symbols: SymbolTable):
        self.bridge = bridge
        self.message_mode_address = symbols.address("sFieldMessageBoxMode")
        self.text_printers_address = symbols.address("sTextPrinters")

        # `make syms` uses objdump -t and includes local/static symbols. When sizes
        # are present, reject a mismatched build/layout instead of silently decoding
        # the wrong bytes.
        printer_symbol = symbols.get("sTextPrinters")
        if printer_symbol is not None and printer_symbol.size is not None:
            if printer_symbol.size < TEXT_PRINTER_SIZE:
                raise ValueError(
                    "sTextPrinters symbol is smaller than one Emerald TextPrinter; "
                    "the harness layout does not match this ROM build"
                )

    def snapshot(self, printer_index: int = 0) -> DialogueState:
        if printer_index < 0:
            raise ValueError("printer_index must be non-negative")
        base = self.text_printers_address + printer_index * TEXT_PRINTER_SIZE
        raw = self.bridge.read_range(base, TEXT_PRINTER_SIZE)
        if len(raw) != TEXT_PRINTER_SIZE:
            raise RuntimeError(
                f"expected {TEXT_PRINTER_SIZE} bytes for TextPrinter, got {len(raw)}"
            )

        mode = self.bridge.read8(self.message_mode_address)
        active = raw[TEXT_PRINTER_ACTIVE_OFFSET] != 0
        printer_state = raw[TEXT_PRINTER_STATE_OFFSET]
        wait_kind = _WAIT_KIND.get(printer_state)
        waiting = active and wait_kind is not None

        # Strict safety rule: only ordinary field messages are eligible. Auto-scroll
        # text advances itself, and menus/Yes-No are intentionally outside this API.
        safe = mode == FIELD_MESSAGE_BOX_NORMAL and waiting

        return DialogueState(
            message_mode=mode,
            message_mode_name=_MODE_NAME.get(mode, f"unknown_{mode}"),
            printer_active=active,
            printer_state=printer_state,
            printer_state_name=_STATE_NAME.get(printer_state, f"unknown_{printer_state}"),
            text_speed=raw[TEXT_PRINTER_SPEED_OFFSET],
            delay_counter=raw[TEXT_PRINTER_DELAY_OFFSET],
            waiting_for_input=waiting,
            wait_kind=wait_kind,
            safe_to_advance=safe,
        )


class DialogueAdvancer:
    """Advance only RAM-proven normal field dialogue waits with the A button."""

    def __init__(
        self,
        bridge,
        state_reader: AraunaStateReader,
        dialogue_reader: DialogueReader,
    ):
        self.bridge = bridge
        self.state_reader = state_reader
        self.dialogue_reader = dialogue_reader

    def advance_once(self, *, press_frames: int = 2) -> DialogueAdvanceResult:
        if press_frames < 1:
            raise ValueError("press_frames must be positive")
        game_state = self.state_reader.snapshot()
        before = self.dialogue_reader.snapshot()

        if game_state.in_battle:
            return DialogueAdvanceResult(
                False, "in_battle", 0, 0, before, game_state, ()
            )
        if not before.safe_to_advance:
            reason = (
                "auto_scroll"
                if before.message_mode == FIELD_MESSAGE_BOX_AUTO_SCROLL
                else "no_verified_dialogue_wait"
            )
            return DialogueAdvanceResult(False, reason, 0, 0, before, game_state, ())

        self.bridge.press("A", frames=press_frames)
        after = self.dialogue_reader.snapshot()
        event = DialogueAdvanceEvent(1, "press_a", before, after)
        return DialogueAdvanceResult(
            True,
            "advanced",
            1,
            1,
            after,
            self.state_reader.snapshot(),
            (event,),
        )

    def run(
        self,
        *,
        max_advances: int = 64,
        max_cycles: int = 1024,
        wait_frames: int = 2,
        stall_cycles: int = 120,
        press_frames: int = 2,
    ) -> DialogueAdvanceResult:
        if min(max_advances, max_cycles, wait_frames, stall_cycles, press_frames) < 1:
            raise ValueError("dialogue limits must be positive")

        advances = 0
        events: list[DialogueAdvanceEvent] = []
        last_signature: tuple[object, ...] | None = None
        unchanged = 0

        for cycle in range(1, max_cycles + 1):
            game_state = self.state_reader.snapshot()
            dialogue = self.dialogue_reader.snapshot()

            if game_state.in_battle:
                return DialogueAdvanceResult(
                    True,
                    "battle_started",
                    advances,
                    cycle - 1,
                    dialogue,
                    game_state,
                    tuple(events),
                )

            if dialogue.message_mode == FIELD_MESSAGE_BOX_AUTO_SCROLL:
                # Auto-scroll is intentionally left alone. It should progress from
                # no-input frames below, never by injected confirmation input.
                pass
            elif dialogue.safe_to_advance:
                if advances >= max_advances:
                    return DialogueAdvanceResult(
                        False,
                        "max_advances",
                        advances,
                        cycle,
                        dialogue,
                        game_state,
                        tuple(events),
                    )
                before = dialogue
                self.bridge.press("A", frames=press_frames)
                after = self.dialogue_reader.snapshot()
                events.append(DialogueAdvanceEvent(cycle, "press_a", before, after))
                advances += 1
                last_signature = None
                unchanged = 0
                continue
            elif not dialogue.printer_active:
                # A normal field message is complete when printer 0 becomes inactive.
                # We deliberately stop here rather than pressing through whatever
                # script/menu may follow (for example a Yes/No choice).
                reason = (
                    "dialogue_finished"
                    if dialogue.message_mode == FIELD_MESSAGE_BOX_HIDDEN
                    else "printer_inactive"
                )
                return DialogueAdvanceResult(
                    True,
                    reason,
                    advances,
                    cycle - 1,
                    dialogue,
                    game_state,
                    tuple(events),
                )

            signature = (
                dialogue.message_mode,
                dialogue.printer_active,
                dialogue.printer_state,
                dialogue.delay_counter,
            )
            if signature == last_signature:
                unchanged += 1
            else:
                last_signature = signature
                unchanged = 0

            if unchanged >= stall_cycles:
                return DialogueAdvanceResult(
                    False,
                    "stalled_without_verified_input_wait",
                    advances,
                    cycle,
                    dialogue,
                    game_state,
                    tuple(events),
                )

            # Printing, scrolling, sound waits, pauses and auto-scroll progress with
            # no input. This is what prevents accidental confirmation of menus.
            self.bridge.press(0, frames=wait_frames)

        final_dialogue = self.dialogue_reader.snapshot()
        return DialogueAdvanceResult(
            False,
            "max_cycles",
            advances,
            max_cycles,
            final_dialogue,
            self.state_reader.snapshot(),
            tuple(events),
        )
