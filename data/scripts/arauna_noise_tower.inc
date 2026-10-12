@ Post-League Noise Tower, TR01-TR09: own state, no Emerald crisis bypass.
NoiseTower_OnFrame::
	map_script_2 VAR_TEMP_1, 0, NoiseTower_Admission
	.2byte 0

NoiseTower_Admission::
	setvar VAR_TEMP_1, 1
	goto_if_set FLAG_SYS_GAME_CLEAR, NoiseTower_End
	lockall
	msgbox NoiseTower_Text_LeagueRequired, MSGBOX_DEFAULT
	warp MAP_ARAUNA_CASA_FOGUEIRA_ENTRADA, 0
	waitstate
	releaseall
	end

NoiseTower_End::
	end

NoiseTower_NotChampion::
	msgbox NoiseTower_Text_NoChampion, MSGBOX_DEFAULT
	releaseall
	end

NoiseTower_OutOfOrder::
	msgbox NoiseTower_Text_Order, MSGBOX_DEFAULT
	releaseall
	end

NoiseTower_Travel::
	lockall
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, NoiseTower_NotChampion
	msgbox NoiseTower_Text_Travel, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, NoiseTower_Stay
	warp MAP_ARAUNA_TORRE_RUIDO_RECEPCAO, 0
	waitstate
	releaseall
	end

NoiseTower_Stay::
	msgbox NoiseTower_Text_Stay, MSGBOX_DEFAULT
	releaseall
	end

NoiseTower_Lobby::
	lockall
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, NoiseTower_NotChampion
	goto_if_lt VAR_ARAUNA_TOWER_STATE, 0, NoiseTower_OutOfOrder
	goto_if_ge VAR_ARAUNA_TOWER_STATE, 1, NoiseTower_LobbyAfter
	msgbox NoiseTower_Text_Lobby, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, NoiseTower_Evacuate
	msgbox NoiseTower_Text_Explain, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, NoiseTower_Stay
	setvar VAR_ARAUNA_TOWER_WORKERS, 2
	goto NoiseTower_LobbyDone
	releaseall
	end

NoiseTower_Evacuate::
	setvar VAR_ARAUNA_TOWER_WORKERS, 1
	goto NoiseTower_LobbyDone

NoiseTower_LobbyDone::
	msgbox NoiseTower_Text_LobbyDone, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_TOWER_STATE, 1
	releaseall
	end

NoiseTower_LobbyAfter::
	msgbox NoiseTower_Text_LobbyAfter, MSGBOX_DEFAULT
	releaseall
	end

NoiseTower_Worker::
	lockall
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, NoiseTower_NotChampion
	goto_if_lt VAR_ARAUNA_TOWER_STATE, 0, NoiseTower_OutOfOrder
	msgbox NoiseTower_Text_Worker, MSGBOX_DEFAULT
	releaseall
	end

NoiseTower_Lot1::
	lockall
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, NoiseTower_NotChampion
	goto_if_lt VAR_ARAUNA_TOWER_STATE, 1, NoiseTower_OutOfOrder
	goto_if_set FLAG_ARAUNA_TOWER_LOT_1, NoiseTower_LotAfter
	msgbox NoiseTower_Text_Lot1, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, NoiseTower_Stay
	setflag FLAG_ARAUNA_TOWER_LOT_1
	msgbox NoiseTower_Text_ReleaseLot, MSGBOX_DEFAULT
	call NoiseTower_CheckLots
	releaseall
	end

NoiseTower_Lot2::
	lockall
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, NoiseTower_NotChampion
	goto_if_lt VAR_ARAUNA_TOWER_STATE, 1, NoiseTower_OutOfOrder
	goto_if_set FLAG_ARAUNA_TOWER_LOT_2, NoiseTower_LotAfter
	msgbox NoiseTower_Text_Lot2, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, NoiseTower_Stay
	setflag FLAG_ARAUNA_TOWER_LOT_2
	msgbox NoiseTower_Text_ReleaseLot, MSGBOX_DEFAULT
	call NoiseTower_CheckLots
	releaseall
	end

