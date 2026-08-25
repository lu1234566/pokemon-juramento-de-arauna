from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .state import AraunaState, AraunaStateReader

DIRECTIONS = {"UP", "DOWN", "LEFT", "RIGHT"}


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


class Navigator:
    def __init__(self, bridge, reader: AraunaStateReader, max_polls: int = 8):
        self.bridge = bridge
        self.reader = reader
        self.max_polls = max_polls

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
