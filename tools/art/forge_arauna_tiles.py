#!/usr/bin/env python3
"""Forge new ground materials into the shared outdoor tileset.

The primary tileset every outdoor map loads is full: 512 of 512 tiles, 512 of
512 metatiles, and not one spare colour in any of its six palettes. Nothing can
be appended. What it does have is dead space — 64 metatiles no map references
and no script names, and a handful of tiles no live metatile draws — and that
space is free to take, because writing into it changes nothing that is on
screen today and does not move a single byte of the ROM's tileset budget.

So a new material is built the only way that space allows, and the only way
that guarantees it looks like Emerald: take a material the artists already drew
and re-index it onto a colour ramp they already mixed. Not a redraw. Every
pixel keeps its position, every dither keeps its pattern, every edge keeps its
shape; only which entry of which palette each pixel points at changes. A
material forged this way cannot drift out of style, because there is no step in
which anything is drawn.

TERRA is the packed red earth of Arauna's roads. It is Emerald's beach sand,
re-indexed from the sand ramp of palette 5 onto the rock ramp of palette 3 —
which happens to carry the identical grass green at entry F, so the material's
own edge tiles still meet a lawn exactly as the originals did.

    python3 tools/art/forge_arauna_tiles.py --check
    python3 tools/art/forge_arauna_tiles.py
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import struct

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GENERAL = os.path.join(ROOT, "data/tilesets/primary/general")
LABELS = os.path.join(ROOT, "include/constants/metatile_labels.h")

NUM_TILES = 512
NUM_METATILES = 512

# Tiles the animation code rewrites in VRAM every few frames. Art parked here
# would be overwritten on screen, so they are not free however unreferenced.
ANIMATED_TILES = (set(range(432, 462)) | set(range(464, 474))
                  | set(range(480, 490)) | set(range(496, 502)) | set(range(508, 512)))

MATERIALS = {
    # Arauna's biomes, as lawns. Emerald's grass is three entries of palette 2 -
    # a highlight speckle, a body and a shadow speckle - and that same palette
    # already carries two more three-step green ramps the artists mixed. So a
    # biome's lawn is the same two tiles of grass pointing at a different ramp.
    "MATA": {
        "source": [0x001, 0x1CE, 0x1CF],
        "palette": 2,
        "recolour": {0xC: 0x2, 0xD: 0x3, 0xE: 0x4},
        # Everything green in this palette that the lawn ramp above does not
        # reach: the four shades Emerald draws leaves with, 1-2-3-4, and F,
        # the grass ramp's deepest step, which no lawn block uses but every
        # tree block does - leaving it alone put a mint outline around every
        # tree in a re-greened town. Mata Atlantica: a dense canopy lit
        # blue-green at the top and going almost black beneath.
        "foliage": {0x1: 0xF, 0x2: 0x3, 0x3: 0x4, 0x4: 0x8, 0xF: 0x8},
        "tiles": [0x16D, 0x17D],
        "metatiles": [0x02A, 0x02E, 0x02F],
        "label": "Arauna_Mata",
    },
    "CERRADO": {
        "source": [0x001, 0x1CE, 0x1CF],
        "palette": 2,
        "recolour": {0xC: 0x1, 0xD: 0x2, 0xE: 0x3},
        # Cerrado: dark olive foliage over the bleached grass of the ramp
        # above. Sending the canopy's body to the grey-brown instead read as
        # dead wood rather than dry leaves, because the body is the largest
        # part of a tree - only the deepest shadow goes brown.
        "foliage": {0x1: 0x2, 0x2: 0x3, 0x3: 0x4, 0x4: 0x8, 0xF: 0x4},
        "tiles": [0x18A, 0x1F8],
        "metatiles": [0x035, 0x046, 0x05C],
        "label": "Arauna_Cerrado",
    },
    "PAMPA": {
        "source": [0x001, 0x1CE, 0x1CF],
        "palette": 2,
        "recolour": {0xC: 0x1, 0xD: 0xC, 0xE: 0xD},
        # Pampa: low scrub, cool and blue-green against the pale open grass.
        "foliage": {0x1: 0xD, 0x2: 0xE, 0x3: 0xF, 0x4: 0x4, 0xF: 0xE},
        "tiles": [0x1F9, 0x1FA],
        "metatiles": [0x07E, 0x07F, 0x097],
        "label": "Arauna_Pampa",
    },
    "TERRA": {
        "source": [0x118, 0x119, 0x11A, 0x120, 0x121, 0x122, 0x128, 0x129, 0x12A],
        "palette": 3,
        # Emerald's sand ramp -> Emerald's rock ramp, lightest to darkest, with
        # the grass green landing on the identical green.
        "recolour": {0xB: 0x9, 0xC: 0xA, 0xD: 0xB, 0xE: 0xC, 0xF: 0xF},
        "tiles": [0x1EA, 0x1EB, 0x1EC, 0x1ED, 0x1EE, 0x1EF, 0x1F6, 0x1F7],
        "metatiles": [0x0DB, 0x0DC, 0x0DD, 0x0DE, 0x0E3, 0x0E4, 0x0E5, 0x0E6, 0x0E7],
        "label": "Arauna_Terra",
    },
}


# -- what is genuinely free ------------------------------------------------
def live_metatiles():
    live = set()
    layouts = json.load(open(os.path.join(ROOT, "data/layouts/layouts.json"), encoding="utf-8"))["layouts"]
    for layout in layouts:
        for key in ("blockdata_filepath", "border_filepath"):
            path = os.path.join(ROOT, layout.get(key) or "")
            if not layout.get(key) or not os.path.exists(path):
                continue
            raw = open(path, "rb").read()
            for value in struct.unpack("<%dH" % (len(raw) // 2), raw):
                if (value & 0x03FF) < NUM_METATILES:
                    live.add(value & 0x03FF)
    # A block a script names by constant is spoken for even if no map lays it.
    for m in re.finditer(r"#define\s+METATILE_\w+\s+(0x[0-9A-Fa-f]+|\d+)",
                         open(LABELS, encoding="utf-8").read()):
        value = int(m.group(1), 0)
        if value < NUM_METATILES:
            live.add(value)
    return live


def live_tiles(metatiles, live_mt):
    live = set(ANIMATED_TILES)
    for mid in sorted(live_mt):
        for entry in struct.unpack("<8H", metatiles[mid * 16:mid * 16 + 16]):
            live.add(entry & 0x03FF)
    # A secondary tileset's blocks address the primary tileset's tiles too.
    secondary = os.path.join(ROOT, "data/tilesets/secondary")
    for name in sorted(os.listdir(secondary)):
        path = os.path.join(secondary, name, "metatiles.bin")
        if not os.path.exists(path):
            continue
        blob = open(path, "rb").read()
        for entry in struct.unpack("<%dH" % (len(blob) // 2), blob):
            if (entry & 0x03FF) < NUM_TILES:
                live.add(entry & 0x03FF)
    return live


# -- the tile sheet --------------------------------------------------------
class Sheet:
    def __init__(self, path):
        self.path = path
        self.image = Image.open(path)
        if self.image.mode != "P":
            raise SystemExit("%s is not an indexed image" % path)
        self.px = self.image.load()
        self.per_row = self.image.width // 8

    def origin(self, tile_id):
        return (tile_id % self.per_row) * 8, (tile_id // self.per_row) * 8

    def read(self, tile_id):
        ox, oy = self.origin(tile_id)
        return [self.px[ox + x, oy + y] for y in range(8) for x in range(8)]

    def write(self, tile_id, pixels):
        ox, oy = self.origin(tile_id)
        for i, value in enumerate(pixels):
            self.px[ox + i % 8, oy + i // 8] = value

    def save(self):
        self.image.save(self.path)


def forge(name, spec, check_only):
    metatiles = bytearray(open(os.path.join(GENERAL, "metatiles.bin"), "rb").read())
    attributes = bytearray(open(os.path.join(GENERAL, "metatile_attributes.bin"), "rb").read())
    sheet = Sheet(os.path.join(GENERAL, "tiles.png"))

    mine_mt = set(spec["metatiles"])
    mine_tiles = set(spec["tiles"])
    used_mt = live_metatiles() - mine_mt
    used_tiles = live_tiles(metatiles, used_mt) - mine_tiles

    taken_mt = sorted(mine_mt & used_mt)
    taken_tiles = sorted(mine_tiles & used_tiles)
    if taken_mt or taken_tiles:
        raise SystemExit("%s: slots are in use — blocks %s, tiles %s"
                         % (name, ["%03X" % v for v in taken_mt], ["%03X" % v for v in taken_tiles]))

    # Which source tile becomes which of ours, in first-seen order. Tile 0 is
    # the blank one an unused layer points at; it carries no art and is copied
    # through untouched. A tile the ramp does not cover is not part of the
    # material either - the shadow a tree casts across the grass, say - so it
    # is referenced exactly as it is rather than recoloured into nonsense.
    recolour = spec["recolour"]
    order, mapping = [], {}
    for mid in spec["source"]:
        for entry in struct.unpack("<8H", metatiles[mid * 16:mid * 16 + 16]):
            tile_id = entry & 0x03FF
            if not tile_id or tile_id in mapping:
                continue
            if not set(sheet.read(tile_id)) <= set(recolour):
                mapping[tile_id] = tile_id
                continue
            if len(order) >= len(spec["tiles"]):
                raise SystemExit("%s needs more than the %d tiles reserved"
                                 % (name, len(spec["tiles"])))
            mapping[tile_id] = spec["tiles"][len(order)]
            order.append(tile_id)
    for source, dest in mapping.items():
        if source == dest:
            continue
        sheet.write(dest, [recolour[v] for v in sheet.read(source)])

    for slot, mid in zip(spec["metatiles"], spec["source"]):
        entries = list(struct.unpack("<8H", metatiles[mid * 16:mid * 16 + 16]))
        rebuilt = []
        for entry in entries:
            if not (entry & 0x03FF):
                rebuilt.append(entry)
                continue
            flips = entry & 0x0C00
            rebuilt.append(mapping[entry & 0x03FF] | flips | (spec["palette"] << 12))
        metatiles[slot * 16:slot * 16 + 16] = struct.pack("<8H", *rebuilt)
        attributes[slot * 2:slot * 2 + 2] = attributes[mid * 2:mid * 2 + 2]

    if check_only:
        return {"material": name, "tiles": len(order), "blocks": len(spec["metatiles"]), "written": False}

    open(os.path.join(GENERAL, "metatiles.bin"), "wb").write(metatiles)
    open(os.path.join(GENERAL, "metatile_attributes.bin"), "wb").write(attributes)
    sheet.save()
    write_labels(name, spec)
    return {"material": name, "tiles": len(order), "blocks": len(spec["metatiles"]), "written": True}


def write_labels(name, spec):
    """Name the blocks in the header, so nothing later reads the slots as free."""
    text = open(LABELS, encoding="utf-8").read()
    marker = "// Arauna materials"
    block = [marker, "// Forged by tools/art/forge_arauna_tiles.py into blocks no map used.", ""]
    for i, mid in enumerate(spec["metatiles"]):
        block.append("#define METATILE_General_%s_%d 0x%03X" % (spec["label"], i, mid))
    block.append("")
    body = "\n".join(block)
    if marker in text:
        text = re.sub(re.escape(marker) + r".*?(?=\n#endif)", body.rstrip("\n") + "\n",
                      text, flags=re.S)
    else:
        text = text.replace("\n#endif", "\n" + body + "\n#endif")
    open(LABELS, "w", encoding="utf-8").write(text)


def substitution(name):
    """Which block of the source material each forged block stands in for.

    A forged material appears in no Emerald map, so its autotile table cannot
    be learned the way a real one's is. It does not have to be: block for
    block it is the source material, so the source's learned table maps
    straight through this.
    """
    spec = MATERIALS[name]
    return dict(zip(spec["source"], spec["metatiles"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report without writing")
    args = ap.parse_args()
    # Each material checks its slots against the map data, but not against its
    # siblings: two of them claiming one slot would only show up on screen.
    for field in ("tiles", "metatiles"):
        seen = {}
        for name, spec in MATERIALS.items():
            for slot in spec[field]:
                if slot in seen:
                    raise SystemExit("%s and %s both claim %s slot 0x%03X"
                                     % (seen[slot], name, field[:-1], slot))
                seen[slot] = name
    for name, spec in MATERIALS.items():
        r = forge(name, spec, args.check)
        print("%-6s %d tile(s), %d block(s) %s"
              % (r["material"], r["tiles"], r["blocks"], "checked" if args.check else "forged"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
