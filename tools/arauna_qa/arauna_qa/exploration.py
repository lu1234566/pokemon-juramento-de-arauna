from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from .navigation import DIRECTION_DELTAS, MoveResult, Navigator
from .repo_map import CollisionGrid, MapDefinition, RepoMapIndex
from .state import AraunaState


@dataclass(frozen=True)
class ExplorationResult:
    map_id: str
    reached_targets: int
    visited_tiles: tuple[tuple[int, int], ...]
    blocked_tiles: tuple[tuple[int, int], ...]
    excluded_tiles: tuple[tuple[int, int], ...]
    safe_static_reachable: int
    coverage_ratio: float
    reason: str
    final_state: AraunaState
    moves: tuple[MoveResult, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "map_id": self.map_id,
            "reached_targets": self.reached_targets,
            "visited_count": len(self.visited_tiles),
            "visited_tiles": [{"x": x, "y": y} for x, y in self.visited_tiles],
            "blocked_tiles": [{"x": x, "y": y} for x, y in self.blocked_tiles],
            "excluded_tiles": [{"x": x, "y": y} for x, y in self.excluded_tiles],
            "safe_static_reachable": self.safe_static_reachable,
            "coverage_ratio": self.coverage_ratio,
            "reason": self.reason,
            "final_state": self.final_state.to_dict(),
            "move_count": len(self.moves),
            "moves": [move.to_dict() for move in self.moves],
        }


