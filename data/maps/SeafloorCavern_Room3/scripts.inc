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
	.string "MARTA: OTACILIO esta perto do\n"
	.string "nucleo. Nao vou deixar voce\n"
	.string "interromper tudo agora.$"

SeafloorCavern_Room3_Text_ShellyDefeat:
	.string "MARTA: Heh... voce e pior do\n"
	.string "que os relatorios diziam.$"

SeafloorCavern_Room3_Text_ShellyPostBattle:
	.string "MARTA: Nao confunda obediencia\n"
	.string "com certeza.\p"
	.string "Eu sigo OTACILIO porque vi o\n"
	.string "que lembrancas podem fazer.$"

SeafloorCavern_Room3_Text_Grunt5Intro:
	.string "MARTA mandou proteger esta rota.\n"
	.string "Se quer passar, tente a sorte.$"

SeafloorCavern_Room3_Text_Grunt5Defeat:
	.string "Eu devia ter ficado nos\n"
	.string "relatorios...$"

SeafloorCavern_Room3_Text_Grunt5PostBattle:
	.string "O ARQUIVO ficou instavel desde\n"
	.string "que descemos para M'BOI.\p"
	.string "Mesmo assim, OTACILIO continua.$"

