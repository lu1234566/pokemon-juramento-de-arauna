SkyPillar_3F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SkyPillar_3F_OnTransition
	.byte 0

SkyPillar_3F_OnTransition:
	call_if_lt VAR_SKY_PILLAR_STATE, 2, SkyPillar_3F_EventScript_CleanFloor
	end

SkyPillar_3F_EventScript_CleanFloor::
	setmaplayoutindex LAYOUT_ARAUNA_TORRE_3F_CLEAN_V1
	return

