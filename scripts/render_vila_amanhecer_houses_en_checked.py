#!/usr/bin/env python3
from __future__ import annotations

import render_vila_amanhecer_houses_en as base

base.ENGLISH["PlayersHouse_1F_Text_YouShouldRestABit"] = (
    "MOM: You look like you need\\n",
    "some rest.\\p",
    "Sleep a little before going\\n",
    "back on the road.$",
)
base.ENGLISH["PlayersHouse_1F_Text_GotDadsBadgeHeresSomethingFromMom"] = (
    "MOM: ELIAS gave you that BADGE?\\p",
    "Then take this too.\\p",
    "This one is from your mother.$",
)


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
