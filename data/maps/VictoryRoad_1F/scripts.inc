VictoryRoad_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, VictoryRoad_1F_OnTransition
	.byte 0

VictoryRoad_1F_OnTransition:
	call_if_eq VAR_VICTORY_ROAD_1F_STATE, 1, VictoryRoad_1F_EventScript_SetEntranceWallyPos1
	call_if_eq VAR_VICTORY_ROAD_1F_STATE, 2, VictoryRoad_1F_EventScript_SetEntranceWallyPos2
	end

VictoryRoad_1F_EventScript_SetEntranceWallyPos1::
	setobjectxyperm LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, 2, 24
	setobjectmovementtype LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, MOVEMENT_TYPE_FACE_DOWN
	return

VictoryRoad_1F_EventScript_SetEntranceWallyPos2::
	setobjectxyperm LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, 3, 24
	setobjectmovementtype LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, MOVEMENT_TYPE_FACE_DOWN
	return

VictoryRoad_1F_EventScript_WallyBattleTrigger1::
	lockall
	setvar VAR_0x8008, 1
	addobject LOCALID_VICTORY_ROAD_ENTRANCE_WALLY
	applymovement LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, VictoryRoad_1F_Movement_WallyApproachPlayer1
	waitmovement 0
	goto VictoryRoad_1F_EventScript_WallyEntranceBattle
	end

VictoryRoad_1F_EventScript_WallyBattleTrigger2::
	lockall
	setvar VAR_0x8008, 2
	addobject LOCALID_VICTORY_ROAD_ENTRANCE_WALLY
	applymovement LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, VictoryRoad_1F_Movement_WallyApproachPlayer2
	waitmovement 0
	goto VictoryRoad_1F_EventScript_WallyEntranceBattle
	end

VictoryRoad_1F_EventScript_WallyEntranceBattle::
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox VictoryRoad_1F_Text_WallyNotGoingToLoseAnymore, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_WALLY_VR_1, VictoryRoad_1F_Text_WallyEntranceDefeat
	msgbox VictoryRoad_1F_Text_WallyPostEntranceBattle, MSGBOX_DEFAULT
	clearflag FLAG_HIDE_VICTORY_ROAD_ENTRANCE_WALLY
	copyobjectxytoperm LOCALID_VICTORY_ROAD_ENTRANCE_WALLY
	setflag FLAG_DEFEATED_WALLY_VICTORY_ROAD
	copyvar VAR_VICTORY_ROAD_1F_STATE, VAR_0x8008
	releaseall
	end

VictoryRoad_1F_Movement_WallyApproachPlayer1:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_up
	step_end

VictoryRoad_1F_Movement_WallyApproachPlayer2:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_up
	step_end

@ This Wally appears near the entrance once his battle is triggered and remains there until the Hall of Fame is entered
VictoryRoad_1F_EventScript_EntranceWally::
	msgbox VictoryRoad_1F_Text_WallyPostEntranceBattle, MSGBOX_NPC
	end

@ This Wally appears and remains at the exit after the Hall of Fame is entered
VictoryRoad_1F_EventScript_ExitWally::
	trainerbattle_single TRAINER_WALLY_VR_2, VictoryRoad_1F_Text_WallyIntro, VictoryRoad_1F_Text_WallyDefeat
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, VictoryRoad_1F_EventScript_RematchWally
	msgbox VictoryRoad_1F_Text_WallyPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_RematchWally::
	trainerbattle_rematch TRAINER_WALLY_VR_2, VictoryRoad_1F_Text_WallyIntro, VictoryRoad_1F_Text_WallyDefeat
	msgbox VictoryRoad_1F_Text_WallyPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Edgar::
	trainerbattle_single TRAINER_EDGAR, VictoryRoad_1F_Text_EdgarIntro, VictoryRoad_1F_Text_EdgarDefeat
	msgbox VictoryRoad_1F_Text_EdgarPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Albert::
	trainerbattle_single TRAINER_ALBERT, VictoryRoad_1F_Text_AlbertIntro, VictoryRoad_1F_Text_AlbertDefeat
	msgbox VictoryRoad_1F_Text_AlbertPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Hope::
	trainerbattle_single TRAINER_HOPE, VictoryRoad_1F_Text_HopeIntro, VictoryRoad_1F_Text_HopeDefeat
	msgbox VictoryRoad_1F_Text_HopePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Quincy::
	trainerbattle_single TRAINER_QUINCY, VictoryRoad_1F_Text_QuincyIntro, VictoryRoad_1F_Text_QuincyDefeat
	msgbox VictoryRoad_1F_Text_QuincyPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Katelynn::
	trainerbattle_single TRAINER_KATELYNN, VictoryRoad_1F_Text_KatelynnIntro, VictoryRoad_1F_Text_KatelynnDefeat
	msgbox VictoryRoad_1F_Text_KatelynnPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_Text_WallyNotGoingToLoseAnymore:
	.string "VAL: Cheguei ate aqui no meu\n"
	.string "ritmo, {PLAYER}. Desta vez nao\p"
	.string "vou tentar ser outra pessoa.\p"
	.string "Quero descobrir ate onde consigo\n"
	.string "ir sendo eu mesmo.$"

