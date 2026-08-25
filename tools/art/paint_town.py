#!/usr/bin/env python3
"""Lay streets and squares through a town, in the tiles Emerald already uses.

Two pieces.

`learn_family` reads the whole Emerald corpus and works out how a material
tiles itself: for every block of the material it records which of its four
neighbours are the same material, and keeps the block the game most often puts
in that situation. What comes back is the material's own autotile table, so a
region painted with it gets the edges and corners the artists drew, not a
rectangle of fill.

`streets` works out where a town's streets belong: it walks the town's own
walkable graph from every door and every route exit to a hub, keeps the union
of those shortest paths, and widens it. A settlement's paths are wherever its
buildings and its map exits already force people to walk, so the streets land
where the town says they should rather than where a grid says.

Nothing here changes a block's collision, elevation or behaviour: painting only
ever replaces one walkable ground block with another walkable ground block of
the same behaviour, and the caller passes the set of blocks that counts as
bare ground.
"""
from __future__ import annotations

import collections
import json
import os
import struct

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NEIGHBOURS = ((0, -1), (1, 0), (0, 1), (-1, 0))


def learn_family(family, primary=None, corpus_root=ROOT):
    """signature of same-material neighbours -> the block Emerald uses there."""
    layouts = json.load(open(os.path.join(corpus_root, "data/layouts/layouts.json"), encoding="utf-8"))["layouts"]
    table = collections.defaultdict(collections.Counter)
    for layout in layouts:
        if primary and layout.get("primary_tileset") != primary:
            continue
        path = os.path.join(corpus_root, layout.get("blockdata_filepath", ""))
        if not os.path.exists(path):
            continue
        w, h = int(layout["width"]), int(layout["height"])
        raw = open(path, "rb").read()
        if len(raw) != w * h * 2:
            continue
        grid = [v & 0x03FF for v in struct.unpack("<%dH" % (w * h), raw)]
        if not any(v in family for v in grid):
            continue
        for y in range(h):
            for x in range(w):
                if grid[y * w + x] not in family:
                    continue
                sig = 0
                for i, (dx, dy) in enumerate(NEIGHBOURS):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and grid[ny * w + nx] in family:
                        sig |= 1 << i
                table[sig][grid[y * w + x]] += 1
    if not table:
        raise SystemExit("family never appears in the corpus; nothing to learn")
    resolved = {sig: counts.most_common(1)[0][0] for sig, counts in table.items()}
    # A material with no edge blocks of its own - a plain city pavement, say -
    # only teaches one answer. Fill the rest with it so the region still lays.
    fill = resolved.get(0x0F) or collections.Counter(
        {mid: sum(c[mid] for c in table.values()) for sig in table for mid in table[sig]}
    ).most_common(1)[0][0]
    return {sig: resolved.get(sig, fill) for sig in range(16)}


def streets(town, anchors, hub=None, width=1, walkable=None):
    """Union of the shortest walks from every anchor to the hub, widened.

    `walkable` defaults to the town's own collision, which is what makes the
    result follow the streets the buildings already imply.
    """
    if walkable is None:
        def walkable(x, y):
            return town.walkable(x, y)

    def neighbours(cell):
        x, y = cell
        for dx, dy in NEIGHBOURS:
            nx, ny = x + dx, y + dy
            if not town.inside(nx, ny) or not walkable(nx, ny):
                continue
            here, there = town.elevation(x, y), town.elevation(nx, ny)
            if here == there or here in (0, 15) or there in (0, 15):
                yield (nx, ny)

    anchors = [a for a in anchors if town.inside(*a)]
    if hub is None:
        hub = _hub(town, anchors, walkable)

    came = {hub: None}
    queue = collections.deque([hub])
    while queue:
        cell = queue.popleft()
        for nxt in neighbours(cell):
            if nxt not in came:
                came[nxt] = cell
                queue.append(nxt)

    road = set()
    for anchor in anchors:
        cell = anchor if anchor in came else _nearest(came, anchor)
        while cell is not None:
            road.add(cell)
            cell = came[cell]

    skeleton = set(road)
    # Widening runs one way only, right and down. Growing in all four
    # directions turns every junction into a blob; this keeps a street a
    # street and a crossroads a crossroads.
    for _ in range(width):
        grown = set(road)
        for x, y in road:
            for dx, dy in ((1, 0), (0, 1)):
                nx, ny = x + dx, y + dy
                if town.inside(nx, ny) and walkable(nx, ny):
                    grown.add((nx, ny))
        road = grown
    # A street runs between the buildings, not up against them: widening stops
    # one block short of anything solid, which leaves every façade its verge.
    road = {c for c in road if c in skeleton or not _touches_solid(town, c)}
    return road


