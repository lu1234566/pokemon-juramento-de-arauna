#!/usr/bin/env python3
"""Drive the built ROM in mGBA with a closed loop on the game's own state.

The earlier harness pressed keys on a timer and hoped. That missed the title
screen three times out of four, because how long the intro takes depends on
the machine. This one asks the game where it is -- gba_probe reads the active
MainCB2 straight out of memory -- and only then decides what to press.

    python3 tools/audit/play.py --to overworld --shot title,overworld
    python3 tools/audit/play.py --resume checkpoints/overworld.ss1 --to gym

Checkpoints are mGBA savestates, so a later run starts from a reached point
instead of replaying the intro.
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gba_probe import Probe                                    # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
ROM = ROOT / "pokemon-juramento-de-arauna-en_modern.gba"
CHECKPOINTS = ROOT / "build" / "arauna-en" / "checkpoints"
DISPLAY = ":99"

# mGBA's SDL frontend maps the GBA buttons onto these keys by default.
KEY = {"a": "x", "b": "z", "start": "Return", "select": "BackSpace",
       "up": "Up", "down": "Down", "left": "Left", "right": "Right",
       "l": "a", "r": "s"}


def sh(*cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def pause(seconds: float) -> None:
    # `sleep` is not available in this environment; a timed blocking read is.
    subprocess.run(["timeout", str(seconds), "tail", "-f", "/dev/null"],
                   capture_output=True)


class Session:
    def __init__(self, rom: pathlib.Path = ROM, savestate: pathlib.Path | None = None,
                 shots: pathlib.Path | None = None):
        self.rom = rom
        self.shots = shots or (ROOT / "build" / "arauna-en" / "shots")
        self.shots.mkdir(parents=True, exist_ok=True)
        self._start(savestate)
        self.probe = Probe()

    def _start(self, savestate: pathlib.Path | None) -> None:
        for name in ("mgba", "matchbox-window-manager", "Xvfb"):
            sh("pkill", "-x", name)
        pause(1.5)
        subprocess.Popen(["Xvfb", DISPLAY, "-screen", "0", "1024x768x24"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        pause(2)
        env = {"DISPLAY": DISPLAY, "SDL_AUDIODRIVER": "dummy",
               "LIBGL_ALWAYS_SOFTWARE": "1", "PATH": "/usr/bin:/bin:/usr/games"}
        # A window manager makes input focus deterministic; XTEST alone is not.
        subprocess.Popen(["matchbox-window-manager", "-use_cursor", "no"], env=env,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        pause(1.5)
        cmd = ["/usr/games/mgba", "-g", "-1"]
        if savestate:
            cmd += ["-t", str(savestate)]
        cmd.append(str(self.rom))
        self.mgba = subprocess.Popen(cmd, env=env,
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        pause(4)
        self.env = env
        found = sh("xdotool", "search", "--name", "mGBA", env=env)
        ids = [i for i in found.stdout.split() if i]
        if not ids:
            raise SystemExit("no mGBA window appeared")
        self.window = ids[-1]
        sh("xdotool", "windowactivate", self.window, env=env)
        pause(1)

    # -- input and capture ------------------------------------------------
    def press(self, button: str, times: int = 1, settle: float = 0.25) -> None:
        """Tap a button.

        `xdotool key` sends the press and release microseconds apart, and mGBA
        polls SDL once a frame -- both events can land between two polls and
        the button is never seen down. Holding it for a few frames makes every
        press register.
        """
        for _ in range(times):
            self.hold(button, 0.12)
            pause(settle)

    def hold(self, button: str, seconds: float = 0.45) -> None:  # noqa: D401
        """Hold a button down. Walking needs the key held across frames;
        a tap only registers as a turn."""
        key = KEY.get(button, button)
        self.probe.cont()
        # Give the emulator a moment to actually be running before the key
        # lands, or the first press after a halt is swallowed.
        pause(0.10)
        sh("xdotool", "keydown", "--clearmodifiers", "--window", self.window, key,
           env=self.env)
        pause(seconds)
        sh("xdotool", "keyup", "--clearmodifiers", "--window", self.window, key,
           env=self.env)
        pause(0.15)
        self.probe.halt()

    def walk(self, button: str, steps: int = 1) -> None:
        for _ in range(steps):
            self.hold(button)

    def dex_goto(self, national_dex: int) -> int:
        """Scroll the open Pokedex list to an entry with the D-pad.

        Deliberately not a memory write: the list loads the selected sprite as
        it scrolls, so poking the index shows the entry's text next to the
        previous entry's artwork.
        """
        current = self.probe.dex_selected()
        delta = national_dex - current
        if delta:
            self.press("down" if delta > 0 else "up", abs(delta), settle=0.02)
            self.probe.run(1.2)             # let the list settle on the sprite
        return self.probe.dex_selected()

    def shot(self, name: str) -> pathlib.Path:
        path = self.shots / f"{name}.png"
        sh("import", "-window", self.window, str(path), env=self.env)
        return path

    def savestate(self, name: str, slot: int = 1) -> pathlib.Path:
        """Write an mGBA savestate and file it under a readable name.

        mGBA drops the state next to the ROM as <rom>.ss<slot>; a run that
        resumes wants it by waypoint name, not slot number.
        """
        self.probe.cont()
        sh("xdotool", "key", "--clearmodifiers", "--window", self.window,
           f"shift+F{slot}", env=self.env)
        pause(1.5)
        self.probe.halt()
        produced = self.rom.with_suffix(f".ss{slot}")
        if not produced.is_file():
            raise SystemExit(f"mGBA wrote no savestate at {produced}")
        target = CHECKPOINTS / f"{name}.ss{slot}"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(produced.read_bytes())
        produced.unlink()
        return target

    # -- the closed loop --------------------------------------------------
    def wait_for(self, predicate, timeout: float = 60.0, step: float = 0.25,
                 button: str | None = None, label: str = "") -> bool:
        """Run (optionally tapping a button) until the game reaches a state."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if predicate(self.probe):
                return True
            if button:
                self.press(button)
            else:
                self.probe.run(step)
        print(f"  timed out waiting for {label or predicate}", file=sys.stderr)
        return False

    def wait_callback(self, *names: str, **kw) -> bool:
        wanted = set(names)
        return self.wait_for(lambda p: p.callback2_name() in wanted,
                             label="callback " + "/".join(names), **kw)

    def close(self) -> None:
        self.probe.close()
        for name in ("mgba", "matchbox-window-manager", "Xvfb"):
            sh("pkill", "-x", name)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--resume", type=pathlib.Path, help="mGBA savestate to boot from")
    ap.add_argument("--watch", type=float, default=0,
                    help="just report the game state for N seconds")
    args = ap.parse_args()

    session = Session(savestate=args.resume)
    try:
        if args.watch:
            deadline = time.time() + args.watch
            while time.time() < deadline:
                print(" ", session.probe.summary())
                session.probe.run(1.0)
            return 0
        print("state:", session.probe.summary())
        return 0
    finally:
        session.close()


if __name__ == "__main__":
    raise SystemExit(main())