VictoryRoad_1F_Text_WallyEntranceDefeat:
	.string "VAL: Perdi... mas nao recuei.\p"
	.string "Antes isso teria me quebrado.\n"
	.string "Agora so me mostra quanto ainda\n"
	.string "posso crescer.$"

VictoryRoad_1F_Text_WallyPostEntranceBattle:
	.string "VAL: Vai em frente, {PLAYER}.\p"
	.string "Eu tambem vou continuar.\n"
	.string "Quando nos virmos de novo,\n"
	.string "quero estar ainda mais forte.$"

VictoryRoad_1F_Text_WallyIntro:
	.string "VAL: Campeao ou nao, eu ainda\n"
	.string "quero medir meu passo com o seu.\p"
	.string "Vamos, {PLAYER}. Sem desculpas.$"

VictoryRoad_1F_Text_WallyDefeat:
	.string "VAL: Ha! Ainda falta estrada\n"
	.string "para eu te alcancar.$"

VictoryRoad_1F_Text_WallyPostBattle:
	.string "VAL: Cada derrota me mostra\n"
	.string "alguma coisa que eu nao via.\p"
	.string "Na proxima, eu chego mais perto.$"

VictoryRoad_1F_Text_EdgarIntro:
	.string "Ja cheguei ate aqui antes,\n"
	.string "mas o fim sempre parece longo.$"

VictoryRoad_1F_Text_EdgarDefeat:
	.string "Meu sonho para aqui de novo...$"

VictoryRoad_1F_Text_EdgarPostBattle:
	.string "Voce chegou longe.\n"
	.string "Nao pare agora!\p"
	.string "Va e conquiste a LIGA!$"

VictoryRoad_1F_Text_AlbertIntro:
	.string "Nao vim ate aqui para perder.\n"
	.string "Essa opcao nao existe!$"

VictoryRoad_1F_Text_AlbertDefeat:
	.string "Impossivel...\n"
	.string "Eu perdi?$"

VictoryRoad_1F_Text_AlbertPostBattle:
	.string "Perdi aqui...\p"
	.string "Ainda nao estou pronto\n"
	.string "para conquistar a LIGA.$"

VictoryRoad_1F_Text_HopeIntro:
	.string "Esta estrada parece nao ter fim.\n"
	.string "Agora entendo seu nome.$"

VictoryRoad_1F_Text_HopeDefeat:
	.string "Seu jeito de lutar e incrivel...$"

VictoryRoad_1F_Text_HopePostBattle:
	.string "Voce tem forca para chegar\n"
	.string "ate o topo da LIGA.$"

VictoryRoad_1F_Text_QuincyIntro:
	.string "O que e esta estrada?\n"
	.string "Eu conto se voce vencer!$"

VictoryRoad_1F_Text_QuincyDefeat:
	.string "Certo!\n"
	.string "Muito bem!$"

VictoryRoad_1F_Text_QuincyPostBattle:
	.string "Este caminho e o ultimo teste\n"
	.string "de quem busca o topo da LIGA.\p"
	.string "Por isso ele se chama\n"
	.string "ESTRADA DO JURAMENTO.$"

VictoryRoad_1F_Text_KatelynnIntro:
	.string "Se chegou ate aqui, nao preciso\n"
	.string "explicar nada. Vamos!$"

VictoryRoad_1F_Text_KatelynnDefeat:
	.string "Que vergonha...$"

VictoryRoad_1F_Text_KatelynnPostBattle:
	.string "Hmph. Pode seguir.\n"
	.string "Veja se eu me importo.$"
