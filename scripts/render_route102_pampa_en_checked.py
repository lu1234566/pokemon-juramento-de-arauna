#!/usr/bin/env python3
from __future__ import annotations

import render_route102_pampa_en as base

markers, _ = base.CITY_TARGETS["PetalburgCity_Text_GymSign"]
base.CITY_TARGETS["PetalburgCity_Text_GymSign"] = (
    markers,
    (
        "PAMPA DA ESPERA GYM\\n",
        "LEADER: ELIAS\\p",
        "Returning doesn't erase\\n",
        "the road.$",
    ),
)


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
