LavaridgeTown_Gym_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LavaridgeTown_Gym_1F_OnTransition
	.byte 0

LavaridgeTown_Gym_1F_OnTransition:
	call LavaridgeTown_Gym_1F_EventScript_SetTrainerTempVars
	call LavaridgeTown_Gym_1F_EventScript_CheckBuryTrainers
	end

@ Unclear where/if these temp vars are getting checked
LavaridgeTown_Gym_1F_EventScript_SetTrainerTempVars::
	setvar VAR_TEMP_B, 0
	setvar VAR_TEMP_C, 0
	setvar VAR_TEMP_D, 0
	setvar VAR_TEMP_E, 0
	setvar VAR_TEMP_F, 0
	goto_if_defeated TRAINER_COLE, LavaridgeTown_Gym_1F_EventScript_SetGeraldTempVar
	setvar VAR_TEMP_B, 1
LavaridgeTown_Gym_1F_EventScript_SetGeraldTempVar::
	goto_if_defeated TRAINER_GERALD, LavaridgeTown_Gym_1F_EventScript_SetAxleTempVar
	setvar VAR_TEMP_C, 1
LavaridgeTown_Gym_1F_EventScript_SetAxleTempVar::
	goto_if_defeated TRAINER_AXLE, LavaridgeTown_Gym_1F_EventScript_SetDanielleTempVar
	setvar VAR_TEMP_D, 1
LavaridgeTown_Gym_1F_EventScript_SetDanielleTempVar::
	goto_if_defeated TRAINER_DANIELLE, LavaridgeTown_Gym_1F_EventScript_EndSetTrainerTempVars
	setvar VAR_TEMP_E, 1
LavaridgeTown_Gym_1F_EventScript_EndSetTrainerTempVars::
	return

LavaridgeTown_Gym_1F_EventScript_CheckBuryTrainers::
	goto_if_defeated TRAINER_COLE, LavaridgeTown_Gym_1F_EventScript_CheckBuryGerald
	setobjectmovementtype LOCALID_COLE, MOVEMENT_TYPE_BURIED
LavaridgeTown_Gym_1F_EventScript_CheckBuryGerald::
	goto_if_defeated TRAINER_GERALD, LavaridgeTown_Gym_1F_EventScript_CheckBuryAxle
	setobjectmovementtype LOCALID_GERALD, MOVEMENT_TYPE_BURIED
LavaridgeTown_Gym_1F_EventScript_CheckBuryAxle::
	goto_if_defeated TRAINER_AXLE, LavaridgeTown_Gym_1F_EventScript_CheckBuryDanielle
	setobjectmovementtype LOCALID_AXLE, MOVEMENT_TYPE_BURIED
LavaridgeTown_Gym_1F_EventScript_CheckBuryDanielle::
	goto_if_defeated TRAINER_DANIELLE, LavaridgeTown_Gym_1F_EventScript_EndCheckBuryTrainers
	setobjectmovementtype LOCALID_DANIELLE, MOVEMENT_TYPE_BURIED
LavaridgeTown_Gym_1F_EventScript_EndCheckBuryTrainers::
	return

LavaridgeTown_Gym_1F_EventScript_Flannery::
	trainerbattle_single TRAINER_FLANNERY_1, LavaridgeTown_Gym_1F_Text_FlanneryIntro, LavaridgeTown_Gym_1F_Text_FlanneryDefeat, LavaridgeTown_Gym_1F_EventScript_FlanneryDefeated, NO_MUSIC
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, LavaridgeTown_Gym_1F_EventScript_FlanneryRematch
	goto_if_unset FLAG_RECEIVED_TM_OVERHEAT, LavaridgeTown_Gym_1F_EventScript_GiveOverheat2
	msgbox LavaridgeTown_Gym_1F_Text_FlanneryPostBattle, MSGBOX_DEFAULT
	release
	end

