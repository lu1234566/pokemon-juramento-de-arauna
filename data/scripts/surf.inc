EventScript_UseSurf::
	goto_if_set FLAG_ARAUNA_BOARD_FIELD_UNLOCKED, EventScript_UseTideBoard
	checkfieldmove FIELD_MOVE_SURF
	goto_if_eq VAR_RESULT, PARTY_SIZE, EventScript_EndUseSurf
	bufferpartymonnick STR_VAR_1, VAR_RESULT
	setfieldeffectargument 0, VAR_RESULT
	lockall
	msgbox gText_WantToUseSurf, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ReleaseUseSurf
	msgbox gText_PlayerUsedSurf, MSGBOX_DEFAULT
	dofieldeffect FLDEFF_USE_SURF
EventScript_ReleaseUseSurf::
	releaseall
EventScript_EndUseSurf::
	end

EventScript_UseTideBoard::
	setfieldeffectargument 0, 0
	lockall
	msgbox AraunaText_WantToUseTideBoard, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ReleaseUseSurf
	msgbox AraunaText_PlayerUsedTideBoard, MSGBOX_DEFAULT
	dofieldeffect FLDEFF_USE_SURF
	goto EventScript_ReleaseUseSurf

AraunaText_WantToUseTideBoard:
	.string "The water is calm enough for\n"
	.string "the TIDE BOARD.\p"
	.string "Cross the channel?$"

AraunaText_PlayerUsedTideBoard:
	.string "{PLAYER} unfolded the TIDE BOARD.\p"
	.string "The lead partner steadied the\n"
	.string "first push into the current.$"

EventScript_CurrentTooFast::
	lockall
	checkfieldmove FIELD_MOVE_SURF
	goto_if_eq VAR_RESULT, FALSE, EventScript_CurrentTooFastEndMsg
	playse SE_SELECT
	msgbox Text_CurrentTooFast
EventScript_CurrentTooFastEndMsg::
	releaseall
	end
