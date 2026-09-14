@ The Arauna quality-of-life menu, reached from START.
@
@ It is a script rather than a new C screen on purpose: multichoice already
@ handles the window, the cursor, the B button and the cancel row, and the
@ move relearner is itself driven from a script, so the two fit together with
@ no new UI code to go wrong.

AraunaQol_EventScript_Menu::
	lockall
	special AraunaSpecial_EggMoveModeOff
AraunaQol_EventScript_Choose::
	message AraunaQol_Text_WhatDoYouNeed
	waitmessage
	multichoice 0, 0, MULTI_ARAUNA_QOL, FALSE
	switch VAR_RESULT
	case 0, AraunaQol_EventScript_LevelCap
	case 1, AraunaQol_EventScript_Relearn
	case 2, AraunaQol_EventScript_EggMoves
	case 3, AraunaQol_EventScript_Storage
	case 4, AraunaQol_EventScript_Heal
	case 5, AraunaQol_EventScript_Done
	case MULTI_B_PRESSED, AraunaQol_EventScript_Done
	goto AraunaQol_EventScript_Done
	end

AraunaQol_EventScript_Done::
	special AraunaSpecial_EggMoveModeOff
	closemessage
	releaseall
	end

@ --- Level cap -------------------------------------------------------------

AraunaQol_EventScript_LevelCap::
	special AraunaSpecial_GetLevelCap
	buffernumberstring STR_VAR_1, VAR_RESULT
	msgbox AraunaQol_Text_LevelCapIs, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, AraunaQol_EventScript_Choose
	special AraunaSpecial_SetPartyToLevelCap
	goto_if_eq VAR_RESULT, 0, AraunaQol_EventScript_AlreadyAtCap
	buffernumberstring STR_VAR_2, VAR_RESULT
	msgbox AraunaQol_Text_PartyRaised, MSGBOX_DEFAULT
	goto AraunaQol_EventScript_Choose
	end

AraunaQol_EventScript_AlreadyAtCap::
	msgbox AraunaQol_Text_AlreadyAtCap, MSGBOX_DEFAULT
	goto AraunaQol_EventScript_Choose
	end

@ --- Move relearner --------------------------------------------------------
@ Same flow as the tutor in Campo das Cinzas, without the Heart Scale.

AraunaQol_EventScript_Relearn::
	special AraunaSpecial_EggMoveModeOff
	msgbox AraunaQol_Text_WhichPokemon, MSGBOX_DEFAULT
	special ChooseMonForMoveRelearner
	waitstate
	goto_if_eq VAR_0x8004, PARTY_NOTHING_CHOSEN, AraunaQol_EventScript_Choose
	special IsSelectedMonEgg
	goto_if_eq VAR_RESULT, TRUE, AraunaQol_EventScript_NotAnEgg
	goto_if_eq VAR_0x8005, 0, AraunaQol_EventScript_NothingToRelearn
	msgbox AraunaQol_Text_WhichMove, MSGBOX_DEFAULT
	special TeachMoveRelearnerMove
	waitstate
	goto_if_eq VAR_0x8004, 0, AraunaQol_EventScript_Relearn
	msgbox AraunaQol_Text_MoveRemembered, MSGBOX_DEFAULT
	goto AraunaQol_EventScript_Choose
	end

AraunaQol_EventScript_NothingToRelearn::
	msgbox AraunaQol_Text_NothingToRelearn, MSGBOX_DEFAULT
	goto AraunaQol_EventScript_Relearn
	end

@ --- Egg moves -------------------------------------------------------------
@ The same screen, pointed at the egg-move list instead.

AraunaQol_EventScript_EggMoves::
	special AraunaSpecial_EggMoveModeOn
	msgbox AraunaQol_Text_WhichPokemonEgg, MSGBOX_DEFAULT
	special ChooseMonForMoveRelearner
	waitstate
	goto_if_eq VAR_0x8004, PARTY_NOTHING_CHOSEN, AraunaQol_EventScript_Done
	special IsSelectedMonEgg
	goto_if_eq VAR_RESULT, TRUE, AraunaQol_EventScript_NotAnEgg
	goto_if_eq VAR_0x8005, 0, AraunaQol_EventScript_NoEggMoves
	msgbox AraunaQol_Text_WhichEggMove, MSGBOX_DEFAULT
	special TeachMoveRelearnerMove
	waitstate
	goto_if_eq VAR_0x8004, 0, AraunaQol_EventScript_EggMoves
	msgbox AraunaQol_Text_EggMoveTaught, MSGBOX_DEFAULT
	goto AraunaQol_EventScript_EggMoves
	end

AraunaQol_EventScript_NoEggMoves::
	msgbox AraunaQol_Text_NoEggMoves, MSGBOX_DEFAULT
	goto AraunaQol_EventScript_EggMoves
	end

AraunaQol_EventScript_NotAnEgg::
	msgbox AraunaQol_Text_NotAnEgg, MSGBOX_DEFAULT
	goto AraunaQol_EventScript_Choose
	end

@ --- Storage and healing ---------------------------------------------------

AraunaQol_EventScript_Storage::
	special AraunaSpecial_EggMoveModeOff
	msgbox AraunaQol_Text_AccessedStorage, MSGBOX_DEFAULT
	playse SE_PC_LOGIN
	special ShowPokemonStorageSystemPC
	waitstate
	goto AraunaQol_EventScript_Choose
	end

AraunaQol_EventScript_Heal::
	special AraunaSpecial_HealParty
	msgbox AraunaQol_Text_PartyHealed, MSGBOX_DEFAULT
	goto AraunaQol_EventScript_Choose
	end

@ --- Text ------------------------------------------------------------------

AraunaQol_Text_WhatDoYouNeed:
	.string "What do you need?$"

AraunaQol_Text_LevelCapIs:
	.string "The next one waiting for you tops out\n"
	.string "at level {STR_VAR_1}.\p"
	.string "Bring the team up to meet them?$"

AraunaQol_Text_PartyRaised:
	.string "{STR_VAR_2} of your POKéMON came up to\n"
	.string "level {STR_VAR_1}.$"

AraunaQol_Text_AlreadyAtCap::
	.string "They are already as ready as this\n"
	.string "stretch of road allows.$"

AraunaQol_Text_WhichPokemon:
	.string "Which POKéMON should remember\n"
	.string "something?$"

AraunaQol_Text_WhichMove:
	.string "Which move should come back?$"

AraunaQol_Text_MoveRemembered:
	.string "It remembered the move.$"

AraunaQol_Text_NothingToRelearn:
	.string "There is nothing back there for that\n"
	.string "one to remember yet.$"

AraunaQol_Text_WhichPokemonEgg:
	.string "Which POKéMON should reach for what\n"
	.string "its line carries?$"

AraunaQol_Text_WhichEggMove:
	.string "Which of them?$"

AraunaQol_Text_EggMoveTaught:
	.string "It learned the move.$"

AraunaQol_Text_NoEggMoves:
	.string "That line has nothing left to pass\n"
	.string "down to it.$"

AraunaQol_Text_NotAnEgg:
	.string "An EGG has nothing to remember yet.$"

AraunaQol_Text_AccessedStorage:
	.string "Opened the STORAGE SYSTEM.$"

AraunaQol_Text_PartyHealed:
	.string "Your POKéMON are rested and whole.$"
