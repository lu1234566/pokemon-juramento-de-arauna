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
	.string "HORIZONTE: O diretor saiu para\nbuscar um componente essencial\p"
	.string "do ARQUIVO VIVO. Nao espere que\neu diga onde.$"

AquaHideout_1F_Text_WhereMightMagmaHideoutBe:
	.string "HORIZONTE: Os LEMBRANTES\nmontaram uma base perto da\p"
	.string "SERRA DA CINZA. Luzia quer\nchegar aos registros antes de\p"
	.string "nos.$"

AquaHideout_1F_Text_BossWentToJackASubmarine:
	.string "HORIZONTE: OTACILIO foi ao\nPORTO DO SAL. O submersivel\p"
	.string "consegue chegar as cavernas de\nM'BOI.$"

AquaHideout_1F_Text_BossIsOnRoute122:
	.string "HORIZONTE: OTACILIO seguiu para\no MEMORIAL DOS NOMES, na ROTA\p"
	.string "122. Ele quer os registros\nguardados la.$"

AquaHideout_1F_Text_TeamMagmaAtMtChimney:
	.string "HORIZONTE: Os LEMBRANTES estao\nna SERRA DA CINZA. Dizem que\p"
	.string "LUZIA pretende devolver\nmemorias extraidas a forca.$"

AquaHideout_1F_Text_BossIsInSlateportCity:
	.string "HORIZONTE: OTACILIO esta no\nPORTO DO SAL. A demonstracao\p"
	.string "publica do ARQUIVO VIVO comeca\nla.$"

AquaHideout_1F_Text_Grunt1Intro:
	.string "HORIZONTE: Os sensores detectam\nVINCULOS instaveis antes do\p"
	.string "DESENCANTO completo. Isso pode\nsalvar familias inteiras.$"

AquaHideout_1F_Text_Grunt1Defeat:
	.string "HORIZONTE: O ARQUIVO VIVO nao\napaga pessoas. Ele separa\p"
	.string "trauma de identidade. Pelo\nmenos e isso que nos ensinaram.$"

AquaHideout_1F_Text_Grunt1PostBattle:
	.string "HORIZONTE: Os sensores detectam\nVINCULOS instaveis antes do\p"
	.string "DESENCANTO completo. Isso pode\nsalvar familias inteiras.$"

