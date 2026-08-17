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
	.string "LEMBRANTE: Guardar um nome pode\nser resistencia. Obrigar alguem\p"
	.string "a reviver tudo tambem pode ser\nviolencia.$"

MagmaHideout_3F_1R_Text_Grunt9Defeat:
	.string "LEMBRANTE: O HORIZONTE quer uma\nArauna estavel. Eu quero uma\p"
	.string "Arauna que saiba por que suas\nruinas existem.$"

MagmaHideout_3F_1R_Text_Grunt9PostBattle:
	.string "LEMBRANTE: Se uma historia\nincomoda quem manda, ela vira\p"
	.string "'ruido', depois 'trauma',\ndepois desaparece do registro.$"

MagmaHideout_3F_1R_Text_Grunt16Intro:
	.string "LEMBRANTE: LUZIA diz que\nmemoria devolvida sem permissao\p"
	.string "ainda e melhor que memoria\nroubada. Nem todos aqui\p"
	.string "concordam com essa parte.$"

MagmaHideout_3F_1R_Text_Grunt16Defeat:
	.string "LEMBRANTE: LUZIA diz que\nmemoria devolvida sem permissao\p"
	.string "ainda e melhor que memoria\nroubada. Nem todos aqui\p"
	.string "concordam com essa parte.$"

MagmaHideout_3F_1R_Text_Grunt16PostBattle:
	.string "LEMBRANTE: Se uma historia\nincomoda quem manda, ela vira\p"
	.string "'ruido', depois 'trauma',\ndepois desaparece do registro.$"

