#!/usr/bin/env python3
from __future__ import annotations

import render_porto_sal_museum_confrontation_en as english


english.base.TARGETS["SlateportCity_OceanicMuseum_2F_Text_ThankYouForTheParts"] = (
    "ENGINEER: These are the OCEANIC\\n",
    "PARTS we were waiting for!\\p",
    "We can calibrate deep sensors\\n",
    "with them.$",
)
english.base.TARGETS["SlateportCity_OceanicMuseum_2F_Text_CameToSeeWhatsTakingSoLong"] = (
    "OTACILIO: I came to see why the\\n",
    "team was taking so long.\\p",
    "So you stopped them.$",
)
english.base.TARGETS["SlateportCity_OceanicMuseum_2F_Text_ArchieWarning"] = (
    "OTACILIO: These parts could help\\n",
    "map the M'BOI caverns.\\p",
    "But forcing a MUSEUM into an\\n",
    "operation is not care.\\p",
    "Stand down. Find another way.$",
)


def main() -> int:
    return english.main()


if __name__ == "__main__":
    raise SystemExit(main())
