#!/usr/bin/env python3
"""Build coherent battle/biology profiles and TM overlays for all 386 Fakemon.

The Arauna Dex deliberately reuses the first 386 engine species slots.  This
generator removes the remaining biological data inherited from those original
species while keeping the slot mapping stable for saves, scripts and graphics.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEX_SIZE = 386

TYPE_ABILITIES = {
    "normal": ("ABILITY_RUN_AWAY", "ABILITY_PICKUP"),
    "fire": ("ABILITY_BLAZE", "ABILITY_FLASH_FIRE"),
    "water": ("ABILITY_TORRENT", "ABILITY_SWIFT_SWIM"),
    "grass": ("ABILITY_OVERGROW", "ABILITY_CHLOROPHYLL"),
    "electric": ("ABILITY_STATIC", "ABILITY_LIGHTNING_ROD"),
    "ice": ("ABILITY_ICE_BODY", "ABILITY_SNOW_CLOAK"),
    "fighting": ("ABILITY_GUTS", "ABILITY_INNER_FOCUS"),
    "poison": ("ABILITY_POISON_POINT", "ABILITY_LIQUID_OOZE"),
    "ground": ("ABILITY_SAND_VEIL", "ABILITY_ARENA_TRAP"),
    "flying": ("ABILITY_KEEN_EYE", "ABILITY_BIG_PECKS"),
    "psychic": ("ABILITY_SYNCHRONIZE", "ABILITY_TELEPATHY"),
    "bug": ("ABILITY_SWARM", "ABILITY_COMPOUND_EYES"),
    "rock": ("ABILITY_STURDY", "ABILITY_ROCK_HEAD"),
    "ghost": ("ABILITY_LEVITATE", "ABILITY_CURSED_BODY"),
    "dragon": ("ABILITY_INNER_FOCUS", "ABILITY_SHED_SKIN"),
    "dark": ("ABILITY_INTIMIDATE", "ABILITY_PRANKSTER"),
    "steel": ("ABILITY_CLEAR_BODY", "ABILITY_BATTLE_ARMOR"),
    "fairy": ("ABILITY_CUTE_CHARM", "ABILITY_MAGIC_GUARD"),
}

STAT_ABILITIES = {
    "hp": "ABILITY_REGENERATOR",
    "atk": "ABILITY_SHEER_FORCE",
    "def": "ABILITY_BATTLE_ARMOR",
    "spa": "ABILITY_COMPETITIVE",
    "spd": "ABILITY_FILTER",
    "spe": "ABILITY_QUICK_FEET",
}

ABILITY_FALLBACKS = (
    "ABILITY_NATURAL_CURE", "ABILITY_ADAPTABILITY", "ABILITY_PRESSURE",
    "ABILITY_ANTICIPATION", "ABILITY_KEEN_EYE", "ABILITY_INNER_FOCUS",
)

STARTER_ABILITIES = {
    1: ("ABILITY_BLAZE", "ABILITY_KEEN_EYE", "ABILITY_FLASH_FIRE"),
    2: ("ABILITY_BLAZE", "ABILITY_INTIMIDATE", "ABILITY_FLASH_FIRE"),
    3: ("ABILITY_BLAZE", "ABILITY_INTIMIDATE", "ABILITY_MULTISCALE"),
    4: ("ABILITY_TORRENT", "ABILITY_KEEN_EYE", "ABILITY_ANTICIPATION"),
    5: ("ABILITY_TORRENT", "ABILITY_COMPOUND_EYES", "ABILITY_SWARM"),
    6: ("ABILITY_TORRENT", "ABILITY_SWARM", "ABILITY_TINTED_LENS"),
    7: ("ABILITY_OVERGROW", "ABILITY_OWN_TEMPO", "ABILITY_SKILL_LINK"),
    8: ("ABILITY_OVERGROW", "ABILITY_DEFIANT", "ABILITY_KEEN_EYE"),
    9: ("ABILITY_OVERGROW", "ABILITY_ROCK_HEAD", "ABILITY_STURDY"),
}

TYPE_EGG_GROUP = {
    "normal": "EGG_GROUP_FIELD", "fire": "EGG_GROUP_FIELD",
    "water": "EGG_GROUP_WATER_1", "grass": "EGG_GROUP_GRASS",
    "electric": "EGG_GROUP_FIELD", "ice": "EGG_GROUP_FIELD",
    "fighting": "EGG_GROUP_HUMAN_LIKE", "poison": "EGG_GROUP_AMORPHOUS",
    "ground": "EGG_GROUP_FIELD", "flying": "EGG_GROUP_FLYING",
    "psychic": "EGG_GROUP_AMORPHOUS", "bug": "EGG_GROUP_BUG",
    "rock": "EGG_GROUP_MINERAL", "ghost": "EGG_GROUP_AMORPHOUS",
    "dragon": "EGG_GROUP_DRAGON", "dark": "EGG_GROUP_FIELD",
    "steel": "EGG_GROUP_MINERAL", "fairy": "EGG_GROUP_FAIRY",
}

TYPE_TEACHABLES = {
    "normal": ("BODY_SLAM", "DOUBLE_EDGE", "SWIFT", "HYPER_VOICE", "WORK_UP", "TRI_ATTACK"),
    "fire": ("FLAMETHROWER", "FIRE_BLAST", "SUNNY_DAY", "WILL_O_WISP", "OVERHEAT", "FIRE_PUNCH"),
    "water": ("WATER_PULSE", "SCALD", "ICE_BEAM", "RAIN_DANCE", "SURF", "LIQUIDATION"),
    "grass": ("MAGICAL_LEAF", "ENERGY_BALL", "SOLAR_BEAM", "SUNNY_DAY", "GIGA_DRAIN", "GRASS_KNOT"),
    "electric": ("SHOCK_WAVE", "THUNDERBOLT", "THUNDER", "THUNDER_WAVE", "VOLT_SWITCH", "CHARGE_BEAM"),
    "ice": ("ICY_WIND", "ICE_BEAM", "BLIZZARD", "HAIL", "ICE_PUNCH", "AVALANCHE"),
    "fighting": ("BRICK_BREAK", "DRAIN_PUNCH", "FOCUS_BLAST", "BULK_UP", "LOW_SWEEP", "AURA_SPHERE"),
    "poison": ("VENOSHOCK", "SLUDGE_BOMB", "SLUDGE_WAVE", "TOXIC", "POISON_JAB", "GUNK_SHOT"),
    "ground": ("MUD_SLAP", "DIG", "BULLDOZE", "EARTHQUAKE", "EARTH_POWER", "SANDSTORM"),
    "flying": ("AERIAL_ACE", "AIR_SLASH", "FLY", "ROOST", "TAILWIND", "HURRICANE"),
    "psychic": ("PSYBEAM", "PSYCHIC", "CALM_MIND", "ZEN_HEADBUTT", "LIGHT_SCREEN", "REFLECT"),
    "bug": ("STRUGGLE_BUG", "X_SCISSOR", "BUG_BUZZ", "UTURN", "POLLEN_PUFF", "LEECH_LIFE"),
    "rock": ("ROCK_TOMB", "ROCK_SLIDE", "STONE_EDGE", "POWER_GEM", "SANDSTORM", "STEALTH_ROCK"),
    "ghost": ("SHADOW_CLAW", "SHADOW_BALL", "HEX", "WILL_O_WISP", "POLTERGEIST", "CONFUSE_RAY"),
    "dragon": ("DRAGON_CLAW", "DRAGON_PULSE", "DRACO_METEOR", "DRAGON_DANCE", "OUTRAGE", "BREAKING_SWIPE"),
    "dark": ("THIEF", "SNARL", "DARK_PULSE", "FOUL_PLAY", "TAUNT", "NASTY_PLOT"),
    "steel": ("METAL_CLAW", "IRON_HEAD", "FLASH_CANNON", "IRON_DEFENSE", "STEEL_BEAM", "GYRO_BALL"),
    "fairy": ("DISARMING_VOICE", "DAZZLING_GLEAM", "MOONBLAST", "CHARM", "MISTY_TERRAIN", "PLAY_ROUGH"),
}

COMMON_TEACHABLES = (
    "PROTECT", "REST", "SLEEP_TALK", "SUBSTITUTE", "FACADE", "ENDURE",
    "SWIFT", "TAKE_DOWN", "HELPING_HAND", "TERA_BLAST", "TOXIC",
)


def constants(path: Path, prefix: str) -> set[str]:
    return set(re.findall(rf"\b{prefix}_[A-Z0-9_]+\b", path.read_text(encoding="utf-8")))


def species_slots(text: str) -> list[str]:
    slots = re.findall(r"^\s*\[SPECIES_([A-Z0-9_]+)\]\s*=", text, flags=re.MULTILINE)
    if len(slots) != DEX_SIZE or len(set(slots)) != DEX_SIZE:
        raise ValueError("species table must contain 386 unique engine slots")
    return slots


def protected_ids(entries: list[dict], story: dict) -> set[int]:
    result = {
        int(entry["id"]) for entry in entries
        if entry.get("legendary") or entry.get("mythical")
    }
    result.update(int(entry["id"]) for entry in story.get("nonCapturable", []))
    return result


def evolution_stages(entries: list[dict]) -> dict[int, int]:
    parent = {}
    for entry in entries:
        for evolution in entry.get("evolvesTo") or []:
            parent[int(evolution["id"])] = int(entry["id"])

    result = {}
    for entry in entries:
        number = int(entry["id"])
        stage = 0
        seen = set()
        cursor = number
        while cursor in parent and cursor not in seen:
            seen.add(cursor)
            cursor = parent[cursor]
            stage += 1
        result[number] = stage
    return result


def abilities_for(entry: dict) -> tuple[str, str, str]:
    number = int(entry["id"])
    if number in STARTER_ABILITIES:
        return STARTER_ABILITIES[number]
    types = entry.get("types") or ["normal"]
    first = TYPE_ABILITIES[types[0]][0]
    second = TYPE_ABILITIES[types[1]][1] if len(types) > 1 else TYPE_ABILITIES[types[0]][1]
    top_stat = max(("hp", "atk", "def", "spa", "spd", "spe"), key=lambda key: int(entry["stats"][key]))
    hidden = STAT_ABILITIES[top_stat]
    if hidden in (first, second):
        hidden = next(value for value in ABILITY_FALLBACKS if value not in (first, second))
    return first, second, hidden


def water_egg_group(entry: dict) -> str:
    words = f"{entry.get('name', '')} {entry.get('inspiration', '')}".lower()
    if any(word in words for word in ("carangue", "camarão", "camarao", "lagosta", "crustáce", "crustace")):
        return "EGG_GROUP_WATER_3"
    if any(word in words for word in ("peixe", "tubar", "arraia", "cavalo-marinho", "pirarucu", "piranha")):
        return "EGG_GROUP_WATER_2"
    return "EGG_GROUP_WATER_1"


def egg_groups_for(entry: dict, protected: bool) -> tuple[str, str]:
    if protected:
        value = "EGG_GROUP_NO_EGGS_DISCOVERED"
        return value, value
    groups = []
    for type_name in entry.get("types") or ["normal"]:
        group = water_egg_group(entry) if type_name == "water" else TYPE_EGG_GROUP[type_name]
        if group not in groups:
            groups.append(group)
    if len(groups) == 1:
        groups.append(groups[0])
    return groups[0], groups[1]


def profile_for(entry: dict, species: str, protected: bool, noncapturable: bool, stage: int) -> dict[str, str]:
    stats = entry["stats"]
    bst = sum(int(stats[key]) for key in ("hp", "atk", "def", "spa", "spd", "spe"))
    ability1, ability2, hidden = abilities_for(entry)
    group1, group2 = egg_groups_for(entry, protected)
    legendary = bool(entry.get("legendary") or entry.get("mythical"))
    growth = "GROWTH_MEDIUM_SLOW" if int(entry["id"]) <= 9 else "GROWTH_SLOW" if legendary or bst >= 560 else "GROWTH_MEDIUM_FAST"
    if noncapturable:
        catch_rate = 0
    elif legendary:
        catch_rate = 3
    elif int(entry["id"]) <= 9:
        catch_rate = 45
    elif stage > 0:
        catch_rate = 45 if bst >= 500 or stage >= 2 else 90
    else:
        catch_rate = 45 if bst >= 560 else 90 if bst >= 490 else 180
    return {
        "id": f"{int(entry['id']):03d}",
        "name": entry["name"],
        "engine_species": f"SPECIES_{species}",
        "types": "/".join(entry.get("types") or ["normal"]),
        "ability1": ability1,
        "ability2": ability2,
        "hidden_ability": hidden,
        "egg_group1": group1,
        "egg_group2": group2,
        "gender_ratio": "MON_GENDERLESS" if protected else "PERCENT_FEMALE(50)",
        "egg_cycles": "120" if legendary else "20" if int(entry["id"]) <= 9 else "40" if protected or bst >= 560 else "20",
        "growth_rate": growth,
        "catch_rate": str(catch_rate),
        "exp_yield": str(min(255, max(40, round(bst / 3)))),
        "source_abilities": " / ".join(entry.get("abilities") or []),
    }


def teachables_for(entry: dict, known_moves: set[str]) -> list[str]:
    types = entry.get("types") or ["normal"]
    names = list(COMMON_TEACHABLES)
    for type_name in types:
        names.extend(TYPE_TEACHABLES[type_name])
    physical = int(entry["stats"]["atk"]) >= int(entry["stats"]["spa"])
    names.extend(("SWORDS_DANCE", "BULK_UP") if physical else ("CALM_MIND", "NASTY_PLOT"))
    if "water" in types:
        names.extend(("SURF", "WATERFALL", "DIVE", "WHIRLPOOL"))
    if "flying" in types:
        names.append("FLY")
    if set(types) & {"grass", "bug", "steel"}:
        names.append("CUT")
    if set(types) & {"rock", "ground", "fighting", "steel"}:
        names.extend(("ROCK_SMASH", "STRENGTH"))
    result = []
    for name in names:
        move = f"MOVE_{name}"
        if move in known_moves and move not in result:
            result.append(move)
    if len(result) < 15:
        raise ValueError(f"#{int(entry['id']):03d} has only {len(result)} known teachable moves")
    return result


def replace_once(block: str, pattern: str, replacement: str, label: str) -> str:
    result, count = re.subn(pattern, replacement, block, count=1, flags=re.MULTILINE)
    if count != 1:
        raise ValueError(f"could not replace {label} in species block")
    return result


def apply_profiles(text: str, profiles: list[dict[str, str]]) -> str:
    starts = list(re.finditer(r"^\s*\[SPECIES_[A-Z0-9_]+\]\s*=", text, flags=re.MULTILINE))
    chunks = [text[:starts[0].start()]]
    for index, (match, profile) in enumerate(zip(starts, profiles)):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        block = text[match.start():end]
        block = replace_once(block, r"^\s*\.catchRate\s*=.*$", f"        .catchRate = {profile['catch_rate']},", "catch rate")
        block = replace_once(block, r"^\s*\.expYield\s*=.*$", f"        .expYield = {profile['exp_yield']},", "exp yield")
        block = replace_once(block, r"^\s*\.genderRatio\s*=.*$", f"        .genderRatio = {profile['gender_ratio']},", "gender ratio")
        block = replace_once(block, r"^\s*\.eggCycles\s*=.*$", f"        .eggCycles = {profile['egg_cycles']},", "egg cycles")
        block = replace_once(block, r"^\s*\.growthRate\s*=.*$", f"        .growthRate = {profile['growth_rate']},", "growth rate")
        groups = profile["egg_group1"] if profile["egg_group1"] == profile["egg_group2"] else f"{profile['egg_group1']}, {profile['egg_group2']}"
        block = replace_once(block, r"^\s*\.eggGroups\s*=.*$", f"        .eggGroups = MON_EGG_GROUPS({groups}),", "egg groups")
        abilities = f"{{ {profile['ability1']}, {profile['ability2']}, {profile['hidden_ability']} }}"
        block = replace_once(block, r"^\s*\.abilities\s*=.*$", f"        .abilities = {abilities},", "abilities")
        block = replace_once(
            block,
            r"^\s*\.levelUpLearnset\s*=.*$",
            f"        .levelUpLearnset = sArauna{profile['id']}LevelUpLearnset,",
            "level-up learnset",
        )
        block = replace_once(
            block,
            r"^\s*\.eggMoveLearnset\s*=.*$",
            "        .eggMoveLearnset = sNoneEggMoveLearnset,",
            "egg-move learnset",
        )
        chunks.append(block)
    return "".join(chunks)


def csv_text(rows: list[dict[str, str]]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dex", type=Path, default=ROOT / "docs/arauna/source/pokedex.json")
    parser.add_argument("--story-roles", type=Path, default=ROOT / "docs/arauna/source/story_roles.json")
    parser.add_argument("--species-table", type=Path, default=ROOT / "src/data/pokemon/species_info/arauna_dex.h")
    parser.add_argument("--moves", type=Path, default=ROOT / "include/constants/moves.h")
    parser.add_argument("--abilities", type=Path, default=ROOT / "include/constants/abilities.h")
    parser.add_argument("--profiles-out", type=Path, default=ROOT / "docs/arauna/ARAUNA_BATTLE_PROFILES.csv")
    parser.add_argument("--teachables-out", type=Path, default=ROOT / "src/data/pokemon/arauna_teachables.json")
    parser.add_argument("--no-apply", action="store_true", help="Do not update the committed species table")
    args = parser.parse_args()

    entries = json.loads(args.dex.read_text(encoding="utf-8"))["pokemon"]
    if len(entries) != DEX_SIZE or {int(entry["id"]) for entry in entries} != set(range(1, DEX_SIZE + 1)):
        raise ValueError("Arauna source must contain IDs 001-386 exactly")
    story = json.loads(args.story_roles.read_text(encoding="utf-8"))
    species_text = args.species_table.read_text(encoding="utf-8")
    slots = species_slots(species_text)
    protected = protected_ids(entries, story)
    noncapturable = {int(entry["id"]) for entry in story.get("nonCapturable", [])}
    stages = evolution_stages(entries)
    profiles = [
        profile_for(
            entry,
            slot,
            int(entry["id"]) in protected,
            int(entry["id"]) in noncapturable,
            stages[int(entry["id"])],
        )
        for entry, slot in zip(entries, slots)
    ]

    known_abilities = constants(args.abilities, "ABILITY")
    used_abilities = {row[key] for row in profiles for key in ("ability1", "ability2", "hidden_ability")}
    unknown_abilities = used_abilities - known_abilities
    if unknown_abilities:
        raise ValueError(f"unknown ability constants: {', '.join(sorted(unknown_abilities))}")

    known_moves = constants(args.moves, "MOVE")
    teachables = {
        slot: teachables_for(entry, known_moves)
        for entry, slot in zip(entries, slots)
    }
    args.profiles_out.parent.mkdir(parents=True, exist_ok=True)
    args.profiles_out.write_text(csv_text(profiles), encoding="utf-8")
    args.teachables_out.parent.mkdir(parents=True, exist_ok=True)
    args.teachables_out.write_text(json.dumps(teachables, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not args.no_apply:
        args.species_table.write_text(apply_profiles(species_text, profiles), encoding="utf-8")
    print(f"generated 386 battle profiles and 386 teachable overlays ({len(protected)} protected slots)")


if __name__ == "__main__":
    main()
