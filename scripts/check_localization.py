#!/usr/bin/env python3
"""Compatibility shim for the retired bilingual intro validator.

Arauna is English-only. The historical PT-BR/EN parity check no longer defines
release readiness; keep this filename only so old documentation/commands fail
forward into the current policy instead of silently validating an obsolete mode.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    print(
        "DEPRECATED: bilingual localization validation was retired. "
        "Running the current English-only policy check instead."
    )
    return subprocess.call(
        [sys.executable, str(ROOT / "scripts" / "check_english_only_policy.py")],
        cwd=ROOT,
    )


if __name__ == "__main__":
    raise SystemExit(main())
