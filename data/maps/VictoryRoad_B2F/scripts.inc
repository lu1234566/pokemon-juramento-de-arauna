VictoryRoad_B2F_MapScripts::
	.byte 0

VictoryRoad_B2F_EventScript_Vito::
	trainerbattle_single TRAINER_VITO, VictoryRoad_B2F_Text_VitoIntro, VictoryRoad_B2F_Text_VitoDefeat
	msgbox VictoryRoad_B2F_Text_VitoPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Owen::
	trainerbattle_single TRAINER_OWEN, VictoryRoad_B2F_Text_OwenIntro, VictoryRoad_B2F_Text_OwenDefeat
	msgbox VictoryRoad_B2F_Text_OwenPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Caroline::
	trainerbattle_single TRAINER_CAROLINE, VictoryRoad_B2F_Text_CarolineIntro, VictoryRoad_B2F_Text_CarolineDefeat
	msgbox VictoryRoad_B2F_Text_CarolinePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Julie::
	trainerbattle_single TRAINER_JULIE, VictoryRoad_B2F_Text_JulieIntro, VictoryRoad_B2F_Text_JulieDefeat
	msgbox VictoryRoad_B2F_Text_JuliePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Felix::
	trainerbattle_single TRAINER_FELIX, VictoryRoad_B2F_Text_FelixIntro, VictoryRoad_B2F_Text_FelixDefeat
	msgbox VictoryRoad_B2F_Text_FelixPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Dianne::
	trainerbattle_single TRAINER_DIANNE, VictoryRoad_B2F_Text_DianneIntro, VictoryRoad_B2F_Text_DianneDefeat
	msgbox VictoryRoad_B2F_Text_DiannePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_Text_VitoIntro:
	.string "Ultimamente alguns Pokemon\nparam diante de suas antigas\p"
	.string "casas como se nunca tivessem\nestado ali.$"

VictoryRoad_B2F_Text_VitoDefeat:
	.string "Voce vai continuar mesmo\nsabendo que ESTRADA DO\p"
	.string "JURAMENTO guarda partes da\nhistoria que muita gente\p"
	.string "preferia deixar enterradas?$"

VictoryRoad_B2F_Text_VitoPostBattle:
	.string "CIRO: O futuro nao espera por\nquem vive olhando para tras.\p"
	.string "Pelo menos era nisso que eu\nacreditava.$"

VictoryRoad_B2F_Text_OwenIntro:
	.string "Voce vai continuar mesmo\nsabendo que ESTRADA DO\p"
	.string "JURAMENTO guarda partes da\nhistoria que muita gente\p"
	.string "preferia deixar enterradas?$"

VictoryRoad_B2F_Text_OwenDefeat:
	.string "Meu avo dizia que lembrar\ntambem cansa. Mas escolher pelo\p"
	.string "outro o que ele deve esquecer\nparece pior.$"

VictoryRoad_B2F_Text_OwenPostBattle:
	.string "Dona Zila diz que uma historia\nmuda toda vez que e contada.\p"
	.string "Talvez seja por isso que ainda\nesta viva.$"

VictoryRoad_B2F_Text_CarolineIntro:
	.string "Existem placas novas por toda\nparte. Curioso e que alguns\p"
	.string "nomes antigos desapareceram\nquando elas chegaram.$"

VictoryRoad_B2F_Text_CarolineDefeat:
	.string "Ultimamente alguns Pokemon\nparam diante de suas antigas\p"
	.string "casas como se nunca tivessem\nestado ali.$"

VictoryRoad_B2F_Text_CarolinePostBattle:
	.string "Meu avo dizia que lembrar\ntambem cansa. Mas escolher pelo\p"
	.string "outro o que ele deve esquecer\nparece pior.$"

VictoryRoad_B2F_Text_JulieIntro:
	.string "O HORIZONTE consertou a estrada\ndaqui. Nao sei se isso torna\p"
	.string "mais facil perguntar o que\nexiste debaixo dela.$"

VictoryRoad_B2F_Text_JulieDefeat:
	.string "Dona Zila diz que uma historia\nmuda toda vez que e contada.\p"
	.string "Talvez seja por isso que ainda\nesta viva.$"

VictoryRoad_B2F_Text_JuliePostBattle:
	.string "Tem gente que chama de\nDESENCANTO. Eu chamava de\p"
	.string "distraicao, ate minha mae\nesquecer a cancao que cantava\p"
	.string "desde crianca.$"

VictoryRoad_B2F_Text_FelixIntro:
	.string "Ultimamente alguns Pokemon\nparam diante de suas antigas\p"
	.string "casas como se nunca tivessem\nestado ali.$"

VictoryRoad_B2F_Text_FelixDefeat:
	.string "O HORIZONTE consertou a estrada\ndaqui. Nao sei se isso torna\p"
	.string "mais facil perguntar o que\nexiste debaixo dela.$"

VictoryRoad_B2F_Text_FelixPostBattle:
	.string "Tem gente que chama de\nDESENCANTO. Eu chamava de\p"
	.string "distraicao, ate minha mae\nesquecer a cancao que cantava\p"
	.string "desde crianca.$"

VictoryRoad_B2F_Text_DianneIntro:
	.string "Voce vai continuar mesmo\nsabendo que ESTRADA DO\p"
	.string "JURAMENTO guarda partes da\nhistoria que muita gente\p"
	.string "preferia deixar enterradas?$"

VictoryRoad_B2F_Text_DianneDefeat:
	.string "Tem gente que chama de\nDESENCANTO. Eu chamava de\p"
	.string "distraicao, ate minha mae\nesquecer a cancao que cantava\p"
	.string "desde crianca.$"

VictoryRoad_B2F_Text_DiannePostBattle:
	.string "Dona Zila diz que uma historia\nmuda toda vez que e contada.\p"
	.string "Talvez seja por isso que ainda\nesta viva.$"

