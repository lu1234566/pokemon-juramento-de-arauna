#!/usr/bin/env python3
"""Give each Arauna creature a voice that fits its body.

Every creature still cries with the voice of whatever used to live in its engine
slot, so Caramelo the street dog clucks like a Torchic. There is no original
audio to import, but the cry table controls two things and both are usable:
which sample plays, and at what pitch.

Sample. A cry's character follows the body, not the battle stats, so the donor
is chosen by the vanilla Pokemon whose primary type matches the creature's and
whose weight is closest to it. A bird gets a bird, a big snake gets something
heavy.

Pitch. The `cry` macro's second byte is the key the sample plays at, 60 by
default, and nothing in the engine cares what it is. So a creature heavier than
its donor speaks lower and a lighter one higher, four semitones per doubling,
clamped to an octave either way. That matters more than it sounds: 386 creatures
draw on far fewer than 386 vanilla voices, so without pitch a lot of them would
be indistinguishable. Where two still land on the same sample at the same key,
the lighter one is nudged up a semitone until they separate.

This does not make the cries original. It makes them stop being wrong.

  --check   report the reassignment
  --write   rewrite sound/cry_tables.inc
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# The tree before the dex landed, where the tables still describe vanilla.
VANILLA = "d4804fcc^"
EXPORT = ROOT / "graphics/arauna/arauna_sprites_gba_export.zip"
MAPPING = ROOT / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv"
CRIES = ROOT / "sound/cry_tables.inc"
MACROS = ROOT / "asm/macros/music_voice.inc"
ROSTER = ROOT / "docs/arauna/ARAUNA_CRIES.csv"

DEFAULT_KEY = 60
MAX_SHIFT = 12          # an octave either way
LOWEST, HIGHEST = 48, 76  # past this a resampled cry stops sounding like one
SEMITONES_PER_DOUBLING = 4


def at_vanilla(path: str) -> str:
    return subprocess.run(["git", "show", f"{VANILLA}:{path}"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout


def vanilla_bodies() -> dict[str, dict]:
    """Every vanilla species' primary type and weight, as the engine had them."""
    info = at_vanilla("src/data/pokemon/species_info.h")
    types = {}
    for block in re.finditer(r"^    \[(SPECIES_\w+)\] =\n    \{\n(.*?)\n    \},?$",
                             info, re.S | re.M):
        found = re.search(r"\.types = \{\s*(TYPE_\w+),", block.group(2))
        if found:
            types[block.group(1)] = found.group(1)[len("TYPE_"):].lower()

    entries = at_vanilla("src/data/pokemon/pokedex_entries.h")
    weights = {}
    for block in re.finditer(r"\[NATIONAL_DEX_(\w+)\] =\s*\{.*?\.weight = (\d+),",
                             entries, re.S):
        weights[f"SPECIES_{block.group(1)}"] = int(block.group(2))

    return {name: {"type": kind, "weight": max(1, weights.get(name, 100))}
            for name, kind in types.items() if name in weights}


def arauna_bodies() -> dict[str, dict]:
    with zipfile.ZipFile(EXPORT) as zf:
        mons = {m["id"]: m for m in json.loads(zf.read("pokedex.json"))["pokemon"]}
    out = {}
    for row in csv.DictReader(MAPPING.open(encoding="utf-8")):
        mon = mons[int(row["arauna_dex"])]
        out[row["species_constant"]] = {
            "dex": int(row["arauna_dex"]), "name": mon["name"],
            "type": mon["types"][0],
            "weight": max(1, int(round(mon["weight"] * 10))),  # hectograms
        }
    return out


def constant(cry_symbol: str) -> str:
    """Cry_Nidoranm -> SPECIES_NIDORAN_M, and the rest by upper-casing."""
    name = cry_symbol[len("Cry_"):]
    special = {"Nidoranm": "NIDORAN_M", "Nidoranf": "NIDORAN_F",
               "Hooh": "HO_OH", "Mrmime": "MR_MIME", "Farfetchd": "FARFETCHD"}
    if name in special:
        return f"SPECIES_{special[name]}"
    return "SPECIES_" + re.sub(r"(?<!^)(?=[A-Z])", "_", name).upper()


