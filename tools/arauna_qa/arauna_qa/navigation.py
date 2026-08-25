from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Iterable

from .repo_map import CollisionGrid, RepoMapIndex
from .state import AraunaState, AraunaStateReader

DIRECTIONS = {"UP", "DOWN", "LEFT", "RIGHT"}
DIRECTION_DELTAS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}
DELTA_DIRECTIONS = {delta: direction for direction, delta in DIRECTION_DELTAS.items()}


@dataclass(frozen=True)
class MoveResult:
    direction: str
    before: AraunaState
    after: AraunaState
    moved: bool
    map_changed: bool
    blocked: bool
    polls: int

    def to_dict(self) -> dict[str, object]:
        return {
            "direction": self.direction,
            "moved": self.moved,
            "map_changed": self.map_changed,
            "blocked": self.blocked,
            "polls": self.polls,
            "before": self.before.to_dict(),
            "after": self.after.to_dict(),
        }

    @property
    def position_before(self) -> tuple[int | None, int | None]:
        return self.before.player_x, self.before.player_y

    @property
    def position_after(self) -> tuple[int | None, int | None]:
        return self.after.player_x, self.after.player_y


@dataclass(frozen=True)
class WalkResult:
    target_x: int
    target_y: int
    reached: bool
    reason: str
    final_state: AraunaState
    moves: tuple[MoveResult, ...]
    replans: int
    blocked_tiles: tuple[tuple[int, int], ...]
    map_changed: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "target": {"x": self.target_x, "y": self.target_y},
            "reached": self.reached,
            "reason": self.reason,
            "map_changed": self.map_changed,
            "replans": self.replans,
            "blocked_tiles": [{"x": x, "y": y} for x, y in self.blocked_tiles],
            "move_count": len(self.moves),
            "moves": [move.to_dict() for move in self.moves],
            "final_state": self.final_state.to_dict(),
        }


