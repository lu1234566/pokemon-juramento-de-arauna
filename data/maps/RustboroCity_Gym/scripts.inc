RustboroCity_Gym_MapScripts::
	.byte 0

RustboroCity_Gym_EventScript_Roxanne::
	trainerbattle_single TRAINER_ROXANNE_1, RustboroCity_Gym_Text_RoxanneIntro, RustboroCity_Gym_Text_RoxanneDefeat, RustboroCity_Gym_EventScript_RoxanneDefeated, NO_MUSIC
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, RustboroCity_Gym_EventScript_RoxanneRematch
	goto_if_unset FLAG_RECEIVED_TM_ROCK_TOMB, RustboroCity_Gym_EventScript_GiveRockTomb
	msgbox RustboroCity_Gym_Text_RoxannePostBattle, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_RoxanneDefeated::
	message RustboroCity_Gym_Text_ReceivedStoneBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox RustboroCity_Gym_Text_StoneBadgeInfoTakeThis, MSGBOX_DEFAULT
	setflag FLAG_DEFEATED_RUSTBORO_GYM
	setflag FLAG_BADGE01_GET
	setvar VAR_RUSTBORO_CITY_STATE, 1
	addvar VAR_PETALBURG_GYM_STATE, 1
	setvar VAR_0x8008, 1
	call Common_EventScript_SetGymTrainers
	call_if_eq VAR_PETALBURG_GYM_STATE, 6, Common_EventScript_ReadyPetalburgGymForBattle
	goto RustboroCity_Gym_EventScript_GiveRockTomb
	end

RustboroCity_Gym_EventScript_GiveRockTomb::
	giveitem ITEM_TM_ROCK_TOMB
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_TM_ROCK_TOMB
	msgbox RustboroCity_Gym_Text_ExplainRockTomb, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_RoxanneRematch::
	trainerbattle_rematch_double TRAINER_ROXANNE_1, RustboroCity_Gym_Text_RoxannePreRematch, RustboroCity_Gym_Text_RoxanneRematchDefeat, RustboroCity_Gym_Text_RoxanneRematchNeedTwoMons
	msgbox RustboroCity_Gym_Text_RoxannePostRematch, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_Josh::
	trainerbattle_single TRAINER_JOSH, RustboroCity_Gym_Text_JoshIntro, RustboroCity_Gym_Text_JoshDefeat
	msgbox RustboroCity_Gym_Text_JoshPostBattle, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_Tommy::
	trainerbattle_single TRAINER_TOMMY, RustboroCity_Gym_Text_TommyIntro, RustboroCity_Gym_Text_TommyDefeat
	msgbox RustboroCity_Gym_Text_TommyPostBattle, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_Marc::
	trainerbattle_single TRAINER_MARC, RustboroCity_Gym_Text_MarcIntro, RustboroCity_Gym_Text_MarcDefeat
	msgbox RustboroCity_Gym_Text_MarcPostBattle, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_RUSTBORO_GYM, RustboroCity_Gym_EventScript_GymGuidePostVictory
	msgbox RustboroCity_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_GymGuidePostVictory::
	msgbox RustboroCity_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_BADGE01_GET, RustboroCity_Gym_EventScript_GymStatueCertified
	goto RustboroCity_Gym_EventScript_GymStatue
	end

RustboroCity_Gym_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_BADGE01_GET, RustboroCity_Gym_EventScript_GymStatueCertified
	goto RustboroCity_Gym_EventScript_GymStatue
	end

RustboroCity_Gym_EventScript_GymStatueCertified::
	msgbox RustboroCity_Gym_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

RustboroCity_Gym_EventScript_GymStatue::
	msgbox RustboroCity_Gym_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

RustboroCity_Gym_EventScript_RegisterRoxanne::
	lockall
	pokenavcall RustboroCity_Gym_Text_RoxanneRegisterCall
	waitmessage
	delay 30
	playfanfare MUS_REGISTER_MATCH_CALL
	msgbox RustboroCity_Gym_Text_RegisteredRoxanne, MSGBOX_DEFAULT
	waitfanfare
	closemessage
	delay 30
	setflag FLAG_ENABLE_ROXANNE_MATCH_CALL
	clearflag FLAG_ENABLE_ROXANNE_FIRST_CALL
	releaseall
	end

RustboroCity_Gym_Text_GymGuideAdvice:
	.string "DALVA: Pedra guarda marcas.\nAlgumas rachaduras contam mais\p"
	.string "que monumentos inteiros.$"

RustboroCity_Gym_Text_GymGuidePostVictory:
	.string "Dona Zila diz que uma historia\nmuda toda vez que e contada.\p"
	.string "Talvez seja por isso que ainda\nesta viva.$"

