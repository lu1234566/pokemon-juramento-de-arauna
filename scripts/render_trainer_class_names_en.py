#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "src" / "data" / "text" / "trainer_class_names.h"

REPLACEMENTS = {
    '[TRAINER_CLASS_TEAM_AQUA] = _("HORIZONTE"),': '[TRAINER_CLASS_TEAM_AQUA] = _("HORIZON"),',
    '[TRAINER_CLASS_TEAM_MAGMA] = _("LEMBRANTE"),': '[TRAINER_CLASS_TEAM_MAGMA] = _("REMEMBRANCER"),',
    '[TRAINER_CLASS_AQUA_ADMIN] = _("HORIZ. ADM"),': '[TRAINER_CLASS_AQUA_ADMIN] = _("HORIZ. ADMIN"),',
    '[TRAINER_CLASS_AQUA_LEADER] = _("HORIZONTE"),': '[TRAINER_CLASS_AQUA_LEADER] = _("HORIZON"),',
    '[TRAINER_CLASS_ELITE_FOUR] = _("CASA MAIOR"),': '[TRAINER_CLASS_ELITE_FOUR] = _("CASA MAIOR"),',
    '[TRAINER_CLASS_LEADER] = _("LIDER"),': '[TRAINER_CLASS_LEADER] = _("LEADER"),',
    '[TRAINER_CLASS_CHAMPION] = _("CAMPEA"),': '[TRAINER_CLASS_CHAMPION] = _("CHAMPION"),',
    '[TRAINER_CLASS_MAGMA_ADMIN] = _("LEMBRANTE"),': '[TRAINER_CLASS_MAGMA_ADMIN] = _("REMEMBRANCER"),',
    '[TRAINER_CLASS_MAGMA_LEADER] = _("LEMBRANTE"),': '[TRAINER_CLASS_MAGMA_LEADER] = _("REMEMBRANCER"),',
}


def render(source: str) -> str:
    out = source
    for old, new in REPLACEMENTS.items():
        count = out.count(old)
        if count != 1:
            raise ValueError(f"expected one trainer-class anchor, found {count}: {old}")
        out = out.replace(old, new, 1)
    return out


def validate(out: str) -> None:
    for old, new in REPLACEMENTS.items():
        if old != new and old in out:
            raise ValueError(f"Portuguese trainer class survived: {old}")
        if new not in out:
            raise ValueError(f"missing rendered trainer class: {new}")
    for forbidden in ('_("HORIZONTE")', '_("LEMBRANTE")', '_("LIDER")', '_("CAMPEA")'):
        if forbidden in out:
            raise ValueError(f"Portuguese trainer-class residue survived: {forbidden}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render shared Arauna trainer classes in English.")
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
        print(f"Trainer-class English overlay OK: {len(REPLACEMENTS)} exact anchors validated.")
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
