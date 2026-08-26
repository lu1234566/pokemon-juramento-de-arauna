#!/usr/bin/env python3
"""Drive the game the way a player does: to a place, not for a number of frames.

`play.Session` can press a button and `gba_probe.Probe` can read where the
player is standing. What was missing between them is the thing every playtest
needs and no amount of button-mashing gives you - "walk over there". A blind
`hold("right", 4)` walks into the first fence it meets and the run silently
stops testing anything.

So this plans the walk on the map's own collision data, the same block grid the
gate reads, and then checks after every step that the player actually moved.
Anything that blocks a planned step is something the grid does not know about -
a person, a script, a closed door - so the plan is thrown away and redrawn from
where the player really is. A walk that stops making progress is reported as a
failure rather than passing quietly.

    from pilot import Pilot
    p = Pilot(session)
    p.walk_to(8, 5)          # on the map the player is standing in
    p.talk()                 # press A and read whatever comes back
"""
from __future__ import annotations

import collections
import json
import os
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from map_invariants import DIRECTIONS, LEDGE_JUMPS, TownMap  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]

# How many replans a single walk is allowed before it is called stuck. A person
# pacing across a doorway can block a step for several seconds, so this is
# generous; a wall never clears, so it still terminates.
REPLANS = 8

# A tap, and the time a step needs to finish. Holding a direction is how a
# person walks and it is the wrong primitive here: the same 0.75s hold walks
# three tiles down a corridor and none at all into a wall, so a harness that
# measures after each hold cannot tell overshooting from being blocked. A tap
# is exact instead - the game starts a whole sixteen-frame step from a single
# frame of input and finishes it with the key already released - and the only
# thing a tap can do other than step is turn, which is visible as "did not
# move" and is retried once.
TAP = 0.06
STEP_SETTLE = 0.38


def map_registry():
    """(group, number) -> folder name, for every map in the game."""
    groups = json.load(open(ROOT / "data/maps/map_groups.json", encoding="utf-8"))
    out = {}
    for group, name in enumerate(groups["group_order"]):
        for num, map_name in enumerate(groups[name]):
            out[(group, num)] = map_name
    return out


class Stuck(Exception):
    """A walk stopped making progress."""


