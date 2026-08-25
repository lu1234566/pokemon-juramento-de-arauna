from __future__ import annotations

from dataclasses import asdict, dataclass

from .battle_advisor import BattleAdvisor, MoveAdvice
from .symbols import SymbolTable

MAX_BATTLERS = 4
BATTLE_BUFFER_SIZE = 0x200
CONTROLLER_CHOOSEACTION = 18
CONTROLLER_CHOOSEMOVE = 20


@dataclass(frozen=True)
class BattlePromptState:
    battler: int
    side: str
    controller_active: bool
    command: int
    action_cursor: int
    move_cursor: int
    is_double_prompt: bool
    no_pp_number: bool
    target_cursor: int | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class BattleInputResult:
    success: bool
    reason: str
    selected_slot: int | None
    recommendation: MoveAdvice | None
    before: BattlePromptState | None
    after: BattlePromptState | None
    inputs: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "success": self.success,
            "reason": self.reason,
            "selected_slot": self.selected_slot,
            "recommendation": self.recommendation.to_dict() if self.recommendation else None,
            "before": self.before.to_dict() if self.before else None,
            "after": self.after.to_dict() if self.after else None,
            "inputs": list(self.inputs),
        }


class BattleMenuReader:
    """Read battle controller prompts/cursors without changing battle memory."""

    def __init__(self, bridge, symbols: SymbolTable):
        self.bridge = bridge
        self.symbols = symbols

    def _read_u8_array(self, name: str, length: int) -> bytes:
        return self.bridge.read_range(self.symbols.address(name), length)

    def prompts(self) -> tuple[BattlePromptState, ...]:
        count = min(int(self.bridge.read8(self.symbols.address("gBattlersCount"))), MAX_BATTLERS)
        exec_flags = self.bridge.read32(self.symbols.address("gBattleControllerExecFlags"))
        positions = self._read_u8_array("gBattlerPositions", MAX_BATTLERS)
        action = self._read_u8_array("gActionSelectionCursor", MAX_BATTLERS)
        moves = self._read_u8_array("gMoveSelectionCursor", MAX_BATTLERS)
        target_symbol = self.symbols.get("gMultiUsePlayerCursor")
        target_cursor = self.bridge.read8(target_symbol.address) if target_symbol is not None else None
        buffer_base = self.symbols.address("gBattleBufferA")

        result = []
        for battler in range(count):
            head = self.bridge.read_range(buffer_base + battler * BATTLE_BUFFER_SIZE, 4)
            command = head[0]
            result.append(
                BattlePromptState(
                    battler=battler,
                    side="opponent" if positions[battler] & 1 else "player",
                    controller_active=bool(exec_flags & (1 << battler)),
                    command=command,
                    action_cursor=action[battler],
                    move_cursor=moves[battler],
                    is_double_prompt=bool(head[1]) if command == CONTROLLER_CHOOSEMOVE else False,
                    no_pp_number=bool(head[2]) if command == CONTROLLER_CHOOSEMOVE else False,
                    target_cursor=target_cursor,
                )
            )
        return tuple(result)

    def player_prompt(self) -> BattlePromptState | None:
        for prompt in self.prompts():
            if (
                prompt.side == "player"
                and prompt.controller_active
                and prompt.command in {CONTROLLER_CHOOSEACTION, CONTROLLER_CHOOSEMOVE}
            ):
                return prompt
        return None


