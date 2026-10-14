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
	.string "MARTA: OTACILIO is near the\n"
	.string "core.\p"
	.string "I will not let you interrupt\n"
	.string "everything now.$"

SeafloorCavern_Room3_Text_ShellyDefeat:
	.string "MARTA: Heh... You are worse than\n"
	.string "the reports said.$"

SeafloorCavern_Room3_Text_ShellyPostBattle:
	.string "MARTA: Do not confuse obedience\n"
	.string "with certainty.\p"
	.string "I follow OTACILIO because I saw\n"
	.string "what memories can do.$"

SeafloorCavern_Room3_Text_Grunt5Intro:
	.string "MARTA ordered us to hold this\n"
	.string "route.\p"
	.string "If you want through, try me.$"

SeafloorCavern_Room3_Text_Grunt5Defeat:
	.string "I should have stayed with the\n"
	.string "reports...$"

SeafloorCavern_Room3_Text_Grunt5PostBattle:
	.string "The ARCHIVE has been unstable\n"
	.string "since we descended into M'BOI.\p"
	.string "OTACILIO keeps going anyway.$"

