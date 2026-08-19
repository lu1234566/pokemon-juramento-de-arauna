#!/usr/bin/env python3
from __future__ import annotations

import render_missoes_ceu_ground_floor_en as english


english.base.TARGETS["MossdeepCity_SpaceCenter_1F_Text_MagmaHaveSightsOnSpaceCenter"] = (
    "SCIENTIST: REMEMBRANCERS want\\n",
    "the regional uplink.\\p",
    "It reaches stations across\\n",
    "most of Arauna.$",
)
english.base.TARGETS["MossdeepCity_SpaceCenter_1F_Text_Grunt2Defeat"] = (
    "REMEMBRANCER: Fine... pass.\\p",
    "Listen before choosing a side.$",
)
english.base.TARGETS["MossdeepCity_SpaceCenter_1F_Text_MagmaIntentToStealNotice"] = (
    "REMEMBRANCER NOTICE:\\p",
    "Regional uplink stays offline\\n",
    "until the sync key is disabled.\\p",
    "No civilian data will be erased.$",
)


def main() -> int:
    return english.main()


if __name__ == "__main__":
    raise SystemExit(main())
