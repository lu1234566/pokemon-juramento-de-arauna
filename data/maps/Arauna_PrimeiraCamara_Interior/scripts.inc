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

PrimeiraCamara_EventScript_Augusto::
	msgbox PrimeiraCamara_Text_Augusto, MSGBOX_SIGN
	end

PrimeiraCamara_Text_Augusto:
	.string "One name on the stone: AUGUSTO.\p"
	.string "What binds us stays.$"

PrimeiraCamara_EventScript_Memory::
	msgbox PrimeiraCamara_Text_Memory, MSGBOX_SIGN
	end

PrimeiraCamara_Text_Memory:
	.string "Remembering is an act of connection,\n"
	.string "not of ownership.$"
