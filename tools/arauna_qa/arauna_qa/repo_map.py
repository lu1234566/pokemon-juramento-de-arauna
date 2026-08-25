from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


MAPGRID_METATILE_ID_MASK = 0x03FF
MAPGRID_COLLISION_MASK = 0x0C00
MAPGRID_ELEVATION_MASK = 0xF000
MAPGRID_COLLISION_SHIFT = 10
MAPGRID_ELEVATION_SHIFT = 12


@dataclass(frozen=True)
class LayoutDefinition:
    id: str
    name: str
    width: int
    height: int
    primary_tileset: str | None
    secondary_tileset: str | None
    blockdata_filepath: str | None


@dataclass(frozen=True)
class MapDefinition:
    id: str
    name: str
    layout_id: str
    directory: str
    group: int | None
    number: int | None
    connections: tuple[dict[str, Any], ...]
    object_events: tuple[dict[str, Any], ...]
    warp_events: tuple[dict[str, Any], ...]
    coord_events: tuple[dict[str, Any], ...]
    bg_events: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MapIssue:
    code: str
    map_id: str | None
    message: str

    def to_dict(self) -> dict[str, str | None]:
        return asdict(self)


@dataclass(frozen=True)
class MapCell:
    raw: int
    metatile_id: int
    collision: int
    elevation: int


@dataclass(frozen=True)
class CollisionGrid:
    width: int
    height: int
    raw_cells: tuple[int, ...]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def raw_at(self, x: int, y: int) -> int:
        if not self.in_bounds(x, y):
            raise IndexError(f"map coordinate ({x},{y}) outside {self.width}x{self.height}")
        return self.raw_cells[y * self.width + x]

    def cell_at(self, x: int, y: int) -> MapCell:
        raw = self.raw_at(x, y)
        return MapCell(
            raw=raw,
            metatile_id=raw & MAPGRID_METATILE_ID_MASK,
            collision=(raw & MAPGRID_COLLISION_MASK) >> MAPGRID_COLLISION_SHIFT,
            elevation=(raw & MAPGRID_ELEVATION_MASK) >> MAPGRID_ELEVATION_SHIFT,
        )

    def is_passable(self, x: int, y: int) -> bool:
        # Static map collision is only the planning hint. Runtime movement remains
        # authoritative for NPCs, scripted blockers, ledges, doors and elevation.
        return self.in_bounds(x, y) and self.cell_at(x, y).collision == 0


