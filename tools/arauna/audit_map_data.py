#!/usr/bin/env python3
"""Look for the map-data faults that make a build crash while you just walk.

Nothing here is opinion: every check reads the same bytes the ROM does and
compares them against the bounds the engine assumes.

  1. warps, objects, signs and trigger tiles standing outside their own map.
     This is what a resized map leaves behind, and the player lands in it.
  2. metatile ids in map.bin and border.bin that no tileset actually defines.
     DrawMetatileAt only clamps ids past NUM_METATILES_TOTAL, so an id inside
     that range but past the tileset's own array reads whatever follows it --
     tiles for the picture, and, worse, a metatile *behaviour* byte, which the
     field code switches on.
  3. map.bin the wrong size for the width and height the layout declares.
  4. warps that name a map or a warp id that does not exist.
  5. connections whose neighbour is missing.
  6. object events on a graphics id with no entry in the pointer table,
     following the aliases the Arauna cast rides in on.
  7. tileset animation callbacks that are not defined anywhere.
  8. warps a player cannot actually reach from the map's Fly/heal point.
     Bounds is one thing, standing room is another: a warp inside the map but
     on water, on a wall or walled off from the arrival tile still strands the
     player, and nothing in the build notices. This floods out from the heal
     point over the collision and behaviour bytes the engine reads, and fails
     only when a warp is out of reach even allowing Surf. Warps that need Surf
     are reported separately, because plenty of them are deliberate.

Run it after dropping in a new map, before wondering why walking into a
doorway does something strange:

    python3 tools/arauna/audit_map_data.py

It is deliberately not wired into scripts/check_arauna_static.sh. It reads
528 maps and every blockdata file, which is slower than the gates, and the
build already refuses the mistakes a compiler can see.
"""
from __future__ import annotations

import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NUM_METATILES_IN_PRIMARY = 512
NUM_METATILES_TOTAL = 1024

# Emerald itself parks ten events one tile outside their own map and drives
# them from script instead of from the grid. They are not defects and they are
# not this project's, so they are named here rather than reported forever.
# Anything else standing outside its map is new, and new is the interesting
# case: Porto do Sal was cut from 56 columns to 52 with the boat's arrival
# warp left behind at x=52, which is how the player landed in the sea.
VANILLA_EVENTS_OUTSIDE_THEIR_MAP = {
    ("SlateportCity", "warp", 40, 7),
    ("SlateportCity_Harbor", "warp", 19, 15),
    ("SlateportCity_Harbor", "warp", 20, 15),
    ("LilycoveCity_DepartmentStore_1F", "bg", 0, 8),
    ("MeteorFalls_1F_1R", "bg", 9, 58),
    ("MeteorFalls_1F_2R", "bg", 9, 58),
    ("BattleFrontier_BattleDomeCorridor", "warp", 6, 8),
    ("BattleFrontier_BattleDomeCorridor", "warp", 7, 8),
    ("BattleFrontier_BattleDomePreBattleRoom", "warp", 6, 8),
    ("BattleFrontier_BattleDomePreBattleRoom", "warp", 7, 8),
}

# The reachability flood reads collision and behaviour but not elevation, and
# it will not jump a one-way ledge. Emerald builds two plateaus that need both:
# Lavaridge's centre sits above the town, and Artisan Cave opens off a Frontier
# terrace. A pure collision flood reads them as cut off. They are vanilla, they
# work in game, and they are named here so a genuinely stranded warp in a new
# map still fails the check instead of drowning in these two.
VANILLA_WARPS_THE_FLOOD_CANNOT_REACH = {
    ("BattleFrontier_OutsideEast", 28, 7),
    ("LavaridgeTown", 9, 2),
}


def load():
    layouts = {e["id"]: e for e in
               json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]}
    groups = json.loads((ROOT / "data/maps/map_groups.json").read_text())
    order = groups["group_order"]
    maps = {}
    const = {}
    for gi, gname in enumerate(order):
        for mi, m in enumerate(groups[gname]):
            maps[m] = (gi, mi)
    # The map constants are generated from the group order, so read them from
    # the header the build produced rather than guessing at the spelling.
    header = (ROOT / "include/constants/map_groups.h").read_text()
    names = re.findall(r"^\s+(MAP_\w+)\s*=\s*\((\d+) \| \((\d+) << 8\)\)", header, re.M)
    by_pos = {(int(g), int(n)): c for c, n, g in names}
    for m, (gi, mi) in maps.items():
        c = by_pos.get((gi, mi))
        if c:
            const[c] = m
    return layouts, maps, const


