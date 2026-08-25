from __future__ import annotations

from dataclasses import asdict, dataclass

from .symbols import SymbolTable

PARTY_SIZE = 6
POKEMON_SIZE = 0x64

SUBSTRUCT_ORDERS = (
    "GAEM", "GAME", "GEAM", "GEMA", "GMAE", "GMEA",
    "AGEM", "AGME", "AEGM", "AEMG", "AMGE", "AMEG",
    "EGAM", "EGMA", "EAGM", "EAMG", "EMGA", "EMAG",
    "MGAE", "MGEA", "MAGE", "MAEG", "MEGA", "MEAG",
)


def _u16(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset:offset + 2], "little")


def _u32(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset:offset + 4], "little")


@dataclass(frozen=True)
class PartyMonState:
    slot: int
    present: bool
    checksum_ok: bool
    species: int
    held_item: int
    experience: int
    friendship: int
    moves: tuple[int, int, int, int]
    pp: tuple[int, int, int, int]
    is_egg: bool
    ability_num: int
    status: int
    level: int
    hp: int
    max_hp: int
    attack: int
    defense: int
    speed: int
    sp_attack: int
    sp_defense: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class PartySnapshot:
    count: int
    mons: tuple[PartyMonState, ...]

    def to_dict(self) -> dict[str, object]:
        return {"count": self.count, "mons": [mon.to_dict() for mon in self.mons]}


class PartyReader:
    def __init__(self, bridge, symbols: SymbolTable):
        self.bridge = bridge
        self.symbols = symbols

    @staticmethod
    def _decrypt_secure(raw: bytes) -> tuple[dict[str, bytes], bool]:
        personality = _u32(raw, 0x00)
        ot_id = _u32(raw, 0x04)
        key = personality ^ ot_id
        encrypted = raw[0x20:0x50]
        decrypted = bytearray()
        for offset in range(0, len(encrypted), 4):
            word = int.from_bytes(encrypted[offset:offset + 4], "little") ^ key
            decrypted += word.to_bytes(4, "little")

        checksum = sum(
            int.from_bytes(decrypted[offset:offset + 2], "little")
            for offset in range(0, len(decrypted), 2)
        ) & 0xFFFF
        checksum_ok = checksum == _u16(raw, 0x1C)

        order = SUBSTRUCT_ORDERS[personality % 24]
        chunks = {
            label: bytes(decrypted[index * 12:(index + 1) * 12])
            for index, label in enumerate(order)
        }
        return chunks, checksum_ok

    @classmethod
    def decode_mon(cls, slot: int, raw: bytes) -> PartyMonState:
        if len(raw) != POKEMON_SIZE:
            raise ValueError(f"Pokemon slot must be {POKEMON_SIZE} bytes")
        chunks, checksum_ok = cls._decrypt_secure(raw)
        growth = chunks["G"]
        attacks = chunks["A"]
        misc = chunks["M"]
        iv_flags = _u32(misc, 0x04)

        species = _u16(growth, 0x00)
        has_species = bool(raw[0x13] & 0x02) and species != 0
        return PartyMonState(
            slot=slot,
            present=has_species,
            checksum_ok=checksum_ok,
            species=species,
            held_item=_u16(growth, 0x02),
            experience=_u32(growth, 0x04),
            friendship=growth[0x09],
            moves=tuple(_u16(attacks, i * 2) for i in range(4)),
            pp=tuple(attacks[0x08 + i] for i in range(4)),
            is_egg=bool((iv_flags >> 30) & 1),
            ability_num=(iv_flags >> 31) & 1,
            status=_u32(raw, 0x50),
            level=raw[0x54],
            hp=_u16(raw, 0x56),
            max_hp=_u16(raw, 0x58),
            attack=_u16(raw, 0x5A),
            defense=_u16(raw, 0x5C),
            speed=_u16(raw, 0x5E),
            sp_attack=_u16(raw, 0x60),
            sp_defense=_u16(raw, 0x62),
        )

    def _read_party(self, party_symbol: str, count_symbol: str) -> PartySnapshot:
        count = min(self.bridge.read8(self.symbols.address(count_symbol)), PARTY_SIZE)
        raw = self.bridge.read_range(self.symbols.address(party_symbol), PARTY_SIZE * POKEMON_SIZE)
        if len(raw) != PARTY_SIZE * POKEMON_SIZE:
            raise RuntimeError("party read returned an unexpected size")
        mons = tuple(
            self.decode_mon(slot, raw[slot * POKEMON_SIZE:(slot + 1) * POKEMON_SIZE])
            for slot in range(PARTY_SIZE)
        )
        return PartySnapshot(count=count, mons=mons[:count])

    def player(self) -> PartySnapshot:
        return self._read_party("gPlayerParty", "gPlayerPartyCount")

    def enemy(self) -> PartySnapshot:
        return self._read_party("gEnemyParty", "gEnemyPartyCount")
