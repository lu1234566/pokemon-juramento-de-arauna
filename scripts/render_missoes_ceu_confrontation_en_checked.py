#!/usr/bin/env python3
from __future__ import annotations

import render_missoes_ceu_confrontation_en as english


english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_MossdeepIdealForRockets"] = (
    "SCIENTIST: MISSOES DO CEU has\\n",
    "steady winds and open horizon.\\p",
    "Our antennas cover Arauna.$",
)
english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_MagmaCantGetAwayWithThis"] = (
    "MAN: Cutting a civilian network\\n",
    "hurts people who never chose\\n",
    "this fight.$",
)
english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_Grunt5Intro"] = (
    "REMEMBRANCER: If HORIZON links\\n",
    "this network to the LIVING\\n",
    "ARCHIVE, orders reach Arauna.$",
)
english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_Grunt5PostBattle"] = (
    "REMEMBRANCER: Civilians use this\\n",
    "network too. I know.$",
)
english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_Grunt6PostBattle"] = (
    "REMEMBRANCER: If HORIZON keeps\\n",
    "that key, it can trigger sensors\\n",
    "from afar.$",
)
english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_Grunt7Intro"] = (
    "REMEMBRANCER: LUZIA wants to air\\n",
    "M'BOI records before breaking\\n",
    "the key.$",
)
english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_Grunt7Defeat"] = (
    "REMEMBRANCER: Exposing truth\\n",
    "shouldn't require taking the whole\\n",
    "network.$",
)
english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_MaxieDontInterfere"] = (
    "LUZIA: HORIZON can use this link\\n",
    "to command the ARCHIVE across\\n",
    "Arauna. I won't allow it.$",
)
english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_StevenWhyStealRocketFuel"] = (
    "SEU BENTO: Stopping HORIZON does\\n",
    "not require taking a city network.\\p",
    "Who authorized you?$",
)
english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_StevenAreYouReadyToBattle"] = (
    "SEU BENTO: {PLAYER}, I'll stop this\\n",
    "takeover.\\p",
    "Fight with me?$",
)
english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_MaxieWeFailedIsAquaAlsoMisguided"] = (
    "LUZIA: I understand.\\p",
    "Taking the network to stop control\\n",
    "still means taking the network.$",
)
english.base.TARGETS["MossdeepCity_SpaceCenter_2F_Text_MaxieWeWillGiveUp"] = (
    "LUZIA: We're leaving.\\p",
    "The M'BOI evidence still exists.\\p",
    "I'll find another way to share it.$",
)


def main() -> int:
    return english.main()


if __name__ == "__main__":
    raise SystemExit(main())
