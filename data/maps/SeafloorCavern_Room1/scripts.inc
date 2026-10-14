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
	.string "You should not have reached the\n"
	.string "M'BOI chambers.\p"
	.string "While OTACILIO is below, no one\n"
	.string "passes.$"

SeafloorCavern_Room1_Text_Grunt1Defeat:
	.string "You got past me...$"

SeafloorCavern_Room1_Text_Grunt1PostBattle:
	.string "OTACILIO believes some memories\n"
	.string "only keep hurting.\p"
	.string "I will not pretend I understand\n"
	.string "all of it.$"

SeafloorCavern_Room1_Text_Grunt2Intro:
	.string "These caverns react to things\n"
	.string "our sensors cannot read.\p"
	.string "Do not come any closer.$"

SeafloorCavern_Room1_Text_Grunt2Defeat:
	.string "So even that did not stop you...$"

SeafloorCavern_Room1_Text_Grunt2PostBattle:
	.string "The deeper we go, the less the\n"
	.string "ARCHIVE obeys.\p"
	.string "Maybe it was never really a\n"
	.string "tool.$"

