VictoryRoad_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, VictoryRoad_1F_OnTransition
	.byte 0

VictoryRoad_1F_OnTransition:
	call_if_eq VAR_VICTORY_ROAD_1F_STATE, 1, VictoryRoad_1F_EventScript_SetEntranceWallyPos1
	call_if_eq VAR_VICTORY_ROAD_1F_STATE, 2, VictoryRoad_1F_EventScript_SetEntranceWallyPos2
	end

VictoryRoad_1F_EventScript_SetEntranceWallyPos1::
	setobjectxyperm LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, 2, 24
	setobjectmovementtype LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, MOVEMENT_TYPE_FACE_DOWN
	return

VictoryRoad_1F_EventScript_SetEntranceWallyPos2::
	setobjectxyperm LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, 3, 24
	setobjectmovementtype LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, MOVEMENT_TYPE_FACE_DOWN
	return

VictoryRoad_1F_EventScript_WallyBattleTrigger1::
	lockall
	setvar VAR_0x8008, 1
	addobject LOCALID_VICTORY_ROAD_ENTRANCE_WALLY
	applymovement LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, VictoryRoad_1F_Movement_WallyApproachPlayer1
	waitmovement 0
	goto VictoryRoad_1F_EventScript_WallyEntranceBattle
	end

VictoryRoad_1F_EventScript_WallyBattleTrigger2::
	lockall
	setvar VAR_0x8008, 2
	addobject LOCALID_VICTORY_ROAD_ENTRANCE_WALLY
	applymovement LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, VictoryRoad_1F_Movement_WallyApproachPlayer2
	waitmovement 0
	goto VictoryRoad_1F_EventScript_WallyEntranceBattle
	end

VictoryRoad_1F_EventScript_WallyEntranceBattle::
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox VictoryRoad_1F_Text_WallyNotGoingToLoseAnymore, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_WALLY_VR_1, VictoryRoad_1F_Text_WallyEntranceDefeat
	msgbox VictoryRoad_1F_Text_WallyPostEntranceBattle, MSGBOX_DEFAULT
	clearflag FLAG_HIDE_VICTORY_ROAD_ENTRANCE_WALLY
	copyobjectxytoperm LOCALID_VICTORY_ROAD_ENTRANCE_WALLY
	setflag FLAG_DEFEATED_WALLY_VICTORY_ROAD
	copyvar VAR_VICTORY_ROAD_1F_STATE, VAR_0x8008
	releaseall
	end

VictoryRoad_1F_Movement_WallyApproachPlayer1:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_up
	step_end

VictoryRoad_1F_Movement_WallyApproachPlayer2:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_up
	step_end

@ This Wally appears near the entrance once his battle is triggered and remains there until the Hall of Fame is entered
VictoryRoad_1F_EventScript_EntranceWally::
	msgbox VictoryRoad_1F_Text_WallyPostEntranceBattle, MSGBOX_NPC
	end

@ This Wally appears and remains at the exit after the Hall of Fame is entered
VictoryRoad_1F_EventScript_ExitWally::
	trainerbattle_single TRAINER_WALLY_VR_2, VictoryRoad_1F_Text_WallyIntro, VictoryRoad_1F_Text_WallyDefeat
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, VictoryRoad_1F_EventScript_RematchWally
	msgbox VictoryRoad_1F_Text_WallyPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_RematchWally::
	trainerbattle_rematch TRAINER_WALLY_VR_2, VictoryRoad_1F_Text_WallyIntro, VictoryRoad_1F_Text_WallyDefeat
	msgbox VictoryRoad_1F_Text_WallyPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Edgar::
	trainerbattle_single TRAINER_EDGAR, VictoryRoad_1F_Text_EdgarIntro, VictoryRoad_1F_Text_EdgarDefeat
	msgbox VictoryRoad_1F_Text_EdgarPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Albert::
	trainerbattle_single TRAINER_ALBERT, VictoryRoad_1F_Text_AlbertIntro, VictoryRoad_1F_Text_AlbertDefeat
	msgbox VictoryRoad_1F_Text_AlbertPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Hope::
	trainerbattle_single TRAINER_HOPE, VictoryRoad_1F_Text_HopeIntro, VictoryRoad_1F_Text_HopeDefeat
	msgbox VictoryRoad_1F_Text_HopePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Quincy::
	trainerbattle_single TRAINER_QUINCY, VictoryRoad_1F_Text_QuincyIntro, VictoryRoad_1F_Text_QuincyDefeat
	msgbox VictoryRoad_1F_Text_QuincyPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Katelynn::
	trainerbattle_single TRAINER_KATELYNN, VictoryRoad_1F_Text_KatelynnIntro, VictoryRoad_1F_Text_KatelynnDefeat
	msgbox VictoryRoad_1F_Text_KatelynnPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_Text_WallyNotGoingToLoseAnymore:
	.string "VAL: I reached this place at my\n"
	.string "own pace, {PLAYER}.\p"
	.string "I am done trying to become\n"
	.string "someone else.\p"
	.string "I want to see how far I can go\n"
	.string "as myself.$"