class Explorer:
    def __init__(self, navigator: Navigator, map_index: RepoMapIndex):
        self.navigator = navigator
        self.map_index = map_index

    @staticmethod
    def known_trigger_tiles(map_def: MapDefinition) -> set[tuple[int, int]]:
        excluded: set[tuple[int, int]] = set()
        for event in (*map_def.warp_events, *map_def.coord_events):
            x = event.get("x")
            y = event.get("y")
            if isinstance(x, int) and isinstance(y, int):
                excluded.add((x, y))
        return excluded

    @staticmethod
    def reachable_tiles(
        grid: CollisionGrid,
        start: tuple[int, int],
        blocked: set[tuple[int, int]] | None = None,
        excluded: set[tuple[int, int]] | None = None,
    ) -> list[tuple[int, int]]:
        blocked = blocked or set()
        excluded = excluded or set()
        if not grid.in_bounds(*start):
            return []
        queue = deque([start])
        seen = {start}
        ordered = [start]
        while queue:
            current = queue.popleft()
            for dx, dy in DIRECTION_DELTAS.values():
                nxt = current[0] + dx, current[1] + dy
                if nxt in seen or nxt in blocked or nxt in excluded:
                    continue
                if not grid.in_bounds(*nxt) or not grid.is_passable(*nxt):
                    continue
                seen.add(nxt)
                ordered.append(nxt)
                queue.append(nxt)
        return ordered

    @staticmethod
    def _position(state: AraunaState) -> tuple[int, int] | None:
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

    def explore_current_map(
        self,
        max_targets: int = 64,
        max_total_moves: int = 512,
        avoid_triggers: bool = True,
    ) -> ExplorationResult:
        state = self.navigator.reader.snapshot()
        if not state.player_valid:
            raise RuntimeError("player object is not currently valid; cannot explore")
        unsafe = self._unsafe_reason(state)
        if unsafe:
            raise RuntimeError(f"cannot explore safely: {unsafe}")
        if state.map_group is None or state.map_num is None:
            raise RuntimeError("runtime map group/number are unavailable")
        start = self._position(state)
        if start is None:
            raise RuntimeError("player coordinates are unavailable")

        map_def = self.map_index.from_runtime(state.map_group, state.map_num)
        if map_def is None:
            raise RuntimeError(f"unknown runtime map ({state.map_group},{state.map_num})")
        grid = self.map_index.load_collision_grid(map_def)
        initial_map = (state.map_group, state.map_num)
        excluded = self.known_trigger_tiles(map_def) if avoid_triggers else set()
        excluded.discard(start)

        baseline = self.reachable_tiles(grid, start, excluded=excluded)
        safe_static_reachable = len(baseline)
        visited = {start}
        known_blocked: set[tuple[int, int]] = set()
        moves: list[MoveResult] = []
        reached_targets = 0
        reason = "frontier_exhausted"
        current_state = state

        while reached_targets < max_targets and len(moves) < max_total_moves:
            current = self._position(current_state)
            if current is None:
                reason = "position_unavailable"
                break
            if (current_state.map_group, current_state.map_num) != initial_map:
                reason = "map_changed"
                break
            unsafe = self._unsafe_reason(current_state)
            if unsafe:
                reason = unsafe
                break

            reachable = self.reachable_tiles(grid, current, blocked=known_blocked, excluded=excluded)
            target = next((tile for tile in reachable if tile not in visited), None)
            if target is None:
                reason = "frontier_exhausted"
                break

            path = Navigator.plan_path(
                grid,
                current,
                target,
                blocked_tiles=known_blocked | excluded,
            )
            if not path:
                known_blocked.add(target)
                continue

            path_interrupted = False
            for direction in path:
                if len(moves) >= max_total_moves:
                    reason = "move_limit"
                    path_interrupted = True
                    break

                before = self.navigator.reader.snapshot()
                if (before.map_group, before.map_num) != initial_map:
                    current_state = before
                    reason = "map_changed"
                    path_interrupted = True
                    break
                unsafe = self._unsafe_reason(before)
                if unsafe:
                    current_state = before
                    reason = unsafe
                    path_interrupted = True
                    break
                current = self._position(before)
                if current is None:
                    current_state = before
                    reason = "position_unavailable"
                    path_interrupted = True
                    break

                dx, dy = DIRECTION_DELTAS[direction]
                expected = current[0] + dx, current[1] + dy
                result = self.navigator.step(direction, press_frames=2)
                moves.append(result)
                current_state = result.after

                if result.map_changed:
                    reason = "map_changed"
                    path_interrupted = True
                    break
                unsafe = self._unsafe_reason(current_state)
                if unsafe:
                    reason = unsafe
                    path_interrupted = True
                    break

                if result.blocked:
                    # A very short press can occasionally only turn the avatar.
                    # Retry once before promoting the tile to a dynamic obstacle.
                    retry = self.navigator.step(direction, press_frames=2)
                    moves.append(retry)
                    current_state = retry.after
                    if retry.map_changed:
                        reason = "map_changed"
                        path_interrupted = True
                        break
                    unsafe = self._unsafe_reason(current_state)
                    if unsafe:
                        reason = unsafe
                        path_interrupted = True
                        break
                    if retry.blocked:
                        known_blocked.add(expected)
                        path_interrupted = True
                        break
                    result = retry

                pos = self._position(current_state)
                if pos is not None and (current_state.map_group, current_state.map_num) == initial_map:
                    visited.add(pos)
                if pos != expected:
                    path_interrupted = True
                    break

            if reason in {"map_changed", "battle_started", "controls_locked", "position_unavailable", "move_limit"}:
                break
            if path_interrupted:
                continue

            if self._position(current_state) == target:
                visited.add(target)
                reached_targets += 1
            else:
                reason = "unexpected_displacement"
                break
        else:
            if reached_targets >= max_targets:
                reason = "target_limit"
            elif len(moves) >= max_total_moves:
                reason = "move_limit"

        denominator = safe_static_reachable or 1
        covered_safe = len(set(baseline) & visited)
        return ExplorationResult(
            map_id=map_def.id,
            reached_targets=reached_targets,
            visited_tiles=tuple(sorted(visited)),
            blocked_tiles=tuple(sorted(known_blocked)),
            excluded_tiles=tuple(sorted(excluded)),
            safe_static_reachable=safe_static_reachable,
            coverage_ratio=covered_safe / denominator,
            reason=reason,
            final_state=current_state,
            moves=tuple(moves),
        )
