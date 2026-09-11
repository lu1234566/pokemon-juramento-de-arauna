MagmaHideout_3F_1R_MapScripts::
	.byte 0

MagmaHideout_3F_1R_EventScript_Grunt9::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_9, MagmaHideout_3F_1R_Text_Grunt9Intro, MagmaHideout_3F_1R_Text_Grunt9Defeat
	msgbox MagmaHideout_3F_1R_Text_Grunt9PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_3F_1R_EventScript_Grunt16::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_16, MagmaHideout_3F_1R_Text_Grunt16Intro, MagmaHideout_3F_1R_Text_Grunt16Defeat
	msgbox MagmaHideout_3F_1R_Text_Grunt16PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_3F_1R_Text_Grunt9Intro:
	.string "REMEMBRANCER: Guardar um nome pode\n"
	.string "ser resistencia. Obrigar alguem\p"
	.string "a reviver tudo tambem pode ser\n"
	.string "violencia.$"

MagmaHideout_3F_1R_Text_Grunt9Defeat:
	.string "REMEMBRANCER: O HORIZON quer uma\n"
	.string "Arauna estavel. Eu quero uma\p"
	.string "Arauna que saiba por que suas\n"
	.string "ruinas existem.$"

MagmaHideout_3F_1R_Text_Grunt9PostBattle:
	.string "REMEMBRANCER: Se uma historia\n"
	.string "incomoda quem manda, ela vira\p"
	.string "'ruido', depois 'trauma',\n"
	.string "depois desaparece do registro.$"

MagmaHideout_3F_1R_Text_Grunt16Intro:
	.string "REMEMBRANCER: LUZIA diz que\n"
	.string "memoria devolvida sem permissao\p"
	.string "ainda e melhor que memoria\n"
	.string "roubada. Nem todos aqui\p"
	.string "concordam com essa parte.$"

MagmaHideout_3F_1R_Text_Grunt16Defeat:
	.string "REMEMBRANCER: LUZIA diz que\n"
	.string "memoria devolvida sem permissao\p"
	.string "ainda e melhor que memoria\n"
	.string "roubada. Nem todos aqui\p"
	.string "concordam com essa parte.$"

MagmaHideout_3F_1R_Text_Grunt16PostBattle:
	.string "REMEMBRANCER: Se uma historia\n"
	.string "incomoda quem manda, ela vira\p"
	.string "'ruido', depois 'trauma',\n"
	.string "depois desaparece do registro.$"

