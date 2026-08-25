from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from .state import AraunaState


@dataclass(frozen=True)
class WatchEvent:
    kind: str
    frame_start: int
    frame_end: int
    frame_span: int
    samples: int
    cycle_length: int | None
    signature: tuple[object, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "kind": self.kind,
            "frame_start": self.frame_start,
            "frame_end": self.frame_end,
            "frame_span": self.frame_span,
            "samples": self.samples,
            "cycle_length": self.cycle_length,
            "signature": list(self.signature),
        }


class StateWatchdog:
    """Detect candidate no-progress states and short semantic cycles.

    This class produces evidence, not a definitive softlock verdict. Callers should
    set ``expecting_progress`` only while an action/objective is supposed to advance.
    """

    def __init__(
        self,
        stall_frames: int = 120,
        stall_samples: int = 8,
        max_cycle_length: int = 6,
        cycle_repeats: int = 3,
        history_limit: int = 128,
    ):
        if stall_frames < 1 or stall_samples < 2:
            raise ValueError("stall thresholds must be positive")
        if max_cycle_length < 2 or cycle_repeats < 2:
            raise ValueError("cycle thresholds are too small")
        self.stall_frames = stall_frames
        self.stall_samples = stall_samples
        self.max_cycle_length = max_cycle_length
        self.cycle_repeats = cycle_repeats
        self.history = deque(maxlen=history_limit)
        self._last_emitted: tuple[object, ...] | None = None

    @staticmethod
    def signature(state: AraunaState) -> tuple[object, ...]:
        # Frame and raw key values are intentionally omitted. The signature tracks
        # semantic progress surfaces that matter to black-box QA.
        return (
            state.map_group,
            state.map_num,
            state.player_valid,
            state.player_x,
            state.player_y,
            state.facing,
            state.running_state,
            state.tile_transition_state,
            state.field_controls_locked,
            state.script_enabled,
            state.script_mode,
            state.script_ptr,
            state.in_battle,
            state.callback2,
        )

    def reset(self) -> None:
        self.history.clear()
        self._last_emitted = None

    def observe(self, state: AraunaState, expecting_progress: bool = True) -> WatchEvent | None:
        sig = self.signature(state)
        self.history.append((state.frame, sig))

        if not expecting_progress:
            self._last_emitted = None
            return None

        event = self._detect_stall()
        if event is None:
            event = self._detect_cycle()

        if event is None:
            self._last_emitted = None
            return None

        token = (event.kind, event.cycle_length, event.signature)
        if token == self._last_emitted:
            return None
        self._last_emitted = token
        return event

    def _detect_stall(self) -> WatchEvent | None:
        if len(self.history) < self.stall_samples:
            return None
        frame_end, sig = self.history[-1]
        same: list[tuple[int, tuple[object, ...]]] = []
        for frame, candidate in reversed(self.history):
            if candidate != sig:
                break
            same.append((frame, candidate))
        if len(same) < self.stall_samples:
            return None
        frame_start = same[-1][0]
        if frame_end - frame_start < self.stall_frames:
            return None
        return WatchEvent(
            kind="no_progress",
            frame_start=frame_start,
            frame_end=frame_end,
            frame_span=frame_end - frame_start,
            samples=len(same),
            cycle_length=None,
            signature=sig,
        )

    def _detect_cycle(self) -> WatchEvent | None:
        sigs = [sig for _, sig in self.history]
        for cycle_length in range(2, self.max_cycle_length + 1):
            needed = cycle_length * self.cycle_repeats
            if len(sigs) < needed:
                continue
            tail = sigs[-needed:]
            pattern = tail[:cycle_length]
            if len(set(pattern)) < 2:
                continue
            if all(
                tail[offset : offset + cycle_length] == pattern
                for offset in range(0, needed, cycle_length)
            ):
                frame_start = self.history[-needed][0]
                frame_end = self.history[-1][0]
                return WatchEvent(
                    kind="cycle",
                    frame_start=frame_start,
                    frame_end=frame_end,
                    frame_span=frame_end - frame_start,
                    samples=needed,
                    cycle_length=cycle_length,
                    signature=tuple(pattern),
                )
        return None
