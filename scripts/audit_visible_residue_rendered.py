#!/usr/bin/env python3
"""Compatibility entrypoint for the retired hand-composed rendered audit.

The current project must be rendered through scripts/english_renderers.txt in its
locked order. This wrapper therefore delegates to the canonical static-readiness
entrypoint instead of maintaining another renderer list.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    print(
        "NOTE: audit_visible_residue_rendered.py now delegates to "
        "scripts/check_arauna_static.sh."
    )
    return subprocess.call(["bash", "scripts/check_arauna_static.sh"], cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
