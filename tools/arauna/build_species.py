#!/usr/bin/env python3
"""Install the 386 Arauna species into the engine's species tables.

Inputs, all versioned so a run is reproducible:

  graphics/arauna/arauna_sprites_gba_export.zip  pokedex.json: the approved
                                                 names, types, stats, abilities,
                                                 categories, heights, weights and
                                                 dex prose for all 386
  docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv      which engine species each Arauna
                                                 dex number occupies
  docs/arauna/ARAUNA_ABILITIES.csv               Arauna ability name -> engine ability
  docs/arauna/ARAUNA_NAMES_SHORT.csv             10-character display forms for the
                                                 36 names that do not fit
  docs/arauna/ARAUNA_CATEGORIES_SHORT.csv        11-character forms for the six
                                                 dex categories that do not fit

Outputs:

  src/data/text/species_names.h
  src/data/pokemon/species_info.h
  src/data/pokemon/pokedex_text.h
  src/data/pokemon/pokedex_entries.h
  src/data/pokemon/pokedex_orders.h
  src/data/pokemon/species_to_national.h
  src/data/pokemon/species_to_hoenn.h
  src/data/pokemon/hoenn_to_national.h

The 54 engine slots Arauna does not use -- SPECIES_NONE, SPECIES_EGG, the Unown
forms and the old Unown placeholders -- keep their vanilla rows untouched.

Two constraints shape everything here:

  * The save layout is fixed. BoxPokemon.nickname is ten bytes and
    SetBoxMonData copies POKEMON_NAME_LENGTH of them, so the constant cannot
    grow without corrupting the fields behind it. Names longer than ten
    characters therefore get an explicit display form from ARAUNA_NAMES_SHORT.csv
    rather than being silently cut.

  * The charmap has no 'ã' and no 'õ'. The rest of the project already writes
    Portuguese without them, so every string is transliterated the same way
    before it is emitted, and anything still unmappable is an error. A word-final
    'ã' becomes 'an' rather than 'a', which keeps the nasal reading and, more
    practically, keeps Boitatã apart from Boitatá and Iemanjã apart from Iemanjá.

Fields the source data does not carry -- catch rate, exp yield, EV yield, egg
groups, growth rate, gender ratio, body colour -- are derived by the documented
rules in DERIVED_RULES below rather than invented per species.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import unicodedata
import zipfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPORT = ROOT / "graphics/arauna/arauna_sprites_gba_export.zip"
MAPPING = ROOT / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv"
ABILITIES = ROOT / "docs/arauna/ARAUNA_ABILITIES.csv"
SHORT_NAMES = ROOT / "docs/arauna/ARAUNA_NAMES_SHORT.csv"
SHORT_CATEGORIES = ROOT / "docs/arauna/ARAUNA_CATEGORIES_SHORT.csv"
CHARMAP = ROOT / "charmap.txt"

NAMES_H = ROOT / "src/data/text/species_names.h"
INFO_H = ROOT / "src/data/pokemon/species_info.h"
TEXT_H = ROOT / "src/data/pokemon/pokedex_text.h"
ENTRIES_H = ROOT / "src/data/pokemon/pokedex_entries.h"
ORDERS_H = ROOT / "src/data/pokemon/pokedex_orders.h"
TO_NATIONAL_H = ROOT / "src/data/pokemon/species_to_national.h"
TO_HOENN_H = ROOT / "src/data/pokemon/species_to_hoenn.h"
HOENN_TO_NATIONAL_H = ROOT / "src/data/pokemon/hoenn_to_national.h"

NAME_LENGTH = 10
CATEGORY_LENGTH = 11  # u8 categoryName[12], one byte for the terminator
DEX_LINE_WIDTH = 44   # vanilla entries reach 46; 44 leaves room for wider glyphs
DEX_LINES = 4
HOENN_DEX_COUNT = 202

DERIVED_RULES = """\
Derived fields and the rule behind each:

  catchRate      legendary/mythical 3; final stage of a three-link chain 45;
                 final stage of a two-link chain 60; middle stage 120;
                 basic with an evolution 190; standalone 90
  expYield       base stat total / 3
  evYield        final stage 2 in the highest base stat and 1 in the second;
                 middle stage 1 in the highest; basic 1 in the highest
  genderRatio    legendary/mythical genderless, everything else 50/50
  eggCycles      legendary/mythical 120, everything else 20
  friendship     legendary/mythical 0, everything else STANDARD_FRIENDSHIP
  growthRate     legendary/mythical slow; three-link family medium-slow;
                 everything else medium-fast
  eggGroups      from the two types; legendary/mythical get no eggs discovered
  bodyColor      the dominant opaque colour of the front sprite
  items          none
  safariZoneFleeRate 0
  noFlip         false