def tileset_metatile_counts():
    """How many metatiles each tileset symbol really has, from its own file."""
    headers = (ROOT / "src/data/tilesets/headers.h").read_text()
    graphics = (ROOT / "src/data/tilesets/graphics.h").read_text()
    meta_sym = dict(re.findall(
        r"const struct Tileset (\w+) =\s*\{.*?\.metatiles = (\w+),", headers, re.S))
    sym_file = dict(re.findall(
        r"const u16 (\w+)\[\] = INCBIN_U16\(\"([^\"]+)\"\);", graphics))
    sym_file.update(dict(re.findall(
        r"const u16 (\w+)\[\] = INCGFX_U16\(\"([^\"]+)\"[^)]*\);", graphics)))
    out = {}
    for tileset, sym in meta_sym.items():
        f = sym_file.get(sym)
        if f and (ROOT / f).exists():
            out[tileset] = (ROOT / f).stat().st_size // 16
    return out


def tileset_attributes():
    """Each tileset symbol's metatile attribute words, from its own file."""
    headers = (ROOT / "src/data/tilesets/headers.h").read_text()
    # The attribute arrays live in metatiles.h, not graphics.h -- graphics.h
    # holds the tiles and palettes.
    metatiles = (ROOT / "src/data/tilesets/metatiles.h").read_text()
    attr_sym = dict(re.findall(
        r"const struct Tileset (\w+) =\s*\{.*?\.metatileAttributes = (\w+),",
        headers, re.S))
    sym_file = dict(re.findall(
        r"const u16 (\w+)\[\] = INCBIN_U16\(\"([^\"]+)\"\);", metatiles))
    out = {}
    for tileset, sym in attr_sym.items():
        f = sym_file.get(sym)
        if f and (ROOT / f).exists():
            raw = (ROOT / f).read_bytes()
            out[tileset] = struct.unpack(f"<{len(raw)//2}H", raw)
    return out


def surfable_behaviours() -> set[int]:
    """The metatile behaviours the engine only lets you cross on Surf."""
    table = (ROOT / "src/metatile_behavior.c").read_text()
    start = table.index("static const u8 sTileBitAttributes[NUM_METATILE_BEHAVIORS] =")
    names = [m[0] for m in re.findall(
        r"\[(MB_\w+)\]\s*=\s*([^\n]*TILE_FLAG_SURFABLE[^\n]*),",
        table[start:table.index("\n};", start)])]
    # The behaviours are a plain enum, so count through it to get the values.
    header = (ROOT / "include/constants/metatile_behaviors.h").read_text()
    body = re.search(r"enum\s*\w*\s*\{(.*?)\n\};", header, re.S).group(1)
    values, n = {}, 0
    for line in body.splitlines():
        entry = line.split("//")[0].strip().rstrip(",")
        if not entry.startswith("MB_"):
            continue
        if "=" in entry:
            entry, raw = (p.strip() for p in entry.split("="))
            n = int(raw, 0)
        values[entry] = n
        n += 1
    return {values[name] for name in names if name in values}


