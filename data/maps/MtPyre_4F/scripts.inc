MtPyre_4F_MapScripts::
	.byte 0

@ Seems like the scripts for the 4F and 5F were swapped

MtPyre_5F_EventScript_Atsushi::
	trainerbattle_single TRAINER_ATSUSHI, MtPyre_5F_Text_AtsushiIntro, MtPyre_5F_Text_AtsushiDefeat
	msgbox MtPyre_5F_Text_AtsushiPostBattle, MSGBOX_AUTOCLOSE
	end

MtPyre_5F_Text_AtsushiIntro:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

MtPyre_5F_Text_AtsushiDefeat:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

MtPyre_5F_Text_AtsushiPostBattle:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

