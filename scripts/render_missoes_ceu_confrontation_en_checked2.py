#!/usr/bin/env python3
from __future__ import annotations

import render_missoes_ceu_confrontation_en_checked as english


english.english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_WouldveLikedToBeAstronaut"] = (
    "MAN: When I was young, I wanted\\n",
    "to see Arauna from above.\\p",
    "Maybe I can still learn.$",
)
english.english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_Grunt7Defeat"] = (
    "REMEMBRANCER: Exposing truth\\n",
    "shouldn't require taking a\\n",
    "whole network.$",
)
english.english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_StevenWhyStealRocketFuel"] = (
    "SEU BENTO: Stopping HORIZON does\\n",
    "not require taking city systems.\\p",
    "Who authorized you?$",
)
english.english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_StevenAreYouReadyToBattle"] = (
    "SEU BENTO: {PLAYER}, I'll stop\\n",
    "this takeover.\\p",
    "Fight with me?$",
)
english.english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_MaxieWeFailedIsAquaAlsoMisguided"] = (
    "LUZIA: I understand.\\p",
    "Taking the network to block\\n",
    "control still means taking it.$",
)
english.english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_MaxieWeWillGiveUp"] = (
    "LUZIA: We're leaving.\\p",
    "The M'BOI evidence still exists.\\p",
    "I'll find another way to share.$",
)


def main() -> int:
    return english.main()


if __name__ == "__main__":
    raise SystemExit(main())
