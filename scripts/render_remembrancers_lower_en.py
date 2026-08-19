#!/usr/bin/env python3
from __future__ import annotations

import render_lembrantes_lower_surface as base


base.TARGETS_1F.update({
    "MagmaHideout_1F_Text_Grunt1Intro": (
        "REMEMBRANCER: This base keeps\\n",
        "copies HORIZON tried to remove\\n",
        "from circulation.$",
    ),
    "MagmaHideout_1F_Text_Grunt1Defeat": (
        "REMEMBRANCER: Not every lost\\n",
        "record was an accident.\\p",
        "That's why I joined.$",
    ),
    "MagmaHideout_1F_Text_Grunt1PostBattle": (
        "REMEMBRANCER: Go upstairs and\\n",
        "you'll see we don't all agree\\n",
        "with LUZIA about everything.$",
    ),
    "MagmaHideout_1F_Text_Grunt2Intro": (
        "REMEMBRANCER: The MEMORIAL\\n",
        "keeps names. We keep evidence\\n",
        "of how they tried to erase them.$",
    ),
    "MagmaHideout_1F_Text_Grunt2Defeat": (
        "REMEMBRANCER: I want stories\\n",
        "returned, not forced into\\n",
        "someone's mind.$",
    ),
    "MagmaHideout_1F_Text_Grunt2PostBattle": (
        "REMEMBRANCER: Ask upstairs who\\n",
        "decided to use the\\n",
        "RECORD-MATRIX.$",
    ),
})

base.TARGETS_2F1.update({
    "MagmaHideout_2F_1R_Text_Grunt14Intro": (
        "REMEMBRANCER: These notebooks\\n",
        "came from M'BOI families.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt14Defeat": (
        "REMEMBRANCER: HORIZON stamped\\n",
        "them 'therapeutic material.'\\p",
        "I call them testimony.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt14PostBattle": (
        "REMEMBRANCER: We copied it all\\n",
        "before another disposal order\\n",
        "could arrive.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt3Intro": (
        "REMEMBRANCER: Some statements\\n",
        "have whole passages blacked out.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt3Defeat": (
        "REMEMBRANCER: I can't prove who\\n",
        "ordered each line hidden.\\p",
        "Only that someone did.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt3PostBattle": (
        "REMEMBRANCER:\\n",
        "Incomplete proof still beats\\n",
        "perfect silence.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt4Intro": (
        "REMEMBRANCER: This batch came\\n",
        "from a storehouse set to burn.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt4Defeat": (
        "REMEMBRANCER:\\n",
        "The LEAGUE and HORIZON signed\\n",
        "the same file.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt4PostBattle": (
        "REMEMBRANCER:\\n",
        "ELIAS appears on approvals.\\p",
        "There are objections too.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt5Intro": (
        "REMEMBRANCER: Don't mistake an\\n",
        "archive for the whole truth.\\p",
        "Documents can lie too.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt5Defeat": (
        "REMEMBRANCER:\\n",
        "That's why we cross-check names,\\n",
        "dates and testimony.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt5PostBattle": (
        "REMEMBRANCER:\\n",
        "LUZIA wants everything opened.\\p",
        "I think some voices should still\\n",
        "choose when to speak.$",
    ),
})

base.TARGETS_2F2.update({
    "MagmaHideout_2F_2R_Text_Grunt15Intro": (
        "REMEMBRANCER: We argue over one\\n",
        "simple, impossible question:\\p",
        "who may return a memory?$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt15Defeat": (
        "REMEMBRANCER:\\n",
        "If someone asked to forget,\\n",
        "can we choose the opposite?$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt15PostBattle": (
        "REMEMBRANCER: LUZIA says the\\n",
        "theft came before consent.\\p",
        "She's not wrong about that.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt6Intro": (
        "REMEMBRANCER: The problem is\\n",
        "what comes next: returning\\n",
        "everything at once.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt6Defeat": (
        "REMEMBRANCER:\\n",
        "Truth can save someone.\\p",
        "It can also crush a person who\\n",
        "never chose to receive it.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt6PostBattle": (
        "REMEMBRANCER: I follow LUZIA\\n",
        "because she fights erasure.\\p",
        "Not because she's infallible.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt7Intro": (
        "REMEMBRANCER:\\n",
        "HORIZON calls this instability.\\p",
        "We call them people.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt7Defeat": (
        "REMEMBRANCER: But a person isn't\\n",
        "an archive to restore without\\n",
        "asking.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt7PostBattle": (
        "REMEMBRANCER:\\n",
        "Maybe the OATH is harder than\\n",
        "choosing a side.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt8Intro": (
        "REMEMBRANCER: RAUL ordered the\\n",
        "upper floor prepared.\\p",
        "LUZIA will use the MATRIX.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt8Defeat": (
        "REMEMBRANCER: No one knows how\\n",
        "the current will react.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt8PostBattle": (
        "REMEMBRANCER:\\n",
        "If she's wrong, I hope someone\\n",
        "can stop her.$",
    ),
})


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
