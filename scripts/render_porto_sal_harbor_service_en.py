#!/usr/bin/env python3
from __future__ import annotations

import render_porto_sal_harbor_service as base


base.TARGETS.update({
    "SlateportCity_Harbor_Text_FerryServiceUnavailable": (
        ("ferry service",),
        (
            "ATTENDANT: Looking for a ship?\\p",
            "Sorry, the LINE FERRY is not\\n",
            "operating yet.$",
        ),
    ),
    "SlateportCity_Harbor_Text_MayISeeYourTicket": (
        ("CIRO:", "DESENCANTO"),
        (
            "ATTENDANT: May I see your\\n",
            "TICKET?$",
        ),
    ),
    "SlateportCity_Harbor_Text_YouMustHaveTicket": (
        ("TICKET", "board"),
        (
            "ATTENDANT: You need a TICKET\\n",
            "before you can board.$",
        ),
    ),
    "SlateportCity_Harbor_Text_FlashedTicketWhereTo": (
        ("flashed the TICKET", "where"),
        (
            "{PLAYER} showed the TICKET.\\p",
            "ATTENDANT: Perfect.\\n",
            "Where would you like to go?$",
        ),
    ),
    "SlateportCity_Harbor_Text_SailAnotherTime": (
        ("another time",),
        (
            "ATTENDANT: Travel with us\\n",
            "anytime.$",
        ),
    ),
    "SlateportCity_Harbor_Text_LilycoveItIs": (
        ("BAIA DAS LUZES",),
        (
            "ATTENDANT: BAIA DAS LUZES,\\n",
            "right?$",
        ),
    ),
    "SlateportCity_Harbor_Text_BattleFrontierItIs": (
        ("BATTLE FRONTIER",),
        (
            "ATTENDANT: BATTLE CIRCUIT,\\n",
            "right?$",
        ),
    ),
    "SlateportCity_Harbor_Text_PleaseBoardFerry": (
        ("board the ferry",),
        (
            "ATTENDANT: Board the LINE FERRY\\n",
            "and wait for departure.$",
        ),
    ),
    "SlateportCity_Harbor_Text_WhereWouldYouLikeToGo": (
        ("where would you like",),
        ("ATTENDANT: Where would you like\\n", "to go?$"),
    ),
    "SlateportCity_Harbor_Text_LoveToGoDeepUnderwaterSomeday": (
        ("bottom of the sea", "underwater"),
        (
            "SAILOR: Reaching the seafloor\\n",
            "must be incredible.\\p",
            "Someday I want to ride in a\\n",
            "research submersible.$",
        ),
    ),
    "SlateportCity_Harbor_Text_AbnormalWeather": (
        ("sensores detectam", "DESENCANTO"),
        (
            "SAILOR: The sea weather has\\n",
            "been strange in places.\\p",
            "Currents shift without warning.\\n",
            "Sailors need extra care.$",
        ),
    ),
    "SlateportCity_Harbor_Text_SubTooSmallForMe": (
        ("CAPT. STERN", "sub's too small"),
        (
            "MAN: I wanted to join the\\n",
            "ENGINEER's expedition.\\p",
            "The submersible is too small.\\n",
            "I'd take up half the room.$",
        ),
    ),
    "SlateportCity_Harbor_Text_WontBeLongBeforeWeFinishFerry": (
        ("MR. BRINEY", "SHIPYARD", "ferry"),
        (
            "ENGINEER: The VETERAN is\\n",
            "helping at the SHIPYARD.\\p",
            "The LINE FERRY should be ready\\n",
            "soon.$",
        ),
    ),
    "SlateportCity_Harbor_Text_FinishedMakingFerry": (
        ("MARE ALTA", "MR. BRINEY"),
        (
            "ENGINEER: {PLAYER}, it's ready!\\p",
            "The LINE FERRY can finally sail.\\p",
            "The VETERAN's experience made\\n",
            "all the difference.\\p",
            "Take a trip whenever you like.$",
        ),
    ),
    "SlateportCity_Harbor_Text_WouldYouTradeScanner": (
        ("SCANNER", "DEEPSEATOOTH", "DEEPSEASCALE"),
        (
            "ENGINEER: That's a SCANNER!\\p",
            "It would help our expeditions.\\p",
            "Trade it for a DEEPSEATOOTH\\n",
            "or DEEPSEASCALE?$",
        ),
    ),
    "SlateportCity_Harbor_Text_IfYouWantToTradeLetMeKnow": (
        ("useless to you", "SCANNER"),
        (
            "ENGINEER: That's fine.\\p",
            "If you want to trade the\\n",
            "SCANNER, let me know.$",
        ),
    ),
    "SlateportCity_Harbor_Text_TradeForDeepSeaTooth": (
        ("DEEPSEATOOTH",),
        (
            "ENGINEER: Trade for\\n",
            "DEEPSEATOOTH?$",
        ),
    ),
    "SlateportCity_Harbor_Text_TradeForDeepSeaScale": (
        ("DEEPSEASCALE",),
        (
            "ENGINEER: Trade for\\n",
            "DEEPSEASCALE?$",
        ),
    ),
    "SlateportCity_Harbor_Text_WhichOneDoYouWant": (
        ("Which one",),
        ("ENGINEER: Which one do you want?$",),
    ),
    "SlateportCity_Harbor_Text_HandedScannerToStern": (
        ("SCANNER", "CAPT. STERN"),
        (
            "{PLAYER} handed the SCANNER to\\n",
            "the ENGINEER.$",
        ),
    ),
    "SlateportCity_Harbor_Text_ThisWillHelpResearch": (
        ("help our research",),
        (
            "ENGINEER: Thank you, {PLAYER}!\\p",
            "This will help our research.$",
        ),
    ),
})

# Keep internal gText_* symbol names but replace visible destination literals.
base.STRING_REPLACEMENTS = {
    'const u8 gText_LilycoveCity[] = _("BAIA DAS LUZES");':
        'const u8 gText_LilycoveCity[] = _("BAIA DAS LUZES");',
    'const u8 gText_SlateportCity[] = _("PORTO DO SAL");':
        'const u8 gText_SlateportCity[] = _("PORTO DO SAL");',
}


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
