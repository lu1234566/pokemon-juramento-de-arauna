RustboroCity_PokemonSchool_MapScripts::
	.byte 0

RustboroCity_PokemonSchool_EventScript_Blackboard::
	lockall
	msgbox RustboroCity_PokemonSchool_Text_BlackboardListsStatusChanges, MSGBOX_DEFAULT
	goto RustboroCity_PokemonSchool_EventScript_ChooseBlackboardTopic
	end

RustboroCity_PokemonSchool_EventScript_ChooseBlackboardTopic::
	message RustboroCity_PokemonSchool_Text_ReadWhichTopic
	waitmessage
	multichoicegrid 8, 1, MULTI_STATUS_INFO, 3, FALSE
	switch VAR_RESULT
	case 0, RustboroCity_PokemonSchool_EventScript_Poison
	case 1, RustboroCity_PokemonSchool_EventScript_Paralysis
	case 2, RustboroCity_PokemonSchool_EventScript_Sleep
	case 3, RustboroCity_PokemonSchool_EventScript_Burn
	case 4, RustboroCity_PokemonSchool_EventScript_Freeze
	case 5, RustboroCity_PokemonSchool_EventScript_ExitTopicSelect
	case MULTI_B_PRESSED, RustboroCity_PokemonSchool_EventScript_ExitTopicSelect
	end

RustboroCity_PokemonSchool_EventScript_Poison::
	msgbox RustboroCity_PokemonSchool_Text_ExplainPoison, MSGBOX_DEFAULT
	goto RustboroCity_PokemonSchool_EventScript_ChooseBlackboardTopic
	end

RustboroCity_PokemonSchool_EventScript_Paralysis::
	msgbox RustboroCity_PokemonSchool_Text_ExplainParalysis, MSGBOX_DEFAULT
	goto RustboroCity_PokemonSchool_EventScript_ChooseBlackboardTopic
	end

RustboroCity_PokemonSchool_EventScript_Sleep::
	msgbox RustboroCity_PokemonSchool_Text_ExplainSleep, MSGBOX_DEFAULT
	goto RustboroCity_PokemonSchool_EventScript_ChooseBlackboardTopic
	end

RustboroCity_PokemonSchool_EventScript_Burn::
	msgbox RustboroCity_PokemonSchool_Text_ExplainBurn, MSGBOX_DEFAULT
	goto RustboroCity_PokemonSchool_EventScript_ChooseBlackboardTopic
	end

RustboroCity_PokemonSchool_EventScript_Freeze::
	msgbox RustboroCity_PokemonSchool_Text_ExplainFreeze, MSGBOX_DEFAULT
	goto RustboroCity_PokemonSchool_EventScript_ChooseBlackboardTopic
	end

RustboroCity_PokemonSchool_EventScript_ExitTopicSelect::
	releaseall
	end

RustboroCity_PokemonSchool_EventScript_GameboyKid1::
	msgbox RustboroCity_PokemonSchool_Text_TradingRightNow, MSGBOX_NPC
	end

RustboroCity_PokemonSchool_EventScript_GameboyKid2::
	msgbox RustboroCity_PokemonSchool_Text_AlwaysWantedSeedot, MSGBOX_NPC
	end

RustboroCity_PokemonSchool_EventScript_RichBoy::
	msgbox RustboroCity_PokemonSchool_Text_PokemontCantUseManMadeItems, MSGBOX_NPC
	end

RustboroCity_PokemonSchool_EventScript_Lass::
	msgbox RustboroCity_PokemonSchool_Text_ConfusedPokemonAttacksItself, MSGBOX_NPC
	end

RustboroCity_PokemonSchool_EventScript_SchoolKidM::
	msgbox RustboroCity_PokemonSchool_Text_PokemonHealItselfWithBerry, MSGBOX_NPC
	end

RustboroCity_PokemonSchool_EventScript_StudentNotebook::
	msgbox RustboroCity_PokemonSchool_Text_StudentsNotes, MSGBOX_SIGN
	end

RustboroCity_PokemonSchool_EventScript_Teacher::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_QUICK_CLAW, RustboroCity_PokemonSchool_EventScript_GaveQuickClaw
	call_if_eq VAR_FACING, DIR_EAST, RustboroCity_PokemonSchool_EventScript_TeacherCheckOnStudentsEast
	call_if_eq VAR_FACING, DIR_WEST, RustboroCity_PokemonSchool_EventScript_TeacherCheckOnStudentsWest
	msgbox RustboroCity_PokemonSchool_Text_StudentsWhoDontStudyGetQuickClaw, MSGBOX_DEFAULT
	giveitem ITEM_QUICK_CLAW
	goto_if_eq VAR_RESULT, 0, Common_EventScript_ShowBagIsFull
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	setflag FLAG_RECEIVED_QUICK_CLAW
	release
	end

