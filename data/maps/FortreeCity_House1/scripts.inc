FortreeCity_House1_MapScripts::
	.byte 0

FortreeCity_House1_EventScript_Trader::
	lock
	faceplayer
	goto_if_set FLAG_FORTREE_NPC_TRADE_COMPLETED, FortreeCity_House1_EventScript_TradeCompleted
	setvar VAR_0x8008, INGAME_TRADE_PLUSLE
	copyvar VAR_0x8004, VAR_0x8008
	specialvar VAR_RESULT, GetInGameTradeSpeciesInfo
	copyvar VAR_0x8009, VAR_RESULT
	msgbox FortreeCity_House1_Text_YouWillTradeWontYou, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FortreeCity_House1_EventScript_DeclineTrade
	special ChoosePartyMon
	copyvar VAR_0x800A, VAR_0x8004
	goto_if_eq VAR_0x8004, PARTY_NOTHING_CHOSEN, FortreeCity_House1_EventScript_DeclineTrade
	copyvar VAR_0x8005, VAR_0x800A
	specialvar VAR_RESULT, GetTradeSpecies
	copyvar VAR_0x800B, VAR_RESULT
	goto_if_ne VAR_RESULT, VAR_0x8009, FortreeCity_House1_EventScript_NotRequestedMon
	copyvar VAR_0x8004, VAR_0x8008
	copyvar VAR_0x8005, VAR_0x800A
	special CreateInGameTradePokemon
	special DoInGameTradeScene
	bufferspeciesname STR_VAR_1, VAR_0x8009
	msgbox FortreeCity_House1_Text_MonYouTakeCare, MSGBOX_DEFAULT
	setflag FLAG_FORTREE_NPC_TRADE_COMPLETED
	release
	end

FortreeCity_House1_EventScript_DeclineTrade::
	msgbox FortreeCity_House1_Text_YouWontTradeMe, MSGBOX_DEFAULT
	release
	end

FortreeCity_House1_EventScript_NotRequestedMon::
	bufferspeciesname STR_VAR_1, VAR_0x8009
	msgbox FortreeCity_House1_Text_ThisIsntAMon, MSGBOX_DEFAULT
	release
	end

FortreeCity_House1_EventScript_TradeCompleted::
	msgbox FortreeCity_House1_Text_GoingToMakeVolbeatStrong, MSGBOX_DEFAULT
	release
	end

FortreeCity_House1_EventScript_ExpertF::
	msgbox FortreeCity_House1_Text_TradingMemoriesWithOthers, MSGBOX_NPC
	end

FortreeCity_House1_EventScript_Zigzagoon::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ZIGZAGOON, CRY_MODE_NORMAL
	msgbox FortreeCity_House1_Text_Zigzagoon, MSGBOX_DEFAULT
	waitmoncry
	release
	end

FortreeCity_House1_Text_YouWillTradeWontYou:
	.string "Wrooooaaar! I need it!\n"
	.string "I have to get me a {STR_VAR_1}!\l"
	.string "I'll do anything for it!\p"
	.string "…Uh… Did you hear that?\n"
	.string "My shout from the bottom of my heart?\p"
	.string "Having heard that, you will trade\n"
	.string "your {STR_VAR_1} for my {STR_VAR_2},\l"
	.string "won't you?$"

FortreeCity_House1_Text_MonYouTakeCare:
	.string "Existem placas novas por toda\nparte. Curioso e que alguns\p"
	.string "nomes antigos desapareceram\nquando elas chegaram.$"

FortreeCity_House1_Text_ThisIsntAMon:
	.string "Meu avo dizia que lembrar\ntambem cansa. Mas escolher pelo\p"
	.string "outro o que ele deve esquecer\nparece pior.$"

FortreeCity_House1_Text_YouWontTradeMe:
	.string "No? You won't trade me?\n"
	.string "Even after I bared my heart to you?$"

FortreeCity_House1_Text_GoingToMakeVolbeatStrong:
	.string "Meu avo dizia que lembrar\ntambem cansa. Mas escolher pelo\p"
	.string "outro o que ele deve esquecer\nparece pior.$"

FortreeCity_House1_Text_TradingMemoriesWithOthers:
	.string "Tem gente que chama de\nDESENCANTO. Eu chamava de\p"
	.string "distraicao, ate minha mae\nesquecer a cancao que cantava\p"
	.string "desde crianca.$"

FortreeCity_House1_Text_Zigzagoon:
	.string "Voce vai continuar mesmo\nsabendo que MATA DO MEIO guarda\p"
	.string "partes da historia que muita\ngente preferia deixar\p"
	.string "enterradas?$"

