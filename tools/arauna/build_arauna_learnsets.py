#!/usr/bin/env python3
"""Generate family-aware level-up identities for all 386 Arauna Fakemon."""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEX_SIZE = 386

# low, physical mid/high/finisher, special mid/high/finisher, early/late status
TYPE_MOVES = {
    "normal": ("TACKLE", "BODY_SLAM", "DOUBLE_EDGE", "GIGA_IMPACT", "SWIFT", "HYPER_VOICE", "HYPER_BEAM", "GROWL", "WORK_UP"),
    "fire": ("EMBER", "FLAME_WHEEL", "BLAZE_KICK", "FLARE_BLITZ", "FLAME_BURST", "FLAMETHROWER", "FIRE_BLAST", "SMOKESCREEN", "SUNNY_DAY"),
    "water": ("WATER_GUN", "AQUA_JET", "AQUA_TAIL", "LIQUIDATION", "BUBBLE_BEAM", "SCALD", "HYDRO_PUMP", "TAIL_WHIP", "RAIN_DANCE"),
    "grass": ("ABSORB", "RAZOR_LEAF", "LEAF_BLADE", "POWER_WHIP", "MEGA_DRAIN", "ENERGY_BALL", "SOLAR_BEAM", "GROWTH", "SYNTHESIS"),
    "electric": ("THUNDER_SHOCK", "SPARK", "THUNDER_FANG", "WILD_CHARGE", "SHOCK_WAVE", "DISCHARGE", "THUNDER", "THUNDER_WAVE", "CHARGE"),
    "ice": ("POWDER_SNOW", "ICE_SHARD", "ICE_FANG", "ICICLE_CRASH", "ICY_WIND", "ICE_BEAM", "BLIZZARD", "MIST", "HAIL"),
    "fighting": ("ARM_THRUST", "KARATE_CHOP", "BRICK_BREAK", "CLOSE_COMBAT", "VACUUM_WAVE", "AURA_SPHERE", "FOCUS_BLAST", "FOCUS_ENERGY", "BULK_UP"),
    "poison": ("POISON_STING", "POISON_FANG", "POISON_JAB", "GUNK_SHOT", "ACID", "SLUDGE_BOMB", "SLUDGE_WAVE", "POISON_POWDER", "TOXIC"),
    "ground": ("MUD_SLAP", "DIG", "BULLDOZE", "EARTHQUAKE", "MUD_SHOT", "EARTH_POWER", "SCORCHING_SANDS", "SAND_ATTACK", "SANDSTORM"),
    "flying": ("GUST", "WING_ATTACK", "AERIAL_ACE", "BRAVE_BIRD", "AIR_CUTTER", "AIR_SLASH", "HURRICANE", "LEER", "TAILWIND"),
    "psychic": ("CONFUSION", "ZEN_HEADBUTT", "PSYCHO_CUT", "PSYCHIC_FANGS", "PSYBEAM", "PSYCHIC", "FUTURE_SIGHT", "MEDITATE", "CALM_MIND"),
    "bug": ("STRUGGLE_BUG", "BUG_BITE", "X_SCISSOR", "MEGAHORN", "SIGNAL_BEAM", "BUG_BUZZ", "POLLEN_PUFF", "STRING_SHOT", "QUIVER_DANCE"),
    "rock": ("ROCK_THROW", "ROCK_TOMB", "ROCK_SLIDE", "STONE_EDGE", "ANCIENT_POWER", "POWER_GEM", "METEOR_BEAM", "HARDEN", "ROCK_POLISH"),
    "ghost": ("ASTONISH", "SHADOW_SNEAK", "SHADOW_CLAW", "POLTERGEIST", "NIGHT_SHADE", "SHADOW_BALL", "HEX", "CONFUSE_RAY", "CURSE"),
    "dragon": ("TWISTER", "DRAGON_CLAW", "DRAGON_RUSH", "OUTRAGE", "DRAGON_BREATH", "DRAGON_PULSE", "DRACO_METEOR", "LEER", "DRAGON_DANCE"),
    "dark": ("BITE", "PURSUIT", "NIGHT_SLASH", "SUCKER_PUNCH", "SNARL", "DARK_PULSE", "FOUL_PLAY", "TAUNT", "NASTY_PLOT"),
    "steel": ("METAL_CLAW", "BULLET_PUNCH", "IRON_HEAD", "METEOR_MASH", "MIRROR_SHOT", "FLASH_CANNON", "STEEL_BEAM", "HARDEN", "IRON_DEFENSE"),
    "fairy": ("FAIRY_WIND", "PLAY_ROUGH", "PLAY_ROUGH", "MISTY_EXPLOSION", "DISARMING_VOICE", "DAZZLING_GLEAM", "MOONBLAST", "CHARM", "MISTY_TERRAIN"),
}

