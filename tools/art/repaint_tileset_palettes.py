#!/usr/bin/env python3
"""Repaint a tileset's own palettes, where that tileset belongs to one region.

Re-indexing pixels onto a ramp the artists already mixed keeps a material in
Emerald's world of colour. Sometimes that is not what is wanted: Arauna's
architecture is not Hoenn's, and no ramp Emerald mixed is a whitewashed wall
with a blue trim under a terracotta roof.

A palette can simply be rewritten when the tileset that owns it is only loaded
by maps that all want the change. `gTileset_Petalburg` is loaded by VILA
AMANHECER, VILA DA PASSAGEM, PAMPA DA ESPERA and the three routes between them,
and nothing else, so its building palettes are a regional decision rather than a
global one.

Rewriting a palette in place is also the only way to keep a door honest. A door
is matched to its opening animation by metatile id, and the animation is drawn
with a palette index taken from the tileset - so a door block cannot be swapped
for a recoloured variant without the animation falling out of step with it, but
it follows a repainted palette by itself.

Every colour is quantised to the 5 bits per channel the GBA actually stores, so
nothing here can specify a colour the hardware would round to something else.

    python3 tools/art/repaint_tileset_palettes.py --check
    python3 tools/art/repaint_tileset_palettes.py
"""
from __future__ import annotations

import argparse
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# What the hardware can hold: 5 bits a channel, as the decompilation writes it.
LEVELS = [(v * 255) // 31 for v in range(32)]


def quantise(colour):
    return tuple(min(LEVELS, key=lambda level: abs(level - channel)) for channel in colour)


REPAINTS = {
    "secondary/petalburg": {
        # Roof: Hoenn's straw and tan become the terracotta of a colonial tile
        # roof. The ridge greys and the sky blues are left where they are.
        10: {
            0xB: (255, 197, 148),
            0xC: (222, 131, 90),
            0xD: (172, 82, 66),
            0xE: (115, 49, 49),
        },
        # Wall: whitewash, and the beige woodwork becomes the blue trim that
        # goes with it. Door and window frames are drawn from this ramp.
        6: {
            0x2: (246, 246, 238),
            0x3: (230, 230, 213),
            0x4: (205, 205, 189),
            0xB: (180, 213, 230),
            0xC: (106, 164, 205),
            0xD: (57, 106, 156),
            0xE: (33, 66, 115),
        },
    },
}


def read_palette(path):
    lines = open(path, encoding="utf-8", errors="replace").read().split()
    numbers = [int(v) for v in lines if v.isdigit()]
    colours = [tuple(numbers[i:i + 3]) for i in range(2, len(numbers), 3)][:16]
    while len(colours) < 16:
        colours.append((0, 0, 0))
    return colours


def write_palette(path, colours):
    # .gitattributes marks *.pal as CRLF; JASC-PAL is a DOS format.
    with open(path, "w", encoding="utf-8", newline="\r\n") as handle:
        handle.write("JASC-PAL\n0100\n16\n")
        for colour in colours:
            handle.write("%d %d %d\n" % colour)


def repaint(tileset, plan, check_only):
    out = []
    for index, changes in plan.items():
        path = os.path.join(ROOT, "data/tilesets", tileset, "palettes", "%02d.pal" % index)
        if not os.path.exists(path):
            raise SystemExit("no palette %02d in %s" % (index, tileset))
        colours = read_palette(path)
        touched = 0
        for slot, colour in changes.items():
            wanted = quantise(colour)
            if colours[slot] != wanted:
                colours[slot] = wanted
                touched += 1
        if touched and not check_only:
            write_palette(path, colours)
        out.append((index, touched, len(changes)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    for tileset, plan in REPAINTS.items():
        for index, touched, total in repaint(tileset, plan, args.check):
            print("%-22s palette %2d: %d of %d entries %s"
                  % (tileset, index, touched, total, "differ" if args.check else "repainted"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
