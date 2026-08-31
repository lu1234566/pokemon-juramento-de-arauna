#!/usr/bin/env python3
from __future__ import annotations

import render_porto_sal_shipyard as base


base.TARGETS_1F.update({
    "SlateportCity_SternsShipyard_1F_Text_CantMakeHeadsOrTails": (
        ("heads or tails",),
        (
            "MASTER: If this piece goes here,\\n",
            "where does that one go?\\p",
            "New designs look easy until\\n",
            "they meet a real hull.$",
        ),
    ),
    "SlateportCity_SternsShipyard_1F_Text_MeetDockDeliverToStern": (
        ("projeto de M'BOI",),
        (
            "MASTER: You brought the OCEANIC\\n",
            "PARTS?\\p",
            "I handle hull and structure.\\n",
            "Find the ENGINEER at the MUSEUM.$",
        ),
    ),
    "SlateportCity_SternsShipyard_1F_Text_CouldYouFindStern": (
        ("CAPT. STERN",),
        (
            "MASTER: The HARBOR ENGINEER\\n",
            "should be at the MUSEUM.\\p",
            "Please deliver the OCEANIC\\n",
            "PARTS to him.$",
        ),
    ),
    "SlateportCity_SternsShipyard_1F_Text_CouldUseAdviceFromVeteran": (
        ("Shipbuilding is an art",),
        (
            "MASTER: Shipbuilding is an art.\\p",
            "Not everything fits a plan.\\p",
            "I need a veteran sailor who\\n",
            "knows these currents.$",
        ),
    ),
    "SlateportCity_SternsShipyard_1F_Text_BrineyJoinedUs": (
        ("MR. BRINEY", "veteran sailor"),
        (
            "MASTER: A VETERAN SAILOR came\\n",
            "to help us.\\p",
            "With his experience, the LINE\\n",
            "FERRY is taking shape.$",
        ),
    ),
    "SlateportCity_SternsShipyard_1F_Text_FerryIsReady": (
        ("MARE ALTA",),
        (
            "MASTER: The LINE FERRY is ready!\\p",
            "It's our best design yet.\\p",
            "Every ship teaches us how to\\n",
            "build the next one better.$",
        ),
    ),
    "SlateportCity_SternsShipyard_1F_Text_DecidedToHelpDock": (
        ("MR. BRINEY", "sea dog's"),
        (
            "VETERAN: {PLAYER}! Been a while!\\p",
            "I decided to help the shipyard.\\p",
            "The MASTER knows design.\\n",
            "I know the sea and currents.\\p",
            "Together we'll build a good\\n",
            "ship.$",
        ),
    ),
    "SlateportCity_SternsShipyard_1F_Text_SeaIsLikeLivingThing": (
        ("sea is like a living thing",),
        (
            "TECH: Season, weather, moon...\\p",
            "All of it changes the sea.\\p",
            "Everyone here learns early:\\n",
            "the water never stays the same.$",
        ),
    ),
    "SlateportCity_SternsShipyard_1F_Text_GetSeasickEasily": (
        ("seasick",),
        (
            "TECH: I get seasick easily.\\p",
            "That's why I work better here,\\n",
            "with my feet on solid ground.$",
        ),
    ),
})

base.TARGETS_2F.update({
    "SlateportCity_SternsShipyard_2F_Text_ShipDesignMoreLikeBuilding": (
        ("large ship", "big building"),
        (
            "TECH: Designing a large ship\\n",
            "feels like raising a building\\n",
            "more than assembling a vehicle.$",
        ),
    ),
    "SlateportCity_SternsShipyard_2F_Text_FloatsBecauseBuoyancy": (
        ("heavy iron", "buoyancy"),
        (
            "TECH: So much metal floating...\\p",
            "The hull displaces enough water.\\n",
            "That's called buoyancy.$",
        ),
    ),
})


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
