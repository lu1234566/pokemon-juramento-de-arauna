MagmaHideout_3F_2R_MapScripts::
	.byte 0

MagmaHideout_3F_2R_EventScript_Grunt10::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_10, MagmaHideout_3F_2R_Text_Grunt10Intro, MagmaHideout_3F_2R_Text_Grunt10Defeat
	msgbox MagmaHideout_3F_2R_Text_Grunt10PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_3F_2R_Text_Grunt10Intro:
	.string "REMEMBRANCER: RAUL sealed the\n"
	.string "access.\p"
	.string "The activation has started.$"

MagmaHideout_3F_2R_Text_Grunt10Defeat:
	.string "REMEMBRANCER: I should be up\n"
	.string "there helping.\p"
	.string "Part of me is relieved I'm not.$"

MagmaHideout_3F_2R_Text_Grunt10PostBattle:
	.string "REMEMBRANCER: Don't let HORIZON\n"
	.string "take the MATRIX.\p"
	.string "Don't let LUZIA use it without\n"
	.string "limits either.$"