LavaridgeTown_Gym_1F_EventScript_FlanneryDefeated::
	message LavaridgeTown_Gym_1F_Text_ReceivedHeatBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox LavaridgeTown_Gym_1F_Text_ExplainHeatBadgeTakeThis, MSGBOX_DEFAULT
	setflag FLAG_WHITEOUT_TO_LAVARIDGE
	setflag FLAG_DEFEATED_LAVARIDGE_GYM
	setflag FLAG_BADGE04_GET
	addvar VAR_PETALBURG_GYM_STATE, 1
	call_if_eq VAR_PETALBURG_GYM_STATE, 6, Common_EventScript_ReadyPetalburgGymForBattle
	setvar VAR_0x8008, 4
	call Common_EventScript_SetGymTrainers
	setflag FLAG_HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WALLY
	setvar VAR_LAVARIDGE_TOWN_STATE, 1
	call LavaridgeTown_Gym_1F_EventScript_GiveOverheat
	closemessage
	delay 30
	playfanfare MUS_REGISTER_MATCH_CALL
	msgbox LavaridgeTown_Gym_1F_Text_RegisteredFlannery, MSGBOX_DEFAULT
	waitfanfare
	closemessage
	delay 30
	setflag FLAG_ENABLE_FLANNERY_MATCH_CALL
	release
	end

LavaridgeTown_Gym_1F_EventScript_GiveOverheat2::
	giveitem ITEM_TM_OVERHEAT
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	msgbox LavaridgeTown_Gym_1F_Text_ExplainOverheat, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_OVERHEAT
	release
	end

LavaridgeTown_Gym_1F_EventScript_GiveOverheat::
	giveitem ITEM_TM_OVERHEAT
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_BagIsFull
	msgbox LavaridgeTown_Gym_1F_Text_ExplainOverheat, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_OVERHEAT
	return

LavaridgeTown_Gym_1F_EventScript_FlanneryRematch::
	trainerbattle_rematch_double TRAINER_FLANNERY_1, LavaridgeTown_Gym_1F_Text_FlanneryPreRematch, LavaridgeTown_Gym_1F_Text_FlanneryRematchDefeat, LavaridgeTown_Gym_1F_Text_FlanneryRematchNeedTwoMons
	msgbox LavaridgeTown_Gym_1F_Text_FlanneryPostRematch, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_1F_EventScript_Cole::
	trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, TRAINER_COLE, LOCALID_COLE, LavaridgeTown_Gym_1F_Text_ColeIntro, LavaridgeTown_Gym_1F_Text_ColeDefeat, LavaridgeTown_Gym_EventScript_CheckTrainerScript
	msgbox LavaridgeTown_Gym_1F_Text_ColePostBattle, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_EventScript_CheckTrainerScript::
	call LavaridgeTown_Gym_1F_EventScript_SetTrainerTempVars
	release
	special ShouldTryGetTrainerScript
	goto_if_eq VAR_RESULT, 1, EventScript_GotoTrainerScript
	end

LavaridgeTown_Gym_1F_EventScript_Axle::
	trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, TRAINER_AXLE, LOCALID_AXLE, LavaridgeTown_Gym_1F_Text_AxleIntro, LavaridgeTown_Gym_1F_Text_AxleDefeat, LavaridgeTown_Gym_EventScript_CheckTrainerScript
	msgbox LavaridgeTown_Gym_1F_Text_AxlePostBattle, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_B1F_EventScript_Keegan::
	trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, TRAINER_KEEGAN, LOCALID_KEEGAN, LavaridgeTown_Gym_B1F_Text_KeeganIntro, LavaridgeTown_Gym_B1F_Text_KeeganDefeat, LavaridgeTown_Gym_EventScript_CheckTrainerScript
	msgbox LavaridgeTown_Gym_B1F_Text_KeeganPostBattle, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_1F_EventScript_Danielle::
	trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, TRAINER_DANIELLE, LOCALID_DANIELLE, LavaridgeTown_Gym_1F_Text_DanielleIntro, LavaridgeTown_Gym_1F_Text_DanielleDefeat, LavaridgeTown_Gym_EventScript_CheckTrainerScript
	msgbox LavaridgeTown_Gym_1F_Text_DaniellePostBattle, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_1F_EventScript_Gerald::
	trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, TRAINER_GERALD, LOCALID_GERALD, LavaridgeTown_Gym_1F_Text_GeraldIntro, LavaridgeTown_Gym_1F_Text_GeraldDefeat, LavaridgeTown_Gym_EventScript_CheckTrainerScript
	msgbox LavaridgeTown_Gym_1F_Text_GeraldPostBattle, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_B1F_EventScript_Jace::
	trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, TRAINER_JACE, LOCALID_JACE, LavaridgeTown_Gym_B1F_Text_JaceIntro, LavaridgeTown_Gym_B1F_Text_JaceDefeat, LavaridgeTown_Gym_EventScript_CheckTrainerScript
	msgbox LavaridgeTown_Gym_B1F_Text_JacePostBattle, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_B1F_EventScript_Jeff::
	trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, TRAINER_JEFF, LOCALID_JEFF, LavaridgeTown_Gym_B1F_Text_JeffIntro, LavaridgeTown_Gym_B1F_Text_JeffDefeat, LavaridgeTown_Gym_EventScript_CheckTrainerScript
	msgbox LavaridgeTown_Gym_B1F_Text_JeffPostBattle, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_B1F_EventScript_Eli::
	trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, TRAINER_ELI, LOCALID_ELI, LavaridgeTown_Gym_B1F_Text_EliIntro, LavaridgeTown_Gym_B1F_Text_EliDefeat, LavaridgeTown_Gym_EventScript_CheckTrainerScript
	msgbox LavaridgeTown_Gym_B1F_Text_EliPostBattle, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_1F_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_LAVARIDGE_GYM, LavaridgeTown_Gym_1F_EventScript_GymGuidePostVictory
	msgbox LavaridgeTown_Gym_1F_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

