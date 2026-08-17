SeafloorCavern_Room3_MapScripts::
	.byte 0

SeafloorCavern_Room3_EventScript_Shelly::
	trainerbattle_single TRAINER_SHELLY_SEAFLOOR_CAVERN, SeafloorCavern_Room3_Text_ShellyIntro, SeafloorCavern_Room3_Text_ShellyDefeat
	msgbox SeafloorCavern_Room3_Text_ShellyPostBattle, MSGBOX_AUTOCLOSE
	end

SeafloorCavern_Room3_EventScript_Grunt5::
	trainerbattle_single TRAINER_GRUNT_SEAFLOOR_CAVERN_5, SeafloorCavern_Room3_Text_Grunt5Intro, SeafloorCavern_Room3_Text_Grunt5Defeat
	msgbox SeafloorCavern_Room3_Text_Grunt5PostBattle, MSGBOX_AUTOCLOSE
	end

SeafloorCavern_Room3_Text_ShellyIntro:
	.string "Gravacoes antigas misturam\nordens de evacuacao, pedidos de\p"
	.string "socorro e trechos que alguem\nmarcou para exclusao.$"

SeafloorCavern_Room3_Text_ShellyDefeat:
	.string "Ahahahaha!\p"
	.string "Ouch!$"

SeafloorCavern_Room3_Text_ShellyPostBattle:
	.string "OTACILIO e LUZIA chegaram ao\nmesmo lugar por razoes opostas:\p"
	.string "um quer encerrar a dor; a outra\nquer devolver tudo. Nenhum\p"
	.string "perguntou a quem tera de viver\ncom a escolha.$"

SeafloorCavern_Room3_Text_Grunt5Intro:
	.string "Gravacoes antigas misturam\nordens de evacuacao, pedidos de\p"
	.string "socorro e trechos que alguem\nmarcou para exclusao.$"

SeafloorCavern_Room3_Text_Grunt5Defeat:
	.string "Gravacoes antigas misturam\nordens de evacuacao, pedidos de\p"
	.string "socorro e trechos que alguem\nmarcou para exclusao.$"

SeafloorCavern_Room3_Text_Grunt5PostBattle:
	.string "O ARQUIVO reage como se memoria\ne esquecimento fossem forcas\p"
	.string "fisicas. Pela primeira vez fica\nclaro que ele nunca esteve\p"
	.string "realmente sob controle humano.$"