RustboroCity_Gym_Text_JoshIntro:
	.string "O HORIZONTE consertou a estrada\ndaqui. Nao sei se isso torna\p"
	.string "mais facil perguntar o que\nexiste debaixo dela.$"

RustboroCity_Gym_Text_JoshDefeat:
	.string "O HORIZONTE consertou a estrada\ndaqui. Nao sei se isso torna\p"
	.string "mais facil perguntar o que\nexiste debaixo dela.$"

RustboroCity_Gym_Text_JoshPostBattle:
	.string "Ultimamente alguns Pokemon\nparam diante de suas antigas\p"
	.string "casas como se nunca tivessem\nestado ali.$"

RustboroCity_Gym_Text_TommyIntro:
	.string "DALVA: Pedra guarda marcas.\nAlgumas rachaduras contam mais\p"
	.string "que monumentos inteiros.$"

RustboroCity_Gym_Text_TommyDefeat:
	.string "Dona Zila diz que uma historia\nmuda toda vez que e contada.\p"
	.string "Talvez seja por isso que ainda\nesta viva.$"

RustboroCity_Gym_Text_TommyPostBattle:
	.string "DALVA: Pedra guarda marcas.\nAlgumas rachaduras contam mais\p"
	.string "que monumentos inteiros.$"

RustboroCity_Gym_Text_MarcIntro:
	.string "Voce vai continuar mesmo\nsabendo que SERRA DO UIVO\p"
	.string "guarda partes da historia que\nmuita gente preferia deixar\p"
	.string "enterradas?$"

RustboroCity_Gym_Text_MarcDefeat:
	.string "Dona Zila diz que uma historia\nmuda toda vez que e contada.\p"
	.string "Talvez seja por isso que ainda\nesta viva.$"

RustboroCity_Gym_Text_MarcPostBattle:
	.string "Meu avo dizia que lembrar\ntambem cansa. Mas escolher pelo\p"
	.string "outro o que ele deve esquecer\nparece pior.$"

RustboroCity_Gym_Text_RoxanneIntro:
	.string "DALVA: Pedra guarda marcas.\nAlgumas rachaduras contam mais\p"
	.string "que monumentos inteiros.$"

RustboroCity_Gym_Text_RoxanneDefeat:
	.string "DALVA: Pedra guarda marcas.\nAlgumas rachaduras contam mais\p"
	.string "que monumentos inteiros.$"

RustboroCity_Gym_Text_ReceivedStoneBadge:
	.string "{PLAYER} received the STONE BADGE\n"
	.string "from ROXANNE.$"

RustboroCity_Gym_Text_StoneBadgeInfoTakeThis:
	.string "Ultimamente alguns Pokemon\nparam diante de suas antigas\p"
	.string "casas como se nunca tivessem\nestado ali.$"

RustboroCity_Gym_Text_ExplainRockTomb:
	.string "Dona Zila diz que uma historia\nmuda toda vez que e contada.\p"
	.string "Talvez seja por isso que ainda\nesta viva.$"

RustboroCity_Gym_Text_RoxannePostBattle:
	.string "DALVA: Pedra guarda marcas.\nAlgumas rachaduras contam mais\p"
	.string "que monumentos inteiros.$"

RustboroCity_Gym_Text_GymStatue:
	.string "Meu avo dizia que lembrar\ntambem cansa. Mas escolher pelo\p"
	.string "outro o que ele deve esquecer\nparece pior.$"

RustboroCity_Gym_Text_GymStatueCertified:
	.string "DALVA: Pedra guarda marcas.\nAlgumas rachaduras contam mais\p"
	.string "que monumentos inteiros.$"

RustboroCity_Gym_Text_RoxanneRegisterCall:
	.string "CIRO: O futuro nao espera por\nquem vive olhando para tras.\p"
	.string "Pelo menos era nisso que eu\nacreditava.$"

RustboroCity_Gym_Text_RegisteredRoxanne:
	.string "DALVA: Pedra guarda marcas.\nAlgumas rachaduras contam mais\p"
	.string "que monumentos inteiros.$"

RustboroCity_Gym_Text_RoxannePreRematch:
	.string "DALVA: Pedra guarda marcas.\nAlgumas rachaduras contam mais\p"
	.string "que monumentos inteiros.$"

RustboroCity_Gym_Text_RoxanneRematchDefeat:
	.string "DALVA: Pedra guarda marcas.\nAlgumas rachaduras contam mais\p"
	.string "que monumentos inteiros.$"

RustboroCity_Gym_Text_RoxannePostRematch:
	.string "DALVA: Pedra guarda marcas.\nAlgumas rachaduras contam mais\p"
	.string "que monumentos inteiros.$"

RustboroCity_Gym_Text_RoxanneRematchNeedTwoMons:
	.string "DALVA: Pedra guarda marcas.\nAlgumas rachaduras contam mais\p"
	.string "que monumentos inteiros.$"
