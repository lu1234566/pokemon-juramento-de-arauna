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
	.string "Obrigado por ter ajudado VAL.\p"
	.string "Ele fala de voce como alguem\n"
	.string "que o tratou com paciencia.\p"
	.string "Isso fez bem a ele.$"

PetalburgCity_WallysHouse_Text_WonderHowWallyIsDoing:
	.string "VAL nao manda noticias ha alguns dias.\p"
	.string "Quando ele coloca uma viagem na\n"
	.string "cabeca, esquece do resto.\p"
	.string "Espero que esteja bem.$"

PetalburgCity_WallysHouse_Text_PleaseExcuseUs:
	.string "{PLAYER}! Desculpe trazer voce\n"
	.string "ate aqui desse jeito.\p"
	.string "VAL melhorou muito desde que foi\n"
	.string "para o VALE DO SILENCIO.\p"
	.string "Voce o ajudou quando ele ainda\n"
	.string "tinha medo de viajar sozinho.\p"
	.string "Como pai, eu nao esqueco disso.\p"
	.string "Quero que leve isto.$"

PetalburgCity_WallysHouse_Text_SurfGoAllSortsOfPlaces:
	.string "Com SURF, seu POKéMON pode cruzar\n"
	.string "trechos de agua e abrir novos caminhos.$"

PetalburgCity_WallysHouse_Text_WallyIsComingHomeSoon:
	.string "VAL disse que pretende voltar em breve.\p"
	.string "Acho que agora ele viaja porque quer,\n"
	.string "nao porque precisa provar alguma coisa.$"

PetalburgCity_WallysHouse_Text_YouMetWallyInEverGrandeCity:
	.string "Voce encontrou VAL na\n"
	.string "ESTRADA DO JURAMENTO?\p"
	.string "Ele voltou diferente: mais seguro,\n"
	.string "mas ainda sendo ele mesmo.\p"
	.string "Obrigado por caminhar ao lado dele.$"

PetalburgCity_WallysHouse_Text_WallyWasReallyHappy:
	.string "VAL ficou muito feliz depois\n"
	.string "de conhecer voce.\p"
	.string "Fazia tempo que eu nao via meu filho\n"
	.string "falar de uma viagem com entusiasmo.$"

PetalburgCity_WallysHouse_Text_WallyLeftWithoutTelling:
	.string "VAL saiu sem avisar direito.\p"
	.string "Eu me preocupo, claro. Mas tambem\n"
	.string "sei que ele precisava escolher\l"
	.string "o proprio caminho.$"

