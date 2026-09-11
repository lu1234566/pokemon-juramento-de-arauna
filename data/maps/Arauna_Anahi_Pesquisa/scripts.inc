Arauna_Anahi_Pesquisa_MapScripts::
	.byte 0

AnahiPesquisa_EventScript_Records::
	msgbox AnahiPesquisa_Text_Records, MSGBOX_SIGN
	end

AnahiPesquisa_Text_Records:
	.string "Field notebooks gather maps, drawings\n"
	.string "and notes from all over Arauna.$"

AnahiPesquisa_EventScript_Specimens::
	msgbox AnahiPesquisa_Text_Specimens, MSGBOX_SIGN
	end

AnahiPesquisa_Text_Specimens:
	.string "The samples are labeled with the place\n"
	.string "they were collected.$"

AnahiPesquisa_EventScript_Computer::
	msgbox AnahiPesquisa_Text_Computer, MSGBOX_SIGN
	end

AnahiPesquisa_Text_Computer:
	.string "The computer keeps the records of the\n"
	.string "lab's expeditions in order.$"
