FortreeCity_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FortreeCity_Gym_OnTransition
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, FortreeCity_Gym_OnWarp
	.byte 0

FortreeCity_Gym_OnTransition:
	special RotatingGate_InitPuzzle
	end

FortreeCity_Gym_OnWarp:
	map_script_2 VAR_TEMP_0, VAR_TEMP_0, FortreeCity_Gym_EventScript_InitRotatingGates
	.2byte 0

@ NOTE: This rotating gate puzzle makes use of VAR_TEMP_0 - VAR_TEMP_3
FortreeCity_Gym_EventScript_InitRotatingGates::
	special RotatingGate_InitPuzzleAndGraphics
	end

FortreeCity_Gym_EventScript_Winona::
	trainerbattle_single TRAINER_WINONA_1, FortreeCity_Gym_Text_WinonaIntro, FortreeCity_Gym_Text_WinonaDefeat, FortreeCity_Gym_EventScript_WinonaDefeated, NO_MUSIC
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, FortreeCity_Gym_EventScript_WinonaRematch
	goto_if_unset FLAG_RECEIVED_TM_AERIAL_ACE, FortreeCity_Gym_EventScript_GiveAerialAce2
	msgbox FortreeCity_Gym_Text_WinonaPostBattle, MSGBOX_DEFAULT
	release
	end

FortreeCity_Gym_EventScript_WinonaDefeated::
	message FortreeCity_Gym_Text_ReceivedFeatherBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox FortreeCity_Gym_Text_ExplainFeatherBadgeTakeThis, MSGBOX_DEFAULT
	setflag FLAG_DEFEATED_FORTREE_GYM
	setflag FLAG_BADGE06_GET
	setvar VAR_0x8008, 6
	call Common_EventScript_SetGymTrainers
	call FortreeCity_Gym_EventScript_GiveAerialAce
	closemessage
	delay 30
	playfanfare MUS_REGISTER_MATCH_CALL
	msgbox FortreeCity_Gym_Text_RegisteredWinona, MSGBOX_DEFAULT
	waitfanfare
	closemessage
	delay 30
	setflag FLAG_ENABLE_WINONA_MATCH_CALL
	setvar VAR_SCOTT_FORTREE_CALL_STEP_COUNTER, 0
	setflag FLAG_SCOTT_CALL_FORTREE_GYM
	release
	end

FortreeCity_Gym_EventScript_GiveAerialAce2::
	giveitem ITEM_TM_AERIAL_ACE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	msgbox FortreeCity_Gym_Text_ExplainAerialAce, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_AERIAL_ACE
	release
	end

FortreeCity_Gym_EventScript_GiveAerialAce::
	giveitem ITEM_TM_AERIAL_ACE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_BagIsFull
	msgbox FortreeCity_Gym_Text_ExplainAerialAce, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_AERIAL_ACE
	return

FortreeCity_Gym_EventScript_WinonaRematch::
	trainerbattle_rematch_double TRAINER_WINONA_1, FortreeCity_Gym_Text_WinonaPreRematch, FortreeCity_Gym_Text_WinonaRematchDefeat, FortreeCity_Gym_Text_WinonaRematchNeedTwoMons
	msgbox FortreeCity_Gym_Text_WinonaPostRematch, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Jared::
	trainerbattle_single TRAINER_JARED, FortreeCity_Gym_Text_JaredIntro, FortreeCity_Gym_Text_JaredDefeat
	msgbox FortreeCity_Gym_Text_JaredPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Edwardo::
	trainerbattle_single TRAINER_EDWARDO, FortreeCity_Gym_Text_EdwardoIntro, FortreeCity_Gym_Text_EdwardoDefeat
	msgbox FortreeCity_Gym_Text_EdwardoPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Flint::
	trainerbattle_single TRAINER_FLINT, FortreeCity_Gym_Text_FlintIntro, FortreeCity_Gym_Text_FlintDefeat
	msgbox FortreeCity_Gym_Text_FlintPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Ashley::
	trainerbattle_single TRAINER_ASHLEY, FortreeCity_Gym_Text_AshleyIntro, FortreeCity_Gym_Text_AshleyDefeat
	msgbox FortreeCity_Gym_Text_AshleyPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Humberto::
	trainerbattle_single TRAINER_HUMBERTO, FortreeCity_Gym_Text_HumbertoIntro, FortreeCity_Gym_Text_HumbertoDefeat
	msgbox FortreeCity_Gym_Text_HumbertoPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Darius::
	trainerbattle_single TRAINER_DARIUS, FortreeCity_Gym_Text_DariusIntro, FortreeCity_Gym_Text_DariusDefeat
	msgbox FortreeCity_Gym_Text_DariusPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_FORTREE_GYM, FortreeCity_Gym_EventScript_GymGuidePostVictory
	msgbox FortreeCity_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

FortreeCity_Gym_EventScript_GymGuidePostVictory::
	msgbox FortreeCity_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	release
	end

