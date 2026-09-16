VictoryRoad_B2F_MapScripts::
	.byte 0

VictoryRoad_B2F_EventScript_Vito::
	trainerbattle_single TRAINER_VITO, VictoryRoad_B2F_Text_VitoIntro, VictoryRoad_B2F_Text_VitoDefeat
	msgbox VictoryRoad_B2F_Text_VitoPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Owen::
	trainerbattle_single TRAINER_OWEN, VictoryRoad_B2F_Text_OwenIntro, VictoryRoad_B2F_Text_OwenDefeat
	msgbox VictoryRoad_B2F_Text_OwenPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Caroline::
	trainerbattle_single TRAINER_CAROLINE, VictoryRoad_B2F_Text_CarolineIntro, VictoryRoad_B2F_Text_CarolineDefeat
	msgbox VictoryRoad_B2F_Text_CarolinePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Julie::
	trainerbattle_single TRAINER_JULIE, VictoryRoad_B2F_Text_JulieIntro, VictoryRoad_B2F_Text_JulieDefeat
	msgbox VictoryRoad_B2F_Text_JuliePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Felix::
	trainerbattle_single TRAINER_FELIX, VictoryRoad_B2F_Text_FelixIntro, VictoryRoad_B2F_Text_FelixDefeat
	msgbox VictoryRoad_B2F_Text_FelixPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Dianne::
	trainerbattle_single TRAINER_DIANNE, VictoryRoad_B2F_Text_DianneIntro, VictoryRoad_B2F_Text_DianneDefeat
	msgbox VictoryRoad_B2F_Text_DiannePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_Text_VitoIntro:
	.string "My whole family trained with me.\n"
	.string "I want to make that time count.$"

VictoryRoad_B2F_Text_VitoDefeat:
	.string "You beat me. That does not erase\n"
	.string "what my family taught me.$"

VictoryRoad_B2F_Text_VitoPostBattle:
	.string "I thought being the best at home\n"
	.string "meant I could not lose here.\p"
	.string "I was wrong. I can go home,\n"
	.string "learn, and come back.$"

VictoryRoad_B2F_Text_OwenIntro:
	.string "I heard about a tough young\n"
	.string "TRAINER from VILA AMANHECER.\p"
	.string "So that was you?$"

VictoryRoad_B2F_Text_OwenDefeat:
	.string "The stories did not exaggerate.$"

VictoryRoad_B2F_Text_OwenPostBattle:
	.string "So the traveler from\n"
	.string "VILA AMANHECER reached OATH\n"
	.string "ROAD.\p"
	.string "People will talk about that.$"

VictoryRoad_B2F_Text_CarolineIntro:
	.string "You must be tired by now. Do not\n"
	.string "hide it from your team.$"

VictoryRoad_B2F_Text_CarolineDefeat:
	.string "You managed your strength well.$"

VictoryRoad_B2F_Text_CarolinePostBattle:
	.string "OATH ROAD and the LEAGUE are\n"
	.string "long.\p"
	.string "Rest is part of finishing.$"

VictoryRoad_B2F_Text_JulieIntro:
	.string "Eight BADGES can open the door.\p"
	.string "They cannot fight the next\n"
	.string "battle for you.$"

VictoryRoad_B2F_Text_JulieDefeat:
	.string "You were better in this battle.$"

VictoryRoad_B2F_Text_JuliePostBattle:
	.string "Look at your BADGES and remember\n"
	.string "the people behind each one.\p"
	.string "A record is not the whole\n"
	.string "journey.$"

VictoryRoad_B2F_Text_FelixIntro:
	.string "I came far, but the pressure is\n"
	.string "doing terrible things to my\n"
	.string "stomach.$"

VictoryRoad_B2F_Text_FelixDefeat:
	.string "Ow... That did not help.$"

VictoryRoad_B2F_Text_FelixPostBattle:
	.string "I get tense just thinking about\n"
	.string "how close the LEAGUE is.\p"
	.string "Pretending I am calm makes it\n"
	.string "worse.$"

VictoryRoad_B2F_Text_DianneIntro:
	.string "Strong TRAINERS reach this cave.\p"
	.string "What has the road shown you?$"

VictoryRoad_B2F_Text_DianneDefeat:
	.string "You did not lose your balance.$"

VictoryRoad_B2F_Text_DiannePostBattle:
	.string "Courage is not looking fearless.\p"
	.string "Keep going.$"

