#!/usr/bin/env python3
from __future__ import annotations

import render_missoes_ceu_confrontation as base


base.TARGETS.update({
    "MossdeepCity_SpaceCenter_2F_Text_MossdeepIdealForRockets": (
        "SCIENTIST: MISSOES DO CEU has\\n",
        "steady winds and open horizon.\\p",
        "Our antennas cover Arauna.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_WhyWouldMagmaStealRocketFuel": (
        "SCIENTIST: The regional uplink\\n",
        "can sync BOND sensors across\\n",
        "Arauna. The REMEMBRANCERS want\\n",
        "it cut.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_WouldveLikedToBeAstronaut": (
        "MAN: When I was young, I wanted\\n",
        "to see Arauna from above.\\p",
        "Maybe I can still learn.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_MagmaCantGetAwayWithThis": (
        "MAN: Cutting a civilian network\\n",
        "hurts people who never chose\\n",
        "this fight.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_WishOrdinaryPeopleCouldGoIntoSpace": (
        "BOY: Someday I want the sky to\\n",
        "belong to more than scientists\\n",
        "and rich people.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_DoesMagmaWantToGoToSpace": (
        "BOY: The REMEMBRANCERS aren't\\n",
        "here for space.\\p",
        "They want the network that talks\\n",
        "to all Arauna.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_YoureOutnumberedTakeUsOn": (
        "REMEMBRANCER: There are three of\\n",
        "us. Still want through?$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_GoodAnswer": (
        "REMEMBRANCER: Better this way.\\p",
        "We don't need another fight.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt5Intro": (
        "REMEMBRANCER: If HORIZON links\\n",
        "this network to the LIVING\\n",
        "ARCHIVE, orders reach Arauna.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt5Defeat": (
        "REMEMBRANCER: We shut the uplink\\n",
        "to prevent another M'BOI.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt5PostBattle": (
        "REMEMBRANCER: Civilians use this\\n",
        "network too. I know.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt6Intro": (
        "REMEMBRANCER: RAUL ordered us to\\n",
        "hold this floor while LUZIA gets\\n",
        "to the transmitter.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt6Defeat": (
        "REMEMBRANCER: We aren't stealing\\n",
        "fuel. We want the sync key.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt6PostBattle": (
        "REMEMBRANCER: If HORIZON keeps\\n",
        "that key, it can trigger sensors\\n",
        "from afar.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt7Intro": (
        "REMEMBRANCER: LUZIA wants to air\\n",
        "M'BOI records before breaking\\n",
        "the key.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt7Defeat": (
        "REMEMBRANCER: Exposing truth\\n",
        "shouldn't require taking a\\n",
        "whole network.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt7PostBattle": (
        "REMEMBRANCER:\\n",
        "Maybe SEU BENTO is right.\\p",
        "Don't tell anyone I said that.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_WellTakeCareOfYou": (
        "RAUL: You again.\\p",
        "We're stopping synchronization,\\n",
        "not here to debate you.\\p",
        "But we won't move.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_MaxieDontInterfere": (
        "LUZIA: HORIZON can use this link\\n",
        "to command the ARCHIVE across\\n",
        "Arauna. I won't allow it.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_StevenWhyStealRocketFuel": (
        "SEU BENTO: Stopping HORIZON does\\n",
        "not require taking city systems.\\p",
        "Who authorized you?$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_MaxieUseFuelToEruptVolcano": (
        "LUZIA: I want to transmit proof\\n",
        "from M'BOI and destroy the sync\\n",
        "key. Then the network returns.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_StevenAreYouReadyToBattle": (
        "SEU BENTO: {PLAYER}, I'll stop\\n",
        "this takeover.\\p",
        "Fight with me?$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_StevenHurryGetReadyQuickly": (
        "SEU BENTO: Prepare your team.\\p",
        "I'll hold the passage.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_JustWantToExpandLand": (
        "LUZIA: I only need to break the\\n",
        "key before HORIZON uses it.$",
    ),
    "MossdeepCity_SpaceCenter_Text_TabithaDefeat": (
        "RAUL: I'm with LUZIA.\\p",
        "I still wish there were another\\n",
        "way.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_MaxieWeFailedIsAquaAlsoMisguided": (
        "LUZIA: I understand.\\p",
        "Taking the network to block\\n",
        "control still means taking it.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_MaxieWeWillGiveUp": (
        "LUZIA: We're leaving.\\p",
        "The M'BOI evidence still exists.\\p",
        "I'll find another way to share.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_StevenThankYouComeSeeMeAtHome": (
        "SEU BENTO: Thank you, {PLAYER}.\\p",
        "The network belongs to neither\\n",
        "side.\\p",
        "Come by my house later.\\n",
        "I want to show you something.$",
    ),
})


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
