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
	.string "You should never have reached the\n"
	.string "M'BOI chambers.\p"
	.string "While OTACILIO is down there, nobody\n"
	.string "gets through.$"

SeafloorCavern_Room1_Text_Grunt1Defeat:
	.string "Blast... you got past me.$"

SeafloorCavern_Room1_Text_Grunt1PostBattle:
	.string "OTACILIO believes some memories only\n"
	.string "go on wounding.\p"
	.string "I won't pretend I understand all of it.$"

SeafloorCavern_Room1_Text_Grunt2Intro:
	.string "These caves react to things our\n"
	.string "sensors can't read.\p"
	.string "Don't come any closer.$"

SeafloorCavern_Room1_Text_Grunt2Defeat:
	.string "So not even that stopped you...$"

SeafloorCavern_Room1_Text_Grunt2PostBattle:
	.string "The deeper we go, the less the ARCHIVE\n"
	.string "obeys.\p"
	.string "Perhaps it was never really a tool at\n"
	.string "all.$"

