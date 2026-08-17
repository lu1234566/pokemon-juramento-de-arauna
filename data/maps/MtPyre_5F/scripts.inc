MtPyre_5F_MapScripts::
	.byte 0

@ Seems like the scripts for the 4F and 5F were swapped

MtPyre_4F_EventScript_Tasha::
	trainerbattle_single TRAINER_TASHA, MtPyre_4F_Text_TashaIntro, MtPyre_4F_Text_TashaDefeat
	msgbox MtPyre_4F_Text_TashaPostBattle, MSGBOX_AUTOCLOSE
	end

MtPyre_4F_Text_TashaIntro:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

MtPyre_4F_Text_TashaDefeat:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

MtPyre_4F_Text_TashaPostBattle:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

