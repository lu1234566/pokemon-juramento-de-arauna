Arauna_CasaFogueira_Memorial_MapScripts::
	.byte 0

Arauna_CasaFogueira_Memorial_EventScript_Portraits::
	msgbox Arauna_CasaFogueira_Memorial_Text_Portraits, MSGBOX_SIGN
	end

Arauna_CasaFogueira_Memorial_Text_Portraits:
	.string "Portraits share the wooden wall.\n"
	.string "Each frame has been cared for.$"

Arauna_CasaFogueira_Memorial_EventScript_Letters::
	lockall
	goto_if_set FLAG_ARAUNA_FOGUEIRA_MEMORIAL_READ, Arauna_CasaFogueira_Memorial_EventScript_LettersReturn
	msgbox Arauna_CasaFogueira_Memorial_Text_Letters, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Arauna_CasaFogueira_Memorial_EventScript_LettersDeferred
	msgbox Arauna_CasaFogueira_Memorial_Text_Letter, MSGBOX_DEFAULT
	setflag FLAG_ARAUNA_FOGUEIRA_MEMORIAL_READ
	releaseall
	end

Arauna_CasaFogueira_Memorial_EventScript_LettersReturn::
	msgbox Arauna_CasaFogueira_Memorial_Text_Letter, MSGBOX_DEFAULT
	releaseall
	end

Arauna_CasaFogueira_Memorial_EventScript_LettersDeferred::
	msgbox Arauna_CasaFogueira_Memorial_Text_LettersDeferred, MSGBOX_DEFAULT
	releaseall
	end

Arauna_CasaFogueira_Memorial_Text_Letters:
	.string "Letters rest by an open book.\n"
	.string "Read a letter left for visitors?$"

Arauna_CasaFogueira_Memorial_Text_Letter:
	.string "A note beside the letter says:\n"
	.string "You may read this one aloud.\p"
	.string "We kept your place at the table.\n"
	.string "Not because we forgot you left.\p"
	.string "Because a place can hold a name\n"
	.string "when a voice cannot say it yet.\p"
	.string "The letter has no signature.$"

Arauna_CasaFogueira_Memorial_Text_LettersDeferred:
	.string "You leave the pages as they are.\n"
	.string "There is no hurry.$"

Arauna_CasaFogueira_Memorial_EventScript_Memory::
	msgbox Arauna_CasaFogueira_Memorial_Text_Memory, MSGBOX_SIGN
	end

Arauna_CasaFogueira_Memorial_Text_Memory:
	.string "A room set aside for memory.$"
