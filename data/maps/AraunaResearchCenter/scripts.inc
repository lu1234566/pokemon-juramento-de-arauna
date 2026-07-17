AraunaResearchCenter_MapScripts::
	.byte 0

AraunaResearchCenter_EventScript_Maia::
	lock
	faceplayer
	goto_if_lt VAR_ARAUNA_STORY_STAGE, 1, AraunaResearchCenter_EventScript_BeforeCall
	goto_if_eq VAR_ARAUNA_STORY_STAGE, 1, AraunaResearchCenter_EventScript_Introduction
	goto_if_eq VAR_ARAUNA_STORY_STAGE, 2, AraunaResearchCenter_EventScript_AfterChoice
	msgbox AraunaResearchCenter_Text_RouteOpen, MSGBOX_DEFAULT
	release
	end

AraunaResearchCenter_EventScript_BeforeCall::
	msgbox AraunaResearchCenter_Text_BeforeCall, MSGBOX_DEFAULT
	release
	end

AraunaResearchCenter_EventScript_Introduction::
	msgbox AraunaResearchCenter_Text_MaiaIntroduction, MSGBOX_DEFAULT
	release
	end

AraunaResearchCenter_EventScript_AfterChoice::
	msgbox AraunaResearchCenter_Text_AfterChoice, MSGBOX_DEFAULT
	release
	end

AraunaResearchCenter_EventScript_PicaPau::
	lock
	faceplayer
	goto AraunaResearchCenter_EventScript_CheckPicaPau

AraunaResearchCenter_EventScript_CheckPicaPau::
	goto_if_lt VAR_ARAUNA_STORY_STAGE, 1, AraunaResearchCenter_EventScript_SelectionLocked
	goto_if_ne VAR_ARAUNA_STARTER_CHOICE, 0, AraunaResearchCenter_EventScript_AlreadyChosen
	msgbox AraunaResearchCenter_Text_PicaPauPrompt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, AraunaResearchCenter_EventScript_ChoiceCancelled
	givemon SPECIES_TREECKO, 5, ITEM_NONE
	setvar VAR_STARTER_MON, 0
	setvar VAR_ARAUNA_STARTER_CHOICE, 1
	goto AraunaResearchCenter_EventScript_CompleteChoice

AraunaResearchCenter_EventScript_Caramelo::
	lock
	faceplayer
	goto_if_lt VAR_ARAUNA_STORY_STAGE, 1, AraunaResearchCenter_EventScript_SelectionLocked
	goto_if_ne VAR_ARAUNA_STARTER_CHOICE, 0, AraunaResearchCenter_EventScript_AlreadyChosen
	msgbox AraunaResearchCenter_Text_CarameloPrompt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, AraunaResearchCenter_EventScript_ChoiceCancelled
	givemon SPECIES_TORCHIC, 5, ITEM_NONE
	setvar VAR_STARTER_MON, 1
	setvar VAR_ARAUNA_STARTER_CHOICE, 2
	goto AraunaResearchCenter_EventScript_CompleteChoice

AraunaResearchCenter_EventScript_QueroQuero::
	lock
	faceplayer
	goto_if_lt VAR_ARAUNA_STORY_STAGE, 1, AraunaResearchCenter_EventScript_SelectionLocked
	goto_if_ne VAR_ARAUNA_STARTER_CHOICE, 0, AraunaResearchCenter_EventScript_AlreadyChosen
	msgbox AraunaResearchCenter_Text_QueroQueroPrompt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, AraunaResearchCenter_EventScript_ChoiceCancelled
	givemon SPECIES_MUDKIP, 5, ITEM_NONE
	setvar VAR_STARTER_MON, 2
	setvar VAR_ARAUNA_STARTER_CHOICE, 3

AraunaResearchCenter_EventScript_CompleteChoice::
	setflag FLAG_SYS_POKEMON_GET
	setvar VAR_ARAUNA_STORY_STAGE, 2
	special HealPlayerParty
	msgbox AraunaResearchCenter_Text_PlaceholderNotice, MSGBOX_DEFAULT
	release
	end

AraunaResearchCenter_EventScript_SelectionLocked::
	msgbox AraunaResearchCenter_Text_SelectionLocked, MSGBOX_DEFAULT
	release
	end

AraunaResearchCenter_EventScript_AlreadyChosen::
	msgbox AraunaResearchCenter_Text_AlreadyChosen, MSGBOX_DEFAULT
	release
	end

AraunaResearchCenter_EventScript_ChoiceCancelled::
	msgbox AraunaResearchCenter_Text_ChoiceCancelled, MSGBOX_DEFAULT
	release
	end
