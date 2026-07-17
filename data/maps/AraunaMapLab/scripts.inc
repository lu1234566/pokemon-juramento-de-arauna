AraunaMapLab_MapScripts::
	.byte 0

AraunaMapLab_EventScript_Guide::
	lock
	faceplayer
	goto_if_eq VAR_ARAUNA_STORY_STAGE, 0, AraunaMapLab_EventScript_ObjectiveHome
	goto_if_eq VAR_ARAUNA_STORY_STAGE, 1, AraunaMapLab_EventScript_ObjectiveCenter
	goto_if_eq VAR_ARAUNA_STORY_STAGE, 2, AraunaMapLab_EventScript_ObjectiveNilo
	goto_if_eq VAR_ARAUNA_STORY_STAGE, 7, AraunaMapLab_EventScript_ObjectiveNiloReturn
	goto_if_ge VAR_ARAUNA_STORY_STAGE, 8, AraunaMapLab_EventScript_ObjectiveSliceComplete
	msgbox AraunaMapLab_Text_ObjectiveRoute, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_ObjectiveHome::
	msgbox AraunaMapLab_Text_ObjectiveHome, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_ObjectiveCenter::
	msgbox AraunaMapLab_Text_ObjectiveCenter, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_ObjectiveNilo::
	msgbox AraunaMapLab_Text_ObjectiveNilo, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_ObjectiveNiloReturn::
	msgbox AraunaMapLab_Text_ObjectiveNiloReturn, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_ObjectiveSliceComplete::
	msgbox AraunaMapLab_Text_ObjectiveSliceComplete, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_FieldKit::
	lock
	faceplayer
	giveitem ITEM_POTION
	goto_if_eq VAR_RESULT, FALSE, AraunaMapLab_EventScript_BagFull
	setflag FLAG_ARAUNA_MAP_LAB_FIELD_KIT_TAKEN
	removeobject VAR_LAST_TALKED
	msgbox AraunaMapLab_Text_FieldKit, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_BagFull::
	msgbox AraunaMapLab_Text_BagFull, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_Nilo::
	lock
	faceplayer
	goto_if_lt VAR_ARAUNA_STORY_STAGE, 2, AraunaMapLab_EventScript_NeedPartner
	goto_if_eq VAR_ARAUNA_STORY_STAGE, 7, AraunaMapLab_EventScript_NiloEpilogue
	goto_if_ge VAR_ARAUNA_STORY_STAGE, 8, AraunaMapLab_EventScript_NiloAfterSlice
	goto_if_ge VAR_ARAUNA_STORY_STAGE, 3, AraunaMapLab_EventScript_NiloAfterBattle
	trainerbattle_single TRAINER_ARAUNA_SCOUT_NILO, AraunaMapLab_Text_NiloIntro, AraunaMapLab_Text_NiloDefeat
	setvar VAR_ARAUNA_STORY_STAGE, 3
	msgbox AraunaMapLab_Text_NiloPostBattle, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_NeedPartner::
	msgbox AraunaMapLab_Text_NeedPartner, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_NiloAfterBattle::
	msgbox AraunaMapLab_Text_NiloAfterBattle, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_NiloEpilogue::
	msgbox AraunaMapLab_Text_NiloReturnIntro, MSGBOX_DEFAULT
	goto_if_eq VAR_ARAUNA_BOND_CHOICE, 1, AraunaMapLab_EventScript_NiloCourageReaction
	goto_if_eq VAR_ARAUNA_BOND_CHOICE, 2, AraunaMapLab_EventScript_NiloWisdomReaction
	goto AraunaMapLab_EventScript_NiloCompassionReaction

AraunaMapLab_EventScript_NiloCourageReaction::
	msgbox AraunaMapLab_Text_NiloCourageReaction, MSGBOX_DEFAULT
	goto AraunaMapLab_EventScript_NiloMemoryConclusion

AraunaMapLab_EventScript_NiloWisdomReaction::
	msgbox AraunaMapLab_Text_NiloWisdomReaction, MSGBOX_DEFAULT
	goto AraunaMapLab_EventScript_NiloMemoryConclusion

AraunaMapLab_EventScript_NiloCompassionReaction::
	msgbox AraunaMapLab_Text_NiloCompassionReaction, MSGBOX_DEFAULT

AraunaMapLab_EventScript_NiloMemoryConclusion::
	msgbox AraunaMapLab_Text_NiloMemoryConclusion, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_STORY_STAGE, 8
	msgbox AraunaMapLab_Text_VerticalSliceComplete, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_NiloAfterSlice::
	msgbox AraunaMapLab_Text_NiloAfterSlice, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_EnterPlayerHouse::
	warp MAP_ARAUNA_PLAYER_HOUSE, 255, 8, 7
	waitstate
	end

AraunaMapLab_EventScript_EnterResearchCenter::
	warp MAP_ARAUNA_RESEARCH_CENTER, 255, 6, 11
	waitstate
	end

AraunaMapLab_EventScript_EnterMistRoute::
	goto_if_ge VAR_ARAUNA_STORY_STAGE, 3, AraunaMapLab_EventScript_WarpToMistRoute
	lockall
	msgbox AraunaMapLab_Text_RouteLocked, MSGBOX_DEFAULT
	applymovement LOCALID_PLAYER, AraunaMapLab_Movement_StepBackFromRoute
	waitmovement 0
	releaseall
	end

AraunaMapLab_EventScript_WarpToMistRoute::
	warp MAP_ARAUNA_MIST_ROUTE, 255, 10, 18
	waitstate
	end

AraunaMapLab_Movement_StepBackFromRoute:
	walk_left
	step_end
