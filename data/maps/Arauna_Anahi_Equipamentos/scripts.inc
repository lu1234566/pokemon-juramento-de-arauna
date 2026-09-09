Arauna_Anahi_Equipamentos_MapScripts::
	.byte 0

AnahiEquipamentos_EventScript_Machines::
	msgbox AnahiEquipamentos_Text_Machines, MSGBOX_SIGN
	end

AnahiEquipamentos_Text_Machines:
	.string "Instrumentos limpos e calibrados\n"
	.string "prontos para a proxima pesquisa.$"

AnahiEquipamentos_EventScript_Supplies::
	msgbox AnahiEquipamentos_Text_Supplies, MSGBOX_SIGN
	end

AnahiEquipamentos_Text_Supplies:
	.string "Materiais e ferramentas\n"
	.string "estao separadas por uso.$"

AnahiEquipamentos_EventScript_Notes::
	msgbox AnahiEquipamentos_Text_Notes, MSGBOX_SIGN
	end

AnahiEquipamentos_Text_Notes:
	.string "Cada equipamento tem uma ficha\n"
	.string "de conservacao e manutencao.$"
