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
	.string "LEMBRANTE: Apagar uma historia\nporque ela incomoda quem manda\p"
	.string "e apenas outra forma de\nviolencia.$"

MagmaHideout_3F_1R_Text_Grunt9Defeat:
	.string "LEMBRANTE: Apagar uma historia\nporque ela incomoda quem manda\p"
	.string "e apenas outra forma de\nviolencia.$"

MagmaHideout_3F_1R_Text_Grunt9PostBattle:
	.string "LEMBRANTE: Apagar uma historia\nporque ela incomoda quem manda\p"
	.string "e apenas outra forma de\nviolencia.$"

MagmaHideout_3F_1R_Text_Grunt16Intro:
	.string "HORIZONTE: O Arquivo preserva o\nque o tempo destruiria. Um dia\p"
	.string "voces vao agradecer por nao\nprecisarem mais sofrer para\p"
	.string "lembrar.$"

MagmaHideout_3F_1R_Text_Grunt16Defeat:
	.string "LEMBRANTE: Apagar uma historia\nporque ela incomoda quem manda\p"
	.string "e apenas outra forma de\nviolencia.$"

MagmaHideout_3F_1R_Text_Grunt16PostBattle:
	.string "HORIZONTE: O Arquivo preserva o\nque o tempo destruiria. Um dia\p"
	.string "voces vao agradecer por nao\nprecisarem mais sofrer para\p"
	.string "lembrar.$"

