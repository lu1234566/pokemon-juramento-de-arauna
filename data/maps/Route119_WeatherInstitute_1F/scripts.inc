Route119_WeatherInstitute_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route119_WeatherInstitute_1F_OnTransition
	.byte 0

Route119_WeatherInstitute_1F_OnTransition:
	call_if_eq VAR_WEATHER_INSTITUTE_STATE, 0, Route119_WeatherInstitute_1F_EventScript_SetLittleBoyPos
	end

Route119_WeatherInstitute_1F_EventScript_SetLittleBoyPos::
	setobjectxyperm LOCALID_WEATHER_INSTITUTE_LITTLE_BOY, 0, 5
	setobjectmovementtype LOCALID_WEATHER_INSTITUTE_LITTLE_BOY, MOVEMENT_TYPE_FACE_RIGHT
	return

Route119_WeatherInstitute_1F_EventScript_LittleBoy::
	lock
	faceplayer
	special GetPlayerBigGuyGirlString
	goto_if_eq VAR_WEATHER_INSTITUTE_STATE, 0, Route119_WeatherInstitute_1F_EventScript_LittleBoyTeamAquaHere
	msgbox Route119_WeatherInstitute_1F_Text_WowYoureStrong, MSGBOX_DEFAULT
	release
	end

Route119_WeatherInstitute_1F_EventScript_LittleBoyTeamAquaHere::
	msgbox Route119_WeatherInstitute_1F_Text_EveryoneWentUpstairs, MSGBOX_DEFAULT
	release
	end

Route119_WeatherInstitute_1F_EventScript_InstituteWorker1::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, Route119_WeatherInstitute_1F_EventScript_StudyingRain
	setvar VAR_0x8004, 0
	call_if_set FLAG_DEFEATED_KYOGRE, Route119_WeatherInstitute_1F_EventScript_LegendaryDefeated
	call_if_set FLAG_DEFEATED_GROUDON, Route119_WeatherInstitute_1F_EventScript_LegendaryDefeated
	goto_if_eq VAR_0x8004, 2, Route119_WeatherInstitute_1F_EventScript_StudyingRain  @ Both defeated
	msgbox Route119_WeatherInstitute_1F_Text_NoticingAbnormalWeather, MSGBOX_DEFAULT
	release
	end

Route119_WeatherInstitute_1F_EventScript_LegendaryDefeated::
	addvar VAR_0x8004, 1
	return

Route119_WeatherInstitute_1F_EventScript_StudyingRain::
	msgbox Route119_WeatherInstitute_1F_Text_ProfStudyingRain, MSGBOX_DEFAULT
	release
	end

Route119_WeatherInstitute_1F_EventScript_InstituteWorker2::
	msgbox Route119_WeatherInstitute_1F_Text_WhatWereAquasUpTo, MSGBOX_NPC
	end

Route119_WeatherInstitute_1F_EventScript_Bed::
	lockall
	msgbox Route119_WeatherInstitute_1F_Text_TakeRestInBed, MSGBOX_DEFAULT
	closemessage
	call Common_EventScript_OutOfCenterPartyHeal
	releaseall
	end

Route119_WeatherInstitute_1F_EventScript_Grunt1::
	trainerbattle_single TRAINER_GRUNT_WEATHER_INST_1, Route119_WeatherInstitute_1F_Text_Grunt1Intro, Route119_WeatherInstitute_1F_Text_Grunt1Defeat
	msgbox Route119_WeatherInstitute_1F_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

Route119_WeatherInstitute_1F_EventScript_Grunt4::
	trainerbattle_single TRAINER_GRUNT_WEATHER_INST_4, Route119_WeatherInstitute_1F_Text_Grunt4Intro, Route119_WeatherInstitute_1F_Text_Grunt4Defeat
	msgbox Route119_WeatherInstitute_1F_Text_Grunt4PostBattle, MSGBOX_AUTOCLOSE
	end

Route119_WeatherInstitute_1F_Text_Grunt1Intro:
	.string "These servers were not built\n"
	.string "for weather alone.\p"
	.string "They track DISENCHANTMENT\n"
	.string "near large BOND arrays.$"

Route119_WeatherInstitute_1F_Text_Grunt1Defeat:
	.string "So that's what the logs show...$"

Route119_WeatherInstitute_1F_Text_Grunt1PostBattle:
	.string "HORIZON wants the servers.\p"
	.string "These records challenge their\n"
	.string "LIVING ARCHIVE safety claims.$"

Route119_WeatherInstitute_1F_Text_Grunt4Intro:
	.string "They crossed rain, heat and\n"
	.string "memory-loss reports.\p"
	.string "Weather doesn't fit the pattern.\p"
	.string "The LIVING ARCHIVE does.$"

Route119_WeatherInstitute_1F_Text_Grunt4Defeat:
	.string "Then the pattern is real...$"

Route119_WeatherInstitute_1F_Text_Grunt4PostBattle:
	.string "Someone buried this on purpose.$"

Route119_WeatherInstitute_1F_Text_EveryoneWentUpstairs:
	.string "I was asleep when they came in.\n"
	.string "Everyone ran upstairs!$"

Route119_WeatherInstitute_1F_Text_WowYoureStrong:
	.string "Wow! You are really strong!\p"
	.string "I want to train POKéMON too!$"

Route119_WeatherInstitute_1F_Text_ProfStudyingRain:
	.string "Our lead researcher tracks rain.\p"
	.string "If we understand a storm early,\n"
	.string "we can warn people in time.$"

Route119_WeatherInstitute_1F_Text_NoticingAbnormalWeather:
	.string "The instruments are reading\n"
	.string "weather with no natural source.\p"
	.string "Something under Arauna is\n"
	.string "forcing the pattern.$"

Route119_WeatherInstitute_1F_Text_WhatWereAquasUpTo:
	.string "HORIZON came for the servers.\p"
	.string "They called it a safety review.\p"
	.string "It was not.$"

Route119_WeatherInstitute_1F_Text_TakeRestInBed:
	.string "There is a bed...\n"
	.string "A short rest should help.$"

