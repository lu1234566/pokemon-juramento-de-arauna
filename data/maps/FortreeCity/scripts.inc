FortreeCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FortreeCity_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, FortreeCity_OnResume
	.byte 0

FortreeCity_OnTransition:
	setflag FLAG_VISITED_FORTREE_CITY
	end

FortreeCity_OnResume:
	setstepcallback STEP_CB_FORTREE_BRIDGE
	end

FortreeCity_EventScript_Man::
	msgbox FortreeCity_Text_SawGiganticPokemonInSky, MSGBOX_NPC
	end

FortreeCity_EventScript_Woman::
	lock
	faceplayer
	goto_if_set FLAG_KECLEON_FLED_FORTREE, FortreeCity_EventScript_WomanGymAccessible
	msgbox FortreeCity_Text_SomethingBlockingGym, MSGBOX_DEFAULT
	release
	end

FortreeCity_EventScript_WomanGymAccessible::
	msgbox FortreeCity_Text_ThisTimeIllBeatWinona, MSGBOX_DEFAULT
	release
	end

FortreeCity_EventScript_Girl::
	msgbox FortreeCity_Text_TreesGrowByDrinkingRainwater, MSGBOX_NPC
	end

FortreeCity_EventScript_OldMan::
	msgbox FortreeCity_Text_EveryoneHealthyAndLively, MSGBOX_NPC
	end

FortreeCity_EventScript_Boy::
	msgbox FortreeCity_Text_BugPokemonComeThroughWindow, MSGBOX_NPC
	end

FortreeCity_EventScript_GameboyKid::
	msgbox FortreeCity_Text_PokemonThatEvolveWhenTraded, MSGBOX_NPC
	end

FortreeCity_EventScript_CitySign::
	msgbox FortreeCity_Text_CitySign, MSGBOX_SIGN
	end

FortreeCity_EventScript_GymSign::
	msgbox FortreeCity_Text_GymSign, MSGBOX_SIGN
	end

FortreeCity_EventScript_Kecleon::
	lock
	faceplayer
	checkitem ITEM_DEVON_SCOPE
	goto_if_eq VAR_RESULT, TRUE, FortreeCity_EventScript_AskUseDevonScope
	msgbox FortreeCity_Text_SomethingUnseeable, MSGBOX_DEFAULT
	release
	end

FortreeCity_EventScript_AskUseDevonScope::
	msgbox FortreeCity_Text_UnseeableUseDevonScope, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, FortreeCity_EventScript_UseDevonScope
	release
	end

FortreeCity_EventScript_UseDevonScope::
	msgbox FortreeCity_Text_UsedDevonScopePokemonFled, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Movement_KecleonAppears
	waitmovement 0
	waitse
	playmoncry SPECIES_KECLEON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	applymovement VAR_LAST_TALKED, FortreeCity_Movement_KecleonFlee
	waitmovement 0
	removeobject VAR_LAST_TALKED
	setflag FLAG_KECLEON_FLED_FORTREE
	release
	end

FortreeCity_Movement_KecleonFlee:
	walk_right
	step_end

FortreeCity_Text_SawGiganticPokemonInSky:
	.string "Voce vai continuar mesmo\nsabendo que MATA DO MEIO guarda\p"
	.string "partes da historia que muita\ngente preferia deixar\p"
	.string "enterradas?$"

FortreeCity_Text_SomethingBlockingGym:
	.string "Ultimamente alguns Pokemon\nparam diante de suas antigas\p"
	.string "casas como se nunca tivessem\nestado ali.$"

FortreeCity_Text_ThisTimeIllBeatWinona:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Text_TreesGrowByDrinkingRainwater:
	.string "Os sensores registram duas\ncorrentes antigas sob Arauna:\p"
	.string "uma conserva VINCULOS; a outra\npermite que eles terminem. O\p"
	.string "Arquivo tentou transformar\nambas em ferramentas.$"

FortreeCity_Text_EveryoneHealthyAndLively:
	.string "The CITY consists of homes built on\n"
	.string "trees.\p"
	.string "Perhaps because of that lifestyle,\n"
	.string "everyone is healthy and lively.\p"
	.string "Why, even myself--I feel as if I've\n"
	.string "grown thirty years younger.$"

FortreeCity_Text_BugPokemonComeThroughWindow:
	.string "Ultimamente alguns Pokemon\nparam diante de suas antigas\p"
	.string "casas como se nunca tivessem\nestado ali.$"

FortreeCity_Text_PokemonThatEvolveWhenTraded:
	.string "There are POKéMON that evolve when\n"
	.string "you trade them! That's what I heard.$"

FortreeCity_Text_SomethingUnseeable:
	.string "Dona Zila diz que uma historia\nmuda toda vez que e contada.\p"
	.string "Talvez seja por isso que ainda\nesta viva.$"

FortreeCity_Text_UnseeableUseDevonScope:
	.string "Pokemon selvagens esquecem\nrotas, cantos e habitos\p"
	.string "passados entre geracoes.$"

FortreeCity_Text_UsedDevonScopePokemonFled:
	.string "Pokemon selvagens esquecem\nrotas, cantos e habitos\p"
	.string "passados entre geracoes.$"

FortreeCity_Text_CitySign:
	.string "MATA DO MEIO. Pokemon selvagens\nesquecem rotas, cantos e\p"
	.string "habitos passados entre\ngeracoes.$"

FortreeCity_Text_GymSign:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