FortreeCity_Gym_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_BADGE06_GET, FortreeCity_Gym_EventScript_GymStatueCertified
	goto FortreeCity_Gym_EventScript_GymStatue
	end

FortreeCity_Gym_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_BADGE06_GET, FortreeCity_Gym_EventScript_GymStatueCertified
	goto FortreeCity_Gym_EventScript_GymStatue
	end

FortreeCity_Gym_EventScript_GymStatueCertified::
	msgbox FortreeCity_Gym_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

FortreeCity_Gym_EventScript_GymStatue::
	msgbox FortreeCity_Gym_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

FortreeCity_Gym_Text_GymGuideAdvice:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_GymGuidePostVictory:
	.string "Ultimamente alguns Pokemon\nparam diante de suas antigas\p"
	.string "casas como se nunca tivessem\nestado ali.$"

FortreeCity_Gym_Text_JaredIntro:
	.string "Ultimamente alguns Pokemon\nparam diante de suas antigas\p"
	.string "casas como se nunca tivessem\nestado ali.$"

FortreeCity_Gym_Text_JaredDefeat:
	.string "Ultimamente alguns Pokemon\nparam diante de suas antigas\p"
	.string "casas como se nunca tivessem\nestado ali.$"

FortreeCity_Gym_Text_JaredPostBattle:
	.string "Voce vai continuar mesmo\nsabendo que MATA DO MEIO guarda\p"
	.string "partes da historia que muita\ngente preferia deixar\p"
	.string "enterradas?$"

FortreeCity_Gym_Text_EdwardoIntro:
	.string "Meu avo dizia que lembrar\ntambem cansa. Mas escolher pelo\p"
	.string "outro o que ele deve esquecer\nparece pior.$"

FortreeCity_Gym_Text_EdwardoDefeat:
	.string "Ultimamente alguns Pokemon\nparam diante de suas antigas\p"
	.string "casas como se nunca tivessem\nestado ali.$"

FortreeCity_Gym_Text_EdwardoPostBattle:
	.string "O HORIZONTE consertou a estrada\ndaqui. Nao sei se isso torna\p"
	.string "mais facil perguntar o que\nexiste debaixo dela.$"

FortreeCity_Gym_Text_FlintIntro:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_FlintDefeat:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_FlintPostBattle:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_AshleyIntro:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_AshleyDefeat:
	.string "Meu avo dizia que lembrar\ntambem cansa. Mas escolher pelo\p"
	.string "outro o que ele deve esquecer\nparece pior.$"

FortreeCity_Gym_Text_AshleyPostBattle:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_HumbertoIntro:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_HumbertoDefeat:
	.string "Tem gente que chama de\nDESENCANTO. Eu chamava de\p"
	.string "distraicao, ate minha mae\nesquecer a cancao que cantava\p"
	.string "desde crianca.$"

FortreeCity_Gym_Text_HumbertoPostBattle:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_DariusIntro:
	.string "Voce vai continuar mesmo\nsabendo que MATA DO MEIO guarda\p"
	.string "partes da historia que muita\ngente preferia deixar\p"
	.string "enterradas?$"

FortreeCity_Gym_Text_DariusDefeat:
	.string "Tem gente que chama de\nDESENCANTO. Eu chamava de\p"
	.string "distraicao, ate minha mae\nesquecer a cancao que cantava\p"
	.string "desde crianca.$"

FortreeCity_Gym_Text_DariusPostBattle:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_WinonaIntro:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_WinonaDefeat:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_ReceivedFeatherBadge:
	.string "{PLAYER} received the FEATHER BADGE\n"
	.string "from WINONA.$"

FortreeCity_Gym_Text_ExplainFeatherBadgeTakeThis:
	.string "Tem gente que chama de\nDESENCANTO. Eu chamava de\p"
	.string "distraicao, ate minha mae\nesquecer a cancao que cantava\p"
	.string "desde crianca.$"

FortreeCity_Gym_Text_ExplainAerialAce:
	.string "Existem placas novas por toda\nparte. Curioso e que alguns\p"
	.string "nomes antigos desapareceram\nquando elas chegaram.$"

FortreeCity_Gym_Text_RegisteredWinona:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_WinonaPostBattle:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_GymStatue:
	.string "Meu avo dizia que lembrar\ntambem cansa. Mas escolher pelo\p"
	.string "outro o que ele deve esquecer\nparece pior.$"

FortreeCity_Gym_Text_GymStatueCertified:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_WinonaPreRematch:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_WinonaRematchDefeat:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_WinonaPostRematch:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"

FortreeCity_Gym_Text_WinonaRematchNeedTwoMons:
	.string "LIDIA: A mata ensina caminhos\nsem escrever placas. Quando os\p"
	.string "Pokemon esquecem esses\ncaminhos, alguma coisa muito\p"
	.string "antiga foi ferida.$"
