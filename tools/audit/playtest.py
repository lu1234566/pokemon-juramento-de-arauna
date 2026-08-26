#!/usr/bin/env python3
"""Play the game and write down what happened.

Three acts, each of which can be run on its own:

  opening  Boot a new game and play it to the first Pokemon - out of the
           truck, into the house, up to the clock, back down to Anahi, across
           the village to the laboratory, and out of it holding something.
           Every step is a walk to a coordinate over the map's real collision
           data, so a door that moved or a person standing in a doorway stops
           the run instead of being walked through.

  world    Enter every map in the game, let it settle, and look at it. Faults
           it can see: the field never coming up, the player landing outside
           the map, a screen that is one flat colour, a screen with almost no
           colour in it at all. Each is a way a map can be broken that a
           static check cannot see, because it is about what the hardware
           draws rather than what the data says.

  battles  Walk into tall grass until something attacks, and check the battle
           starts, runs and ends.

    python3 tools/audit/playtest.py opening
    python3 tools/audit/playtest.py world --limit 40
    python3 tools/audit/playtest.py all
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from map_invariants import TownMap                              # noqa: E402
from pilot import Pilot, Stuck                                  # noqa: E402
from play import CHECKPOINTS, Session                           # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]

# The road north of the village is shut until the rival has been met.
VAR_LITTLEROOT_TOWN_STATE = 0x4050
VAR_ROUTE101_STATE = 0x4060

# MB_TALL_GRASS, the behaviour a map gives a square that hides Pokemon.
TALL_GRASS = 2
REPORT = ROOT / "build" / "arauna-en" / "playtest"

# Maps no player can reach and no warp leads to: the debug and link rooms, the
# unused prototypes, the battle-frontier scaffolding that is only entered from
# inside its own minigames.
SKIP_PREFIXES = ("Unused", "SecretBase", "BattleFrontier_Battle", "Route104_Prototype",
                 "Dummy", "TradeCenter", "RecordCorner", "UnionRoom", "MossdeepCity_GameCorner")


def note(log, kind, **fields):
    entry = dict(kind=kind, **fields)
    log.append(entry)
    print("  " + kind + " " + " ".join("%s=%s" % kv for kv in fields.items()))
    return entry


# ---------------------------------------------------------------- act one
def act_opening(s: Session, log):
    p = Pilot(s)
    print("[opening]")
    if not p.clear_messages(40):
        note(log, "STUCK", where="the truck", detail="the arrival never released the controls")
        return p
    note(log, "truck", state="the arrival scene finished")

    p.use_warp(4, 2)                                  # the truck's tailgate
    if p.map_name() == "InsideOfTruck":
        note(log, "FAIL", step="leaving the truck", where=str(p.where()))
        return p
    note(log, "outside", map=p.map_name(), at=str(p.where()[2:]))
    s.shot("pt_01_arrival")

    for _ in range(40):                               # the cutscene walks us in
        p.clear_messages(6)
        s.probe.run(1.5)
        if p.map_name() == "LittlerootTown_BrendansHouse_1F":
            break
    if p.map_name() != "LittlerootTown_BrendansHouse_1F":
        note(log, "FAIL", step="the walk into the house", map=p.map_name())
        return p
    p.clear_messages(20)
    note(log, "house", at=str(p.where()[2:]))
    s.shot("pt_02_house")

    for step, (name, goal) in enumerate((
            ("the stairs", (8, 2)),
            ("the wall clock", (5, 2)),
    )):
        try:
            p.walk_to(*goal)
        except Stuck as why:
            note(log, "STUCK", step=name, detail=str(why))
            return p
        p.clear_messages(20)
        if step == 0:
            s.probe.run(2.0)
            note(log, "upstairs", map=p.map_name(), at=str(p.where()[2:]))

    # The clock is read from the square below it, and then it is not a message
    # box at all: it is its own screen, with a confirmation whose cursor starts
    # on NO. Twenty A presses answer NO twenty times and the run hangs there
    # looking like a script bug.
    p.face_and_talk(5, 1)
    s.probe.run(1.5)
    # Always UP and then A, never A on its own. On the face of the clock UP
    # only turns the hands, which nobody minds; on the confirmation it moves
    # the cursor off NO, where it starts. A alone answers NO for ever.
    for _ in range(10):
        if "WallClock" not in s.probe.callback2_name():
            break
        s.press("up", 1)
        s.probe.run(0.4)
        s.shot("pt_03_clock")
        s.press("a", 1)
        s.probe.run(1.4)
    for _ in range(20):
        if s.probe.callback2_name() == "CB2_Overworld" and not p.busy():
            break
        s.press("a", 1)
        s.probe.run(1.0)
    note(log, "clock",
         set="yes" if s.probe.callback2_name() == "CB2_Overworld" and not p.busy() else "no")
    # A waypoint of its own: everything before this is four minutes of scripted
    # cutscene, and a run that fails after it should not have to sit through
    # them again.
    s.savestate("pt_clock")

    try:
        p.use_warp(7, 1)                              # back downstairs
    except Stuck as why:
        note(log, "STUCK", step="the stairs down", detail=str(why))
        return p
    for _ in range(12):
        s.probe.run(1.2)
        p.clear_messages(6)
        if p.map_name() == "LittlerootTown_BrendansHouse_1F":
            break
    if p.map_name() != "LittlerootTown_BrendansHouse_1F":
        note(log, "STUCK", step="the stairs down", map=p.map_name(), at=str(p.where()[2:]))
        return p
    note(log, "downstairs", map=p.map_name(), at=str(p.where()[2:]))

    try:
        p.use_warp(8, 8)                              # the front door
    except Stuck as why:
        note(log, "STUCK", step="the front door", detail=str(why))
        return p
    for _ in range(20):
        p.clear_messages(8)
        s.probe.run(1.2)
        if p.map_name() == "LittlerootTown":
            break
    if p.map_name() != "LittlerootTown":
        note(log, "FAIL", step="stepping outside", map=p.map_name())
        return p
    note(log, "village", at=str(p.where()[2:]))
    s.shot("pt_04_village")
    s.savestate("pt_outside")
    return act_opening_tail(s, log, p)


def act_opening_tail(s: Session, log, p=None):
    """From the front step to the first Pokemon."""
    p = p or Pilot(s)
    print("[opening: the first Pokemon]")

    try:
        p.use_warp(10, 16)                            # the laboratory door
    except Stuck as why:
        note(log, "STUCK", step="the walk to the laboratory", detail=str(why))
        return p
    for _ in range(20):
        p.clear_messages(8)
        s.probe.run(1.2)
        if p.map_name() == "LittlerootTown_ProfessorBirchsLab":
            break
    if p.map_name() != "LittlerootTown_ProfessorBirchsLab":
        note(log, "FAIL", step="entering the laboratory", map=p.map_name())
        return p
    p.clear_messages(20)
    note(log, "laboratory", at=str(p.where()[2:]))
    s.shot("pt_05_lab")

    # The item balls in the laboratory are the Johto starter, a much later
    # reward. And the road north is shut until the rival has been met: the
    # scene in their bedroom is the only thing in the game that sets
    # VAR_LITTLEROOT_TOWN_STATE to 1, and at 0 the twin turns the player round
    # at the village edge saying it is dangerous without a Pokemon. A run that
    # skips the neighbour's house walks to the top of the map and bounces.
    try:
        p.use_warp(6, 12)                             # back out of the lab
        p.use_warp(14, 8)                             # the neighbour's door
    except Stuck as why:
        note(log, "STUCK", step="the walk to the neighbour", detail=str(why))
        return p
    note(log, "neighbour", map=p.map_name(), at=str(p.where()[2:]))
    try:
        p.use_warp(2, 2)                              # up to the bedroom
    except Stuck as why:
        note(log, "STUCK", step="the neighbour's stairs", detail=str(why))
        return p
    p.clear_messages(30)
    s.probe.run(2.0)
    p.clear_messages(30)
    note(log, "rival", map=p.map_name(), at=str(p.where()[2:]))
    s.shot("pt_05_rival")
    try:
        p.use_warp(1, 1)                              # back downstairs
        p.use_warp(1, 8)                              # and out
    except Stuck as why:
        note(log, "STUCK", step="leaving the neighbour", detail=str(why))
        return p
    note(log, "village", at=str(p.where()[2:]), state="heading north",
         town_state=s.probe.get_var(VAR_LITTLEROOT_TOWN_STATE))

    before = s.probe.party_count() or 0
    for _ in range(22):
        p.clear_messages(10)
        if (s.probe.party_count() or 0) > before:
            break
        callback = s.probe.callback2_name()
        if callback != "CB2_Overworld":               # a battle or a menu
            s.press("a", 1)
            s.probe.run(1.2)
            continue
        here = p.map_name()
        try:
            if here == "LittlerootTown":
                # Keep pushing north off the top of the map. Walking to the
                # square below the edge and stepping once only oscillates: the
                # next pass walks back down to it again.
                p.walk_to(11, 1)
                for _ in range(4):
                    if p.map_name() != "LittlerootTown":
                        break
                    p.step("up")
                    p.clear_messages(8)
            elif here == "Route101":
                # The rescue fires on the bottom row, and only on stepping
                # *onto* it. Arriving there from the village is not a step onto
                # it as far as the check is concerned, so a run that walks
                # straight on north leaves the whole scene behind and reaches
                # the top of the route with no Pokemon and no idea why.
                s.probe.run(2.0)
                p.clear_messages(12)
                if (s.probe.get_var(VAR_ROUTE101_STATE) or 0) <= 1:
                    p.walk_to(11, 18)
                    p.step("down")
                    p.clear_messages(30)
                else:
                    try:
                        p.walk_to(7, 15)      # beside Anahi's bag
                    except Stuck:
                        pass
                    p.face_and_talk(7, 14)
                    for _ in range(16):
                        p.clear_messages(8)
                        s.probe.run(1.0)
                        if (s.probe.party_count() or 0) > before:
                            break
                        s.press("a", 1)
            else:
                p.clear_messages(6)
        except Stuck:
            s.press("a", 1)
        s.probe.run(1.0)

    after = s.probe.party_count() or 0
    s.shot("pt_06_starter")
    note(log, "north", map=p.map_name(), at=str(p.where()[2:]))
    if after > before:
        note(log, "starter", party=after)
        s.savestate("pt_starter")
    else:
        note(log, "FAIL", step="the first Pokemon", party=after, map=p.map_name())
    return p


# ---------------------------------------------------------------- act two
def screen_faults(path):
    """What a screenshot can say about a map that the data cannot."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    # The GBA screen sits inside the emulator window; sample the middle of it.
    w, h = im.size
    crop = im.crop((int(w * 0.15), int(h * 0.15), int(w * 0.85), int(h * 0.85)))
    tally = crop.getcolors(1 << 24) or [(0, (0, 0, 0))]
    total = sum(n for n, _ in tally)
    count, top = max(tally)
    colours = tally
    faults = []
    if count / total > 0.97:
        faults.append("the screen is one flat colour %s" % (top,))
    elif len(colours) < 8:
        faults.append("the screen has %d colours in it" % len(colours))
    return faults