TYPE_SIGNATURES = {
    "normal": (("DOUBLE_EDGE", "EXTREME_SPEED", "GIGA_IMPACT"), ("HYPER_VOICE", "BOOMBURST", "HYPER_BEAM")),
    "fire": (("FLARE_BLITZ", "BLAZE_KICK", "FIRE_LASH"), ("FIRE_BLAST", "OVERHEAT", "ERUPTION")),
    "water": (("LIQUIDATION", "WAVE_CRASH", "AQUA_TAIL"), ("HYDRO_PUMP", "WATER_SPOUT", "STEAM_ERUPTION")),
    "grass": (("POWER_WHIP", "SOLAR_BLADE", "LEAF_BLADE"), ("LEAF_STORM", "SOLAR_BEAM", "PETAL_DANCE")),
    "electric": (("WILD_CHARGE", "VOLT_TACKLE", "THUNDER_PUNCH"), ("THUNDER", "ZAP_CANNON", "RISING_VOLTAGE")),
    "ice": (("ICICLE_CRASH", "TRIPLE_AXEL", "ICE_HAMMER"), ("BLIZZARD", "FREEZE_DRY", "SHEER_COLD")),
    "fighting": (("CLOSE_COMBAT", "DRAIN_PUNCH", "SUPERPOWER"), ("FOCUS_BLAST", "AURA_SPHERE", "VACUUM_WAVE")),
    "poison": (("GUNK_SHOT", "POISON_JAB", "DIRE_CLAW"), ("SLUDGE_WAVE", "SLUDGE_BOMB", "VENOSHOCK")),
    "ground": (("EARTHQUAKE", "HEADLONG_RUSH", "HIGH_HORSEPOWER"), ("EARTH_POWER", "SCORCHING_SANDS", "SANDSEAR_STORM")),
    "flying": (("BRAVE_BIRD", "DUAL_WINGBEAT", "DRILL_PECK"), ("HURRICANE", "AIR_SLASH", "BLEAKWIND_STORM")),
    "psychic": (("PSYCHIC_FANGS", "PSYCHO_CUT", "ZEN_HEADBUTT"), ("PSYCHIC", "FUTURE_SIGHT", "EXPANDING_FORCE")),
    "bug": (("MEGAHORN", "FIRST_IMPRESSION", "X_SCISSOR"), ("BUG_BUZZ", "POLLEN_PUFF", "SIGNAL_BEAM")),
    "rock": (("STONE_EDGE", "HEAD_SMASH", "ROCK_WRECKER"), ("METEOR_BEAM", "POWER_GEM", "ANCIENT_POWER")),
    "ghost": (("POLTERGEIST", "SHADOW_CLAW", "PHANTOM_FORCE"), ("SHADOW_BALL", "HEX", "INFERNAL_PARADE")),
    "dragon": (("OUTRAGE", "DRAGON_RUSH", "DRAGON_CLAW"), ("DRACO_METEOR", "DRAGON_PULSE", "CORE_ENFORCER")),
    "dark": (("SUCKER_PUNCH", "KNOCK_OFF", "WICKED_BLOW"), ("DARK_PULSE", "FOUL_PLAY", "FIERY_WRATH")),
    "steel": (("METEOR_MASH", "IRON_HEAD", "DOUBLE_IRON_BASH"), ("STEEL_BEAM", "FLASH_CANNON", "MAKE_IT_RAIN")),
    "fairy": (("PLAY_ROUGH", "SPIRIT_BREAK", "MISTY_EXPLOSION"), ("MOONBLAST", "DAZZLING_GLEAM", "FLEUR_CANNON")),
}

ROLE_MOVE = {
    "hp": "RECOVER", "atk": "SWORDS_DANCE", "def": "IRON_DEFENSE",
    "spa": "CALM_MIND", "spd": "AMNESIA", "spe": "AGILITY",
}

THEMATIC_SIGNATURES = (
    (("cachorro", "cão", "cao", "canino", "lobo", "onça", "gato", "felino"), "CRUNCH"),
    (("pica-pau", "quero-quero", "tucano", "beija-flor", "ave", "pássaro", "passaro"), "BRAVE_BIRD"),
    (("cobra", "serpente", "sucuri", "jiboia"), "COIL"),
    (("peixe", "piranha", "tubarão", "tubarao", "pirarucu"), "AQUA_TAIL"),
    (("formiga", "borboleta", "abelha", "besouro", "mosquito", "inseto"), "FIRST_IMPRESSION"),
    (("flor", "árvore", "arvore", "cacto", "orquídea", "orquidea"), "SOLAR_BLADE"),
    (("pedra", "rocha", "montanha", "cristal", "minério", "minerio"), "STONE_EDGE"),
    (("samba", "maracatu", "frevo", "música", "musica", "cantor", "canto"), "BOOMBURST"),
    (("dragão", "dragao"), "DRAGON_RUSH"),
)

