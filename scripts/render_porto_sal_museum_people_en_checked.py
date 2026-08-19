#!/usr/bin/env python3
from __future__ import annotations

import render_porto_sal_museum_people_en as english

base = english.base


def patch(targets, label: str, payloads: tuple[str, ...]) -> None:
    markers, _ = targets[label]
    targets[label] = (markers, payloads)


patch(base.CITY_TARGETS, "SlateportCity_Text_WhatsLongLineOverThere", (
    "MAN: What's happening there?\\p",
    "Look at that line.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_VisitedMuseumOften", (
    "WOMAN: I came here often as a\\n",
    "kid.\\p",
    "This museum taught me to love\\n",
    "the mysteries of the sea.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_AquaHasPolicy", (
    "HORIZON: Orders say enter\\n",
    "quietly.\\p",
    "So yes, we're paying admission.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_OurBossIsntHere", (
    "HORIZON: OTACILIO isn't here.\\p",
    "We were only meant to observe.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_WouldStuffHereMakeMeRich", (
    "HORIZON: Some gear is costly.\\p",
    "No, we're not here to steal it.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_RustboroBungled", (
    "HORIZON: If the last operation\\n",
    "had worked, I wouldn't be here.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_DidntHaveMoney", (
    "HORIZON: I paid ¥50 too.\\p",
    "Orders are orders.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_LearnAboutSeaForBattling", (
    "VISITOR: I came to study the sea\\n",
    "to understand my POKéMON better.$",
))


def main() -> int:
    return english.main()


if __name__ == "__main__":
    raise SystemExit(main())
