#!/usr/bin/env python3
from __future__ import annotations

import render_porto_sal_museum_people_checked as checked

base = checked.base


def patch(targets, label: str, payloads: tuple[str, ...]) -> None:
    markers, _ = targets[label]
    targets[label] = (markers, payloads)


# Queue outside the museum.
patch(base.CITY_TARGETS, "SlateportCity_Text_WhatsLongLineOverThere", (
    "MAN: What's happening over there?\\p",
    "Look at that line.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_VisitedMuseumOften", (
    "WOMAN: I came here often as a kid.\\p",
    "This museum taught me to love\\n",
    "the mysteries of the sea.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_QuitPushing", (
    "HORIZON: No pushing.\\p",
    "The line starts here.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_AquaHasPolicy", (
    "HORIZON: Orders say enter quietly.\\p",
    "So yes, we're paying admission.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_BossIsBrilliant", (
    "HORIZON: The director wants to\\n",
    "inspect oceanographic equipment.\\p",
    "I don't know why so many came.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_WhatsNewSchemeIWonder", (
    "HORIZON: They only said\\n",
    "'field inspection.'\\p",
    "Vague orders make me nervous.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_ShouldTakeItAll", (
    "HORIZON: If equipment is vital,\\n",
    "we should requisition it.\\p",
    "That's why we're here, right?$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_DontButtIn", (
    "HORIZON: Hey, respect the line.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_RemindsMeOfLongLineForGames", (
    "HORIZON: I haven't seen a line\\n",
    "this long in years.\\p",
    "Looks like a game launch.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_WhyAreWeLiningUp", (
    "HORIZON: Why are we paying ¥50?\\p",
    "HORIZON: Because it's a civilian\\n",
    "MUSEUM. Pay and enter.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_WhatDoYouWant", (
    "HORIZON: Need something?$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_IllReadSignForYou", (
    "HORIZON: Want the sign read?\\p",
    "I'll read it for you.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_SaysSomethingLikeSeaIsEndless", (
    "HORIZON: It says life in the sea\\n",
    "has no end.\\p",
    "Nice. I think that's it.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_ShouldveBroughtMyGameBoy", (
    "HORIZON: I should've brought\\n",
    "something to pass the time.\\p",
    "This line isn't moving.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_HotSpringsAfterOperation", (
    "HORIZON: Dinner is on me after\\n",
    "the mission.\\p",
    "If we leave this line today.$",
))

# Museum 1F reception, agents and visitors.
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_WouldYouLikeToEnter", (
    "RECEPTION: Welcome to the\\n",
    "OCEANOGRAPHIC MUSEUM.\\p",
    "Admission is ¥50. Enter?$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_PleaseEnjoyYourself", (
    "RECEPTION: Enjoy your visit.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_NotEnoughMoney", (
    "RECEPTION: Sorry, you don't have\\n",
    "enough money.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_CatchUpWithYourGroup", (
    "RECEPTION: Are you with the\\n",
    "technical group?\\p",
    "They're upstairs. Go ahead.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_AquaExistForGoodOfAll", (
    "HORIZON: I'm field staff, not a\\n",
    "tourist.\\p",
    "But I paid, so I'll look around.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_OurBossIsntHere", (
    "HORIZON: OTACILIO isn't here yet.\\p",
    "We were only meant to observe.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_WouldStuffHereMakeMeRich", (
    "HORIZON: Some equipment is costly.\\p",
    "No, we're not here to steal it.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_CanLearnForNefariousDeeds", (
    "HORIZON: These models explain\\n",
    "currents and pressure.\\p",
    "Useful field knowledge.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_RustboroBungled", (
    "HORIZON: If the previous operation\\n",
    "had worked, I wouldn't be here.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_DidntHaveMoney", (
    "HORIZON: I paid ¥50 like everyone.\\p",
    "Orders are orders.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_LearnAboutSeaForBattling", (
    "VISITOR: I came to study the sea\\n",
    "and understand my POKéMON better.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_SternIsRoleModel", (
    "VISITOR: The HARBOR ENGINEER is\\n",
    "my biggest inspiration.\\p",
    "I want to explore the deep sea.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_MustBePokemonWeDontKnow", (
    "VISITOR: The sea feels endless.\\p",
    "How many POKéMON live where no\\n",
    "one has ever reached?$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_WantSeaPokemon", (
    "VISITOR: I want a sea POKéMON.\\p",
    "It must be cold and nice to hug.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_RememberMeTakeThis", (
    "HORIZON: Remember me?\\p",
    "You beat me before.\\p",
    "This TM shouldn't be mine.\\n",
    "Take it. Call it a debt.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_HopeINeverSeeYouAgain", (
    "HORIZON: We're even now.\\p",
    "I hope next time we're not on\\n",
    "opposite sides.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_YouHaveToTakeThis", (
    "HORIZON: Your BAG is full?\\p",
    "Come back with room. I still owe\\n",
    "you this TM.$",
))


def main() -> int:
    return checked.main()


if __name__ == "__main__":
    raise SystemExit(main())
