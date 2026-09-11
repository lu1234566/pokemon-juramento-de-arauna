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
	.string "MARTA: OTACILIO is near the core. I'm\n"
	.string "not letting you cut this short now.$"

SeafloorCavern_Room3_Text_ShellyDefeat:
	.string "MARTA: Heh... you're worse than the\n"
	.string "reports said.$"

SeafloorCavern_Room3_Text_ShellyPostBattle:
	.string "MARTA: Don't mistake obedience for\n"
	.string "certainty.\p"
	.string "I follow OTACILIO because I have seen\n"
	.string "what memories can do.$"

SeafloorCavern_Room3_Text_Grunt5Intro:
	.string "MARTA gave orders to hold this route.\n"
	.string "If you want through, try your luck.$"

SeafloorCavern_Room3_Text_Grunt5Defeat:
	.string "I should have stuck to the reports...$"

SeafloorCavern_Room3_Text_Grunt5PostBattle:
	.string "The ARCHIVE has been unstable ever\n"
	.string "since we went down to M'BOI.\p"
	.string "OTACILIO is carrying on regardless.$"

