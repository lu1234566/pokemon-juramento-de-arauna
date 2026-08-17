SeafloorCavern_Room4_MapScripts::
	.byte 0

SeafloorCavern_Room4_EventScript_Grunt3::
	trainerbattle_single TRAINER_GRUNT_SEAFLOOR_CAVERN_3, SeafloorCavern_Room4_Text_Grunt3Intro, SeafloorCavern_Room4_Text_Grunt3Defeat
	msgbox SeafloorCavern_Room4_Text_Grunt3PostBattle, MSGBOX_AUTOCLOSE
	end

SeafloorCavern_Room4_EventScript_Grunt4::
	trainerbattle_single TRAINER_GRUNT_SEAFLOOR_CAVERN_4, SeafloorCavern_Room4_Text_Grunt4Intro, SeafloorCavern_Room4_Text_Grunt4Defeat
	msgbox SeafloorCavern_Room4_Text_Grunt4PostBattle, MSGBOX_AUTOCLOSE
	end

SeafloorCavern_Room4_Text_Grunt3Intro:
	.string "Gravacoes antigas misturam\nordens de evacuacao, pedidos de\p"
	.string "socorro e trechos que alguem\nmarcou para exclusao.$"

SeafloorCavern_Room4_Text_Grunt3Defeat:
	.string "O ARQUIVO reage como se memoria\ne esquecimento fossem forcas\p"
	.string "fisicas. Pela primeira vez fica\nclaro que ele nunca esteve\p"
	.string "realmente sob controle humano.$"

SeafloorCavern_Room4_Text_Grunt3PostBattle:
	.string "Gravacoes antigas misturam\nordens de evacuacao, pedidos de\p"
	.string "socorro e trechos que alguem\nmarcou para exclusao.$"

SeafloorCavern_Room4_Text_Grunt4Intro:
	.string "O ARQUIVO reage como se memoria\ne esquecimento fossem forcas\p"
	.string "fisicas. Pela primeira vez fica\nclaro que ele nunca esteve\p"
	.string "realmente sob controle humano.$"

SeafloorCavern_Room4_Text_Grunt4Defeat:
	.string "Gravacoes antigas misturam\nordens de evacuacao, pedidos de\p"
	.string "socorro e trechos que alguem\nmarcou para exclusao.$"

SeafloorCavern_Room4_Text_Grunt4PostBattle:
	.string "Os sensores enlouquecem. As\ncavernas de M'BOI ainda\p"
	.string "carregam VINCULOS que o ARQUIVO\nnunca conseguiu classificar.$"

