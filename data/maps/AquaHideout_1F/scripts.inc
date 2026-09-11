AquaHideout_1F_MapScripts::
	.byte 0

@ The below two entrance guards give hints about what to do to progress the story
AquaHideout_1F_EventScript_HideoutEntranceGrunt1::
	lock
	faceplayer
	goto_if_set FLAG_GROUDON_AWAKENED_MAGMA_HIDEOUT, AquaHideout_1F_EventScript_SlateportHint1
	goto_if_set FLAG_RECEIVED_RED_OR_BLUE_ORB, AquaHideout_1F_EventScript_MagmaHideoutHint1
	msgbox AquaHideout_1F_Text_OurBossIsSnatchingSomething, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_MagmaHideoutHint1::
	msgbox AquaHideout_1F_Text_WhereMightMagmaHideoutBe, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_SlateportHint1::
	msgbox AquaHideout_1F_Text_BossWentToJackASubmarine, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_HideoutEntranceGrunt2::
	lock
	faceplayer
	goto_if_set FLAG_GROUDON_AWAKENED_MAGMA_HIDEOUT, AquaHideout_1F_EventScript_SlateportHint2
	goto_if_set FLAG_RECEIVED_RED_OR_BLUE_ORB, AquaHideout_1F_EventScript_MagmaHideoutHint2
	msgbox AquaHideout_1F_Text_BossIsOnRoute122, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_MagmaHideoutHint2::
	msgbox AquaHideout_1F_Text_TeamMagmaAtMtChimney, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_SlateportHint2::
	msgbox AquaHideout_1F_Text_BossIsInSlateportCity, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_Grunt1::
	trainerbattle_single TRAINER_GRUNT_AQUA_HIDEOUT_1, AquaHideout_1F_Text_Grunt1Intro, AquaHideout_1F_Text_Grunt1Defeat, AquaHideout_1F_EventScript_Grunt1Defeated
	msgbox AquaHideout_1F_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

AquaHideout_1F_EventScript_Grunt1Defeated::
	msgbox AquaHideout_1F_Text_Grunt1PostBattle, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_Text_OurBossIsSnatchingSomething:
	.string "HORIZON: O diretor saiu para\n"
	.string "buscar um componente essencial\p"
	.string "do LIVING ARCHIVE. Nao espere que\n"
	.string "eu diga onde.$"

AquaHideout_1F_Text_WhereMightMagmaHideoutBe:
	.string "HORIZON: Os REMEMBRANCERS\n"
	.string "montaram uma base perto da\p"
	.string "SERRA DA CINZA. Luzia quer\n"
	.string "chegar aos registros antes de\p"
	.string "nos.$"

AquaHideout_1F_Text_BossWentToJackASubmarine:
	.string "HORIZON: OTACILIO foi ao\n"
	.string "PORTO DO SAL. O submersivel\p"
	.string "consegue chegar as cavernas de\n"
	.string "M'BOI.$"

AquaHideout_1F_Text_BossIsOnRoute122:
	.string "HORIZON: OTACILIO seguiu para\n"
	.string "o MEMORIAL DOS NOMES, na ROTA\p"
	.string "122. Ele quer os registros\n"
	.string "guardados la.$"

AquaHideout_1F_Text_TeamMagmaAtMtChimney:
	.string "HORIZON: Os REMEMBRANCERS estao\n"
	.string "na SERRA DA CINZA. Dizem que\p"
	.string "LUZIA pretende devolver\n"
	.string "memorias extraidas a forca.$"

AquaHideout_1F_Text_BossIsInSlateportCity:
	.string "HORIZON: OTACILIO esta no\n"
	.string "PORTO DO SAL. A demonstracao\p"
	.string "publica do LIVING ARCHIVE comeca\n"
	.string "la.$"

AquaHideout_1F_Text_Grunt1Intro:
	.string "HORIZON: Os sensores detectam\n"
	.string "BONDS instaveis antes do\p"
	.string "DISENCHANTMENT completo. Isso pode\n"
	.string "salvar familias inteiras.$"

AquaHideout_1F_Text_Grunt1Defeat:
	.string "HORIZON: O LIVING ARCHIVE nao\n"
	.string "apaga pessoas. Ele separa\p"
	.string "trauma de identidade. Pelo\n"
	.string "menos e isso que nos ensinaram.$"

AquaHideout_1F_Text_Grunt1PostBattle:
	.string "HORIZON: Os sensores detectam\n"
	.string "BONDS instaveis antes do\p"
	.string "DISENCHANTMENT completo. Isso pode\n"
	.string "salvar familias inteiras.$"

