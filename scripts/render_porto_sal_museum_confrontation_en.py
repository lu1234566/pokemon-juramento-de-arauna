#!/usr/bin/env python3
from __future__ import annotations

import re

import render_porto_sal_museum_confrontation as base


base.TARGETS.update({
    "SlateportCity_OceanicMuseum_2F_Text_ThankYouForTheParts": (
        "ENGINEER: These are the OCEANIC\\n",
        "PARTS we were waiting for!\\p",
        "We can calibrate deep-sea\\n",
        "sensors with them.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_WellTakeThoseParts": (
        "HORIZON: Stop there.\\p",
        "Those parts are requisitioned\\n",
        "for a field operation.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_SternWhoAreYou": (
        "ENGINEER: Requisitioned?\\p",
        "Who authorized you?$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_WereTeamAqua": (
        "HORIZON: Field unit.\\p",
        "The sensors help map anomalies\\n",
        "beneath M'BOI.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_Grunt1Defeat": (
        "HORIZON: This wasn't supposed\\n",
        "to become a battle.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_BossGoingToBeFurious": (
        "HORIZON: The director won't like\\n",
        "us returning without the parts.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_LetMeTakeCareOfThis": (
        "HORIZON: Step aside.\\p",
        "I'll handle this.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_Grunt2Defeat": (
        "HORIZON: Fine...\\p",
        "We're not getting past you.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_MeddlingKid": (
        "HORIZON: What now?\\p",
        "We can't return empty-handed.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_CameToSeeWhatsTakingSoLong": (
        "OTACILIO: I came to see why the\\n",
        "team was taking so long.\\p",
        "So you're the one who stopped\\n",
        "them.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_ArchieWarning": (
        "OTACILIO: These parts could help\\n",
        "map the M'BOI caverns.\\p",
        "But turning a MUSEUM into a\\n",
        "forced operation is not care.\\p",
        "Stand down. We'll find another\\n",
        "way.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_SternThankYouForSavingUs": (
        "ENGINEER: Thank you, {PLAYER}.\\p",
        "Now I can receive the parts\\n",
        "safely.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_SternIveGotToGo": (
        "ENGINEER: I need to take these\\n",
        "to the harbor lab.\\p",
        "The deep-sea expedition can't\\n",
        "wait much longer.\\p",
        "Feel free to visit the rest\\n",
        "of the MUSEUM.$",
    ),
})

base.ITEM_NAME_NEW = '.name = _("OCEANIC PARTS"),'
base.ITEM_DESC_RE = re.compile(
    r'(?ms)^static const u8 sDevonGoodsDesc\[\] = _\(\n(?P<body>.*?^\s*"[^"\n]*"\);)'
)
base.ITEM_DESC_NEW = (
    'static const u8 sDevonGoodsDesc[] = _(\n'
    '    "Parts for deep-sea\\n"\n'
    '    "oceanographic\\n"\n'
    '    "research.");'
)


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