VictoryRoad_1F_Text_WallyEntranceDefeat:
	.string "VAL: I lost... but I did not\n"
	.string "fold.\p"
	.string "That used to break me. Now it\n"
	.string "shows me where I can still grow.$"

VictoryRoad_1F_Text_WallyPostEntranceBattle:
	.string "VAL: Keep going,\n"
	.string "{PLAYER}.\p"
	.string "I will keep moving too.\p"
	.string "Next time we meet, I want to be\n"
	.string "stronger on my own terms.$"

VictoryRoad_1F_Text_WallyIntro:
	.string "VAL: CHAMPION or not, I still\n"
	.string "want to measure my pace with\n"
	.string "yours.\p"
	.string "Come on, {PLAYER}.\n"
	.string "No excuses.$"

VictoryRoad_1F_Text_WallyDefeat:
	.string "VAL: Ha! I still have some road\n"
	.string "left before I catch you.$"

VictoryRoad_1F_Text_WallyPostBattle:
	.string "VAL: Every loss shows me\n"
	.string "something I could not see\l"
	.string "before.\p"
	.string "Next time, I will be closer.$"

VictoryRoad_1F_Text_EdgarIntro:
	.string "I have made it this far before.\n"
	.string "The end still feels distant.$"

VictoryRoad_1F_Text_EdgarDefeat:
	.string "My run ends here again...$"

VictoryRoad_1F_Text_EdgarPostBattle:
	.string "You have come a long way.\p"
	.string "Do not stop because I did. Go\n"
	.string "face the LEAGUE.$"

VictoryRoad_1F_Text_AlbertIntro:
	.string "I did not come here planning to\n"
	.string "lose. Let us see what happens.$"

VictoryRoad_1F_Text_AlbertDefeat:
	.string "So I lost. I have work to do.$"

VictoryRoad_1F_Text_AlbertPostBattle:
	.string "This road showed me what my plan\n"
	.string "did not account for.\p"
	.string "I will learn before I return.$"

VictoryRoad_1F_Text_HopeIntro:
	.string "This road feels endless. Now I\n"
	.string "understand its name.$"

VictoryRoad_1F_Text_HopeDefeat:
	.string "You kept your footing to the\n"
	.string "end.$"

VictoryRoad_1F_Text_HopePostBattle:
	.string "You can reach the LEAGUE.\p"
	.string "What matters next is what you do\n"
	.string "with the chance.$"

VictoryRoad_1F_Text_QuincyIntro:
	.string "What makes this an oath road?\n"
	.string "Beat me and I will answer.$"

VictoryRoad_1F_Text_QuincyDefeat:
	.string "All right. Fair is fair.$"

VictoryRoad_1F_Text_QuincyPostBattle:
	.string "OATH ROAD is not a promise that\n"
	.string "you will win.\p"
	.string "It is a promise to answer for\n"
	.string "the choices that brought you\n"
	.string "here.$"

VictoryRoad_1F_Text_KatelynnIntro:
	.string "If you reached this point, you\n"
	.string "do not need another speech. Go!$"

VictoryRoad_1F_Text_KatelynnDefeat:
	.string "Hmph. You got through.$"

VictoryRoad_1F_Text_KatelynnPostBattle:
	.string "You may pass.\p"
	.string "The LEAGUE will ask more of you.$"
