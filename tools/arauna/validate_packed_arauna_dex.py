#!/usr/bin/env python3
"""Validate the committed 386-species Arauna replacement before a ROM build.

This check intentionally uses only Python's standard library.  It verifies the
compact engine tables and packed graphic declarations that are consumed by the
English-first build; it does not inspect story or character scripts.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEX_SIZE = 386
EXPECTED_IDS = set(range(1, DEX_SIZE + 1))
EXPECTED_SYMBOL_IDS = {f"{number:03d}" for number in EXPECTED_IDS}
EXPECTED_METHODS = {
    "hand-prepared-approved": 9,
    "reference-front-plus-reconstructed-back": 305,
    "procedural-concept-front-and-back": 72,
}
STARTERS = {
    1: ("Caramelo", "fire"),
    2: ("Caramelão", "fire"),
    3: ("Draguará", "fire/dragon"),
    4: ("Querô", "water"),
    5: ("Queribela", "water/bug"),
    6: ("Terolibra", "water/bug"),
    7: ("Pimpau", "grass"),
    8: ("Bicopau", "grass"),
    9: ("Petropico", "grass/rock"),
}
ADDITIONAL_STORY_RESERVED_IDS = {256}


class ValidationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def read_text(relative: str) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing required file: {relative}")
    text = path.read_text(encoding="utf-8")
    require(
        not text.startswith("version https://git-lfs.github.com/spec/v1"),
        f"{relative} is still a Git LFS pointer; run 'git lfs pull'",
    )
    return text


def read_json(relative: str) -> dict:
    return json.loads(read_text(relative))


def read_csv(relative: str) -> list[dict[str, str]]:
    return list(csv.DictReader(read_text(relative).splitlines()))


def numeric_ids(rows: list[dict[str, str]], field: str, label: str) -> set[int]:
    require(len(rows) == DEX_SIZE, f"{label}: expected 386 rows, found {len(rows)}")
    try:
        ids = {int(row[field]) for row in rows}
    except (KeyError, ValueError) as exc:
        raise ValidationError(f"{label}: invalid {field} column") from exc
    require(ids == EXPECTED_IDS, f"{label}: IDs must cover 001-386 exactly")
    return ids


def validate_sources() -> None:
    source = read_json("docs/arauna/source/pokedex.json")
    english = read_json("docs/arauna/source/pokedex.en.json")

    require(source.get("total") == DEX_SIZE, "Portuguese source total is not 386")
    require(english.get("language") == "en", "English Dex language must be 'en'")
    require(english.get("region") == "Arauna", "English region name must be Arauna")
    require(english.get("total") == DEX_SIZE, "English source total is not 386")

    source_rows = source.get("pokemon", [])
    english_rows = english.get("pokemon", [])
    numeric_ids(source_rows, "id", "Portuguese Dex source")
    numeric_ids(english_rows, "id", "English Dex source")

    english_by_id = {int(row["id"]): row for row in english_rows}
    for number, row in english_by_id.items():
        for field in ("category", "region", "dex"):
            require(str(row.get(field, "")).strip(), f"English Dex #{number:03d} lacks {field}")


def validate_mapping_and_manifest() -> None:
    mapping = read_csv("docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv")
    manifest = read_csv("docs/arauna/FULL_DEX_ART_MANIFEST.csv")
    numeric_ids(mapping, "arauna_dex", "engine mapping")
    numeric_ids(manifest, "dex", "art manifest")

    require(len({row["species_constant"] for row in mapping}) == DEX_SIZE,
            "engine mapping contains duplicate species constants")
    require(len({row["national_slot"] for row in mapping}) == DEX_SIZE,
            "engine mapping contains duplicate National Dex slots")
    require(all(1 <= len(row["engine_name"]) <= 12 for row in mapping),
            "engine names must contain 1-12 characters")

    mapping_by_id = {int(row["arauna_dex"]): row for row in mapping}
    manifest_by_id = {int(row["dex"]): row for row in manifest}
    for number in EXPECTED_IDS:
        mapped = mapping_by_id[number]
        art = manifest_by_id[number]
        for field in ("name", "types", "status", "productionMethod", "referenceStatus",
                      "frontPicBox", "backPicBox", "iconPalIndex", "visibleColors",
                      "animation", "shiny"):
            require(art.get(field, "").strip(), f"art manifest #{number:03d} lacks {field}")
        require(art["status"] == "integrated", f"art manifest #{number:03d} is not integrated")
        require(art["productionMethod"] == mapped["production_method"],
                f"production method mismatch at #{number:03d}")
        require(art["types"] == mapped["types"], f"type mismatch at #{number:03d}")
        require(0 <= int(art["iconPalIndex"]) <= 5,
                f"invalid icon palette at #{number:03d}")
        require(1 <= int(art["visibleColors"]) <= 15,
                f"invalid visible-color count at #{number:03d}")

    methods = Counter(row["productionMethod"] for row in manifest)
    require(dict(methods) == EXPECTED_METHODS,
            f"unexpected art production counts: {dict(methods)}")

    for number, (name, types) in STARTERS.items():
        mapped = mapping_by_id[number]
        art = manifest_by_id[number]
        require(mapped["full_name"] == name and art["name"] == name,
                f"starter name mismatch at #{number:03d}")
        require(mapped["types"] == types and art["types"] == types,
                f"starter type mismatch at #{number:03d}")


def matches(text: str, pattern: str) -> list[str]:
    return re.findall(pattern, text, flags=re.MULTILINE)


def validate_species_table() -> None:
    text = read_text("src/data/pokemon/species_info/arauna_dex.h")
    blocks = matches(text, r"^\s*\[SPECIES_[A-Z0-9_]+\]\s*=")
    require(len(blocks) == DEX_SIZE, f"species table has {len(blocks)} entries, expected 386")
    require(text.count(".natDexNum") == DEX_SIZE, "species table must contain 386 National Dex slots")
    require(text.count(".speciesName") == DEX_SIZE, "species table must contain 386 names")
    require(text.count(".categoryName") == DEX_SIZE, "species table must contain 386 categories")
    require(text.count(".description") == DEX_SIZE, "species table must contain 386 descriptions")
    require(text.count(".evolutions = EVOLUTION") == 81, "species table must contain 81 evolution links")
    require(text.count("{") == text.count("}"), "species table braces are unbalanced")
    require(not re.search(r"[\u2013\u2014]", text), "species table contains an unsupported dash character")

    references = {
        "front": r"\.frontPic\s*=\s*gAraunaFrontPic_(\d{3})",
        "back": r"\.backPic\s*=\s*gAraunaBackPic_(\d{3})",
        "palette": r"\.palette\s*=\s*gAraunaPalette_(\d{3})",
        "shiny palette": r"\.shinyPalette\s*=\s*gAraunaShinyPalette_(\d{3})",
        "icon": r"\.iconSprite\s*=\s*gAraunaIcon_(\d{3})",
    }
    for label, pattern in references.items():
        ids = set(matches(text, pattern))
        require(ids == EXPECTED_SYMBOL_IDS, f"species table {label} references do not cover 001-386")


def validate_packed_graphics() -> None:
    text = read_text("src/data/graphics/arauna_fakemon_graphics.h")
    declarations = {
        "front": r"^const\s+u32\s+gAraunaFrontPic_(\d{3})\[\]",
        "back": r"^const\s+u32\s+gAraunaBackPic_(\d{3})\[\]",
        "palette": r"^const\s+u16\s+gAraunaPalette_(\d{3})\[\]",
        "shiny palette": r"^const\s+u16\s+gAraunaShinyPalette_(\d{3})\[\]",
        "icon": r"^const\s+u8\s+gAraunaIcon_(\d{3})\[\]",
    }
    for label, pattern in declarations.items():
        ids = set(matches(text, pattern))
        require(ids == EXPECTED_SYMBOL_IDS, f"packed {label} declarations do not cover 001-386")

    pokemon_graphics = read_text("src/data/graphics/pokemon.h")
    require('#include "arauna_fakemon_graphics.h"' in pokemon_graphics,
            "pokemon graphics table does not include Arauna packed graphics")
    species_info = read_text("src/data/pokemon/species_info.h")
    require('#include "species_info/arauna_dex.h"' in species_info,
            "species table does not include the Arauna replacement")
    require(not re.search(r'#include "species_info/gen_[123]_families\.h"', species_info),
            "original Gen 1-3 family tables are still enabled")


def validate_learnsets() -> None:
    text = read_text("src/data/pokemon/level_up_learnsets/arauna.h")
    declarations = set(matches(
        text,
        r"^static const struct LevelUpMove sArauna(\d{3})LevelUpLearnset\[\]",
    ))
    require(declarations == EXPECTED_SYMBOL_IDS,
            "Arauna level-up learnsets do not cover 001-386")
    require(text.count("LEVEL_UP_END") == DEX_SIZE,
            "each Arauna learnset must contain exactly one terminator")

    for number, block in re.findall(
        r"sArauna(\d{3})LevelUpLearnset\[\]\s*=\s*\{(.*?)\n\};",
        text,
        flags=re.DOTALL,
    ):
        require(block.count("LEVEL_UP_MOVE") >= 8,
                f"Arauna learnset #{number} has fewer than eight moves")

    forbidden_field_moves = {
        "MOVE_CUT", "MOVE_FLY", "MOVE_SURF", "MOVE_STRENGTH",
        "MOVE_ROCK_SMASH", "MOVE_WATERFALL", "MOVE_DIVE",
    }
    found = sorted(move for move in forbidden_field_moves if move in text)
    require(not found,
            f"level-up learnsets would bypass field progression: {', '.join(found)}")

    species = read_text("src/data/pokemon/species_info/arauna_dex.h")
    references = set(matches(
        species,
        r"\.levelUpLearnset\s*=\s*sArauna(\d{3})LevelUpLearnset",
    ))
    require(references == EXPECTED_SYMBOL_IDS,
            "species table is not wired to all 386 Arauna learnsets")

    pokemon = read_text("src/pokemon.c")
    require('#include "data/pokemon/level_up_learnsets/arauna.h"' in pokemon,
            "src/pokemon.c does not load the Arauna learnsets")


def normalize_species(value: str) -> str:
    value = value.upper().removeprefix("SPECIES_")
    return re.sub(r"[^A-Z0-9]", "", value)


def trainer_species(line: str) -> str | None:
    stripped = line.strip()
    if (not stripped or ":" in stripped or stripped.startswith(("===", "/*", "*", "//", "-"))
            or stripped.endswith("*/")):
        return None
    core = stripped.split(" @ ", 1)[0]
    parentheses = list(re.finditer(r"\(([^()]*)\)", core))
    species_paren = next((match for match in parentheses if match.group(1) not in {"M", "F"}), None)
    if species_paren:
        return species_paren.group(1)
    return re.sub(r"\s+\([MF]\)$", "", core).strip()


def validate_battle_profiles() -> None:
    source = read_json("docs/arauna/source/pokedex.json")
    story = read_json("docs/arauna/source/story_roles.json")
    profiles = read_csv("docs/arauna/ARAUNA_BATTLE_PROFILES.csv")
    numeric_ids(profiles, "id", "battle profiles")
    profiles_by_id = {int(row["id"]): row for row in profiles}
    source_by_id = {int(entry["id"]): entry for entry in source["pokemon"]}

    species_text = read_text("src/data/pokemon/species_info/arauna_dex.h")
    species_blocks = re.findall(
        r"^\s*\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\{(.*?)^\s*\},",
        species_text,
        flags=re.MULTILINE | re.DOTALL,
    )
    require(len(species_blocks) == DEX_SIZE, "battle profiles could not map all species blocks")
    species_by_id = {number: f"SPECIES_{species_blocks[number - 1][0]}" for number in EXPECTED_IDS}

    noncapturable = {int(entry["id"]) for entry in story.get("nonCapturable", [])}
    biologically_protected = set(noncapturable)
    biologically_protected.update(
        number for number, entry in source_by_id.items()
        if entry.get("legendary") or entry.get("mythical")
    )
    known_abilities = set(matches(read_text("include/constants/abilities.h"), r"\b(ABILITY_[A-Z0-9_]+)\b"))
    used_abilities = set()
    egg_groups = set()
    for number in EXPECTED_IDS:
        row = profiles_by_id[number]
        block = species_blocks[number - 1][1]
        require(row["engine_species"] == species_by_id[number],
                f"battle profile engine mapping mismatch at #{number:03d}")
        for field in ("ability1", "ability2", "hidden_ability"):
            ability = row[field]
            require(ability in known_abilities and ability != "ABILITY_NONE",
                    f"battle profile #{number:03d} has invalid {field}")
            used_abilities.add(ability)
        egg_groups.update((row["egg_group1"], row["egg_group2"]))

        groups = row["egg_group1"] if row["egg_group1"] == row["egg_group2"] else f"{row['egg_group1']}, {row['egg_group2']}"
        expected_lines = (
            f".catchRate = {row['catch_rate']},",
            f".expYield = {row['exp_yield']},",
            f".genderRatio = {row['gender_ratio']},",
            f".eggCycles = {row['egg_cycles']},",
            f".growthRate = {row['growth_rate']},",
            f".eggGroups = MON_EGG_GROUPS({groups}),",
            f".abilities = {{ {row['ability1']}, {row['ability2']}, {row['hidden_ability']} }},",
            f".levelUpLearnset = sArauna{number:03d}LevelUpLearnset,",
            ".eggMoveLearnset = sNoneEggMoveLearnset,",
        )
        for line in expected_lines:
            require(line in block, f"species table differs from battle profile #{number:03d}: {line}")

        if number in biologically_protected:
            require(row["gender_ratio"] == "MON_GENDERLESS",
                    f"protected species #{number:03d} must be genderless")
            require(row["egg_group1"] == row["egg_group2"] == "EGG_GROUP_NO_EGGS_DISCOVERED",
                    f"protected species #{number:03d} must not breed")
        else:
            require(row["gender_ratio"] != "MON_GENDERLESS",
                    f"ordinary species #{number:03d} is unexpectedly genderless")
            require("EGG_GROUP_NO_EGGS_DISCOVERED" not in (row["egg_group1"], row["egg_group2"]),
                    f"ordinary species #{number:03d} cannot breed")
        if number in noncapturable:
            require(row["catch_rate"] == "0", f"non-capturable species #{number:03d} has a catch rate")

    require(len(used_abilities) >= 35,
            f"battle profiles use too little ability variety: {len(used_abilities)}")
    require(len(egg_groups) >= 12,
            f"battle profiles use too little egg-group variety: {len(egg_groups)}")

    teachables = read_json("src/data/pokemon/arauna_teachables.json")
    expected_keys = {species.removeprefix("SPECIES_") for species in species_by_id.values()}
    require(set(teachables) == expected_keys,
            "Arauna teachable overlay must cover the 386 engine species exactly")
    known_moves = set(matches(read_text("include/constants/moves.h"), r"\b(MOVE_[A-Z0-9_]+)\b"))
    for number in EXPECTED_IDS:
        key = species_by_id[number].removeprefix("SPECIES_")
        moves = teachables[key]
        require(len(moves) >= 15 and len(moves) == len(set(moves)),
                f"teachable overlay #{number:03d} must contain at least 15 unique moves")
        require(set(moves) <= known_moves,
                f"teachable overlay #{number:03d} contains an unknown move")
        types = source_by_id[number].get("types") or ["normal"]
        if "water" in types:
            require("MOVE_SURF" in moves, f"water species #{number:03d} cannot learn Surf")
        if "flying" in types:
            require("MOVE_FLY" in moves, f"flying species #{number:03d} cannot learn Fly")

    makefile = read_text("Makefile")
    helper = read_text("tools/learnset_helpers/make_teachables.py")
    require("ARAUNA_TEACHABLES_JSON" in makefile and "$(ARAUNA_TEACHABLES_JSON)" in makefile,
            "Makefile does not track the Arauna teachable overlay")
    require("all_learnables.update(json.load(source_fp))" in helper,
            "teachable generator does not apply the Arauna overlay")
    require("--battle-profiles" in read_text("tools/arauna/integrate_full_arauna_dex.py"),
            "full-Dex integrator does not consume battle profiles")

    trainer_protected = set(ADDITIONAL_STORY_RESERVED_IDS) | biologically_protected
    trainer_protected.update(int(number) for number in story.get("fadedStorySpecies", []))
    trainer_protected.update(int(number) for number in story.get("sensitivityReviewRequired", []))
    by_normalized_species = {
        normalize_species(species): number for number, species in species_by_id.items()
    }
    trainer_text = read_text("src/data/trainers.party")
    found = set()
    party_members = 0
    for line in trainer_text.splitlines():
        token = trainer_species(line)
        if token is None:
            continue
        number = by_normalized_species.get(normalize_species(token))
        if number is not None:
            party_members += 1
            if number in trainer_protected:
                found.add(number)
    require(not found,
            "ordinary trainer data uses protected Arauna slots: "
            + ", ".join(f"#{number:03d}" for number in sorted(found)))
    require(party_members >= 1800, f"trainer audit parsed only {party_members} party members")
    levels = [int(value) for value in matches(trainer_text, r"^Level:\s*(\d+)\s*$")]
    require(levels and min(levels) >= 1 and max(levels) <= 100,
            "trainer levels must remain within 1-100")


def validate_encounter_ecology() -> None:
    source = read_json("docs/arauna/source/pokedex.json")
    story = read_json("docs/arauna/source/story_roles.json")
    ecology = read_csv("docs/arauna/ARAUNA_ENCOUNTER_ECOLOGY.csv")
    numeric_ids(ecology, "id", "encounter ecology")

    source_by_id = {int(entry["id"]): entry for entry in source["pokemon"]}
    species_text = read_text("src/data/pokemon/species_info/arauna_dex.h")
    species_blocks = re.findall(
        r"^\s*\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\{(.*?)^\s*\},",
        species_text,
        flags=re.MULTILINE | re.DOTALL,
    )
    require(len(species_blocks) == DEX_SIZE,
            "could not map all 386 Arauna IDs to engine species")
    constant_by_id = {
        number: f"SPECIES_{species_blocks[number - 1][0]}"
        for number in EXPECTED_IDS
    }

    noncapturable_ids = {
        int(entry["id"]) for entry in story.get("nonCapturable", [])
    }
    story_ids = set(ADDITIONAL_STORY_RESERVED_IDS)
    story_ids.update(noncapturable_ids)
    story_ids.update(int(value) for value in story.get("fadedStorySpecies", []))
    story_ids.update(int(value) for value in story.get("sensitivityReviewRequired", []))
    legendary_ids = {
        number for number, entry in source_by_id.items()
        if entry.get("legendary") or entry.get("mythical")
    }
    starter_ids = set(range(1, 10))
    wild_ids = EXPECTED_IDS - story_ids - legendary_ids - starter_ids
    for number in noncapturable_ids:
        require(re.search(r"\.catchRate\s*=\s*0,", species_blocks[number - 1][1]) is not None,
                f"non-capturable story species #{number:03d} has a nonzero catch rate")

    ecology_by_id = {int(row["id"]): row for row in ecology}
    for number in EXPECTED_IDS:
        row = ecology_by_id[number]
        source_entry = source_by_id[number]
        expected = (
            "starter" if number in starter_ids else
            "mythical" if source_entry.get("mythical") else
            "legendary" if source_entry.get("legendary") else
            "story" if number in story_ids else
            "wild"
        )
        require(row["species"] == constant_by_id[number],
                f"ecology species mapping mismatch at #{number:03d}")
        require(row["availability"] == expected,
                f"ecology availability mismatch at #{number:03d}")
        for field in ("types", "source_region", "biome", "tier", "stage", "methods"):
            require(row[field].strip(), f"ecology #{number:03d} lacks {field}")

    encounters = read_json("src/data/wild_encounters.json")
    used = set()
    early_violations = []
    evolution_violations = []
    bst_by_species = {row["species"]: int(row["bst"]) for row in ecology}
    evo_by_species = {row["species"]: int(row["evolution_level"]) for row in ecology}
    for group in encounters["wild_encounter_groups"]:
        for encounter in group.get("encounters", []):
            map_name = encounter.get("map", group["label"])
            for field, table in encounter.items():
                if not field.endswith("_mons") or not isinstance(table, dict):
                    continue
                for mon in table["mons"]:
                    species = mon["species"]
                    max_level = int(mon["max_level"])
                    used.add(species)
                    if max_level <= 5 and bst_by_species[species] > 400:
                        early_violations.append(f"{map_name}:{species}")
                    if evo_by_species[species] and max_level + 1 < evo_by_species[species]:
                        evolution_violations.append(f"{map_name}:{species}")

    expected_wild = {constant_by_id[number] for number in wild_ids}
    require(used == expected_wild,
            "wild tables must cover every ordinary species and no protected species")
    require(not early_violations,
            f"early encounters exceed the BST cap: {', '.join(early_violations[:5])}")
    require(not evolution_violations,
            f"evolved species appear too early: {', '.join(evolution_violations[:5])}")

    protected = {
        constant_by_id[number]
        for number in story_ids | legendary_ids
    }
    trainers = read_text("src/data/trainers.party")
    found = sorted(species for species in protected if re.search(rf"\b{species}\b", trainers))
    require(not found,
            f"ordinary trainer data still uses protected species: {', '.join(found)}")


def validate_runtime_integration() -> None:
    constants = read_text("include/constants/pokedex.h")
    regional_match = re.search(
        r"#define FOREACH_SPECIES_IN_HOENN_DEX_ORDER\(F\) \\\n"
        r"(?P<body>.*?)(?=\n\n// Arauna regional Pokédex order)",
        constants,
        flags=re.DOTALL,
    )
    require(regional_match is not None, "Arauna regional Dex macro is missing")
    regional = re.findall(r"F\(([A-Z0-9_]+)\)", regional_match.group("body"))

    national_match = re.search(
        r"enum NationalDexOrder\s*\{(?P<body>.*?)\n\};",
        constants,
        flags=re.DOTALL,
    )
    require(national_match is not None, "National Dex enum is missing")
    national = re.findall(r"NATIONAL_DEX_([A-Z0-9_]+),", national_match.group("body"))
    national = [name for name in national if name != "NONE"][:DEX_SIZE]
    require(len(regional) == DEX_SIZE, f"Arauna regional Dex has {len(regional)} slots")
    require(regional == national,
            "Arauna regional Dex must map slots 001-386 in National order")

    research_center = read_text("data/maps/AraunaResearchCenter/scripts.inc")
    require("EnableNationalPokedex" not in research_center,
            "research center still enables the unstable National Dex mode")
    require("special SetUnlockedPokedexFlags" in research_center,
            "research center no longer unlocks the Arauna Dex")

    strings = read_text("src/strings.c")
    require('gText_DexHoennTitle[] = _("ARAUNA DEX")' in strings,
            "regional Dex title is not ARAUNA DEX")
    require('gText_DexHoennDescription[] = _("ARAUNA region\'s POKéDEX")' in strings,
            "regional Dex description is not branded for Arauna")

    battle_controllers = read_text("src/battle_controllers.c")
    field_specials = read_text("src/field_specials.c")
    require("CreateWildMon(SPECIES_ZIGZAGOON, 2);" not in battle_controllers,
            "battle tutorial still presents Pomba-Gira as a common wild species")
    require("CreateWildMon(SPECIES_BULBASAUR, 2);" in battle_controllers,
            "battle tutorial does not use the approved common placeholder")
    require("SPECIES_ZIGZAGOON, 7" not in field_specials,
            "catching tutorial still uses Pomba-Gira")
    require("SPECIES_BULBASAUR, 7" in field_specials,
            "catching tutorial does not use the approved common placeholder")


def main() -> int:
    try:
        validate_sources()
        validate_mapping_and_manifest()
        validate_species_table()
        validate_packed_graphics()
        validate_learnsets()
        validate_battle_profiles()
        validate_encounter_ecology()
        validate_runtime_integration()
    except (OSError, UnicodeError, json.JSONDecodeError, csv.Error, ValidationError, ValueError) as exc:
        print(f"Arauna packed Dex validation failed: {exc}", file=sys.stderr)
        return 1

    print("Arauna packed Dex validation passed: 386 battle profiles, 386 learnsets, 386 TM overlays, 321 wild species, 81 evolutions, 1,930 graphic resources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
