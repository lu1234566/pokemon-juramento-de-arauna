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
	.string "LEMBRANTE: Apagar uma historia\nporque ela incomoda quem manda\p"
	.string "e apenas outra forma de\nviolencia.$"

MagmaHideout_1F_Text_Grunt1Defeat:
	.string "LEMBRANTE: Apagar uma historia\nporque ela incomoda quem manda\p"
	.string "e apenas outra forma de\nviolencia.$"

MagmaHideout_1F_Text_Grunt1PostBattle:
	.string "LEMBRANTE: Apagar uma historia\nporque ela incomoda quem manda\p"
	.string "e apenas outra forma de\nviolencia.$"

MagmaHideout_1F_Text_Grunt2Intro:
	.string "LEMBRANTE: Apagar uma historia\nporque ela incomoda quem manda\p"
	.string "e apenas outra forma de\nviolencia.$"

MagmaHideout_1F_Text_Grunt2Defeat:
	.string "LEMBRANTE: Apagar uma historia\nporque ela incomoda quem manda\p"
	.string "e apenas outra forma de\nviolencia.$"

MagmaHideout_1F_Text_Grunt2PostBattle:
	.string "LEMBRANTE: Apagar uma historia\nporque ela incomoda quem manda\p"
	.string "e apenas outra forma de\nviolencia.$"