"""

TYPE_TO_ENGINE = {
    "normal": "TYPE_NORMAL", "fighting": "TYPE_FIGHTING", "flying": "TYPE_FLYING",
    "poison": "TYPE_POISON", "ground": "TYPE_GROUND", "rock": "TYPE_ROCK",
    "bug": "TYPE_BUG", "ghost": "TYPE_GHOST", "steel": "TYPE_STEEL",
    "fire": "TYPE_FIRE", "water": "TYPE_WATER", "grass": "TYPE_GRASS",
    "electric": "TYPE_ELECTRIC", "psychic": "TYPE_PSYCHIC", "ice": "TYPE_ICE",
    "dragon": "TYPE_DRAGON", "dark": "TYPE_DARK", "fairy": "TYPE_FAIRY",
}

# Egg group per primary type, then a refinement from the secondary type.
EGG_BY_TYPE = {
    "water": "EGG_GROUP_WATER_1", "bug": "EGG_GROUP_BUG", "grass": "EGG_GROUP_GRASS",
    "flying": "EGG_GROUP_FLYING", "fire": "EGG_GROUP_FIELD", "normal": "EGG_GROUP_FIELD",
    "ground": "EGG_GROUP_FIELD", "electric": "EGG_GROUP_FIELD", "rock": "EGG_GROUP_MINERAL",
    "steel": "EGG_GROUP_MINERAL", "ghost": "EGG_GROUP_AMORPHOUS", "poison": "EGG_GROUP_AMORPHOUS",
    "psychic": "EGG_GROUP_AMORPHOUS", "fairy": "EGG_GROUP_FAIRY", "dragon": "EGG_GROUP_DRAGON",
    "dark": "EGG_GROUP_FIELD", "fighting": "EGG_GROUP_HUMAN_LIKE", "ice": "EGG_GROUP_FIELD",
}

# Body colours the engine offers, with a representative RGB to match sprites against.
BODY_COLORS = [
    ("BODY_COLOR_RED", (200, 50, 50)),
    ("BODY_COLOR_BLUE", (60, 90, 200)),
    ("BODY_COLOR_YELLOW", (230, 210, 70)),
    ("BODY_COLOR_GREEN", (70, 170, 80)),
    ("BODY_COLOR_BLACK", (40, 40, 45)),
    ("BODY_COLOR_BROWN", (140, 100, 60)),
    ("BODY_COLOR_PURPLE", (140, 70, 180)),
    ("BODY_COLOR_GRAY", (130, 130, 130)),
    ("BODY_COLOR_WHITE", (235, 235, 235)),
    ("BODY_COLOR_PINK", (240, 150, 180)),
]

TRANSLITERATE = {"ã": "a", "õ": "o", "Ã": "A", "Õ": "O", "’": "'", "“": '"', "”": '"', "—": "-", "–": "-"}
# A word-final tilde carries the whole reading of the word, so spell it out.
FINAL_TILDE = re.compile(r"ã(?![a-zà-ÿ])")


# ---------------------------------------------------------------- text helpers

def charmap_chars() -> set[str]:
    chars = set()
    for line in CHARMAP.read_text(encoding="utf-8").splitlines():
        line = line.split("@")[0].strip()
        if "=" not in line:
            continue
        key = line.split("=")[0].strip()
        if key.startswith("'") and key.endswith("'"):
            key = key[1:-1]
        chars.add(key)
    return chars


CHARS = None
# Read once, before the file is overwritten by this run.
ORDERS_SOURCE = ORDERS_H.read_text(encoding="utf-8")


def sanitize(text: str) -> str:
    """Make a string writable with this ROM's charmap."""
    text = FINAL_TILDE.sub("an", text)
    out = "".join(TRANSLITERATE.get(c, c) for c in text)
    missing = [c for c in out if c not in CHARS and c not in " "]
    if missing:
        # Last resort: strip the accent rather than emit a character the
        # assembler cannot encode.
        stripped = []
        for c in out:
            if c in CHARS or c == " ":
                stripped.append(c)
            else:
                base = unicodedata.normalize("NFD", c)[0]
                stripped.append(base if base in CHARS else "")
        out = "".join(stripped)
    return out


def escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def wrap_dex(text: str) -> list[str]:
    """Fit the dex prose into the four lines the Pokédex page shows."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= DEX_LINE_WIDTH:
            current = candidate
            continue
        lines.append(current)
        current = word
        if len(lines) == DEX_LINES:
            break
    if current and len(lines) < DEX_LINES:
        lines.append(current)
    return lines[:DEX_LINES]


def identifier(name: str, dex: int) -> str:
    """Caramelão #002 -> Caramelao002, so near-duplicate names stay distinct.

    The dex has four pairs that differ only by an accent or a capital letter --
    Boitatá/Boitatã, Iemanjá/Iemanjã, Beija-flor/Beija-Flor and two Tamanduás --
    and the number keeps their C symbols apart without renaming anything.
    """
    ascii_name = unicodedata.normalize("NFD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]", "", ascii_name.title()) + f"{dex:03d}"


# ---------------------------------------------------------------- data loading

def load_export():
    with zipfile.ZipFile(EXPORT) as zf:
        dex = json.loads(zf.read("pokedex.json"))
        sprites = {}
        for entry in dex["pokemon"]:
            name = f"front/{entry['spriteFile'].split('/')[-1]}"
            sprites[entry["id"]] = zf.read(name) if name in zf.namelist() else None
    return dex["pokemon"], sprites


def load_tables():
    mapping = {int(r["arauna_dex"]): r for r in csv.DictReader(MAPPING.open(encoding="utf-8"))}
    abilities = {r["arauna_ability"]: r["engine_ability"]
                 for r in csv.DictReader(ABILITIES.open(encoding="utf-8"))}
    short = {int(r["arauna_dex"]): r["display_name"]
             for r in csv.DictReader(SHORT_NAMES.open(encoding="utf-8"))}
    categories = {int(r["arauna_dex"]): r["short_category"]
                  for r in csv.DictReader(SHORT_CATEGORIES.open(encoding="utf-8"))}
    return mapping, abilities, short, categories


def dominant_color(png: bytes | None) -> str:
    if png is None:
        return "BODY_COLOR_BROWN"
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        return "BODY_COLOR_BROWN"
    image = Image.open(io.BytesIO(png))
    indexed = np.array(image.convert("P"))
    palette = image.getpalette() or []
    opaque = indexed != 0
    if not opaque.any():
        return "BODY_COLOR_BROWN"
    values, counts = np.unique(indexed[opaque], return_counts=True)
    total = counts.sum()
    r = g = b = 0.0
    for value, count in zip(values, counts):
        base = int(value) * 3
        if base + 2 >= len(palette):
            continue
        weight = count / total
        r += palette[base] * weight
        g += palette[base + 1] * weight
        b += palette[base + 2] * weight
    return min(BODY_COLORS, key=lambda c: sum((a - b2) ** 2 for a, b2 in zip(c[1], (r, g, b))))[0]


# ---------------------------------------------------------------- derivation

def build_species(entries, mapping, abilities, short, categories, sprites):
    by_id = {e["id"]: e for e in entries}
    evolves_to = {e["id"]: [t["id"] for t in e.get("evolvesTo", [])] for e in entries}
    evolves_from = {e["id"]: e.get("evolvesFrom") for e in entries}

    def chain_length(dex: int) -> int:
        length, current, seen = 1, dex, set()
        while evolves_to.get(current) and current not in seen:
            seen.add(current)
            current = evolves_to[current][0]
            length += 1
        return length

    def chain_root(dex: int) -> int:
        current, seen = dex, set()
        while evolves_from.get(current) and current not in seen:
            seen.add(current)
            nxt = evolves_from[current]
            current = nxt["id"] if isinstance(nxt, dict) else nxt
        return current

    species = []
    for entry in entries:
        dex = entry["id"]
        row = mapping[dex]
        stats = entry["stats"]
        bst = sum(stats.values())
        special = bool(entry.get("legendary") or entry.get("mythical"))
        has_evo = bool(evolves_to.get(dex))
        has_pre = evolves_from.get(dex) is not None
        family = chain_length(chain_root(dex))

        if special:
            catch = 3
        elif not has_evo and has_pre:
            catch = 45 if family >= 3 else 60
        elif has_evo and has_pre:
            catch = 120
        elif has_evo:
            catch = 190
        else:
            catch = 90

        order = sorted(stats.items(), key=lambda kv: -kv[1])
        ev = {k: 0 for k in stats}
        if special or (has_pre and not has_evo):
            ev[order[0][0]] = 2
            ev[order[1][0]] = 1
        elif has_pre:
            ev[order[0][0]] = 1
        else:
            ev[order[0][0]] = 1

        types = [TYPE_TO_ENGINE[t] for t in entry["types"]]
        if len(types) == 1:
            types.append(types[0])

        if special:
            eggs = ["EGG_GROUP_NO_EGGS_DISCOVERED", "EGG_GROUP_NO_EGGS_DISCOVERED"]
        else:
            primary = EGG_BY_TYPE[entry["types"][0]]
            secondary = EGG_BY_TYPE[entry["types"][1]] if len(entry["types"]) > 1 else primary
            eggs = [primary, secondary if secondary != primary else primary]

        if special:
            growth = "GROWTH_SLOW"
        elif family >= 3:
            growth = "GROWTH_MEDIUM_SLOW"
        else:
            growth = "GROWTH_MEDIUM_FAST"

        names = [abilities[a] for a in entry.get("abilities", [])]
        while len(names) < 2:
            names.append("ABILITY_NONE")
        if names[0] == names[1]:
            names[1] = "ABILITY_NONE"

        display = sanitize(short.get(dex, entry["name"]))
        category = categories.get(dex) or re.sub(r"^Pok[eé]mon\s+", "", entry["category"]).strip()
        category = sanitize(category)

        species.append(dict(
            dex=dex,
            constant=row["species_constant"],
            national=row["national_slot"],
            folder=row["graphics_folder"],
            full_name=entry["name"],
            display=display,
            symbol=identifier(entry["name"], dex),
            types=types,
            stats=stats,
            bst=bst,
            catch=catch,
            exp=max(1, bst // 3),
            ev=ev,
            gender="MON_GENDERLESS" if special else "PERCENT_FEMALE(50)",
            egg_cycles=120 if special else 20,
            friendship="0" if special else "STANDARD_FRIENDSHIP",
            growth=growth,
            eggs=eggs,
            abilities=names,
            body=dominant_color(sprites.get(dex)),
            category=category,
            height=int(round(entry["height"] * 10)),
            weight=int(round(entry["weight"] * 10)),
            dex_lines=[sanitize(line) for line in wrap_dex(entry["dex"])],
            dex_full=entry["dex"],
        ))
    return species


def validate(species):
    problems = []
    for s in species:
        if len(s["display"]) > NAME_LENGTH:
            problems.append(f"#{s['dex']:03d} display name {s['display']!r} is {len(s['display'])} chars")
        if len(s["category"]) > CATEGORY_LENGTH:
            problems.append(f"#{s['dex']:03d} category {s['category']!r} is {len(s['category'])} chars")
        if not s["dex_lines"]:
            problems.append(f"#{s['dex']:03d} has no dex text")
    symbols = defaultdict(list)
    for s in species:
        symbols[s["symbol"]].append(s["dex"])
    for symbol, ids in symbols.items():
        if len(ids) > 1:
            problems.append(f"dex-text symbol {symbol!r} is shared by {ids}")
    return problems


# ---------------------------------------------------------------- rendering

BANNER = ("// Generated by tools/arauna/build_species.py from the approved Arauna dex.\n"
          "// Edit the CSVs under docs/arauna/ and rerun rather than editing this file.\n\n")


def vanilla_rows(path: Path, pattern: str, keep: set[str]) -> list[str]:
    """Pull the rows of an existing table whose key is not one Arauna occupies."""
    rows, source = [], path.read_text(encoding="utf-8")
    for match in re.finditer(pattern, source, re.M):
        if match.group(1) in keep:
            rows.append(match.group(0).rstrip())
    return rows


def render_names(species) -> str:
    used = {s["constant"] for s in species}
    kept = vanilla_rows(NAMES_H, r"^\s*\[(SPECIES_\w+)\] = _\(\"[^\"]*\"\),",
                        set(re.findall(r"\[(SPECIES_\w+)\]", NAMES_H.read_text(encoding="utf-8"))) - used)
    lines = [BANNER + "const u8 gSpeciesNames[][POKEMON_NAME_LENGTH + 1] = {"]
    lines += [row for row in kept]
    lines.append("")
    for s in sorted(species, key=lambda x: x["dex"]):
        comment = "" if s["display"] == s["full_name"] else f"  // #{s['dex']:03d} {s['full_name']}"
        lines.append(f'    [{s["constant"]}] = _("{escape(s["display"])}"),{comment}')
    lines.append("};\n")
    return "\n".join(lines)


def render_info(species) -> str:
    source = INFO_H.read_text(encoding="utf-8")
    header = source[:source.index("const struct SpeciesInfo gSpeciesInfo[] =")]
    used = {s["constant"] for s in species}
    kept = []
    for match in re.finditer(r"^    \[(SPECIES_\w+)\] =\n    \{.*?^    \},$", source, re.M | re.S):
        if match.group(1) not in used:
            kept.append(match.group(0))
    for match in re.finditer(r"^    \[(SPECIES_\w+)\] = \{0\},$", source, re.M):
        if match.group(1) not in used:
            kept.append(match.group(0))
    for match in re.finditer(r"^    \[(SPECIES_\w+)\] = OLD_UNOWN_SPECIES_INFO,$", source, re.M):
        if match.group(1) not in used:
            kept.append(match.group(0))

    out = [BANNER + header + "const struct SpeciesInfo gSpeciesInfo[] =", "{"]
    out += [row + "\n" for row in kept]
    for s in sorted(species, key=lambda x: x["dex"]):
        st = s["stats"]
        ev = s["ev"]
        out.append(f"    [{s['constant']}] = // #{s['dex']:03d} {s['full_name']}")
        out.append("    {")
        out.append(f"        .baseHP        = {st['hp']},")
        out.append(f"        .baseAttack    = {st['atk']},")
        out.append(f"        .baseDefense   = {st['def']},")
        out.append(f"        .baseSpeed     = {st['spe']},")
        out.append(f"        .baseSpAttack  = {st['spa']},")
        out.append(f"        .baseSpDefense = {st['spd']},")
        out.append(f"        .types = {{ {s['types'][0]}, {s['types'][1]} }},")
        out.append(f"        .catchRate = {s['catch']},")
        out.append(f"        .expYield = {s['exp']},")
        out.append(f"        .evYield_HP        = {ev['hp']},")
        out.append(f"        .evYield_Attack    = {ev['atk']},")
        out.append(f"        .evYield_Defense   = {ev['def']},")
        out.append(f"        .evYield_Speed     = {ev['spe']},")
        out.append(f"        .evYield_SpAttack  = {ev['spa']},")
        out.append(f"        .evYield_SpDefense = {ev['spd']},")
        out.append("        .itemCommon = ITEM_NONE,")
        out.append("        .itemRare   = ITEM_NONE,")
        out.append(f"        .genderRatio = {s['gender']},")
        out.append(f"        .eggCycles = {s['egg_cycles']},")
        out.append(f"        .friendship = {s['friendship']},")
        out.append(f"        .growthRate = {s['growth']},")
        out.append(f"        .eggGroups = {{ {s['eggs'][0]}, {s['eggs'][1]} }},")
        out.append(f"        .abilities = {{{s['abilities'][0]}, {s['abilities'][1]}}},")
        out.append("        .safariZoneFleeRate = 0,")
        out.append(f"        .bodyColor = {s['body']},")
        out.append("        .noFlip = FALSE,")
        out.append("    },\n")
    out.append("};\n")
    return "\n".join(out)


def render_text(species) -> str:
    source = TEXT_H.read_text(encoding="utf-8")
    dummy = re.search(r"^const u8 gDummyPokedexText\[\] = _\(.*?\);$", source, re.M | re.S).group(0)
    out = [BANNER + dummy + "\n"]
    for s in sorted(species, key=lambda x: x["dex"]):
        lines = s["dex_lines"]
        newline = "\\n"
        body = "\n".join(
            '    "' + escape(line) + (newline if i < len(lines) - 1 else "") + '"'
            for i, line in enumerate(lines))
        out.append(f"const u8 g{s['symbol']}PokedexText[] = _(\n{body});\n")
    return "\n".join(out)


def render_entries(species) -> str:
    source = ENTRIES_H.read_text(encoding="utf-8")
    scales = {}
    for match in re.finditer(
            r"\[(NATIONAL_DEX_\w+)\] =\s*\{.*?\.pokemonScale = (\d+),\s*\.pokemonOffset = (-?\d+),"
            r"\s*\.trainerScale = (\d+),\s*\.trainerOffset = (-?\d+),", source, re.S):
        scales[match.group(1)] = tuple(int(match.group(i)) for i in range(2, 6))

    out = [BANNER + "const struct PokedexEntry gPokedexEntries[] =", "{",
           "    [NATIONAL_DEX_NONE] =", "    {",
           '        .categoryName = _("UNKNOWN"),',
           "        .height = 0,", "        .weight = 0,",
           "        .description = gDummyPokedexText,",
           "        .pokemonScale = 256,", "        .pokemonOffset = 0,",
           "        .trainerScale = 256,", "        .trainerOffset = 0,",
           "    },\n"]
    for s in sorted(species, key=lambda x: x["dex"]):
        ps, po, ts, to = scales.get(s["national"], (256, 0, 256, 0))
        out.append(f"    [{s['national']}] = // #{s['dex']:03d} {s['full_name']}")
        out.append("    {")
        out.append(f'        .categoryName = _("{escape(s["category"])}"),')
        out.append(f"        .height = {s['height']},")
        out.append(f"        .weight = {s['weight']},")
        out.append(f"        .description = g{s['symbol']}PokedexText,")
        out.append(f"        .pokemonScale = {ps},")
        out.append(f"        .pokemonOffset = {po},")
        out.append(f"        .trainerScale = {ts},")
        out.append(f"        .trainerOffset = {to},")
        out.append("    },\n")
    out.append("};\n")
    return "\n".join(out)


def render_orders(species) -> str:
    # The alphabetical list is walked NUM_SPECIES - 1 times, the other two only
    # NATIONAL_DEX_COUNT times, so the first table also carries the national
    # slots Arauna does not use. Their names are "?", which is where vanilla
    # sorts them too: first.
    used = {s["national"] for s in species}
    spare = [c for c in re.findall(r"^\s*(NATIONAL_DEX_\w+),", ORDERS_SOURCE, re.M)
             if c not in used and c != "NATIONAL_DEX_NONE"]
    spare = list(dict.fromkeys(spare))

    def table(name, key, head=()):
        rows = sorted(species, key=key)
        body = "\n".join([f"    {c}," for c in head] + [f"    {s['national']}," for s in rows])
        return f"const u16 {name}[] =\n{{\n{body}\n}};\n"

    return (BANNER
            + table("gPokedexOrder_Alphabetical",
                    lambda s: (s["display"].upper(), s["dex"]), spare) + "\n"
            + table("gPokedexOrder_Weight", lambda s: (s["weight"], s["dex"])) + "\n"
            + table("gPokedexOrder_Height", lambda s: (s["height"], s["dex"])))


def render_dex_numbers(species):
    """Arauna has one dex read in one order, so regional number == national number.

    HOENN_DEX_COUNT stays 202, which makes the regional Pokédex exactly
    #001-#202 and leaves the completion check the campaign already uses intact.
    """
    used = {s["constant"] for s in species}
    source = (ROOT / "src/pokemon.c").read_text(encoding="utf-8")

    def leftovers(macro):
        names = re.findall(rf"^\s*{macro}\((\w+)\),$", source, re.M)
        return [n for n in names if f"SPECIES_{n}" not in used]

    national = [BANNER + "// [SPECIES_x - 1] = its Arauna dex number."]
    hoenn = [BANNER + "// [SPECIES_x - 1] = its Arauna regional number, which is the same number."]
    for s in sorted(species, key=lambda x: x["dex"]):
        comment = f"// #{s['dex']:03d} {s['full_name']}"
        national.append(f"    [{s['constant']} - 1] = {s['dex']}, {comment}")
        hoenn.append(f"    [{s['constant']} - 1] = {s['dex']}, {comment}")
    for name in leftovers("SPECIES_TO_NATIONAL"):
        national.append(f"    SPECIES_TO_NATIONAL({name}),")
    for name in leftovers("SPECIES_TO_HOENN"):
        hoenn.append(f"    SPECIES_TO_HOENN({name}),")

    order = [BANNER + "// [regional number - 1] = national number; the two orders coincide."]
    for s in sorted(species, key=lambda x: x["dex"]):
        order.append(f"    [{s['dex']} - 1] = {s['dex']}, // {s['full_name']}")
    for name in re.findall(r"^\s*HOENN_TO_NATIONAL\((\w+)\),$", source, re.M):
        if f"SPECIES_{name}" not in used:
            order.append(f"    HOENN_TO_NATIONAL({name}),")

    return ("\n".join(national) + "\n", "\n".join(hoenn) + "\n", "\n".join(order) + "\n")


# ---------------------------------------------------------------- entry point

def main() -> int:
    global CHARS
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="validate only, write nothing")
    parser.add_argument("--write", action="store_true", help="write the generated tables")
    args = parser.parse_args()

    CHARS = charmap_chars()
    entries, sprites = load_export()
    mapping, abilities, short, categories = load_tables()

    unknown = sorted({a for e in entries for a in e.get("abilities", [])} - set(abilities))
    if unknown:
        print(f"abilities with no engine mapping: {unknown}", file=sys.stderr)
        return 1

    species = build_species(entries, mapping, abilities, short, categories, sprites)
    problems = validate(species)
    if problems:
        for problem in problems:
            print(f"species data problem: {problem}", file=sys.stderr)
        return 1

    shared = defaultdict(list)
    for entry in species:
        shared[entry["display"]].append(entry["dex"])
    for name, ids in sorted(shared.items()):
        if len(ids) > 1:
            print(f"note: {name!r} is the displayed name of {ids} in the source data")

    trimmed = sum(1 for s in species if len(" ".join(s["dex_lines"])) < len(s["dex_full"]) - 2)
    print(f"design OK: {len(species)} species, {len(short)} shortened names, "
          f"{trimmed} dex entries trimmed to fit four lines")

    if not args.write:
        return 0

    NAMES_H.write_text(render_names(species), encoding="utf-8")
    INFO_H.write_text(render_info(species), encoding="utf-8")
    TEXT_H.write_text(render_text(species), encoding="utf-8")
    ENTRIES_H.write_text(render_entries(species), encoding="utf-8")
    ORDERS_H.write_text(render_orders(species), encoding="utf-8")
    national, hoenn, order = render_dex_numbers(species)
    TO_NATIONAL_H.write_text(national, encoding="utf-8")
    TO_HOENN_H.write_text(hoenn, encoding="utf-8")
    HOENN_TO_NATIONAL_H.write_text(order, encoding="utf-8")
    for path in (NAMES_H, INFO_H, TEXT_H, ENTRIES_H, ORDERS_H,
                 TO_NATIONAL_H, TO_HOENN_H, HOENN_TO_NATIONAL_H):
        print(f"wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
