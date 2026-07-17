#!/usr/bin/env python3
"""Stage the complete Arauna Dex as a pokeemerald-expansion repository overlay."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import textwrap
import unicodedata
from pathlib import Path


STARTER_TARGETS = [
    "TORCHIC", "COMBUSKEN", "BLAZIKEN",
    "MUDKIP", "MARSHTOMP", "SWAMPERT",
    "TREECKO", "GROVYLE", "SCEPTILE",
]

SOURCE_SUFFIX = {"CASTFORM": "CASTFORM_NORMAL", "DEOXYS": "DEOXYS_NORMAL"}

TYPE_CONSTANT = {
    "normal": "TYPE_NORMAL", "fire": "TYPE_FIRE", "water": "TYPE_WATER",
    "grass": "TYPE_GRASS", "electric": "TYPE_ELECTRIC", "ice": "TYPE_ICE",
    "fighting": "TYPE_FIGHTING", "poison": "TYPE_POISON", "ground": "TYPE_GROUND",
    "flying": "TYPE_FLYING", "psychic": "TYPE_PSYCHIC", "bug": "TYPE_BUG",
    "rock": "TYPE_ROCK", "ghost": "TYPE_GHOST", "dragon": "TYPE_DRAGON",
    "dark": "TYPE_DARK", "steel": "TYPE_STEEL", "fairy": "TYPE_FAIRY",
}

TYPE_ABILITY = {
    "normal": "ABILITY_RUN_AWAY", "fire": "ABILITY_BLAZE", "water": "ABILITY_TORRENT",
    "grass": "ABILITY_OVERGROW", "electric": "ABILITY_STATIC", "ice": "ABILITY_ICE_BODY",
    "fighting": "ABILITY_GUTS", "poison": "ABILITY_POISON_POINT", "ground": "ABILITY_SAND_VEIL",
    "flying": "ABILITY_KEEN_EYE", "psychic": "ABILITY_SYNCHRONIZE", "bug": "ABILITY_SWARM",
    "rock": "ABILITY_STURDY", "ghost": "ABILITY_LEVITATE", "dragon": "ABILITY_INNER_FOCUS",
    "dark": "ABILITY_INTIMIDATE", "steel": "ABILITY_CLEAR_BODY", "fairy": "ABILITY_CUTE_CHARM",
}

TYPE_COLOR = {
    "normal": "BODY_COLOR_BROWN", "fire": "BODY_COLOR_RED", "water": "BODY_COLOR_BLUE",
    "grass": "BODY_COLOR_GREEN", "electric": "BODY_COLOR_YELLOW", "ice": "BODY_COLOR_BLUE",
    "fighting": "BODY_COLOR_RED", "poison": "BODY_COLOR_PURPLE", "ground": "BODY_COLOR_BROWN",
    "flying": "BODY_COLOR_WHITE", "psychic": "BODY_COLOR_PINK", "bug": "BODY_COLOR_GREEN",
    "rock": "BODY_COLOR_GRAY", "ghost": "BODY_COLOR_PURPLE", "dragon": "BODY_COLOR_BLUE",
    "dark": "BODY_COLOR_BLACK", "steel": "BODY_COLOR_GRAY", "fairy": "BODY_COLOR_PINK",
}

ENGINE_NAME_ALIASES = {
    39: "BichoPregça", 99: "Mula-Cabeça", 155: "FormigãoPrto",
    175: "João-Barro", 223: "CavalMarinho", 240: "PernaCabelda",
    256: "Iemanjá-Pq", 261: "CurupAncião", 262: "CaiporaFêm",
    266: "CabocGuerro", 273: "BumbaMeuBoi", 282: "DraguaráAlfa",
    283: "TerolRainha", 284: "PetropAncião", 297: "CorcovAncião",
}


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def national_suffixes(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    suffixes = [value for value in re.findall(r"^\s*NATIONAL_DEX_([A-Z0-9_]+),", text, re.MULTILINE) if value != "NONE"]
    if len(suffixes) < 386:
        raise ValueError("could not read the first 386 National Dex constants")
    return suffixes[:386]


def extract_species_block(text: str, suffix: str) -> str:
    match = re.search(rf"^\s*\[SPECIES_{re.escape(suffix)}\]\s*=\s*\{{", text, re.MULTILINE)
    if not match:
        raise ValueError(f"missing source block for SPECIES_{suffix}")
    start = match.start()
    brace = text.find("{", match.start())
    depth = 0
    quote = False
    escape = False
    for index in range(brace, len(text)):
        char = text[index]
        if quote:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                end = index + 1
                while end < len(text) and text[end] in " \t":
                    end += 1
                if end < len(text) and text[end] == ",":
                    end += 1
                return text[start:end]
    raise ValueError(f"unclosed source block for SPECIES_{suffix}")


def field(block: str, name: str, default: str) -> str:
    match = re.search(rf"\.{re.escape(name)}\s*=\s*([A-Za-z0-9_]+)", block)
    return match.group(1) if match else default


def footprint_symbol(block: str) -> str:
    match = re.search(r"FOOTPRINT\(([A-Za-z0-9_]+)\)", block)
    return match.group(1) if match else "QuestionMark"


def source_block(family_text: str, target: str) -> str:
    if target == "UNOWN":
        return """
        .cryId = CRY_UNOWN,
        .frontPic = gMonFrontPic_UnownA,
        .backPic = gMonBackPic_UnownA,
        .palette = gMonPalette_Unown,
        .shinyPalette = gMonShinyPalette_Unown,
        .iconSprite = gMonIcon_UnownA,
        FOOTPRINT(Unown)
        .levelUpLearnset = sUnownLevelUpLearnset,
        .teachableLearnset = sUnownTeachableLearnset,
        .eggMoveLearnset = sNoneEggMoveLearnset,
        """
    return extract_species_block(family_text, SOURCE_SUFFIX.get(target, target))


def wrapped_description(text: str, width: int = 36, lines: int = 4) -> list[str]:
    text = " ".join(text.replace("\n", " ").split()).replace('"', "'").replace("—", "-").replace("–", "-")
    wrapped = textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False)
    if len(wrapped) > lines:
        wrapped = wrapped[:lines]
        wrapped[-1] = wrapped[-1].rstrip(".,;: ")
        if len(wrapped[-1]) >= width - 2:
            wrapped[-1] = wrapped[-1][:width - 3].rstrip()
        wrapped[-1] += "..."
    return wrapped or ["Sem dados disponíveis."]


def engine_name(entry: dict) -> str:
    value = ENGINE_NAME_ALIASES.get(entry["id"], entry["name"])
    if len(value) > 12:
        raise ValueError(f"engine name exceeds 12 chars: {entry['id']} {value}")
    return value


def category(entry: dict) -> str:
    value = re.sub(r"^Pokémon\s+", "", entry.get("category", "Arauna"), flags=re.IGNORECASE)
    return value[:12]


def apply_localization(entries: list[dict], path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("language") != "en":
        raise ValueError("the English-first build requires an English Dex localization")
    localized = {int(entry["id"]): entry for entry in data["pokemon"]}
    if set(localized) != set(range(1, 387)):
        raise ValueError("English Dex localization must contain IDs 001-386")
    result = []
    for source in entries:
        merged = dict(source)
        translated = localized[int(source["id"])]
        for field_name in ("category", "region", "dex"):
            merged[field_name] = translated[field_name]
        result.append(merged)
    return result


def apply_story_roles(entries: list[dict], path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    non_capturable = {int(entry["id"]) for entry in data["nonCapturable"]}
    if not non_capturable:
        raise ValueError("story roles must declare the non-capturable Census entries")
    result = []
    for source in entries:
        merged = dict(source)
        merged["capturable"] = int(source["id"]) not in non_capturable
        result.append(merged)
    return result


def evolution_level(method: str) -> int:
    match = re.search(r"(\d+)", method)
    if not match:
        raise ValueError(f"unsupported evolution method: {method}")
    return int(match.group(1))


def build_block(entry: dict, target: str, nat_slot: str, target_for_id: dict[int, str], original: str, profile: dict, battle_profile: dict) -> str:
    stats = entry["stats"]
    types = entry.get("types") or ["normal"]
    type_values = ", ".join(TYPE_CONSTANT[t] for t in types[:2])
    lines = wrapped_description(entry.get("dex", ""))
    description = "\n".join(f'            "{line}\\n"' for line in lines[:-1])
    if lines:
        description += ("\n" if description else "") + f'            "{lines[-1]}."' if not lines[-1].endswith(('.', '!', '?')) else ("\n" if description else "") + f'            "{lines[-1]}"'

    evolutions = entry.get("evolvesTo") or []
    evolution_line = ""
    if evolutions:
        evo = evolutions[0]
        evolution_line = f"\n        .evolutions = EVOLUTION({{EVO_LEVEL, {evolution_level(evo['method'])}, SPECIES_{target_for_id[int(evo['id'])]}}}),"

    cry = field(original, "cryId", "CRY_PORYGON")
    front = field(original, "frontPic", "gMonFrontPic_CircledQuestionMark")
    back = field(original, "backPic", front)
    palette = field(original, "palette", "gMonPalette_CircledQuestionMark")
    shiny = field(original, "shinyPalette", "gMonShinyPalette_CircledQuestionMark")
    icon = field(original, "iconSprite", "gMonIcon_QuestionMark")
    level = f"sArauna{int(entry['id']):03d}LevelUpLearnset"
    teachable = field(original, "teachableLearnset", "sNoneTeachableLearnset")
    egg = "sNoneEggMoveLearnset"
    footprint = footprint_symbol(original)
    name = engine_name(entry).replace('"', "'")
    cat = category(entry).replace('"', "'")

    return f'''    [SPECIES_{target}] =
    {{
        .baseHP        = {int(stats['hp'])},
        .baseAttack    = {int(stats['atk'])},
        .baseDefense   = {int(stats['def'])},
        .baseSpeed     = {int(stats['spe'])},
        .baseSpAttack  = {int(stats['spa'])},
        .baseSpDefense = {int(stats['spd'])},
        .types = MON_TYPES({type_values}),
        .catchRate = {battle_profile['catch_rate']},
        .expYield = {battle_profile['exp_yield']},
        .genderRatio = {battle_profile['gender_ratio']},
        .eggCycles = {battle_profile['egg_cycles']},
        .friendship = STANDARD_FRIENDSHIP,
        .growthRate = {battle_profile['growth_rate']},
        .eggGroups = MON_EGG_GROUPS({battle_profile['egg_group1']}{'' if battle_profile['egg_group1'] == battle_profile['egg_group2'] else ', ' + battle_profile['egg_group2']}),
        .abilities = {{ {battle_profile['ability1']}, {battle_profile['ability2']}, {battle_profile['hidden_ability']} }},
        .bodyColor = {TYPE_COLOR[types[0]]},
        .speciesName = _("{name}"),
        .cryId = {cry},
        .natDexNum = NATIONAL_DEX_{nat_slot},
        .categoryName = _("{cat}"),
        .height = {max(1, round(float(entry.get('height', 1)) * 10))},
        .weight = {max(1, round(float(entry.get('weight', 1)) * 10))},
        .description = COMPOUND_STRING(
{description}),
        .pokemonScale = 256,
        .pokemonOffset = 0,
        .trainerScale = 256,
        .trainerOffset = 0,
        .frontPic = {front},
        .frontPicSize = MON_COORDS_SIZE(64, 64),
        .frontPicYOffset = 0,
        .frontAnimFrames = ANIM_FRAMES(
            ANIMCMD_FRAME(0, 30),
            ANIMCMD_FRAME(1, 20),
            ANIMCMD_FRAME(0, 1),
        ),
        .frontAnimId = ANIM_V_SQUISH_AND_BOUNCE,
        .backPic = {back},
        .backPicSize = MON_COORDS_SIZE(64, 64),
        .backPicYOffset = 0,
        .backAnimId = BACK_ANIM_DIP_RIGHT_SIDE,
        .palette = {palette},
        .shinyPalette = {shiny},
        .iconSprite = {icon},
        .iconPalIndex = {int(profile['iconPalIndex'])},
        .pokemonJumpType = PKMN_JUMP_TYPE_NORMAL,
        SHADOW(0, 0, SHADOW_SIZE_M)
        FOOTPRINT({footprint})
        .levelUpLearnset = {level},
        .teachableLearnset = {teachable},
        .eggMoveLearnset = {egg},{evolution_line}
    }},
'''


def graphics_asset_paths(path: Path) -> dict[str, list[str]]:
    text = path.read_text(encoding="utf-8")
    result: dict[str, list[str]] = {}
    pattern = re.compile(r'const\s+[^;=]+\s+(gMon(?:FrontPic|BackPic|Palette|ShinyPalette|Icon)_[A-Za-z0-9_]+)\[\]\s*=\s*INCGFX_[A-Z0-9]+\("([^"]+)"')
    for symbol, asset_path in pattern.findall(text):
        result.setdefault(symbol, [])
        if asset_path not in result[symbol]:
            result[symbol].append(asset_path)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dex", type=Path, default=Path("arauna_dex_import/pokedex.json"))
    parser.add_argument("--localization", type=Path, default=Path("docs/arauna/source/pokedex.en.json"))
    parser.add_argument("--story-roles", type=Path, default=Path("docs/arauna/source/story_roles.json"))
    parser.add_argument("--battle-profiles", type=Path, default=Path("docs/arauna/ARAUNA_BATTLE_PROFILES.csv"))
    parser.add_argument("--packages", type=Path, default=Path("art_candidates/full_dex/gba"))
    parser.add_argument("--engine", type=Path, default=Path("engine-reference"))
    parser.add_argument("--out", type=Path, default=Path("full_dex_build/repo_overlay"))
    args = parser.parse_args()

    entries = json.loads(args.dex.read_text(encoding="utf-8"))["pokemon"]
    entries = apply_localization(entries, args.localization)
    entries = apply_story_roles(entries, args.story_roles)
    with args.battle_profiles.open(encoding="utf-8", newline="") as source:
        battle_profiles = {int(row["id"]): row for row in csv.DictReader(source)}
    if set(battle_profiles) != set(range(1, 387)):
        raise ValueError("battle profiles must contain IDs 001-386")
    nat = national_suffixes(args.engine / "include/constants/pokedex.h")
    targets = STARTER_TARGETS + [suffix for suffix in nat if suffix not in STARTER_TARGETS]
    if len(targets) != 386 or len(set(targets)) != 386:
        raise ValueError("target mapping must contain 386 unique species")
    target_for_id = {entry["id"]: targets[entry["id"] - 1] for entry in entries}

    family_text = "\n".join((args.engine / f"src/data/pokemon/species_info/gen_{gen}_families.h").read_text(encoding="utf-8") for gen in (1, 2, 3))
    asset_paths = graphics_asset_paths(args.engine / "src/data/graphics/pokemon.h")
    header_blocks = []
    mapping_rows = []
    for entry, target, nat_slot in zip(entries, targets, nat):
        original = source_block(family_text, target)
        front_symbol = field(original, "frontPic", "")
        if not front_symbol.startswith("gMonFrontPic_"):
            raise ValueError(f"could not resolve front graphic for {target}")
        symbol = front_symbol.removeprefix("gMonFrontPic_")
        front_paths = asset_paths.get(front_symbol, [])
        if not front_paths:
            raise ValueError(f"could not resolve graphics path for {front_symbol}")
        folder = str(Path(front_paths[0]).parent).removeprefix("graphics/pokemon/")
        package = args.packages / f"{entry['id']:03d}_{slugify(entry['name'])}"
        profile = json.loads((package / "candidate_profile.json").read_text(encoding="utf-8"))
        header_blocks.append(build_block(entry, target, nat_slot, target_for_id, original, profile, battle_profiles[int(entry["id"])]))

        symbol_sources = {
            front_symbol: "anim_front.png",
            field(original, "backPic", ""): "back.png",
            field(original, "iconSprite", ""): "icon.png",
            field(original, "palette", ""): "normal.pal",
            field(original, "shinyPalette", ""): "shiny.pal",
        }
        copied = 0
        for asset_symbol, source_name in symbol_sources.items():
            paths = asset_paths.get(asset_symbol, [])
            if not paths:
                raise ValueError(f"could not resolve graphics paths for {asset_symbol} ({target})")
            for relative in paths:
                destination = args.out / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(package / source_name, destination)
                copied += 1
        mapping_rows.append({
            "arauna_dex": f"{entry['id']:03d}", "full_name": entry["name"],
            "engine_name": engine_name(entry), "species_constant": f"SPECIES_{target}",
            "national_slot": f"NATIONAL_DEX_{nat_slot}", "graphics_folder": folder,
            "types": "/".join(entry.get("types", [])), "production_method": profile["productionMethod"],
            "capturable": "yes" if entry.get("capturable", True) else "no",
        })

    header = """// Auto-generated by tools/integrate_full_arauna_dex.py.\n// Complete Arauna replacement for National Dex slots 001-386.\n\n""" + "\n".join(header_blocks)
    header_path = args.out / "src/data/pokemon/species_info/arauna_dex.h"
    header_path.parent.mkdir(parents=True, exist_ok=True)
    header_path.write_text(header, encoding="utf-8")

    species_info_source = (args.engine / "src/data/pokemon/species_info.h").read_text(encoding="utf-8")
    old_includes = '''    #include "species_info/gen_1_families.h"
    #include "species_info/gen_2_families.h"
    #include "species_info/gen_3_families.h"'''
    if old_includes not in species_info_source:
        raise ValueError("could not locate the Gen 1-3 include block in species_info.h")
    species_info_source = species_info_source.replace(
        old_includes,
        '    // Arauna replaces National Dex slots 001-386.\n    #include "species_info/arauna_dex.h"',
        1,
    )
    species_info_path = args.out / "src/data/pokemon/species_info.h"
    species_info_path.parent.mkdir(parents=True, exist_ok=True)
    species_info_path.write_text(species_info_source, encoding="utf-8")

    mapping_path = args.out / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv"
    mapping_path.parent.mkdir(parents=True, exist_ok=True)
    with mapping_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(mapping_rows[0]))
        writer.writeheader(); writer.writerows(mapping_rows)

    readme = args.out / "docs/arauna/FULL_FAKEMON_ART_INTEGRATION.md"
    readme.write_text(f"""# Integração integral da Dex de Arauna\n\n- 386 entradas substituem, uma a uma, os slots nacionais 001–386.\n- Slots de batalha dos iniciais: Torchic/Combusken/Blaziken, Mudkip/Marshtomp/Swampert e Treecko/Grovyle/Sceptile.\n- 314 referências fornecidas foram convertidas para o formato do GBA.\n- 72 entradas sem imagem receberam conceitos procedurais originais e reproduzíveis.\n- Cada entrada tem frontal animada em dois quadros, traseira, ícone, paleta normal e paleta shiny.\n- Nomes, tipos, atributos, altura, peso, descrição e evoluções por nível vêm de `pokedex.json`.\n- Quinze nomes acima do limite técnico de 12 caracteres usam abreviação apenas dentro do motor; os nomes integrais permanecem no manifesto e no mapeamento.\n\nA arte fonte de 010–314 só possui vista frontal. As traseiras desses números são reconstruções técnicas da silhueta para batalha; podem ser refinadas individualmente no mesmo slot sem alterar dados ou scripts.\n""", encoding="utf-8")
    graphic_count = sum(1 for path in (args.out / "graphics/pokemon").rglob("*") if path.is_file())
    print(f"staged 386 species, {graphic_count} graphic files, header={header_path}, mapping={mapping_path}")


if __name__ == "__main__":
    main()
