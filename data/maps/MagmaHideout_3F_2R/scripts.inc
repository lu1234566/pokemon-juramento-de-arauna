MagmaHideout_3F_2R_MapScripts::
	.byte 0

MagmaHideout_3F_2R_EventScript_Grunt10::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_10, MagmaHideout_3F_2R_Text_Grunt10Intro, MagmaHideout_3F_2R_Text_Grunt10Defeat
	msgbox MagmaHideout_3F_2R_Text_Grunt10PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_3F_2R_Text_Grunt10Intro:
	.string "LEMBRANTE: Apagar uma historia\nporque ela incomoda quem manda\p"
	.string "e apenas outra forma de\nviolencia.$"

MagmaHideout_3F_2R_Text_Grunt10Defeat:
	.string "LEMBRANTE: Apagar uma historia\nporque ela incomoda quem manda\p"
	.string "e apenas outra forma de\nviolencia.$"

MagmaHideout_3F_2R_Text_Grunt10PostBattle:
	.string "LEMBRANTE: Apagar uma historia\nporque ela incomoda quem manda\p"
	.string "e apenas outra forma de\nviolencia.$"

