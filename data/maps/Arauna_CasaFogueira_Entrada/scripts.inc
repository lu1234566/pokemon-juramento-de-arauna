Arauna_CasaFogueira_Entrada_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Fogueira_Entrada_OnTransition
	.byte 0

Fogueira_Entrada_OnTransition:
	setflag FLAG_ARAUNA_TOWER_HIDE_CIRO
	call_if_set FLAG_SYS_GAME_CLEAR, Fogueira_Entrada_ShowCiro
	end

Fogueira_Entrada_ShowCiro:
	clearflag FLAG_ARAUNA_TOWER_HIDE_CIRO
	return

Arauna_CasaFogueira_Entrada_EventScript_Notice::
	msgbox Arauna_CasaFogueira_Entrada_Text_Notice, MSGBOX_SIGN
	end

Arauna_CasaFogueira_Entrada_Text_Notice:
	.string "CASA DA FOGUEIRA\n"
	.string "The door is open to the community.$"

Arauna_CasaFogueira_Entrada_EventScript_GuestBook::
	goto_if_set FLAG_ARAUNA_FOGUEIRA_SHARED, Arauna_CasaFogueira_Entrada_EventScript_GuestBookReturn
	msgbox Arauna_CasaFogueira_Entrada_Text_GuestBook, MSGBOX_SIGN
	end

Arauna_CasaFogueira_Entrada_EventScript_GuestBookReturn::
	msgbox Arauna_CasaFogueira_Entrada_Text_GuestBookReturn, MSGBOX_SIGN
	end

Arauna_CasaFogueira_Entrada_Text_GuestBookReturn:
	.string "A new line marks today's circle.\n"
	.string "A letter was heard by the fire.$"

Arauna_CasaFogueira_Entrada_Text_GuestBook:
	.string "Names fill the guest book.\n"
	.string "There is room for another page.$"

Arauna_CasaFogueira_Entrada_EventScript_Welcome::
	lockall
	faceplayer
	goto_if_set FLAG_ARAUNA_FOGUEIRA_SHARED, Arauna_CasaFogueira_Entrada_EventScript_WelcomeReturn
	msgbox Arauna_CasaFogueira_Entrada_Text_Welcome, MSGBOX_SIGN
	releaseall
	end

Arauna_CasaFogueira_Entrada_EventScript_WelcomeReturn::
	msgbox Arauna_CasaFogueira_Entrada_Text_WelcomeReturn, MSGBOX_DEFAULT
	releaseall
	end

Arauna_CasaFogueira_Entrada_Text_WelcomeReturn:
	.string "Welcome back. Your place is here,\n"
	.string "even when you have no words.$"

Arauna_CasaFogueira_Entrada_Text_Welcome:
	.string "The hall is gathering to listen.\n"
	.string "You can join or just rest.\p"
	.string "The memorial is to the left.\n"
	.string "The door stays open.$"