class BattleInputController:
    """Verified single-battle move selection using only normal GBA inputs."""

    def __init__(
        self,
        bridge,
        menu_reader: BattleMenuReader,
        advisor: BattleAdvisor | None = None,
        max_polls: int = 24,
    ):
        self.bridge = bridge
        self.menu_reader = menu_reader
        self.advisor = advisor
        self.max_polls = max_polls

    def _poll_for_command(self, command: int) -> BattlePromptState | None:
        for _ in range(self.max_polls):
            prompt = self.menu_reader.player_prompt()
            if prompt is not None and prompt.command == command:
                return prompt
        return None

    def _press_and_verify_cursor(
        self,
        key: str,
        expected_cursor: int,
        *,
        move_cursor: bool,
        inputs: list[str],
    ) -> BattlePromptState | None:
        self.bridge.press(key, frames=1)
        inputs.append(key)
        for _ in range(self.max_polls):
            prompt = self.menu_reader.player_prompt()
            if prompt is None:
                continue
            cursor = prompt.move_cursor if move_cursor else prompt.action_cursor
            if cursor == expected_cursor:
                return prompt
        return None

    @staticmethod
    def _cursor_path(current: int, target: int) -> list[tuple[str, int]]:
        if not 0 <= current <= 3 or not 0 <= target <= 3:
            raise ValueError("battle cursor must be in range 0..3")
        path: list[tuple[str, int]] = []
        cursor = current
        if (cursor & 1) != (target & 1):
            key = "RIGHT" if target & 1 else "LEFT"
            cursor ^= 1
            path.append((key, cursor))
        if (cursor & 2) != (target & 2):
            key = "DOWN" if target & 2 else "UP"
            cursor ^= 2
            path.append((key, cursor))
        return path

    def choose_move(self, slot: int, recommendation: MoveAdvice | None = None) -> BattleInputResult:
        if not 0 <= slot <= 3:
            raise ValueError("move slot must be in range 0..3")
        inputs: list[str] = []
        before = self.menu_reader.player_prompt()
        if before is None:
            return BattleInputResult(False, "no_player_prompt", slot, recommendation, None, None, ())

        prompt = before
        if prompt.command == CONTROLLER_CHOOSEACTION:
            for key, expected in self._cursor_path(prompt.action_cursor, 0):
                verified = self._press_and_verify_cursor(
                    key, expected, move_cursor=False, inputs=inputs
                )
                if verified is None:
                    return BattleInputResult(
                        False, "action_cursor_not_confirmed", slot, recommendation,
                        before, self.menu_reader.player_prompt(), tuple(inputs)
                    )
                prompt = verified
            self.bridge.press("A", frames=1)
            inputs.append("A")
            prompt = self._poll_for_command(CONTROLLER_CHOOSEMOVE)
            if prompt is None:
                return BattleInputResult(
                    False, "move_prompt_not_observed", slot, recommendation,
                    before, self.menu_reader.player_prompt(), tuple(inputs)
                )

        if prompt.command != CONTROLLER_CHOOSEMOVE:
            return BattleInputResult(
                False, "not_at_move_prompt", slot, recommendation,
                before, prompt, tuple(inputs)
            )
        if prompt.is_double_prompt:
            return BattleInputResult(
                False, "double_battle_not_supported", slot, recommendation,
                before, prompt, tuple(inputs)
            )

        for key, expected in self._cursor_path(prompt.move_cursor, slot):
            verified = self._press_and_verify_cursor(
                key, expected, move_cursor=True, inputs=inputs
            )
            if verified is None:
                return BattleInputResult(
                    False, "move_cursor_not_confirmed", slot, recommendation,
                    before, self.menu_reader.player_prompt(), tuple(inputs)
                )
            prompt = verified

        self.bridge.press("A", frames=1)
        inputs.append("A")
        after = None
        for _ in range(self.max_polls):
            after = self.menu_reader.player_prompt()
            if after is None:
                return BattleInputResult(
                    True, "move_submitted", slot, recommendation,
                    before, None, tuple(inputs)
                )
            if after.command != CONTROLLER_CHOOSEMOVE:
                return BattleInputResult(
                    True, "move_submitted", slot, recommendation,
                    before, after, tuple(inputs)
                )

        # In single battles, an active CHOOSEMOVE controller after A can mean
        # the selected move requires an explicit target. Do not guess that target.
        return BattleInputResult(
            False, "target_selection_or_unconfirmed_submission", slot, recommendation,
            before, after, tuple(inputs)
        )

    def choose_recommended(self) -> BattleInputResult:
        if self.advisor is None:
            raise RuntimeError("choose_recommended requires a BattleAdvisor")
        advice = self.advisor.recommend()
        if not advice.available or not advice.recommendations:
            return BattleInputResult(
                False, advice.reason, None, None,
                self.menu_reader.player_prompt(), self.menu_reader.player_prompt(), ()
            )
        recommendation = advice.recommendations[0]
        return self.choose_move(recommendation.slot, recommendation=recommendation)