LavaridgeTown_Gym_1F_EventScript_GymGuidePostVictory::
	msgbox LavaridgeTown_Gym_1F_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	release
	end

LavaridgeTown_Gym_1F_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_BADGE04_GET, LavaridgeTown_Gym_1F_EventScript_GymStatueCertified
	goto LavaridgeTown_Gym_1F_EventScript_GymStatue
	end

LavaridgeTown_Gym_1F_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_BADGE04_GET, LavaridgeTown_Gym_1F_EventScript_GymStatueCertified
	goto LavaridgeTown_Gym_1F_EventScript_GymStatue
	end

LavaridgeTown_Gym_1F_EventScript_GymStatueCertified::
	msgbox LavaridgeTown_Gym_1F_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

LavaridgeTown_Gym_1F_EventScript_GymStatue::
	msgbox LavaridgeTown_Gym_1F_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

LavaridgeTown_Gym_1F_Text_GymGuideAdvice:
	.string "NARA leads CASA DA CINZA GYM.\p"
	.string "Her FIRE-types punish reckless\n"
	.string "pressure.\p"
	.string "Watch the heat. Pick a moment.$"

LavaridgeTown_Gym_1F_Text_GymGuidePostVictory:
	.string "You handled the heat without\n"
	.string "letting it handle you.$"

LavaridgeTown_Gym_1F_Text_ColeIntro:
	.string "Hot sand hides every step.\p"
	.string "Can you keep your footing?$"

LavaridgeTown_Gym_1F_Text_ColeDefeat:
	.string "I lost track of your rhythm.$"

LavaridgeTown_Gym_1F_Text_ColePostBattle:
	.string "Heat makes people rush.\p"
	.string "That is when mistakes multiply.$"

LavaridgeTown_Gym_1F_Text_AxleIntro:
	.string "Pressure rises fast in here.\p"
	.string "Let's see what you do with it.$"

LavaridgeTown_Gym_1F_Text_AxleDefeat:
	.string "You never let me set the pace.$"

LavaridgeTown_Gym_1F_Text_AxlePostBattle:
	.string "NARA says cooling down is part\n"
	.string "of controlling heat.$"

LavaridgeTown_Gym_B1F_Text_KeeganIntro:
	.string "The lower chambers hold heat.\p"
	.string "Fatigue makes choices louder.$"

LavaridgeTown_Gym_B1F_Text_KeeganDefeat:
	.string "You stayed clear-headed.$"

LavaridgeTown_Gym_B1F_Text_KeeganPostBattle:
	.string "NARA never asks us to ignore\n"
	.string "pain.\p"
	.string "She asks what it is telling us.$"

LavaridgeTown_Gym_1F_Text_GeraldIntro:
	.string "Steam hides more than distance.\p"
	.string "Read the room before you move.$"

LavaridgeTown_Gym_1F_Text_GeraldDefeat:
	.string "You read it better than I did.$"

LavaridgeTown_Gym_1F_Text_GeraldPostBattle:
	.string "A gauge is useful.\p"
	.string "So is noticing what the gauge\n"
	.string "cannot measure.$"

LavaridgeTown_Gym_1F_Text_DanielleIntro:
	.string "Ash marks where heat has been.\p"
	.string "Show me what your path leaves.$"

