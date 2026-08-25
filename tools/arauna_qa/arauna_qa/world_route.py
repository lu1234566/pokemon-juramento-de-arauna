from __future__ import annotations

from collections import deque
from dataclasses import asdict, dataclass

from .repo_map import MapDefinition, RepoMapIndex


@dataclass(frozen=True)
class MapTransition:
    kind: str
    source_map: str
    destination_map: str
    source_x: int | None = None
    source_y: int | None = None
    direction: str | None = None
    source_index: int | None = None
    destination_warp_id: int | None = None
    offset: int | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class WorldRoute:
    start_map: str
    target_map: str
    transitions: tuple[MapTransition, ...]

    @property
    def map_sequence(self) -> tuple[str, ...]:
        sequence = [self.start_map]
        sequence.extend(step.destination_map for step in self.transitions)
        return tuple(sequence)

    def to_dict(self) -> dict[str, object]:
        return {
            "start_map": self.start_map,
            "target_map": self.target_map,
            "transition_count": len(self.transitions),
            "map_sequence": list(self.map_sequence),
            "transitions": [step.to_dict() for step in self.transitions],
        }


class WorldRouter:
    """Plan static map-to-map routes through declared connections and warps."""

    def __init__(self, map_index: RepoMapIndex):
        self.map_index = map_index

    @staticmethod
    def _parse_warp_id(value) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def _connection_transition(
        self,
        source: MapDefinition,
        index: int,
        connection: dict,
    ) -> MapTransition | None:
        destination_id = connection.get("map")
        if not isinstance(destination_id, str) or destination_id == "MAP_DYNAMIC":
            return None
        destination = self.map_index.maps_by_id.get(destination_id)
        if destination is None:
            return None

        direction = str(connection.get("direction", "")).lower()
        if direction not in {"up", "down", "left", "right"}:
            return None
        try:
            offset = int(connection.get("offset", 0))
        except (TypeError, ValueError):
            offset = 0

        source_layout = self.map_index.layouts.get(source.layout_id)
        destination_layout = self.map_index.layouts.get(destination.layout_id)
        x = y = None

        # Emerald places a connected map with its origin shifted by `offset`
        # along the shared axis. Pick the middle of the overlapping source edge
        # as a deterministic approach coordinate for later runtime execution.
        if source_layout is not None and destination_layout is not None:
            if direction in {"up", "down"}:
                low = max(0, offset)
                high = min(source_layout.width - 1, offset + destination_layout.width - 1)
                if low <= high:
                    x = (low + high) // 2
                    y = 0 if direction == "up" else source_layout.height - 1
            else:
                low = max(0, offset)
                high = min(source_layout.height - 1, offset + destination_layout.height - 1)
                if low <= high:
                    y = (low + high) // 2
                    x = 0 if direction == "left" else source_layout.width - 1

        return MapTransition(
            kind="connection",
            source_map=source.id,
            destination_map=destination.id,
            source_x=x,
            source_y=y,
            direction=direction.upper(),
            source_index=index,
            offset=offset,
        )

    def _warp_transition(
        self,
        source: MapDefinition,
        index: int,
        warp: dict,
    ) -> MapTransition | None:
        destination_id = warp.get("dest_map")
        if not isinstance(destination_id, str) or destination_id == "MAP_DYNAMIC":
            return None
        destination = self.map_index.maps_by_id.get(destination_id)
        if destination is None:
            return None
        x = warp.get("x")
        y = warp.get("y")
        if not isinstance(x, int) or not isinstance(y, int):
            x = y = None
        return MapTransition(
            kind="warp",
            source_map=source.id,
            destination_map=destination.id,
            source_x=x,
            source_y=y,
            source_index=index,
            destination_warp_id=self._parse_warp_id(warp.get("dest_warp_id")),
        )

    def transitions_from(self, map_or_key: MapDefinition | str) -> tuple[MapTransition, ...]:
        source = map_or_key if isinstance(map_or_key, MapDefinition) else self.map_index.require(map_or_key)
        transitions: list[MapTransition] = []
        for index, connection in enumerate(source.connections):
            transition = self._connection_transition(source, index, connection)
            if transition is not None:
                transitions.append(transition)
        for index, warp in enumerate(source.warp_events):
            transition = self._warp_transition(source, index, warp)
            if transition is not None:
                transitions.append(transition)
        return tuple(transitions)

    def plan(self, start_key: str, target_key: str) -> WorldRoute | None:
        start = self.map_index.require(start_key)
        target = self.map_index.require(target_key)
        if start.id == target.id:
            return WorldRoute(start.id, target.id, ())

        queue = deque([start.id])
        came_from: dict[str, tuple[str, MapTransition]] = {}
        seen = {start.id}

        while queue:
            current_id = queue.popleft()
            current = self.map_index.maps_by_id[current_id]
            for transition in self.transitions_from(current):
                destination_id = transition.destination_map
                if destination_id in seen:
                    continue
                seen.add(destination_id)
                came_from[destination_id] = (current_id, transition)
                if destination_id == target.id:
                    queue.clear()
                    break
                queue.append(destination_id)

        if target.id not in came_from:
            return None

        steps: list[MapTransition] = []
        current_id = target.id
        while current_id != start.id:
            previous_id, transition = came_from[current_id]
            steps.append(transition)
            current_id = previous_id
        steps.reverse()
        return WorldRoute(start.id, target.id, tuple(steps))