class Navigator:
    def __init__(
        self,
        bridge,
        reader: AraunaStateReader,
        max_polls: int = 8,
        map_index: RepoMapIndex | None = None,
    ):
        self.bridge = bridge
        self.reader = reader
        self.max_polls = max_polls
        self.map_index = map_index

    @staticmethod
    def _normalize_direction(direction: str) -> str:
        direction = direction.upper()
        if direction not in DIRECTIONS:
            raise ValueError(f"direction must be one of {sorted(DIRECTIONS)}")
        return direction

    @staticmethod
    def _map_key(state: AraunaState) -> tuple[int | None, int | None]:
        return state.map_group, state.map_num

    @staticmethod
    def _position(state: AraunaState) -> tuple[int | None, int | None]:
        return state.player_x, state.player_y

    def step(self, direction: str, press_frames: int = 1) -> MoveResult:
        direction = self._normalize_direction(direction)
        before = self.reader.snapshot()
        if not before.player_valid:
            raise RuntimeError("player object is not currently valid; cannot navigate")
        if before.in_battle:
            raise RuntimeError("cannot use field navigation while in battle")

        self.bridge.press(direction, frames=press_frames)
        after = before
        changed = False
        map_changed = False
        polls = 0

        for polls in range(1, self.max_polls + 1):
            after = self.reader.snapshot()
            map_changed = self._map_key(after) != self._map_key(before)
            changed = map_changed or self._position(after) != self._position(before)
            if map_changed:
                break
            if changed and after.tile_transition_state == 0:
                break

        moved = changed
        blocked = (
            not moved
            and self._map_key(after) == self._map_key(before)
            and self._position(after) == self._position(before)
        )
        return MoveResult(
            direction=direction,
            before=before,
            after=after,
            moved=moved,
            map_changed=map_changed,
            blocked=blocked,
            polls=polls,
        )

    def walk_sequence(self, directions: Iterable[str], stop_on_block: bool = True) -> list[MoveResult]:
        results: list[MoveResult] = []
        for direction in directions:
            result = self.step(direction)
            results.append(result)
            if stop_on_block and result.blocked:
                break
        return results

    @staticmethod
    def _heuristic(a: tuple[int, int], b: tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @classmethod
    def plan_path(
        cls,
        grid: CollisionGrid,
        start: tuple[int, int],
        target: tuple[int, int],
        blocked_tiles: Iterable[tuple[int, int]] = (),
    ) -> list[str] | None:
        if not grid.in_bounds(*start) or not grid.in_bounds(*target):
            return None
        if start == target:
            return []
        blocked = set(blocked_tiles)
        blocked.discard(start)
        if target in blocked or not grid.is_passable(*target):
            return None

        frontier: list[tuple[int, int, tuple[int, int]]] = []
        serial = 0
        heappush(frontier, (cls._heuristic(start, target), serial, start))
        came_from: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}
        cost_so_far = {start: 0}

        while frontier:
            _, _, current = heappop(frontier)
            if current == target:
                break

            for direction, (dx, dy) in DIRECTION_DELTAS.items():
                nxt = current[0] + dx, current[1] + dy
                if nxt in blocked or not grid.in_bounds(*nxt) or not grid.is_passable(*nxt):
                    continue
                new_cost = cost_so_far[current] + 1
                if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                    cost_so_far[nxt] = new_cost
                    serial += 1
                    priority = new_cost + cls._heuristic(nxt, target)
                    heappush(frontier, (priority, serial, nxt))
                    came_from[nxt] = (current, direction)

        if target not in came_from:
            return None

        directions: list[str] = []
        current = target
        while current != start:
            previous, direction = came_from[current]
            directions.append(direction)
            current = previous
        directions.reverse()
        return directions

    def _require_current_grid(self, state: AraunaState) -> CollisionGrid:
        if self.map_index is None:
            raise RuntimeError("walk_to requires a RepoMapIndex")
        if state.map_group is None or state.map_num is None:
            raise RuntimeError("runtime map group/number are unavailable")
        map_def = self.map_index.from_runtime(state.map_group, state.map_num)
        if map_def is None:
            raise RuntimeError(
                f"runtime map ({state.map_group},{state.map_num}) is not present in the repository index"
            )
        return self.map_index.load_collision_grid(map_def)

    def walk_to(
        self,
        target_x: int,
        target_y: int,
        max_steps: int = 256,
        press_frames: int = 2,
    ) -> WalkResult:
        initial = self.reader.snapshot()
        if not initial.player_valid:
            raise RuntimeError("player object is not currently valid; cannot navigate")
        if initial.in_battle:
            raise RuntimeError("cannot use field navigation while in battle")
        if initial.player_x is None or initial.player_y is None:
            raise RuntimeError("player coordinates are unavailable")

        initial_map = self._map_key(initial)
        grid = self._require_current_grid(initial)
        target = (int(target_x), int(target_y))
        if not grid.in_bounds(*target):
            raise ValueError(
                f"target {target} is outside current map bounds {grid.width}x{grid.height}"
            )

        moves: list[MoveResult] = []
        dynamic_blocked: set[tuple[int, int]] = set()
        blocked_attempts: dict[tuple[tuple[int, int], tuple[int, int]], int] = {}
        replans = 0
        current_state = initial

        for _ in range(max_steps):
            if self._map_key(current_state) != initial_map:
                return WalkResult(
                    target_x=target[0],
                    target_y=target[1],
                    reached=False,
                    reason="map_changed",
                    final_state=current_state,
                    moves=tuple(moves),
                    replans=replans,
                    blocked_tiles=tuple(sorted(dynamic_blocked)),
                    map_changed=True,
                )

            if current_state.player_x is None or current_state.player_y is None:
                return WalkResult(
                    target_x=target[0],
                    target_y=target[1],
                    reached=False,
                    reason="position_unavailable",
                    final_state=current_state,
                    moves=tuple(moves),
                    replans=replans,
                    blocked_tiles=tuple(sorted(dynamic_blocked)),
                    map_changed=False,
                )

            current = (current_state.player_x, current_state.player_y)
            if current == target:
                return WalkResult(
                    target_x=target[0],
                    target_y=target[1],
                    reached=True,
                    reason="reached",
                    final_state=current_state,
                    moves=tuple(moves),
                    replans=replans,
                    blocked_tiles=tuple(sorted(dynamic_blocked)),
                    map_changed=False,
                )

            path = self.plan_path(grid, current, target, dynamic_blocked)
            if not path:
                return WalkResult(
                    target_x=target[0],
                    target_y=target[1],
                    reached=False,
                    reason="no_path",
                    final_state=current_state,
                    moves=tuple(moves),
                    replans=replans,
                    blocked_tiles=tuple(sorted(dynamic_blocked)),
                    map_changed=False,
                )

            direction = path[0]
            dx, dy = DIRECTION_DELTAS[direction]
            expected = current[0] + dx, current[1] + dy
            result = self.step(direction, press_frames=press_frames)
            moves.append(result)
            current_state = result.after

            if result.map_changed:
                return WalkResult(
                    target_x=target[0],
                    target_y=target[1],
                    reached=False,
                    reason="map_changed",
                    final_state=current_state,
                    moves=tuple(moves),
                    replans=replans,
                    blocked_tiles=tuple(sorted(dynamic_blocked)),
                    map_changed=True,
                )

            if result.blocked:
                edge = (current, expected)
                attempts = blocked_attempts.get(edge, 0) + 1
                blocked_attempts[edge] = attempts
                if attempts >= 2:
                    dynamic_blocked.add(expected)
                    replans += 1
                continue

            actual = self._position(current_state)
            if actual != expected:
                replans += 1

        return WalkResult(
            target_x=target[0],
            target_y=target[1],
            reached=False,
            reason="max_steps",
            final_state=current_state,
            moves=tuple(moves),
            replans=replans,
            blocked_tiles=tuple(sorted(dynamic_blocked)),
            map_changed=self._map_key(current_state) != initial_map,
        )