NoiseTower_Lot3::
	lockall
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, NoiseTower_NotChampion
	goto_if_lt VAR_ARAUNA_TOWER_STATE, 1, NoiseTower_OutOfOrder
	goto_if_set FLAG_ARAUNA_TOWER_LOT_3, NoiseTower_LotAfter
	msgbox NoiseTower_Text_Lot3, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, NoiseTower_Stay
	setflag FLAG_ARAUNA_TOWER_LOT_3
	msgbox NoiseTower_Text_ReleaseLot, MSGBOX_DEFAULT
	call NoiseTower_CheckLots
	releaseall
	end

NoiseTower_LotAfter::
	msgbox NoiseTower_Text_LotAfter, MSGBOX_DEFAULT
	releaseall
	end

NoiseTower_CheckLots::
	goto_if_ge VAR_ARAUNA_TOWER_STATE, 2, NoiseTower_Return
	goto_if_unset FLAG_ARAUNA_TOWER_LOT_1, NoiseTower_Return
	goto_if_unset FLAG_ARAUNA_TOWER_LOT_2, NoiseTower_Return
	goto_if_unset FLAG_ARAUNA_TOWER_LOT_3, NoiseTower_Return
	setvar VAR_ARAUNA_TOWER_STATE, 2
	return

NoiseTower_Return::
	return

NoiseTower_Zila::
	lockall
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, NoiseTower_NotChampion
	goto_if_lt VAR_ARAUNA_TOWER_STATE, 2, NoiseTower_OutOfOrder
	goto_if_ge VAR_ARAUNA_TOWER_STATE, 3, NoiseTower_ZilaAfter
	msgbox NoiseTower_Text_Zila, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, NoiseTower_CopyZila
	msgbox NoiseTower_Text_ZilaReturn, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, NoiseTower_Stay
	setvar VAR_ARAUNA_TOWER_ZILA, 2
	goto NoiseTower_ZilaDone
	releaseall
	end

NoiseTower_CopyZila::
	setvar VAR_ARAUNA_TOWER_ZILA, 1
	goto NoiseTower_ZilaDone

NoiseTower_ZilaDone::
	msgbox NoiseTower_Text_ZilaDone, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_TOWER_STATE, 3
	releaseall
	end

NoiseTower_ZilaAfter::
	msgbox NoiseTower_Text_ZilaAfter, MSGBOX_DEFAULT
	releaseall
	end

NoiseTower_Ciro::
	lockall
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, NoiseTower_NotChampion
	goto_if_lt VAR_ARAUNA_TOWER_STATE, 3, NoiseTower_OutOfOrder
	goto_if_ge VAR_ARAUNA_TOWER_STATE, 4, NoiseTower_CiroAfter
	msgbox NoiseTower_Text_Ciro, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, NoiseTower_Stay
	msgbox NoiseTower_Text_CiroPublic, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_TOWER_STATE, 4
	releaseall
	end

NoiseTower_CiroAfter::
	msgbox NoiseTower_Text_CiroAfter, MSGBOX_DEFAULT
	releaseall
	end

NoiseTower_ItemRECORDING::
	lockall
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, NoiseTower_NotChampion
	goto_if_lt VAR_ARAUNA_TOWER_STATE, 4, NoiseTower_OutOfOrder
	msgbox NoiseTower_Text_ItemRECORDING, MSGBOX_DEFAULT
	setflag FLAG_ARAUNA_TOWER_DAUGHTER_RECORDING
	call NoiseTower_CheckItems
	releaseall
	end

NoiseTower_ItemDRAWING::
	lockall
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, NoiseTower_NotChampion
	goto_if_lt VAR_ARAUNA_TOWER_STATE, 4, NoiseTower_OutOfOrder
	msgbox NoiseTower_Text_ItemDRAWING, MSGBOX_DEFAULT
	setflag FLAG_ARAUNA_TOWER_DAUGHTER_DRAWING
	call NoiseTower_CheckItems
	releaseall
	end

