from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .battle import BattleReader
from .battle_control import BattleInputController, BattleMenuReader
from .state import AraunaState, AraunaStateReader


@dataclass(frozen=True)
class BattleLoopEvent:
    cycle: int
    kind: str
    detail: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BattleLoopResult:
    success: bool
    reason: str
    turns_submitted: int
    cycles: int
    final_state: AraunaState
    events: tuple[BattleLoopEvent, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "reason": self.reason,
            "turns_submitted": self.turns_submitted,
            "cycles": self.cycles,
            "final_state": self.final_state.to_dict(),
            "events": [event.to_dict() for event in self.events],
        }


class BattleAutoplayer:
    """Bounded battle loop that never guesses unknown battle prompts."""

    def __init__(
        self,
        bridge,
        state_reader: AraunaStateReader,
        battle_reader: BattleReader,
        menu_reader: BattleMenuReader,
        input_controller: BattleInputController,
    ):
        self.bridge = bridge
        self.state_reader = state_reader
        self.battle_reader = battle_reader
        self.menu_reader = menu_reader
        self.input_controller = input_controller

    def _signature(self) -> tuple[object, ...]:
        snapshot = self.battle_reader.snapshot()
        mons = tuple(
            (
                mon.battler,
                mon.species,
                mon.hp,
                mon.status1,
                mon.status2,
                mon.moves,
                mon.pp,
            )
            for mon in snapshot.mons
        )
        prompts = tuple(
            (p.battler, p.controller_active, p.command, p.action_cursor, p.move_cursor)
            for p in self.menu_reader.prompts()
        )
        return mons, prompts

    def run(
        self,
        *,
        max_turns: int = 64,
        max_cycles: int = 1024,
        wait_frames: int = 4,
        stall_cycles: int = 80,
    ) -> BattleLoopResult:
        if max_turns < 1 or max_cycles < 1 or wait_frames < 1 or stall_cycles < 1:
            raise ValueError("battle loop limits must be positive")

        state = self.state_reader.snapshot()
        if not state.in_battle:
            return BattleLoopResult(False, "not_in_battle", 0, 0, state, ())

        turns = 0
        events: list[BattleLoopEvent] = []
        last_signature: tuple[object, ...] | None = None
        unchanged = 0

        for cycle in range(1, max_cycles + 1):
            state = self.state_reader.snapshot()
            if not state.in_battle:
                return BattleLoopResult(
                    True, "battle_ended", turns, cycle - 1, state, tuple(events)
                )

            prompt = self.menu_reader.player_prompt()
            if prompt is not None:
                result = self.input_controller.choose_recommended()
                events.append(BattleLoopEvent(cycle, "move_decision", result.to_dict()))
                if not result.success:
                    return BattleLoopResult(
                        False, result.reason, turns, cycle, self.state_reader.snapshot(), tuple(events)
                    )
                turns += 1
                if turns >= max_turns:
                    return BattleLoopResult(
                        False, "max_turns", turns, cycle, self.state_reader.snapshot(), tuple(events)
                    )
                last_signature = None
                unchanged = 0
                continue

            signature = self._signature()
            if signature == last_signature:
                unchanged += 1
            else:
                unchanged = 0
                last_signature = signature

            if unchanged >= stall_cycles:
                events.append(
                    BattleLoopEvent(
                        cycle,
                        "stall",
                        {"unchanged_cycles": unchanged, "policy": "no_blind_confirm_input"},
                    )
                )
                return BattleLoopResult(
                    False, "stalled_without_known_prompt", turns, cycle, state, tuple(events)
                )

            # Let the emulator advance animations, messages and battle scripts with no key held.
            self.bridge.press(0, frames=wait_frames)

        return BattleLoopResult(
            False, "max_cycles", turns, max_cycles, self.state_reader.snapshot(), tuple(events)
        )
