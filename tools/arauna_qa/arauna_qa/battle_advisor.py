from __future__ import annotations

from dataclasses import asdict, dataclass

from .battle import BattleMonState, BattleReader, BattleSnapshot
from .symbols import SymbolTable

BATTLE_MOVE_SIZE = 9
TYPE_EFFECT_TABLE_SIZE = 336
TYPE_MUL_NORMAL = 10
TYPE_FORESIGHT = 0xFE
TYPE_ENDTABLE = 0xFF


def _s8(value: int) -> int:
    return value - 256 if value >= 128 else value


@dataclass(frozen=True)
class MoveInfo:
    move_id: int
    effect: int
    power: int
    type: int
    accuracy: int
    base_pp: int
    secondary_effect_chance: int
    target: int
    priority: int
    flags: int

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass(frozen=True)
class MoveAdvice:
    battler: int
    target_battler: int
    slot: int
    move: MoveInfo
    current_pp: int
    stab: float
    effectiveness: float
    accuracy_factor: float
    score: float
    caveats: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "battler": self.battler,
            "target_battler": self.target_battler,
            "slot": self.slot,
            "move": self.move.to_dict(),
            "current_pp": self.current_pp,
            "stab": self.stab,
            "effectiveness": self.effectiveness,
            "accuracy_factor": self.accuracy_factor,
            "score": self.score,
            "caveats": list(self.caveats),
        }


@dataclass(frozen=True)
class BattleAdvice:
    available: bool
    reason: str
    recommendations: tuple[MoveAdvice, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "available": self.available,
            "reason": self.reason,
            "recommendations": [item.to_dict() for item in self.recommendations],
        }


class BattleMetadataReader:
    def __init__(self, bridge, symbols: SymbolTable):
        self.bridge = bridge
        self.symbols = symbols
        self._type_table: bytes | None = None

    def move(self, move_id: int) -> MoveInfo:
        if move_id < 0:
            raise ValueError("move_id must be non-negative")
        address = self.symbols.address("gBattleMoves") + move_id * BATTLE_MOVE_SIZE
        raw = self.bridge.read_range(address, BATTLE_MOVE_SIZE)
        if len(raw) != BATTLE_MOVE_SIZE:
            raise RuntimeError("gBattleMoves read returned an unexpected size")
        return MoveInfo(
            move_id=move_id,
            effect=raw[0],
            power=raw[1],
            type=raw[2],
            accuracy=raw[3],
            base_pp=raw[4],
            secondary_effect_chance=raw[5],
            target=raw[6],
            priority=_s8(raw[7]),
            flags=raw[8],
        )

    def _load_type_table(self) -> bytes:
        if self._type_table is None:
            raw = self.bridge.read_range(
                self.symbols.address("gTypeEffectiveness"),
                TYPE_EFFECT_TABLE_SIZE,
            )
            if len(raw) != TYPE_EFFECT_TABLE_SIZE:
                raise RuntimeError("gTypeEffectiveness read returned an unexpected size")
            self._type_table = raw
        return self._type_table

    def type_multiplier(self, attack_type: int, defend_types: tuple[int, int]) -> float:
        table = self._load_type_table()
        multiplier = 1.0
        for defend_type in dict.fromkeys(defend_types):
            type_mul = TYPE_MUL_NORMAL
            for offset in range(0, len(table) - 2, 3):
                atk, defense, value = table[offset : offset + 3]
                if atk == TYPE_ENDTABLE:
                    break
                if atk == TYPE_FORESIGHT or defense == TYPE_FORESIGHT:
                    continue
                if atk == attack_type and defense == defend_type:
                    type_mul = value
                    break
            multiplier *= type_mul / TYPE_MUL_NORMAL
        return multiplier


class BattleAdvisor:
    """Read-only move heuristic; intentionally not a full battle AI."""

    def __init__(
        self,
        battle_reader: BattleReader,
        metadata: BattleMetadataReader,
    ):
        self.battle_reader = battle_reader
        self.metadata = metadata

    @staticmethod
    def _pick_side(snapshot: BattleSnapshot, side: str) -> BattleMonState | None:
        for mon in snapshot.mons:
            if mon.side == side and mon.species != 0 and mon.hp > 0:
                return mon
        return None

    def recommend(self) -> BattleAdvice:
        snapshot = self.battle_reader.snapshot()
        attacker = self._pick_side(snapshot, "player")
        defender = self._pick_side(snapshot, "opponent")
        if attacker is None or defender is None:
            return BattleAdvice(False, "active_battlers_unavailable", ())

        ranked: list[MoveAdvice] = []
        for slot, (move_id, current_pp) in enumerate(zip(attacker.moves, attacker.pp)):
            if move_id == 0 or current_pp <= 0:
                continue
            move = self.metadata.move(move_id)
            stab = 1.5 if move.type in attacker.types else 1.0
            effectiveness = self.metadata.type_multiplier(move.type, defender.types)
            accuracy_factor = 1.0 if move.accuracy == 0 else move.accuracy / 100.0
            score = float(move.power) * stab * effectiveness * accuracy_factor
            caveats = [
                "heuristic_only",
                "special_move_effects_not_scored",
                "abilities_items_and_status_interactions_not_scored",
            ]
            if move.power == 0:
                caveats.append("status_or_variable_power_move_scored_as_zero")
            ranked.append(
                MoveAdvice(
                    battler=attacker.battler,
                    target_battler=defender.battler,
                    slot=slot,
                    move=move,
                    current_pp=current_pp,
                    stab=stab,
                    effectiveness=effectiveness,
                    accuracy_factor=accuracy_factor,
                    score=score,
                    caveats=tuple(caveats),
                )
            )

        if not ranked:
            return BattleAdvice(False, "no_usable_moves_observed", ())
        ranked.sort(key=lambda item: (item.score, item.current_pp, -item.slot), reverse=True)
        return BattleAdvice(True, "ranked", tuple(ranked))
