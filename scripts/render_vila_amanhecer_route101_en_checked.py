#!/usr/bin/env python3
from __future__ import annotations

import render_vila_amanhecer_route101_en as base

markers, _ = base.ROUTE_TARGETS["Route101_Text_RouteSign"]
base.ROUTE_TARGETS["Route101_Text_RouteSign"] = (
    markers,
    (
        "ROUTE 101\\n",
        "{UP_ARROW} VILA DA PASSAGEM$",
    ),
)


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
