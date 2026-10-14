SootopolisCity_Gym_1F_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, SootopolisCity_Gym_1F_OnResume
	map_script MAP_SCRIPT_ON_LOAD, SootopolisCity_Gym_1F_OnLoad
	.byte 0

@ O piso de cima nao e mais o quebra-cabeca de gelo contado por passos: as
@ tres travessias centrais abrem pelos testemunhos do piso de baixo, e o
@ estado vem das flags de derrota guardadas no save.
SootopolisCity_Gym_1F_OnResume:
	setstepcallback STEP_CB_DUMMY
	end

SootopolisCity_Gym_1F_OnLoad:
	call_if_defeated TRAINER_ANDREA, SootopolisCity_Gym_1F_EventScript_OpenOldCrossing
	call_if_defeated TRAINER_DAPHNE, SootopolisCity_Gym_1F_EventScript_OpenNewCrossing
	call_if_defeated TRAINER_BRIANNA, SootopolisCity_Gym_1F_EventScript_OpenArchiveCrossing
	end

SootopolisCity_Gym_1F_EventScript_OpenOldCrossing::
	setmetatile 8, 16, 0x211, FALSE
	return

SootopolisCity_Gym_1F_EventScript_OpenNewCrossing::
	setmetatile 8, 11, 0x211, FALSE
	return

SootopolisCity_Gym_1F_EventScript_OpenArchiveCrossing::
	setmetatile 8, 6, 0x211, FALSE
	return

SootopolisCity_Gym_1F_EventScript_OldCrossing::
	lockall
	goto_if_defeated TRAINER_ANDREA, SootopolisCity_Gym_1F_EventScript_OldCrossingOpen
	msgbox SootopolisCity_Gym_1F_Text_OldCrossingClosed, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_Gym_1F_EventScript_OldCrossingOpen::
	call SootopolisCity_Gym_1F_EventScript_OpenOldCrossing
	special DrawWholeMapView
	releaseall
	end

SootopolisCity_Gym_1F_EventScript_NewCrossing::
	lockall
	goto_if_defeated TRAINER_DAPHNE, SootopolisCity_Gym_1F_EventScript_NewCrossingOpen
	msgbox SootopolisCity_Gym_1F_Text_NewCrossingClosed, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_Gym_1F_EventScript_NewCrossingOpen::
	call SootopolisCity_Gym_1F_EventScript_OpenNewCrossing
	special DrawWholeMapView
	releaseall
	end

SootopolisCity_Gym_1F_EventScript_ArchiveCrossing::
	lockall
	goto_if_defeated TRAINER_BRIANNA, SootopolisCity_Gym_1F_EventScript_ArchiveCrossingOpen
	msgbox SootopolisCity_Gym_1F_Text_ArchiveCrossingClosed, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_Gym_1F_EventScript_ArchiveCrossingOpen::
	call SootopolisCity_Gym_1F_EventScript_OpenArchiveCrossing
	special DrawWholeMapView
	releaseall
	end

SootopolisCity_Gym_1F_EventScript_OldBankMural::
	lockall
	msgbox SootopolisCity_Gym_1F_Text_OldBankMural, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_Gym_1F_EventScript_NewBankMural::
	lockall
	msgbox SootopolisCity_Gym_1F_Text_NewBankMural, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_Gym_1F_EventScript_Juan::
@ As tres testemunhas do piso de baixo -- a margem antiga, a margem nova e o
@ arquivo alagado -- precisam ser ouvidas antes da CELINA. A guarda usa as
@ flags de treinador derrotado que ja existem, entao um save antigo em que as
@ tres ja cairam abre o desafio direto.
	goto_if_set FLAG_DEFEATED_SOOTOPOLIS_GYM, SootopolisCity_Gym_1F_EventScript_CelinaReady
	goto_if_not_defeated TRAINER_ANDREA, SootopolisCity_Gym_1F_EventScript_ThreeMemoriesMissing
	goto_if_not_defeated TRAINER_DAPHNE, SootopolisCity_Gym_1F_EventScript_ThreeMemoriesMissing
	goto_if_not_defeated TRAINER_BRIANNA, SootopolisCity_Gym_1F_EventScript_ThreeMemoriesMissing
	msgbox SootopolisCity_Gym_1F_Text_MemoriesTogether, MSGBOX_DEFAULT
	special HealPlayerParty
	setrespawn HEAL_LOCATION_SOOTOPOLIS_CITY
SootopolisCity_Gym_1F_EventScript_CelinaReady::
	trainerbattle_single TRAINER_JUAN_1, SootopolisCity_Gym_1F_Text_JuanIntro, SootopolisCity_Gym_1F_Text_JuanDefeat, SootopolisCity_Gym_1F_EventScript_JuanDefeated, NO_MUSIC
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, SootopolisCity_Gym_1F_EventScript_JuanRematch
	goto_if_unset FLAG_RECEIVED_TM_WATER_PULSE, SootopolisCity_Gym_1F_EventScript_GiveWaterPulse2
	goto_if_unset FLAG_BADGE06_GET, SootopolisCity_Gym_1F_EventScript_GoGetFortreeBadge
	msgbox SootopolisCity_Gym_1F_Text_JuanPostBattle, MSGBOX_DEFAULT
	release
	end

