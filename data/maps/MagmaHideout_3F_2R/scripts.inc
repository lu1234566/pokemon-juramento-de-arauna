MagmaHideout_3F_2R_MapScripts::
	.byte 0

MagmaHideout_3F_2R_EventScript_Grunt10::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_10, MagmaHideout_3F_2R_Text_Grunt10Intro, MagmaHideout_3F_2R_Text_Grunt10Defeat
	msgbox MagmaHideout_3F_2R_Text_Grunt10PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_3F_2R_Text_Grunt10Intro:
	.string "LEMBRANTE: LUZIA diz que\nmemoria devolvida sem permissao\p"
	.string "ainda e melhor que memoria\nroubada. Nem todos aqui\p"
	.string "concordam com essa parte.$"

MagmaHideout_3F_2R_Text_Grunt10Defeat:
	.string "LEMBRANTE: O HORIZONTE quer uma\nArauna estavel. Eu quero uma\p"
	.string "Arauna que saiba por que suas\nruinas existem.$"

MagmaHideout_3F_2R_Text_Grunt10PostBattle:
	.string "LEMBRANTE: Se uma historia\nincomoda quem manda, ela vira\p"
	.string "'ruido', depois 'trauma',\ndepois desaparece do registro.$"

