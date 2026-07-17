AraunaMistRoute_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, AraunaMistRoute_OnTransition
	.byte 0

AraunaMistRoute_OnTransition:
	goto_if_eq VAR_ARAUNA_STORY_STAGE, 3, AraunaMistRoute_EventScript_BeginExploration
	end

AraunaMistRoute_EventScript_BeginExploration::
	setvar VAR_ARAUNA_STORY_STAGE, 4
	end

AraunaMistRoute_EventScript_ReturnToVillage::
	warp MAP_ARAUNA_MAP_LAB, 255, 17, 11
	waitstate
	end

AraunaMistRoute_EventScript_EnterRuin::
	warp MAP_ARAUNA_FIRST_LINK_RUIN, 255, 10, 13
	waitstate
	end
