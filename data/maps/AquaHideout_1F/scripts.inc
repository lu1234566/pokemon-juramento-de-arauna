AquaHideout_1F_MapScripts::
	.byte 0

@ The below two entrance guards give hints about what to do to progress the story
AquaHideout_1F_EventScript_HideoutEntranceGrunt1::
	lock
	faceplayer
	goto_if_set FLAG_GROUDON_AWAKENED_MAGMA_HIDEOUT, AquaHideout_1F_EventScript_SlateportHint1
	goto_if_set FLAG_RECEIVED_RED_OR_BLUE_ORB, AquaHideout_1F_EventScript_MagmaHideoutHint1
	msgbox AquaHideout_1F_Text_OurBossIsSnatchingSomething, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_MagmaHideoutHint1::
	msgbox AquaHideout_1F_Text_WhereMightMagmaHideoutBe, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_SlateportHint1::
	msgbox AquaHideout_1F_Text_BossWentToJackASubmarine, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_HideoutEntranceGrunt2::
	lock
	faceplayer
	goto_if_set FLAG_GROUDON_AWAKENED_MAGMA_HIDEOUT, AquaHideout_1F_EventScript_SlateportHint2
	goto_if_set FLAG_RECEIVED_RED_OR_BLUE_ORB, AquaHideout_1F_EventScript_MagmaHideoutHint2
	msgbox AquaHideout_1F_Text_BossIsOnRoute122, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_MagmaHideoutHint2::
	msgbox AquaHideout_1F_Text_TeamMagmaAtMtChimney, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_SlateportHint2::
	msgbox AquaHideout_1F_Text_BossIsInSlateportCity, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_Grunt1::
	trainerbattle_single TRAINER_GRUNT_AQUA_HIDEOUT_1, AquaHideout_1F_Text_Grunt1Intro, AquaHideout_1F_Text_Grunt1Defeat, AquaHideout_1F_EventScript_Grunt1Defeated
	msgbox AquaHideout_1F_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

AquaHideout_1F_EventScript_Grunt1Defeated::
	msgbox AquaHideout_1F_Text_Grunt1PostBattle, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_Text_OurBossIsSnatchingSomething:
	.string "HORIZON: The director left to\n"
	.string "find a key LIVING ARCHIVE\n"
	.string "component.\p"
	.string "Do not expect me to say where.$"

AquaHideout_1F_Text_WhereMightMagmaHideoutBe:
	.string "HORIZON: The REMEMBRANCERS built\n"
	.string "a base near ASHEN RIDGE.\p"
	.string "Luzia wants the records before\n"
	.string "we can reach them.$"

AquaHideout_1F_Text_BossWentToJackASubmarine:
	.string "HORIZON: OTACILIO went to PORTO\n"
	.string "DO SAL.\p"
	.string "The submersible can reach the\n"
	.string "M'BOI caverns.$"

AquaHideout_1F_Text_BossIsOnRoute122:
	.string "HORIZON: OTACILIO went to the\n"
	.string "MEMORIAL OF NAMES on ROUTE 122.\p"
	.string "He wants the records kept there.$"

AquaHideout_1F_Text_TeamMagmaAtMtChimney:
	.string "HORIZON: The REMEMBRANCERS are\n"
	.string "at ASHEN RIDGE.\p"
	.string "They say LUZIA plans to return\n"
	.string "memories taken by force.$"

AquaHideout_1F_Text_BossIsInSlateportCity:
	.string "HORIZON: OTACILIO is in PORTO DO\n"
	.string "SAL.\p"
	.string "The public LIVING ARCHIVE demo\n"
	.string "starts there.$"

AquaHideout_1F_Text_Grunt1Intro:
	.string "HORIZON: Our sensors detect\n"
	.string "unstable BONDS before full\n"
	.string "DISENCHANTMENT.\p"
	.string "That can save whole families.$"

AquaHideout_1F_Text_Grunt1Defeat:
	.string "HORIZON: The LIVING ARCHIVE does\n"
	.string "not erase people.\p"
	.string "It separates trauma from\n"
	.string "identity. At least, that is what\n"
	.string "we were taught.$"

AquaHideout_1F_Text_Grunt1PostBattle:
	.string "HORIZON: Our sensors detect\n"
	.string "unstable BONDS before full\n"
	.string "DISENCHANTMENT.\p"
	.string "That can save whole families.$"

