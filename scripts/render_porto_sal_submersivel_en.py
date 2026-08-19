#!/usr/bin/env python3
from __future__ import annotations

import render_porto_sal_submersivel as base


base.CITY_TARGETS.update({
    "SlateportCity_Text_SternMoveAheadWithExploration": (
        "ENGINEER: New maps confirm\\n",
        "caverns beneath M'BOI.\\p",
        "The submersible can reach them.$",
    ),
    "SlateportCity_Text_GabbyWonderfulThanksForInterview": (
        "REPORTER: So the expedition\\n",
        "continues! Thank you.\\p",
        "We'll return when there are new\\n",
        "findings.$",
    ),
    "SlateportCity_Text_SternWhewFirstInterview": (
        "ENGINEER: Whew...\\p",
        "First live interview.\\p",
        "I'd rather face the ocean floor.$",
    ),
    "SlateportCity_Text_OhPlayerWeMadeDiscovery": (
        "ENGINEER: {PLAYER}, good timing.\\p",
        "Readings beneath M'BOI rose with\\n",
        "the latest tremors.\\p",
        "A BOND current is moving through\\n",
        "the caverns.$",
    ),
    "SlateportCity_Text_AquaWillAssumeControlOfSubmarine": (
        "HORIZON: EMERGENCY PROTOCOL.\\p",
        "The submersible is requisitioned\\n",
        "for the M'BOI anomaly.\\p",
        "Harbor staff, do not interfere.$",
    ),
    "SlateportCity_Text_SternWhatWasAllThat": (
        "ENGINEER: Requisitioned?\\p",
        "That voice came from the harbor!$",
    ),
    "SlateportCity_Text_FromHarborTryingToTakeSub": (
        "WORKER: Engineer!\\p",
        "HORIZON entered the hangar.\\p",
        "They're taking the submersible!$",
    ),
    "SlateportCity_Text_PleaseComeWithMe": (
        "ENGINEER: {PLAYER}, with me!$",
    ),
})

base.HARBOR_TARGETS.update({
    "SlateportCity_Harbor_Text_SameThugsTriedToRobAtMuseum": (
        "ENGINEER: HORIZON again...\\p",
        "I saw those uniforms during the\\n",
        "MUSEUM equipment dispute.$",
    ),
    "SlateportCity_Harbor_Text_ArchieYouAgainHideoutInLilycove": (
        "OTACILIO: You again.\\p",
        "This submersible is the only one\\n",
        "that reaches CAVERNAS DE M'BOI.\\p",
        "First, we finish loading at the\\n",
        "CENTRAL ARCHIVE.\\p",
        "Then we go to M'BOI.\\p",
        "We cannot wait for permission.$",
    ),
    "SlateportCity_Harbor_Text_CaptSternWhyStealMySubmarine": (
        "ENGINEER: You could have asked.\\p",
        "The submersible was built for\\n",
        "research, not for a faction.\\p",
        "Now we need to follow them.$",
    ),
    "SlateportCity_Harbor_Text_TeamAquaLeftNeedDive": (
        "ENGINEER: The submersible left\\n",
        "the CENTRAL ARCHIVE and dived.\\p",
        "Its route leads to M'BOI.$",
    ),
    "SlateportCity_Harbor_Text_NeedDiveToCatchSub": (
        "ENGINEER: To reach CAVERNAS DE\\n",
        "M'BOI, you need open-sea depth.\\p",
        "Use DIVE when you're ready.$",
    ),
})


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
