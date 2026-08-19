#!/usr/bin/env python3
from __future__ import annotations

import render_pampa_gym_rooms_en as base

# Short inherited defeat lines do not contain a room/faction marker. Add only
# their literal source cues instead of weakening validation for all room text.
base.SOURCE_MARKERS += (
    "magnificent battle",
    "cut above",
    "real deal",
    "went all out",
)

base.TARGETS["PetalburgCity_Gym_Text_ParkerIntro"] = (
    "TRAINER: CONFUSION ROOM.\\p",
    "Let's see if your BOND holds\\n",
    "when commands become uncertain.$",
)
base.TARGETS["PetalburgCity_Gym_Text_GeorgeDefeat"] = (
    "You broke through each recovery.$",
)
base.TARGETS["PetalburgCity_Gym_Text_BerkePostBadge"] = (
    "PAMPA DA ESPERA grew tougher\\n",
    "under ELIAS.\\p",
    "Now we know you can push us too.$",
)
base.TARGETS["PetalburgCity_Gym_Text_AlexiaIntro"] = (
    "TRAINER: DEFENSE ROOM.\\p",
    "Defense lets me take more risks.\\p",
    "Let's see if yours does too.$",
)
base.TARGETS["PetalburgCity_Gym_Text_JodyIntro"] = (
    "TRAINER: POWER ROOM.\\p",
    "ELIAS told us to go all out.\\p",
    "Your family name means nothing.$",
)


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
