#!/usr/bin/env python3
"""Build deterministic wild encounters from Arauna biomes and progression."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEX_SIZE = 386
FIELD_METHOD = {
    "land_mons": "land",
    "water_mons": "water",
    "fishing_mons": "fishing",
    "rock_smash_mons": "rock_smash",
}
REGION_BIOME = {
    "Periferia de Arauana": "urban",
    "Serra de Arauana": "highlands",
    "Pampas de Arauana": "pampas",
    "Banhados de Arauana": "wetlands",
    "Cerrado de Arauana": "cerrado",
    "Chapadas de Arauana": "chapadas",
    "Rios de Arauana": "rivers",
    "Mata Atlântica de Arauana": "atlantic_forest",
    "Campos queimados de Arauana": "cerrado",
    "Rio Solimões de Arauana": "amazon_rivers",
    "Caatinga de Arauana": "caatinga",
    "Amazônia de Arauana": "amazon",
    "Pantanal de Arauana": "pantanal",
    "Rio Amazonas de Arauana": "amazon_rivers",
    "Cavernas de Arauana": "caves",
    "Litoral de Arauana": "coast",
    "Cidades de Arauana": "urban",
    "Sertão de Arauana": "caatinga",
}
AQUATIC_WORDS = re.compile(
    r"peixe|piranha|tubar|arraia|enguia|boto|golfin|baleia|orca|"
    r"cavalo-marinho|polvo|lula|água-viva|marinho|bagre|mandi|"
    r"traíra|dourado|lambari|pirarucu|sardinha|atum|camarão",
    re.IGNORECASE,
)
ADDITIONAL_STORY_RESERVED = {256}


def stable_index(key: str, size: int) -> int:
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % size


def evolution_level(method: str) -> int:
    match = re.search(r"(\d+)", method)
    if not match:
        raise ValueError(f"unsupported evolution method: {method}")
    return int(match.group(1))


def map_biomes(map_name: str) -> tuple[str, ...]:
    route = re.fullmatch(r"MAP_ROUTE(\d+)", map_name)
    if route:
        number = int(route.group(1))
        if 101 <= number <= 104:
            return ("atlantic_forest",)
        if 105 <= number <= 109:
            return ("coast",)
        if number == 110:
            return ("urban", "coast")
        if 111 <= number <= 113:
            return ("caatinga", "chapadas")
        if 114 <= number <= 116:
            return ("highlands", "caves")
        if number == 117:
            return ("cerrado", "pampas")
        if number == 118:
            return ("rivers", "cerrado")
        if 119 <= number <= 120:
            return ("amazon", "amazon_rivers")
        if number == 121:
            return ("atlantic_forest", "coast")
        if number == 122:
            return ("highlands", "caves")
        if number == 123:
            return ("cerrado", "atlantic_forest")
        if 124 <= number <= 134:
            return ("coast",)
        cycle = ("atlantic_forest", "cerrado", "caatinga", "rivers", "pampas")
        return (cycle[(number - 1) % len(cycle)],)

    if "ARAUNA_MIST_ROUTE" in map_name:
        return ("atlantic_forest", "wetlands")
    if "SAFARI_ZONE_SOUTHWEST" in map_name:
        return ("pampas",)
    if "SAFARI_ZONE_SOUTH" in map_name:
        return ("pantanal",)
    if "SAFARI_ZONE_NORTHWEST" in map_name:
        return ("amazon",)
    if "SAFARI_ZONE_NORTH" in map_name:
        return ("cerrado",)
    if "SAFARI_ZONE_SOUTHEAST" in map_name:
        return ("atlantic_forest",)
    if "SAFARI_ZONE_NORTHEAST" in map_name:
        return ("coast",)
    if any(word in map_name for word in ("UNDERWATER", "SEAFLOOR", "SHIP", "SHOAL", "SEAFOAM")):
        return ("coast", "caves")
    if any(word in map_name for word in ("FIERY", "MAGMA", "EMBER", "JAGGED", "DESERT", "MIRAGE")):
        return ("caatinga", "chapadas")
    if any(word in map_name for word in ("WOODS", "FOREST", "BERRY", "BUSH", "GREEN_PATH")):
        return ("atlantic_forest", "amazon")
    if any(word in map_name for word in ("CAVE", "TUNNEL", "VICTORY_ROAD", "MT_MOON", "RUINS")):
        return ("caves", "highlands")
    if any(word in map_name for word in ("MT_PYRE", "POKEMON_TOWER", "LOST_CAVE")):
        return ("highlands", "caves")
    if any(word in map_name for word in ("CITY", "TOWN", "MANSION", "NEW_MAUVILLE", "POWER_PLANT")):
        return ("urban", "coast")
    if "SKY_PILLAR" in map_name:
        return ("highlands", "chapadas")
    return ("cerrado", "atlantic_forest")


def preferred_types(map_name: str) -> set[str]:
    if any(word in map_name for word in ("MT_PYRE", "POKEMON_TOWER", "LOST_CAVE")):
        return {"ghost", "dark", "psychic"}
    if any(word in map_name for word in ("NEW_MAUVILLE", "POWER_PLANT")):
        return {"electric", "steel"}
    if any(word in map_name for word in ("FIERY", "MAGMA", "EMBER", "JAGGED")):
        return {"fire", "ground", "rock"}
    return set()


def story_reserved_ids(source: dict, story: dict) -> tuple[set[int], set[int]]:
    legendary = {
        int(entry["id"])
        for entry in source["pokemon"]
        if entry.get("legendary") or entry.get("mythical")
    }
    story_ids = set(ADDITIONAL_STORY_RESERVED)
    story_ids.update(int(entry["id"]) for entry in story.get("nonCapturable", []))
    story_ids.update(int(value) for value in story.get("fadedStorySpecies", []))
    story_ids.update(int(value) for value in story.get("sensitivityReviewRequired", []))
    return story_ids, legendary


def build_profiles(source: dict, species_constants: list[str], story: dict) -> list[dict]:
    entries = source["pokemon"]
    if len(entries) != DEX_SIZE or len(species_constants) != DEX_SIZE:
        raise ValueError("Arauna encounter builder requires 386 source and engine entries")
    incoming = {}
    for entry in entries:
        for evolution in entry.get("evolvesTo") or []:
            incoming[int(evolution["id"])] = evolution_level(evolution["method"])
    story_ids, legendary_ids = story_reserved_ids(source, story)
    profiles = []
    for entry, species in zip(entries, species_constants):
        number = int(entry["id"])
        types = list(entry.get("types") or ["normal"])
        text = " ".join(str(entry.get(field, "")) for field in ("name", "inspiration", "dex"))
        methods = {"land"}
        if "water" in types:
            methods.update(("water", "fishing"))
            if AQUATIC_WORDS.search(text):
                methods.discard("land")
        if {"rock", "ground", "steel"} & set(types):
            methods.add("rock_smash")

        if 1 <= number <= 9:
            availability = "starter"
        elif entry.get("mythical"):
            availability = "mythical"
        elif entry.get("legendary"):
            availability = "legendary"
        elif number in story_ids:
            availability = "story"
        else:
            availability = "wild"

        has_from = number in incoming
        has_to = bool(entry.get("evolvesTo"))
        stage = "middle" if has_from and has_to else "final" if has_from else "base" if has_to else "standalone"
        bst = sum(int(entry["stats"][key]) for key in ("hp", "atk", "def", "spa", "spd", "spe"))
        tier = "early" if bst <= 420 or has_to else "mid" if bst <= 520 else "late"
        if availability != "wild":
            tier = availability
        profiles.append({
            "id": number,
            "name": entry["name"],
            "species": species,
            "types": types,
            "biome": REGION_BIOME.get(entry.get("region"), "cerrado"),
            "source_region": entry.get("region", ""),
            "methods": methods,
            "availability": availability,
            "stage": stage,
            "evolution_level": incoming.get(number, 0),
            "bst": bst,
            "tier": tier,
            "legendary": number in legendary_ids,
        })
    return profiles


def choose_species(
    profiles: list[dict],
    map_name: str,
    field: str,
    slot: int,
    rate: int,
    max_rate: int,
    max_level: int,
    used_species: set[str],
) -> str:
    method = FIELD_METHOD[field]
    biomes = set(map_biomes(map_name))
    affinities = preferred_types(map_name)
    rarity = 1.0 - (rate / max_rate if max_rate else 0)
    cap = min(610, round(300 + max_level * 7 + rarity * 80))
    target = max(260, cap - 35)

    candidates = []
    for profile in profiles:
        if profile["availability"] != "wild" or method not in profile["methods"]:
            continue
        if profile["evolution_level"] and max_level + 1 < profile["evolution_level"]:
            continue
        if profile["bst"] > cap:
            continue
        biome_penalty = 0 if profile["biome"] in biomes else 170
        affinity_bonus = -30 if affinities & set(profile["types"]) else 0
        stage_penalty = 25 if max_level <= 10 and profile["stage"] == "standalone" else 0
        score = abs(profile["bst"] - target) + biome_penalty + affinity_bonus + stage_penalty
        candidates.append((score, profile["id"], profile["species"]))

    if not candidates:
        raise ValueError(f"no encounter candidate for {map_name} {field} level {max_level}")
    candidates.sort()
    shortlist = candidates[:min(18, len(candidates))]
    unused = [candidate for candidate in shortlist if candidate[2] not in used_species]
    if unused:
        shortlist = unused
    key = f"{map_name}|{field}|{slot}|{max_level}|{rate}"
    return shortlist[stable_index(key, len(shortlist))][2]


def rewrite_encounters(data: dict, profiles: list[dict]) -> int:
    changed = 0
    for group in data["wild_encounter_groups"]:
        rates = {
            field["type"]: field["encounter_rates"]
            for field in group.get("fields", [])
        }
        for encounter in group.get("encounters", []):
            map_name = encounter.get("map", group["label"])
            for field, method in FIELD_METHOD.items():
                table = encounter.get(field)
                if not table:
                    continue
                field_rates = rates.get(field) or [1] * len(table["mons"])
                max_rate = max(field_rates)
                used_species = set()
                for slot, mon in enumerate(table["mons"]):
                    rate = field_rates[min(slot, len(field_rates) - 1)]
                    species = choose_species(
                        profiles,
                        map_name,
                        field,
                        slot,
                        rate,
                        max_rate,
                        int(mon["max_level"]),
                        used_species,
                    )
                    used_species.add(species)
                    if mon["species"] != species:
                        mon["species"] = species
                        changed += 1
    return changed


def ensure_wild_coverage(data: dict, profiles: list[dict]) -> int:
    wild_profiles = {profile["species"]: profile for profile in profiles
                     if profile["availability"] == "wild"}
    counts = Counter()
    slots = []
    for group in data["wild_encounter_groups"]:
        rates = {
            field["type"]: field["encounter_rates"]
            for field in group.get("fields", [])
        }
        for encounter in group.get("encounters", []):
            map_name = encounter.get("map", group["label"])
            for field, method in FIELD_METHOD.items():
                table = encounter.get(field)
                if not table:
                    continue
                field_rates = rates.get(field) or [1] * len(table["mons"])
                for slot, mon in enumerate(table["mons"]):
                    counts[mon["species"]] += 1
                    slots.append({
                        "map": map_name,
                        "biomes": set(map_biomes(map_name)),
                        "method": method,
                        "rate": field_rates[min(slot, len(field_rates) - 1)],
                        "max_level": int(mon["max_level"]),
                        "mon": mon,
                    })

    missing = [profile for species, profile in wild_profiles.items() if not counts[species]]
    for profile in sorted(missing, key=lambda value: (value["bst"], value["id"])):
        target_level = max(
            profile["evolution_level"],
            min(55, max(2, round((profile["bst"] - 300) / 8))),
        )
        candidates = []
        for slot in slots:
            if slot["method"] not in profile["methods"]:
                continue
            if profile["evolution_level"] and slot["max_level"] + 1 < profile["evolution_level"]:
                continue
            current = slot["mon"]["species"]
            if counts[current] <= 1:
                continue
            biome_penalty = 0 if profile["biome"] in slot["biomes"] else 1
            level_penalty = max(0, target_level - slot["max_level"])
            score = (
                biome_penalty,
                level_penalty,
                slot["rate"],
                abs(slot["max_level"] - target_level),
                stable_index(f"{profile['id']}|{slot['map']}|{slot['method']}", 1_000_000),
            )
            candidates.append((score, slot))
        if not candidates:
            raise ValueError(f"could not place wild species #{profile['id']:03d}")
        _, selected = min(candidates, key=lambda value: value[0])
        old_species = selected["mon"]["species"]
        selected["mon"]["species"] = profile["species"]
        counts[old_species] -= 1
        counts[profile["species"]] += 1

    remaining = sorted(species for species in wild_profiles if not counts[species])
    if remaining:
        raise ValueError(f"wild species without an encounter: {', '.join(remaining)}")
    return len(missing)


def species_constants(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    result = re.findall(r"^\s*\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\{", text, re.MULTILINE)
    if len(result) != DEX_SIZE:
        raise ValueError(f"expected 386 Arauna species blocks, found {len(result)}")
    return [f"SPECIES_{value}" for value in result]


def write_ecology(path: Path, profiles: list[dict]) -> None:
    fields = (
        "id", "name", "species", "types", "source_region", "biome",
        "availability", "tier", "stage", "evolution_level", "bst", "methods",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for profile in profiles:
            row = {field: profile[field] for field in fields}
            row["id"] = f"{profile['id']:03d}"
            row["types"] = "/".join(profile["types"])
            row["methods"] = "/".join(sorted(profile["methods"]))
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dex", type=Path, default=ROOT / "docs/arauna/source/pokedex.json")
    parser.add_argument("--story-roles", type=Path, default=ROOT / "docs/arauna/source/story_roles.json")
    parser.add_argument("--species", type=Path, default=ROOT / "src/data/pokemon/species_info/arauna_dex.h")
    parser.add_argument("--template", type=Path, default=ROOT / "src/data/wild_encounters.json")
    parser.add_argument("--out", type=Path, default=ROOT / "src/data/wild_encounters.json")
    parser.add_argument("--ecology-out", type=Path, default=ROOT / "docs/arauna/ARAUNA_ENCOUNTER_ECOLOGY.csv")
    args = parser.parse_args()

    source = json.loads(args.dex.read_text(encoding="utf-8"))
    story = json.loads(args.story_roles.read_text(encoding="utf-8"))
    profiles = build_profiles(source, species_constants(args.species), story)
    data = json.loads(args.template.read_text(encoding="utf-8"))
    changed = rewrite_encounters(data, profiles)
    coverage_changes = ensure_wild_coverage(data, profiles)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_ecology(args.ecology_out, profiles)
    print(
        f"rewrote {changed} encounter slots, placed {coverage_changes} coverage entries, "
        f"and documented {len(profiles)} species"
    )


if __name__ == "__main__":
    main()
