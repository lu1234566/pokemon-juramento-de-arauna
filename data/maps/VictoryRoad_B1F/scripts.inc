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
	.string "The closer I get to the LEAGUE,\n"
	.string "the more nervous I become...$"

VictoryRoad_B1F_Text_SamuelDefeat:
	.string "I froze when it mattered.$"

VictoryRoad_B1F_Text_SamuelPostBattle:
	.string "I am disappointed, but the road\n"
	.string "does not owe me a victory.\p"
	.string "I can try again.$"

VictoryRoad_B1F_Text_ShannonIntro:
	.string "A battle this late in the road\n"
	.string "depends on trust. Show me yours.$"

VictoryRoad_B1F_Text_ShannonDefeat:
	.string "You and your POKéMON stayed\n"
	.string "steady.$"

VictoryRoad_B1F_Text_ShannonPostBattle:
	.string "Trust grows through time\n"
	.string "together.\p"
	.string "It is not the same as control.$"

VictoryRoad_B1F_Text_MichelleIntro:
	.string "This is not the finish. It is\n"
	.string "one more step to the LEAGUE.$"

VictoryRoad_B1F_Text_MichelleDefeat:
	.string "That was a clean step forward.$"

VictoryRoad_B1F_Text_MichellePostBattle:
	.string "You look ready. So do your\n"
	.string "POKéMON.$"

VictoryRoad_B1F_Text_MitchellIntro:
	.string "My POKéMON have carried me far.\n"
	.string "Let us see how far together.$"

VictoryRoad_B1F_Text_MitchellDefeat:
	.string "I have not faced a team like\n"
	.string "yours.$"

VictoryRoad_B1F_Text_MitchellPostBattle:
	.string "Even outside battle, I can see\n"
	.string "how well your team reads you.$"

VictoryRoad_B1F_Text_HalleIntro:
	.string "Hey, loosen your shoulders. We\n"
	.string "can battle without pretending\n"
	.string "the pressure is not here.$"

VictoryRoad_B1F_Text_HalleDefeat:
	.string "That was good! Really good!$"

VictoryRoad_B1F_Text_HallePostBattle:
	.string "Yes, this is OATH ROAD.\p"
	.string "It is still only a road. Walk\n"
	.string "the part in front of you.$"

