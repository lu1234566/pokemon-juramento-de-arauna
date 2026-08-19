#!/usr/bin/env python3
from __future__ import annotations

import render_porto_sal_daily_life as base


base.TARGETS.update({
    "SlateportCity_Text_EnergyGuruSellWhatYouNeed": (
        "SHOPKEEPER: Need help training\\n",
        "your POKéMON? I have supplies.$",
    ),
    "SlateportCity_Text_OhYourPokemon": (
        "JUDGE: Ah... your {STR_VAR_1}.$",
    ),
    "SlateportCity_Text_PleaseGiveItThisEffortRibbon": (
        "JUDGE: You trained it well!\\p",
        "It deserves this EFFORT BAND.$",
    ),
    "SlateportCity_Text_ReceivedEffortRibbon": (
        "{PLAYER} received the\\n",
        "EFFORT BAND!$",
    ),
    "SlateportCity_Text_PutEffortRibbonOnMon": (
        "{PLAYER} placed the EFFORT BAND\\n",
        "on {STR_VAR_1}.$",
    ),
    "SlateportCity_Text_GoForItLittleHarder": (
        "JUDGE: It can improve more.\\p",
        "Keep training. I may have\\n",
        "something special later.$",
    ),
    "SlateportCity_Text_EffortRibbonLooksGoodOnIt": (
        "JUDGE: That EFFORT BAND looks\\n",
        "great on {STR_VAR_1}!$",
    ),
    "SlateportCity_Text_WonderIfLighthouseStartlesPokemon": (
        "MAN: The lighthouse beam reaches\\n",
        "far across the sea.\\p",
        "I wonder if it startles POKéMON.$",
    ),
    "SlateportCity_Text_SeaweedFullOfLife": (
        "COOK: Look at this seaweed!\\p",
        "It arrives fresh every morning.\\p",
        "Almost looks ready to jump.$",
    ),
    "SlateportCity_Text_HowTownIsBornAndGrows": (
        "WOMAN: Clean water brings fish\\n",
        "and harvests.\\p",
        "Where goods and people meet,\\n",
        "a market grows.\\p",
        "That's how this city grew.$",
    ),
    "SlateportCity_Text_SlateportWonderfulPlace": (
        "GIRL: Shopping with the smell\\n",
        "of the sea is the best!\\p",
        "PORTO DO SAL is one of a kind.$",
    ),
    "SlateportCity_Text_BuyBricksSoDecorWontGetDirty": (
        "GIRL: DOLLS and CUSHIONS get\\n",
        "dirty on the floor.\\p",
        "I'll buy blocks to lift them.$",
    ),
    "SlateportCity_Text_GoingToCompeteInBattleTent": (
        "BOY: I'm entering the BATTLE\\n",
        "TENT too!\\p",
        "First I need a better team.$",
    ),
    "SlateportCity_Text_BushedHikingFromMauville": (
        "MAN: Whew... I'm exhausted.\\p",
        "I walked here from inland.\\p",
        "I'd bring a BIKE next time.$",
    ),
    "SlateportCity_Text_EveryoneCallsHimCaptStern": (
        "MAN: The HARBOR ENGINEER helped\\n",
        "build the MUSEUM.\\p",
        "He also leads deep-sea trips.$",
    ),
    "SlateportCity_Text_SeaIsSoWet": (
        "SAILOR: The sea is enormous...\\p",
        "Could it hold every tear a\\n",
        "POKéMON has ever cried?$",
    ),
    "SlateportCity_Text_SinkOldBoats": (
        "SAILOR: An old ship can become\\n",
        "a shelter after retirement.\\p",
        "Sunk with care, it becomes home\\n",
        "for many POKéMON.$",
    ),
    "SlateportCity_Text_BuyTooMuch": (
        "WOMAN: Every time I visit the\\n",
        "MARKET, I buy too much.$",
    ),
    "SlateportCity_Text_GetNameRaterToHelpYou": (
        "MAN: Want to change a POKéMON's\\n",
        "nickname?\\p",
        "Ask the NAME RATER.$",
    ),
    "SlateportCity_Text_CantChangeTradeMonName": (
        "WOMAN: Traded POKéMON keep the\\n",
        "nickname they arrived with.\\p",
        "It's a trace of the TRAINER who\\n",
        "cared for them first.$",
    ),
    "SlateportCity_Text_BattleTentBuiltRecently": (
        "MAN: The BATTLE TENT opened in\\n",
        "PORTO DO SAL not long ago.\\p",
        "It isn't a GYM, but it still\\n",
        "tests a good team.$",
    ),
    "SlateportCity_Text_CaptSternBeingInterviewed": (
        "WOMAN: I thought that was a\\n",
        "famous performer.\\p",
        "It's the HARBOR ENGINEER!$",
    ),
    "SlateportCity_Text_InterviewerSoCool": (
        "GIRL: That reporter is so cool.\\p",
        "I want to tell stories all over\\n",
        "the world someday.$",
    ),
    "SlateportCity_Text_SternSaysDiscoveredSomething": (
        "BOY: The ENGINEER says they found\\n",
        "something on the seafloor.\\p",
        "I wonder what it is.$",
    ),
    "SlateportCity_Text_CaptainComeBackWithBigFish": (
        "COOK: What happened?\\p",
        "Did the expedition return with\\n",
        "a giant fish?$",
    ),
    "SlateportCity_Text_AmIOnTV": (
        "MAN: Hey! Am I on TV?$",
    ),
    "SlateportCity_Text_CaptainsACelebrity": (
        "MAN: A live interview here?\\p",
        "The ENGINEER is a celebrity now.$",
    ),
    "SlateportCity_Text_BigSmileForCamera": (
        "CAMERAMAN: ENGINEER, smile for\\n",
        "the camera!$",
    ),
    "SlateportCity_Text_MostInvaluableExperience": (
        "REPORTER: I understand...\\p",
        "That was a valuable experience.$",
    ),
})


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
