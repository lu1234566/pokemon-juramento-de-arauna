SeafloorCavern_Room1_MapScripts::
	.byte 0

SeafloorCavern_Room1_EventScript_Grunt1::
	trainerbattle_single TRAINER_GRUNT_SEAFLOOR_CAVERN_1, SeafloorCavern_Room1_Text_Grunt1Intro, SeafloorCavern_Room1_Text_Grunt1Defeat
	msgbox SeafloorCavern_Room1_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

SeafloorCavern_Room1_EventScript_Grunt2::
	trainerbattle_single TRAINER_GRUNT_SEAFLOOR_CAVERN_2, SeafloorCavern_Room1_Text_Grunt2Intro, SeafloorCavern_Room1_Text_Grunt2Defeat
	msgbox SeafloorCavern_Room1_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

SeafloorCavern_Room1_Text_Grunt1Intro:
	.string "O ARQUIVO reage como se memoria\ne esquecimento fossem forcas\p"
	.string "fisicas. Pela primeira vez fica\nclaro que ele nunca esteve\p"
	.string "realmente sob controle humano.$"

SeafloorCavern_Room1_Text_Grunt1Defeat:
	.string "O ARQUIVO reage como se memoria\ne esquecimento fossem forcas\p"
	.string "fisicas. Pela primeira vez fica\nclaro que ele nunca esteve\p"
	.string "realmente sob controle humano.$"

SeafloorCavern_Room1_Text_Grunt1PostBattle:
	.string "Gravacoes antigas misturam\nordens de evacuacao, pedidos de\p"
	.string "socorro e trechos que alguem\nmarcou para exclusao.$"

SeafloorCavern_Room1_Text_Grunt2Intro:
	.string "Gravacoes antigas misturam\nordens de evacuacao, pedidos de\p"
	.string "socorro e trechos que alguem\nmarcou para exclusao.$"

SeafloorCavern_Room1_Text_Grunt2Defeat:
	.string "Os sensores enlouquecem. As\ncavernas de M'BOI ainda\p"
	.string "carregam VINCULOS que o ARQUIVO\nnunca conseguiu classificar.$"

SeafloorCavern_Room1_Text_Grunt2PostBattle:
	.string "Gravacoes antigas misturam\nordens de evacuacao, pedidos de\p"
	.string "socorro e trechos que alguem\nmarcou para exclusao.$"

