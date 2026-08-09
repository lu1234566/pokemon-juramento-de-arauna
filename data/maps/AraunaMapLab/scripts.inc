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

@ P12 — the badge. The material conflict between the two friends is placed on
@ the table before they part; staying silent is a real answer, not a skip.
AraunaMapLab_EventScript_CiroBadge::
	msgbox AraunaMapLab_Text_CiroBadgeReveal, MSGBOX_DEFAULT
	setflag FLAG_ARAUNA_CIRO_BADGE_REVEALED
	msgbox AraunaMapLab_Text_CiroBadgeAskMother, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, AraunaMapLab_EventScript_CiroBadgeAskMother
	msgbox AraunaMapLab_Text_CiroBadgeCriticize, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, AraunaMapLab_EventScript_CiroBadgeCriticize
	msgbox AraunaMapLab_Text_CiroBadgeSilentReply, MSGBOX_DEFAULT
	return

AraunaMapLab_EventScript_CiroBadgeAskMother::
	addvar VAR_ARAUNA_BOND_AXES, ARAUNA_BOND_COMPASSION_POINT
	msgbox AraunaMapLab_Text_CiroBadgeAskMotherReply, MSGBOX_DEFAULT
	return

AraunaMapLab_EventScript_CiroBadgeCriticize::
	addvar VAR_ARAUNA_BOND_AXES, ARAUNA_BOND_COURAGE_POINT
	msgbox AraunaMapLab_Text_CiroBadgeCriticizeReply, MSGBOX_DEFAULT
	return

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
	call AraunaMapLab_EventScript_CiroBadge
	msgbox AraunaMapLab_Text_CiroDeparture, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_STORY_STAGE, 8
	msgbox AraunaMapLab_Text_PortoLead, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_CiroAfterPrologue::
	msgbox AraunaMapLab_Text_CiroAfterPrologue, MSGBOX_DEFAULT
	call_if_eq VAR_ARAUNA_BOND_CHOICE, 1, AraunaMapLab_EventScript_CiroBondCourage
	release
	end

@ Bond payoff: Ciro admires the Courage rescue but names what it cost.
AraunaMapLab_EventScript_CiroBondCourage::
	msgbox AraunaMapLab_Text_CiroBondCourage, MSGBOX_DEFAULT
	return

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
	goto_if_ge VAR_ARAUNA_STORY_STAGE, 3, AraunaMapLab_EventScript_WarpToMistRoute
	lockall
	msgbox AraunaMapLab_Text_RouteLocked, MSGBOX_DEFAULT
	applymovement LOCALID_PLAYER, AraunaMapLab_Movement_StepBackFromRoute
	waitmovement 0
	releaseall
	end

AraunaMapLab_EventScript_WarpToMistRoute::
	warp MAP_ARAUNA_MIST_ROUTE, 255, 10, 17
	waitstate
	end

AraunaMapLab_Movement_StepBackFromRoute:
	walk_left
	step_end
