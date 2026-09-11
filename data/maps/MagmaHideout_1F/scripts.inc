MagmaHideout_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MagmaHideout_1F_OnTransition
	.byte 0

MagmaHideout_1F_OnTransition:
	setvar VAR_JAGGED_PASS_ASH_WEATHER, 0
	end

MagmaHideout_1F_EventScript_Grunt1::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_1, MagmaHideout_1F_Text_Grunt1Intro, MagmaHideout_1F_Text_Grunt1Defeat
	msgbox MagmaHideout_1F_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_1F_EventScript_Grunt2::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_2, MagmaHideout_1F_Text_Grunt2Intro, MagmaHideout_1F_Text_Grunt2Defeat
	msgbox MagmaHideout_1F_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_1F_Text_Grunt1Intro:
	.string "REMEMBRANCER: Guardar um nome pode\n"
	.string "ser resistencia. Obrigar alguem\p"
	.string "a reviver tudo tambem pode ser\n"
	.string "violencia.$"

MagmaHideout_1F_Text_Grunt1Defeat:
	.string "REMEMBRANCER: O HORIZON quer uma\n"
	.string "Arauna estavel. Eu quero uma\p"
	.string "Arauna que saiba por que suas\n"
	.string "ruinas existem.$"

MagmaHideout_1F_Text_Grunt1PostBattle:
	.string "REMEMBRANCER: Se uma historia\n"
	.string "incomoda quem manda, ela vira\p"
	.string "'ruido', depois 'trauma',\n"
	.string "depois desaparece do registro.$"

MagmaHideout_1F_Text_Grunt2Intro:
	.string "REMEMBRANCER: Se uma historia\n"
	.string "incomoda quem manda, ela vira\p"
	.string "'ruido', depois 'trauma',\n"
	.string "depois desaparece do registro.$"

MagmaHideout_1F_Text_Grunt2Defeat:
	.string "REMEMBRANCER: LUZIA diz que\n"
	.string "memoria devolvida sem permissao\p"
	.string "ainda e melhor que memoria\n"
	.string "roubada. Nem todos aqui\p"
	.string "concordam com essa parte.$"

MagmaHideout_1F_Text_Grunt2PostBattle:
	.string "REMEMBRANCER: Se uma historia\n"
	.string "incomoda quem manda, ela vira\p"
	.string "'ruido', depois 'trauma',\n"
	.string "depois desaparece do registro.$"