def pitch(creature_weight: int, donor_weight: int) -> int:
    """Heavier than the donor speaks lower, a semitone per doubling."""
    shift = -SEMITONES_PER_DOUBLING * math.log2(creature_weight / donor_weight)
    return DEFAULT_KEY + max(-MAX_SHIFT, min(MAX_SHIFT, int(round(shift))))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    vanilla = vanilla_bodies()
    creatures = arauna_bodies()
    source = at_vanilla("sound/cry_tables.inc")

    by_type = {}
    for name, body in vanilla.items():
        by_type.setdefault(body["type"], []).append(name)

    rows, unmatched, retuned = [], 0, 0
    lines, voice_lines = [], {}
    for line in source.splitlines():
        found = re.match(r"^\t(cry|cry_reverse) (Cry_\w+)$", line)
        if not found:
            lines.append(line)
            continue
        slot = constant(found.group(2))
        creature = creatures.get(slot)
        if not creature or slot not in vanilla:
            lines.append(line)
            unmatched += 1
            continue

        pool = by_type.get(creature["type"]) or list(vanilla)
        donor = min(pool, key=lambda n: (abs(math.log2(vanilla[n]["weight"]
                                                       / creature["weight"])), n))
        key = pitch(creature["weight"], vanilla[donor]["weight"])
        symbol = "Cry_" + "".join(part.capitalize()
                                  for part in donor[len("SPECIES_"):].split("_"))
        lines.append(f"\t{found.group(1)}_pitched {symbol}, {key}")
        if key != DEFAULT_KEY:
            retuned += 1
        rows.append({"arauna_dex": f"{creature['dex']:03d}", "name": creature["name"],
                     "type": creature["type"], "weight_hg": creature["weight"],
                     "donor": donor[len("SPECIES_"):], "key": key})
        voice_lines.setdefault((symbol, key), []).append(len(lines) - 1)

    # Two creatures on the same sample at the same key are the same voice. Walk
    # the collisions and step the later ones up a semitone until they part.
    nudged, used = 0, set()
    for (symbol, key), where in sorted(voice_lines.items()):
        used.add((symbol, key))
        for index in where[1:]:
            # Alternate up and down around the fitted key so the nudge stays as
            # close to the size-correct pitch as possible, and never leaves a
            # range a GBA sample still sounds like itself in.
            for offset in (o for step in range(1, MAX_SHIFT + 1) for o in (step, -step)):
                step_key = key + offset
                if not LOWEST <= step_key <= HIGHEST or (symbol, step_key) in used:
                    continue
                used.add((symbol, step_key))
                lines[index] = re.sub(r", \d+$", f", {step_key}", lines[index])
                nudged += 1
                break
    for row, line in zip(rows, [l for l in lines if "_pitched" in l]):
        row["key"] = int(line.rsplit(",", 1)[1])

    print(f"{len(rows)} cries reassigned, {retuned} of them re-pitched, "
          f"{unmatched} lines left alone")
    voices = len({(r["donor"], r["key"]) for r in rows})
    print(f"  {len({r['donor'] for r in rows})} donor samples, {voices} distinct "
          f"voices for {len(rows)} entries ({nudged} nudged apart)")
    for row in rows[:8]:
        print(f"  #{row['arauna_dex']} {row['name']:18} {row['type']:9} "
              f"{row['weight_hg']:5} hg -> {row['donor']:12} key {row['key']}")

    if not args.write:
        return 0

    macros = MACROS.read_text(encoding="utf-8")
    if "cry_pitched" not in macros:
        macros = macros.replace("""	.macro cry_reverse sample:req""",
"""	@ Same as cry, but the sample plays at an explicit key instead of 60.
	@ Nothing in the engine reads this byte for anything else, so it is free to
	@ tell two creatures sharing a sample apart by size.
	.macro cry_pitched sample:req, key=60
	.byte 0x20, \\key, 0, 0
	.4byte \\sample
	.byte 0xff, 0, 0xff, 0
	.endm

	.macro cry_reverse_pitched sample:req, key=60
	.byte 0x30, \\key, 0, 0
	.4byte \\sample
	.byte 0xff, 0, 0xff, 0
	.endm

	.macro cry_reverse sample:req""", 1)
        MACROS.write_text(macros, encoding="utf-8")

    CRIES.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with ROSTER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nwrote {CRIES.relative_to(ROOT)} and {ROSTER.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