SootopolisCity_Gym_1F_EventScript_ThreeMemoriesMissing::
	msgbox SootopolisCity_Gym_1F_Text_ThreeMemoriesMissing, MSGBOX_DEFAULT
	release
	end

@ A passarela da arena devolve o jogador a cidade sem precisar perder: o
@ quebra-cabeca do piso pode ser refeito.
SootopolisCity_Gym_1F_EventScript_ReturnToCity::
	lock
	faceplayer
	msgbox SootopolisCity_Gym_1F_Text_ReturnToCity, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SootopolisCity_Gym_1F_EventScript_StayInHouse
	warp MAP_SOOTOPOLIS_CITY, 25, 23
	waitstate
	release
	end

SootopolisCity_Gym_1F_EventScript_StayInHouse::
	release
	end

SootopolisCity_Gym_1F_EventScript_JuanDefeated::
	message SootopolisCity_Gym_1F_Text_ReceivedRainBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox SootopolisCity_Gym_1F_Text_ExplainRainBadgeTakeThis, MSGBOX_DEFAULT
	setflag FLAG_DEFEATED_SOOTOPOLIS_GYM
	setflag FLAG_BADGE08_GET
	setflag FLAG_HIDE_SOOTOPOLIS_CITY_RESIDENTS
	setflag FLAG_HIDE_SOOTOPOLIS_CITY_STEVEN
	setflag FLAG_HIDE_SOOTOPOLIS_CITY_WALLACE
	setvar VAR_SOOTOPOLIS_CITY_STATE, 6
	clearflag FLAG_HIDE_SOOTOPOLIS_CITY_MAN_1
	setvar VAR_0x8008, 8
	call Common_EventScript_SetGymTrainers
	call SootopolisCity_Gym_1F_EventScript_GiveWaterPulse
	closemessage
	delay 30
	playfanfare MUS_REGISTER_MATCH_CALL
	msgbox SootopolisCity_Gym_1F_Text_RegisteredJuan, MSGBOX_DEFAULT
	waitfanfare
	closemessage
	delay 30
	setflag FLAG_ENABLE_JUAN_MATCH_CALL
	release
	end

SootopolisCity_Gym_1F_EventScript_GiveWaterPulse::
	giveitem ITEM_TM_WATER_PULSE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_BagIsFull
	msgbox SootopolisCity_Gym_1F_Text_ExplainWaterPulse, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_WATER_PULSE
	return

SootopolisCity_Gym_1F_EventScript_GiveWaterPulse2::
	giveitem ITEM_TM_WATER_PULSE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	msgbox SootopolisCity_Gym_1F_Text_ExplainWaterPulse, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_WATER_PULSE
	release
	end

SootopolisCity_Gym_1F_EventScript_GoGetFortreeBadge::
	msgbox SootopolisCity_Gym_1F_Text_GoGetFortreeBadge, MSGBOX_DEFAULT
	release
	end

SootopolisCity_Gym_1F_EventScript_JuanRematch::
	trainerbattle_rematch_double TRAINER_JUAN_1, SootopolisCity_Gym_1F_Text_JuanPreRematch, SootopolisCity_Gym_1F_Text_JuanRematchDefeat, SootopolisCity_Gym_1F_Text_JuanRematchNeedTwoMons
	msgbox SootopolisCity_Gym_1F_Text_JuanPostRematch, MSGBOX_AUTOCLOSE
	end

SootopolisCity_Gym_1F_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_SOOTOPOLIS_GYM, SootopolisCity_Gym_1F_EventScript_GymGuidePostVictory
	msgbox SootopolisCity_Gym_1F_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

SootopolisCity_Gym_1F_EventScript_GymGuidePostVictory::
	msgbox SootopolisCity_Gym_1F_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	release
	end

SootopolisCity_Gym_1F_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_BADGE08_GET, SootopolisCity_Gym_1F_EventScript_GymStatueCertified
	goto SootopolisCity_Gym_1F_EventScript_GymStatue
	end

SootopolisCity_Gym_1F_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_BADGE08_GET, SootopolisCity_Gym_1F_EventScript_GymStatueCertified
	goto SootopolisCity_Gym_1F_EventScript_GymStatue
	end

SootopolisCity_Gym_1F_EventScript_GymStatueCertified::
	msgbox SootopolisCity_Gym_1F_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_Gym_1F_EventScript_GymStatue::
	msgbox SootopolisCity_Gym_1F_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_Gym_1F_Text_GymGuideAdvice:
	.string "Guide: AGUAS DE M'BOI GYM tests\n"
	.string "careful movement over ice.\p"
	.string "MS. CELINA values judgment more\n"
	.string "than speed. Watch every step.$"

