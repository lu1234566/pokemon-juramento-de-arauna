SootopolisCity_House3_MapScripts::
	.byte 0

SootopolisCity_House3_EventScript_Woman::
	lock
	faceplayer
	msgbox SootopolisCity_House3_Text_JuanHasManyFansDoYou, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, SootopolisCity_House3_EventScript_HaveFans
	msgbox SootopolisCity_House3_Text_LonesomeTryWorkingHarder, MSGBOX_DEFAULT
	release
	end

SootopolisCity_House3_EventScript_HaveFans::
	msgbox SootopolisCity_House3_Text_YouMustBePrettyStrong, MSGBOX_DEFAULT
	release
	end

SootopolisCity_House3_EventScript_Girl::
	msgbox SootopolisCity_House3_Text_TrainerFanClubWasWild, MSGBOX_NPC
	end

SootopolisCity_House3_Text_JuanHasManyFansDoYou:
	.string "MS. CELINA has many people who\n"
	.string "seek her advice.\p"
	.string "Do people follow your battles\n"
	.string "too?$"

SootopolisCity_House3_Text_YouMustBePrettyStrong:
	.string "Then you must have made quite an\n"
	.string "impression.$"

SootopolisCity_House3_Text_LonesomeTryWorkingHarder:
	.string "Not yet? That is all right.\p"
	.string "A reputation should follow your\n"
	.string "actions, not the other way\n"
	.string "around.$"

SootopolisCity_House3_Text_TrainerFanClubWasWild:
	.string "People come from across ARAUNA\n"
	.string "to talk about strong TRAINERS.\p"
	.string "The loudest stories are not\n"
	.string "always the truest ones.$"

