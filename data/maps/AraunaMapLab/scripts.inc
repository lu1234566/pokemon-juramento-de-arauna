AraunaMapLab_MapScripts::
	.byte 0

AraunaMapLab_EventScript_Guide::
	lock
	faceplayer
	goto_if_eq VAR_ARAUNA_STORY_STAGE, 0, AraunaMapLab_EventScript_ObjectiveHome
	goto_if_eq VAR_ARAUNA_STORY_STAGE, 1, AraunaMapLab_EventScript_ObjectiveCenter
	goto_if_eq VAR_ARAUNA_STORY_STAGE, 2, AraunaMapLab_EventScript_ObjectiveCiro
	goto_if_eq VAR_ARAUNA_STORY_STAGE, 6, AraunaMapLab_EventScript_ObjectiveCiroBattle
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

AraunaMapLab_EventScript_ObjectiveCiro::
	msgbox AraunaMapLab_Text_ObjectiveCiro, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_ObjectiveCiroBattle::
	msgbox AraunaMapLab_Text_ObjectiveCiroBattle, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_ObjectiveSliceComplete::
	msgbox AraunaMapLab_Text_ObjectiveSliceComplete, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_FieldKit::
	lock
	faceplayer
	goto_if_lt VAR_ARAUNA_STORY_STAGE, 2, AraunaMapLab_EventScript_FieldKitLocked
	checkitemspace ITEM_POKE_BALL, 5
	goto_if_eq VAR_RESULT, FALSE, AraunaMapLab_EventScript_BagFull
	checkitemspace ITEM_POTION, 3
	goto_if_eq VAR_RESULT, FALSE, AraunaMapLab_EventScript_BagFull
	giveitem ITEM_POKE_BALL, 5
	giveitem ITEM_POTION, 3
	setflag FLAG_ARAUNA_MAP_LAB_FIELD_KIT_TAKEN
	removeobject VAR_LAST_TALKED
	msgbox AraunaMapLab_Text_FieldKit, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_FieldKitLocked::
	msgbox AraunaMapLab_Text_FieldKitLocked, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_BagFull::
	msgbox AraunaMapLab_Text_BagFull, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_Ciro::
	lock
	faceplayer
	goto_if_lt VAR_ARAUNA_STORY_STAGE, 2, AraunaMapLab_EventScript_NeedPartner
	goto_if_ge VAR_ARAUNA_STORY_STAGE, 8, AraunaMapLab_EventScript_CiroAfterPrologue
	goto_if_eq VAR_ARAUNA_STORY_STAGE, 6, AraunaMapLab_EventScript_CiroBattle
	goto_if_ge VAR_ARAUNA_STORY_STAGE, 3, AraunaMapLab_EventScript_CiroWaiting
	goto AraunaMapLab_EventScript_CiroBeforeRoute

AraunaMapLab_EventScript_CiroBeforeRoute::
	msgbox AraunaMapLab_Text_CiroBeforeRoute, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_STORY_STAGE, 3
	release
	end

AraunaMapLab_EventScript_CiroWaiting::
	msgbox AraunaMapLab_Text_CiroWaiting, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_CiroBattle::
	goto_if_set FLAG_ARAUNA_CIRO_STARTER_PIMPAU, AraunaMapLab_EventScript_CiroBattlePimpau
	goto_if_set FLAG_ARAUNA_CIRO_STARTER_CARAMELO, AraunaMapLab_EventScript_CiroBattleCaramelo
	goto AraunaMapLab_EventScript_CiroBattleQuero

AraunaMapLab_EventScript_CiroBattlePimpau::
	trainerbattle_single TRAINER_ARAUNA_CIRO_PIMPAU, AraunaMapLab_Text_CiroIntro, AraunaMapLab_Text_CiroDefeat
	goto AraunaMapLab_EventScript_CiroBattleWon

AraunaMapLab_EventScript_CiroBattleCaramelo::
	trainerbattle_single TRAINER_ARAUNA_CIRO_CARAMELO, AraunaMapLab_Text_CiroIntro, AraunaMapLab_Text_CiroDefeat
	goto AraunaMapLab_EventScript_CiroBattleWon

AraunaMapLab_EventScript_CiroBattleQuero::
	trainerbattle_single TRAINER_ARAUNA_CIRO_QUERO, AraunaMapLab_Text_CiroIntro, AraunaMapLab_Text_CiroDefeat
	goto AraunaMapLab_EventScript_CiroBattleWon

AraunaMapLab_EventScript_CiroBattleWon::
	setvar VAR_ARAUNA_STORY_STAGE, 7
	msgbox AraunaMapLab_Text_CiroPostBattle, MSGBOX_DEFAULT
	msgbox AraunaMapLab_Text_CiroDeparture, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_STORY_STAGE, 8
	msgbox AraunaMapLab_Text_PortoLead, MSGBOX_DEFAULT
	goto AraunaMapLab_EventScript_OfferPortoTravel

AraunaMapLab_EventScript_CiroAfterPrologue::
	msgbox AraunaMapLab_Text_CiroAfterPrologue, MSGBOX_DEFAULT
	goto AraunaMapLab_EventScript_OfferPortoTravel

AraunaMapLab_EventScript_OfferPortoTravel::
	msgbox AraunaPorto_Text_CiroTravelPrompt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, AraunaMapLab_EventScript_CiroStay
	goto_if_ge VAR_ARAUNA_ARC_STAGE, 10, AraunaMapLab_EventScript_TravelToPorto
	setvar VAR_ARAUNA_ARC_STAGE, 10
	setflag FLAG_ARAUNA_PORTO_ARRIVED

AraunaMapLab_EventScript_TravelToPorto::
	@ Route 109 (30, 6) is dry north-beach ground, outside swimmer paths.
	warp MAP_ROUTE109, 255, 30, 6
	waitstate
	end

AraunaMapLab_EventScript_CiroStay::
	msgbox AraunaPorto_Text_CiroStay, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_NeedPartner::
	msgbox AraunaMapLab_Text_NeedPartner, MSGBOX_DEFAULT
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
	goto_if_ge VAR_ARAUNA_STORY_STAGE, 8, AraunaMapLab_EventScript_DepartForPorto
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

AraunaMapLab_EventScript_DepartForPorto::
	lockall
	goto_if_ge VAR_ARAUNA_ARC_STAGE, 10, AraunaMapLab_EventScript_DepartForPortoReady
	setvar VAR_ARAUNA_ARC_STAGE, 10
	setflag FLAG_ARAUNA_PORTO_ARRIVED

AraunaMapLab_EventScript_DepartForPortoReady::
	msgbox AraunaPorto_Text_CoastRoadDeparture, MSGBOX_DEFAULT
	goto AraunaMapLab_EventScript_TravelToPorto

AraunaMapLab_Movement_StepBackFromRoute:
	walk_left
	step_end
