#!/usr/bin/env python3
"""Say what a .gba actually is, before anyone spends an evening testing it.

A built ROM carries no version number, and two of them look identical in a file
listing. The one thing worse than a bug is an hour of manual testing spent on a
build from last week - every note taken against it is about a game that no
longer exists.

So this reads a ROM and reports what is *in* it, by looking for things this
working tree knows how to describe: the header the Makefile stamps, the species
names in `src/data/text/species_names.h`, the settlement names in the region
map, the palettes `repaint_tileset_palettes.py` and `forge_town_variants.py`
write. Every marker is read out of the source rather than written down here, so
the tool cannot drift from the repository it lives in.

    python3 tools/audit/rom_id.py some_build.gba
    python3 tools/audit/rom_id.py a.gba b.gba      # and how they differ
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "art"))

ROOT = pathlib.Path(__file__).resolve().parents[2]
BUILT = ROOT / "pokemon-juramento-de-arauna-en_modern.gba"


def charmap():
    """The game's own text encoding, read from charmap.txt."""
    table = {}
    for line in (ROOT / "charmap.txt").read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"^'(.)'\s*=\s*([0-9A-Fa-f]{2})\s*$", line)
        if m:
            table.setdefault(m.group(1), int(m.group(2), 16))
    return table


def encode(text, table):
    try:
        return bytes(table[ch] for ch in text)
    except KeyError:
        return None


def gba_palette(colours):
    """A run of colours as the hardware stores them: five bits a channel."""
    return b"".join(struct.pack("<H", (r >> 3) | ((g >> 3) << 5) | ((b >> 3) << 10))
                    for r, g, b in colours)


def markers():
    """Things to look for, each with the commit-era it belongs to."""
    table = charmap()
    out = []

    names = (ROOT / "src/data/text/species_names.h").read_text(encoding="utf-8", errors="replace")
    for species in re.findall(r'_\("([A-Za-z ]{3,10})"\)', names)[1:4]:
        sig = encode(species, table)
        if sig:
            out.append(("the Arauna species names", "%r" % species, sig))
            break

    sections = json.loads((ROOT / "src/data/region_map/region_map_sections.json")
                          .read_text(encoding="utf-8", errors="replace"))
    rows = sections.get("map_sections") or sections
    for row in (rows if isinstance(rows, list) else rows["map_sections"]):
        name = row.get("name") or ""
        if name.startswith("VILA "):
            sig = encode(name, table)
            if sig:
                out.append(("the Arauna place names", "%r" % name, sig))
                break

    try:
        import repaint_tileset_palettes as repaint
        for tileset, plan in repaint.REPAINTS.items():
            for index, entries in plan.items():
                colours = [repaint.quantise(c) for _, c in sorted(entries.items())]
                out.append(("the colonial repaint",
                            "%s palette %d" % (tileset, index), gba_palette(colours)))
                break
            break
    except Exception:                                        # noqa: BLE001
        pass

    try:
        import forge_town_variants as forge
        for biome, spec in sorted(forge.BIOME_GREENS.items()):
            colours = [forge.repaint.quantise(c) for c in spec["grass"]]
            out.append(("the biome palettes", "%s grass" % biome, gba_palette(colours)))
    except Exception:                                        # noqa: BLE001
        pass

    return out


def header(rom):
    title = rom[0xA0:0xAC].decode("ascii", "replace").rstrip("\x00")
    code = rom[0xAC:0xB0].decode("ascii", "replace")
    checksum = (-(0x19 + sum(rom[0xA0:0xBD]))) & 0xFF
    return title, code, checksum == rom[0xBD]


def wanted_title():
    for line in (ROOT / "Makefile").read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"\s*TITLE\s*:?=\s*(\S+)", line)
        if m:
            return m.group(1)
    return None


def describe(path, found_markers):
    rom = pathlib.Path(path).read_bytes()
    title, code, ok = header(rom)
    print("%s  %.1f MiB" % (path, len(rom) / (1 << 20)))
    expected = wanted_title()
    verdict = "" if expected is None or title == expected \
        else "   <- the Makefile stamps %r; this was built somewhere else" % expected
    print("  header      title=%r code=%r checksum=%s%s"
          % (title, code, "ok" if ok else "BAD", verdict))
    seen = {}
    for era, what, sig in found_markers:
        seen.setdefault(era, []).append((what, rom.find(sig) >= 0))
    for era, rows in seen.items():
        have = sum(1 for _, present in rows if present)
        print("  %-22s %d of %d present%s"
              % (era, have, len(rows),
                 "" if have == len(rows) else
                 "   missing: " + ", ".join(w for w, p in rows if not p)))
    return rom


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roms", nargs="+")
    args = ap.parse_args()
    found = markers()
    if not found:
        print("no markers could be read from this working tree", file=sys.stderr)
        return 2
    roms = []
    for path in args.roms:
        roms.append(describe(path, found))
        print()
    if BUILT.is_file() and str(BUILT) not in args.roms:
        print("against this tree's own build:")
        roms.append(describe(str(BUILT), found))
        print()
    for i in range(len(roms) - 1):
        a, b = roms[i], roms[-1]
        if len(a) != len(b):
            print("  sizes differ, so they are not the same build")
            continue
        pages = sum(1 for at in range(0, len(a), 4096) if a[at:at + 4096] != b[at:at + 4096])
        print("  %s vs %s: %d of %d 4KB pages differ"
              % (os.path.basename(args.roms[i]), BUILT.name if len(roms) > len(args.roms)
                 else os.path.basename(args.roms[-1]), pages, len(a) // 4096))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
