VictoryRoad_B1F_MapScripts::
	.byte 0

VictoryRoad_B1F_EventScript_Samuel::
	trainerbattle_single TRAINER_SAMUEL, VictoryRoad_B1F_Text_SamuelIntro, VictoryRoad_B1F_Text_SamuelDefeat
	msgbox VictoryRoad_B1F_Text_SamuelPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_EventScript_Shannon::
	trainerbattle_single TRAINER_SHANNON, VictoryRoad_B1F_Text_ShannonIntro, VictoryRoad_B1F_Text_ShannonDefeat
	msgbox VictoryRoad_B1F_Text_ShannonPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_EventScript_Michelle::
	trainerbattle_single TRAINER_MICHELLE, VictoryRoad_B1F_Text_MichelleIntro, VictoryRoad_B1F_Text_MichelleDefeat
	msgbox VictoryRoad_B1F_Text_MichellePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_EventScript_Mitchell::
	trainerbattle_single TRAINER_MITCHELL, VictoryRoad_B1F_Text_MitchellIntro, VictoryRoad_B1F_Text_MitchellDefeat
	msgbox VictoryRoad_B1F_Text_MitchellPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_EventScript_Halle::
	trainerbattle_single TRAINER_HALLE, VictoryRoad_B1F_Text_HalleIntro, VictoryRoad_B1F_Text_HalleDefeat
	msgbox VictoryRoad_B1F_Text_HallePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_Text_SamuelIntro:
	.string "The closer I get to the LEAGUE, the\n"
	.string "more nervous I feel...$"

VictoryRoad_B1F_Text_SamuelDefeat:
	.string "I couldn't do a thing...$"

VictoryRoad_B1F_Text_SamuelPostBattle:
	.string "The LEAGUE feels far away again... How\n"
	.string "disappointing...$"

VictoryRoad_B1F_Text_ShannonIntro:
	.string "At the LEAGUE, you need your POKéMON\n"
	.string "to trust you.$"

VictoryRoad_B1F_Text_ShannonDefeat:
	.string "The trust between you two is strong.$"

VictoryRoad_B1F_Text_ShannonPostBattle:
	.string "The longer they spend together, the\n"
	.string "more trust grows between a TRAINER and\l"
	.string "a POKéMON.$"

VictoryRoad_B1F_Text_MichelleIntro:
	.string "This isn't the finish. It's one more step\n"
	.string "toward the LEAGUE.$"

VictoryRoad_B1F_Text_MichelleDefeat:
	.string "That's the way!$"

VictoryRoad_B1F_Text_MichellePostBattle:
	.string "You'll be fine! Your POKéMON are ready.$"

VictoryRoad_B1F_Text_MitchellIntro:
	.string "My POKéMON are a force from another\n"
	.string "world!$"

VictoryRoad_B1F_Text_MitchellDefeat:
	.string "I've never faced anyone like that.$"

VictoryRoad_B1F_Text_MitchellPostBattle:
	.string "Even outside battle, you can feel the\n"
	.string "strength between you and your POKéMON.$"

VictoryRoad_B1F_Text_HalleIntro:
	.string "Hey, loosen up a little! Let's battle\n"
	.string "without all that tension.$"

VictoryRoad_B1F_Text_HalleDefeat:
	.string "Wow! How wonderful!$"

VictoryRoad_B1F_Text_HallePostBattle:
	.string "Yes, this is ESTRADA DO JURAMENTO.\p"
	.string "But it isn't so different from the road\n"
	.string "that brought you here. Enjoy the rest\l"
	.string "of it!$"

