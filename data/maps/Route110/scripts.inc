Route110_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route110_OnTransition
	.byte 0

Route110_OnTransition:
	setweather WEATHER_FOG_HORIZONTAL
	doweather
	end

Route110_EventScript_CoastRoadArrival::
	lockall
	setvar VAR_TEMP_1, 1
	goto_if_set FLAG_ARAUNA_COAST_ROAD_ENTERED, Route110_EventScript_CoastRoadArrivalRepeat
	setflag FLAG_ARAUNA_COAST_ROAD_ENTERED
	msgbox Route110_Text_CoastRoadArrival, MSGBOX_DEFAULT
	releaseall
	end

Route110_EventScript_CoastRoadArrivalRepeat::
	msgbox Route110_Text_CoastRoadReturn, MSGBOX_DEFAULT
	releaseall
	end

Route110_EventScript_BlockNorthRoad::
	goto_if_set FLAG_ARAUNA_NORTH_ROAD_REOPENED, Route110_EventScript_NorthRoadOpen
	lockall
	msgbox Route110_Text_NorthRoadBlocked, MSGBOX_DEFAULT
	applymovement LOCALID_PLAYER, Route110_Movement_StepSouth
	waitmovement 0
	releaseall
	end

Route110_EventScript_NorthRoadOpen::
	end

Route110_EventScript_NorthRoadWorker::
	lock
	faceplayer
	goto_if_set FLAG_ARAUNA_NORTH_ROAD_REOPENED, Route110_EventScript_NorthRoadWorkerOpen
	msgbox Route110_Text_NorthRoadWorker, MSGBOX_DEFAULT
	release
	end

Route110_EventScript_NorthRoadWorkerOpen::
	msgbox Route110_Text_NorthRoadWorkerOpen, MSGBOX_DEFAULT
	release
	end

Route110_EventScript_ConsortiumCheckpoint::
	lock
	faceplayer
	goto_if_set FLAG_ARAUNA_NORTH_ROAD_REOPENED, Route110_EventScript_ConsortiumCheckpointOpen
	msgbox Route110_Text_ConsortiumCheckpoint, MSGBOX_DEFAULT
	release
	end

Route110_EventScript_ConsortiumCheckpointOpen::
	msgbox Route110_Text_ConsortiumCheckpointOpen, MSGBOX_DEFAULT
	release
	end

Route110_EventScript_PortoGuide::
	msgbox Route110_Text_PortoGuide, MSGBOX_NPC
	end

Route110_EventScript_Fisher::
	msgbox Route110_Text_Fisher, MSGBOX_NPC
	end

Route110_EventScript_Migrant::
	msgbox Route110_Text_Migrant, MSGBOX_NPC
	end

Route110_EventScript_Mechanic::
	msgbox Route110_Text_Mechanic, MSGBOX_NPC
	end

Route110_EventScript_Courier::
	msgbox Route110_Text_Courier, MSGBOX_NPC
	end

Route110_EventScript_PortoSign::
	msgbox Route110_Text_PortoSign, MSGBOX_SIGN
	end

Route110_EventScript_NorthClosureSign::
	msgbox Route110_Text_NorthClosureSign, MSGBOX_SIGN
	end

Route110_EventScript_OldCheckpointSign::
	msgbox Route110_Text_OldCheckpointSign, MSGBOX_SIGN
	end

Route110_EventScript_FieldStationSign::
	msgbox Route110_Text_FieldStationSign, MSGBOX_SIGN
	end

Route110_EventScript_ConsortiumFenceSign::
	msgbox Route110_Text_ConsortiumFenceSign, MSGBOX_SIGN
	end

Route110_Movement_StepSouth:
	walk_down
	step_end