NoiseTower_ItemSCHOOL::
	lockall
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, NoiseTower_NotChampion
	goto_if_lt VAR_ARAUNA_TOWER_STATE, 4, NoiseTower_OutOfOrder
	msgbox NoiseTower_Text_ItemSCHOOL, MSGBOX_DEFAULT
	setflag FLAG_ARAUNA_TOWER_DAUGHTER_SCHOOL
	call NoiseTower_CheckItems
	releaseall
	end

NoiseTower_ItemDAM_REPORT::
	lockall
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, NoiseTower_NotChampion
	goto_if_lt VAR_ARAUNA_TOWER_STATE, 4, NoiseTower_OutOfOrder
	msgbox NoiseTower_Text_ItemDAM_REPORT, MSGBOX_DEFAULT
	setflag FLAG_ARAUNA_TOWER_DAM_REPORT
	call NoiseTower_CheckItems
	releaseall
	end

NoiseTower_CheckItems::
	goto_if_ge VAR_ARAUNA_TOWER_STATE, 5, NoiseTower_Return
	goto_if_unset FLAG_ARAUNA_TOWER_DAUGHTER_RECORDING, NoiseTower_Return
	goto_if_unset FLAG_ARAUNA_TOWER_DAUGHTER_DRAWING, NoiseTower_Return
	goto_if_unset FLAG_ARAUNA_TOWER_DAUGHTER_SCHOOL, NoiseTower_Return
	goto_if_unset FLAG_ARAUNA_TOWER_DAM_REPORT, NoiseTower_Return
	setvar VAR_ARAUNA_TOWER_STATE, 5
	return

NoiseTower_Agent::
	lockall
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, NoiseTower_NotChampion
	goto_if_lt VAR_ARAUNA_TOWER_STATE, 5, NoiseTower_OutOfOrder
	goto_if_ge VAR_ARAUNA_TOWER_STATE, 6, NoiseTower_AgentAfter
	goto_if_eq VAR_ARAUNA_TOWER_WORKERS, 2, NoiseTower_AgentTrust
	msgbox NoiseTower_Text_AgentHesitates, MSGBOX_DEFAULT
	goto NoiseTower_AgentDone
	releaseall
	end

NoiseTower_AgentTrust::
	msgbox NoiseTower_Text_AgentTrust, MSGBOX_DEFAULT
	goto NoiseTower_AgentDone

NoiseTower_AgentDone::
	setvar VAR_ARAUNA_TOWER_STATE, 6
	releaseall
	end

NoiseTower_AgentAfter::
	msgbox NoiseTower_Text_AgentAfter, MSGBOX_DEFAULT
	releaseall
	end

NoiseTower_Meira::
	lockall
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, NoiseTower_NotChampion
	goto_if_lt VAR_ARAUNA_TOWER_STATE, 6, NoiseTower_OutOfOrder
	goto_if_ge VAR_ARAUNA_TOWER_STATE, 9, NoiseTower_MeiraAfter
	goto_if_ge VAR_ARAUNA_TOWER_STATE, 8, NoiseTower_Custody
	goto_if_ge VAR_ARAUNA_TOWER_STATE, 7, NoiseTower_StopSiphon
	msgbox NoiseTower_Text_MeiraBefore, MSGBOX_DEFAULT
	goto_if_defeated TRAINER_ARAUNA_TOWER_MEIRA, NoiseTower_MeiraWon
	trainerbattle_no_intro TRAINER_ARAUNA_TOWER_MEIRA, NoiseTower_Text_MeiraDefeat
NoiseTower_MeiraWon:
	setvar VAR_ARAUNA_TOWER_STATE, 7
	goto NoiseTower_StopSiphon
	releaseall
	end

NoiseTower_StopSiphon::
	msgbox NoiseTower_Text_Siphon, MSGBOX_DEFAULT
	playse SE_EXP_MAX
	msgbox NoiseTower_Text_Stop, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_TOWER_STATE, 8
	goto NoiseTower_Custody

NoiseTower_Custody::
	msgbox NoiseTower_Text_Custody, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, NoiseTower_CustodyHouses
	msgbox NoiseTower_Text_Public, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, NoiseTower_CustodyJustice
	msgbox NoiseTower_Text_Distributed, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, NoiseTower_Stay
	setvar VAR_ARAUNA_TOWER_CUSTODY, 3
	goto NoiseTower_Surrender

