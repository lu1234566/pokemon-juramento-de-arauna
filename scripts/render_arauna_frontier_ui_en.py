#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "src" / "strings.c"

REPLACEMENTS = {
    'const u8 gText_CheckFrontierMap[] = _("Check BATTLE FRONTIER MAP.");':
        'const u8 gText_CheckFrontierMap[] = _("Check CIRCUITO DE BATALHA MAP.");',
    'const u8 gText_PutAwayFrontierPass[] = _("Put away the FRONTIER PASS.");':
        'const u8 gText_PutAwayFrontierPass[] = _("Put away the CIRCUIT PASS.");',
    'const u8 gText_BattleFrontier[] = _("BATTLE FRONTIER");':
        'const u8 gText_BattleFrontier[] = _("CIRCUITO DE BATALHA");',
}


def render(source: str) -> str:
    out = source
    for old, new in REPLACEMENTS.items():
        count = out.count(old)
        if count != 1:
            raise ValueError(f"expected exactly one source anchor, found {count}: {old}")
        out = out.replace(old, new, 1)
    return out


def validate(out: str) -> None:
    for old, new in REPLACEMENTS.items():
        if old in out:
            raise ValueError(f"legacy Battle Frontier UI survived: {old}")
        if new not in out:
            raise ValueError(f"missing Battle Circuit UI target: {new}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Arauna's Battle Circuit UI in English.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.output and args.in_place:
        parser.error("use either --output or --in-place, not both")
    source = args.input.read_text(encoding="utf-8")
    out = render(source)
    validate(out)
    if args.check:
        print(f"Battle Circuit English UI OK: {len(REPLACEMENTS)} exact anchors validated.")
        return 0
    if args.in_place:
        args.input.write_text(out, encoding="utf-8")
    elif args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(out, encoding="utf-8")
    else:
        print(out, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
