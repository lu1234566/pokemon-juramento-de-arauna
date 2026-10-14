MagmaHideout_3F_1R_MapScripts::
	.byte 0

MagmaHideout_3F_1R_EventScript_Grunt9::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_9, MagmaHideout_3F_1R_Text_Grunt9Intro, MagmaHideout_3F_1R_Text_Grunt9Defeat
	msgbox MagmaHideout_3F_1R_Text_Grunt9PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_3F_1R_EventScript_Grunt16::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_16, MagmaHideout_3F_1R_Text_Grunt16Intro, MagmaHideout_3F_1R_Text_Grunt16Defeat
	msgbox MagmaHideout_3F_1R_Text_Grunt16PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_3F_1R_Text_Grunt9Intro:
	.string "REMEMBRANCER: The RECORD-MATRIX\n"
	.string "responds to ancient BONDS.$"

MagmaHideout_3F_1R_Text_Grunt9Defeat:
	.string "REMEMBRANCER:\n"
	.string "It does not contain memory.\p"
	.string "It points to where memory was\n"
	.string "pushed.$"

MagmaHideout_3F_1R_Text_Grunt9PostBattle:
	.string "REMEMBRANCER: LUZIA wants to\n"
	.string "open the current and let it all\n"
	.string "return.$"

MagmaHideout_3F_1R_Text_Grunt16Intro:
	.string "REMEMBRANCER: The sensors are\n"
	.string "already off the scale.$"

MagmaHideout_3F_1R_Text_Grunt16Defeat:
	.string "REMEMBRANCER: This doesn't look\n"
	.string "like controlled restoration.$"

MagmaHideout_3F_1R_Text_Grunt16PostBattle:
	.string "REMEMBRANCER: Reach LUZIA and\n"
	.string "ask if she still knows justice\n"
	.string "from urgency.$"

