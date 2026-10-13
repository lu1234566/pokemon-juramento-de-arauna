Arauna_PrimeiraCamara_Interior_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, PrimeiraCamara_Interior_OnLoad
	.byte 0

PrimeiraCamara_Interior_OnLoad:
	call_if_set FLAG_ARAUNA_FIRST_CHAMBER_ALTAR_HEARD, PrimeiraCamara_ActiveAltarTiles
	end

PrimeiraCamara_EventScript_Altar::
	lockall
	goto_if_set FLAG_ARAUNA_FIRST_CHAMBER_ALTAR_HEARD, PrimeiraCamara_AltarReturn
	msgbox PrimeiraCamara_Text_Listen, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PrimeiraCamara_AltarDecline
	setflag FLAG_ARAUNA_FIRST_CHAMBER_ALTAR_HEARD
	call PrimeiraCamara_ActiveAltarTiles
	special DrawWholeMapView
	playse SE_SHOP
	msgbox PrimeiraCamara_Text_Heard, MSGBOX_DEFAULT
	releaseall
	end

PrimeiraCamara_AltarDecline:
	msgbox PrimeiraCamara_Text_Decline, MSGBOX_DEFAULT
	releaseall
	end

PrimeiraCamara_AltarReturn:
	msgbox PrimeiraCamara_Text_Return, MSGBOX_DEFAULT
	goto_if_set FLAG_ARAUNA_FIRST_LINK_MADE, PrimeiraCamara_LinkKept
	msgbox PrimeiraCamara_Text_RiteOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PrimeiraCamara_RiteLater
	goto PrimeiraCamara_ChooseLink

@ The first link -- DRAFT of the Sistema de Vinculos rite
@ (docs/ARCOS_RASCUNHO.md). The altar reads how much a companion trusts the
@ player; the one named here holds on in battle once it trusts them fully
@ (src/arauna_bond.c). The name can be given again to someone else.
PrimeiraCamara_LinkKept:
	special AraunaBond_FindFirstLink
	goto_if_eq VAR_RESULT, PARTY_SIZE, PrimeiraCamara_LinkAway
	msgbox PrimeiraCamara_Text_LinkHere, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PrimeiraCamara_RiteLater
	goto PrimeiraCamara_ChooseLink

PrimeiraCamara_LinkAway:
	msgbox PrimeiraCamara_Text_LinkAway, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PrimeiraCamara_RiteLater
PrimeiraCamara_ChooseLink:
	msgbox PrimeiraCamara_Text_Choose, MSGBOX_DEFAULT
	special ChoosePartyMon
	goto_if_ge VAR_0x8004, PARTY_SIZE, PrimeiraCamara_RiteLater
	special AraunaBond_ReadSelected
	switch VAR_RESULT
	case 0, PrimeiraCamara_ReadThin
	case 1, PrimeiraCamara_ReadFlicker
	case 2, PrimeiraCamara_ReadSteady
	case 3, PrimeiraCamara_ReadFull
	msgbox PrimeiraCamara_Text_Egg, MSGBOX_DEFAULT
	releaseall
	end

PrimeiraCamara_ReadThin:
	msgbox PrimeiraCamara_Text_ReadThin, MSGBOX_DEFAULT
	goto PrimeiraCamara_ConfirmLink

PrimeiraCamara_ReadFlicker:
	msgbox PrimeiraCamara_Text_ReadFlicker, MSGBOX_DEFAULT
	goto PrimeiraCamara_ConfirmLink

PrimeiraCamara_ReadSteady:
	msgbox PrimeiraCamara_Text_ReadSteady, MSGBOX_DEFAULT
	goto PrimeiraCamara_ConfirmLink

PrimeiraCamara_ReadFull:
	msgbox PrimeiraCamara_Text_ReadFull, MSGBOX_DEFAULT
PrimeiraCamara_ConfirmLink:
	msgbox PrimeiraCamara_Text_ConfirmLink, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PrimeiraCamara_RiteLater
	special AraunaBond_MakeFirstLink
	playse SE_M_HEAL_BELL
	msgbox PrimeiraCamara_Text_Linked, MSGBOX_DEFAULT
	waitse
	releaseall
	end

PrimeiraCamara_RiteLater:
	msgbox PrimeiraCamara_Text_RiteLater, MSGBOX_DEFAULT
	releaseall
	end

