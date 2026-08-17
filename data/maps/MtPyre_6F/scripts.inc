MtPyre_6F_MapScripts::
	.byte 0

MtPyre_6F_EventScript_Valerie::
	trainerbattle_single TRAINER_VALERIE_1, MtPyre_6F_Text_ValerieIntro, MtPyre_6F_Text_ValerieDefeat, MtPyre_6F_EventScript_RegisterValerie
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, MtPyre_6F_EventScript_RematchValerie
	msgbox MtPyre_6F_Text_ValeriePostBattle, MSGBOX_DEFAULT
	release
	end

MtPyre_6F_EventScript_RegisterValerie::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox MtPyre_6F_Text_ValerieRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_VALERIE_1
	release
	end

MtPyre_6F_EventScript_RematchValerie::
	trainerbattle_rematch TRAINER_VALERIE_1, MtPyre_6F_Text_ValerieRematchIntro, MtPyre_6F_Text_ValerieRematchDefeat
	msgbox MtPyre_6F_Text_ValeriePostRematch, MSGBOX_AUTOCLOSE
	end

MtPyre_6F_EventScript_Cedric::
	trainerbattle_single TRAINER_CEDRIC, MtPyre_6F_Text_CedricIntro, MtPyre_6F_Text_CedricDefeat
	msgbox MtPyre_6F_Text_CedricPostBattle, MSGBOX_AUTOCLOSE
	end

MtPyre_6F_Text_ValerieIntro:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

MtPyre_6F_Text_ValerieDefeat:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

MtPyre_6F_Text_ValeriePostBattle:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

MtPyre_6F_Text_ValerieRegister:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

MtPyre_6F_Text_ValerieRematchIntro:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

MtPyre_6F_Text_ValerieRematchDefeat:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

MtPyre_6F_Text_ValeriePostRematch:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

MtPyre_6F_Text_CedricIntro:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

MtPyre_6F_Text_CedricDefeat:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

MtPyre_6F_Text_CedricPostBattle:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