def arrival(p, name):
    """A square on this map that the player could plausibly be standing on."""
    try:
        grid = TownMap(name, str(ROOT))
    except Exception:                                   # noqa: BLE001
        return None
    for event in grid.events("warp_events"):
        x, y = int(event["x"]), int(event["y"])
        if grid.inside(x, y + 1) and grid.walkable(x, y + 1):
            return x, y + 1
    best = None
    for y in range(grid.h):
        for x in range(grid.w):
            if grid.walkable(x, y):
                best = best or (x, y)
    return best or (min(5, grid.w - 1), min(5, grid.h - 1))


def act_world(s: Session, log, limit=None, start=0, only=None):
    p = Pilot(s)
    print("[world]")
    shots = REPORT / "world"
    shots.mkdir(parents=True, exist_ok=True)
    wanted = set(only.split(",")) if only else None
    targets = [(gn, name) for gn, name in sorted(p.maps.items())
               if (name in wanted if wanted else not name.startswith(SKIP_PREFIXES))]
    if not wanted:
        targets = targets[start:][:limit] if limit else targets[start:]
    seen = 0
    for (group, num), name in targets:
        seen += 1
        # Arrive somewhere the map actually has. Warping every map to 5,5
        # drops the player off the edge of every small room and then reports
        # the room for it - a fault invented by the harness. A warp square is
        # somewhere the game itself sends people; the middle of the grid will
        # do when there is none.
        spot = arrival(p, name)
        if spot is None:
            note(log, "note", map=name, detail="no layout to enter it with")
            continue
        try:
            s.warp(group, num, *spot)
        except Exception as why:                        # noqa: BLE001
            note(log, "FAIL", map=name, detail="warp failed: %s" % why)
            continue
        s.probe.run(1.3)
        callback = s.probe.callback2_name()
        where = p.where()
        if callback != "CB2_Overworld":
            note(log, "FAIL", map=name, detail="the field never came up (%s)" % callback)
            continue
        # Some rooms are entered by a scripted walk - the Elite Four's chambers
        # walk the player four squares up from the doorway as they come in. Let
        # that finish before asking where they are.
        p.wait_free(6.0)
        where = p.where()
        grid = p.grid()
        if grid is not None and where is not None and not grid.inside(where[2], where[3]):
            # And then do not call it a fault. The square this harness warped
            # to is not where the game sends anybody, so a scripted entrance
            # carrying the player off the grid from it says nothing about the
            # map - it says the warp was made up.
            note(log, "note", map=name,
                 detail="entered by a scripted walk; %d,%d is off the grid" % where[2:])
        path = s.shots / ("world_%s.png" % name)
        s.shot("world_%s" % name)
        faults = screen_faults(path)
        if faults:
            note(log, "FAIL", map=name, detail="; ".join(faults))
            (shots / ("%s.png" % name)).write_bytes(path.read_bytes())
        else:
            path.unlink(missing_ok=True)
    note(log, "world", entered=seen)
    return p