PrimeiraCamara_ActiveAltarTiles:
	setmetatile 9, 8, 604, TRUE
	setmetatile 10, 8, 605, TRUE
	setmetatile 11, 8, 606, TRUE
	setmetatile 12, 8, 604, TRUE
	setmetatile 9, 9, 607, TRUE
	setmetatile 10, 9, 608, TRUE
	setmetatile 11, 9, 609, TRUE
	setmetatile 12, 9, 610, TRUE
	setmetatile 9, 10, 611, TRUE
	setmetatile 10, 10, 612, TRUE
	setmetatile 11, 10, 613, TRUE
	setmetatile 12, 10, 614, TRUE
	setmetatile 9, 11, 615, TRUE
	setmetatile 10, 11, 616, TRUE
	setmetatile 11, 11, 617, TRUE
	setmetatile 12, 11, 618, TRUE
	return

PrimeiraCamara_Text_Listen:
	.string "The tie is broken, but there is a light\n"
	.string "between the parts.\p"
	.string "Will you stop and listen?$"

PrimeiraCamara_Text_Heard:
	.string "The light reaches both ends of the tie.\p"
	.string "What binds us stays.$"

PrimeiraCamara_Text_Decline:
	.string "The silence waits. You can come back\n"
	.string "whenever you like.$"

PrimeiraCamara_Text_Return:
	.string "The tie keeps the light of your\n"
	.string "listening.$"

PrimeiraCamara_Text_RiteOffer:
	.string "Between the broken ends there is\n"
	.string "room for one name.\p"
	.string "Will you name the companion\n"
	.string "you trust most?$"

PrimeiraCamara_Text_LinkHere:
	.string "{STR_VAR_1}'s name still glows\n"
	.string "between the ends of the tie.\p"
	.string "Name a different first link?$"

PrimeiraCamara_Text_LinkAway:
	.string "The light between the ends waits\n"
	.string "for your first link to return.\p"
	.string "Name a different first link?$"

PrimeiraCamara_Text_Choose:
	.string "Choose the companion whose name\n"
	.string "you will speak at the tie.$"

PrimeiraCamara_Text_Egg:
	.string "An EGG has no name to give yet.$"

PrimeiraCamara_Text_ReadThin:
	.string "The light is as thin as a thread.\p"
	.string "{STR_VAR_1} doesn't know you\n"
	.string "very well yet.$"

PrimeiraCamara_Text_ReadFlicker:
	.string "The light flickers, then holds.\p"
	.string "{STR_VAR_1} is still learning\n"
	.string "to trust you.$"

PrimeiraCamara_Text_ReadSteady:
	.string "The light is strong and steady.\p"
	.string "{STR_VAR_1} trusts you. The tie\n"
	.string "can still grow brighter.$"

PrimeiraCamara_Text_ReadFull:
	.string "The light runs from one end of the\n"
	.string "tie to the other without a flicker.\p"
	.string "{STR_VAR_1} would follow you\n"
	.string "anywhere.$"

PrimeiraCamara_Text_ConfirmLink:
	.string "Name {STR_VAR_1} as your\n"
	.string "first link?$"

PrimeiraCamara_Text_Linked:
	.string "You speak {STR_VAR_1}'s name at\n"
	.string "the broken tie.\p"
	.string "Both ends glow together, and the\n"
	.string "light settles on {STR_VAR_1}.\p"
	.string "{STR_VAR_1} is your first link.\p"
	.string "A first link that trusts you with\n"
	.string "its whole heart holds on for you,\l"
	.string "once in every battle, when it\l"
	.string "would otherwise fall.$"

PrimeiraCamara_Text_RiteLater:
	.string "The light waits. The tie will\n"
	.string "still be here.$"

PrimeiraCamara_EventScript_Augusto::
	lockall
	msgbox PrimeiraCamara_Text_Augusto, MSGBOX_DEFAULT
	goto_if_unset FLAG_ARAUNA_FIRST_LINK_MADE, PrimeiraCamara_AugustoEnd
	msgbox PrimeiraCamara_Text_AugustoLinked, MSGBOX_DEFAULT
PrimeiraCamara_AugustoEnd:
	releaseall
	end

PrimeiraCamara_Text_AugustoLinked:
	.string "Below his name the stone is warm,\n"
	.string "as if someone had just spoken.$"

PrimeiraCamara_Text_Augusto:
	.string "One name on the stone: AUGUSTO.\p"
	.string "What binds us stays.$"

PrimeiraCamara_EventScript_Memory::
	msgbox PrimeiraCamara_Text_Memory, MSGBOX_SIGN
	end

PrimeiraCamara_Text_Memory:
	.string "Remembering is an act of connection,\n"
	.string "not of ownership.$"
