#!/usr/bin/env python3
from __future__ import annotations

import render_arquivo_central_surface as base


def set_payload(targets, label: str, payloads: tuple[str, ...]) -> None:
    markers, _ = targets[label]
    targets[label] = (markers, payloads)


# CENTRAL ARCHIVE — B1F: evidence, responsibility, and the M'BOI record.
set_payload(base.B1F_TARGETS, "AquaHideout_B1F_Text_Grunt2Intro", (
    "HORIZON: You opened the M'BOI\\n",
    "file. You were never meant to.\\p",
    "These reports survived because\\n",
    "someone refused to erase them.$",
))
set_payload(base.B1F_TARGETS, "AquaHideout_B1F_Text_Grunt2Defeat", (
    "HORIZON: ANAHI helped build the\\n",
    "first BOND sensors.\\p",
    "That does not make her innocent.\\n",
    "Nor does it make her guilty.$",
))
set_payload(base.B1F_TARGETS, "AquaHideout_B1F_Text_Grunt2PostBattle", (
    "HORIZON: The reports call M'BOI\\n",
    "an operational failure.\\p",
    "That phrase feels too small.$",
))
set_payload(base.B1F_TARGETS, "AquaHideout_B1F_Text_Grunt3Intro", (
    "HORIZON: CIRO's father is on\\n",
    "the list of the dead.$",
))
set_payload(base.B1F_TARGETS, "AquaHideout_B1F_Text_Grunt3Defeat", (
    "HORIZON: CIRO received support\\n",
    "from us years later.\\p",
    "I don't know what he was told.$",
))
set_payload(base.B1F_TARGETS, "AquaHideout_B1F_Text_Grunt3PostBattle", (
    "HORIZON: If he learns this from\\n",
    "you, that is on us too.$",
))
set_payload(base.B1F_TARGETS, "AquaHideout_B1F_Text_Grunt5Intro", (
    "HORIZON: ELIAS approved part of\\n",
    "the M'BOI protocols.$",
))
set_payload(base.B1F_TARGETS, "AquaHideout_B1F_Text_Grunt5Defeat", (
    "HORIZON: Guilt does not erase\\n",
    "a signature.\\p",
    "A signature explains only part.$",
))
set_payload(base.B1F_TARGETS, "AquaHideout_B1F_Text_Grunt5PostBattle", (
    "HORIZON: Whole pages are nothing\\n",
    "but approvals and objections.$",
))
set_payload(base.B1F_TARGETS, "AquaHideout_B1F_Text_Grunt7Intro", (
    "HORIZON: OTACILIO lost family\\n",
    "at M'BOI.$",
))
set_payload(base.B1F_TARGETS, "AquaHideout_B1F_Text_Grunt7Defeat", (
    "HORIZON: After M'BOI, the\\n",
    "LIVING ARCHIVE became his life's\\n",
    "work.$",
))
set_payload(base.B1F_TARGETS, "AquaHideout_B1F_Text_Grunt7PostBattle", (
    "HORIZON: Understanding his pain\\n",
    "does not justify every order.$",
))

# CENTRAL ARCHIVE — B2F: evacuation, Breno, and the M'BOI departure.
set_payload(base.B2F_TARGETS, "AquaHideout_B2F_Text_MattIntro", (
    "BRENO: Earlier than expected.\\p",
    "The loading has already started.\\p",
    "My job is to slow you down.$",
))
set_payload(base.B2F_TARGETS, "AquaHideout_B2F_Text_MattDefeat", (
    "BRENO: Fine...\\n",
    "I can't buy them more time.$",
))
set_payload(base.B2F_TARGETS, "AquaHideout_B2F_Text_OurBossGotThroughHisPreparations", (
    "BRENO: Too late.\\p",
    "OTACILIO finished the transfer\\n",
    "and left for M'BOI.$",
))
set_payload(base.B2F_TARGETS, "AquaHideout_B2F_Text_MattPostBattle", (
    "BRENO: If you're chasing him,\\n",
    "go beyond BAIA DAS LUZES.\\p",
    "The caverns are under the sea.$",
))
set_payload(base.B2F_TARGETS, "AquaHideout_B2F_Text_Grunt4Intro", (
    "HORIZON: We're wiping local\\n",
    "copies. The archive is already\\n",
    "aboard the submersible.$",
))
set_payload(base.B2F_TARGETS, "AquaHideout_B2F_Text_Grunt4Defeat", (
    "HORIZON: I can't call this\\n",
    "maintenance anymore.$",
))
set_payload(base.B2F_TARGETS, "AquaHideout_B2F_Text_Grunt4PostBattle", (
    "HORIZON: The M'BOI servers were\\n",
    "the first ones loaded.$",
))
set_payload(base.B2F_TARGETS, "AquaHideout_B2F_Text_Grunt6Intro", (
    "HORIZON: Protocol says evacuate\\n",
    "the data and destroy the keys.$",
))
set_payload(base.B2F_TARGETS, "AquaHideout_B2F_Text_Grunt6Defeat", (
    "HORIZON: You want proof.\\p",
    "I understand.$",
))
set_payload(base.B2F_TARGETS, "AquaHideout_B2F_Text_Grunt6PostBattle", (
    "HORIZON: The submersible route\\n",
    "ends at the CAVERNAS DE M'BOI.$",
))
set_payload(base.B2F_TARGETS, "AquaHideout_B2F_Text_Grunt8Intro", (
    "HORIZON: OTACILIO took the full\\n",
    "copy of the BOND records.$",
))
set_payload(base.B2F_TARGETS, "AquaHideout_B2F_Text_Grunt8Defeat", (
    "HORIZON: Not everyone here knows\\n",
    "what happened at M'BOI.$",
))
set_payload(base.B2F_TARGETS, "AquaHideout_B2F_Text_Grunt8PostBattle", (
    "HORIZON: When truth depends on\\n",
    "internal permission, truth is\\n",
    "already being held captive.$",
))


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
