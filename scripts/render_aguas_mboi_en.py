#!/usr/bin/env python3
from __future__ import annotations

import render_aguas_mboi_daily_surface as daily

base = daily.base


def set_payload(targets, label: str, payloads: tuple[str, ...]) -> None:
    markers, _ = targets[label]
    targets[label] = (markers, payloads)


# Crisis and post-crisis city surface.
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_DoorIsClosed", (
    "The door is sealed under an\\n",
    "emergency order.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_GiantPokemonSuddenlyAppeared", (
    "BOY: I remembered a house\\n",
    "I've never seen.\\p",
    "Mom forgot my name for a few\\n",
    "seconds.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_WhatIsThatGreenPokemon", (
    "BOY: Did that come from the\\n",
    "TOWER?\\p",
    "It made both currents retreat.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_TwoPokemonArentAngry", (
    "BOY: They don't look angry.\\p",
    "It looks like neither can stop\\n",
    "on its own.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_FlyingMonStoppedRampage", (
    "BOY: The GUARDIAN OF THE\\n",
    "TOWER pushed the currents back.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_ThisIsWicked", (
    "BOY: My head is full of\\n",
    "someone else's memories.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_ThatWasWicked", (
    "BOY: It stopped...\\p",
    "But I still remember things\\n",
    "I never lived.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_GoRedAndBlueMon", (
    "MAN: One returns everything!\\n",
    "The other takes everything away!\\p",
    "They'll tear the city apart!$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_DoYouKnowMonNames", (
    "MAN: Do you know what those\\n",
    "currents are?\\p",
    "Why do they seem to know us?$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_GreenOneSettlesThings", (
    "MAN: The TOWER GUARDIAN\\n",
    "separated the two currents.\\p",
    "I hope that is enough.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_SeeingLegendWithOwnEyes", (
    "MAN: My grandmother spoke of\\n",
    "IARA-MAE and ANHANGUERA.\\p",
    "I thought they were metaphors.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_SawLegendWithOwnEyes", (
    "MAN: Now I know those stories\\n",
    "were warnings, not legends.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_BigPokemonFighting", (
    "KIRI: People are crying for\\n",
    "people they never knew.\\p",
    "Please make it stop.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_PrettyMonCameFromSky", (
    "KIRI: The GUARDIAN came down...\\p",
    "For a moment, everyone\\n",
    "remembered their own name.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_SootopolisWillBeWrecked", (
    "WOMAN: AGUAS DE M'BOI will\\n",
    "split apart like this!$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_SootopolisDidntGetWrecked", (
    "WOMAN: The city is standing.\\p",
    "Not every memory went back.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_CityRegainedCalm", (
    "MAN: The water is calm again.\\p",
    "People still check each other's\\n",
    "names.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_GiganticPokemonFight", (
    "WOMAN: This isn't a battle.\\p",
    "Both currents are pulling at\\n",
    "the same people.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_FearedWorstWhenPokemonFlewDown", (
    "WOMAN: When the GUARDIAN came\\n",
    "down, I feared worse.\\p",
    "It was the first thing that made\\n",
    "them retreat.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_YouBroughtFlyingMon", (
    "WOMAN: Were you the one who\\n",
    "climbed TORRE DO JURAMENTO?\\p",
    "Then you called the GUARDIAN.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_GroudonPleaseStop", (
    "LUZIA: IARA-MAE, stop!\\p",
    "Returning everything without\\n",
    "choice is not repair.\\p",
    "I should have known sooner.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_AfterAllOurScheming", (
    "LUZIA: I fought erasure for so\\n",
    "long that I nearly made\\n",
    "remembering another duty.\\p",
    "I was wrong.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_KyogreCalmDown", (
    "OTACILIO: ANHANGUERA, stop!\\p",
    "Ending pain without consent is\\n",
    "another form of power.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_TryingMeaninglessToPokemon", (
    "OTACILIO: I called control care\\n",
    "for too long.\\p",
    "M'BOI never gave me the right\\n",
    "to choose for others.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_InvolvedWithCrisisComeWithMe", (
    "SEU BENTO: Look at the water.\\p",
    "IARA-MAE and ANHANGUERA were\\n",
    "forced awake together.\\p",
    "Come. AMALIA needs you at the\\n",
    "city's core.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_DoesThisMakeYourFearPokemon", (
    "SEU BENTO: This isn't cruelty.\\p",
    "These are BONDS without choice,\\n",
    "pulled in opposite directions.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_HereWereAreHelpWallace", (
    "SEU BENTO: AMALIA is inside.\\p",
    "She knows the story of TORRE DO\\n",
    "JURAMENTO.\\p",
    "Listen to what she found.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_KnowWhatsNeededToHelpHim", (
    "SEU BENTO: AMALIA found an old\\n",
    "record from the TOWER.\\p",
    "She thinks a third force can\\n",
    "separate the two.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_NeverBeenToSkyPillar", (
    "SEU BENTO: The TOWER lies beyond\\n",
    "the western routes.\\p",
    "AMALIA opened the way.\\p",
    "Climb. I'll stay with the city.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_SoThatsRayquaza", (
    "SEU BENTO: So the GUARDIAN\\n",
    "answered the OATH.\\p",
    "Not to decide for us.\\p",
    "To stop anyone deciding alone\\n",
    "for everyone.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_MaxieArchieLeft", (
    "SEU BENTO: LUZIA and OTACILIO\\n",
    "returned to the MEMORIAL.\\p",
    "This time, to return what they\\n",
    "took.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_LeadSuperiorTrainerToCave", (
    "GUARD: SEU BENTO asked me to\\n",
    "let you pass.\\p",
    "AMALIA is at the core.\\p",
    "The city needs a decision that\\n",
    "comes from no faction.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_AwakenedPokemonClash", (
    "GUARD: Both currents yielded to\\n",
    "a third force.\\p",
    "I've never seen the OATH answer\\n",
    "like that.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_CaveOfOriginSleepsToo", (
    "GUARD: The core is quiet again.\\p",
    "May it remain memory, not a\\n",
    "tool.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_HaventYouScaledSkyPillar", (
    "AMALIA: The city worsens by the\\n",
    "minute.\\p",
    "TORRE DO JURAMENTO is still our\\n",
    "only option. Go!$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_AquaMagmaDidntMeanHarm", (
    "AMALIA: LUZIA and OTACILIO must\\n",
    "answer for what they did.\\p",
    "First, stop the city from losing\\n",
    "itself.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_ThankYouForHelpAcceptThis", (
    "AMALIA: You kept two ideas from\\n",
    "becoming a sentence.\\p",
    "Take this. There is more road\\n",
    "ahead.$",
))
set_payload(base.CITY_TARGETS, "SootopolisCity_Text_DazzledByMentor", (
    "AMALIA: The TOWER answered you,\\n",
    "not an order from me.\\p",
    "Carry that into the GYM.$",
))

# Torre do Juramento handoff.
set_payload(base.TOWER_TARGETS, "SkyPillar_Outside_Text_OpenedDoorToSkyPillar", (
    "AMALIA: I opened the entrance.\\p",
    "TORRE DO JURAMENTO reacted to\\n",
    "the collapse at M'BOI.\\p",
    "We climb before it gets worse.$",
))
set_payload(base.TOWER_TARGETS, "SkyPillar_Outside_Text_EarthquakeNotMomentToWaste", (
    "AMALIA: Another tremor!\\p",
    "Both currents are still pressing\\n",
    "against the city.\\p",
    "Keep moving.$",
))
set_payload(base.TOWER_TARGETS, "SkyPillar_Outside_Text_SituationGettingWorse", (
    "AMALIA: Wait...\\p",
    "The readings changed again.\\p",
    "Something in AGUAS DE M'BOI is\\n",
    "giving way.$",
))
set_payload(base.TOWER_TARGETS, "SkyPillar_Outside_Text_GotToGoBackForSootopolis", (
    "AMALIA: I need to return to\\n",
    "AGUAS DE M'BOI.\\p",
    "You keep climbing.\\p",
    "Find the GUARDIAN OF THE TOWER.$",
))

# Ordinary city life after the crisis.
set_payload(daily.DAILY_CITY_TARGETS, "SootopolisCity_Text_PhysicallyFitLivingHere", (
    "MAN: You dive, climb stairs,\\n",
    "cross bridges...\\p",
    "In AGUAS DE M'BOI, walking is\\n",
    "exercise.$",
))
set_payload(daily.DAILY_CITY_TARGETS, "SootopolisCity_Text_WonderWhatWorldIsLike", (
    "BOY: I've never left AGUAS DE\\n",
    "M'BOI.\\p",
    "I want to see the sky without\\n",
    "the crater around it.$",
))
set_payload(daily.DAILY_CITY_TARGETS, "SootopolisCity_Text_NoOrdinaryTourist", (
    "MAN: You came from far away?\\p",
    "Few people reach AGUAS DE M'BOI\\n",
    "by accident.$",
))
set_payload(daily.DAILY_CITY_TARGETS, "SootopolisCity_Text_SootopolisSkyBeautiful", (
    "WOMAN: The city grew inside a\\n",
    "crater.\\p",
    "The sky looks like a circle.\\p",
    "At night it feels like an open\\n",
    "window.$",
))
set_payload(daily.DAILY_CITY_TARGETS, "SootopolisCity_Text_NightSkyFavoriteScenery", (
    "WOMAN: At night, the crater rim\\n",
    "becomes a frame.\\p",
    "Stars seem to float on water.\\p",
    "It's my favorite view.$",
))
set_payload(daily.DAILY_CITY_TARGETS, "SootopolisCity_Text_WhereDidLegendariesGo", (
    "BOY: The currents are gone, but\\n",
    "the city remembers the collapse.\\p",
    "Mom writes down our names before\\n",
    "we sleep now.$",
))
set_payload(daily.DAILY_CITY_TARGETS, "SootopolisCity_Text_WeatherWentWild", (
    "WOMAN: The water changed first.\\p",
    "Then came memories that were not\\n",
    "ours.$",
))
set_payload(daily.DAILY_CITY_TARGETS, "SootopolisCity_Text_ExplainWaterfallGoToGym", (
    "AMALIA: This HM teaches\\n",
    "WATERFALL.\\p",
    "With the SPRING BADGE, a POKéMON\\n",
    "can climb waterfalls.\\p",
    "Earn it at the AGUAS DE M'BOI\\n",
    "GYM.$",
))

# Kiri keeps the lighter everyday voice of the city.
set_payload(daily.KIRI_TARGETS, "SootopolisCity_Text_NameIsKiriHaveOneOfThese", (
    "Hi! What's your name?\\p",
    "... ... ...\\p",
    "I like it! I'm KIRI.\\p",
    "My parents chose my name as a\\n",
    "wish for health and kindness.\\p",
    "You can have one of these.$",
))
set_payload(daily.KIRI_TARGETS, "SootopolisCity_Text_GiveYouThisBerryToo", (
    "KIRI: Take this BERRY too!\\p",
    "I really like this one.$",
))
set_payload(daily.KIRI_TARGETS, "SootopolisCity_Text_WhatKindOfWishInYourName", (
    "KIRI: I wonder what wish they\\n",
    "put inside your name?$",
))
set_payload(daily.KIRI_TARGETS, "SootopolisCity_Text_LikeSeasonBornIn", (
    "KIRI: Spring, summer, autumn,\\n",
    "winter...\\p",
    "Do people grow fondest of the\\n",
    "season they were born in?$",
))
set_payload(daily.KIRI_TARGETS, "SootopolisCity_Text_ThenILoveAutumn", (
    "KIRI: I was born in autumn, so\\n",
    "autumn is my favorite!\\p",
    "Which season do you like?$",
))
set_payload(daily.KIRI_TARGETS, "SootopolisCity_Text_OhDoesntMatter", (
    "KIRI: Oh... that's okay.\\p",
    "There is still so much I want\\n",
    "to learn.$",
))


def main() -> int:
    return daily.main()


if __name__ == "__main__":
    raise SystemExit(main())
