#!/usr/bin/env python3
from __future__ import annotations

import render_missoes_ceu_ground_floor as base


base.TARGETS.update({
    "MossdeepCity_SpaceCenter_1F_Text_RocketLaunchImminent": (
        "CENTER: The next launch is\\n",
        "about to begin!$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_SuccessfulLaunchNumber": (
        "CENTER: Launch completed safely!\\p",
        "That was launch no. {STR_VAR_1}!$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_HaywireButRocketLaunchImminent": (
        "CENTER: The occupation changed\\n",
        "our routine, not the orbit.\\p",
        "Launch window is still open.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_HaywireButSuccessfulLaunchNumber": (
        "CENTER: Even under occupation,\\n",
        "the launch was safe.\\p",
        "That was launch no. {STR_VAR_1}!$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_RocketLaunchDemandsPerfection": (
        "SCIENTIST: A launch has no room\\n",
        "for a small mistake.\\p",
        "One percent can cost years.\\p",
        "Still, we try again.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_MagmaHaveSightsOnSpaceCenter": (
        "SCIENTIST: REMEMBRANCERS want\\n",
        "the regional uplink.\\p",
        "It reaches stations across\\n",
        "most of Arauna.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_FoundThisYouCanHaveIt": (
        "MAN: I found this stone while\\n",
        "walking near the coast.\\p",
        "I have no use for it. Take it.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_HoennFamousForMeteorShowers": (
        "MAN: Arauna has watched meteor\\n",
        "showers for generations.\\p",
        "That's how MISSOES DO CEU began.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_MagmaCantStealFuelTakeThis": (
        "MAN: Before this gets worse,\\n",
        "take this stone.\\p",
        "I'd rather it leave with you.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_CantStrollOnBeachWithMagma": (
        "MAN: With the building occupied,\\n",
        "no one is thinking about the\\n",
        "beach.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_DidPokemonComeFromSpace": (
        "WOMAN: Some researchers think\\n",
        "certain POKéMON came from space.\\p",
        "I still like the question.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_AquaShouldBeatMagma": (
        "WOMAN: I want the REMEMBRANCERS\\n",
        "out of here.\\p",
        "Handing it all to HORIZON scares\\n",
        "me too.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_RocketsBoggleMyMind": (
        "OLD MAN: A huge machine breaks\\n",
        "through the sky and keeps going.\\p",
        "That still amazes me.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_MagmaWantsToSpoilMyDream": (
        "OLD MAN: I waited years to see\\n",
        "a launch up close.\\p",
        "Now factions made this place a\\n",
        "battlefield.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_StevenMagmaCantBeAllowedToTakeFuel": (
        "SEU BENTO: Upstairs is the key\\n",
        "to the regional uplink.\\p",
        "No faction gets to decide for\\n",
        "all Arauna.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt3Intro": (
        "REMEMBRANCER: This transmitter\\n",
        "reaches sensors far from here.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt3Defeat": (
        "REMEMBRANCER: If HORIZON links\\n",
        "this to the LIVING ARCHIVE,\\n",
        "the scale changes.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt3PostBattle": (
        "REMEMBRANCER: RAUL is upstairs.\\n",
        "He knows about the key.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt1Intro": (
        "REMEMBRANCER: This is not a\\n",
        "HORIZON base. I know.\\p",
        "But this network could be one.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt1Defeat": (
        "REMEMBRANCER: Civilians use this\\n",
        "uplink too... I know.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt1PostBattle": (
        "REMEMBRANCER: I hate occupying\\n",
        "a public center.\\p",
        "I hate the alternative more.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt4Intro": (
        "REMEMBRANCER: The uplink doesn't\\n",
        "carry memory. It carries orders.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt4Defeat": (
        "REMEMBRANCER: One remote command\\n",
        "can trigger many sensors.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt4PostBattle": (
        "REMEMBRANCER: That shortcut is\\n",
        "exactly what M'BOI should have\\n",
        "taught us to fear.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt2Intro": (
        "REMEMBRANCER: The stairs are\\n",
        "sealed. LUZIA and RAUL are up.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt2Defeat": (
        "REMEMBRANCER: Fine... pass.\\p",
        "Listen before choosing a side.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt2PostBattle": (
        "REMEMBRANCER: The center isn't\\n",
        "the issue.\\p",
        "Who controls the key is.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_MagmaIntentToStealNotice": (
        "REMEMBRANCER NOTICE:\\p",
        "Regional uplink stays offline\\n",
        "until the sync key is disabled.\\p",
        "No civilian data will be erased.$",
    ),
})


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
