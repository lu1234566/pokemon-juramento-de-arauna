CaveOfOrigin_B1F_MapScripts::
	.byte 0

CaveOfOrigin_B1F_EventScript_Wallace::
	lock
	faceplayer
	msgbox CaveOfOrigin_B1F_Text_WallaceStory, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CAVE_OF_ORIGIN_WALLACE, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	delay 60
	playse SE_PIN
	applymovement LOCALID_CAVE_OF_ORIGIN_WALLACE, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_CAVE_OF_ORIGIN_WALLACE, Common_Movement_Delay48
	waitmovement 0
	delay 30
	applymovement LOCALID_CAVE_OF_ORIGIN_WALLACE, Common_Movement_FacePlayer
	waitmovement 0
	message CaveOfOrigin_B1F_Text_WhereIsRayquaza
	waitmessage
	goto CaveOfOrigin_B1F_EventScript_WheresRayquaza

CaveOfOrigin_B1F_EventScript_WheresRayquaza::
	multichoice 0, 0, MULTI_WHERES_RAYQUAZA, FALSE
	switch VAR_RESULT
	case 0, CaveOfOrigin_B1F_EventScript_AtCaveOfOrigin
	case 1, CaveOfOrigin_B1F_EventScript_AtMtPyre
	case 2, CaveOfOrigin_B1F_EventScript_AtSkyPillar
	case 3, CaveOfOrigin_B1F_EventScript_DontRemember
	goto CaveOfOrigin_B1F_EventScript_DontRemember
	end

CaveOfOrigin_B1F_EventScript_AtCaveOfOrigin::
	message CaveOfOrigin_B1F_Text_ButWereInCaveOfOrigin
	waitmessage
	goto CaveOfOrigin_B1F_EventScript_WheresRayquaza

CaveOfOrigin_B1F_EventScript_AtMtPyre::
	message CaveOfOrigin_B1F_Text_OldLadyDidntMentionThat
	waitmessage
	goto CaveOfOrigin_B1F_EventScript_WheresRayquaza

CaveOfOrigin_B1F_EventScript_DontRemember::
	message CaveOfOrigin_B1F_Text_CantYouRememberSomehow
	waitmessage
	goto CaveOfOrigin_B1F_EventScript_WheresRayquaza

CaveOfOrigin_B1F_EventScript_AtSkyPillar::
	msgbox CaveOfOrigin_B1F_Text_WellHeadToSkyPillar, MSGBOX_DEFAULT
	closemessage
	playse SE_EXIT
	fadescreenspeed FADE_TO_BLACK, 4
	setflag FLAG_WALLACE_GOES_TO_SKY_PILLAR
	setvar VAR_SOOTOPOLIS_CITY_STATE, 3
	removeobject LOCALID_CAVE_OF_ORIGIN_WALLACE
	clearflag FLAG_HIDE_SKY_PILLAR_WALLACE
	fadescreen FADE_FROM_BLACK
	release
	end

CaveOfOrigin_B1F_Text_WallaceStory:
	.string "AMALIA: {PLAYER}, the current\n"
	.string "beneath M'BOI is not alone.\p"
	.string "Old records describe a third\n"
	.string "force between two currents.\p"
	.string "MR. BENTO calls it the GUARDIAN\n"
	.string "OF THE TOWER.\p"
	.string "I checked city records, the\n"
	.string "MEMORIAL, and old route notes.\p"
	.string "One place keeps returning.\n"
	.string "Did your road find it too?$"

CaveOfOrigin_B1F_Text_WhereIsRayquaza:
	.string "AMALIA: Where would you look for\n"
	.string "the GUARDIAN now?\p"
	.string "Which place does your road show?$"

CaveOfOrigin_B1F_Text_ButWereInCaveOfOrigin:
	.string "AMALIA: M'BOI CORE is already\n"
	.string "open beneath us.\p"
	.string "We need somewhere above it,\n"
	.string "not its center.$"

CaveOfOrigin_B1F_Text_OldLadyDidntMentionThat:
	.string "AMALIA: The MEMORIAL preserves\n"
	.string "names and records.\p"
	.string "But the old route points higher.$"

CaveOfOrigin_B1F_Text_CantYouRememberSomehow:
	.string "AMALIA: Use what you have seen.\p"
	.string "Think of the place watching the\n"
	.string "region from above.$"

CaveOfOrigin_B1F_Text_WellHeadToSkyPillar:
	.string "AMALIA: OATH TOWER. Yes.\p"
	.string "The old routes converge there.\p"
	.string "{PLAYER}, we cannot leave the two\n"
	.string "currents fighting below us.\p"
	.string "I will head there now.$"

