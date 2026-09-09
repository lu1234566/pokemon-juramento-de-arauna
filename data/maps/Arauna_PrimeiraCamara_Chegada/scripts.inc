Arauna_PrimeiraCamara_Chegada_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, PrimeiraCamara_Chegada_OnLoad
	.byte 0

PrimeiraCamara_Chegada_OnLoad:
	call_if_set FLAG_ARAUNA_FIRST_CHAMBER_OPEN, PrimeiraCamara_OpenTiles
	end

PrimeiraCamara_EventScript_Door::
	lockall
	goto_if_set FLAG_ARAUNA_FIRST_CHAMBER_OPEN, PrimeiraCamara_DoorAlreadyOpen
	goto_if_unset FLAG_ARAUNA_FIRST_CHAMBER_DOOR_SEEN, PrimeiraCamara_DoorFirstSeen
	goto_if_unset FLAG_BADGE01_GET, PrimeiraCamara_DoorLocked
	goto_if_unset FLAG_BADGE02_GET, PrimeiraCamara_DoorLocked
	setflag FLAG_ARAUNA_FIRST_CHAMBER_OPEN
	call PrimeiraCamara_OpenTiles
	special DrawWholeMapView
	playse SE_DOOR
	msgbox PrimeiraCamara_Text_Opened, MSGBOX_DEFAULT
	releaseall
	end

PrimeiraCamara_DoorFirstSeen:
	setflag FLAG_ARAUNA_FIRST_CHAMBER_DOOR_SEEN
	msgbox PrimeiraCamara_Text_FirstSeen, MSGBOX_DEFAULT
	releaseall
	end

PrimeiraCamara_DoorLocked:
	msgbox PrimeiraCamara_Text_Locked, MSGBOX_DEFAULT
	releaseall
	end

PrimeiraCamara_DoorAlreadyOpen:
	msgbox PrimeiraCamara_Text_AlreadyOpen, MSGBOX_DEFAULT
	releaseall
	end

PrimeiraCamara_OpenTiles:
	setmetatile 14, 7, 583, TRUE
	setmetatile 15, 7, 584, TRUE
	setmetatile 14, 8, 587, FALSE
	setmetatile 15, 8, 588, FALSE
	return

PrimeiraCamara_Text_FirstSeen:
	.string "Duas marcas fecham a passagem:\n"
	.string "MARE e TERRA.\p"
	.string "A pedra guarda o sinal\n"
	.string "da sua visita.$"

PrimeiraCamara_Text_Locked:
	.string "A porta ainda esta selada.\p"
	.string "Faltam as conquistas das\n"
	.string "Casas da Mare e da Terra.$"

PrimeiraCamara_Text_Opened:
	.string "As duas marcas respondem.\p"
	.string "A passagem se abre diante\n"
	.string "do nucleo azul.$"

PrimeiraCamara_Text_AlreadyOpen:
	.string "A passagem permanece aberta.$"

PrimeiraCamara_EventScript_Mare::
	msgbox PrimeiraCamara_Text_Mare, MSGBOX_SIGN
	end

PrimeiraCamara_Text_Mare:
	.string "MARE: as historias chegam\n"
	.string "de muitas margens.$"

PrimeiraCamara_EventScript_Terra::
	msgbox PrimeiraCamara_Text_Terra, MSGBOX_SIGN
	end

PrimeiraCamara_Text_Terra:
	.string "TERRA: os nomes permanecem\n"
	.string "onde alguem os recorda.$"
