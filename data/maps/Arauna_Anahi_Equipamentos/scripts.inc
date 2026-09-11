Arauna_Anahi_Equipamentos_MapScripts::
	.byte 0

AnahiEquipamentos_EventScript_Machines::
	msgbox AnahiEquipamentos_Text_Machines, MSGBOX_SIGN
	end

AnahiEquipamentos_Text_Machines:
	.string "Clean, calibrated instruments, ready\n"
	.string "for the next survey.$"

AnahiEquipamentos_EventScript_Supplies::
	msgbox AnahiEquipamentos_Text_Supplies, MSGBOX_SIGN
	end

AnahiEquipamentos_Text_Supplies:
	.string "Materials and tools are sorted by what\n"
	.string "they're for.$"

AnahiEquipamentos_EventScript_Notes::
	msgbox AnahiEquipamentos_Text_Notes, MSGBOX_SIGN
	end

AnahiEquipamentos_Text_Notes:
	.string "Every piece of equipment has a\n"
	.string "conservation and maintenance record.$"
