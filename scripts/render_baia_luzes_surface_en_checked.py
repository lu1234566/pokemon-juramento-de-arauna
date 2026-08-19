#!/usr/bin/env python3
from __future__ import annotations

import render_baia_luzes_surface_en as english


english.TARGETS["LilycoveCity_Text_DontGoNearCaveInCove"] = (
    ("cave in the cove", "adult"),
    (
        "HORIZON: That service tunnel is\\n",
        "restricted.\\p",
        "Please use the public pier.$",
    ),
)
english.TARGETS["LilycoveCity_Text_SomeoneStoleMyPokemon"] = (
    ("stole my POKéMON", "CONSORCIO HORIZONTE"),
    (
        "I fell asleep to the waves...\\p",
        "When I woke, my POKéMON was gone.\\p",
        "I blamed HORIZON immediately.\\n",
        "Maybe I was too quick.$",
    ),
)
english.TARGETS["LilycoveCity_Text_SeaRemainsForeverYoung"] = (
    ("sea remains forever young",),
    (
        "I have watched this water for\\n",
        "most of my life.\\p",
        "The coast changes. The tide\\n",
        "still returns.$",
    ),
)
english.TARGETS["LilycoveCity_Text_SawTallTowerOnRoute131"] = (
    ("tall tower", "ROUTE 131"),
    (
        "I saw a tall tower far west.\\p",
        "Could it be TORRE DO JURAMENTO?$",
    ),
)
english.TARGETS["LilycoveCity_Text_JustArrivedAndSawRarePokemon"] = (
    ("honeymoon vacation", "DRAGON-type"),
    (
        "We arrived for our honeymoon.\\p",
        "We saw a huge POKéMON silhouette\\n",
        "high above the sea.\\p",
        "Arauna already surprised us.$",
    ),
)
english.TARGETS["LilycoveCity_Text_HoneymoonVowToSeeRarePokemon"] = (
    ("honeymoon", "rare POKéMON"),
    (
        "We promised to see as many rare\\n",
        "POKéMON as we could together.\\p",
        "We saw one on our first day.$",
    ),
)


def main() -> int:
    return english.main()


if __name__ == "__main__":
    raise SystemExit(main())
