MagmaHideout_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MagmaHideout_1F_OnTransition
	.byte 0

MagmaHideout_1F_OnTransition:
	setvar VAR_JAGGED_PASS_ASH_WEATHER, 0
	end

MagmaHideout_1F_EventScript_Grunt1::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_1, MagmaHideout_1F_Text_Grunt1Intro, MagmaHideout_1F_Text_Grunt1Defeat
	msgbox MagmaHideout_1F_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_1F_EventScript_Grunt2::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_2, MagmaHideout_1F_Text_Grunt2Intro, MagmaHideout_1F_Text_Grunt2Defeat
	msgbox MagmaHideout_1F_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_1F_Text_Grunt1Intro:
	.string "REMEMBRANCER: Keeping a name can be\n"
	.string "resistance. Forcing someone to live it\l"
	.string "all again can be violence.$"

MagmaHideout_1F_Text_Grunt1Defeat:
	.string "REMEMBRANCER: HORIZON wants a stable\n"
	.string "Arauna. I want an Arauna that knows why\l"
	.string "its ruins are there.$"

MagmaHideout_1F_Text_Grunt1PostBattle:
	.string "REMEMBRANCER: When a story bothers the\n"
	.string "people in charge, it becomes 'noise',\l"
	.string "then 'trauma', then it is gone from the\l"
	.string "record.$"

MagmaHideout_1F_Text_Grunt2Intro:
	.string "REMEMBRANCER: When a story bothers the\n"
	.string "people in charge, it becomes 'noise',\l"
	.string "then 'trauma', then it is gone from the\l"
	.string "record.$"

MagmaHideout_1F_Text_Grunt2Defeat:
	.string "REMEMBRANCER: LUZIA says memory\n"
	.string "handed back without permission is still\l"
	.string "better than memory stolen. Not\l"
	.string "everyone here agrees with that part.$"

MagmaHideout_1F_Text_Grunt2PostBattle:
	.string "REMEMBRANCER: When a story bothers the\n"
	.string "people in charge, it becomes 'noise',\l"
	.string "then 'trauma', then it is gone from the\l"
	.string "record.$"

