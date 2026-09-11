PetalburgCity_WallysHouse_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, PetalburgCity_WallysHouse_OnFrame
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, PetalburgCity_WallysHouse_OnWarp
	.byte 0

PetalburgCity_WallysHouse_OnWarp:
	map_script_2 VAR_PETALBURG_CITY_STATE, 4, PetalburgCity_WallysHouse_EventScript_PlayerWallysDadFaceEachOther
	.2byte 0

PetalburgCity_WallysHouse_EventScript_PlayerWallysDadFaceEachOther::
	turnobject LOCALID_PLAYER, DIR_EAST
	turnobject LOCALID_WALLYS_HOUSE_WALLYS_DAD, DIR_WEST
	end

PetalburgCity_WallysHouse_OnFrame:
	map_script_2 VAR_PETALBURG_CITY_STATE, 4, PetalburgCity_WallysHouse_EventScript_GiveHMSurf
	.2byte 0

PetalburgCity_WallysHouse_EventScript_GiveHMSurf::
	lockall
	msgbox PetalburgCity_WallysHouse_Text_PleaseExcuseUs, MSGBOX_DEFAULT
	giveitem ITEM_HM_SURF
	setflag FLAG_RECEIVED_HM_SURF
	msgbox PetalburgCity_WallysHouse_Text_SurfGoAllSortsOfPlaces, MSGBOX_DEFAULT
	setvar VAR_PETALBURG_CITY_STATE, 5
	releaseall
	end

PetalburgCity_WallysHouse_EventScript_WallysDad::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_WALLY_VICTORY_ROAD, PetalburgCity_WallysHouse_EventScript_DefeatedWallyInVictoryRoad
	goto_if_set FLAG_RECEIVED_HM_SURF, PetalburgCity_WallysHouse_EventScript_ReceievedHMSurf
	goto_if_set FLAG_THANKED_FOR_PLAYING_WITH_WALLY, PetalburgCity_WallysHouse_EventScript_PlayedWithWally
	msgbox PetalburgCity_WallysHouse_Text_ThanksForPlayingWithWally, MSGBOX_DEFAULT
	setflag FLAG_THANKED_FOR_PLAYING_WITH_WALLY
	release
	end

PetalburgCity_WallysHouse_EventScript_ReceievedHMSurf::
	msgbox PetalburgCity_WallysHouse_Text_WallyIsComingHomeSoon, MSGBOX_DEFAULT
	release
	end

PetalburgCity_WallysHouse_EventScript_DefeatedWallyInVictoryRoad::
	msgbox PetalburgCity_WallysHouse_Text_YouMetWallyInEverGrandeCity, MSGBOX_DEFAULT
	release
	end

PetalburgCity_WallysHouse_EventScript_PlayedWithWally::
	msgbox PetalburgCity_WallysHouse_Text_WonderHowWallyIsDoing, MSGBOX_DEFAULT
	release
	end

PetalburgCity_WallysHouse_EventScript_WallysMom::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_HM_SURF, PetalburgCity_WallysHouse_EventScript_ReceivedHMSurf
	msgbox PetalburgCity_WallysHouse_Text_WallyWasReallyHappy, MSGBOX_DEFAULT
	release
	end

PetalburgCity_WallysHouse_EventScript_ReceivedHMSurf::
	msgbox PetalburgCity_WallysHouse_Text_WallyLeftWithoutTelling, MSGBOX_DEFAULT
	release
	end

PetalburgCity_WallysHouse_Text_ThanksForPlayingWithWally:
	.string "Thank you for helping VAL.\p"
	.string "He talks about you as someone who\n"
	.string "treated him with patience.\p"
	.string "That did him good.$"

PetalburgCity_WallysHouse_Text_WonderHowWallyIsDoing:
	.string "VAL hasn't sent word for a few days.\p"
	.string "Once he sets his mind on a trip he\n"
	.string "forgets everything else.\p"
	.string "I hope he's all right.$"

PetalburgCity_WallysHouse_Text_PleaseExcuseUs:
	.string "{PLAYER}! I'm sorry to bring you all the\n"
	.string "way here like this.\p"
	.string "VAL has come a long way since he went\n"
	.string "to VALE DO SILENCIO.\p"
	.string "You helped him when he was still afraid\n"
	.string "to travel alone.\p"
	.string "As his father, I don't forget that.\p"
	.string "I want you to take this.$"

PetalburgCity_WallysHouse_Text_SurfGoAllSortsOfPlaces:
	.string "With SURF, your POKéMON can cross\n"
	.string "stretches of water and open new roads.$"

PetalburgCity_WallysHouse_Text_WallyIsComingHomeSoon:
	.string "VAL said he means to come back soon.\p"
	.string "I think he travels because he wants to\n"
	.string "now, not because he has something to\l"
	.string "prove.$"

PetalburgCity_WallysHouse_Text_YouMetWallyInEverGrandeCity:
	.string "Did you meet VAL on\n"
	.string "ESTRADA DO JURAMENTO?\p"
	.string "He came back different: surer of\n"
	.string "himself, but still himself.\p"
	.string "Thank you for walking beside him.$"

PetalburgCity_WallysHouse_Text_WallyWasReallyHappy:
	.string "VAL was very happy after meeting you.\p"
	.string "It had been a long time since I heard my\n"
	.string "son talk about a journey with any\l"
	.string "excitement.$"

PetalburgCity_WallysHouse_Text_WallyLeftWithoutTelling:
	.string "VAL left without really saying\n"
	.string "anything.\p"
	.string "I worry, of course. But I also know he\n"
	.string "had to choose his own road.$"