def unreachable_warps(name, blob, w, h, vals, lay, attrs, surfable, heal):
    """Warps of this map the player cannot walk to from its Fly/heal tile.

    Returns (stranded, surf_only). Stranded means out of reach even by sea.
    """
    start = heal.get(name)
    if start is None or not blob.get("warp_events"):
        return [], []
    prim = attrs.get(lay["primary_tileset"]) or ()
    sec = attrs.get(lay["secondary_tileset"]) or ()

    def behaviour(mid):
        if mid < NUM_METATILES_IN_PRIMARY:
            return prim[mid] & 0xFF if mid < len(prim) else 0
        i = mid - NUM_METATILES_IN_PRIMARY
        return sec[i] & 0xFF if i < len(sec) else 0

    def flood(allow_surf):
        if not (0 <= start[0] < w and 0 <= start[1] < h):
            return set()

        def open_at(x, y):
            if not (0 <= x < w and 0 <= y < h):
                return False
            cell = vals[y * w + x]
            if (cell >> 10) & 0x3:
                return False
            return allow_surf or behaviour(cell & 0x3FF) not in surfable

        if not open_at(*start):
            return set()
        seen, stack = set(), [start]
        while stack:
            x, y = stack.pop()
            if (x, y) in seen:
                continue
            seen.add((x, y))
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if (x + dx, y + dy) not in seen and open_at(x + dx, y + dy):
                    stack.append((x + dx, y + dy))
        return seen

    on_foot = flood(False)
    if not on_foot:
        return [], []
    by_sea = flood(True)

    def served_by(area, p):
        """A warp is served if you can stand on it, or in front of it.

        Emerald has both kinds of door. Some you step onto -- the tile is
        walkable and the warp fires under your feet. Others are a wall tile
        you walk *into*: the Pokemon League gate is collision 1, and the warp
        fires from the tile below. Requiring the warp tile itself to be
        walkable calls every door of the second kind stranded.
        """
        return p in area or any((p[0] + dx, p[1] + dy) in area
                                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))

    stranded, surf_only = [], []
    for wev in blob["warp_events"]:
        p = (int(wev["x"]), int(wev["y"]))
        if served_by(on_foot, p):
            continue
        dest = (wev.get("dest_map") or "").replace("MAP_", "")
        if (name, p[0], p[1]) in VANILLA_WARPS_THE_FLOOD_CANNOT_REACH:
            continue
        if served_by(by_sea, p):
            surf_only.append(f"{name}: warp at {p} -> {dest} needs Surf")
        else:
            stranded.append(f"{name}: warp at {p} -> {dest} cannot be reached "
                            f"from the heal point at {start}")
    return stranded, surf_only


