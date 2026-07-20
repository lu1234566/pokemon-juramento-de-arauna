@ Porto das Redes runtime layer for the reused Slateport exterior.

AraunaPorto_EventScript_RoadArrival::
	lockall
	setvar VAR_TEMP_2, 1
	goto_if_set FLAG_ARAUNA_PORTO_IDENTITY_SEEN, AraunaPorto_EventScript_RoadArrivalRepeat
	setflag FLAG_ARAUNA_PORTO_ARRIVED
	setflag FLAG_ARAUNA_PORTO_IDENTITY_SEEN
	goto_if_ge VAR_ARAUNA_ARC_STAGE, 10, AraunaPorto_EventScript_RoadArrivalShow
	setvar VAR_ARAUNA_ARC_STAGE, 10
AraunaPorto_EventScript_RoadArrivalShow::
	msgbox AraunaPorto_Text_RoadArrival, MSGBOX_DEFAULT
	releaseall
	end

AraunaPorto_EventScript_RoadArrivalRepeat::
	msgbox AraunaPorto_Text_RoadArrivalRepeat, MSGBOX_DEFAULT
	releaseall
	end

AraunaPorto_EventScript_HarborResident::
	msgbox AraunaPorto_Text_HarborResident, MSGBOX_NPC
	end

AraunaPorto_EventScript_NetMender::
	msgbox AraunaPorto_Text_NetMender, MSGBOX_NPC
	end

AraunaPorto_EventScript_MemorialKeeper::
	msgbox AraunaPorto_Text_MemorialKeeper, MSGBOX_NPC
	end

AraunaPorto_EventScript_WarehouseWorker::
	msgbox AraunaPorto_Text_WarehouseWorker, MSGBOX_NPC
	end

AraunaPorto_EventScript_CiroPorto::
	lock
	faceplayer
	goto_if_set FLAG_ARAUNA_PORTO_AGENT_DEFEATED, AraunaPorto_EventScript_CiroPortoAfterAgent
	msgbox AraunaPorto_Text_CiroPorto, MSGBOX_DEFAULT
	release
	end

AraunaPorto_EventScript_CiroPortoAfterAgent::
	msgbox AraunaPorto_Text_CiroPortoAfterAgent, MSGBOX_DEFAULT
	release
	end

AraunaPorto_EventScript_BoardBuilder::
	lock
	faceplayer
	goto_if_set FLAG_ARAUNA_BOARD_RECEIVED, AraunaPorto_EventScript_BoardBuilderAfter
	goto_if_unset FLAG_ARAUNA_BADGE_MARE, AraunaPorto_EventScript_BoardBuilderBefore
	checkitemspace ITEM_DEVON_SCOPE, 1
	goto_if_eq VAR_RESULT, FALSE, AraunaPorto_EventScript_BoardBagFull
	msgbox AraunaPorto_Text_BoardOffer, MSGBOX_DEFAULT
	giveitem ITEM_DEVON_SCOPE
	setflag FLAG_ARAUNA_BOARD_RECEIVED
	setflag FLAG_ARAUNA_BOARD_FIELD_UNLOCKED
	msgbox AraunaPorto_Text_BoardReceived, MSGBOX_DEFAULT
	release
	end

AraunaPorto_EventScript_BoardBuilderBefore::
	msgbox AraunaPorto_Text_BoardBeforeBadge, MSGBOX_DEFAULT
	release
	end

AraunaPorto_EventScript_BoardBuilderAfter::
	msgbox AraunaPorto_Text_BoardAfter, MSGBOX_DEFAULT
	release
	end

AraunaPorto_EventScript_BoardBagFull::
	msgbox AraunaPorto_Text_BoardBagFull, MSGBOX_DEFAULT
	release
	end

AraunaPorto_EventScript_CitySign::
	msgbox AraunaPorto_Text_CitySign, MSGBOX_SIGN
	end

AraunaPorto_EventScript_HouseOfTideSign::
	msgbox AraunaPorto_Text_HouseOfTideSign, MSGBOX_SIGN
	end

AraunaPorto_EventScript_MemorialSign::
	msgbox AraunaPorto_Text_MemorialSign, MSGBOX_SIGN
	end

AraunaPorto_EventScript_ConsortiumPostSign::
	msgbox AraunaPorto_Text_ConsortiumPostSign, MSGBOX_SIGN
	end

AraunaPorto_EventScript_NetMarketSign::
	msgbox AraunaPorto_Text_NetMarketSign, MSGBOX_SIGN
	end

AraunaPorto_EventScript_ClosedBuildingSign::
	msgbox AraunaPorto_Text_ClosedBuildingSign, MSGBOX_SIGN
	end

AraunaPorto_EventScript_BoardWorkshopSign::
	msgbox AraunaPorto_Text_BoardWorkshopSign, MSGBOX_SIGN
	end
