LilycoveCity_House1_MapScripts::
	.byte 0

LilycoveCity_House1_EventScript_ExpertM::
	msgbox LilycoveCity_House1_Text_PokemonPartnersNotTools, MSGBOX_NPC
	end

LilycoveCity_House1_EventScript_Kecleon::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_KECLEON, CRY_MODE_NORMAL
	msgbox LilycoveCity_House1_Text_Kecleon, MSGBOX_DEFAULT
	waitmoncry
	release
	end

LilycoveCity_House1_Text_PokemonPartnersNotTools:
	.string "Dona Zila diz que uma historia\nmuda toda vez que e contada.\p"
	.string "Talvez seja por isso que ainda\nesta viva.$"

LilycoveCity_House1_Text_Kecleon:
	.string "Voce vai continuar mesmo\nsabendo que BAIA DAS LUZES\p"
	.string "guarda partes da historia que\nmuita gente preferia deixar\p"
	.string "enterradas?$"

