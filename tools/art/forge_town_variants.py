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
import repaint_tileset_palettes as repaint  # noqa: E402
from map_invariants import TownMap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANIFEST = os.path.join(ROOT, "data/tilesets/arauna_variants.json")
ANIMS = os.path.join(ROOT, "src/tileset_anims.c")

TILES_PER_ROW = 16
NUM_TILES_IN_PRIMARY = 512
NUM_METATILES_IN_PRIMARY = 512
SECONDARY_CAPACITY = 512
NUM_PALS_IN_PRIMARY = 6
NUM_PALS_TOTAL = 13

# Everything Emerald draws in green, in the one palette it draws it from:
# four entries for the grass underfoot, C to F, and four for the leaves above
# it, 1 to 4. The first version of this took three of the eight, and a town
# came back re-greened from the ankles down with Emerald's own trees standing
# in it.
GRASS_PALETTE = 2
GRASS_INDICES = (0xC, 0xD, 0xE, 0xF)
LEAF_INDICES = (0x1, 0x2, 0x3, 0x4)
GREEN_INDICES = set(GRASS_INDICES) | set(LEAF_INDICES)

# The eight greens each biome is drawn in, lightest to darkest, grass first and
# leaves second.
#
# Re-indexing pixels onto other entries of Emerald's own palette - which is
# what this did before - can only ever reach colours Emerald already mixed,
# and Emerald mixed one green world. Six biomes squeezed into those eight
# entries came back looking like six shades of the same place. A secondary
# tileset has palettes of its own, though, and every one of Arauna's has at
# least one nobody is using. Claim it, fill it with a copy of the palette the
# greenery is already drawn in, and repaint only these eight entries: any tile
# that pointed at Emerald's palette renders identically under it except for
# what was green. Nothing is re-indexed and no tile is copied - a block's
# variant is the same tiles pointing at a different palette.
BIOME_GREENS = {
    # Mata Atlantica: humid and saturated, a canopy several shades deeper than
    # the clearing it stands around.
    "MATA": {
        "grass": [(148, 208, 112), (96, 176, 84), (52, 136, 58), (28, 96, 44)],
        "leaves": [(124, 220, 140), (60, 168, 104), (28, 112, 68), (16, 68, 44)],
    },
    # Cerrado: straw underfoot, bleached almost to yellow, with dark olive
    # foliage standing sparsely in it.
    "CERRADO": {
        "grass": [(224, 224, 144), (188, 192, 104), (148, 152, 68), (108, 112, 48)],
        "leaves": [(176, 188, 92), (124, 140, 56), (84, 96, 40), (52, 58, 26)],
    },
    # Pampa: open country, pale and cool, more sage than green.
    "PAMPA": {
        "grass": [(204, 226, 188), (164, 200, 152), (124, 166, 118), (88, 130, 92)],
        "leaves": [(160, 200, 158), (112, 158, 120), (72, 118, 90), (46, 80, 62)],
    },
    # Mata de araucaria: highland, cold, blue-green, the darkest of the six.
    "ARAUCARIA": {
        "grass": [(146, 198, 182), (100, 160, 148), (62, 120, 112), (38, 86, 82)],
        "leaves": [(76, 164, 156), (36, 118, 116), (18, 80, 80), (10, 50, 52)],
    },
    # Caatinga: the sertao. Grey-khaki, dusty, sun-bleached, barely green.
    "CAATINGA": {
        "grass": [(228, 214, 176), (194, 178, 140), (154, 140, 106), (114, 102, 74)],
        "leaves": [(176, 182, 140), (132, 140, 102), (92, 98, 70), (60, 64, 46)],
    },
    # Manguezal: brackish and muddy, dark green with the tide in it.
    "MANGUE": {
        "grass": [(140, 172, 120), (98, 132, 88), (64, 96, 62), (40, 64, 42)],
        "leaves": [(96, 140, 86), (56, 102, 62), (32, 70, 46), (18, 44, 30)],
    },
}


def biome_palette(biome):
    """This biome's greens, as {palette entry: colour}."""
    spec = BIOME_GREENS[biome]
    out = {}
    for indices, key in ((GRASS_INDICES, "grass"), (LEAF_INDICES, "leaves")):
        for index, colour in zip(indices, spec[key]):
            out[index] = repaint.quantise(colour)
    return out


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


SECONDARY_PALETTES = range(NUM_PALS_IN_PRIMARY, NUM_PALS_TOTAL)


def busy_palettes(tileset, live_blocks):
    """Which of a secondary tileset's own palettes something is drawn in.

    Only blocks that are actually spoken for count. A palette nothing live
    points at is dead space of exactly the same kind as an unused block slot,
    and it is what makes a biome's own colours possible at all.
    """
    busy = set()
    for index in sorted(live_blocks):
        if index >= tileset.block_count:
            continue
        for entry in tileset.entries(index):
            if entry & 0x03FF:
                busy.add((entry >> 12) & 0x0F)
    return busy


