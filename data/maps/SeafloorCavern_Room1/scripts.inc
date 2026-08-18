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
	.string "Voce nao deveria ter chegado\n"
	.string "ate as camaras de M'BOI.\p"
	.string "Enquanto OTACILIO estiver la\n"
	.string "embaixo, ninguem passa.$"

SeafloorCavern_Room1_Text_Grunt1Defeat:
	.string "Droga... voce passou por mim.$"

SeafloorCavern_Room1_Text_Grunt1PostBattle:
	.string "OTACILIO acredita que certas\n"
	.string "memorias so continuam ferindo.\p"
	.string "Nao vou fingir que entendo tudo.$"

SeafloorCavern_Room1_Text_Grunt2Intro:
	.string "Estas cavernas reagem a coisas\n"
	.string "que nossos sensores nao leem.\p"
	.string "Nao chegue mais perto.$"

SeafloorCavern_Room1_Text_Grunt2Defeat:
	.string "Entao nem isso te deteve...$"

SeafloorCavern_Room1_Text_Grunt2PostBattle:
	.string "Quanto mais fundo descemos,\n"
	.string "menos o ARQUIVO obedece.\p"
	.string "Talvez nunca tenha sido uma\n"
	.string "ferramenta de verdade.$"

