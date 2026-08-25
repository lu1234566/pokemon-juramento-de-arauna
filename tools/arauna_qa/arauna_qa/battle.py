from __future__ import annotations

from dataclasses import asdict, dataclass

from .symbols import SymbolTable

MAX_BATTLERS = 4
BATTLE_MON_SIZE = 0x58


def _u16(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset:offset + 2], "little")


def _u32(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset:offset + 4], "little")


@dataclass(frozen=True)
class BattleMonState:
    battler: int
    side: str | None
    species: int
    level: int
    hp: int
    max_hp: int
    status1: int
    status2: int
    ability: int
    types: tuple[int, int]
    item: int
    moves: tuple[int, int, int, int]
    pp: tuple[int, int, int, int]
    attack: int
    defense: int
    speed: int
    sp_attack: int
    sp_defense: int
    stat_stages: tuple[int, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class BattleSnapshot:
    battlers_count: int
    mons: tuple[BattleMonState, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "battlers_count": self.battlers_count,
            "mons": [mon.to_dict() for mon in self.mons],
        }


class BattleReader:
    def __init__(self, bridge, symbols: SymbolTable):
        self.bridge = bridge
        self.symbols = symbols

    def snapshot(self) -> BattleSnapshot:
        count_symbol = self.symbols.get("gBattlersCount")
        count = self.bridge.read8(count_symbol.address) if count_symbol is not None else MAX_BATTLERS
        count = max(0, min(int(count), MAX_BATTLERS))

        raw = self.bridge.read_range(
            self.symbols.address("gBattleMons"),
            MAX_BATTLERS * BATTLE_MON_SIZE,
        )
        if len(raw) != MAX_BATTLERS * BATTLE_MON_SIZE:
            raise RuntimeError("gBattleMons read returned an unexpected size")

        positions_symbol = self.symbols.get("gBattlerPositions")
        positions = (
            self.bridge.read_range(positions_symbol.address, MAX_BATTLERS)
            if positions_symbol is not None
            else bytes(range(MAX_BATTLERS))
        )

        mons = []
        for battler in range(count):
            data = raw[battler * BATTLE_MON_SIZE:(battler + 1) * BATTLE_MON_SIZE]
            position = positions[battler] if battler < len(positions) else battler
            side = "opponent" if position & 1 else "player"
            mons.append(
                BattleMonState(
                    battler=battler,
                    side=side,
                    species=_u16(data, 0x00),
                    attack=_u16(data, 0x02),
                    defense=_u16(data, 0x04),
                    speed=_u16(data, 0x06),
                    sp_attack=_u16(data, 0x08),
                    sp_defense=_u16(data, 0x0A),
                    moves=tuple(_u16(data, 0x0C + i * 2) for i in range(4)),
                    stat_stages=tuple(data[0x18:0x20]),
                    ability=data[0x20],
                    types=(data[0x21], data[0x22]),
                    pp=tuple(data[0x24 + i] for i in range(4)),
                    hp=_u16(data, 0x28),
                    level=data[0x2A],
                    max_hp=_u16(data, 0x2C),
                    item=_u16(data, 0x2E),
                    status1=_u32(data, 0x4C),
                    status2=_u32(data, 0x50),
                )
            )
        return BattleSnapshot(count, tuple(mons))
