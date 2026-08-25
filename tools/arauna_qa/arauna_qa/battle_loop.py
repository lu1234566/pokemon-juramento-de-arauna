from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .battle import BattleReader
from .battle_control import BattleInputController, BattleMenuReader
from .state import AraunaState, AraunaStateReader


# Player-controller commands that require a user decision but are intentionally
# not automated yet. Detecting these explicitly is safer and much more useful
# than waiting for the generic stall watchdog.
CONTROLLER_YESNOBOX = 19
CONTROLLER_OPENBAG = 21
CONTROLLER_CHOOSEPOKEMON = 22
UNSUPPORTED_DECISION_COMMANDS = {
    CONTROLLER_YESNOBOX: "yes_no_prompt_not_supported",
    CONTROLLER_OPENBAG: "bag_prompt_not_supported",
    CONTROLLER_CHOOSEPOKEMON: "party_selection_not_supported",
}


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

    def _unsupported_player_decision(self):
        for prompt in self.menu_reader.prompts():
            if prompt.side != "player" or not prompt.controller_active:
                continue
            reason = UNSUPPORTED_DECISION_COMMANDS.get(prompt.command)
            if reason is not None:
                return prompt, reason
        return None

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
                # max_turns is a cap on submitted decisions, not a reason to abort
                # immediately after the final allowed move. This lets the engine
                # finish animations and end the battle after that move. We only
                # fail if another player decision is actually required.
                if turns >= max_turns:
                    return BattleLoopResult(
                        False, "max_turns", turns, cycle, state, tuple(events)
                    )
                result = self.input_controller.choose_recommended()
                events.append(BattleLoopEvent(cycle, "move_decision", result.to_dict()))
                if not result.success:
                    return BattleLoopResult(
                        False, result.reason, turns, cycle, self.state_reader.snapshot(), tuple(events)
                    )
                turns += 1
                last_signature = None
                unchanged = 0
                continue

            unsupported = self._unsupported_player_decision()
            if unsupported is not None:
                blocked_prompt, reason = unsupported
                events.append(
                    BattleLoopEvent(
                        cycle,
                        "unsupported_player_decision",
                        {
                            "reason": reason,
                            "prompt": blocked_prompt.to_dict(),
                            "policy": "abort_without_guessing_input",
                        },
                    )
                )
                return BattleLoopResult(
                    False, reason, turns, cycle, state, tuple(events)
                )

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
