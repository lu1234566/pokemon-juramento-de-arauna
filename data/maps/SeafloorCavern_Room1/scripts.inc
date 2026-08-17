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
	.string "Otacilio volta ao lugar onde\nperdeu a familia. Luzia chega\p"
	.string "para libertar tudo que foi\narmazenado. Os dois extremos\p"
	.string "colidem.$"

SeafloorCavern_Room1_Text_Grunt1Defeat:
	.string "Otacilio volta ao lugar onde\nperdeu a familia. Luzia chega\p"
	.string "para libertar tudo que foi\narmazenado. Os dois extremos\p"
	.string "colidem.$"

SeafloorCavern_Room1_Text_Grunt1PostBattle:
	.string "Otacilio volta ao lugar onde\nperdeu a familia. Luzia chega\p"
	.string "para libertar tudo que foi\narmazenado. Os dois extremos\p"
	.string "colidem.$"

SeafloorCavern_Room1_Text_Grunt2Intro:
	.string "Otacilio volta ao lugar onde\nperdeu a familia. Luzia chega\p"
	.string "para libertar tudo que foi\narmazenado. Os dois extremos\p"
	.string "colidem.$"

SeafloorCavern_Room1_Text_Grunt2Defeat:
	.string "Otacilio volta ao lugar onde\nperdeu a familia. Luzia chega\p"
	.string "para libertar tudo que foi\narmazenado. Os dois extremos\p"
	.string "colidem.$"

SeafloorCavern_Room1_Text_Grunt2PostBattle:
	.string "Otacilio volta ao lugar onde\nperdeu a familia. Luzia chega\p"
	.string "para libertar tudo que foi\narmazenado. Os dois extremos\p"
	.string "colidem.$"

