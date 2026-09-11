Arauna_CasaFogueira_Entrada_MapScripts::
	.byte 0

Arauna_CasaFogueira_Entrada_EventScript_Notice::
	msgbox Arauna_CasaFogueira_Entrada_Text_Notice, MSGBOX_SIGN
	end

Arauna_CasaFogueira_Entrada_Text_Notice:
	.string "CASA DA FOGUEIRA\n"
	.string "The door is open to the community.$"

Arauna_CasaFogueira_Entrada_EventScript_GuestBook::
	msgbox Arauna_CasaFogueira_Entrada_Text_GuestBook, MSGBOX_SIGN
	end

Arauna_CasaFogueira_Entrada_Text_GuestBook:
	.string "Names fill the guest book.\n"
	.string "There is room for another page.$"

Arauna_CasaFogueira_Entrada_EventScript_Welcome::
	msgbox Arauna_CasaFogueira_Entrada_Text_Welcome, MSGBOX_SIGN
	end

Arauna_CasaFogueira_Entrada_Text_Welcome:
	.string "Come in and rest for a while.\n"
	.string "The hall is just beyond this room.$"