NoiseTower_CustodyHouses::
	setvar VAR_ARAUNA_TOWER_CUSTODY, 1
	goto NoiseTower_Surrender

NoiseTower_CustodyJustice::
	setvar VAR_ARAUNA_TOWER_CUSTODY, 2
	goto NoiseTower_Surrender

NoiseTower_Surrender::
	msgbox NoiseTower_Text_Surrender, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_TOWER_STATE, 9
	setflag FLAG_ARAUNA_TOWER_COMPLETE
	releaseall
	end

NoiseTower_MeiraAfter::
	msgbox NoiseTower_Text_MeiraAfter, MSGBOX_DEFAULT
	releaseall
	end

NoiseTower_Text_LeagueRequired:
	.string "The access code is issued only\n"
	.string "after the League. Return to the\l"
	.string "circle first.$"

NoiseTower_Text_NoChampion:
	.string "The League must witness your\n"
	.string "journey before this door opens.$"

NoiseTower_Text_Order:
	.string "There are still people and\n"
	.string "records waiting on the floors\l"
	.string "below.$"

NoiseTower_Text_Travel:
	.string "CIRO: The League heard you.\n"
	.string "Horizon has not stopped. I found\l"
	.string "the route to the NOISE TOWER.\p"
	.string "Go there together?$"

NoiseTower_Text_Stay:
	.string "CIRO: I will wait here. The\n"
	.string "circle keeps your place.$"

NoiseTower_Text_Lobby:
	.string "CIRO: I forged access. They call\n"
	.string "our stories residual assets.\l"
	.string "There are workers upstairs.\p"
	.string "Evacuate the workers?$"

NoiseTower_Text_Explain:
	.string "Explain the danger and let them\n"
	.string "decide how to leave?$"

NoiseTower_Text_LobbyDone:
	.string "The workers leave by the service\n"
	.string "exit. Ciro holds the door.\p"
	.string "CIRO: Nobody stays inside a\n"
	.string "machine meant to erase them.$"

NoiseTower_Text_LobbyAfter:
	.string "CIRO: The essence archive is\n"
	.string "above us. The way out stays\l"
	.string "open.$"

NoiseTower_Text_Worker:
	.string "WORKER: We were told the\n"
	.string "recordings were voluntary.\l"
	.string "Nobody showed us the withdrawal\l"
	.string "forms.$"

NoiseTower_Text_Lot1:
	.string "A sealed essence lot is marked\n"
	.string "with names from the mountain\l"
	.string "ridge.\p"
	.string "Return these records to their\n"
	.string "authors?$"

NoiseTower_Text_ReleaseLot:
	.string "The export queue stops. Ciro\n"
	.string "sends the records back to the\l"
	.string "named community.$"

NoiseTower_Text_Lot2:
	.string "A sealed essence lot is marked\n"
	.string "with names from the coastal\l"
	.string "community.\p"
	.string "Return these records to their\n"
	.string "authors?$"

NoiseTower_Text_Lot3:
	.string "A sealed essence lot is marked\n"
	.string "with names from the people at\l"
	.string "the fire.\p"
	.string "Return these records to their\n"
	.string "authors?$"

NoiseTower_Text_LotAfter:
	.string "This lot is empty. Its records\n"
	.string "have gone back to their authors.$"

NoiseTower_Text_Zila:
	.string "ANAHI: Item 11.407. They\n"
	.string "catalogued ZILA as an\l"
	.string "asset.\p"
	.string "Destroying it now would lose her\n"
	.string "words. Make a protected copy\l"
	.string "first?$"

NoiseTower_Text_ZilaReturn:
	.string "Ask Anahi to return the record\n"
	.string "directly to the community?$"

NoiseTower_Text_ZilaDone:
	.string "ANAHI: We preserve the voice and\n"
	.string "return the right to choose.\p"
	.string "{PLAYER}: Her name is not an\n"
	.string "inventory number.$"

NoiseTower_Text_ZilaAfter:
	.string "ZILA is named beside her\n"
	.string "words. The corporate copy is\l"
	.string "sealed from use.$"