LavaridgeTown_Gym_1F_Text_DanielleDefeat:
	.string "That answer was clear enough.$"

LavaridgeTown_Gym_1F_Text_DaniellePostBattle:
	.string "I want NARA's kind of strength.\p"
	.string "Not louder. Steadier.$"

LavaridgeTown_Gym_B1F_Text_JaceIntro:
	.string "A flame can flare in one breath.\p"
	.string "Control takes longer.$"

LavaridgeTown_Gym_B1F_Text_JaceDefeat:
	.string "Mine flared. Yours held.$"

LavaridgeTown_Gym_B1F_Text_JacePostBattle:
	.string "You may be ready for NARA.\p"
	.string "She notices when people mistake\n"
	.string "heat for courage.$"

LavaridgeTown_Gym_B1F_Text_JeffIntro:
	.string "Everyone watches the flame.\p"
	.string "I watch what survives it.$"

LavaridgeTown_Gym_B1F_Text_JeffDefeat:
	.string "You left me with ash.$"

LavaridgeTown_Gym_B1F_Text_JeffPostBattle:
	.string "Ash looks empty until you study\n"
	.string "what is mixed into it.$"

LavaridgeTown_Gym_B1F_Text_EliIntro:
	.string "Volcanoes build and destroy.\p"
	.string "Neither fact erases the other.$"

LavaridgeTown_Gym_B1F_Text_EliDefeat:
	.string "I lost control of the slope.$"

LavaridgeTown_Gym_B1F_Text_EliPostBattle:
	.string "NARA taught me not to worship\n"
	.string "destruction just because it is\n"
	.string "powerful.$"

LavaridgeTown_Gym_1F_Text_FlanneryIntro:
	.string "NARA: Fire gets all the songs.\p"
	.string "Ash is what stays after.\p"
	.string "It records what changed and what\n"
	.string "was lost.\p"
	.string "Show me how you handle heat.$"

LavaridgeTown_Gym_1F_Text_FlanneryDefeat:
	.string "NARA: You knew when to press...\n"
	.string "and when to cool.$"

LavaridgeTown_Gym_1F_Text_ReceivedHeatBadge:
	.string "{PLAYER} received the\n"
	.string "ASH BADGE from NARA.$"

LavaridgeTown_Gym_1F_Text_ExplainHeatBadgeTakeThis:
	.string "With the ASH BADGE, POKéMON\n"
	.string "up to Lv. 50 will obey.\p"
	.string "You can also use STRENGTH\n"
	.string "outside battle.\p"
	.string "Take this too.$"

LavaridgeTown_Gym_1F_Text_ExplainOverheat:
	.string "TM50 contains OVERHEAT.\p"
	.string "It hits hard, then lowers\n"
	.string "the user's SP. ATK sharply.\p"
	.string "Power always leaves a cost.$"

LavaridgeTown_Gym_1F_Text_RegisteredFlannery:
	.string "Registered GYM LEADER NARA\n"
	.string "in the POKéNAV.$"

LavaridgeTown_Gym_1F_Text_FlanneryPostBattle:
	.string "NARA: Ash isn't failure.\p"
	.string "It's evidence that something\n"
	.string "burned.\p"
	.string "Remember that before anyone\n"
	.string "calls erasure a clean start.$"

LavaridgeTown_Gym_1F_Text_GymStatue:
	.string "CASA DA CINZA GYM\p"
	.string "LEADER: NARA$"

LavaridgeTown_Gym_1F_Text_GymStatueCertified:
	.string "CASA DA CINZA GYM\p"
	.string "NARA'S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

LavaridgeTown_Gym_1F_Text_FlanneryPreRematch:
	.string "NARA: Heat changes with time.\p"
	.string "So should a good battle. Ready?$"

LavaridgeTown_Gym_1F_Text_FlanneryRematchDefeat:
	.string "NARA: Better control.\p"
	.string "Same lesson.$"

LavaridgeTown_Gym_1F_Text_FlanneryPostRematch:
	.string "NARA: You knew when to stop\n"
	.string "feeding the flame.$"

LavaridgeTown_Gym_1F_Text_FlanneryRematchNeedTwoMons:
	.string "NARA: Bring two POKéMON or more.\p"
	.string "A rematch needs enough room to\n"
	.string "change.$"
