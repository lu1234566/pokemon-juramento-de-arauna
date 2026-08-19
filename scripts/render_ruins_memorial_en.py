#!/usr/bin/env python3
from __future__ import annotations

import re

import render_ruinas_memorial_surface as base


def set_payload(targets, label: str, payloads: tuple[str, ...]) -> None:
    markers, _ = targets[label]
    targets[label] = (markers, payloads)


# RUINAS DA QUEDA / Meteor Falls story bridge.
set_payload(base.METEOR_TARGETS, "MeteorFalls_1F_1R_Text_WithThisMeteorite", (
    "REMEMBRANCER: This METEORITE\\n",
    "makes the amplifier react.\\p",
    "At SERRA DA CINZA, we'll return\\n",
    "what was extracted.$",
))
set_payload(base.METEOR_TARGETS, "MeteorFalls_1F_1R_Text_DontExpectMercyFromMagma", (
    "REMEMBRANCER: If you stand\\n",
    "in the way, don't expect mercy.$",
))
set_payload(base.METEOR_TARGETS, "MeteorFalls_1F_1R_Text_HoldItRightThereMagma", (
    "HORIZON: Stop right there!\\p",
    "That METEORITE cannot be\\n",
    "activated without control.$",
))
set_payload(base.METEOR_TARGETS, "MeteorFalls_1F_1R_Text_BeSeeingYouTeamAqua", (
    "REMEMBRANCER: We have the\\n",
    "METEORITE. Next, SERRA DA CINZA.\\p",
    "HORIZON, try to keep up.$",
))
set_payload(base.METEOR_TARGETS, "MeteorFalls_1F_1R_Text_ArchieSeenYouBefore", (
    "OTACILIO: You again.\\p",
    "They don't know what that\\n",
    "amplifier could release.$",
))
set_payload(base.METEOR_TARGETS, "MeteorFalls_1F_1R_Text_BossWeShouldChaseMagma", (
    "HORIZON: Director, we need to\\n",
    "go after the REMEMBRANCERS.$",
))
set_payload(base.METEOR_TARGETS, "MeteorFalls_1F_1R_Text_ArchieYesNoTellingWhatMagmaWillDo", (
    "OTACILIO: Yes. We move now.\\p",
    "LUZIA took the METEORITE to\\n",
    "SERRA DA CINZA.$",
))
set_payload(base.METEOR_TARGETS, "MeteorFalls_1F_1R_Text_ArchieFarewell", (
    "OTACILIO: Don't confuse stopping\\n",
    "her with agreeing with me.\\p",
    "This dispute is not over.$",
))
set_payload(base.METEOR_TARGETS, "MeteorFalls_1F_1R_Text_MeetProfCozmo", (
    "I'm a mineral researcher.\\p",
    "The REMEMBRANCERS asked me to\\n",
    "guide them through RUINAS DA\\n",
    "QUEDA.\\p",
    "Then they took my METEORITE.\\p",
    "HORIZON arrived right after.\\p",
    "I don't know who to trust.$",
))
set_payload(base.METEOR_TARGETS, "MeteorFalls_1F_1R_Text_WhatsTeamMagmaDoingAtMtChimney", (
    "RESEARCHER: The REMEMBRANCERS\\n",
    "took my METEORITE to\\n",
    "SERRA DA CINZA. Why?$",
))