FORBIDDEN_FIELD_MOVES = {
    "CUT", "FLY", "SURF", "STRENGTH", "ROCK_SMASH", "WATERFALL", "DIVE",
}


def normalize(value: str) -> str:
    return unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()


def move_constants(path: Path) -> set[str]:
    return set(re.findall(r"\bMOVE_([A-Z0-9_]+)\b", path.read_text(encoding="utf-8")))


def evolution_level(method: str) -> int:
    match = re.search(r"(\d+)", method)
    if not match:
        raise ValueError(f"unsupported evolution method: {method}")
    return int(match.group(1))


def family_context(entries: list[dict]) -> tuple[dict[int, int], dict[int, int], dict[int, int], dict[int, list[dict]]]:
    parent = {}
    incoming_level = {}
    for entry in entries:
        for evolution in entry.get("evolvesTo") or []:
            child = int(evolution["id"])
            parent[child] = int(entry["id"])
            incoming_level[child] = evolution_level(evolution["method"])
    roots = {}
    stages = {}
    families: dict[int, list[dict]] = {}
    for entry in entries:
        number = int(entry["id"])
        cursor = number
        stage = 0
        seen = set()
        while cursor in parent and cursor not in seen:
            seen.add(cursor)
            cursor = parent[cursor]
            stage += 1
        roots[number] = cursor
        stages[number] = stage
        families.setdefault(cursor, []).append(entry)
    return roots, stages, incoming_level, families


def battle_role(entry: dict) -> str:
    order = ("hp", "atk", "def", "spa", "spd", "spe")
    return max(order, key=lambda key: (int(entry["stats"][key]), -order.index(key)))


def thematic_signature(members: list[dict], known_moves: set[str]) -> str | None:
    text = normalize(" ".join(
        f"{member.get('name', '')} {member.get('inspiration', '')}"
        for member in members
    ))
    for keywords, move in THEMATIC_SIGNATURES:
        if move in known_moves and any(normalize(keyword) in text for keyword in keywords):
            return move
    return None


def family_identity(root: int, members: list[dict], known_moves: set[str]) -> dict[str, str]:
    representative = max(members, key=lambda entry: sum(int(value) for value in entry["stats"].values()))
    physical = int(representative["stats"]["atk"]) >= int(representative["stats"]["spa"])
    types = []
    for member in members:
        for type_name in member.get("types") or ["normal"]:
            if type_name not in types:
                types.append(type_name)
    themed = thematic_signature(members, known_moves)
    pool = TYPE_SIGNATURES[types[0]][0 if physical else 1]
    available = [move for move in pool if move in known_moves]
    if not available:
        raise ValueError(f"family #{root:03d} has no valid signature move")
    signature = themed or available[root % len(available)]
    if signature not in known_moves:
        signature = available[root % len(available)]
    role = battle_role(representative)
    return {
        "signature": signature,
        "role": role,
        "role_move": ROLE_MOVE[role],
        "final_types": "/".join(types[:2]),
    }


def choose_moves(entry: dict, identity: dict[str, str], incoming_level: int | None) -> list[tuple[int, str]]:
    types = entry.get("types") or ["normal"]
    family_types = identity["final_types"].split("/")
    primary = TYPE_MOVES[types[0]]
    secondary_name = types[1] if len(types) > 1 else family_types[1] if len(family_types) > 1 else None
    secondary = TYPE_MOVES[secondary_name] if secondary_name else None
    physical = int(entry["stats"]["atk"]) >= int(entry["stats"]["spa"])
    mid, high, finisher = (1, 2, 3) if physical else (4, 5, 6)
    opposite_high = 5 if physical else 2
    start_status = "LEER" if physical else "GROWL"

    candidates = [
        (1, primary[0]),
        (1, start_status),
        (5, primary[7]),
        (9, primary[mid]),
        (13, secondary[0] if secondary else "QUICK_ATTACK"),
        (17, primary[8]),
        (22, primary[high]),
        (27, identity["role_move"]),
        (32, secondary[mid] if secondary else primary[opposite_high]),
        (38, secondary[high] if secondary else primary[finisher]),
        (45, identity["signature"]),
        (52, secondary[finisher] if secondary else primary[6 if physical else 3]),
        (58, primary[finisher]),
    ]
    if incoming_level is not None and secondary is not None:
        candidates.append((incoming_level, secondary[mid]))

    result = []
    seen = set()
    for level, move in sorted(candidates, key=lambda item: item[0]):
        if move in FORBIDDEN_FIELD_MOVES or move in seen:
            continue
        result.append((level, move))
        seen.add(move)

    fallbacks = list(primary) + (list(secondary) if secondary else []) + [
        identity["role_move"], "PROTECT", "ENDURE", "REST", "SUBSTITUTE",
    ]
    next_level = 60
    for move in fallbacks:
        if len(result) >= 10:
            break
        if move in FORBIDDEN_FIELD_MOVES or move in seen:
            continue
        result.append((next_level, move))
        seen.add(move)
        next_level += 2
    return sorted(result, key=lambda item: item[0])


