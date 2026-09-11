MagmaHideout_3F_2R_MapScripts::
	.byte 0

MagmaHideout_3F_2R_EventScript_Grunt10::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_10, MagmaHideout_3F_2R_Text_Grunt10Intro, MagmaHideout_3F_2R_Text_Grunt10Defeat
	msgbox MagmaHideout_3F_2R_Text_Grunt10PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_3F_2R_Text_Grunt10Intro:
	.string "REMEMBRANCER: LUZIA diz que\n"
	.string "memoria devolvida sem permissao\p"
	.string "ainda e melhor que memoria\n"
	.string "roubada. Nem todos aqui\p"
	.string "concordam com essa parte.$"

MagmaHideout_3F_2R_Text_Grunt10Defeat:
	.string "REMEMBRANCER: O HORIZON quer uma\n"
	.string "Arauna estavel. Eu quero uma\p"
	.string "Arauna que saiba por que suas\n"
	.string "ruinas existem.$"

MagmaHideout_3F_2R_Text_Grunt10PostBattle:
	.string "REMEMBRANCER: Se uma historia\n"
	.string "incomoda quem manda, ela vira\p"
	.string "'ruido', depois 'trauma',\n"
	.string "depois desaparece do registro.$"

