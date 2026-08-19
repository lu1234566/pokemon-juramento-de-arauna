#!/usr/bin/env python3
from __future__ import annotations

import render_missoes_ceu_ground_floor_en_checked as english


english.english.base.TARGETS["MossdeepCity_SpaceCenter_1F_Text_Grunt1Intro"] = (
    "REMEMBRANCER: This is not a\\n",
    "HORIZON base. I know.\\p",
    "But this network could be one.$",
)
english.english.base.TARGETS["MossdeepCity_SpaceCenter_1F_Text_Grunt4Intro"] = (
    "REMEMBRANCER: The uplink doesn't\\n",
    "carry memory. It carries orders.$",
)


def main() -> int:
    return english.main()


if __name__ == "__main__":
    raise SystemExit(main())