# MEMORIAL DOS NOMES confrontation and aftermath.
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_Grunt1Intro", (
    "HORIZON: Step away.\\p",
    "These plaques are being removed.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_Grunt1Defeat", (
    "HORIZON: You don't understand\\n",
    "what we're trying to contain.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_Grunt1PostBattle", (
    "HORIZON: Scanning them first\\n",
    "doesn't make removal right.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_Grunt2Intro", (
    "HORIZON: The MEMORIAL is under\\n",
    "a security protocol.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_Grunt2Defeat", (
    "HORIZON: I didn't expect\\n",
    "resistance here.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_Grunt2PostBattle", (
    "HORIZON: Some orders sound worse\\n",
    "when you say them out loud.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_Grunt3Intro", (
    "HORIZON: These records are going\\n",
    "to the CENTRAL ARCHIVE.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_Grunt3Defeat", (
    "HORIZON: Fine... You won\\n",
    "this part of the argument.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_Grunt3PostBattle", (
    "HORIZON: Cataloging memory\\n",
    "doesn't make it ours.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_Grunt4Intro", (
    "HORIZON: Don't touch the plaques\\n",
    "marked for removal.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_Grunt4Defeat", (
    "HORIZON: This complicates\\n",
    "the operation.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_Grunt4PostBattle", (
    "HORIZON: OTACILIO thinks some\\n",
    "wounds need an ending.\\p",
    "I'm still thinking about that.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_ArchieWeGotTheOrbLetsGo", (
    "OTACILIO: We have the\\n",
    "RECORD-MATRIX. Recall the team.\\p",
    "We're leaving.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_BothOrbsTakenMagmaLeftThis", (
    "GUARDIAN: HORIZON took one\\n",
    "RECORD-MATRIX from here.\\p",
    "The REMEMBRANCERS took another.\\p",
    "They left this emblem behind.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_OrbsHaveBeenTaken", (
    "GUARDIAN: Two RECORD-MATRICES\\n",
    "were removed from the memorial.\\p",
    "One by HORIZON. One by the\\n",
    "REMEMBRANCERS.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_GroudonKyogreAwakened", (
    "GUARDIAN: Both ancient currents\\n",
    "reacted to the collapse.\\p",
    "What was kept is returning\\n",
    "without asking permission.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_ThoseTwoMenReturnedOrbs", (
    "GUARDIAN: OTACILIO and LUZIA\\n",
    "returned both records.\\p",
    "Neither left with all the answers.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_SuperAncientPokemonTaughtUs", (
    "GUARDIAN: The collapse showed us\\n",
    "memory and forgetting become\\n",
    "violence when one person chooses\\n",
    "for everyone else.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_WillYouHearOutMyTale", (
    "GUARDIAN: This is the MEMORIAL\\n",
    "DOS NOMES. We repeat stories\\n",
    "so silence does not win.\\p",
    "Would you like to hear one?$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_GroudonKyogreTale", (
    "GUARDIAN: Long before HORIZON,\\n",
    "people spoke of two currents.\\p",
    "One pulls memory back.\\n",
    "The other lets BONDS end.\\p",
    "The OATH exists so no one\\n",
    "chooses that alone.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_WellThatTooIsFine", (
    "GUARDIAN: That's all right.\\p",
    "A story also needs someone\\n",
    "willing to hear it.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_MaxieSilence", (
    "LUZIA: We returned what we never\\n",
    "had the right to take.\\p",
    "Neither OTACILIO nor I did.$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_HearTheNewLegendOfHoenn", (
    "GUARDIAN: After M'BOI, the story\\n",
    "of this memorial changed.\\p",
    "Would you hear the new version?$",
))
set_payload(base.MEMORIAL_TARGETS, "MtPyre_Summit_Text_HoennTrioTale", (
    "GUARDIAN: For a long time, we said\\n",
    "remembering was always just,\\n",
    "and forgetting was always loss.\\p",
    "M'BOI taught us absolutes can\\n",
    "hurt too.\\p",
    "The new OATH does not demand\\n",
    "every memory or erase all pain.\\p",
    "It demands that no one person\\n",
    "decide for everyone else.$",
))

# Visible item surface for the unchanged ITEM_MAGMA_EMBLEM slot.
base.ITEM_NAME_NEW = '.name = _("REMEM. EMBLEM"),'
base.ITEM_DESC_RE = re.compile(
    r'(?ms)^static const u8 sMagmaEmblemDesc\[\] = _\(\n'
    r'(?P<body>.*?^\s*"[^"\n]*"\);)'
)
base.ITEM_DESC_NEW = (
    'static const u8 sMagmaEmblemDesc[] = _(\n'
    '    "An emblem carried\\n"\n'
    '    "by REMEMBRANCERS.\\n"\n'
    '    "Opens their base.");'
)


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
