Route111_OldLadysRestStop_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route111_OldLadysRestStop_OnTransition
	.byte 0

Route111_OldLadysRestStop_OnTransition:
	setflag FLAG_LANDMARK_OLD_LADY_REST_SHOP
	end

Route111_OldLadysRestStop_EventScript_OldLady::
	lock
	faceplayer
	msgbox Route111_OldLadysRestStop_Text_RestUpHere, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Route111_OldLadysRestStop_EventScript_Rest
	goto_if_eq VAR_RESULT, NO, Route111_OldLadysRestStop_EventScript_DeclineRest
	end

Route111_OldLadysRestStop_EventScript_Rest::
	msgbox Route111_OldLadysRestStop_Text_TakeYourTimeRestUp, MSGBOX_DEFAULT
	closemessage
	call Common_EventScript_OutOfCenterPartyHeal
	msgbox Route111_OldLadysRestStop_Text_StillTiredTakeAnotherRest, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Route111_OldLadysRestStop_EventScript_Rest
	goto_if_eq VAR_RESULT, NO, Route111_OldLadysRestStop_EventScript_DeclineRest
	end

Route111_OldLadysRestStop_EventScript_DeclineRest::
	msgbox Route111_OldLadysRestStop_Text_DontNeedToBeShy, MSGBOX_DEFAULT
	release
	end

Route111_OldLadysRestStop_Text_RestUpHere:
	.string "Voce vai continuar mesmo\nsabendo que\p"
	.string "ROUTE111 OLDLADYSRESTSTOP\nguarda partes da historia que\p"
	.string "muita gente preferia deixar\nenterradas?$"

Route111_OldLadysRestStop_Text_TakeYourTimeRestUp:
	.string "Meu avo dizia que lembrar\ntambem cansa. Mas escolher pelo\p"
	.string "outro o que ele deve esquecer\nparece pior.$"

Route111_OldLadysRestStop_Text_StillTiredTakeAnotherRest:
	.string "Voce vai continuar mesmo\nsabendo que\p"
	.string "ROUTE111 OLDLADYSRESTSTOP\nguarda partes da historia que\p"
	.string "muita gente preferia deixar\nenterradas?$"

Route111_OldLadysRestStop_Text_DontNeedToBeShy:
	.string "Voce vai continuar mesmo\nsabendo que\p"
	.string "ROUTE111 OLDLADYSRESTSTOP\nguarda partes da historia que\p"
	.string "muita gente preferia deixar\nenterradas?$"

