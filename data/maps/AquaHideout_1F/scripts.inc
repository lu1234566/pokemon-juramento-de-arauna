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
	.string "HORIZON: The director went out for a\n"
	.string "part the LIVING ARCHIVE can't do\l"
	.string "without. Don't expect me to say where.$"

AquaHideout_1F_Text_WhereMightMagmaHideoutBe:
	.string "HORIZON: The REMEMBRANCERS have set\n"
	.string "up a base near SERRA DA CINZA. Luzia\l"
	.string "wants to reach the records before we\l"
	.string "do.$"

AquaHideout_1F_Text_BossWentToJackASubmarine:
	.string "HORIZON: OTACILIO went to\n"
	.string "PORTO DO SAL. The submersible can reach\l"
	.string "the M'BOI caverns.$"

AquaHideout_1F_Text_BossIsOnRoute122:
	.string "HORIZON: OTACILIO headed for\n"
	.string "MEMORIAL DOS NOMES, on ROUTE 122. He\l"
	.string "wants the records kept there.$"

AquaHideout_1F_Text_TeamMagmaAtMtChimney:
	.string "HORIZON: The REMEMBRANCERS are at\n"
	.string "SERRA DA CINZA. Word is LUZIA means to\l"
	.string "give back memories that were taken by\l"
	.string "force.$"

AquaHideout_1F_Text_BossIsInSlateportCity:
	.string "HORIZON: OTACILIO is at PORTO DO SAL.\n"
	.string "The public demonstration of the LIVING\l"
	.string "ARCHIVE starts there.$"

AquaHideout_1F_Text_Grunt1Intro:
	.string "HORIZON: The sensors pick up unstable\n"
	.string "BONDS before DISENCHANTMENT is\l"
	.string "complete. That can save whole families.$"

AquaHideout_1F_Text_Grunt1Defeat:
	.string "HORIZON: The LIVING ARCHIVE does not\n"
	.string "erase people. It separates trauma from\l"
	.string "identity. At least that is what we were\l"
	.string "taught.$"

AquaHideout_1F_Text_Grunt1PostBattle:
	.string "HORIZON: The sensors pick up unstable\n"
	.string "BONDS before DISENCHANTMENT is\l"
	.string "complete. That can save whole families.$"