RustboroCity_PokemonSchool_EventScript_TeacherCheckOnStudentsEast::
	applymovement VAR_LAST_TALKED, RustboroCity_PokemonSchool_Movement_TeacherCheckOnStudentsEast
	waitmovement 0
	return

RustboroCity_PokemonSchool_EventScript_TeacherCheckOnStudentsWest::
	applymovement VAR_LAST_TALKED, RustboroCity_PokemonSchool_Movement_TeacherCheckOnStudentsWest
	waitmovement 0
	return

RustboroCity_PokemonSchool_EventScript_GaveQuickClaw::
	msgbox RustboroCity_PokemonSchool_Text_ExplainQuickClaw, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	release
	end

RustboroCity_PokemonSchool_Movement_TeacherCheckOnStudentsWest:
	walk_left
	walk_down
	walk_down
	walk_right
	walk_in_place_faster_down
	delay_16
	delay_16
	delay_16
	walk_down
	walk_in_place_faster_left
	delay_16
	delay_16
	walk_right
	delay_16
	delay_16
	delay_8
	walk_up
	walk_left
	walk_left
	walk_up
	walk_up
	walk_right
	step_end

RustboroCity_PokemonSchool_Movement_TeacherCheckOnStudentsEast:
	walk_right
	walk_right
	walk_down
	walk_down
	walk_left
	walk_left
	walk_in_place_faster_down
	delay_16
	delay_16
	delay_16
	walk_down
	walk_in_place_faster_left
	delay_16
	delay_16
	walk_right
	delay_16
	delay_16
	delay_8
	walk_up
	walk_right
	walk_up
	walk_up
	walk_left
	walk_left
	step_end

RustboroCity_PokemonSchool_EventScript_Scott::
	lock
	faceplayer
	goto_if_set FLAG_MET_SCOTT_AFTER_OBTAINING_STONE_BADGE, RustboroCity_PokemonSchool_EventScript_ScottWatchStudents
	goto_if_set FLAG_MET_SCOTT_RUSTBORO, RustboroCity_PokemonSchool_EventScript_ScottSpokeAlready
	goto_if_set FLAG_BADGE01_GET, RustboroCity_PokemonSchool_EventScript_ScottGreetHasBadge
	msgbox RustboroCity_PokemonSchool_Text_ScottMetAlreadyCut, MSGBOX_DEFAULT
	addvar VAR_SCOTT_STATE, 1
	setflag FLAG_MET_SCOTT_RUSTBORO
	release
	end

RustboroCity_PokemonSchool_EventScript_ScottSpokeAlready::
	goto_if_set FLAG_BADGE01_GET, RustboroCity_PokemonSchool_EventScript_ScottNoticeBadge
	msgbox RustboroCity_PokemonSchool_Text_StudentTalentLevelUnknown, MSGBOX_DEFAULT
	release
	end

RustboroCity_PokemonSchool_EventScript_ScottGreetHasBadge::
	msgbox RustboroCity_PokemonSchool_Text_ScottMetAlreadyStoneBadge, MSGBOX_DEFAULT
	goto RustboroCity_PokemonSchool_EventScript_MetScottAfterBadge
	end

RustboroCity_PokemonSchool_EventScript_ScottNoticeBadge::
	msgbox RustboroCity_PokemonSchool_Text_ScottStoneBadge, MSGBOX_DEFAULT
	goto RustboroCity_PokemonSchool_EventScript_MetScottAfterBadge
	end

RustboroCity_PokemonSchool_EventScript_MetScottAfterBadge::
	addvar VAR_SCOTT_STATE, 1
	setflag FLAG_MET_SCOTT_AFTER_OBTAINING_STONE_BADGE
	release
	end

RustboroCity_PokemonSchool_EventScript_ScottWatchStudents::
	msgbox RustboroCity_PokemonSchool_Text_StudentTalentLevelUnknown, MSGBOX_DEFAULT
	release
	end

RustboroCity_PokemonSchool_Text_BlackboardListsStatusChanges:
	.string "CIRO: O futuro nao espera por\nquem vive olhando para tras.\p"
	.string "Pelo menos era nisso que eu\nacreditava.$"

RustboroCity_PokemonSchool_Text_ReadWhichTopic:
	.string "Voce vai continuar mesmo\nsabendo que SERRA DO UIVO\p"
	.string "guarda partes da historia que\nmuita gente preferia deixar\p"
	.string "enterradas?$"

RustboroCity_PokemonSchool_Text_ExplainPoison:
	.string "O HORIZONTE consertou a estrada\ndaqui. Nao sei se isso torna\p"
	.string "mais facil perguntar o que\nexiste debaixo dela.$"

RustboroCity_PokemonSchool_Text_ExplainParalysis:
	.string "CIRO: O futuro nao espera por\nquem vive olhando para tras.\p"
	.string "Pelo menos era nisso que eu\nacreditava.$"

