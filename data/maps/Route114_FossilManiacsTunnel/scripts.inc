Route114_FossilManiacsTunnel_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route114_FossilManiacsTunnel_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, Route114_FossilManiacsTunnel_OnLoad
	.byte 0

Route114_FossilManiacsTunnel_OnTransition:
	call_if_set FLAG_SYS_GAME_CLEAR, Route114_FossilManiacsTunnel_EventScript_MoveFossilManiac
	end

Route114_FossilManiacsTunnel_EventScript_MoveFossilManiac::
	setobjectxyperm LOCALID_FOSSIL_MANIAC, 6, 5
	setobjectmovementtype LOCALID_FOSSIL_MANIAC, MOVEMENT_TYPE_FACE_DOWN
	return

Route114_FossilManiacsTunnel_OnLoad:
	call_if_unset FLAG_SYS_GAME_CLEAR, Route114_FossilManiacsTunnel_EventScript_CloseDesertUnderpass
	end

Route114_FossilManiacsTunnel_EventScript_CloseDesertUnderpass::
	setmetatile 6, 1, METATILE_Fallarbor_RedRockWall, TRUE
	setmetatile 6, 2, METATILE_Fallarbor_RedRockWall, TRUE
	return

Route114_FossilManiacsTunnel_EventScript_ManiacMentionCaveIn::
	lockall
	applymovement LOCALID_FOSSIL_MANIAC, Common_Movement_WalkInPlaceFasterUp
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox Route114_FossilManiacsTunnel_Text_NotSafeThatWay, MSGBOX_DEFAULT
	setvar VAR_FOSSIL_MANIAC_STATE, 2
	releaseall
	end

Route114_FossilManiacsTunnel_EventScript_FossilManiac::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_REVIVED_FOSSIL_MON, Route114_FossilManiacsTunnel_EventScript_PlayerRevivedFossil
	checkitem ITEM_ROOT_FOSSIL
	goto_if_eq VAR_RESULT, TRUE, Route114_FossilManiacsTunnel_EventScript_PlayerHasFossil
	checkitem ITEM_CLAW_FOSSIL
	goto_if_eq VAR_RESULT, TRUE, Route114_FossilManiacsTunnel_EventScript_PlayerHasFossil
	msgbox Route114_FossilManiacsTunnel_Text_LookInDesertForFossils, MSGBOX_DEFAULT
	release
	end

Route114_FossilManiacsTunnel_EventScript_PlayerHasFossil::
	msgbox Route114_FossilManiacsTunnel_Text_DevonCorpRevivingFossils, MSGBOX_DEFAULT
	release
	end

Route114_FossilManiacsTunnel_EventScript_PlayerRevivedFossil::
	msgbox Route114_FossilManiacsTunnel_Text_FossilsAreWonderful, MSGBOX_DEFAULT
	release
	end

Route114_FossilManiacsTunnel_Text_LookInDesertForFossils:
	.string "Sou o MANIACO DOS FOSSEIS...\n"
	.string "Gosto muito de FOSSEIS.\p"
	.string "Voce quer um FOSSIL?\p"
	.string "Os daqui eu encontrei primeiro.\p"
	.string "Se quiser procurar por conta\n"
	.string "propria, tente o deserto.\p"
	.string "Pedras e areia escondem\n"
	.string "coisas por muito tempo.$"

Route114_FossilManiacsTunnel_Text_DevonCorpRevivingFossils:
	.string "Voce encontrou um FOSSIL?\n"
	.string "Que achado bonito...\p"
	.string "O que pretende fazer com ele?\p"
	.string "Ouvi dizer que o HORIZONTE\n"
	.string "pesquisa formas de recuperar\l"
	.string "POKéMON a partir de FOSSEIS.\p"
	.string "Eu prefiro deixar os meus\n"
	.string "do jeito que encontrei.$"

Route114_FossilManiacsTunnel_Text_FossilsAreWonderful:
	.string "FOSSEIS sao maravilhosos...\n"
	.string "Da vontade de ficar olhando.$"

Route114_FossilManiacsTunnel_Text_NotSafeThatWay:
	.string "Ei... por ali nao e seguro.\p"
	.string "Eu estava escavando quando\n"
	.string "a parede inteira desabou.\p"
	.string "Parece haver uma caverna\n"
	.string "enorme logo abaixo.\p"
	.string "Deixei tudo quieto porque\n"
	.string "nao achei FOSSEIS por la.$"

