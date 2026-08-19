#!/usr/bin/env python3
from __future__ import annotations

import render_mboi_climax_surface as base


def set_payload(label: str, payloads: tuple[str, ...]) -> None:
    markers, _ = base.TARGETS[label]
    base.TARGETS[label] = (markers, payloads)


set_payload("SeafloorCavern_Room9_Text_ArchieHoldItRightThere", (
    "OTACILIO: Stop there.\\p",
    "Do not touch the archive core.$",
))
set_payload("SeafloorCavern_Room9_Text_ArchieSoItWasYou", (
    "OTACILIO: So you opened the\\n",
    "M'BOI files.\\p",
    "Now you know why I came.$",
))
set_payload("SeafloorCavern_Room9_Text_ArchieBeholdKyogre", (
    "OTACILIO: This is where it\\n",
    "began.\\p",
    "Beneath M'BOI runs a current\\n",
    "that pulls BONDS back.$",
))
set_payload("SeafloorCavern_Room9_Text_ArchieYouMustDisappear", (
    "OTACILIO: If I shut it down,\\n",
    "we lose our only chance to\\n",
    "control the DISENCHANTMENT.\\p",
    "I won't allow that.$",
))
set_payload("SeafloorCavern_Room9_Text_ArchieDefeat", (
    "OTACILIO: Even after winning,\\n",
    "you still don't understand\\n",
    "what is at stake.$",
))
set_payload("SeafloorCavern_Room9_Text_ArchieWithThisRedOrb", (
    "OTACILIO: The RECORD-MATRIX\\n",
    "will sync the LIVING ARCHIVE\\n",
    "with that ancient current.$",
))
set_payload("SeafloorCavern_Room9_Text_RedOrbShinesByItself", (
    "The RECORD-MATRIX responds\\n",
    "without a command.\\p",
    "The archive breaks containment.$",
))
set_payload("SeafloorCavern_Room9_Text_ArchieWhereDidKyogreGo", (
    "OTACILIO: No...\\p",
    "I did not order this.$",
))
set_payload("SeafloorCavern_Room9_Text_ArchieAMessageFromOutside", (
    "OTACILIO: Central, respond.\\p",
    "What is happening outside?$",
))
set_payload("SeafloorCavern_Room9_Text_ArchieWhatRainingTooHard", (
    "OTACILIO: Readings are rising\\n",
    "across Arauna?\\p",
    "That was not possible.$",
))
set_payload("SeafloorCavern_Room9_Text_ArchieWhyDidKyogreDisappear", (
    "OTACILIO: The LIVING ARCHIVE\\n",
    "is not containing the current.\\p",
    "It spread it.$",
))
set_payload("SeafloorCavern_Room9_Text_MaxieWhatHaveYouWrought", (
    "LUZIA: OTACILIO, what happened?\\p",
    "You opened M'BOI to all Arauna.$",
))
set_payload("SeafloorCavern_Room9_Text_ArchieDontGetAllHighAndMighty", (
    "OTACILIO: I wanted to end\\n",
    "the pain, not spread it.\\p",
    "This was not supposed to happen.$",
))
set_payload("SeafloorCavern_Room9_Text_MaxieWeDontHaveTimeToArgue", (
    "LUZIA: We have no time to\\n",
    "argue about blame.\\p",
    "Both currents reacted.$",
))
set_payload("SeafloorCavern_Room9_Text_MaxieComeOnPlayer", (
    "LUZIA: Come on.\\p",
    "We need to see what happened\\n",
    "in AGUAS DE M'BOI.$",
))


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