def main() -> int:
    layouts, maps, const = load()
    counts = tileset_metatile_counts()
    headers = (ROOT / "src/data/tilesets/headers.h").read_text()
    callbacks = dict(re.findall(
        r"const struct Tileset (\w+) =\s*\{.*?\.callback = (\w+),", headers, re.S))
    src = "\n".join((ROOT / p).read_text(errors="ignore")
                    for p in ("src/tileset_anims.c",))
    pointers = set(re.findall(r"\[OBJ_EVENT_GFX_(\w+)\]",
                              (ROOT / "src/data/object_events/"
                                      "object_event_graphics_info_pointers.h").read_text()))
    gfx_header = (ROOT / "include/constants/event_objects.h").read_text()
    gfx_consts = set(re.findall(r"#define OBJ_EVENT_GFX_(\w+)\s", gfx_header))
    # Arauna characters ride in unused vanilla slots by way of an alias --
    # OBJ_EVENT_GFX_DONA_ZILA is OBJ_EVENT_GFX_UNUSED_NATU_DOLL. The pointer
    # table is keyed by the slot, so the alias has to be followed or every one
    # of them reads as unwired.
    alias = dict(re.findall(
        r"#define\s+OBJ_EVENT_GFX_(\w+)\s+OBJ_EVENT_GFX_(\w+)\s*$", gfx_header, re.M))

    def slot_of(name: str) -> str:
        seen = set()
        while name in alias and name not in seen:
            seen.add(name)
            name = alias[name]
        return name

    bad_metatile, bad_size, bad_warp, bad_conn, bad_gfx, bad_cb = [], [], [], [], [], []
    bad_bounds = []
    stranded, surf_only = [], []

    attrs = tileset_attributes()
    surfable = surfable_behaviours()
    heal = {}
    for hl in json.loads((ROOT / "src/data/heal_locations.json").read_text())["heal_locations"]:
        m = const.get(hl.get("map"))
        if m:
            heal[m] = (int(hl["x"]), int(hl["y"]))

    for tileset, cb in callbacks.items():
        if cb != "NULL" and f"{cb}(" not in src:
            bad_cb.append(f"{tileset} -> {cb}")

    for name, (gi, mi) in sorted(maps.items()):
        mj = ROOT / "data/maps" / name / "map.json"
        if not mj.exists():
            continue
        blob = json.loads(mj.read_text())
        lay = layouts.get(blob.get("layout"))
        if not lay:
            continue
        w, h = lay["width"], lay["height"]
        prim = counts.get(lay["primary_tileset"].replace("gTileset_", "gTileset_"))
        prim = counts.get(lay["primary_tileset"])
        sec = counts.get(lay["secondary_tileset"])

        raw = (ROOT / lay["blockdata_filepath"]).read_bytes()
        if len(raw) != w * h * 2:
            bad_size.append(f"{name}: map.bin {len(raw)}B but {w}x{h} needs {w*h*2}B")
        vals = struct.unpack(f"<{len(raw)//2}H", raw)
        border = (ROOT / lay["border_filepath"]).read_bytes()
        bvals = struct.unpack(f"<{len(border)//2}H", border)

        worst = None
        for tag, series in (("map", vals), ("border", bvals)):
            for v in series:
                mid = v & 0x3FF
                if mid < NUM_METATILES_IN_PRIMARY:
                    limit, which = prim, lay["primary_tileset"]
                    idx = mid
                else:
                    limit, which = sec, lay["secondary_tileset"]
                    idx = mid - NUM_METATILES_IN_PRIMARY
                if limit is not None and idx >= limit:
                    if worst is None or idx - limit > worst[1]:
                        worst = (f"{name} {tag}: metatile {mid} but "
                                 f"{which} defines {limit}", idx - limit)
        if worst:
            bad_metatile.append(worst[0])

        # A warp or an object placed outside the map is how a narrowed map
        # strands the player: Porto do Sal was cut from 56 columns to 52 with
        # the boat's arrival warp left at x=52.
        for kind in ("warp_events", "object_events", "bg_events", "coord_events"):
            for ev in blob.get(kind, []) or []:
                try:
                    ex, ey = int(ev["x"]), int(ev["y"])
                except (KeyError, TypeError, ValueError):
                    continue
                if 0 <= ex < w and 0 <= ey < h:
                    continue
                if (name, kind[:-7], ex, ey) in VANILLA_EVENTS_OUTSIDE_THEIR_MAP:
                    continue
                bad_bounds.append(f"{name}: {kind[:-7]} at ({ex},{ey}) "
                                  f"but the map is {w}x{h}")

        for wev in blob.get("warp_events", []) or []:
            dest = const.get(wev.get("dest_map", ""))
            if wev.get("dest_map") in ("MAP_NONE", "MAP_DYNAMIC"):
                continue
            if dest is None:
                bad_warp.append(f"{name} -> unknown map {wev.get('dest_map')}")
                continue
            dj = ROOT / "data/maps" / dest / "map.json"
            if not dj.exists():
                continue
            n_warps = len(json.loads(dj.read_text()).get("warp_events", []) or [])
            try:
                wid = int(wev.get("dest_warp_id"))
            except (TypeError, ValueError):
                continue
            if wid >= n_warps:
                bad_warp.append(f"{name} -> {dest} warp id {wid} but it has {n_warps}")

        lost, swum = unreachable_warps(name, blob, w, h, vals, lay,
                                       attrs, surfable, heal)
        stranded += lost
        surf_only += swum

        for c in blob.get("connections") or []:
            if const.get(c.get("map", "")) is None:
                bad_conn.append(f"{name} {c.get('direction')} -> unknown {c.get('map')}")

        for o in blob.get("object_events", []) or []:
            g = (o.get("graphics_id") or "").replace("OBJ_EVENT_GFX_", "")
            if g.startswith("VAR_"):
                continue          # resolved at runtime from an object gfx var
            if g and slot_of(g) not in pointers and g in gfx_consts:
                bad_gfx.append(f"{name}: {o.get('graphics_id')} has no pointer entry")
            elif g and g not in gfx_consts:
                bad_gfx.append(f"{name}: {o.get('graphics_id')} is not a known id")

    fails = 0
    for label, rows in (("events standing outside their own map", bad_bounds),
                        ("metatile ids past the end of their tileset", bad_metatile),
                        ("map.bin size disagreeing with the layout", bad_size),
                        ("warps naming a map or warp id that does not exist", bad_warp),
                        ("connections to a map that does not exist", bad_conn),
                        ("object events on an unwired graphics id", bad_gfx),
                        ("tileset animation callbacks with no definition", bad_cb),
                        ("warps unreachable from their map's heal point", stranded)):
        mark = "FAIL" if rows else "PASS"
        fails += bool(rows)
        print(f"  [{mark}] {label}: {len(rows)}")
        for r in rows[:12]:
            print(f"          {r}")
        if len(rows) > 12:
            print(f"          ... and {len(rows)-12} more")

    # Not a fault: a warp behind water is how the game gates a place off.
    # Printed so a new one is noticed rather than assumed.
    print(f"  [note] warps that need Surf to reach: {len(surf_only)}")
    for r in surf_only[:12]:
        print(f"          {r}")
    if len(surf_only) > 12:
        print(f"          ... and {len(surf_only)-12} more")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
