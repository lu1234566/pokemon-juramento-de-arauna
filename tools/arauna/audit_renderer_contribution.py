#!/usr/bin/env python3
"""Which English renderers write text a player never sees.

The manifest is ordered and the renderers overwrite whole text blocks, so the
last renderer to touch a block wins -- silently. A renderer whose blocks are
all claimed further down the manifest still passes its own --check, still
passes every gate, and still contributes nothing to the ROM. That is a hard
mistake to notice by reading, because the failure is the absence of a symptom.

So: run the chain once, record the lines each renderer adds, and ask whether
those lines are still there when the chain finishes.

Two things this deliberately does not call a fault. A renderer that changes
nothing is healthy -- its output is already the committed state, which is true
of the ones whose surface was rendered into the tree long ago. And a renderer
cannot simply be re-run at the end as a check, because almost none of them are
idempotent: they anchor to markers in the source and consume those markers as
they write, so a second run fails by design rather than by accident.

Partial survival is reported but is not always a fault either -- the manifest
says order is significant where surfaces overlap, and a later renderer refining
part of an earlier one's file is intended. Nothing surviving is the signal that
matters.

It rewrites the working tree while it runs, so it refuses to start on a dirty
one and restores from git at the end.

  (no arguments)  audit every renderer in the manifest
  --verbose       also list the renderers that land everything they write
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "scripts" / "english_renderers.txt"
WATCHED = ("data", "src")


def renderers() -> list[str]:
    lines = MANIFEST.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines
            if line.strip() and not line.lstrip().startswith("#")]


def tracked() -> list[Path]:
    out = subprocess.run(["git", "ls-files", *WATCHED], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    return [ROOT / name for name in out.split()]


def snapshot(files: list[Path]) -> dict[Path, str]:
    return {path: path.read_text(encoding="utf-8", errors="surrogateescape")
            for path in files if path.is_file()}


def added(before: dict[Path, str], after: dict[Path, str]) -> dict[Path, set[str]]:
    """The lines a renderer put into each file that were not there before."""
    new: dict[Path, set[str]] = {}
    for path, text in after.items():
        was = before.get(path, "")
        if was == text:
            continue
        lines = set(text.splitlines()) - set(was.splitlines())
        if lines:
            new[path] = lines
    return new


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    dirty = subprocess.run(["git", "status", "--porcelain", *WATCHED], cwd=ROOT,
                           capture_output=True, text=True, check=True).stdout.strip()
    if dirty:
        print("refusing to run: the working tree has uncommitted changes under "
              "data/ or src/, and this rewrites both", file=sys.stderr)
        return 2

    files = tracked()
    try:
        subprocess.run([sys.executable, "tools/cleanup_region_map_names.py"],
                       cwd=ROOT, capture_output=True, check=True)
        state = snapshot(files)
        written: list[tuple[str, dict[Path, set[str]]]] = []
        for name in renderers():
            done = subprocess.run([sys.executable, f"scripts/{name}", "--in-place"],
                                  cwd=ROOT, capture_output=True, text=True)
            if done.returncode != 0:
                print(f"the chain itself fails at {name}:\n{done.stderr}", file=sys.stderr)
                return 2
            after = snapshot(files)
            written.append((name, added(state, after)))
            state = after
        final = state
    finally:
        subprocess.run(["git", "checkout", "--", *WATCHED], cwd=ROOT, check=True)

    dead, partial, ok = [], [], []
    for name, lines_by_file in written:
        wrote = sum(len(lines) for lines in lines_by_file.values())
        if wrote == 0:
            ok.append(f"{name}: writes what the tree already holds")
            continue
        survived = sum(len(lines & set(final[path].splitlines()))
                       for path, lines in lines_by_file.items())
        if survived == 0:
            dead.append(f"DEAD    {name}: wrote {wrote} lines, none reach the ROM")
        elif survived < wrote:
            partial.append(f"partial {name}: {survived} of {wrote} lines reach the ROM")
        else:
            ok.append(f"{name}: {wrote} lines")

    for line in dead:
        print(line)
    for line in partial:
        print(line)
    if args.verbose:
        for line in ok:
            print(f"ok      {line}")

    if dead:
        print(f"\n{len(dead)} renderer(s) write text the ROM never receives.")
        return 1
    print(f"\nall {len(written)} renderers land text; "
          f"{len(partial)} share a surface with a later one.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
