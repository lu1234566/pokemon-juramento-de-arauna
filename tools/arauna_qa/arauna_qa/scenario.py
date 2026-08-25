from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .battle_loop import BattleAutoplayer
from .dialogue import DialogueAdvancer
from .interaction import NpcInteractor
from .navigation import Navigator
from .repo_map import RepoMapIndex
from .state import AraunaState
from .world_nav import WorldNavigator


@dataclass(frozen=True)
class ScenarioStepResult:
    index: int
    action: str
    success: bool
    reason: str
    state: AraunaState
    detail: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "action": self.action,
            "success": self.success,
            "reason": self.reason,
            "detail": self.detail,
            "state": self.state.to_dict(),
        }


@dataclass(frozen=True)
class ScenarioResult:
    name: str
    success: bool
    reason: str
    steps: tuple[ScenarioStepResult, ...]
    final_state: AraunaState

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "success": self.success,
            "reason": self.reason,
            "step_count": len(self.steps),
            "steps": [step.to_dict() for step in self.steps],
            "final_state": self.final_state.to_dict(),
        }


class ScenarioRunner:
    """Execute declarative QA steps without generic RAM writes or blind confirms."""

    def __init__(
        self,
        navigator: Navigator,
        world_navigator: WorldNavigator,
        npc: NpcInteractor,
        map_index: RepoMapIndex,
        battle_autoplayer: BattleAutoplayer | None = None,
        dialogue_advancer: DialogueAdvancer | None = None,
    ):
        self.navigator = navigator
        self.world_navigator = world_navigator
        self.npc = npc
        self.map_index = map_index
        self.battle_autoplayer = battle_autoplayer
        self.dialogue_advancer = dialogue_advancer

    @classmethod
    def load(cls, path: str | Path) -> dict[str, Any]:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("scenario root must be a JSON object")
        if not isinstance(data.get("steps"), list):
            raise ValueError("scenario must contain a steps array")
        return data

    def _current_map_id(self, state: AraunaState) -> str | None:
        if state.map_group is None or state.map_num is None:
            return None
        map_def = self.map_index.from_runtime(state.map_group, state.map_num)
        return map_def.id if map_def is not None else None

    def _assert(self, step: dict[str, Any], state: AraunaState) -> tuple[bool, str, dict[str, Any]]:
        checks: dict[str, Any] = {}
        expected_map = step.get("map")
        if expected_map is not None:
            actual = self._current_map_id(state)
            expected = self.map_index.require(str(expected_map)).id
            checks["map"] = {"expected": expected, "actual": actual}
            if actual != expected:
                return False, "map_mismatch", checks

        fields = (
            "player_x",
            "player_y",
            "in_battle",
            "script_enabled",
            "field_controls_locked",
            "player_valid",
        )
        for field in fields:
            if field not in step:
                continue
            expected = step[field]
            actual = getattr(state, field)
            checks[field] = {"expected": expected, "actual": actual}
            if actual != expected:
                return False, f"{field}_mismatch", checks
        return True, "asserted", checks

    @staticmethod
    def _dialogue_limits(raw: dict[str, Any]) -> dict[str, int]:
        return {
            "max_advances": int(raw.get("max_advances", raw.get("max_presses", 64))),
            "max_cycles": int(raw.get("max_cycles", 1024)),
            "wait_frames": int(raw.get("wait_frames", 2)),
            "stall_cycles": int(raw.get("stall_cycles", 120)),
            "press_frames": int(raw.get("press_frames", 2)),
        }

    def _advance_to_battle(
        self,
        index: int,
        action: str,
        raw: dict[str, Any],
    ) -> ScenarioStepResult:
        if self.dialogue_advancer is None:
            state = self.navigator.reader.snapshot()
            return ScenarioStepResult(index, action, False, "dialogue_advancer_unavailable", state, {})

        limits = self._dialogue_limits(raw)
        max_phases = int(raw.get("max_phases", 64))
        settle_frames = int(raw.get("settle_frames", 4))
        if min(*limits.values(), max_phases, settle_frames) < 1:
            state = self.navigator.reader.snapshot()
            return ScenarioStepResult(index, action, False, "invalid_advance_limits", state, {})

        initial = self.navigator.reader.snapshot()
        if initial.in_battle:
            return ScenarioStepResult(
                index, action, True, "already_in_battle", initial,
                {"verified_advances": 0, "phases": []},
            )
        if not initial.script_enabled and not initial.field_controls_locked:
            return ScenarioStepResult(index, action, False, "no_script_to_advance", initial, {})

        initial_map = self._current_map_id(initial)
        remaining_advances = limits["max_advances"]
        phases: list[dict[str, Any]] = []

        for phase in range(1, max_phases + 1):
            before = self.navigator.reader.snapshot()
            if before.in_battle:
                return ScenarioStepResult(
                    index, action, True, "battle_started", before,
                    {
                        "verified_advances": limits["max_advances"] - remaining_advances,
                        "phases": phases,
                    },
                )

            actual_map = self._current_map_id(before)
            if actual_map != initial_map:
                return ScenarioStepResult(
                    index, action, False, "map_changed_before_battle", before,
                    {
                        "verified_advances": limits["max_advances"] - remaining_advances,
                        "initial_map": initial_map,
                        "actual_map": actual_map,
                        "phases": phases,
                    },
                )

            if phase > 1 and not before.script_enabled and not before.field_controls_locked:
                return ScenarioStepResult(
                    index, action, False, "script_ended_before_battle", before,
                    {
                        "verified_advances": limits["max_advances"] - remaining_advances,
                        "phases": phases,
                    },
                )

            if remaining_advances <= 0:
                return ScenarioStepResult(
                    index, action, False, "max_verified_advances", before,
                    {"verified_advances": limits["max_advances"], "phases": phases},
                )

            phase_limits = dict(limits)
            phase_limits["max_advances"] = remaining_advances
            result = self.dialogue_advancer.run(**phase_limits)
            remaining_advances -= result.advances
            phases.append({"phase": phase, "dialogue": result.to_dict()})

            if result.reason == "battle_started":
                return ScenarioStepResult(
                    index, action, True, "battle_started", result.final_state,
                    {
                        "verified_advances": limits["max_advances"] - remaining_advances,
                        "phases": phases,
                    },
                )
            if not result.success:
                return ScenarioStepResult(
                    index, action, False, f"dialogue_{result.reason}", result.final_state,
                    {
                        "verified_advances": limits["max_advances"] - remaining_advances,
                        "phases": phases,
                    },
                )

            # The text printer can finish one frame before the script starts the next
            # message or battle. Advance only no-input frames here. If a Yes/No/menu
            # follows, it remains untouched and this bounded phase loop fails safely.
            self.navigator.bridge.press(0, frames=settle_frames)
            after = self.navigator.reader.snapshot()
            if after.in_battle:
                return ScenarioStepResult(
                    index, action, True, "battle_started", after,
                    {
                        "verified_advances": limits["max_advances"] - remaining_advances,
                        "phases": phases,
                    },
                )

        final_state = self.navigator.reader.snapshot()
        return ScenarioStepResult(
            index, action, False, "battle_not_reached_without_safe_input", final_state,
            {
                "verified_advances": limits["max_advances"] - remaining_advances,
                "initial_map": initial_map,
                "phases": phases,
            },
        )

    def _run_step(self, index: int, raw: dict[str, Any]) -> ScenarioStepResult:
        action = str(raw.get("action", "")).lower()
        if not action:
            state = self.navigator.reader.snapshot()
            return ScenarioStepResult(index, "", False, "action_missing", state, {})

        if action == "goto_map":
            target = raw.get("map")
            if target is None:
                state = self.navigator.reader.snapshot()
                return ScenarioStepResult(index, action, False, "map_missing", state, {})
            result = self.world_navigator.route_to(str(target))
            return ScenarioStepResult(index, action, result.reached, result.reason, result.final_state, result.to_dict())

        if action == "walk_to":
            if "x" not in raw or "y" not in raw:
                state = self.navigator.reader.snapshot()
                return ScenarioStepResult(index, action, False, "coordinates_missing", state, {})
            result = self.navigator.walk_to(int(raw["x"]), int(raw["y"]), max_steps=int(raw.get("max_steps", 256)))
            return ScenarioStepResult(index, action, result.reached, result.reason, result.final_state, result.to_dict())

        if action == "talk":
            if "object_index" in raw:
                result = self.npc.interact(object_index=int(raw["object_index"]))
            elif "local_id" in raw:
                result = self.npc.interact(local_id=int(raw["local_id"]))
            else:
                state = self.navigator.reader.snapshot()
                return ScenarioStepResult(index, action, False, "target_missing", state, {})
            return ScenarioStepResult(index, action, result.success, result.reason, result.final_state, result.to_dict())

        if action in {"advance_dialogue", "dialogue_auto"}:
            if self.dialogue_advancer is None:
                state = self.navigator.reader.snapshot()
                return ScenarioStepResult(index, action, False, "dialogue_advancer_unavailable", state, {})
            result = self.dialogue_advancer.run(**self._dialogue_limits(raw))
            return ScenarioStepResult(index, action, result.success, result.reason, result.final_state, result.to_dict())

        if action in {"advance_to_battle", "advance_until_battle"}:
            return self._advance_to_battle(index, action, raw)

        if action in {"play_battle", "playbattle"}:
            if self.battle_autoplayer is None:
                state = self.navigator.reader.snapshot()
                return ScenarioStepResult(index, action, False, "battle_autoplayer_unavailable", state, {})
            limits = {
                "max_turns": int(raw.get("max_turns", 64)),
                "max_cycles": int(raw.get("max_cycles", 1024)),
                "wait_frames": int(raw.get("wait_frames", 4)),
                "stall_cycles": int(raw.get("stall_cycles", 80)),
            }
            result = self.battle_autoplayer.run(**limits)
            return ScenarioStepResult(index, action, result.success, result.reason, result.final_state, result.to_dict())

        if action == "press":
            key = raw.get("key")
            if key is None:
                state = self.navigator.reader.snapshot()
                return ScenarioStepResult(index, action, False, "key_missing", state, {})
            frames = int(raw.get("frames", 2))
            self.navigator.bridge.press(str(key), frames=frames)
            state = self.navigator.reader.snapshot()
            return ScenarioStepResult(index, action, True, "pressed", state, {"key": str(key), "frames": frames})

        if action == "wait":
            frames = int(raw.get("frames", 1))
            if frames < 1:
                state = self.navigator.reader.snapshot()
                return ScenarioStepResult(index, action, False, "invalid_frames", state, {})
            self.navigator.bridge.press(0, frames=frames)
            state = self.navigator.reader.snapshot()
            return ScenarioStepResult(index, action, True, "waited", state, {"frames": frames})

        if action == "screenshot":
            path = raw.get("path")
            if not path:
                state = self.navigator.reader.snapshot()
                return ScenarioStepResult(index, action, False, "path_missing", state, {})
            self.navigator.bridge.screenshot(str(path))
            state = self.navigator.reader.snapshot()
            return ScenarioStepResult(index, action, True, "captured", state, {"path": str(path)})

        if action == "assert":
            state = self.navigator.reader.snapshot()
            success, reason, detail = self._assert(raw, state)
            return ScenarioStepResult(index, action, success, reason, state, detail)

        state = self.navigator.reader.snapshot()
        return ScenarioStepResult(index, action, False, "unknown_action", state, {})

    def run(self, spec: dict[str, Any]) -> ScenarioResult:
        name = str(spec.get("name") or "unnamed")
        steps_raw = spec.get("steps")
        if not isinstance(steps_raw, list):
            raise ValueError("scenario must contain a steps array")

        results: list[ScenarioStepResult] = []
        for index, raw in enumerate(steps_raw):
            if not isinstance(raw, dict):
                state = self.navigator.reader.snapshot()
                result = ScenarioStepResult(index, "", False, "step_not_object", state, {})
            else:
                result = self._run_step(index, raw)
            results.append(result)
            if not result.success and not (isinstance(raw, dict) and raw.get("continue_on_failure")):
                return ScenarioResult(name, False, result.reason, tuple(results), result.state)

        final_state = self.navigator.reader.snapshot()
        return ScenarioResult(name, True, "completed", tuple(results), final_state)

    def run_file(self, path: str | Path) -> ScenarioResult:
        return self.run(self.load(path))
