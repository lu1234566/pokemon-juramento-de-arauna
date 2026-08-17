PacifidlogTown_House4_MapScripts::
	.byte 0

PacifidlogTown_House4_EventScript_LittleGirl::
	msgbox PacifidlogTown_House4_Text_SkyPokemon, MSGBOX_NPC
	end

PacifidlogTown_House4_EventScript_Woman::
	msgbox PacifidlogTown_House4_Text_PeopleSawHighFlyingPokemon, MSGBOX_NPC
	end

PacifidlogTown_House4_EventScript_Boy::
	lock
	faceplayer
	msgbox PacifidlogTown_House4_Text_WhereDidYouComeFrom, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, PacifidlogTown_House4_EventScript_Yes
	goto_if_eq VAR_RESULT, NO, PacifidlogTown_House4_EventScript_No
	end

PacifidlogTown_House4_EventScript_Yes::
	msgbox PacifidlogTown_House4_Text_YesTown, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_House4_EventScript_No::
	msgbox PacifidlogTown_House4_Text_YouHaveToComeFromSomewhere, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_House4_Text_PeopleSawHighFlyingPokemon:
	.string "Voce vai continuar mesmo\nsabendo que CASA DA FOGUEIRA\p"
	.string "guarda partes da historia que\nmuita gente preferia deixar\p"
	.string "enterradas?$"

PacifidlogTown_House4_Text_SkyPokemon:
	.string "O HORIZONTE consertou a estrada\ndaqui. Nao sei se isso torna\p"
	.string "mais facil perguntar o que\nexiste debaixo dela.$"

PacifidlogTown_House4_Text_WhereDidYouComeFrom:
	.string "Voce vai continuar mesmo\nsabendo que CASA DA FOGUEIRA\p"
	.string "guarda partes da historia que\nmuita gente preferia deixar\p"
	.string "enterradas?$"

PacifidlogTown_House4_Text_YesTown:
	.string "Voce vai continuar mesmo\nsabendo que CASA DA FOGUEIRA\p"
	.string "guarda partes da historia que\nmuita gente preferia deixar\p"
	.string "enterradas?$"

PacifidlogTown_House4_Text_YouHaveToComeFromSomewhere:
	.string "Voce vai continuar mesmo\nsabendo que CASA DA FOGUEIRA\p"
	.string "guarda partes da historia que\nmuita gente preferia deixar\p"
	.string "enterradas?$"

