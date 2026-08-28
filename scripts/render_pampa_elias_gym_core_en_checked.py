#!/usr/bin/env python3
from __future__ import annotations

import render_pampa_elias_gym_core_en as base

base.TARGETS["PetalburgCity_Gym_Text_YouHaveGottenStronger"] = (
    "ELIAS: You've changed, {PLAYER}.\\p",
    "The BADGES show experience.\\p",
    "Your POKéMON show more than\\n",
    "that.$",
)
base.TARGETS["PetalburgCity_Gym_Text_NormanIntro"] = (
    "ELIAS: I kept this from you.\\p",
    "I approved part of the M'BOI\\n",
    "project.\\p",
    "For years I called my fear\\n",
    "prudence.\\p",
    "Today I'm your GYM LEADER.\\p",
    "After this, ask me again.$",
)
base.TARGETS["PetalburgCity_Gym_Text_ExplainFacade"] = (
    "ELIAS: TM42 contains FACADE.\\p",
    "Its power doubles if the user\\n",
    "is poisoned, paralyzed\\n",
    "or burned.\\p",
    "A bad state can become leverage.$",
)
base.TARGETS["PetalburgCity_Gym_Text_DadHappyAndSad"] = (
    "ELIAS: As LEADER, losing hurts.\\p",
    "As your father... I'm proud.\\p",
    "Both feelings can be true.$",
)
base.TARGETS["PetalburgCity_Gym_Text_DadNoAmountOfTrainingIsEnough"] = (
    "ELIAS: Training never ends.\\p",
    "Neither does learning how to\\n",
    "live with what we remember.$",
)
base.TARGETS["PetalburgCity_Gym_Text_GymGuideAdvice"] = (
    "GUIDE: This GYM has seven rooms.\\p",
    "Each TRAINER tests a different\\n",
    "battle habit.\\p",
    "Win and the next doors open.\\p",
    "Choose your path carefully.$",
)


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