class RepoMapIndex:
    def __init__(
        self,
        root: Path,
        layouts: dict[str, LayoutDefinition],
        maps_by_id: dict[str, MapDefinition],
        maps_by_name: dict[str, MapDefinition],
        runtime_map_names: dict[tuple[int, int], str],
    ):
        self.root = root
        self.layouts = layouts
        self.maps_by_id = maps_by_id
        self.maps_by_name = maps_by_name
        self.runtime_map_names = runtime_map_names

    @classmethod
    def from_repo(cls, root: str | Path) -> "RepoMapIndex":
        root = Path(root).resolve()
        layouts_json = json.loads((root / "data/layouts/layouts.json").read_text(encoding="utf-8"))
        layouts: dict[str, LayoutDefinition] = {}
        for raw in layouts_json.get("layouts", []):
            layout = LayoutDefinition(
                id=raw["id"],
                name=raw["name"],
                width=int(raw["width"]),
                height=int(raw["height"]),
                primary_tileset=raw.get("primary_tileset"),
                secondary_tileset=raw.get("secondary_tileset"),
                blockdata_filepath=raw.get("blockdata_filepath"),
            )
            layouts[layout.id] = layout

        groups_json = json.loads((root / "data/maps/map_groups.json").read_text(encoding="utf-8"))
        runtime_map_names: dict[tuple[int, int], str] = {}
        runtime_for_name: dict[str, tuple[int, int]] = {}
        for group_index, group_label in enumerate(groups_json.get("group_order", [])):
            for map_number, map_name in enumerate(groups_json.get(group_label, [])):
                runtime_map_names[(group_index, map_number)] = map_name
                runtime_for_name[map_name] = (group_index, map_number)

        maps_by_id: dict[str, MapDefinition] = {}
        maps_by_name: dict[str, MapDefinition] = {}
        for path in sorted((root / "data/maps").glob("*/map.json")):
            raw = json.loads(path.read_text(encoding="utf-8"))
            name = raw.get("name") or path.parent.name
            runtime = runtime_for_name.get(name)
            map_def = MapDefinition(
                id=raw["id"],
                name=name,
                layout_id=raw["layout"],
                directory=path.parent.name,
                group=runtime[0] if runtime else None,
                number=runtime[1] if runtime else None,
                connections=tuple(raw.get("connections") or ()),
                object_events=tuple(raw.get("object_events") or ()),
                warp_events=tuple(raw.get("warp_events") or ()),
                coord_events=tuple(raw.get("coord_events") or ()),
                bg_events=tuple(raw.get("bg_events") or ()),
            )
            maps_by_id[map_def.id] = map_def
            maps_by_name[map_def.name] = map_def

        return cls(root, layouts, maps_by_id, maps_by_name, runtime_map_names)

    def get(self, key: str) -> MapDefinition | None:
        return self.maps_by_id.get(key) or self.maps_by_name.get(key)

    def require(self, key: str) -> MapDefinition:
        map_def = self.get(key)
        if map_def is None:
            raise KeyError(f"unknown map: {key}")
        return map_def

    def from_runtime(self, group: int, number: int) -> MapDefinition | None:
        name = self.runtime_map_names.get((group, number))
        return self.maps_by_name.get(name) if name is not None else None

    def require_layout(self, map_def: MapDefinition) -> LayoutDefinition:
        layout = self.layouts.get(map_def.layout_id)
        if layout is None:
            raise KeyError(f"map {map_def.id} references missing layout {map_def.layout_id}")
        return layout

    def load_collision_grid(self, map_or_key: MapDefinition | str) -> CollisionGrid:
        map_def = map_or_key if isinstance(map_or_key, MapDefinition) else self.require(map_or_key)
        layout = self.require_layout(map_def)
        if not layout.blockdata_filepath:
            raise FileNotFoundError(f"layout {layout.id} does not define blockdata_filepath")

        path = self.root / layout.blockdata_filepath
        data = path.read_bytes()
        expected_size = layout.width * layout.height * 2
        if len(data) != expected_size:
            raise ValueError(
                f"{layout.blockdata_filepath} has {len(data)} bytes; "
                f"expected {expected_size} for {layout.width}x{layout.height}"
            )

        raw_cells = tuple(
            data[offset] | (data[offset + 1] << 8)
            for offset in range(0, len(data), 2)
        )
        return CollisionGrid(layout.width, layout.height, raw_cells)

    def summarize(self, key: str) -> dict[str, Any]:
        map_def = self.require(key)
        layout = self.layouts.get(map_def.layout_id)
        return {
            "id": map_def.id,
            "name": map_def.name,
            "runtime": {"group": map_def.group, "number": map_def.number},
            "layout": (
                {
                    "id": layout.id,
                    "width": layout.width,
                    "height": layout.height,
                    "primary_tileset": layout.primary_tileset,
                    "secondary_tileset": layout.secondary_tileset,
                    "blockdata_filepath": layout.blockdata_filepath,
                }
                if layout
                else {"id": map_def.layout_id, "missing": True}
            ),
            "counts": {
                "connections": len(map_def.connections),
                "objects": len(map_def.object_events),
                "warps": len(map_def.warp_events),
                "coord_events": len(map_def.coord_events),
                "bg_events": len(map_def.bg_events),
            },
            "connections": list(map_def.connections),
            "warps": list(map_def.warp_events),
            "objects": list(map_def.object_events),
            "coord_events": list(map_def.coord_events),
            "bg_events": list(map_def.bg_events),
        }

    def validate(self) -> list[MapIssue]:
        issues: list[MapIssue] = []

        for (group, number), name in self.runtime_map_names.items():
            if name not in self.maps_by_name:
                issues.append(
                    MapIssue(
                        "GROUP_MAP_MISSING",
                        None,
                        f"map_groups ({group},{number}) references missing map directory {name}",
                    )
                )

        for map_def in self.maps_by_id.values():
            layout = self.layouts.get(map_def.layout_id)
            if layout is None:
                issues.append(
                    MapIssue(
                        "LAYOUT_MISSING",
                        map_def.id,
                        f"layout {map_def.layout_id} does not exist in layouts.json",
                    )
                )

            if map_def.group is None or map_def.number is None:
                issues.append(
                    MapIssue(
                        "MAP_NOT_GROUPED",
                        map_def.id,
                        f"map {map_def.name} is not present in map_groups.json",
                    )
                )

            for connection in map_def.connections:
                dest = connection.get("map")
                if isinstance(dest, str) and dest not in self.maps_by_id and dest != "MAP_DYNAMIC":
                    issues.append(MapIssue("CONNECTION_DEST_MISSING", map_def.id, f"connection targets {dest}"))

            for warp_index, warp in enumerate(map_def.warp_events):
                dest = warp.get("dest_map")
                dest_warp = warp.get("dest_warp_id")
                if isinstance(dest, str) and dest != "MAP_DYNAMIC":
                    target = self.maps_by_id.get(dest)
                    if target is None:
                        issues.append(MapIssue("WARP_DEST_MISSING", map_def.id, f"warp {warp_index} targets {dest}"))
                    elif isinstance(dest_warp, (str, int)):
                        try:
                            dest_index = int(dest_warp)
                        except (TypeError, ValueError):
                            dest_index = None
                        if dest_index is not None and not (0 <= dest_index < len(target.warp_events)):
                            issues.append(
                                MapIssue(
                                    "WARP_DEST_INDEX_INVALID",
                                    map_def.id,
                                    f"warp {warp_index} targets {dest} warp {dest_index}, but target has {len(target.warp_events)} warps",
                                )
                            )

            if layout is not None:
                event_sets = (
                    ("object", map_def.object_events),
                    ("warp", map_def.warp_events),
                    ("coord", map_def.coord_events),
                    ("bg", map_def.bg_events),
                )
                for kind, events in event_sets:
                    for index, event in enumerate(events):
                        x = event.get("x")
                        y = event.get("y")
                        if isinstance(x, int) and isinstance(y, int):
                            if not (0 <= x < layout.width and 0 <= y < layout.height):
                                issues.append(
                                    MapIssue(
                                        "EVENT_OUT_OF_BOUNDS",
                                        map_def.id,
                                        f"{kind} event {index} at ({x},{y}) outside {layout.width}x{layout.height}",
                                    )
                                )

        return issues
