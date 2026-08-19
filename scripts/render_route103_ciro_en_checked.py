#!/usr/bin/env python3
from __future__ import annotations

import render_route103_ciro_en as base

markers, _ = base.TARGETS["Route103_Text_ShortcutToOldale"]
base.TARGETS["Route103_Text_ShortcutToOldale"] = (
    markers,
    (
        "Across the water is a shortcut\\n",
        "back to VILA DA PASSAGEM.\\p",
        "Useful if you can cross the sea.$",
    ),
)
markers, _ = base.TARGETS["Route103_Text_RouteSign"]
base.TARGETS["Route103_Text_RouteSign"] = (
    markers,
    (
        "ROUTE 103\\n",
        "{DOWN_ARROW} VILA DA PASSAGEM$",
    ),
)


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
