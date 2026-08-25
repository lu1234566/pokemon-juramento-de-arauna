from __future__ import annotations

from dataclasses import dataclass

from .exploration import Explorer
from .navigation import DIRECTION_DELTAS, MoveResult, Navigator
from .repo_map import MapDefinition, RepoMapIndex
from .state import AraunaState
from .world_route import MapTransition, WorldRouter


@dataclass(frozen=True)
class TransitionResult:
    transition: MapTransition
    success: bool
    reason: str
    moves: tuple[MoveResult, ...]
    final_state: AraunaState

    def to_dict(self) -> dict[str, object]:
        return {
            "transition": self.transition.to_dict(),
            "success": self.success,
            "reason": self.reason,
            "move_count": len(self.moves),
            "moves": [move.to_dict() for move in self.moves],
            "final_state": self.final_state.to_dict(),
        }


@dataclass(frozen=True)
class WorldNavigationResult:
    target_map: str
    reached: bool
    reason: str
    transition_results: tuple[TransitionResult, ...]
    final_state: AraunaState

    def to_dict(self) -> dict[str, object]:
        return {
            "target_map": self.target_map,
            "reached": self.reached,
            "reason": self.reason,
            "transition_count": len(self.transition_results),
            "transitions": [item.to_dict() for item in self.transition_results],
            "final_state": self.final_state.to_dict(),
        }


