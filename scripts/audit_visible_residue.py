#!/usr/bin/env python3
"""Compatibility entrypoint for the old visible-residue inventory.

The project is English-only now. The former scanner classified ordinary English
as a localization problem and manually composed an obsolete subset of renderers,
so it is no longer authoritative. This wrapper keeps old references usable while
routing them to the current English-visible inventory.

For the authoritative rendered composition, run:
    bash scripts/check_arauna_static.sh
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    print(
        "NOTE: audit_visible_residue.py is a compatibility wrapper. "
        "English text is not residue; use check_arauna_static.sh for the official rendered composition."
    )
    return subprocess.call(
        [sys.executable, str(ROOT / "scripts" / "audit_rendered_visible_residue_en.py")],
        cwd=ROOT,
    )


if __name__ == "__main__":
    raise SystemExit(main())
