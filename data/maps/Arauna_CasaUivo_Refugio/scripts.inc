Arauna_CasaUivo_Refugio_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CasaUivo_Refugio_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, CasaUivo_Refugio_OnFrame
	.byte 0

@ Casa do Uivo, U06-U07 -- DRAFT (docs/ARCOS_RASCUNHO.md). With the cloth in
@ hand, the howl is a GUARACIM pup by the waterfall. It is too frightened to
@ listen until it has spent itself; then the cloth does what the notebook
@ said. Catching it is allowed and the story follows that choice too.

CasaUivo_Refugio_OnTransition:
	setvar VAR_OBJ_GFX_ID_F, ARAUNA_VIRTUAL_GFX_UIVO_PUP
	setflag FLAG_ARAUNA_UIVO_HIDE_PUP
	call_if_eq VAR_ARAUNA_UIVO_STATE, 4, CasaUivo_Refugio_ShowPup
	end

CasaUivo_Refugio_ShowPup:
	clearflag FLAG_ARAUNA_UIVO_HIDE_PUP
	return

CasaUivo_Refugio_OnFrame:
	map_script_2 VAR_TEMP_1, 0, CasaUivo_Refugio_Howl
	.2byte 0

CasaUivo_Refugio_Howl:
	setvar VAR_TEMP_1, 1
	goto_if_ne VAR_ARAUNA_UIVO_STATE, 4, CasaUivo_Refugio_End
	lockall
	playmoncry SPECIES_ODDISH, CRY_MODE_ENCOUNTER
	msgbox CasaUivo_Text_HowlHeard, MSGBOX_DEFAULT
	waitmoncry
	releaseall
CasaUivo_Refugio_End:
	end

CasaUivo_EventScript_Pup::
	lock
	faceplayer
	playmoncry SPECIES_ODDISH, CRY_MODE_ENCOUNTER
	msgbox CasaUivo_Text_PupPanics, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_ODDISH, 17
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, CasaUivo_Pup_Caught
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, CasaUivo_Pup_StillScared
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, CasaUivo_Pup_StillScared
	@ It spent itself, or bolted and came back: either way it can hear now.
	msgbox CasaUivo_Text_PupCalms, MSGBOX_DEFAULT
	playmoncry SPECIES_GLOOM, CRY_MODE_NORMAL
	waitmoncry
	msgbox CasaUivo_Text_PupAnswered, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CASA_UIVO_PUP, CasaUivo_Movement_PupGoesHome
	waitmovement 0
	removeobject LOCALID_CASA_UIVO_PUP
	setvar VAR_ARAUNA_UIVO_STATE, 5
	release
	end

CasaUivo_Pup_Caught:
	setflag FLAG_ARAUNA_UIVO_PUP_CAUGHT
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_CASA_UIVO_PUP
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox CasaUivo_Text_PupInYourCare, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_UIVO_STATE, 5
	release
	end

CasaUivo_Pup_StillScared:
	msgbox CasaUivo_Text_PupStillScared, MSGBOX_DEFAULT
	release
	end

CasaUivo_Movement_PupGoesHome:
	walk_in_place_faster_up
	walk_left
	walk_up
	step_end

CasaUivo_Text_HowlHeard:
	.string "A thin howl echoes off the rocks\n"
	.string "by the waterfall.$"

CasaUivo_Text_PupPanics:
	.string "A GUARACIM pup is pressed against\n"
	.string "the rocks, shaking.\p"
	.string "Sparks crackle in its fur. It's too\n"
	.string "frightened to hear anything!$"

CasaUivo_Text_PupCalms:
	.string "The sparks die down. The pup is\n"
	.string "worn out, still trembling.\p"
	.string "You kneel and lay the cloth on the\n"
	.string "stones, the way the notebook said.\p"
	.string "The pup sniffs it for a long time.\n"
	.string "Then it lies down on it.\p"
	.string "From high on the ridge, a deeper\n"
	.string "howl answers.$"

CasaUivo_Text_PupAnswered:
	.string "The pup lifts its head and howls\n"
	.string "back, softly this time.\p"
	.string "Then it bounds up the rocks\n"
	.string "toward the voice.\p"
	.string "You fold the cloth. A few orange\n"
	.string "hairs cling to it.$"

CasaUivo_Text_PupInYourCare:
	.string "The pup is in your care now.\p"
	.string "You tuck the cloth into your bag,\n"
	.string "beside its BALL. It will smell of\l"
	.string "home wherever you go.$"

CasaUivo_Text_PupStillScared:
	.string "The pup is still too frightened to\n"
	.string "listen. It hasn't left the rocks.$"

CasaUivo_EventScript_Refuge::
	msgbox CasaUivo_Text_Refuge, MSGBOX_SIGN
	end

CasaUivo_Text_Refuge:
	.string "Casa do Uivo\n"
	.string "A place to meet and remember.$"

CasaUivo_EventScript_Water::
	msgbox CasaUivo_Text_Water, MSGBOX_SIGN
	end

CasaUivo_Text_Water:
	.string "Water falls through the rocks.\n"
	.string "The path stays above the pool.$"

