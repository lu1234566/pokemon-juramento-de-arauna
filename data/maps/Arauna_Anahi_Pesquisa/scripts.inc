Arauna_Anahi_Pesquisa_MapScripts::
	.byte 0

AnahiPesquisa_EventScript_Records::
	msgbox AnahiPesquisa_Text_Records, MSGBOX_SIGN
	end

AnahiPesquisa_Text_Records:
	.string "Cadernos de campo reunem mapas,\n"
	.string "desenhos e anotacoes de Arauna.$"

AnahiPesquisa_EventScript_Specimens::
	msgbox AnahiPesquisa_Text_Specimens, MSGBOX_SIGN
	end

AnahiPesquisa_Text_Specimens:
	.string "As amostras estao identificadas\n"
	.string "com seu local de coleta.$"

AnahiPesquisa_EventScript_Computer::
	msgbox AnahiPesquisa_Text_Computer, MSGBOX_SIGN
	end

AnahiPesquisa_Text_Computer:
	.string "O computador organiza registros\n"
	.string "das expedicoes do laboratorio.$"
