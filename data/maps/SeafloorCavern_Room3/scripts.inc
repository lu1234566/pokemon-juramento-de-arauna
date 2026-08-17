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
	.string "Otacilio volta ao lugar onde\nperdeu a familia. Luzia chega\p"
	.string "para libertar tudo que foi\narmazenado. Os dois extremos\p"
	.string "colidem.$"

SeafloorCavern_Room3_Text_ShellyDefeat:
	.string "Otacilio volta ao lugar onde\nperdeu a familia. Luzia chega\p"
	.string "para libertar tudo que foi\narmazenado. Os dois extremos\p"
	.string "colidem.$"

SeafloorCavern_Room3_Text_ShellyPostBattle:
	.string "HORIZONTE: O Arquivo preserva o\nque o tempo destruiria. Um dia\p"
	.string "voces vao agradecer por nao\nprecisarem mais sofrer para\p"
	.string "lembrar.$"

SeafloorCavern_Room3_Text_Grunt5Intro:
	.string "Otacilio volta ao lugar onde\nperdeu a familia. Luzia chega\p"
	.string "para libertar tudo que foi\narmazenado. Os dois extremos\p"
	.string "colidem.$"

SeafloorCavern_Room3_Text_Grunt5Defeat:
	.string "Otacilio volta ao lugar onde\nperdeu a familia. Luzia chega\p"
	.string "para libertar tudo que foi\narmazenado. Os dois extremos\p"
	.string "colidem.$"

SeafloorCavern_Room3_Text_Grunt5PostBattle:
	.string "CIRO: O futuro nao espera por\nquem vive olhando para tras.\p"
	.string "Pelo menos era nisso que eu\nacreditava.$"

