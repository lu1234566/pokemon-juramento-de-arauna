#!/usr/bin/env python3
"""Read the built ROM for names that belong to the game it was made from.

`check_arauna_static.sh` reports "Arauna canonical visible coverage: OK (16/16
stages; 100%)" and it is telling the truth about what it measures: the source
renderers. It never opens the ROM, and it says so - "compile step intentionally
skipped". So a name can be covered by a renderer, survive in a file the
renderer does not reach, and be read by a player anyway, with the gate green
the whole time.

This closes that loop the only way it can be closed: by looking at the bytes a
player's cartridge actually holds, through the game's own charmap.

    python3 tools/audit/check_rom_text.py
    python3 tools/audit/check_rom_text.py --list SLATEPORT
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
ROM = ROOT / "pokemon-juramento-de-arauna-en_modern.gba"

# Hoenn's settlements, its two teams and its corporation. Each of these has an
# Arauna name; anywhere one of them is still readable, a player is being told
# they are somewhere they are not.
HOENN = [
    "LITTLEROOT", "OLDALE", "PETALBURG", "RUSTBORO", "DEWFORD", "SLATEPORT",
    "MAUVILLE", "VERDANTURF", "FALLARBOR", "LAVARIDGE", "FORTREE", "LILYCOVE",
    "MOSSDEEP", "SOOTOPOLIS", "PACIFIDLOG", "EVER GRANDE", "HOENN",
    "DEVON", "AQUA", "MAGMA",
]

# Ordinary English that a raw byte search cannot tell from a faction name.
# AQUATIC is a Pokedex category - "the AQUATIC POKeMON" - and MAGMA ARMOR is an
# ability every game in the series ships. Counting them as Hoenn would make the
# number say something it does not mean, so they are named here, and what they
# account for is printed rather than quietly dropped.
INNOCENT = ("AQUATIC", "MAGMA ARMOR")


def charmap():
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


def occurrences(rom, needle):
    at, out = rom.find(needle), []
    while at >= 0:
        out.append(at)
        at = rom.find(needle, at + 1)
    return out


def context(rom, table, at, span=48):
    """The text around a hit, decoded as far as the charmap can take it."""
    back = {v: k for k, v in table.items()}
    start = max(0, at - span // 2)
    return "".join(back.get(b, "." if b else " ") for b in rom[start:at + span])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", default=str(ROM))
    ap.add_argument("--list", metavar="NAME", help="show the text around each hit for one name")
    args = ap.parse_args()
    path = pathlib.Path(args.rom)
    if not path.is_file():
        print("no ROM at %s - build one first" % path, file=sys.stderr)
        return 2
    rom = path.read_bytes()
    table = charmap()

    if args.list:
        needle = encode(args.list, table)
        for at in occurrences(rom, needle):
            print("  %06X  %s" % (at, context(rom, table, at)))
        return 0

    # Where each innocent word sits, so a hit inside one is not a hit.
    covered = set()
    for word in INNOCENT:
        needle = encode(word, table)
        if needle is None:
            continue
        for at in occurrences(rom, needle):
            covered.update(range(at, at + len(needle)))

    total, excused = 0, 0
    for name in HOENN:
        needle = encode(name, table)
        if needle is None:
            continue
        hits = occurrences(rom, needle)
        real = [at for at in hits if at not in covered]
        excused += len(hits) - len(real)
        if real:
            total += len(real)
            print("  %-12s %4d" % (name, len(real)))
    if excused:
        print("  (%d hit(s) inside %s, which are English and not Hoenn)"
              % (excused, " and ".join(INNOCENT)))
    print("%d readable mention(s) of Hoenn in the built ROM" % total)
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