NoiseTower_Text_Ciro:
	.string "CIRO: That is my signature. And\n"
	.string "the consent form for my mother.\l"
	.string "They bundled them into one\l"
	.string "contract.\p"
	.string "Will you stay while I publish\n"
	.string "both?$"

NoiseTower_Text_CiroPublic:
	.string "CIRO: I believed signing made me\n"
	.string "useful. It made me owned.\p"
	.string "The contracts leave the private\n"
	.string "server. Their authors receive\l"
	.string "copies.$"

NoiseTower_Text_CiroAfter:
	.string "CIRO: My mother chooses for\n"
	.string "herself. My signature does not\l"
	.string "speak for her.$"

NoiseTower_Text_ItemRECORDING:
	.string "A recording: Meira's daughter\n"
	.string "laughing as she tries to sing.$"

NoiseTower_Text_ItemDRAWING:
	.string "A drawing: a river, her house\n"
	.string "and a person she names as her\l"
	.string "father.$"

NoiseTower_Text_ItemSCHOOL:
	.string "A school report: the things she\n"
	.string "wanted to learn, not the date\l"
	.string "she died.$"

NoiseTower_Text_ItemDAM_REPORT:
	.string "The dam-pilot report: a Horizon\n"
	.string "test caused the flood. The\l"
	.string "creatures were blamed for a\l"
	.string "corporate decision.$"

NoiseTower_Text_AgentHesitates:
	.string "AGENT: The order says erase this\n"
	.string "floor. With the workers still\l"
	.string "here.\p"
	.string "CIRO: Look. We got them out.\p"
	.string "The agent lowers the recorder.$"

NoiseTower_Text_AgentTrust:
	.string "AGENT: They told me you listened\n"
	.string "before asking them to leave.\p"
	.string "I will not erase the people who\n"
	.string "trusted you. I will open the\l"
	.string "control room.$"

NoiseTower_Text_AgentAfter:
	.string "AGENT: The order is on public\n"
	.string "record. I cannot make it\l"
	.string "unspoken.$"

NoiseTower_Text_MeiraBefore:
	.string "MEIRA: You call it memory\n"
	.string "because you never had to sleep\l"
	.string "beside it.\p"
	.string "{PLAYER}: I do. It has a\n"
	.string "different name.$"

NoiseTower_Text_MeiraDefeat:
	.string "You cannot take her name from\n"
	.string "me.$"

NoiseTower_Text_Siphon:
	.string "MEIRA: If I forget her face, the\n"
	.string "rest ends.\p"
	.string "{PLAYER}: Only the part where\n"
	.string "she could be more than the worst\l"
	.string "night of your life.\p"
	.string "You set the recording, drawing\n"
	.string "and school report beside the dam\l"
	.string "test.\p"
	.string "The report tells how she died.\n"
	.string "The other records tell who she\l"
	.string "was.$"

NoiseTower_Text_Stop:
	.string "Ciro holds the emergency\n"
	.string "control. Anahi reads the report\l"
	.string "with its authors named.\p"
	.string "The MASTER SIPHON stops. Nobody\n"
	.string "removes Meira's memories for\l"
	.string "him.$"

NoiseTower_Text_Custody:
	.string "MEIRA: Thirty years making\n"
	.string "Arauna pay for a lie.\p"
	.string "He switches off the NOISE TOWER.\n"
	.string "The archives still need\l"
	.string "custodians.\p"
	.string "Entrust them to the Houses?$"

NoiseTower_Text_Public:
	.string "Entrust them to public justice?$"

NoiseTower_Text_Distributed:
	.string "Return custody through a\n"
	.string "distributed community census?$"

NoiseTower_Text_Surrender:
	.string "Meira surrenders. The records\n"
	.string "leave corporate custody with\l"
	.string "their authors and your decision\l"
	.string "named.\p"
	.string "CIRO: Go back to the Fogueira.\n"
	.string "Silence is not the same as a\l"
	.string "story returned.$"

NoiseTower_Text_MeiraAfter:
	.string "The controls are dark. Meira\n"
	.string "waits for those entrusted with\l"
	.string "the archives.$"
