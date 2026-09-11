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
	.string "Below this point the ARCHIVE stops\n"
	.string "answering properly.\p"
	.string "This is no place for the curious.$"

SeafloorCavern_Room4_Text_Grunt3Defeat:
	.string "Are you really going on?$"

SeafloorCavern_Room4_Text_Grunt3PostBattle:
	.string "The recordings here run evacuation,\n"
	.string "rescue and silence together.\p"
	.string "Maybe that is why OTACILIO came in\n"
	.string "person.$"

SeafloorCavern_Room4_Text_Grunt4Intro:
	.string "The core is just ahead. One more step\n"
	.string "and I stop you.$"

SeafloorCavern_Room4_Text_Grunt4Defeat:
	.string "I failed to hold the way.$"

SeafloorCavern_Room4_Text_Grunt4PostBattle:
	.string "The sensors have lost the reading.\p"
	.string "If something wakes down there, nobody\n"
	.string "knows what happens.$"

