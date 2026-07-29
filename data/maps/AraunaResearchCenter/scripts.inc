AraunaResearchCenter_MapScripts::
	.byte 0

AraunaResearchCenter_EventScript_Maia::
	lock
	faceplayer
	goto_if_eq VAR_ARAUNA_STARTER_CHOICE, 0, AraunaResearchCenter_EventScript_BeforeChoice
	goto_if_eq VAR_ARAUNA_STORY_STAGE, 2, AraunaResearchCenter_EventScript_AfterChoice
	goto AraunaResearchCenter_EventScript_RouteOpen

AraunaResearchCenter_EventScript_BeforeChoice::
	msgbox AraunaResearchCenter_Text_BeforeCall, MSGBOX_DEFAULT
	release
	end

AraunaResearchCenter_EventScript_AfterChoice::
	special HealPlayerParty
	msgbox AraunaResearchCenter_Text_AfterChoice, MSGBOX_DEFAULT
	release
	end

AraunaResearchCenter_EventScript_RouteOpen::
	special HealPlayerParty
	msgbox AraunaResearchCenter_Text_RouteOpen, MSGBOX_DEFAULT
	release
	end

AraunaResearchCenter_EventScript_PicaPau::
	lock
	faceplayer
	goto_if_ne VAR_ARAUNA_STARTER_CHOICE, 0, AraunaResearchCenter_EventScript_AlreadyChosen
	msgbox AraunaPlayerHouse_Text_PimpauStory, MSGBOX_DEFAULT
	msgbox AraunaPlayerHouse_Text_PimpauPrompt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, AraunaResearchCenter_EventScript_ChoiceCancelled
	givemon SPECIES_TREECKO, 5, ITEM_NONE
	setvar VAR_STARTER_MON, 0
	setvar VAR_ARAUNA_STARTER_CHOICE, 1
	goto AraunaPlayerHouse_EventScript_CompleteChoice

AraunaResearchCenter_EventScript_Caramelo::
	lock
	faceplayer
	goto_if_ne VAR_ARAUNA_STARTER_CHOICE, 0, AraunaResearchCenter_EventScript_AlreadyChosen
	msgbox AraunaPlayerHouse_Text_CarameloStory, MSGBOX_DEFAULT
	msgbox AraunaPlayerHouse_Text_CarameloPrompt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, AraunaResearchCenter_EventScript_ChoiceCancelled
	givemon SPECIES_TORCHIC, 5, ITEM_NONE
	setvar VAR_STARTER_MON, 1
	setvar VAR_ARAUNA_STARTER_CHOICE, 2
	goto AraunaPlayerHouse_EventScript_CompleteChoice

AraunaResearchCenter_EventScript_QueroQuero::
	lock
	faceplayer
	goto_if_ne VAR_ARAUNA_STARTER_CHOICE, 0, AraunaResearchCenter_EventScript_AlreadyChosen
	msgbox AraunaPlayerHouse_Text_QueroStory, MSGBOX_DEFAULT
	msgbox AraunaPlayerHouse_Text_QueroPrompt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, AraunaResearchCenter_EventScript_ChoiceCancelled
	givemon SPECIES_MUDKIP, 5, ITEM_NONE
	setvar VAR_STARTER_MON, 2
	setvar VAR_ARAUNA_STARTER_CHOICE, 3
	goto AraunaPlayerHouse_EventScript_CompleteChoice

AraunaResearchCenter_EventScript_AlreadyChosen::
	msgbox AraunaResearchCenter_Text_AlreadyChosen, MSGBOX_DEFAULT
	release
	end

AraunaResearchCenter_EventScript_ChoiceCancelled::
	msgbox AraunaPlayerHouse_Text_ChoiceCancelled, MSGBOX_DEFAULT
	release
	end
