#!/usr/bin/env python3
from __future__ import annotations

import render_porto_sal_museum_science_en as english


def patch(targets, label: str, payloads: tuple[str, ...]) -> None:
    markers, _ = targets[label]
    targets[label] = (markers, payloads)


patch(english.base.TARGETS_1F, "SlateportCity_OceanicMuseum_1F_Text_BeachSandDisplay", (
    "SAMPLE: COASTAL SAND\\p",
    "Stone travels down rivers and\\n",
    "wears away on the journey.\\p",
    "Small grains form beaches.$",
))
patch(english.base.TARGETS_2F, "SlateportCity_OceanicMuseum_2F_Text_HoennModel", (
    "MODEL OF ARAUNA\\p",
    "A miniature shows cities and\\n",
    "rivers, ridges and coastal routes.$",
))
patch(english.base.TARGETS_2F, "SlateportCity_OceanicMuseum_2F_Text_RemindsMeOfAbandonedShip", (
    "VISITOR: That model reminds me\\n",
    "of a ship stranded on the coast.$",
))
patch(english.base.TARGETS_2F, "SlateportCity_OceanicMuseum_2F_Text_DontRunInMuseum", (
    "VISITOR: No running in here,\\n",
    "all right?$",
))


def main() -> int:
    return english.main()


if __name__ == "__main__":
    raise SystemExit(main())
