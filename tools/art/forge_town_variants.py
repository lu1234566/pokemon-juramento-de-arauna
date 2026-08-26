#!/usr/bin/env python3
"""Carry a town's biome into every block that still shows Emerald's green.

Relaying a lawn only reaches the blocks that are nothing but lawn. Emerald
draws grass inside a great many other blocks too - between the crowns of a
tree line, in the strip at the foot of a house, under a flowerbed's petals -
and those keep the old mint however the lawn around them is repainted, which
is what makes a restyled town read as patched rather than designed.

The primary tileset has no room to fix that: one free tile. Each town's
secondary tileset does, once dead space is counted properly - the tiles no
live block draws, minus the ranges the animation code rewrites in VRAM. So the
fix goes there. For each block a town lays that draws palette 2's grass ramp,
this forges a variant into that town's own secondary tileset: the tiles that
carry grass are copied across with only their grass indices re-indexed onto
the biome's ramp, every other tile of the block is referenced exactly as it
is, and the variant block inherits the original's attributes wholesale, so its
behaviour and layer type cannot drift.

Nothing about the map's physics changes: only which block id each cell holds,
and every variant answers the behaviour question the same way its source did.

    python3 tools/art/forge_town_variants.py --report
    python3 tools/art/forge_town_variants.py --all
"""
from __future__ import annotations

import argparse
import json
import os
import re
import struct
import subprocess
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audit"))

import forge_arauna_tiles as forge  # noqa: E402
from map_invariants import TownMap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANIFEST = os.path.join(ROOT, "data/tilesets/arauna_variants.json")
ANIMS = os.path.join(ROOT, "src/tileset_anims.c")

TILES_PER_ROW = 16
NUM_TILES_IN_PRIMARY = 512
NUM_METATILES_IN_PRIMARY = 512
SECONDARY_CAPACITY = 512

# Everything Emerald draws in green, in the one palette it draws it from:
# three entries for the grass underfoot and four for the leaves above it. The
# first version of this took only the grass, and a town came back re-greened
# from the ankles down with Emerald's own trees still standing in it.
GRASS_PALETTE = 2


def biome_ramp(biome):
    spec = forge.MATERIALS[biome]
    return {**spec["recolour"], **spec.get("foliage", {})}


class OutOfRoom(Exception):
    """A tileset ran out of dead space part-way through a town."""


def slug(symbol):
    name = symbol.replace("gTileset_", "")
    return "".join(("_" if c.isupper() and i else "") + c.lower() for i, c in enumerate(name))


def animated_tiles(symbol):
    """Tiles of a secondary tileset the animation code rewrites every few frames."""
    name = symbol.replace("gTileset_", "")
    text = open(ANIMS, encoding="utf-8").read()
    out, current = set(), None
    for line in text.splitlines():
        m = re.search(r"QueueAnimTiles_(\w+?)_\w+\(", line)
        if m:
            current = m.group(1)
        if current != name:
            continue
        m = re.search(r"NUM_TILES_IN_PRIMARY \+ (\d+)\)\)\s*,\s*(\d+) \* TILE_SIZE_4BPP", line)
        if m:
            out.update(range(int(m.group(1)), int(m.group(1)) + int(m.group(2))))
        elif re.search(r"NUM_TILES_IN_PRIMARY \+ (\d+)\s*\+", line):
            # An offset the code computes at runtime; claim a generous block.
            start = int(re.search(r"NUM_TILES_IN_PRIMARY \+ (\d+)", line).group(1))
            out.update(range(start, start + 64))
    return out