SootopolisCity_Gym_1F_Text_GymGuidePostVictory:
	.string "You beat MS. CELINA!\p"
	.string "With all eight BADGES, OATH ROAD\n"
	.string "and the ARAUNA LEAGUE await.$"

SootopolisCity_Gym_1F_Text_JuanIntro:
	.string "MS. CELINA: Living means\n"
	.string "learning what to keep and what\n"
	.string "to let go.\p"
	.string "Choosing that for someone else\n"
	.string "is not ours to do.$"

@ NOTE: This defeat text actually causes a buffer overflow. It's about 50 bytes too long for
@ the gDisplayedStringBattle buffer that it's put into, and it stomps all over the gBattleTextBuffs
@ after, as well as the otherwise unused array after that. One wonders if that's the reason for
@ the existence of that unused array of ints.
SootopolisCity_Gym_1F_Text_JuanDefeat:
	.string "MS. CELINA: You knew when to\n"
	.string "hold and when to release.$"

SootopolisCity_Gym_1F_Text_ReceivedRainBadge:
	.string "{PLAYER} received the\n"
	.string "SPRING BADGE from MS. CELINA.$"

SootopolisCity_Gym_1F_Text_ExplainRainBadgeTakeThis:
	.string "The SPRING BADGE lets POKéMON\n"
	.string "use WATERFALL outside battle.\p"
	.string "Take this too, to remember our\n"
	.string "battle.$"

SootopolisCity_Gym_1F_Text_ExplainWaterPulse:
	.string "This TM contains WATER PULSE.\p"
	.string "It may confuse the target with\n"
	.string "ultrasonic waves.$"

SootopolisCity_Gym_1F_Text_RegisteredJuan:
	.string "Registered MS. CELINA in the\n"
	.string "POKéNAV.$"

SootopolisCity_Gym_1F_Text_JuanPostBattle:
	.string "MS. CELINA: Memory can be kept\n"
	.string "without becoming a cage.\p"
	.string "That balance is the lesson.$"

SootopolisCity_Gym_1F_Text_GoGetFortreeBadge:
	.string "One BADGE is still missing.\p"
	.string "Return after earning the MATA DO\n"
	.string "MEIO GYM BADGE.$"

SootopolisCity_Gym_1F_Text_GymStatue:
	.string "AGUAS DE M'BOI POKéMON GYM\p"
	.string "LEADER: MS. CELINA$"

SootopolisCity_Gym_1F_Text_GymStatueCertified:
	.string "AGUAS DE M'BOI POKéMON GYM\p"
	.string "MS. CELINA'S CERTIFIED\n"
	.string "TRAINERS: {PLAYER}$"

SootopolisCity_Gym_1F_Text_JuanPreRematch:
	.string "MS. CELINA: A lesson changes\n"
	.string "when you return to it.\p"
	.string "Show me what changed in you.$"

SootopolisCity_Gym_1F_Text_JuanRematchDefeat:
	.string "MS. CELINA: You found the\n"
	.string "balance again.$"

SootopolisCity_Gym_1F_Text_JuanPostRematch:
	.string "MS. CELINA: Keep choosing with\n"
	.string "care. No BADGE can do that for\n"
	.string "you.$"

SootopolisCity_Gym_1F_Text_JuanRematchNeedTwoMons:
	.string "MS. CELINA: Bring at least two\n"
	.string "POKéMON for this rematch.$"


SootopolisCity_Gym_1F_Text_ThreeMemoriesMissing:
	.string "MRS. CELINA: Hear the three voices\n"
	.string "below before you face me:\p"
	.string "the old bank, the new bank\n"
	.string "and the flooded archive.$"

SootopolisCity_Gym_1F_Text_MemoriesTogether:
	.string "MRS. CELINA: You heard all three.\p"
	.string "Rest your POKéMON here.\n"
	.string "If you fall, return through town.$"

SootopolisCity_Gym_1F_Text_ReturnToCity:
	.string "This return bridge leads\n"
	.string "back to town. Leave now?$"

SootopolisCity_Gym_1F_Text_OldCrossingClosed:
	.string "The old-bank crossing waits\n"
	.string "for BEATRIZ's account.$"

SootopolisCity_Gym_1F_Text_NewCrossingClosed:
	.string "The new-bank crossing waits\n"
	.string "for ELENA's account.$"

SootopolisCity_Gym_1F_Text_ArchiveCrossingClosed:
	.string "The last crossing holds\n"
	.string "CILENE's flooded record.$"

SootopolisCity_Gym_1F_Text_OldBankMural:
	.string "The old-bank mural lists\n"
	.string "families displaced by the dam.\p"
	.string "Several names were scratched\n"
	.string "out but can still be read.$"

SootopolisCity_Gym_1F_Text_NewBankMural:
	.string "The new-bank mural records\n"
	.string "homes saved from the flood.\p"
	.string "A corner marked COST has\n"
	.string "no names beside it.$"