def claim_palette(tileset, biome, manifest, live_blocks, dry_run=False):
    """A palette slot of this tileset's own, filled with the biome's greens.

    Returns the slot, or None when every palette this tileset owns is spoken
    for - two towns of different biomes sharing one tileset can want two, and
    gTileset_Mauville has one to give. The second one falls back to re-indexing
    onto Emerald's palette, which is a smaller change but not no change.
    """
    palettes = manifest.setdefault("palettes", {})
    key = "%s|%s" % (tileset.symbol, biome)
    if key in palettes:
        return palettes[key]
    mine = {v for k, v in palettes.items() if k.startswith(tileset.symbol + "|")}
    taken = busy_palettes(tileset, live_blocks) | mine
    free = [p for p in SECONDARY_PALETTES if p not in taken]
    if not free:
        return None
    slot = free[0]
    path = os.path.join(tileset.dir, "palettes", "%02d.pal" % slot)
    colours = repaint.read_palette(os.path.join(
        ROOT, "data/tilesets/primary/general/palettes/%02d.pal" % GRASS_PALETTE))
    for index, colour in biome_palette(biome).items():
        colours[index] = colour
    if not dry_run:
        repaint.write_palette(path, colours)
    palettes[key] = slot
    return slot


class Forge:
    def __init__(self, town, biome, manifest, baseline="HEAD", dry_run=False):
        self.town = town
        self.biome = biome
        self.manifest = manifest
        self.primary = Tileset(town.layout["primary_tileset"], secondary=False)
        self.secondary = Tileset(town.layout["secondary_tileset"], secondary=True)

        used_blocks = live_secondary(self.secondary.symbol, baseline)
        self.palette = claim_palette(self.secondary, biome, manifest, used_blocks, dry_run)
        if self.palette is None:
            # No palette left: re-index onto Emerald's own, which needs the
            # biome to have a ramp written for it.
            if biome not in forge.MATERIALS:
                raise SystemExit("%s has no free palette for %s and no ramp to fall back on"
                                 % (self.secondary.symbol, biome))
            self.ramp = biome_ramp(biome)
            spec = forge.MATERIALS[biome]
            # The lawn a ramp biome may already have was forged out of the same
            # palette and landed in the range the leaf ramp reads from, so
            # running the ramp over it would darken it twice.
            self.forged_blocks = set(spec["metatiles"])
            self.forged_tiles = set(spec["tiles"])
        else:
            self.ramp = None
            self.forged_blocks = set()
            self.forged_tiles = set()

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
            if set(self.tile_pixels(tile_id)) & GREEN_INDICES:
                return True
        return False

    def greenery(self, entry):
        """Is this entry of a block drawing something green?"""
        tile_id, palette = entry & 0x03FF, (entry >> 12) & 0x0F
        return (bool(tile_id) and palette == GRASS_PALETTE
                and tile_id not in self.forged_tiles
                and bool(set(self.tile_pixels(tile_id)) & GREEN_INDICES))

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
            if not self.greenery(entry):
                rebuilt.append(entry)
            elif self.palette is not None:
                # Same tile, this biome's palette. Bits 12-15 are the palette,
                # 10 and 11 the flips, 0-9 the tile.
                rebuilt.append((entry & 0x0FFF) | (self.palette << 12))
            else:
                slot = self.variant_tile(entry & 0x03FF)
                rebuilt.append((entry & 0xFC00) | (NUM_TILES_IN_PRIMARY + slot))
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


# Emerald's plain grass, in the tileset every outdoor map shares.
PLAIN_LAWN = 0x001


def town_lawn(city, manifest=None):
    """The block this town lays as plain, open lawn.

    Every tool that has to put ground back where something used to stand needs
    this: the mover filling a footprint, the replanner deciding what a grove
    may stand on. It used to be the biome's forged material, named straight
    out of `forge_arauna_tiles`. It cannot be any more, because a town wearing
    a palette of its own does not need a forged lawn at all - Emerald's own
    grass block, pointed at the biome's palette, *is* the biome's lawn.
    """
    town = TownMap(city, ROOT)
    biome = biome_of(city)
    if not biome:
        return None
    manifest = manifest if manifest is not None else load_manifest()
    key = "%s|%s|%d" % (town.layout["secondary_tileset"], biome, PLAIN_LAWN)
    slot = manifest["blocks"].get(key)
    return PLAIN_LAWN if slot is None else NUM_METATILES_IN_PRIMARY + slot


def dress(city, dry_run=False, manifest=None, baseline="HEAD"):
    biome = biome_of(city)
    if not biome:
        return None
    town = TownMap(city, ROOT)
    manifest = manifest if manifest is not None else load_manifest()
    smith = Forge(town, biome, manifest, baseline, dry_run)
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
            "palette": smith.palette, "slots_left": len(smith.free_blocks)}


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
            print("%-16s %-10s %s  %3d block kinds redressed%s, %3d slots left"
                  % (r["city"], r["biome"],
                     "palette %2d" % r["palette"] if r["palette"] is not None
                     else "on the ramp",
                     r["blocks"],
                     "" if not r["short"] else ", %d SHORT" % r["short"],
                     r["slots_left"]))
    if not args.report:
        save_manifest(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