class Pilot:
    def __init__(self, session):
        self.s = session
        self.probe = session.probe
        self.maps = map_registry()
        self._grids = {}

    # -- where we are ------------------------------------------------------
    def where(self, wait: float = 0.0):
        """(mapGroup, mapNum, x, y), or None if the save block is not up yet.

        There is a window at the very start of a new game where the arrival
        scene has finished and gSaveBlock1Ptr is still null; asking for a
        position inside it answers None, and a caller that indexes the answer
        crashes on the truck's tailgate. Callers that need a position say how
        long they are prepared to wait for one.
        """
        deadline = time.time() + wait
        while True:
            here = self.probe.location()
            if here is not None or time.time() >= deadline:
                return here
            self.probe.run(0.25)

    def map_name(self):
        where = self.where()
        return None if where is None else self.maps.get((where[0], where[1]))

    def grid(self):
        """The block grid of the map the player is standing in."""
        name = self.map_name()
        if name is None:
            return None
        if name not in self._grids:
            try:
                self._grids[name] = TownMap(name, str(ROOT))
            except (FileNotFoundError, StopIteration, SystemExit):
                self._grids[name] = None
        return self._grids[name]

    # -- messages ----------------------------------------------------------
    def locked(self):
        """The game's own answer to "can the player step?".

        Reading the task list for `Task_DrawFieldMessage` is not that answer.
        A script can have a box on screen and be waiting on input with that
        task already gone, and then a harness that trusts the task list walks
        confidently into a locked player and reports eight attempts of nothing.
        `gPlayerAvatar.preventStep` is the flag the game itself checks.
        """
        return bool(self.probe.u8(self.probe.sym["gPlayerAvatar"] + 6))

    def message_up(self):
        """Is a field message box on screen? (sFieldMessageBoxMode != 0)"""
        return bool(self.probe.u8(self.probe.sym["sFieldMessageBoxMode"]))

    def controls_locked(self):
        """Is a script holding the field controls?

        This is the one that catches a cutscene. `preventStep` is clear and the
        avatar still reports itself controllable while a script runs, so the
        harness sees a free player, holds a direction, watches `gMain.heldKeys`
        light up with the right bit - and nothing moves, because
        `FieldGetPlayerInput` is never reached. `sLockFieldControls` is what
        `ArePlayerFieldControlsLocked` reads.
        """
        return bool(self.probe.u8(self.probe.sym["sLockFieldControls"]))

    def busy(self):
        """Is a script, a message box or a doorway holding the player still?"""
        if self.locked() or self.message_up() or self.controls_locked():
            return True
        tasks = self.probe.active_tasks()
        return any(t in tasks for t in ("Task_WarpAndLoadMap", "Task_ExitNonAnimDoor",
                                        "Task_ExitDoor", "Task_EnterDoor"))

    def advance(self, presses=1, settle=1.2):
        """Push A through whatever is on screen."""
        for _ in range(presses):
            self.s.press("a", 1)
            self.probe.run(settle)

    def wait_free(self, seconds=12.0):
        """Wait until nothing is holding the player, then say whether it worked."""
        waited = 0.0
        while waited < seconds:
            if not self.busy():
                return True
            self.probe.run(1.0)
            waited += 1.0
        return not self.busy()

    def clear_messages(self, tries=12):
        """Read a conversation to its end.

        A is the right button and B is not: B closes the box a script is
        waiting on and the script simply opens it again, so a B-loop looks
        exactly like a hang. A advances it.
        """
        for _ in range(tries):
            if not self.busy():
                return True
            self.s.press("a", 1)
            self.probe.run(1.0)
        return not self.busy()

    # -- walking -----------------------------------------------------------
    def _open(self, grid, x, y):
        return grid.inside(x, y) and (grid.walkable(x, y) or grid.surfable(x, y))

    def plan(self, grid, start, goal):
        """A shortest path over the map's own collision and elevation rules."""
        if start == goal:
            return []
        seen = {start: None}
        queue = collections.deque([start])
        while queue:
            x, y = queue.popleft()
            here = grid.elevation(x, y)
            for name, (dx, dy) in DIRECTIONS.items():
                nx, ny = x + dx, y + dy
                step = None
                if self._open(grid, nx, ny) and (nx, ny) not in seen:
                    there = grid.elevation(nx, ny)
                    if here == there or here in (0, 15) or there in (0, 15):
                        step = (nx, ny)
                if step is None and LEDGE_JUMPS.get(
                        grid.behavior(nx, ny) if grid.inside(nx, ny) else -1) == (dx, dy):
                    land = (x + dx * 2, y + dy * 2)
                    if self._open(grid, *land) and land not in seen:
                        step = land
                if step is None or step in seen:
                    continue
                seen[step] = (x, y, name)
                if step == goal:
                    path = []
                    at = step
                    while seen[at] is not None:
                        px, py, how = seen[at]
                        path.append(how)
                        at = (px, py)
                    return list(reversed(path))
                queue.append(step)
        return None

    def step(self, direction):
        """Take exactly one step, or report that something is in the way.

        The first tap may only turn the player, which is not a failure - it is
        what the game does when the button is not the way they are facing - so
        it is worth a second tap before calling the square blocked.
        """
        for _ in range(2):
            before = self.where()
            self.s.hold(direction, TAP)
            self.probe.run(STEP_SETTLE)
            after = self.where()
            if after is None or after[:2] != before[:2]:
                return "warped"
            if after[2:] != before[2:]:
                return "moved"
        return "blocked"

    def walk_to(self, x, y):
        """Walk to a square, replanning around whatever the grid cannot see."""
        grid = self.grid()
        if grid is None:
            raise Stuck("no block grid for %s" % (self.map_name(),))
        goal = (x, y)
        for _ in range(REPLANS):
            # A script that is still running blocks every step, and a harness
            # that does not deal with it reads that as a wall and gives up on a
            # perfectly open corridor. Waiting is not enough either: most of
            # what holds the controls is a person talking, and they hold them
            # until somebody presses A.
            if not self.clear_messages(20):
                raise Stuck("something is still holding the controls on %s" % self.map_name())
            where = self.where()
            start = (where[2], where[3])
            if start == goal:
                return True
            path = self.plan(grid, start, goal)
            if path is None:
                raise Stuck("no way from %d,%d to %d,%d on %s"
                            % (start[0], start[1], x, y, self.map_name()))
            for move in path:
                outcome = self.step(move)
                if outcome == "warped":
                    return True              # a door took us somewhere else
                if outcome == "blocked":
                    break                    # replan around whatever it is
                if self.where()[2:] == goal:
                    return True
        return self.where()[2:] == goal

    def use_warp(self, x, y, tries=4):
        """Go through the door at a square, however that door works.

        A door is not somewhere you can stand. Almost every warp in the game
        sits on a solid block - the front of a house, the tailgate of the truck
        - and fires when the player walks *into* it, so a harness that plans a
        path onto the square finds no path and calls the front door of the
        player's own house broken. A staircase or a hole is the other kind, and
        that one really is stood on.

        So: stand on the square the door is approached from - below it by
        preference, because that is where a doorstep is - and then push.
        """
        here = self.where(wait=10.0)
        if here is None:
            raise Stuck("the game has no position to warp from")
        was = here[:2]
        grid = self.grid()
        if grid is not None and grid.walkable(x, y):
            self.walk_to(x, y)
            for _ in range(6):
                if self.where()[:2] != was:
                    return True
                self.probe.run(1.0)

        approaches = []
        for name, (dx, dy) in DIRECTIONS.items():
            step_from = (x - dx, y - dy)
            if grid is not None and grid.inside(*step_from) and grid.walkable(*step_from):
                approaches.append((0 if name == "up" else 1, name, step_from))
        for _, name, step_from in sorted(approaches):
            if self.where()[:2] != was:
                return True
            try:
                self.walk_to(*step_from)
            except Stuck:
                continue
            if self.where()[2:] != step_from:
                continue
            for _ in range(tries):
                if self.where()[:2] != was:
                    return True
                self.s.hold(name, 0.25)
                self.probe.run(1.3)
        if self.where()[:2] == was:
            raise Stuck("the door at %d,%d on %s did not open"
                        % (x, y, self.map_name()))
        return True

    def face_and_talk(self, x, y):
        """Stand next to a square, turn to it, and read what it says."""
        where = self.where()
        dx, dy = x - where[2], y - where[3]
        for name, (mx, my) in DIRECTIONS.items():
            if (mx, my) == (max(-1, min(1, dx)), max(-1, min(1, dy))):
                self.s.press(name, 1)
                break
        self.probe.run(0.4)
        self.s.press("a", 1)
        self.probe.run(1.2)
        return self.clear_messages()
