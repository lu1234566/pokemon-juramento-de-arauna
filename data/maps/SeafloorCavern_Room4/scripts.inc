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
	.string "Daqui para baixo, o ARQUIVO\n"
	.string "deixa de responder direito.\p"
	.string "Nao e lugar para curiosos.$"

SeafloorCavern_Room4_Text_Grunt3Defeat:
	.string "Voce realmente vai continuar?$"

SeafloorCavern_Room4_Text_Grunt3PostBattle:
	.string "As gravacoes daqui misturam\n"
	.string "evacuacao, socorro e silencio.\p"
	.string "Talvez por isso OTACILIO tenha\n"
	.string "vindo pessoalmente.$"

SeafloorCavern_Room4_Text_Grunt4Intro:
	.string "O nucleo esta logo adiante.\n"
	.string "Um passo a mais e eu te paro.$"

SeafloorCavern_Room4_Text_Grunt4Defeat:
	.string "Nao consegui proteger a passagem.$"

SeafloorCavern_Room4_Text_Grunt4PostBattle:
	.string "Os sensores perderam a leitura.\p"
	.string "Se algo despertar la embaixo,\n"
	.string "ninguem sabe o que acontece.$"

