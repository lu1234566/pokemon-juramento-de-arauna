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
from pilot import Pilot, Stuck                                  # noqa: E402
from play import CHECKPOINTS, Session                           # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]

# The road north of the village is shut until the rival has been met.
VAR_LITTLEROOT_TOWN_STATE = 0x4050
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
    for _ in range(40):
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
                where = p.where()
                p.walk_to(where[2], max(1, where[3] - 4))
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
    colours = collections.Counter(crop.getdata())
    total = sum(colours.values())
    top, count = colours.most_common(1)[0]
    faults = []
    if count / total > 0.97:
        faults.append("the screen is one flat colour %s" % (top,))
    elif len(colours) < 8:
        faults.append("the screen has %d colours in it" % len(colours))
    return faults


def act_world(s: Session, log, limit=None, start=0):
    p = Pilot(s)
    print("[world]")
    shots = REPORT / "world"
    shots.mkdir(parents=True, exist_ok=True)
    targets = [(gn, name) for gn, name in sorted(p.maps.items())
               if not name.startswith(SKIP_PREFIXES)]
    targets = targets[start:][:limit] if limit else targets[start:]
    seen = 0
    for (group, num), name in targets:
        seen += 1
        try:
            s.warp(group, num, 5, 5)
        except Exception as why:                        # noqa: BLE001
            note(log, "FAIL", map=name, detail="warp failed: %s" % why)
            continue
        s.probe.run(1.5)
        callback = s.probe.callback2_name()
        where = p.where()
        if callback != "CB2_Overworld":
            note(log, "FAIL", map=name, detail="the field never came up (%s)" % callback)
            continue
        grid = p.grid()
        if grid is not None and where is not None and not grid.inside(where[2], where[3]):
            note(log, "FAIL", map=name, detail="landed outside the map at %d,%d" % where[2:])
            continue
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
def act_battles(s: Session, log, spots=None):
    p = Pilot(s)
    print("[battles]")
    spots = spots or [("Route101", 0, 16, 8, 12), ("Route102", 0, 17, 12, 8),
                      ("Route116", 0, 32, 20, 8)]
    for name, group, num, x, y in spots:
        s.warp(group, num, x, y)
        s.probe.run(2.0)
        started = False
        for _ in range(30):
            for move in ("left", "right"):
                s.hold(move, 0.5)
                s.probe.run(0.4)
                if s.probe.callback2_name() != "CB2_Overworld":
                    started = True
                    break
            if started:
                break
        if not started:
            note(log, "note", map=name, detail="no wild encounter in 30 paces")
            continue
        s.probe.run(4.0)
        s.shot("pt_battle_%s" % name)
        note(log, "battle", map=name, callback=s.probe.callback2_name())
        for _ in range(40):                            # run away
            s.press("b", 1)
            s.probe.run(0.8)
            if s.probe.callback2_name() == "CB2_Overworld":
                break
        if s.probe.callback2_name() != "CB2_Overworld":
            note(log, "FAIL", map=name, detail="the battle did not end")
        else:
            note(log, "battle-end", map=name, state="back on the field")
    return p


ACTS = {"opening": act_opening, "opening_tail": act_opening_tail,
        "world": act_world, "battles": act_battles}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("act", choices=sorted(ACTS) + ["all"])
    ap.add_argument("--limit", type=int)
    ap.add_argument("--start", type=int, default=0)
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
            act_world(s, log, limit=args.limit, start=args.start)
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
