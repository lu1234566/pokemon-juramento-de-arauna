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
	.string "REMEMBRANCER: Keeping a name can be\n"
	.string "resistance. Forcing someone to live it\l"
	.string "all again can be violence.$"

MagmaHideout_3F_1R_Text_Grunt9Defeat:
	.string "REMEMBRANCER: HORIZON wants a stable\n"
	.string "Arauna. I want an Arauna that knows why\l"
	.string "its ruins are there.$"

MagmaHideout_3F_1R_Text_Grunt9PostBattle:
	.string "REMEMBRANCER: When a story bothers the\n"
	.string "people in charge, it becomes 'noise',\l"
	.string "then 'trauma', then it is gone from the\l"
	.string "record.$"

MagmaHideout_3F_1R_Text_Grunt16Intro:
	.string "REMEMBRANCER: LUZIA says memory\n"
	.string "handed back without permission is still\l"
	.string "better than memory stolen. Not\l"
	.string "everyone here agrees with that part.$"

MagmaHideout_3F_1R_Text_Grunt16Defeat:
	.string "REMEMBRANCER: LUZIA says memory\n"
	.string "handed back without permission is still\l"
	.string "better than memory stolen. Not\l"
	.string "everyone here agrees with that part.$"

MagmaHideout_3F_1R_Text_Grunt16PostBattle:
	.string "REMEMBRANCER: When a story bothers the\n"
	.string "people in charge, it becomes 'noise',\l"
	.string "then 'trauma', then it is gone from the\l"
	.string "record.$"

