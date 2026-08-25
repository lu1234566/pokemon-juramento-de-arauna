from __future__ import annotations

from dataclasses import dataclass

from .exploration import Explorer
from .navigation import MoveResult, Navigator
from .objects import ObjectEventReader, ObjectEventState
from .repo_map import RepoMapIndex
from .state import AraunaState

DELTA_TO_INPUT = {
    (0, 1): "DOWN",
    (0, -1): "UP",
    (-1, 0): "LEFT",
    (1, 0): "RIGHT",
}


@dataclass(frozen=True)
class InteractionResult:
    object_index: int
    local_id: int
    success: bool
    reason: str
    target_before: ObjectEventState
    target_after: ObjectEventState | None
    final_state: AraunaState
    moves: tuple[MoveResult, ...]
    selected_object_event: int | None

    def to_dict(self) -> dict[str, object]:
        return {
            "object_index": self.object_index,
            "local_id": self.local_id,
            "success": self.success,
            "reason": self.reason,
            "move_count": len(self.moves),
            "moves": [move.to_dict() for move in self.moves],
            "target_before": self.target_before.to_dict(),
            "target_after": self.target_after.to_dict() if self.target_after else None,
            "selected_object_event": self.selected_object_event,
            "final_state": self.final_state.to_dict(),
        }


