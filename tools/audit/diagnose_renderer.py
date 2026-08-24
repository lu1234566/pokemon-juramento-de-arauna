#!/usr/bin/env python3
"""Diagnose one English renderer against the exact source state it will see.

The official build applies renderers in manifest order, so a renderer's source
markers must be checked *after* its predecessors have run -- not against the
pristine checkout. This driver renders the manifest up to (but excluding) the
requested renderer, reports every marker/token problem that renderer would hit,
and always restores the working tree.

Usage: python3 tools/audit/diagnose_renderer.py render_foo_en.py
"""
from __future__ import annotations

import importlib
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"


def manifest() -> list[str]:
    text = (SCRIPTS / "english_renderers.txt").read_text(encoding="utf-8")
    return [l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")]


def tracked_files() -> list[pathlib.Path]:
    out = subprocess.run(
        ["git", "ls-files", "data", "src"], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return [ROOT / p for p in out.stdout.split() if p]


def audit(module, header: str = "") -> int:
    """Report marker problems for every target group the renderer defines."""
    groups: list[tuple[str, dict, pathlib.Path]] = []
    lone_paths = [
        v for n, v in vars(module).items()
        if isinstance(v, pathlib.Path) and n != "ROOT" and v.is_file()
    ]
    for name in dir(module):
        value = getattr(module, name)
        if not isinstance(value, dict) or not value:
            continue
        if name == "TARGETS":
            prefix = ""
        elif name.endswith("_TARGETS"):
            prefix = name[: -len("_TARGETS")]
        else:
            continue
        path = None
        candidates = (
            [prefix, prefix + "_PATH", prefix + "_FILE", prefix + "_TARGET"]
            if prefix else ["TARGET", "TARGET_PATH", "PATH"]
        )
        for candidate in candidates:
            attr = getattr(module, candidate, None)
            if isinstance(attr, pathlib.Path):
                path = attr
                break
        if path is None and len(lone_paths) == 1:
            path = lone_paths[0]
        if isinstance(path, pathlib.Path):
            groups.append((name, value, path))

    # Some renderers key their targets by file ("1F", "gym", ...) and hold a
    # sibling dict mapping the same keys to paths.
    path_maps = [
        v for n, v in vars(module).items()
        if isinstance(v, dict) and v and all(isinstance(x, pathlib.Path) for x in v.values())
    ]
    for name, value in vars(module).items():
        if not isinstance(value, dict) or not value:
            continue
        if not all(isinstance(x, dict) for x in value.values()):
            continue
        for pmap in path_maps:
            if set(value) <= set(pmap):
                for key, inner in value.items():
                    groups.append((f"{name}[{key}]", inner, pmap[key]))
                break
    if not groups:
        if not header:
            print("  (no TARGETS/<PATH> pairs discovered -- inspect this renderer by hand)")
        return 0

    template = getattr(module, "BLOCK_RE_TEMPLATE", None)
    block_pattern = getattr(module, "block_pattern", None)
    shared = getattr(module, "SOURCE_MARKERS", None) or getattr(
        module, "SOURCE_SIGNATURES", None
    )

    problems = 0
    printed_header = not header
    for name, targets, path in groups:
        source = path.read_text(encoding="utf-8")
        for label, spec in targets.items():
            if template:
                pattern = re.compile(template.format(label=re.escape(label)))
            elif block_pattern:
                pattern = block_pattern(label)
            else:
                return problems
            found = list(pattern.finditer(source))
            if len(found) != 1:
                problems += 1
                if not printed_header:
                    print(f"\n### {header}")
                    printed_header = True
                print(f"  {name}/{label}: expected 1 block, found {len(found)}")
                continue
            body = found[0].group("body")
            # (markers, payloads) form, else a bare payload tuple + SOURCE_MARKERS.
            if isinstance(spec, tuple) and len(spec) == 2 and all(isinstance(p, tuple) for p in spec):
                missing = [k for k in spec[0] if k not in body]
                if missing:
                    problems += 1
                    if not printed_header:
                        print(f"\n### {header}")
                        printed_header = True
                    print(f"  {name}/{label}\n     missing markers: {missing}")
                    print(f"     body: {summarize(body)}")
            elif shared:
                if not any(k in body for k in shared):
                    problems += 1
                    if not printed_header:
                        print(f"\n### {header}")
                        printed_header = True
                    print(f"  {name}/{label}\n     no shared source marker matched")
                    print(f"     body: {summarize(body)}")
    return problems


def summarize(body: str) -> str:
    strings = " ".join(l.strip() for l in body.splitlines() if ".string" in l)
    return strings[:200] if strings else "(no .string lines)"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    wanted = sys.argv[1]
    entries = manifest()
    sweep = wanted == "--all"
    if not sweep and wanted not in entries:
        print(f"{wanted} is not in the official manifest")
        return 2

    backup = pathlib.Path(tempfile.mkdtemp())
    files = tracked_files()
    for f in files:
        dest = backup / f.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dest)
    try:
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / "cleanup_region_map_names.py")],
            cwd=ROOT, check=True, capture_output=True,
        )
        sys.path.insert(0, str(SCRIPTS))
        problems = 0
        for entry in entries:
            if not sweep and entry == wanted:
                break
            if sweep:
                # Audit each renderer against the state its predecessors left.
                module = importlib.import_module(entry[:-3])
                found = audit(module, header=entry)
                problems += found
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / entry), "--in-place"],
                cwd=ROOT, capture_output=True, text=True,
            )
            if result.returncode != 0 and sweep:
                last = result.stderr.strip().splitlines()[-1:] or ["(no stderr)"]
                print(f"  !! {entry} still fails: {last[0]}")
        if not sweep:
            module = importlib.import_module(wanted[:-3])
            print(f"Diagnosing {wanted} against its real pre-render state:\n")
            problems = audit(module)
        print(f"\n{problems} marker problem(s).")
        return 1 if problems else 0
    finally:
        for f in files:
            src = backup / f.relative_to(ROOT)
            if src.exists():
                shutil.copy2(src, f)
        shutil.rmtree(backup, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
