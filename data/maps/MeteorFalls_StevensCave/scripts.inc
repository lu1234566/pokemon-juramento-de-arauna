MeteorFalls_StevensCave_MapScripts::
	.byte 0

MeteorFalls_StevensCave_EventScript_Steven::
	lock
	goto_if_set FLAG_DEFEATED_METEOR_FALLS_STEVEN, MeteorFalls_StevensCave_EventScript_Defeated
	waitse
	playse SE_PIN
	applymovement LOCALID_METEOR_FALLS_STEVEN, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_METEOR_FALLS_STEVEN, Common_Movement_Delay48
	waitmovement 0
	applymovement LOCALID_METEOR_FALLS_STEVEN, Common_Movement_FacePlayer
	waitmovement 0
	msgbox MeteorFalls_StevensCave_Text_ShouldKnowHowGoodIAmExpectWorst, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_STEVEN, MeteorFalls_StevensCave_Text_StevenDefeat
	msgbox MeteorFalls_StevensCave_Text_MyPredictionCameTrue, MSGBOX_DEFAULT
	setflag FLAG_DEFEATED_METEOR_FALLS_STEVEN
	release
	end

MeteorFalls_StevensCave_EventScript_Defeated::
	applymovement LOCALID_METEOR_FALLS_STEVEN, Common_Movement_FacePlayer
	waitmovement 0
	msgbox MeteorFalls_StevensCave_Text_MyPredictionCameTrue, MSGBOX_DEFAULT
	release
	end

MeteorFalls_StevensCave_Text_ShouldKnowHowGoodIAmExpectWorst:
	.string "SEU BENTO: Quando um nome some\nda boca das pessoas, eu\p"
	.string "escrevo. Nao para substituir\nquem lembra; para deixar uma\p"
	.string "pista.$"

MeteorFalls_StevensCave_Text_StevenDefeat:
	.string "SEU BENTO: Quando um nome some\nda boca das pessoas, eu\p"
	.string "escrevo. Nao para substituir\nquem lembra; para deixar uma\p"
	.string "pista.$"

MeteorFalls_StevensCave_Text_MyPredictionCameTrue:
	.string "SEU BENTO: Quando um nome some\nda boca das pessoas, eu\p"
	.string "escrevo. Nao para substituir\nquem lembra; para deixar uma\p"
	.string "pista.$"