class NpcInteractor:
    """Approach a live object event, face it, press A, and verify a response."""

    def __init__(
        self,
        navigator: Navigator,
        object_reader: ObjectEventReader,
        map_index: RepoMapIndex,
    ):
        self.navigator = navigator
        self.object_reader = object_reader
        self.map_index = map_index

    @staticmethod
    def _player_pos(state: AraunaState) -> tuple[int, int] | None:
        if state.player_x is None or state.player_y is None:
            return None
        return state.player_x, state.player_y

    @staticmethod
    def _unsafe_reason(state: AraunaState) -> str | None:
        if state.in_battle:
            return "battle_started"
        if state.field_controls_locked or state.script_enabled:
            return "controls_locked"
        return None

    def _current_map(self, state: AraunaState):
        if state.map_group is None or state.map_num is None:
            return None
        return self.map_index.from_runtime(state.map_group, state.map_num)

    def _selected_object_event(self) -> int | None:
        symbol = self.object_reader.symbols.get("gSelectedObjectEvent")
        if symbol is None:
            return None
        return self.object_reader.bridge.read8(symbol.address)

    def list_current(self) -> tuple[ObjectEventState, ...]:
        state = self.navigator.reader.snapshot()
        if state.map_group is None or state.map_num is None:
            return ()
        return self.object_reader.active_on_map(state.map_group, state.map_num)

    def _resolve_target(
        self,
        *,
        object_index: int | None = None,
        local_id: int | None = None,
    ) -> ObjectEventState | None:
        state = self.navigator.reader.snapshot()
        if state.map_group is None or state.map_num is None:
            return None
        if object_index is not None:
            obj = self.object_reader.find_index(object_index)
            if (
                obj is not None
                and not obj.is_player
                and obj.map_group == state.map_group
                and obj.map_num == state.map_num
            ):
                return obj
            return None
        if local_id is not None:
            return self.object_reader.find_local_id(local_id, state.map_group, state.map_num)
        raise ValueError("object_index or local_id is required")

    def _candidate_approaches(
        self,
        target: ObjectEventState,
        state: AraunaState,
    ) -> list[tuple[int, tuple[int, int], str]]:
        current_map = self._current_map(state)
        if current_map is None:
            return []
        grid = self.map_index.load_collision_grid(current_map)
        player = self._player_pos(state)
        if player is None:
            return []
        occupied = {
            obj.position
            for obj in self.object_reader.active_on_map(state.map_group, state.map_num)
            if obj.index != target.index
        }
        excluded = Explorer.known_trigger_tiles(current_map)
        choices: list[tuple[int, tuple[int, int], str]] = []
        for (dx, dy), face in DELTA_TO_INPUT.items():
            approach = (target.current_x - dx, target.current_y - dy)
            if (
                not grid.in_bounds(*approach)
                or not grid.is_passable(*approach)
                or approach in occupied
                or approach in excluded
            ):
                continue
            path = Navigator.plan_path(
                grid,
                player,
                approach,
                blocked_tiles=occupied | excluded | {target.position},
            )
            if path is not None:
                choices.append((len(path), approach, face))
        choices.sort(key=lambda item: item[0])
        return choices

    def _approach(
        self,
        target_index: int,
        max_moves: int,
    ) -> tuple[ObjectEventState | None, list[MoveResult], str | None]:
        moves: list[MoveResult] = []
        for _ in range(max_moves + 1):
            state = self.navigator.reader.snapshot()
            unsafe = self._unsafe_reason(state)
            if unsafe:
                return None, moves, unsafe
            target = self._resolve_target(object_index=target_index)
            if target is None:
                return None, moves, "target_disappeared"
            player = self._player_pos(state)
            if player is None:
                return target, moves, "position_unavailable"
            distance = abs(player[0] - target.current_x) + abs(player[1] - target.current_y)
            if distance == 1:
                return target, moves, None
            choices = self._candidate_approaches(target, state)
            if not choices:
                return target, moves, "target_unreachable"
            _, approach, _ = choices[0]
            current_map = self._current_map(state)
            if current_map is None:
                return target, moves, "current_map_unknown"
            grid = self.map_index.load_collision_grid(current_map)
            occupied = {
                obj.position
                for obj in self.object_reader.active_on_map(state.map_group, state.map_num)
                if obj.index != target.index
            }
            excluded = Explorer.known_trigger_tiles(current_map)
            path = Navigator.plan_path(
                grid,
                player,
                approach,
                blocked_tiles=occupied | excluded | {target.position},
            )
            if not path:
                continue
            result = self.navigator.step(path[0], press_frames=2)
            moves.append(result)
            if result.map_changed:
                return target, moves, "map_changed"
            if result.after.in_battle:
                return target, moves, "battle_started"
        target = self._resolve_target(object_index=target_index)
        return target, moves, "move_limit"

    def interact(
        self,
        *,
        object_index: int | None = None,
        local_id: int | None = None,
        max_moves: int = 192,
        response_polls: int = 12,
    ) -> InteractionResult:
        target = self._resolve_target(object_index=object_index, local_id=local_id)
        if target is None:
            raise RuntimeError("target object is not active on the current map")
        target_before = target

        target, moves, approach_error = self._approach(target.index, max_moves)
        if target is None or approach_error is not None:
            final_state = self.navigator.reader.snapshot()
            return InteractionResult(
                target_before.index,
                target_before.local_id,
                False,
                approach_error or "target_disappeared",
                target_before,
                target,
                final_state,
                tuple(moves),
                self._selected_object_event(),
            )

        state = self.navigator.reader.snapshot()
        player = self._player_pos(state)
        if player is None:
            return InteractionResult(
                target.index, target.local_id, False, "position_unavailable",
                target_before, target, state, tuple(moves), self._selected_object_event(),
            )

        delta = (target.current_x - player[0], target.current_y - player[1])
        face = DELTA_TO_INPUT.get(delta)
        if face is None:
            return InteractionResult(
                target.index, target.local_id, False, "target_not_adjacent",
                target_before, target, state, tuple(moves), self._selected_object_event(),
            )

        face_result = self.navigator.step(face, press_frames=1)
        moves.append(face_result)
        refreshed = self._resolve_target(object_index=target.index)
        after_face = face_result.after
        if refreshed is None:
            return InteractionResult(
                target.index, target.local_id, False, "target_disappeared",
                target_before, None, after_face, tuple(moves), self._selected_object_event(),
            )
        player_after_face = self._player_pos(after_face)
        if player_after_face is None:
            return InteractionResult(
                target.index, target.local_id, False, "position_unavailable",
                target_before, refreshed, after_face, tuple(moves), self._selected_object_event(),
            )
        if abs(player_after_face[0] - refreshed.current_x) + abs(player_after_face[1] - refreshed.current_y) != 1:
            return InteractionResult(
                target.index, target.local_id, False, "target_moved_during_facing",
                target_before, refreshed, after_face, tuple(moves), self._selected_object_event(),
            )

        before = after_face
        selected_before = self._selected_object_event()
        self.navigator.bridge.press("A", frames=2)
        final_state = before
        selected = selected_before
        reason = "no_observable_response"
        success = False

        for _ in range(response_polls):
            final_state = self.navigator.reader.snapshot()
            selected = self._selected_object_event()
            if final_state.in_battle and not before.in_battle:
                success, reason = True, "battle_started"
                break
            if final_state.map_group != before.map_group or final_state.map_num != before.map_num:
                success, reason = True, "map_changed"
                break
            if final_state.script_enabled and not before.script_enabled:
                success, reason = True, "script_started"
                break
            if final_state.field_controls_locked and not before.field_controls_locked:
                success, reason = True, "controls_locked"
                break
            if selected == target.index and selected_before != target.index:
                success, reason = True, "selected_object"

        target_after = self._resolve_target(object_index=target.index)
        return InteractionResult(
            target.index,
            target.local_id,
            success,
            reason,
            target_before,
            target_after,
            final_state,
            tuple(moves),
            selected,
        )
