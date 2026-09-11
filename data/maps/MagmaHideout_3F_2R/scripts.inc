MagmaHideout_3F_2R_MapScripts::
	.byte 0

MagmaHideout_3F_2R_EventScript_Grunt10::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_10, MagmaHideout_3F_2R_Text_Grunt10Intro, MagmaHideout_3F_2R_Text_Grunt10Defeat
	msgbox MagmaHideout_3F_2R_Text_Grunt10PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_3F_2R_Text_Grunt10Intro:
	.string "REMEMBRANCER: LUZIA says memory\n"
	.string "handed back without permission is still\l"
	.string "better than memory stolen. Not\l"
	.string "everyone here agrees with that part.$"

MagmaHideout_3F_2R_Text_Grunt10Defeat:
	.string "REMEMBRANCER: HORIZON wants a stable\n"
	.string "Arauna. I want an Arauna that knows why\l"
	.string "its ruins are there.$"

MagmaHideout_3F_2R_Text_Grunt10PostBattle:
	.string "REMEMBRANCER: When a story bothers the\n"
	.string "people in charge, it becomes 'noise',\l"
	.string "then 'trauma', then it is gone from the\l"
	.string "record.$"

