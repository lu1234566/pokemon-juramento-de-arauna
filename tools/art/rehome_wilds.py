#!/usr/bin/env python3
"""Put the creatures where the land they live in says they should be.

Every route wears a biome now, drawn into its grass and its leaves. What walks
around in the grass was never touched: the wild tables are still Hoenn's, on
slots that have since been renamed and retyped, so a caatinga can hold nothing
of a caatinga.

Choosing new creatures for each route would be the obvious fix and the wrong
one: it makes some species unobtainable, others suddenly common, and it moves
the difficulty of every route it touches. So nothing is chosen. The species
already in the ground are *permuted* between maps, and only between slots whose
occupants are about equally strong, so that:

  * every species still appears exactly as many times as it did - the Pokedex
    stays completable and nothing becomes a rarity by accident;
  * every slot keeps its own levels and its own encounter rate, so a route is
    as hard as it was;
  * and what lives on a map is as much of that map's biome as the permutation
    can manage.

That last line used to be decided greedily, biome by biome, which is where the
coverage stopped. It is a transportation problem and it has an exact answer:
species on one side with their counts, slots on the other with theirs, an edge
wherever the strengths are close enough, and a cost that is large when the
species does not belong to the biome and equal to the strength difference when
it does. Minimum-cost flow then buys every fit that is available and, among
equally good answers, the one that disturbs the least.

Water is left alone. A sea route is not a caatinga whatever the tileset says,
and surfing tables are water-typed by their nature.

    python3 tools/art/rehome_wilds.py --report
    python3 tools/art/rehome_wilds.py
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/art"))
sys.path.insert(0, str(ROOT / "tools/audit"))

WILDS = ROOT / "src/data/wild_encounters.json"

# What each biome reads as, in the type language the species already speak.
from check_biome_encounters import BELONGS, map_biomes  # noqa: E402

# How far apart two base-stat totals may be and still count as "about as
# strong". A slot keeps its own levels, so this is what keeps a level 3 slot
# from being handed something that evolves twice.
TOLERANCE = 60

# Belonging is worth more than any strength difference this permits, so the
# solver buys every fit that exists and only then minimises disturbance.
MISFIT = 10_000


def species_facts():
    text = (ROOT / "src/data/pokemon/species_info.h").read_text(encoding="utf-8",
                                                                errors="replace")
    types, power = {}, {}
    for name, body in re.findall(r"\[SPECIES_(\w+)\]\s*=\s*\{(.*?)\n    \},", text, re.S):
        m = re.search(r"\.types\s*=\s*\{\s*TYPE_(\w+),\s*TYPE_(\w+)\s*\}", body)
        if m:
            types[name] = set(m.groups())
        total = 0
        for field in ("baseHP", "baseAttack", "baseDefense", "baseSpeed",
                      "baseSpAttack", "baseSpDefense"):
            got = re.search(r"\.%s\s*=\s*(\d+)" % field, body)
            total += int(got.group(1)) if got else 0
        power[name] = total
    return types, power


# --- minimum-cost flow ------------------------------------------------------

class Flow:
    """Successive shortest paths. The graph here is tens of nodes wide."""

    def __init__(self, n):
        self.g = [[] for _ in range(n)]

    def edge(self, u, v, cap, cost):
        self.g[u].append([v, cap, cost, len(self.g[v])])
        self.g[v].append([u, 0, -cost, len(self.g[u]) - 1])

    def run(self, src, snk):
        sent = spent = 0
        while True:
            dist = [None] * len(self.g)
            dist[src] = 0
            prev = [None] * len(self.g)
            queue, waiting = collections.deque([src]), {src}
            while queue:
                u = queue.popleft()
                waiting.discard(u)
                for i, (v, cap, cost, _) in enumerate(self.g[u]):
                    if cap > 0 and (dist[v] is None or dist[u] + cost < dist[v]):
                        dist[v] = dist[u] + cost
                        prev[v] = (u, i)
                        if v not in waiting:
                            waiting.add(v)
                            queue.append(v)
            if dist[snk] is None:
                return sent, spent
            step, v = None, snk
            while v != src:
                u, i = prev[v]
                step = self.g[u][i][1] if step is None else min(step, self.g[u][i][1])
                v = u
            v = snk
            while v != src:
                u, i = prev[v]
                self.g[u][i][1] -= step
                self.g[self.g[u][i][0]][self.g[u][i][3]][1] += step
                v = u
            sent += step
            spent += step * dist[snk]


def assign(slots, types, power, tolerance):
    """Hand every slot a species, keeping the multiset and the strengths.

    Slots that hold the same species and sit on the same map are one and the
    same question, so they are asked once. The map is part of that key and not
    only the biome, because a table is a place and not a category: without it
    the twelve slots of one route are indistinguishable from twelve slots
    spread over four, and the answer can be one species twelve times. It was,
    once - Route 113 lost SKARMORY, SLUGMA and SPINDA and came back holding
    nothing but ZIGZAGOON. So each map also carries a ceiling on how many
    copies of any one species it may hold: the largest number of copies it
    already held, which the table it starts from satisfies by definition.

    Returns {(map, biome, species): [names]}.
    """
    def fits(species, biome):
        return bool(types.get(species, set()) & BELONGS[biome])

    pool = collections.Counter(s["species"] for s in slots)
    groups = collections.Counter((s["map"], s["biome"], s["species"]) for s in slots)
    crowd = collections.defaultdict(collections.Counter)
    for slot in slots:
        crowd[slot["map"]][slot["species"]] += 1
    ceiling = {name: max(seen.values()) for name, seen in crowd.items()}

    kinds, cells = sorted(pool), sorted(groups)
    def price(species, cell):
        _, biome, was = cell
        drift = abs(power.get(species, 0) - power.get(was, 0))
        # The last term keeps the incumbent when nothing else separates two
        # answers, so running this twice moves nothing.
        return (drift + (0 if fits(species, biome) else MISFIT)
                + (0 if species == was else 1))

    reach = collections.defaultdict(list)      # (map, species) -> cell indices
    for i, cell in enumerate(cells):
        for species in kinds:
            if tolerance is None or abs(power.get(species, 0)
                                        - power.get(cell[2], 0)) <= tolerance:
                reach[(cell[0], species)].append(i)
    holders = sorted(reach)

    base = len(kinds)
    hold = {key: base + len(cells) + n for n, key in enumerate(holders)}
    src, snk = base + len(cells) + len(holders), base + len(cells) + len(holders) + 1
    net = Flow(snk + 1)
    for j, species in enumerate(kinds):
        net.edge(src, j, pool[species], 0)
    for i, cell in enumerate(cells):
        net.edge(base + i, snk, groups[cell], 0)
    for (name, species), cell_ids in reach.items():
        node = hold[(name, species)]
        net.edge(kinds.index(species), node,
                 min(pool[species], ceiling[name]), 0)
        for i in cell_ids:
            net.edge(node, base + i, groups[cells[i]], price(species, cells[i]))

    sent, _ = net.run(src, snk)
    if sent != len(slots):
        raise SystemExit("could not place every slot: %d of %d" % (sent, len(slots)))

    filled = collections.defaultdict(list)
    for (name, species), _ in reach.items():
        node = hold[(name, species)]
        for v, cap, cost, back in net.g[node]:
            if v < base or v >= base + len(cells):
                continue                       # the way back to the species
            moved = net.g[v][back][1]          # what came back is what flowed
            filled[cells[v - base]] += [species] * moved
    return filled


def spread(slots, types, power, tolerance):
    """Let no map end holding nothing of itself.

    Two biomes ask for more than the whole land pool can give - a caatinga
    wants rock, ground and fire, and the game has 42 such creatures for 60
    slots - so some slots must hold something that does not belong. Minimum
    cost is indifferent to *where* those land, and it will happily pile the
    entire shortfall onto one route: an optimal answer in which one caatinga is
    100% itself and the caatinga beside it is 0%. A player reads that as the
    biome not being there at all.

    So afterwards, any map left with nothing of itself trades with a map of the
    same biome that has fits to spare. A trade is a swap, so the multiset is
    untouched; both sides are checked against their own original occupant, so
    the strength promise holds; and neither side may break its crowding
    ceiling.

    Returns the number of trades made.
    """
    def fits(slot, species):
        return bool(types.get(species, set()) & BELONGS[slot["biome"]])

    def near(slot, species):
        return abs(power.get(species, 0) - power.get(slot["species"], 0)) <= tolerance

    by_map = collections.defaultdict(list)
    for slot in slots:
        by_map[slot["map"]].append(slot)
    ceiling = {name: max(collections.Counter(s["species"] for s in group).values())
               for name, group in by_map.items()}

    def crowded(group, out, into):
        seen = collections.Counter(s["new"] for s in group)
        seen[out] -= 1
        seen[into] += 1
        return seen[into] > ceiling[group[0]["map"]]

    trades = 0
    for _ in range(len(slots)):
        scored = {name: sum(1 for s in group if fits(s, s["new"])) for name, group in by_map.items()}
        starved = [n for n, got in scored.items() if got == 0]
        if not starved:
            break
        done = False
        for name in starved:
            group, biome = by_map[name], by_map[name][0]["biome"]
            donors = sorted((n for n, g in by_map.items()
                             if g[0]["biome"] == biome and scored[n] >= 2),
                            key=lambda n: -scored[n])
            for other in donors:
                for mine in group:
                    for theirs in by_map[other]:
                        if not fits(theirs, theirs["new"]) or fits(mine, mine["new"]):
                            continue
                        if not (near(mine, theirs["new"]) and near(theirs, mine["new"])):
                            continue
                        if crowded(group, mine["new"], theirs["new"]) or \
                           crowded(by_map[other], theirs["new"], mine["new"]):
                            continue
                        mine["new"], theirs["new"] = theirs["new"], mine["new"]
                        trades += 1
                        done = True
                        break
                    if done:
                        break
                if done:
                    break
            if done:
                break
        if not done:
            break
    return trades


def read_slots(where):
    data = json.loads(WILDS.read_text(encoding="utf-8", errors="replace"))
    slots = []
    for entry in data["wild_encounter_groups"][0]["encounters"]:
        biome = where.get(entry["map"].replace("MAP_", ""))
        if not biome or not entry.get("land_mons"):
            continue
        for i, mon in enumerate(entry["land_mons"]["mons"]):
            slots.append({"entry": entry, "index": i, "biome": biome,
                          "map": entry["map"],
                          "species": mon["species"].replace("SPECIES_", "")})
    return data, slots


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--tolerance", type=int, default=TOLERANCE)
    args = ap.parse_args()

    types, power = species_facts()
    data, slots = read_slots(map_biomes())
    if not slots:
        print("no land slots on any map with a biome")
        return 0

    def fits(species, biome):
        return bool(types.get(species, set()) & BELONGS[biome])

    before = sum(1 for s in slots if fits(s["species"], s["biome"]))
    filled = assign(slots, types, power, args.tolerance)
    handout = {cell: list(names) for cell, names in filled.items()}
    moved = drifted = 0
    for slot in slots:
        slot["new"] = handout[(slot["map"], slot["biome"], slot["species"])].pop()
        if slot["new"] != slot["species"]:
            moved += 1
            drifted = max(drifted, abs(power.get(slot["new"], 0)
                                       - power.get(slot["species"], 0)))
    traded = spread(slots, types, power, args.tolerance)
    if traded:
        moved = sum(1 for s in slots if s["new"] != s["species"])
        drifted = max(abs(power.get(s["new"], 0) - power.get(s["species"], 0))
                      for s in slots)
    after = sum(1 for s in slots if fits(s["new"], s["biome"]))

    maps = len({id(s["entry"]) for s in slots})
    print("%d land slot(s) on %d map(s) with a biome" % (len(slots), maps))
    print("  belonged before: %d (%.0f%%)" % (before, 100 * before / len(slots)))
    print("  belongs after:   %d (%.0f%%)" % (after, 100 * after / len(slots)))
    print("  %d slot(s) change hands; every species keeps its exact count"
          % moved)
    print("  widest strength change: %d base-stat points (allowed %d)"
          % (drifted, args.tolerance))
    if traded:
        print("  %d trade(s) so that no map holds nothing of itself" % traded)

    # What the permutation cannot reach, and the price of reaching it.
    loose = assign(slots, types, power, None)
    ceiling = sum(len([n for n in names if fits(n, biome)])
                  for (_, biome, _), names in loose.items())
    print("  ceiling if strength were ignored: %d (%.0f%%)"
          % (ceiling, 100 * ceiling / len(slots)))
    short = []
    for biome in sorted({s["biome"] for s in slots}):
        want = sum(1 for s in slots if s["biome"] == biome)
        have = sum(1 for s in slots if fits(s["species"], biome))
        if have < want:
            short.append("%s wants %d, the whole land pool holds %d"
                         % (biome, want, have))
    for line in short:
        print("  " + line)

    if args.report:
        return 0

    for slot in slots:
        slot["entry"]["land_mons"]["mons"][slot["index"]]["species"] = \
            "SPECIES_" + slot["new"]
    WILDS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
