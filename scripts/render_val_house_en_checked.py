#!/usr/bin/env python3
from __future__ import annotations

import render_val_house_en as base

base.TARGETS["PetalburgCity_WallysHouse_Text_ThanksForPlayingWithWally"] = (
    ("Obrigado por ter ajudado VAL",),
    (
        "MAN: Thank you for helping VAL.\\p",
        "He talks about how patient you\\n",
        "were with him.\\p",
        "That mattered more than you\\n",
        "think.$",
    ),
)
base.TARGETS["PetalburgCity_WallysHouse_Text_PleaseExcuseUs"] = (
    ("Desculpe trazer voce", "VALE DO SILENCIO"),
    (
        "MAN: {PLAYER}, sorry to bring you\\n",
        "here so suddenly.\\p",
        "VAL changed after leaving for\\n",
        "VALE DO SILENCIO.\\p",
        "You helped when he was afraid\\n",
        "to travel alone.\\p",
        "As his father, I remember that.\\p",
        "Please take this.$",
    ),
)
base.TARGETS["PetalburgCity_WallysHouse_Text_YouMetWallyInEverGrandeCity"] = (
    ("ESTRADA DO JURAMENTO",),
    (
        "MAN: You met VAL on\\n",
        "ESTRADA DO JURAMENTO?\\p",
        "He came back more certain,\\n",
        "but still himself.\\p",
        "Thanks for walking beside him.$",
    ),
)
base.TARGETS["PetalburgCity_WallysHouse_Text_WallyLeftWithoutTelling"] = (
    ("VAL saiu sem avisar",),
    (
        "WOMAN: VAL left in a hurry.\\p",
        "I worry, of course.\\p",
        "Choosing his own road is part\\n",
        "of what he needed.$",
    ),
)


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
