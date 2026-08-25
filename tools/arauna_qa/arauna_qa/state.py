from __future__ import annotations

from dataclasses import asdict, dataclass

from .symbols import SymbolTable

MAP_OFFSET = 7
OBJECT_EVENT_SIZE = 0x24
MAIN_READ_SIZE = 0x43A
PLAYER_AVATAR_READ_SIZE = 0x24
MAP_HEADER_READ_SIZE = 0x1C


def _u16(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset : offset + 2], "little")


def _s16(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset : offset + 2], "little", signed=True)


def _u32(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset : offset + 4], "little")


@dataclass(frozen=True)
class AraunaState:
    frame: int
    map_group: int | None
    map_num: int | None
    map_layout_id: int
    region_map_section_id: int
    map_type: int
    weather: int
    music: int
    player_valid: bool
    player_x: int | None
    player_y: int | None
    player_x_internal: int | None
    player_y_internal: int | None
    facing: int | None
    movement_direction: int | None
    elevation: int | None
    metatile_behavior: int | None
    avatar_flags: int
    running_state: int
    tile_transition_state: int
    field_controls_locked: bool | None
    script_enabled: bool | None
    script_mode: int | None
    script_ptr: int | None
    in_battle: bool
    held_keys: int
    new_keys: int
    callback1: int
    callback2: int

    def to_dict(self) -> dict[str, int | bool | None]:
        return asdict(self)


class AraunaStateReader:
    def __init__(self, bridge, symbols: SymbolTable):
        self.bridge = bridge
        self.symbols = symbols

    def _read_optional_u8(self, symbol_name: str) -> int | None:
        symbol = self.symbols.get(symbol_name)
        if symbol is None:
            return None
        return self.bridge.read8(symbol.address)

    def snapshot(self) -> AraunaState:
        main = self.bridge.read_range(self.symbols.address("gMain"), MAIN_READ_SIZE)
        avatar = self.bridge.read_range(
            self.symbols.address("gPlayerAvatar"), PLAYER_AVATAR_READ_SIZE
        )
        map_header = self.bridge.read_range(
            self.symbols.address("gMapHeader"), MAP_HEADER_READ_SIZE
        )

        object_event_id = avatar[0x05]
        player_valid = False
        player_x_internal = None
        player_y_internal = None
        player_x = None
        player_y = None
        map_num = None
        map_group = None
        facing = None
        movement_direction = None
        elevation = None
        metatile_behavior = None

        # OBJECT_EVENTS_COUNT is 16 in vanilla Emerald. The object index is stored
        # in a byte, but reject obviously invalid values before computing an address.
        if object_event_id < 16:
            object_base = (
                self.symbols.address("gObjectEvents")
                + object_event_id * OBJECT_EVENT_SIZE
            )
            obj = self.bridge.read_range(object_base, OBJECT_EVENT_SIZE)
            active = bool(obj[0x00] & 0x01)
            is_player = bool(obj[0x02] & 0x01)
            player_valid = active and is_player
            if player_valid:
                map_num = obj[0x09]
                map_group = obj[0x0A]
                elevation = obj[0x0B] & 0x0F
                player_x_internal = _s16(obj, 0x10)
                player_y_internal = _s16(obj, 0x12)
                player_x = player_x_internal - MAP_OFFSET
                player_y = player_y_internal - MAP_OFFSET
                directions = _u16(obj, 0x18)
                facing = directions & 0x0F
                movement_direction = (directions >> 4) & 0x0F
                metatile_behavior = obj[0x1E]

        script_enabled = self._read_optional_u8("sGlobalScriptContextStatus")
        field_controls_locked = self._read_optional_u8("sLockFieldControls")

        script_mode = None
        script_ptr = None
        script_symbol = self.symbols.get("sGlobalScriptContext")
        if script_symbol is not None:
            script_head = self.bridge.read_range(script_symbol.address, 12)
            script_mode = script_head[0x01]
            script_ptr = _u32(script_head, 0x08)

        return AraunaState(
            frame=_u32(main, 0x20),
            map_group=map_group,
            map_num=map_num,
            map_layout_id=_u16(map_header, 0x12),
            region_map_section_id=map_header[0x14],
            map_type=map_header[0x17],
            weather=map_header[0x16],
            music=_u16(map_header, 0x10),
            player_valid=player_valid,
            player_x=player_x,
            player_y=player_y,
            player_x_internal=player_x_internal,
            player_y_internal=player_y_internal,
            facing=facing,
            movement_direction=movement_direction,
            elevation=elevation,
            metatile_behavior=metatile_behavior,
            avatar_flags=avatar[0x00],
            running_state=avatar[0x02],
            tile_transition_state=avatar[0x03],
            field_controls_locked=(
                bool(field_controls_locked) if field_controls_locked is not None else None
            ),
            script_enabled=(
                bool(script_enabled) if script_enabled is not None else None
            ),
            script_mode=script_mode,
            script_ptr=script_ptr,
            in_battle=bool(main[0x439] & 0x02),
            held_keys=_u16(main, 0x2C),
            new_keys=_u16(main, 0x2E),
            callback1=_u32(main, 0x00),
            callback2=_u32(main, 0x04),
        )
