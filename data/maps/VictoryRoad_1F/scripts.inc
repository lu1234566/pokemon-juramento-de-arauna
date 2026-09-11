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
	.string "VAL: I got here at my own pace, {PLAYER}.\n"
	.string "This time I'm not going to try to be\l"
	.string "somebody else.\p"
	.string "I want to find out how far I can go as\n"
	.string "myself.$"

VictoryRoad_1F_Text_WallyEntranceDefeat:
	.string "VAL: I lost... but I didn't back away.\p"
	.string "That would have broken me once. Now it\n"
	.string "only shows me how much further I can\l"
	.string "grow.$"

VictoryRoad_1F_Text_WallyPostEntranceBattle:
	.string "VAL: Go on ahead, {PLAYER}.\p"
	.string "I'm going to keep at it too. When we\n"
	.string "meet again, I want to be stronger still.$"

VictoryRoad_1F_Text_WallyIntro:
	.string "VAL: CHAMPION or not, I still want to\n"
	.string "measure my stride against yours.\p"
	.string "Come on, {PLAYER}. No excuses.$"

VictoryRoad_1F_Text_WallyDefeat:
	.string "VAL: Ha! I've still got road to cover\n"
	.string "before I catch you.$"

VictoryRoad_1F_Text_WallyPostBattle:
	.string "VAL: Every defeat shows me something I\n"
	.string "wasn't seeing.\p"
	.string "Next time, I'll get closer.$"

VictoryRoad_1F_Text_EdgarIntro:
	.string "I've made it this far before, but the\n"
	.string "end always looks a long way off.$"

VictoryRoad_1F_Text_EdgarDefeat:
	.string "My dream stops here again...$"

VictoryRoad_1F_Text_EdgarPostBattle:
	.string "You've come a long way. Don't stop now!\p"
	.string "Go and take the LEAGUE!$"

VictoryRoad_1F_Text_AlbertIntro:
	.string "I didn't come this far to lose. That\n"
	.string "option doesn't exist!$"

VictoryRoad_1F_Text_AlbertDefeat:
	.string "Impossible... I lost?$"

VictoryRoad_1F_Text_AlbertPostBattle:
	.string "I lost here...\p"
	.string "I'm not ready to take the LEAGUE yet.$"

VictoryRoad_1F_Text_HopeIntro:
	.string "This road seems to have no end. Now I\n"
	.string "understand its name.$"

VictoryRoad_1F_Text_HopeDefeat:
	.string "The way you battle is incredible...$"

VictoryRoad_1F_Text_HopePostBattle:
	.string "You have the strength to reach the top\n"
	.string "of the LEAGUE.$"

VictoryRoad_1F_Text_QuincyIntro:
	.string "What is this road? I'll tell you if you\n"
	.string "win!$"

VictoryRoad_1F_Text_QuincyDefeat:
	.string "Right! Very good!$"

VictoryRoad_1F_Text_QuincyPostBattle:
	.string "This path is the last test for anyone\n"
	.string "reaching for the top of the LEAGUE.\p"
	.string "That is why it is called\n"
	.string "ESTRADA DO JURAMENTO.$"

VictoryRoad_1F_Text_KatelynnIntro:
	.string "If you got this far, I don't need to\n"
	.string "explain a thing. Let's go!$"

VictoryRoad_1F_Text_KatelynnDefeat:
	.string "How embarrassing...$"

VictoryRoad_1F_Text_KatelynnPostBattle:
	.string "Hmph. Go on through. See if I care.$"
