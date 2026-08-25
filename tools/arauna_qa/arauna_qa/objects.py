from __future__ import annotations

from dataclasses import asdict, dataclass

from .symbols import SymbolTable

MAP_OFFSET = 7
OBJECT_EVENT_SIZE = 0x24
OBJECT_EVENT_COUNT = 16


def _s16(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset : offset + 2], "little", signed=True)


@dataclass(frozen=True)
class ObjectEventState:
    index: int
    active: bool
    is_player: bool
    frozen: bool
    invisible: bool
    local_id: int
    map_num: int
    map_group: int
    graphics_id: int
    movement_type: int
    trainer_type: int
    elevation: int
    initial_x: int
    initial_y: int
    current_x: int
    current_y: int
    previous_x: int
    previous_y: int
    facing_direction: int
    movement_direction: int
    current_metatile_behavior: int

    def to_dict(self) -> dict[str, int | bool]:
        return asdict(self)

    @property
    def position(self) -> tuple[int, int]:
        return self.current_x, self.current_y


class ObjectEventReader:
    """Decode Emerald's 16 runtime ObjectEvent slots from gObjectEvents."""

    def __init__(self, bridge, symbols: SymbolTable):
        self.bridge = bridge
        self.symbols = symbols

    @staticmethod
    def _decode(index: int, data: bytes) -> ObjectEventState:
        flags0 = data[0x00]
        flags1 = data[0x01]
        flags2 = data[0x02]
        directions = int.from_bytes(data[0x18:0x1A], "little")
        return ObjectEventState(
            index=index,
            active=bool(flags0 & 0x01),
            frozen=bool(flags1 & 0x01),
            invisible=bool(flags1 & 0x20),
            is_player=bool(flags2 & 0x01),
            graphics_id=data[0x05],
            movement_type=data[0x06],
            trainer_type=data[0x07],
            local_id=data[0x08],
            map_num=data[0x09],
            map_group=data[0x0A],
            elevation=data[0x0B] & 0x0F,
            initial_x=_s16(data, 0x0C) - MAP_OFFSET,
            initial_y=_s16(data, 0x0E) - MAP_OFFSET,
            current_x=_s16(data, 0x10) - MAP_OFFSET,
            current_y=_s16(data, 0x12) - MAP_OFFSET,
            previous_x=_s16(data, 0x14) - MAP_OFFSET,
            previous_y=_s16(data, 0x16) - MAP_OFFSET,
            facing_direction=directions & 0x0F,
            movement_direction=(directions >> 4) & 0x0F,
            current_metatile_behavior=data[0x1E],
        )

    def snapshot(self) -> tuple[ObjectEventState, ...]:
        base = self.symbols.address("gObjectEvents")
        raw = self.bridge.read_range(base, OBJECT_EVENT_SIZE * OBJECT_EVENT_COUNT)
        if len(raw) != OBJECT_EVENT_SIZE * OBJECT_EVENT_COUNT:
            raise RuntimeError(
                f"gObjectEvents read returned {len(raw)} bytes; expected "
                f"{OBJECT_EVENT_SIZE * OBJECT_EVENT_COUNT}"
            )
        return tuple(
            self._decode(
                index,
                raw[index * OBJECT_EVENT_SIZE : (index + 1) * OBJECT_EVENT_SIZE],
            )
            for index in range(OBJECT_EVENT_COUNT)
        )

    def active_on_map(
        self,
        map_group: int,
        map_num: int,
        *,
        include_player: bool = False,
        include_invisible: bool = False,
    ) -> tuple[ObjectEventState, ...]:
        result = []
        for obj in self.snapshot():
            if not obj.active or obj.map_group != map_group or obj.map_num != map_num:
                continue
            if not include_player and obj.is_player:
                continue
            if not include_invisible and obj.invisible:
                continue
            result.append(obj)
        return tuple(result)

    def find_index(self, index: int) -> ObjectEventState | None:
        if not 0 <= index < OBJECT_EVENT_COUNT:
            return None
        obj = self.snapshot()[index]
        return obj if obj.active else None

    def find_local_id(
        self,
        local_id: int,
        map_group: int,
        map_num: int,
    ) -> ObjectEventState | None:
        for obj in self.active_on_map(map_group, map_num, include_invisible=True):
            if obj.local_id == local_id:
                return obj
        return None