RustboroCity_PokemonSchool_Text_ExplainSleep:
	.string "CIRO: O futuro nao espera por\nquem vive olhando para tras.\p"
	.string "Pelo menos era nisso que eu\nacreditava.$"

RustboroCity_PokemonSchool_Text_ExplainBurn:
	.string "Dona Zila diz que uma historia\nmuda toda vez que e contada.\p"
	.string "Talvez seja por isso que ainda\nesta viva.$"

RustboroCity_PokemonSchool_Text_ExplainFreeze:
	.string "Meu avo dizia que lembrar\ntambem cansa. Mas escolher pelo\p"
	.string "outro o que ele deve esquecer\nparece pior.$"

RustboroCity_PokemonSchool_Text_StudentsWhoDontStudyGetQuickClaw:
	.string "Dona Zila diz que uma historia\nmuda toda vez que e contada.\p"
	.string "Talvez seja por isso que ainda\nesta viva.$"

RustboroCity_PokemonSchool_Text_ExplainQuickClaw:
	.string "Meu avo dizia que lembrar\ntambem cansa. Mas escolher pelo\p"
	.string "outro o que ele deve esquecer\nparece pior.$"

RustboroCity_PokemonSchool_Text_TradingRightNow:
	.string "Ultimamente alguns Pokemon\nparam diante de suas antigas\p"
	.string "casas como se nunca tivessem\nestado ali.$"

RustboroCity_PokemonSchool_Text_AlwaysWantedSeedot:
	.string "Voce vai continuar mesmo\nsabendo que SERRA DO UIVO\p"
	.string "guarda partes da historia que\nmuita gente preferia deixar\p"
	.string "enterradas?$"

RustboroCity_PokemonSchool_Text_PokemontCantUseManMadeItems:
	.string "Existem placas novas por toda\nparte. Curioso e que alguns\p"
	.string "nomes antigos desapareceram\nquando elas chegaram.$"

RustboroCity_PokemonSchool_Text_ConfusedPokemonAttacksItself:
	.string "Voce vai continuar mesmo\nsabendo que SERRA DO UIVO\p"
	.string "guarda partes da historia que\nmuita gente preferia deixar\p"
	.string "enterradas?$"

RustboroCity_PokemonSchool_Text_PokemonHealItselfWithBerry:
	.string "A POKéMON holding a BERRY will heal\n"
	.string "itself…\p"
	.string "There are many kinds of items that\n"
	.string "POKéMON can hold…\p"
	.string "Boy, it sure is hard taking notes\n"
	.string "down…$"

RustboroCity_PokemonSchool_Text_StudentsNotes:
	.string "Ultimamente alguns Pokemon\nparam diante de suas antigas\p"
	.string "casas como se nunca tivessem\nestado ali.$"

RustboroCity_PokemonSchool_Text_ScottMetAlreadyCut:
	.string "Hello? Didn't we meet before?\n"
	.string "I think back in PETALBURG CITY.\p"
	.string "Let me introduce myself.\n"
	.string "My name's SCOTT.\p"
	.string "I've been traveling everywhere in\n"
	.string "search of outstanding TRAINERS.\p"
	.string "More specifically, I'm looking for\n"
	.string "POKéMON battle experts.\p"
	.string "So, what brings you to this SCHOOL?\n"
	.string "Are you a TRAINER, too?\p"
	.string "The first thing you should do is to\n"
	.string "have a POKéMON learn the move CUT.\p"
	.string "If I remember correctly, someone in\n"
	.string "this town has CUT.$"

RustboroCity_PokemonSchool_Text_StudentTalentLevelUnknown:
	.string "Existem placas novas por toda\nparte. Curioso e que alguns\p"
	.string "nomes antigos desapareceram\nquando elas chegaram.$"

RustboroCity_PokemonSchool_Text_ScottStoneBadge:
	.string "Voce vai continuar mesmo\nsabendo que SERRA DO UIVO\p"
	.string "guarda partes da historia que\nmuita gente preferia deixar\p"
	.string "enterradas?$"

RustboroCity_PokemonSchool_Text_ScottMetAlreadyStoneBadge:
	.string "Hello? Didn't we meet before?\n"
	.string "I think back in PETALBURG CITY.\p"
	.string "Let me introduce myself.\n"
	.string "My name's SCOTT.\p"
	.string "I've been traveling everywhere in\n"
	.string "search of outstanding TRAINERS.\p"
	.string "More specifically, I'm looking for\n"
	.string "POKéMON battle experts.\p"
	.string "Oh, what's that?\n"
	.string "It's a STONE BADGE, isn't it?\p"
	.string "That's pretty impressive, I'd say, for\n"
	.string "a starting TRAINER like yourself.\p"
	.string "But, you know, I would've loved to see\n"
	.string "you in battle.\p"
	.string "It's hard to tell what you're like as\n"
	.string "a TRAINER from a LEAGUE BADGE.$"

