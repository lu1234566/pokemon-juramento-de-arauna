#!/usr/bin/env python3
from __future__ import annotations

import render_anahi_lab_en as base

# One inherited/unused Johto-starter nickname block contains neither a character
# name nor the other Portuguese Arauna markers used by the main renderer. Keep
# its original visible word as an explicit source anchor rather than weakening
# validation for all 50 lab blocks.
base.SOURCE_MARKERS += ("apelido",)


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
