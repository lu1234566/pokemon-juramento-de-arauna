AraunaMapLab_MapScripts::
	.byte 0

AraunaMapLab_EventScript_Guide::
	lock
	faceplayer
	goto_if_set FLAG_ARAUNA_MAP_LAB_GUIDE_MET, AraunaMapLab_EventScript_ReturnPrompt
	setflag FLAG_ARAUNA_MAP_LAB_GUIDE_MET
	getpartysize
	goto_if_ne VAR_RESULT, 0, AraunaMapLab_EventScript_GuideIntroduction
	msgbox AraunaMapLab_Text_TestPartner, MSGBOX_DEFAULT
	givemon SPECIES_TREECKO, 5, ITEM_NONE
	setflag FLAG_SYS_POKEMON_GET
	special HealPlayerParty

AraunaMapLab_EventScript_GuideIntroduction::
	msgbox AraunaMapLab_Text_GuideIntroduction, MSGBOX_DEFAULT
	release
	end

AraunaMapLab_EventScript_ReturnPrompt::
	msgbox AraunaMapLab_Text_ReturnPrompt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, AraunaMapLab_EventScript_Stay
	closemessage
	warp MAP_LITTLEROOT_TOWN, 255, 11, 13
	waitstate
	end

AraunaMapLab_EventScript_Stay::
	msgbox AraunaMapLab_Text_Stay, MSGBOX_DEFAULT
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
	getpartysize
	goto_if_eq VAR_RESULT, 0, AraunaMapLab_EventScript_NeedPartner
	trainerbattle_single TRAINER_ARAUNA_SCOUT_NILO, AraunaMapLab_Text_NiloIntro, AraunaMapLab_Text_NiloDefeat
	msgbox AraunaMapLab_Text_NiloPostBattle, MSGBOX_AUTOCLOSE
	end

AraunaMapLab_EventScript_NeedPartner::
	msgbox AraunaMapLab_Text_NeedPartner, MSGBOX_NPC
	end
