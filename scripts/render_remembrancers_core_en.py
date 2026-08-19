#!/usr/bin/env python3
from __future__ import annotations

import render_lembrantes_core_surface as base


base.TARGETS_3F1.update({
    "MagmaHideout_3F_1R_Text_Grunt9Intro": (
        "REMEMBRANCER: The RECORD-MATRIX\\n",
        "responds to ancient BONDS.$",
    ),
    "MagmaHideout_3F_1R_Text_Grunt9Defeat": (
        "REMEMBRANCER:\\n",
        "It does not contain memory.\\p",
        "It points to where memory was\\n",
        "pushed.$",
    ),
    "MagmaHideout_3F_1R_Text_Grunt9PostBattle": (
        "REMEMBRANCER: LUZIA wants to\\n",
        "open the current and let it all\\n",
        "return.$",
    ),
    "MagmaHideout_3F_1R_Text_Grunt16Intro": (
        "REMEMBRANCER: The sensors are\\n",
        "already off the scale.$",
    ),
    "MagmaHideout_3F_1R_Text_Grunt16Defeat": (
        "REMEMBRANCER: This doesn't look\\n",
        "like controlled restoration.$",
    ),
    "MagmaHideout_3F_1R_Text_Grunt16PostBattle": (
        "REMEMBRANCER: Reach LUZIA and\\n",
        "ask if she still knows justice\\n",
        "from urgency.$",
    ),
})

base.TARGETS_3F2.update({
    "MagmaHideout_3F_2R_Text_Grunt10Intro": (
        "REMEMBRANCER: RAUL sealed the\\n",
        "access.\\p",
        "The activation has started.$",
    ),
    "MagmaHideout_3F_2R_Text_Grunt10Defeat": (
        "REMEMBRANCER: I should be up\\n",
        "there helping.\\p",
        "Part of me is relieved I'm not.$",
    ),
    "MagmaHideout_3F_2R_Text_Grunt10PostBattle": (
        "REMEMBRANCER: Don't let HORIZON\\n",
        "take the MATRIX.\\p",
        "Don't let LUZIA use it without\\n",
        "limits either.$",
    ),
})

base.TARGETS_4F.update({
    "MagmaHideout_4F_Text_Grunt11Intro": (
        "REMEMBRANCER:\\n",
        "The core is reacting.\\p",
        "Stay away from the equipment.$",
    ),
    "MagmaHideout_4F_Text_Grunt11Defeat": (
        "REMEMBRANCER: Readings jumped\\n",
        "when LUZIA touched the MATRIX.$",
    ),
    "MagmaHideout_4F_Text_Grunt11PostBattle": (
        "REMEMBRANCER:\\n",
        "This isn't returning one story\\n",
        "at a time.\\p",
        "It's pulling thousands.$",
    ),
    "MagmaHideout_4F_Text_Grunt12Intro": (
        "REMEMBRANCER:\\n",
        "LUZIA asked for trust.\\p",
        "I wish I'd asked for a plan.$",
    ),
    "MagmaHideout_4F_Text_Grunt12Defeat": (
        "REMEMBRANCER: HORIZON will use\\n",
        "this against all of us.$",
    ),
    "MagmaHideout_4F_Text_Grunt12PostBattle": (
        "REMEMBRANCER: And they may be\\n",
        "right about the risk.\\p",
        "I hate admitting that.$",
    ),
    "MagmaHideout_4F_Text_Grunt13Intro": (
        "REMEMBRANCER:\\n",
        "The MATRIX opened a passage\\n",
        "we don't know how to close.$",
    ),
    "MagmaHideout_4F_Text_Grunt13Defeat": (
        "REMEMBRANCER:\\n",
        "I can't call this simple\\n",
        "restoration anymore.$",
    ),
    "MagmaHideout_4F_Text_Grunt13PostBattle": (
        "REMEMBRANCER:\\n",
        "Go. If LUZIA won't hear us,\\n",
        "maybe she'll hear you.$",
    ),
    "MagmaHideout_4F_Text_TabithaIntro": (
        "RAUL: Enough.\\p",
        "You've seen more of this base\\n",
        "than you should have.$",
    ),
    "MagmaHideout_4F_Text_TabithaDefeat": (
        "RAUL: Damn...\\p",
        "Then pass. But beating me does\\n",
        "not make you right.$",
    ),
    "MagmaHideout_4F_Text_TabithaPostBattle": (
        "RAUL: I follow LUZIA because I\\n",
        "saw families erased on paper.\\p",
        "That doesn't mean I'm not afraid\\n",
        "of what she'll do.$",
    ),
    "MagmaHideout_4F_Text_MaxieAwakenGroudon": (
        "LUZIA: This RECORD-MATRIX was\\n",
        "built to find what the ARCHIVE\\n",
        "tore away.\\p",
        "Today it returns to Arauna.$",
    ),
    "MagmaHideout_4F_Text_MaxieGroudonWhatsWrong": (
        "LUZIA: Wait...\\p",
        "The current isn't following the\\n",
        "MATRIX.\\p",
        "It's pulling everything.$",
    ),
    "MagmaHideout_4F_Text_MaxieOhItWasYou": (
        "LUZIA: You made it this far.\\p",
        "If you came to stop me, show me\\n",
        "another way.$",
    ),
    "MagmaHideout_4F_Text_MaxieDefeat": (
        "LUZIA: Losing a battle doesn't\\n",
        "make HORIZON right.\\p",
        "But I heard what you showed me.$",
    ),
    "MagmaHideout_4F_Text_MaxieImGoingAfterGroudon": (
        "LUZIA: The current escaped.\\p",
        "Signals lead toward the coast.\\p",
        "I'm going to PORTO DO SAL before\\n",
        "HORIZON gets there.$",
    ),
})


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
