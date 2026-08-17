PacifidlogTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PacifidlogTown_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, PacifidlogTown_OnResume
	.byte 0

PacifidlogTown_OnTransition:
	setflag FLAG_VISITED_PACIFIDLOG_TOWN
	end

PacifidlogTown_OnResume:
	setstepcallback STEP_CB_PACIFIDLOG_BRIDGE
	end

PacifidlogTown_EventScript_NinjaBoy::
	msgbox PacifidlogTown_Text_NeatHousesOnWater, MSGBOX_NPC
	end

PacifidlogTown_EventScript_Girl::
	msgbox PacifidlogTown_Text_FastRunningCurrent, MSGBOX_NPC
	end

PacifidlogTown_EventScript_Fisherman::
	msgbox PacifidlogTown_Text_SkyPillarTooScary, MSGBOX_NPC
	end

PacifidlogTown_EventScript_TownSign::
	msgbox PacifidlogTown_Text_TownSign, MSGBOX_SIGN
	end

PacifidlogTown_Text_FastRunningCurrent:
	.string "O HORIZONTE consertou a estrada\ndaqui. Nao sei se isso torna\p"
	.string "mais facil perguntar o que\nexiste debaixo dela.$"

PacifidlogTown_Text_NeatHousesOnWater:
	.string "Voce vai continuar mesmo\nsabendo que CASA DA FOGUEIRA\p"
	.string "guarda partes da historia que\nmuita gente preferia deixar\p"
	.string "enterradas?$"

PacifidlogTown_Text_SkyPillarTooScary:
	.string "Aqui historias sao repetidas\npara continuar vivas, nao para\p"
	.string "permanecer identicas.$"

PacifidlogTown_Text_TownSign:
	.string "CASA DA FOGUEIRA. Aqui\nhistorias sao repetidas para\p"
	.string "continuar vivas, nao para\npermanecer identicas.$"