class Sheet:
    """A tileset's 4bpp tile sheet, growable up to the hardware's window."""

    def __init__(self, path):
        self.path = path
        self.image = Image.open(path)
        if self.image.mode != "P":
            raise SystemExit("%s is not an indexed image" % path)
        self.palette = self.image.getpalette()
        self.px = self.image.load()

    @property
    def count(self):
        return (self.image.width // 8) * (self.image.height // 8)

    def grow_to(self, tiles):
        rows = (tiles + TILES_PER_ROW - 1) // TILES_PER_ROW
        height = rows * 8
        if height <= self.image.height:
            return
        if rows * TILES_PER_ROW > SECONDARY_CAPACITY:
            raise SystemExit("%s: %d tiles exceeds the %d the hardware loads"
                             % (self.path, rows * TILES_PER_ROW, SECONDARY_CAPACITY))
        grown = Image.new("P", (self.image.width, height), 0)
        grown.putpalette(self.palette)
        grown.paste(self.image, (0, 0))
        self.image = grown
        self.px = self.image.load()

    def read(self, tile_id):
        ox, oy = (tile_id % TILES_PER_ROW) * 8, (tile_id // TILES_PER_ROW) * 8
        return [self.px[ox + x, oy + y] for y in range(8) for x in range(8)]

    def write(self, tile_id, pixels):
        self.grow_to(tile_id + 1)
        ox, oy = (tile_id % TILES_PER_ROW) * 8, (tile_id // TILES_PER_ROW) * 8
        for i, value in enumerate(pixels):
            self.px[ox + i % 8, oy + i // 8] = value

    def save(self):
        self.image.save(self.path)


class Tileset:
    def __init__(self, symbol, secondary):
        self.symbol = symbol
        self.dir = os.path.join(ROOT, "data/tilesets",
                                "secondary" if secondary else "primary", slug(symbol))
        self.secondary = secondary
        self.sheet = Sheet(os.path.join(self.dir, "tiles.png"))
        self.metatiles = bytearray(open(os.path.join(self.dir, "metatiles.bin"), "rb").read())
        self.attributes = bytearray(open(os.path.join(self.dir, "metatile_attributes.bin"), "rb").read())

    @property
    def block_count(self):
        return len(self.metatiles) // 16

    def entries(self, index):
        return list(struct.unpack("<8H", self.metatiles[index * 16:index * 16 + 16]))

    def set_block(self, index, entries, attribute):
        self.grow_blocks(index + 1)
        self.metatiles[index * 16:index * 16 + 16] = struct.pack("<8H", *entries)
        self.attributes[index * 2:index * 2 + 2] = attribute

    def grow_blocks(self, count):
        if count > SECONDARY_CAPACITY:
            raise SystemExit("%s: %d blocks exceeds the %d the hardware loads"
                             % (self.symbol, count, SECONDARY_CAPACITY))
        while self.block_count < count:
            self.metatiles.extend(b"\x00" * 16)
            self.attributes.extend(b"\x00\x00")

    def save(self):
        open(os.path.join(self.dir, "metatiles.bin"), "wb").write(self.metatiles)
        open(os.path.join(self.dir, "metatile_attributes.bin"), "wb").write(self.attributes)
        self.sheet.save()


def load_manifest():
    if os.path.exists(MANIFEST):
        return json.load(open(MANIFEST, encoding="utf-8"))
    return {"tiles": {}, "blocks": {}}


def save_manifest(manifest):
    json.dump(manifest, open(MANIFEST, "w", encoding="utf-8"), indent=1, sort_keys=True)


def live_secondary(symbol, baseline="HEAD"):
    """Which of a secondary tileset's blocks are spoken for.

    A block is spoken for if a map lays it now, if a map laid it in the
    baseline revision, or if a script names it by constant.

    The baseline matters because redressing a town frees the blocks it used to
    lay: substitute every cell that held one and it looks unused. Reusing it
    would then make the result depend on the order the towns were processed
    in, and would silently rewrite the meaning of a block id another map may
    still be laying. Blocks are only ever added to, never recycled.

    The baseline is the committed revision, except when the whole variant pass
    is being rebuilt from an earlier one: then every variant the current commit
    holds is about to stop existing, and treating those slots as spoken for
    reserves the tileset against itself. That is what `--rebase-from` is for -
    pass the revision the tilesets were reset to.

    Scripts matter because `setmetatile` addresses blocks that may appear in no
    map at all - the Wailmer that blocks Lilycove's shore, Sootopolis's gym
    doors. Overwriting one of those would break the script silently.
    """
    layouts = json.load(open(os.path.join(ROOT, "data/layouts/layouts.json"), encoding="utf-8"))["layouts"]
    blocks = set()
    for layout in layouts:
        if layout.get("secondary_tileset") != symbol:
            continue
        for key in ("blockdata_filepath", "border_filepath"):
            path = os.path.join(ROOT, layout.get(key) or "")
            if not layout.get(key) or not os.path.exists(path):
                continue
            blobs = [open(path, "rb").read()]
            try:
                blobs.append(subprocess.check_output(
                    ["git", "show", "%s:%s" % (baseline, layout[key])], cwd=ROOT,
                    stderr=subprocess.DEVNULL))
            except subprocess.CalledProcessError:
                pass
            for raw in blobs:
                for value in struct.unpack("<%dH" % (len(raw) // 2), raw):
                    if (value & 0x03FF) >= NUM_METATILES_IN_PRIMARY:
                        blocks.add((value & 0x03FF) - NUM_METATILES_IN_PRIMARY)
    # A block a theme names by number is spoken for too: recycling its slot
    # would silently change what that number means the next time a theme runs.
    import retheme_cities
    for theme in retheme_cities.THEMES.values():
        for block in theme.get("ground") or ():
            if block >= NUM_METATILES_IN_PRIMARY:
                blocks.add(block - NUM_METATILES_IN_PRIMARY)
    prefix = "METATILE_%s_" % symbol.replace("gTileset_", "")
    labels = os.path.join(ROOT, "include/constants/metatile_labels.h")
    for m in re.finditer(r"#define\s+(METATILE_\w+)\s+(0x[0-9A-Fa-f]+|\d+)",
                         open(labels, encoding="utf-8").read()):
        if m.group(1).startswith(prefix):
            value = int(m.group(2), 0)
            if value >= NUM_METATILES_IN_PRIMARY:
                blocks.add(value - NUM_METATILES_IN_PRIMARY)
    return blocks


def scripted_metatiles(city):
    """Coordinates a script rewrites by hand are left holding their own block."""
    path = os.path.join(ROOT, "data/maps/%s/scripts.inc" % city)
    if not os.path.exists(path):
        return set()
    out = set()
    for m in re.finditer(r"setmetatile\s+(\d+)\s*,\s*(\d+)", open(path, encoding="utf-8").read()):
        out.add((int(m.group(1)), int(m.group(2))))
    return out


class Forge:
    def __init__(self, town, biome, manifest, baseline="HEAD"):
        self.town = town
        self.biome = biome
        self.manifest = manifest
        self.ramp = biome_ramp(biome)
        self.greens = set(self.ramp)
        # The lawn this biome already has was forged out of the same palette,
        # and it landed in the range the canopy ramp reads from. Redressing it
        # would run the ramp over it a second time and take the town two
        # shades darker than it was drawn to be, so the material's own blocks
        # and tiles are off limits: they are already this biome's green.
        spec = forge.MATERIALS[biome]
        self.forged_blocks = set(spec["metatiles"])
        self.forged_tiles = set(spec["tiles"])
        self.primary = Tileset(town.layout["primary_tileset"], secondary=False)
        self.secondary = Tileset(town.layout["secondary_tileset"], secondary=True)

        used_blocks = live_secondary(self.secondary.symbol, baseline)
        claimed_blocks = {v for k, v in manifest["blocks"].items()
                          if k.startswith(self.secondary.symbol + "|")}
        self.free_blocks = [i for i in range(SECONDARY_CAPACITY)
                            if i not in used_blocks and i not in claimed_blocks]

        live_tiles = set(animated_tiles(self.secondary.symbol))
        for index in used_blocks:
            if index < self.secondary.block_count:
                for entry in self.secondary.entries(index):
                    if (entry & 0x03FF) >= NUM_TILES_IN_PRIMARY:
                        live_tiles.add((entry & 0x03FF) - NUM_TILES_IN_PRIMARY)
        claimed_tiles = {v for k, v in manifest["tiles"].items()
                         if k.startswith(self.secondary.symbol + "|")}
        self.free_tiles = [i for i in range(SECONDARY_CAPACITY)
                           if i not in live_tiles and i not in claimed_tiles]

    # -- reading a block wherever it lives ---------------------------------
    def owner(self, block):
        if block < NUM_METATILES_IN_PRIMARY:
            return self.primary, block
        return self.secondary, block - NUM_METATILES_IN_PRIMARY

    def tile_pixels(self, tile_id):
        if tile_id < NUM_TILES_IN_PRIMARY:
            return self.primary.sheet.read(tile_id)
        return self.secondary.sheet.read(tile_id - NUM_TILES_IN_PRIMARY)

    def wears_emerald_green(self, block):
        if block in self.forged_blocks:
            return False
        tileset, index = self.owner(block)
        if index >= tileset.block_count:
            return False
        for entry in tileset.entries(index):
            tile_id, palette = entry & 0x03FF, (entry >> 12) & 0x0F
            if not tile_id or palette != GRASS_PALETTE or tile_id in self.forged_tiles:
                continue
            if set(self.tile_pixels(tile_id)) & self.greens:
                return True
        return False

    # -- forging -----------------------------------------------------------
    def variant_tile(self, tile_id):
        key = "%s|%s|%d" % (self.secondary.symbol, self.biome, tile_id)
        if key in self.manifest["tiles"]:
            return self.manifest["tiles"][key]
        if not self.free_tiles:
            raise OutOfRoom("%s is out of tiles" % self.secondary.symbol)
        slot = self.free_tiles.pop(0)
        pixels = self.tile_pixels(tile_id)
        self.secondary.sheet.write(slot, [self.ramp.get(v, v) for v in pixels])
        self.manifest["tiles"][key] = slot
        return slot

    def variant_block(self, block):
        key = "%s|%s|%d" % (self.secondary.symbol, self.biome, block)
        if key in self.manifest["blocks"]:
            return NUM_METATILES_IN_PRIMARY + self.manifest["blocks"][key]
        tileset, index = self.owner(block)
        rebuilt = []
        for entry in tileset.entries(index):
            tile_id, palette = entry & 0x03FF, (entry >> 12) & 0x0F
            if (tile_id and palette == GRASS_PALETTE and tile_id not in self.forged_tiles
                    and set(self.tile_pixels(tile_id)) & self.greens):
                slot = self.variant_tile(tile_id)
                rebuilt.append((entry & 0xFC00) | (NUM_TILES_IN_PRIMARY + slot))
            else:
                rebuilt.append(entry)
        if not self.free_blocks:
            raise OutOfRoom("%s is out of blocks" % self.secondary.symbol)
        slot = self.free_blocks.pop(0)
        self.secondary.set_block(slot, rebuilt, tileset.attributes[index * 2:index * 2 + 2])
        self.manifest["blocks"][key] = slot
        return NUM_METATILES_IN_PRIMARY + slot


def border_path(town):
    rel = town.layout.get("border_filepath")
    return os.path.join(ROOT, rel) if rel else None


def read_border(town):
    path = border_path(town)
    if not path or not os.path.exists(path):
        return []
    raw = open(path, "rb").read()
    return list(struct.unpack("<%dH" % (len(raw) // 2), raw))


def biome_of(city):
    import retheme_cities
    theme = retheme_cities.THEMES.get(city) or {}
    return theme.get("biome")


def dress(city, dry_run=False, manifest=None, baseline="HEAD"):
    biome = biome_of(city)
    if not biome:
        return None
    town = TownMap(city, ROOT)
    manifest = manifest if manifest is not None else load_manifest()
    smith = Forge(town, biome, manifest, baseline)
    frozen = scripted_metatiles(city)

    # Redress the commonest blocks first: when a tileset's dead space runs out
    # part-way, the green that is left over should be the green fewest cells
    # are showing, not whichever block the scan happened to reach last.
    tally = {}
    for y in range(town.h):
        for x in range(town.w):
            if (x, y) not in frozen:
                tally[town.metatile(x, y)] = tally.get(town.metatile(x, y), 0) + 1
    # The border is the strip the camera draws past the edge of the map, and
    # it is part of the town's own layout. Leaving it out framed every dark
    # green settlement in Emerald's bright green - most visibly in Vila
    # Amanhecer, where the forest the player's house now backs onto is the
    # border, and it was the only green in the shot that had not changed.
    border = read_border(town)
    for value in border:
        block = value & 0x03FF
        tally[block] = tally.get(block, 0) + 1
    wearing = [b for b in sorted(tally, key=lambda b: -tally[b]) if smith.wears_emerald_green(b)]

    variants, short = {}, []
    for block in wearing:
        try:
            variants[block] = smith.variant_block(block)
        except OutOfRoom as why:
            short = wearing[len(variants):]
            print("  %s: %s; %d block kind(s) keep the old green (%d cells)"
                  % (city, why, len(short), sum(tally[b] for b in short)))
            break

    for y in range(town.h):
        for x in range(town.w):
            if (x, y) in frozen:
                continue
            variant = variants.get(town.metatile(x, y))
            if variant is not None:
                # The variant carries the source block's attribute word
                # verbatim, so its behaviour and layer type are the source's by
                # construction; the gate re-checks it against the committed map.
                town.blocks[town.index(x, y)] = (town.blocks[town.index(x, y)] & 0xFC00) | variant

    border = [(value & 0xFC00) | variants.get(value & 0x03FF, value & 0x03FF)
              for value in border]

    dressed = len(variants)
    if not dry_run and dressed:
        open(town.path, "wb").write(struct.pack("<%dH" % len(town.blocks), *town.blocks))
        path = border_path(town)
        if path and border:
            open(path, "wb").write(struct.pack("<%dH" % len(border), *border))
        smith.secondary.save()
    return {"city": city, "biome": biome, "blocks": dressed, "short": len(short),
            "tiles_left": len(smith.free_tiles), "slots_left": len(smith.free_blocks)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("city", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--rebase-from", metavar="GIT_REF", default="HEAD",
                    help="the revision the tilesets were reset to, when the whole\n"
                         "variant pass is being rebuilt rather than extended")
    args = ap.parse_args()

    import retheme_cities
    cities = [c for c in retheme_cities.THEMES if retheme_cities.THEMES[c].get("biome")] \
        if (args.all or args.report) else [args.city]
    manifest = load_manifest()
    for city in cities:
        r = dress(city, dry_run=args.report, manifest=manifest,
                  baseline=args.rebase_from)
        if r:
            print("%-16s %-8s %3d block kinds redressed%s, %3d tiles / %3d slots left"
                  % (r["city"], r["biome"], r["blocks"],
                     "" if not r["short"] else ", %d SHORT" % r["short"],
                     r["tiles_left"], r["slots_left"]))
    if not args.report:
        save_manifest(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