def _touches_solid(town, cell):
    x, y = cell
    for dx, dy in NEIGHBOURS:
        nx, ny = x + dx, y + dy
        if town.inside(nx, ny) and not town.walkable(nx, ny):
            return True
    return False


def avenues(town, anchors, hub=None, walkable=None, lanes=2):
    """Straight two-lane streets from every anchor to the hub.

    A shortest walk through a town zigzags around whatever is in the way, and
    zigzags do not read as streets. Each anchor is joined to the hub by an
    L instead - one straight run, one turn, one straight run - and the L is
    only accepted if every block of it, across the full width of the street,
    is already walkable. Anything the L cannot reach falls back to the walk,
    so a corner the buildings box in still gets its path.
    """
    if walkable is None:
        def walkable(x, y):
            return town.walkable(x, y)
    anchors = [a for a in anchors if town.inside(*a)]
    if hub is None:
        hub = _hub(town, anchors, walkable)

    def run(a, b, lanes_across):
        """Blocks of a straight run from a to b, `lanes_across` wide."""
        (ax, ay), (bx, by) = a, b
        cells = set()
        if ax == bx:
            for y in range(min(ay, by), max(ay, by) + 1):
                for i in range(lanes_across):
                    cells.add((ax + i, y))
        elif ay == by:
            for x in range(min(ax, bx), max(ax, bx) + 1):
                for i in range(lanes_across):
                    cells.add((x, ay + i))
        else:
            return None
        return cells

    def usable(cells):
        return cells is not None and all(town.inside(x, y) and walkable(x, y) for x, y in cells)

    road = set()
    for anchor in anchors:
        best = None
        for corner in ((anchor[0], hub[1]), (hub[0], anchor[1])):
            for lanes_across in range(lanes, 0, -1):
                first = run(anchor, corner, lanes_across)
                second = run(corner, hub, lanes_across)
                if usable(first) and usable(second):
                    best = first | second
                    break
            if best:
                break
        if best is None:
            best = streets(town, [anchor], hub=hub, width=0, walkable=walkable)
        road |= best
    return road


def _hub(town, anchors, walkable):
    """The walkable cell that is least far from every anchor."""
    if not anchors:
        raise SystemExit("no anchors to route between")
    cx = sum(a[0] for a in anchors) / len(anchors)
    cy = sum(a[1] for a in anchors) / len(anchors)
    best, best_score = None, None
    for y in range(town.h):
        for x in range(town.w):
            if not walkable(x, y):
                continue
            score = (x - cx) ** 2 + (y - cy) ** 2
            if best_score is None or score < best_score:
                best, best_score = (x, y), score
    return best


def _nearest(came, cell):
    x, y = cell
    return min(came, key=lambda c: (c[0] - x) ** 2 + (c[1] - y) ** 2)


def paint(town, region, table, ground, keep=()):
    """Repaint `region` with a learned material. Returns the cells changed.

    A cell is only repainted when it currently holds one of `ground` - the
    blocks that count as bare, paintable floor - so doorsteps, flowerbeds and
    anything else the map already put there survive.
    """
    keep = set(keep)
    # The paved area is the whole region: a doorstep or a flowerbed left alone
    # inside it still reads as paved when the edges are worked out.
    paved = {c for c in region if town.inside(*c)}
    target = {c for c in paved if c not in keep and town.metatile(*c) in ground}
    changed = {}
    for x, y in sorted(target):
        sig = 0
        for i, (dx, dy) in enumerate(NEIGHBOURS):
            if (x + dx, y + dy) in paved:
                sig |= 1 << i
        block = table.get(sig, table[0x0F])
        old = town.blocks[town.index(x, y)]
        new = (old & 0xFC00) | block
        if new != old:
            changed[(x, y)] = new
    return changed


def commit(town, changed):
    for (x, y), value in changed.items():
        town.blocks[town.index(x, y)] = value
    raw = struct.pack("<%dH" % len(town.blocks), *town.blocks)
    open(town.path, "wb").write(raw)
    return len(changed)
