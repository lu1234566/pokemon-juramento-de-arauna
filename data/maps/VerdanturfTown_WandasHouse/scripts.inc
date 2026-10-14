VerdanturfTown_WandasHouse_MapScripts::
	.byte 0

VerdanturfTown_WandasHouse_EventScript_Wally::
	lock
	faceplayer
	goto_if_set FLAG_WALLY_SPEECH, VerdanturfTown_WandasHouse_EventScript_WallyShortSpeech
	msgbox VerdanturfTown_WandasHouse_Text_StrongerSpeech, MSGBOX_DEFAULT
	setflag FLAG_WALLY_SPEECH
	release
	end

VerdanturfTown_WandasHouse_EventScript_WallyShortSpeech::
	msgbox VerdanturfTown_WandasHouse_Text_StrongerSpeechShort, MSGBOX_DEFAULT
	release
	end

VerdanturfTown_WandasHouse_EventScript_WallysUncle::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_WALLY_VICTORY_ROAD, VerdanturfTown_WandasHouse_EventScript_WallysUncleEverGrande
	goto_if_set FLAG_DEFEATED_LAVARIDGE_GYM, VerdanturfTown_WandasHouse_EventScript_WallysUncleSlippedOff
	msgbox VerdanturfTown_WandasHouse_Text_WallysNextDoor, MSGBOX_DEFAULT
	release
	end

VerdanturfTown_WandasHouse_EventScript_WallysUncleSlippedOff::
	msgbox VerdanturfTown_WandasHouse_Text_WallySlippedOff, MSGBOX_DEFAULT
	release
	end

VerdanturfTown_WandasHouse_EventScript_WallysUncleEverGrande::
	msgbox VerdanturfTown_WandasHouse_Text_WallyGoneThatFar, MSGBOX_DEFAULT
	release
	end

VerdanturfTown_WandasHouse_EventScript_WandasBoyfriend::
	msgbox VerdanturfTown_WandasHouse_Text_CanSeeGirlfriendEveryDay, MSGBOX_NPC
	end

VerdanturfTown_WandasHouse_EventScript_Wanda::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_LAVARIDGE_GYM, VerdanturfTown_WandasHouse_EventScript_WandaDontWorry
	goto_if_set FLAG_DEFEATED_WALLY_MAUVILLE, VerdanturfTown_WandasHouse_EventScript_MeetWanda
	msgbox VerdanturfTown_WandasHouse_Text_DontWorryAboutWally, MSGBOX_DEFAULT
	release
	end

VerdanturfTown_WandasHouse_EventScript_MeetWanda::
	msgbox VerdanturfTown_WandasHouse_Text_MeetWanda, MSGBOX_DEFAULT
	release
	end

VerdanturfTown_WandasHouse_EventScript_WandaDontWorry::
	msgbox VerdanturfTown_WandasHouse_Text_DontWorryAboutWally, MSGBOX_DEFAULT
	release
	end

VerdanturfTown_WandasHouse_EventScript_WallysAunt::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_WALLY_VICTORY_ROAD, VerdanturfTown_WandasHouse_EventScript_WallysAuntEverGrande
	goto_if_set FLAG_DEFEATED_LAVARIDGE_GYM, VerdanturfTown_WandasHouse_EventScript_WallysAuntAnythingHappened
	goto_if_set FLAG_RUSTURF_TUNNEL_OPENED, VerdanturfTown_WandasHouse_EventScript_WallysAuntTunnelOpen
	msgbox VerdanturfTown_WandasHouse_Text_DaughtersBoyfriendDriven, MSGBOX_DEFAULT
	release
	end

VerdanturfTown_WandasHouse_EventScript_WallysAuntTunnelOpen::
	msgbox VerdanturfTown_WandasHouse_Text_DaughtersBoyfriendWasDigging, MSGBOX_DEFAULT
	release
	end

VerdanturfTown_WandasHouse_EventScript_WallysAuntAnythingHappened::
	msgbox VerdanturfTown_WandasHouse_Text_IfAnythingHappenedToWally, MSGBOX_DEFAULT
	release
	end

VerdanturfTown_WandasHouse_EventScript_WallysAuntEverGrande::
	msgbox VerdanturfTown_WandasHouse_Text_WallyWasInEverGrande, MSGBOX_DEFAULT
	release
	end

VerdanturfTown_WandasHouse_Text_StrongerSpeech:
	.string "VAL: I am still afraid.\p"
	.string "Now I know courage is not\n"
	.string "forgetting fear. It is walking\n"
	.string "while remembering it.$"

VerdanturfTown_WandasHouse_Text_StrongerSpeechShort:
	.string "VAL: I am still afraid.\p"
	.string "I just know how to keep walking\n"
	.string "with it now.$"

VerdanturfTown_WandasHouse_Text_WallysNextDoor:
	.string "VAL is next door.\p"
	.string "He came here to recover and\n"
	.string "found his own pace instead.$"

VerdanturfTown_WandasHouse_Text_WallySlippedOff:
	.string "VAL left on his own again.\p"
	.string "He said he needed to know how\n"
	.string "far his own pace could take him.$"

VerdanturfTown_WandasHouse_Text_WallyGoneThatFar:
	.string "VAL reached OATH ROAD?\p"
	.string "He spent so long thinking he had\n"
	.string "to become someone else.\p"
	.string "I am glad he kept his own pace.$"

VerdanturfTown_WandasHouse_Text_MeetWanda:
	.string "WANDA: You are {PLAYER}?\p"
	.string "VAL told me about you. I'm his\n"
	.string "cousin. Glad to meet you.\p"
	.string "He has more energy since coming\n"
	.string "here, but we let him set the\n"
	.string "pace.$"

VerdanturfTown_WandasHouse_Text_DontWorryAboutWally:
	.string "VAL: I spent too long thinking I\n"
	.string "had to become someone else to\n"
	.string "keep traveling.\p"
	.string "I only needed to find my own\n"
	.string "pace.$"

VerdanturfTown_WandasHouse_Text_CanSeeGirlfriendEveryDay:
	.string "Thanks to you, the tunnel is\n"
	.string "open.\p"
	.string "I can see my girlfriend every\n"
	.string "day without putting the POKéMON\n"
	.string "in the cave through more\n"
	.string "blasting.$"

VerdanturfTown_WandasHouse_Text_DaughtersBoyfriendDriven:
	.string "My daughter's boyfriend kept\n"
	.string "digging the tunnel by hand.\p"
	.string "She worried about him, so she\n"
	.string "checked on him often.$"

VerdanturfTown_WandasHouse_Text_DaughtersBoyfriendWasDigging:
	.string "He finished the tunnel by hand.\p"
	.string "No blasting, and the cave\n"
	.string "POKéMON were left in peace.$"

VerdanturfTown_WandasHouse_Text_IfAnythingHappenedToWally:
	.string "VAL still worries us sometimes.\p"
	.string "But helping him does not mean\n"
	.string "choosing his life for him.$"

VerdanturfTown_WandasHouse_Text_WallyWasInEverGrande:
	.string "VAL made it all the way to OATH\n"
	.string "ROAD.\p"
	.string "He chose that path himself. That\n"
	.string "matters more than how fast.$"

