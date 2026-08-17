PacifidlogTown_House2_MapScripts::
	.byte 0

PacifidlogTown_House2_EventScript_FanClubYoungerBrother::
	lock
	faceplayer
	dotimebasedevents
	call PacifidlogTown_House2_EventScript_UpdateFanClubTMFlag
	goto_if_set FLAG_RECEIVED_FANCLUB_TM_THIS_WEEK, PacifidlogTown_House2_EventScript_ComeBackInXDays
	call_if_set FLAG_MET_FANCLUB_YOUNGER_BROTHER, PacifidlogTown_House2_EventScript_MonAssessment
	call_if_unset FLAG_MET_FANCLUB_YOUNGER_BROTHER, PacifidlogTown_House2_EventScript_FirstMonAssessment
	setflag FLAG_MET_FANCLUB_YOUNGER_BROTHER
	specialvar VAR_RESULT, GetLeadMonFriendshipScore
	goto_if_ge VAR_RESULT, FRIENDSHIP_150_TO_199, PacifidlogTown_House2_EventScript_GiveReturn
	specialvar VAR_RESULT, GetLeadMonFriendshipScore
	goto_if_ge VAR_RESULT, FRIENDSHIP_50_TO_99, PacifidlogTown_House2_EventScript_PutInEffort
	goto PacifidlogTown_House2_EventScript_GiveFrustration
	end

PacifidlogTown_House2_EventScript_UpdateFanClubTMFlag::
	goto_if_unset FLAG_RECEIVED_FANCLUB_TM_THIS_WEEK, Common_EventScript_NopReturn
	specialvar VAR_RESULT, GetDaysUntilPacifidlogTMAvailable
	call_if_eq VAR_RESULT, 0, PacifidlogTown_House2_EventScript_ClearReceivedFanClubTM
	return

PacifidlogTown_House2_EventScript_MonAssessment::
	msgbox PacifidlogTown_House2_Text_AhYourPokemon, MSGBOX_DEFAULT
	return

PacifidlogTown_House2_EventScript_FirstMonAssessment::
	msgbox PacifidlogTown_House2_Text_ChairmansYoungerBrotherOnVacation, MSGBOX_DEFAULT
	msgbox PacifidlogTown_House2_Text_AhYourPokemon, MSGBOX_DEFAULT
	return

PacifidlogTown_House2_EventScript_ClearReceivedFanClubTM::
	clearflag FLAG_RECEIVED_FANCLUB_TM_THIS_WEEK
	return

PacifidlogTown_House2_EventScript_GiveReturn::
	msgbox PacifidlogTown_House2_Text_AdoringPokemonTakeThis, MSGBOX_DEFAULT
	giveitem ITEM_TM_RETURN
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_FANCLUB_TM_THIS_WEEK
	special SetPacifidlogTMReceivedDay
	msgbox PacifidlogTown_House2_Text_ExplainReturnFrustration, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_House2_EventScript_PutInEffort::
	msgbox PacifidlogTown_House2_Text_PutInSomeMoreEffort, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_House2_EventScript_GiveFrustration::
	msgbox PacifidlogTown_House2_Text_ViciousPokemonTakeThis, MSGBOX_DEFAULT
	giveitem ITEM_TM_FRUSTRATION
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_FANCLUB_TM_THIS_WEEK
	special SetPacifidlogTMReceivedDay
	msgbox PacifidlogTown_House2_Text_ExplainReturnFrustration, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_House2_EventScript_ComeBackInXDays::
	specialvar VAR_RESULT, GetDaysUntilPacifidlogTMAvailable
	buffernumberstring STR_VAR_1, VAR_RESULT
	msgbox PacifidlogTown_House2_Text_GetGoodTMInXDays, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_House2_EventScript_HappyAzurill::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_AZURILL, CRY_MODE_NORMAL
	msgbox PacifidlogTown_House2_Text_Rurii, MSGBOX_DEFAULT
	waitmoncry
	msgbox PacifidlogTown_House2_Text_VeryFriendlyWithTrainer, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_House2_EventScript_UnhappyAzurill::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_AZURILL, CRY_MODE_ENCOUNTER
	msgbox PacifidlogTown_House2_Text_Rururi, MSGBOX_DEFAULT
	waitmoncry
	msgbox PacifidlogTown_House2_Text_DoesntLikeTrainerVeryMuch, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_House2_Text_ChairmansYoungerBrotherOnVacation:
	.string "Tem gente que chama de\nDESENCANTO. Eu chamava de\p"
	.string "distraicao, ate minha mae\nesquecer a cancao que cantava\p"
	.string "desde crianca.$"

PacifidlogTown_House2_Text_AhYourPokemon:
	.string "Meu avo dizia que lembrar\ntambem cansa. Mas escolher pelo\p"
	.string "outro o que ele deve esquecer\nparece pior.$"

PacifidlogTown_House2_Text_AdoringPokemonTakeThis:
	.string "Voce vai continuar mesmo\nsabendo que CASA DA FOGUEIRA\p"
	.string "guarda partes da historia que\nmuita gente preferia deixar\p"
	.string "enterradas?$"

PacifidlogTown_House2_Text_PutInSomeMoreEffort:
	.string "Dona Zila diz que uma historia\nmuda toda vez que e contada.\p"
	.string "Talvez seja por isso que ainda\nesta viva.$"

PacifidlogTown_House2_Text_ViciousPokemonTakeThis:
	.string "Ultimamente alguns Pokemon\nparam diante de suas antigas\p"
	.string "casas como se nunca tivessem\nestado ali.$"

PacifidlogTown_House2_Text_ExplainReturnFrustration:
	.string "Existem placas novas por toda\nparte. Curioso e que alguns\p"
	.string "nomes antigos desapareceram\nquando elas chegaram.$"

PacifidlogTown_House2_Text_GetGoodTMInXDays:
	.string "Oh, yes. In about {STR_VAR_1} or so days,\n"
	.string "I should be getting a good TM or two.\p"
	.string "You should come see me then.\n"
	.string "I'll give you a TM that's suitable for\l"
	.string "your POKéMON.$"

PacifidlogTown_House2_Text_Rurii:
	.string "O HORIZONTE consertou a estrada\ndaqui. Nao sei se isso torna\p"
	.string "mais facil perguntar o que\nexiste debaixo dela.$"

PacifidlogTown_House2_Text_VeryFriendlyWithTrainer:
	.string "Existem placas novas por toda\nparte. Curioso e que alguns\p"
	.string "nomes antigos desapareceram\nquando elas chegaram.$"

PacifidlogTown_House2_Text_Rururi:
	.string "Dona Zila diz que uma historia\nmuda toda vez que e contada.\p"
	.string "Talvez seja por isso que ainda\nesta viva.$"

PacifidlogTown_House2_Text_DoesntLikeTrainerVeryMuch:
	.string "Ultimamente alguns Pokemon\nparam diante de suas antigas\p"
	.string "casas como se nunca tivessem\nestado ali.$"