def build(entries: list[dict], known_moves: set[str]) -> tuple[str, str]:
    if len(entries) != DEX_SIZE or {int(entry["id"]) for entry in entries} != set(range(1, DEX_SIZE + 1)):
        raise ValueError("Arauna source must contain IDs 001-386 exactly")

    configured_moves = {
        move for values in TYPE_MOVES.values() for move in values
    } | {
        move for styles in TYPE_SIGNATURES.values() for values in styles for move in values
    } | set(ROLE_MOVE.values()) | {move for _, move in THEMATIC_SIGNATURES} | {
        "LEER", "GROWL", "QUICK_ATTACK", "PROTECT", "ENDURE", "REST", "SUBSTITUTE",
    }
    unknown = configured_moves - known_moves
    if unknown:
        raise ValueError(f"unknown move constants: {', '.join(sorted(unknown))}")

    roots, stages, incoming_levels, families = family_context(entries)
    identities = {
        root: family_identity(root, members, known_moves)
        for root, members in families.items()
    }
    chunks = [
        "// Auto-generated by tools/arauna/build_arauna_learnsets.py.",
        "// Family-aware level-up identities for Arauna Dex slots 001-386.",
        "",
        "#ifndef GUARD_ARAUNA_LEVEL_UP_LEARNSETS_H",
        "#define GUARD_ARAUNA_LEVEL_UP_LEARNSETS_H",
        "",
    ]
    audit_rows = []
    for entry in entries:
        number = int(entry["id"])
        root = roots[number]
        identity = identities[root]
        moves = choose_moves(entry, identity, incoming_levels.get(number))
        if not 10 <= len(moves) <= 14:
            raise ValueError(f"Arauna learnset #{number:03d} has {len(moves)} moves")
        chunks.append(f"static const struct LevelUpMove sArauna{number:03d}LevelUpLearnset[] = {{")
        for level, move in moves:
            chunks.append(f"    LEVEL_UP_MOVE({level:2d}, MOVE_{move}),")
        chunks.extend(("    LEVEL_UP_END", "};", ""))
        audit_rows.append({
            "id": f"{number:03d}",
            "name": entry["name"],
            "family_root": f"{root:03d}",
            "stage": str(stages[number]),
            "types": "/".join(entry.get("types") or ["normal"]),
            "battle_role": identity["role"],
            "role_move": f"MOVE_{identity['role_move']}",
            "signature_move": f"MOVE_{identity['signature']}",
            "move_count": str(len(moves)),
            "first_stab_level": str(min(
                level for level, move in moves
                if move in TYPE_MOVES[(entry.get("types") or ["normal"])[0]]
            )),
            "final_move": f"MOVE_{moves[-1][1]}",
        })
    chunks.extend(("#endif // GUARD_ARAUNA_LEVEL_UP_LEARNSETS_H", ""))

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(audit_rows[0]))
    writer.writeheader()
    writer.writerows(audit_rows)
    return "\n".join(chunks), buffer.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dex", type=Path, default=ROOT / "docs/arauna/source/pokedex.json")
    parser.add_argument("--moves", type=Path, default=ROOT / "include/constants/moves.h")
    parser.add_argument("--out", type=Path, default=ROOT / "src/data/pokemon/level_up_learnsets/arauna.h")
    parser.add_argument("--audit-out", type=Path, default=ROOT / "docs/arauna/ARAUNA_LEARNSET_AUDIT.csv")
    args = parser.parse_args()

    entries = json.loads(args.dex.read_text(encoding="utf-8"))["pokemon"]
    output, audit = build(entries, move_constants(args.moves))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(output, encoding="utf-8")
    args.audit_out.parent.mkdir(parents=True, exist_ok=True)
    args.audit_out.write_text(audit, encoding="utf-8")
    print(f"generated {len(entries)} family-aware Arauna learnsets at {args.out}")


if __name__ == "__main__":
    main()