class WorldNavigator:
    """Execute a planned map route one verified transition at a time."""

    def __init__(
        self,
        navigator: Navigator,
        map_index: RepoMapIndex,
        router: WorldRouter | None = None,
    ):
        self.navigator = navigator
        self.map_index = map_index
        self.router = router or WorldRouter(map_index)

    @staticmethod
    def _unsafe_reason(state: AraunaState) -> str | None:
        if state.in_battle:
            return "battle_started"
        if state.field_controls_locked or state.script_enabled:
            return "controls_locked"
        return None

    @staticmethod
    def _position(state: AraunaState) -> tuple[int, int] | None:
        if state.player_x is None or state.player_y is None:
            return None
        return state.player_x, state.player_y

    def _current_map(self, state: AraunaState) -> MapDefinition | None:
        if state.map_group is None or state.map_num is None:
            return None
        return self.map_index.from_runtime(state.map_group, state.map_num)

    def _is_destination(self, state: AraunaState, destination_map: str) -> bool:
        current = self._current_map(state)
        return current is not None and current.id == destination_map

    def _execute_transition(
        self,
        transition: MapTransition,
        max_moves: int = 256,
    ) -> TransitionResult:
        state = self.navigator.reader.snapshot()
        source = self._current_map(state)
        if source is None or source.id != transition.source_map:
            return TransitionResult(transition, False, "source_map_mismatch", (), state)
        unsafe = self._unsafe_reason(state)
        if unsafe:
            return TransitionResult(transition, False, unsafe, (), state)
        if transition.source_x is None or transition.source_y is None:
            return TransitionResult(transition, False, "no_approach_coordinate", (), state)

        grid = self.map_index.load_collision_grid(source)
        target = (transition.source_x, transition.source_y)
        if not grid.in_bounds(*target):
            return TransitionResult(transition, False, "approach_out_of_bounds", (), state)

        excluded = Explorer.known_trigger_tiles(source)
        excluded.discard(target)
        dynamic_blocked: set[tuple[int, int]] = set()
        blocked_attempts: dict[tuple[tuple[int, int], tuple[int, int]], int] = {}
        moves: list[MoveResult] = []
        current_state = state

        while len(moves) < max_moves:
            if self._is_destination(current_state, transition.destination_map):
                return TransitionResult(transition, True, "arrived", tuple(moves), current_state)
            current_map = self._current_map(current_state)
            if current_map is None or current_map.id != transition.source_map:
                return TransitionResult(
                    transition, False, "unexpected_destination", tuple(moves), current_state
                )
            unsafe = self._unsafe_reason(current_state)
            if unsafe:
                return TransitionResult(transition, False, unsafe, tuple(moves), current_state)
            current = self._position(current_state)
            if current is None:
                return TransitionResult(
                    transition, False, "position_unavailable", tuple(moves), current_state
                )

            if current == target:
                if transition.kind == "connection":
                    if transition.direction is None:
                        return TransitionResult(
                            transition, False, "connection_direction_missing", tuple(moves), current_state
                        )
                    result = self.navigator.step(transition.direction, press_frames=2)
                    moves.append(result)
                    current_state = result.after
                    if self._is_destination(current_state, transition.destination_map):
                        return TransitionResult(
                            transition, True, "arrived", tuple(moves), current_state
                        )
                    if result.map_changed:
                        return TransitionResult(
                            transition, False, "unexpected_destination", tuple(moves), current_state
                        )
                    return TransitionResult(
                        transition, False, "connection_did_not_transition", tuple(moves), current_state
                    )
                return TransitionResult(
                    transition, False, "warp_not_triggered", tuple(moves), current_state
                )

            path = Navigator.plan_path(
                grid,
                current,
                target,
                blocked_tiles=dynamic_blocked | excluded,
            )
            if not path:
                return TransitionResult(
                    transition, False, "transition_unreachable", tuple(moves), current_state
                )

            direction = path[0]
            dx, dy = DIRECTION_DELTAS[direction]
            expected = current[0] + dx, current[1] + dy
            result = self.navigator.step(direction, press_frames=2)
            moves.append(result)
            current_state = result.after

            if self._is_destination(current_state, transition.destination_map):
                return TransitionResult(transition, True, "arrived", tuple(moves), current_state)
            if result.map_changed:
                return TransitionResult(
                    transition, False, "unexpected_destination", tuple(moves), current_state
                )

            unsafe = self._unsafe_reason(current_state)
            if unsafe:
                return TransitionResult(transition, False, unsafe, tuple(moves), current_state)

            if result.blocked:
                edge = (current, expected)
                attempts = blocked_attempts.get(edge, 0) + 1
                blocked_attempts[edge] = attempts
                if attempts >= 2:
                    dynamic_blocked.add(expected)
                continue

            if self._position(current_state) != expected:
                continue

        return TransitionResult(transition, False, "move_limit", tuple(moves), current_state)

    def route_to(
        self,
        target_key: str,
        max_transitions: int = 32,
        max_moves_per_transition: int = 256,
    ) -> WorldNavigationResult:
        target = self.map_index.require(target_key)
        state = self.navigator.reader.snapshot()
        current = self._current_map(state)
        if current is None:
            return WorldNavigationResult(target.id, False, "current_map_unknown", (), state)
        if current.id == target.id:
            return WorldNavigationResult(target.id, True, "already_there", (), state)

        results: list[TransitionResult] = []

        for _ in range(max_transitions):
            unsafe = self._unsafe_reason(state)
            if unsafe:
                return WorldNavigationResult(target.id, False, unsafe, tuple(results), state)

            current = self._current_map(state)
            if current is None:
                return WorldNavigationResult(
                    target.id, False, "current_map_unknown", tuple(results), state
                )
            if current.id == target.id:
                return WorldNavigationResult(target.id, True, "reached", tuple(results), state)

            route = self.router.plan(current.id, target.id)
            if route is None or not route.transitions:
                return WorldNavigationResult(target.id, False, "no_world_route", tuple(results), state)

            transition = route.transitions[0]
            execution = self._execute_transition(
                transition,
                max_moves=max_moves_per_transition,
            )
            results.append(execution)
            state = execution.final_state
            if not execution.success:
                return WorldNavigationResult(
                    target.id, False, execution.reason, tuple(results), state
                )

        current = self._current_map(state)
        return WorldNavigationResult(
            target.id,
            current is not None and current.id == target.id,
            "transition_limit",
            tuple(results),
            state,
        )
