MtPyre_1F_MapScripts::
	.byte 0

MtPyre_1F_EventScript_CleanseTagWoman::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_CLEANSE_TAG, MtPyre_1F_EventScript_ReceivedCleanseTag
	msgbox MtPyre_1F_Text_TakeThisForYourOwnGood, MSGBOX_DEFAULT
	giveitem ITEM_CLEANSE_TAG
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_CLEANSE_TAG
	release
	end

MtPyre_1F_EventScript_ReceivedCleanseTag::
	msgbox MtPyre_1F_Text_ExplainCleanseTag, MSGBOX_DEFAULT
	release
	end

MtPyre_1F_EventScript_PokefanF::
	msgbox MtPyre_1F_Text_ComeToPayRespects, MSGBOX_NPC
	end

MtPyre_1F_EventScript_Man::
	msgbox MtPyre_1F_Text_RestingPlaceOfZigzagoon, MSGBOX_NPC
	end

MtPyre_1F_Text_TakeThisForYourOwnGood:
	.string "CIRO: O futuro nao espera por\nquem vive olhando para tras.\p"
	.string "Pelo menos era nisso que eu\nacreditava.$"

MtPyre_1F_Text_ExplainCleanseTag:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

MtPyre_1F_Text_ComeToPayRespects:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

MtPyre_1F_Text_RestingPlaceOfZigzagoon:
	.string "Os nomes de mortos e\ndesaparecidos sao mantidos\p"
	.string "aqui. O HORIZONTE comeca a\nretirar registros em nome da\p"
	.string "estabilidade.$"