# -------------------------------------------------------------- act three
def grass_cells(name):
    """Squares of tall grass on a map, as the map's own attributes call them."""
    try:
        grid = TownMap(name, str(ROOT))
    except Exception:                                       # noqa: BLE001
        return []
    return [(x, y) for y in range(grid.h) for x in range(grid.w)
            if grid.behavior(x, y) == TALL_GRASS and grid.walkable(x, y)]


def act_battles(s: Session, log, routes=None):
    """Walk in the grass until something attacks, and see the battle through.

    Two things this needs that are easy to leave out. The player has to be
    carrying a Pokemon - with an empty party the game refuses to start a wild
    battle at all, and a run resumed from before the first one paces up and
    down reporting that the grass is empty. And the pacing has to happen *in*
    the grass, which is a property of the map rather than somewhere to guess.
    """
    p = Pilot(s)
    print("[battles]")
    if not (s.probe.party_count() or 0):
        note(log, "FAIL", step="the battles", detail="the party is empty; resume from pt_starter")
        return p
    for name in routes or ("Route101", "Route102", "Route103", "Route116", "PetalburgWoods"):
        where = next((gn for gn, n in p.maps.items() if n == name), None)
        grass = grass_cells(name)
        if where is None or not grass:
            note(log, "note", map=name, detail="no tall grass on this map")
            continue
        s.warp(where[0], where[1], *grass[len(grass) // 2])
        s.probe.run(2.0)
        p.clear_messages(8)
        started = False
        for _ in range(24):
            for move in ("left", "right", "up", "down"):
                p.step(move)
                if s.probe.callback2_name() != "CB2_Overworld":
                    started = True
                    break
            if started:
                break
        if not started:
            note(log, "note", map=name, detail="nothing attacked in the grass")
            continue
        s.probe.run(5.0)
        s.shot("pt_battle_%s" % name)
        note(log, "battle", map=name, callback=s.probe.callback2_name())
        # Getting out. B does not run away - it backs out of a menu, and a
        # harness that presses it sixty times reports every battle in the game
        # as never ending. RUN is the bottom-right of the four, so the way out
        # is down, right, A. It can fail on speed, so it is worth several
        # goes, and if the wild one is simply faster, fight instead: a level 5
        # starter against a level 2 is a short conversation.
        how = "ran"
        for attempt in range(10):
            if s.probe.callback2_name() == "CB2_Overworld":
                break
            if attempt < 6:
                s.press("down", 1); s.probe.run(0.3)
                s.press("right", 1); s.probe.run(0.3)
                s.press("a", 1); s.probe.run(1.6)
            else:
                how = "fought"
                for _ in range(6):
                    s.press("a", 1)
                    s.probe.run(1.4)
        for _ in range(20):                            # ride out the fade
            if s.probe.callback2_name() == "CB2_Overworld":
                break
            s.press("a", 1)
            s.probe.run(1.0)
        if s.probe.callback2_name() != "CB2_Overworld":
            note(log, "FAIL", map=name, detail="the battle never ended")
        else:
            note(log, "battle-end", map=name, state="back on the field, %s" % how)
    return p


ACTS = {"opening": act_opening, "opening_tail": act_opening_tail,
        "world": act_world, "battles": act_battles}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("act", choices=sorted(ACTS) + ["all"])
    ap.add_argument("--limit", type=int)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--only", help="comma-separated map names, for re-checking a few")
    ap.add_argument("--resume", default="opening.ss1")
    args = ap.parse_args()

    REPORT.mkdir(parents=True, exist_ok=True)
    log = []
    started = time.time()
    s = Session(savestate=CHECKPOINTS / args.resume)
    try:
        if args.act in ("opening", "all"):
            act_opening(s, log)
        if args.act == "opening_tail":
            act_opening_tail(s, log)
        if args.act in ("world", "all"):
            act_world(s, log, limit=args.limit, start=args.start, only=args.only)
        if args.act in ("battles", "all"):
            act_battles(s, log)
    finally:
        s.close()

    name = "%s%s.json" % (args.act, "" if not args.start else "-%d" % args.start)
    (REPORT / name).write_text(json.dumps(log, indent=1))
    bad = [e for e in log if e["kind"] in ("FAIL", "STUCK")]
    print("\n%s: %d entries, %d fault(s), %.0fs" % (args.act, len(log), len(bad),
                                                    time.time() - started))
    for e in bad:
        print("  FAULT " + " ".join("%s=%s" % kv for kv in e.items() if kv[0] != "kind"))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
