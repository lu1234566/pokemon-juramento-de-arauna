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
	.string "Os dados mostram picos de\nDESENCANTO perto de instalacoes\p"
	.string "que usam sensores de VINCULO em\ngrande escala.$"

Route119_WeatherInstitute_1F_Text_Grunt1Defeat:
	.string "Os dados mostram picos de\nDESENCANTO perto de instalacoes\p"
	.string "que usam sensores de VINCULO em\ngrande escala.$"

Route119_WeatherInstitute_1F_Text_Grunt1PostBattle:
	.string "O HORIZONTE veio buscar os\nservidores. Os dados daqui\p"
	.string "contradizem a versao oficial\nsobre a seguranca do ARQUIVO\p"
	.string "VIVO.$"

Route119_WeatherInstitute_1F_Text_Grunt4Intro:
	.string "Os pesquisadores cruzaram\nchuva, temperatura e relatos de\p"
	.string "perda de memoria. O clima nao\nexplica o padrao; a\p"
	.string "infraestrutura do ARQUIVO\nexplica melhor.$"

Route119_WeatherInstitute_1F_Text_Grunt4Defeat:
	.string "Os pesquisadores cruzaram\nchuva, temperatura e relatos de\p"
	.string "perda de memoria. O clima nao\nexplica o padrao; a\p"
	.string "infraestrutura do ARQUIVO\nexplica melhor.$"

Route119_WeatherInstitute_1F_Text_Grunt4PostBattle:
	.string "Os pesquisadores cruzaram\nchuva, temperatura e relatos de\p"
	.string "perda de memoria. O clima nao\nexplica o padrao; a\p"
	.string "infraestrutura do ARQUIVO\nexplica melhor.$"

Route119_WeatherInstitute_1F_Text_EveryoneWentUpstairs:
	.string "While I was sleeping, everyone went\n"
	.string "upstairs!$"

Route119_WeatherInstitute_1F_Text_WowYoureStrong:
	.string "Wow, you're really strong!\p"
	.string "I wish I could be a POKéMON TRAINER\n"
	.string "like you!$"

Route119_WeatherInstitute_1F_Text_ProfStudyingRain:
	.string "The PROFESSOR loves rain.\n"
	.string "That's a fact.\p"
	.string "But if it keeps raining, people will be in\n"
	.string "trouble. That's another fact.\p"
	.string "And thus, the PROFESSOR is studying\n"
	.string "if the rain can be put to good use.$"

Route119_WeatherInstitute_1F_Text_NoticingAbnormalWeather:
	.string "Os pesquisadores cruzaram\nchuva, temperatura e relatos de\p"
	.string "perda de memoria. O clima nao\nexplica o padrao; a\p"
	.string "infraestrutura do ARQUIVO\nexplica melhor.$"

Route119_WeatherInstitute_1F_Text_WhatWereAquasUpTo:
	.string "O HORIZONTE veio buscar os\nservidores. Os dados daqui\p"
	.string "contradizem a versao oficial\nsobre a seguranca do ARQUIVO\p"
	.string "VIVO.$"

Route119_WeatherInstitute_1F_Text_TakeRestInBed:
	.string "There's a bed…\n"
	.string "Let's take a rest.$"

