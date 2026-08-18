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
	.string "Treinei com toda minha familia.\n"
	.string "Nao vou perder para ninguem!$"

VictoryRoad_B2F_Text_VitoDefeat:
	.string "Melhor que toda minha familia?!\n"
	.string "Isso e possivel?!$"

VictoryRoad_B2F_Text_VitoPostBattle:
	.string "Eu era o melhor da familia\n"
	.string "e nunca tinha perdido...\p"
	.string "Acho que perdi a confianca.\n"
	.string "Talvez eu volte para casa.$"

VictoryRoad_B2F_Text_OwenIntro:
	.string "Ouvi falar de um jovem durao.\n"
	.string "Entao era voce?$"

VictoryRoad_B2F_Text_OwenDefeat:
	.string "O baixinho e forte!$"

VictoryRoad_B2F_Text_OwenPostBattle:
	.string "Entao os boatos eram verdade.\n"
	.string "Aquele jovem forte veio da\n"
	.string "VILA AMANHECER.$"

VictoryRoad_B2F_Text_CarolineIntro:
	.string "Voce deve estar ficando cansado.$"

VictoryRoad_B2F_Text_CarolineDefeat:
	.string "Nem sinal de cansaco!$"

VictoryRoad_B2F_Text_CarolinePostBattle:
	.string "A ESTRADA DO JURAMENTO e a LIGA\n"
	.string "sao desafios longos.\p"
	.string "Nao deixe o cansaco vencer.$"

VictoryRoad_B2F_Text_JulieIntro:
	.string "Nao se acomode so porque\n"
	.string "conquistou muitas INSIGNIAS.\p"
	.string "Sempre existe alguem melhor.$"

VictoryRoad_B2F_Text_JulieDefeat:
	.string "Voce e melhor do que eu!$"

VictoryRoad_B2F_Text_JuliePostBattle:
	.string "Olhe para suas INSIGNIAS e\n"
	.string "lembre dos TRAINERS que venceu.$"

VictoryRoad_B2F_Text_FelixIntro:
	.string "Cheguei longe, mas a tensao\n"
	.string "esta atacando meu estomago...$"

VictoryRoad_B2F_Text_FelixDefeat:
	.string "Ai...\n"
	.string "Isso doi...$"

VictoryRoad_B2F_Text_FelixPostBattle:
	.string "Fico tenso so de pensar que\n"
	.string "estou perto da LIGA.\p"
	.string "So consigo fingir calma.$"

VictoryRoad_B2F_Text_DianneIntro:
	.string "Os melhores chegam ate esta\n"
	.string "caverna.\p"
	.string "E entao, o que esta achando?$"

VictoryRoad_B2F_Text_DianneDefeat:
	.string "Voce nem se abalou!$"

VictoryRoad_B2F_Text_DiannePostBattle:
	.string "Voce tem coragem! Gostei!\n"
	.string "Continue assim!$"

