AraunaMistRoute_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, AraunaMistRoute_OnTransition
	.byte 0

AraunaMistRoute_OnTransition:
	goto_if_eq VAR_ARAUNA_STORY_STAGE, 3, AraunaMistRoute_EventScript_BeginExploration
	end

AraunaMistRoute_EventScript_BeginExploration::
	setvar VAR_ARAUNA_STORY_STAGE, 4
	end

AraunaMistRoute_EventScript_FieldObserver::
	lock
	faceplayer
	goto_if_eq VAR_ARAUNA_OPTIONAL_MISSION, 0, AraunaMistRoute_EventScript_OfferNotebookMission
	goto_if_eq VAR_ARAUNA_OPTIONAL_MISSION, 1, AraunaMistRoute_EventScript_NotebookReminder
	goto_if_eq VAR_ARAUNA_OPTIONAL_MISSION, 2, AraunaMistRoute_EventScript_ReturnNotebook
	msgbox AraunaMistRoute_Text_NotebookThanks, MSGBOX_DEFAULT
	release
	end

AraunaMistRoute_EventScript_OfferNotebookMission::
	msgbox AraunaMistRoute_Text_NotebookOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, AraunaMistRoute_EventScript_DeclineNotebookMission
	setvar VAR_ARAUNA_OPTIONAL_MISSION, 1
	msgbox AraunaMistRoute_Text_NotebookAccepted, MSGBOX_DEFAULT
	release
	end

AraunaMistRoute_EventScript_DeclineNotebookMission::
	msgbox AraunaMistRoute_Text_NotebookDeclined, MSGBOX_DEFAULT
	release
	end

AraunaMistRoute_EventScript_NotebookReminder::
	msgbox AraunaMistRoute_Text_NotebookReminder, MSGBOX_DEFAULT
	release
	end

AraunaMistRoute_EventScript_ReturnNotebook::
	giveitem ITEM_SUPER_POTION
	goto_if_eq VAR_RESULT, FALSE, AraunaMistRoute_EventScript_RewardBagFull
	setvar VAR_ARAUNA_OPTIONAL_MISSION, 3
	msgbox AraunaMistRoute_Text_NotebookReturned, MSGBOX_DEFAULT
	release
	end

AraunaMistRoute_EventScript_RewardBagFull::
	msgbox AraunaMistRoute_Text_RewardBagFull, MSGBOX_DEFAULT
	release
	end

AraunaMistRoute_EventScript_FieldNotebook::
	lock
	faceplayer
	setvar VAR_ARAUNA_OPTIONAL_MISSION, 2
	setflag FLAG_ARAUNA_MIST_ROUTE_NOTEBOOK_TAKEN
	removeobject LOCALID_ARAUNA_MIST_ROUTE_NOTEBOOK
	msgbox AraunaMistRoute_Text_NotebookFound, MSGBOX_DEFAULT
	release
	end

AraunaMistRoute_EventScript_AffectedPokemon::
	goto_if_ge VAR_ARAUNA_STORY_STAGE, 5, AraunaMistRoute_EventScript_AffectedPokemonGone
	lockall
	msgbox AraunaMistRoute_Text_AffectedPokemon, MSGBOX_DEFAULT
	setflag FLAG_ARAUNA_MIST_ROUTE_AFFECTED_MON_CLEARED
	setvar VAR_ARAUNA_STORY_STAGE, 5
	msgbox AraunaMistRoute_Text_RuinOpened, MSGBOX_DEFAULT
	releaseall
	end

AraunaMistRoute_EventScript_AffectedPokemonGone::
	end

AraunaMistRoute_EventScript_ReturnToVillage::
	warp MAP_ARAUNA_MAP_LAB, 255, 14, 3
	waitstate
	end

AraunaMistRoute_EventScript_EnterRuin::
	goto_if_ge VAR_ARAUNA_STORY_STAGE, 5, AraunaMistRoute_EventScript_WarpToRuin
	lockall
	msgbox AraunaMistRoute_Text_RuinBlocked, MSGBOX_DEFAULT
	applymovement LOCALID_PLAYER, AraunaMistRoute_Movement_StepBackFromRuin
	waitmovement 0
	releaseall
	end

AraunaMistRoute_EventScript_WarpToRuin::
	warp MAP_ARAUNA_FIRST_LINK_RUIN, 255, 10, 13
	waitstate
	end


AraunaMistRoute_Movement_StepBackFromRuin:
	walk_down
	step_end
