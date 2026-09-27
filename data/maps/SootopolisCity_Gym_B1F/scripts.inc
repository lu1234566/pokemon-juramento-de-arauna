SootopolisCity_Gym_B1F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, SootopolisCity_Gym_B1F_OnLoad
	.byte 0

SootopolisCity_Gym_B1F_OnLoad:
	call_if_defeated TRAINER_ANDREA, SootopolisCity_Gym_B1F_EventScript_OpenOldBankGate
	call_if_defeated TRAINER_DAPHNE, SootopolisCity_Gym_B1F_EventScript_OpenNewBankGate
	end

SootopolisCity_Gym_B1F_EventScript_OpenOldBankGate::
	setmetatile 8, 16, 0x20F, FALSE
	return

SootopolisCity_Gym_B1F_EventScript_OpenNewBankGate::
	setmetatile 8, 11, 0x20F, FALSE
	return

SootopolisCity_Gym_B1F_EventScript_Andrea::
	trainerbattle_single TRAINER_ANDREA, SootopolisCity_Gym_B1F_Text_AndreaIntro, SootopolisCity_Gym_B1F_Text_AndreaDefeat
	call SootopolisCity_Gym_B1F_EventScript_OpenOldBankGate
	special DrawWholeMapView
	msgbox SootopolisCity_Gym_B1F_Text_AndreaPostBattle, MSGBOX_AUTOCLOSE
	end

SootopolisCity_Gym_B1F_EventScript_Crissy::
	trainerbattle_single TRAINER_CRISSY, SootopolisCity_Gym_B1F_Text_CrissyIntro, SootopolisCity_Gym_B1F_Text_CrissyDefeat
	msgbox SootopolisCity_Gym_B1F_Text_CrissyPostBattle, MSGBOX_AUTOCLOSE
	end

SootopolisCity_Gym_B1F_EventScript_Brianna::
	goto_if_not_defeated TRAINER_DAPHNE, SootopolisCity_Gym_B1F_EventScript_NeedNewBank
	trainerbattle_single TRAINER_BRIANNA, SootopolisCity_Gym_B1F_Text_BriannaIntro, SootopolisCity_Gym_B1F_Text_BriannaDefeat
	msgbox SootopolisCity_Gym_B1F_Text_BriannaPostBattle, MSGBOX_AUTOCLOSE
	end

SootopolisCity_Gym_B1F_EventScript_NeedNewBank::
	msgbox SootopolisCity_Gym_B1F_Text_NeedNewBank, MSGBOX_DEFAULT
	release
	end

SootopolisCity_Gym_B1F_EventScript_NeedOldBank::
	msgbox SootopolisCity_Gym_B1F_Text_NeedOldBank, MSGBOX_DEFAULT
	release
	end

SootopolisCity_Gym_B1F_EventScript_Connie::
	trainerbattle_single TRAINER_CONNIE, SootopolisCity_Gym_B1F_Text_ConnieIntro, SootopolisCity_Gym_B1F_Text_ConnieDefeat
	msgbox SootopolisCity_Gym_B1F_Text_ConniePostBattle, MSGBOX_AUTOCLOSE
	end

SootopolisCity_Gym_B1F_EventScript_Bridget::
	trainerbattle_single TRAINER_BRIDGET, SootopolisCity_Gym_B1F_Text_BridgetIntro, SootopolisCity_Gym_B1F_Text_BridgetDefeat
	msgbox SootopolisCity_Gym_B1F_Text_BridgetPostBattle, MSGBOX_AUTOCLOSE
	end

SootopolisCity_Gym_B1F_EventScript_Olivia::
	trainerbattle_single TRAINER_OLIVIA, SootopolisCity_Gym_B1F_Text_OliviaIntro, SootopolisCity_Gym_B1F_Text_OliviaDefeat
	msgbox SootopolisCity_Gym_B1F_Text_OliviaPostBattle, MSGBOX_AUTOCLOSE
	end

SootopolisCity_Gym_B1F_EventScript_Tiffany::
	trainerbattle_single TRAINER_TIFFANY, SootopolisCity_Gym_B1F_Text_TiffanyIntro, SootopolisCity_Gym_B1F_Text_TiffanyDefeat
	msgbox SootopolisCity_Gym_B1F_Text_TiffanyPostBattle, MSGBOX_AUTOCLOSE
	end

SootopolisCity_Gym_B1F_EventScript_Bethany::
	trainerbattle_single TRAINER_BETHANY, SootopolisCity_Gym_B1F_Text_BethanyIntro, SootopolisCity_Gym_B1F_Text_BethanyDefeat
	msgbox SootopolisCity_Gym_B1F_Text_BethanyPostBattle, MSGBOX_AUTOCLOSE
	end

SootopolisCity_Gym_B1F_EventScript_Annika::
	trainerbattle_single TRAINER_ANNIKA, SootopolisCity_Gym_B1F_Text_AnnikaIntro, SootopolisCity_Gym_B1F_Text_AnnikaDefeat
	msgbox SootopolisCity_Gym_B1F_Text_AnnikaPostBattle, MSGBOX_AUTOCLOSE
	end

SootopolisCity_Gym_B1F_EventScript_Daphne::
	goto_if_not_defeated TRAINER_ANDREA, SootopolisCity_Gym_B1F_EventScript_NeedOldBank
	trainerbattle_single TRAINER_DAPHNE, SootopolisCity_Gym_B1F_Text_DaphneIntro, SootopolisCity_Gym_B1F_Text_DaphneDefeat
	call SootopolisCity_Gym_B1F_EventScript_OpenNewBankGate
	special DrawWholeMapView
	msgbox SootopolisCity_Gym_B1F_Text_DaphnePostBattle, MSGBOX_AUTOCLOSE
	end

SootopolisCity_Gym_B1F_EventScript_OldBankGate::
	lockall
	getplayerxy VAR_0x8004, VAR_0x8005
	goto_if_lt VAR_0x8005, 16, SootopolisCity_Gym_B1F_EventScript_OldBankGateOpen
	goto_if_defeated TRAINER_ANDREA, SootopolisCity_Gym_B1F_EventScript_OldBankGateOpen
	msgbox SootopolisCity_Gym_B1F_Text_OldBankGateClosed, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_Gym_B1F_EventScript_OldBankGateOpen::
	call SootopolisCity_Gym_B1F_EventScript_OpenOldBankGate
	special DrawWholeMapView
	releaseall
	end

SootopolisCity_Gym_B1F_EventScript_NewBankGate::
	lockall
	getplayerxy VAR_0x8004, VAR_0x8005
	goto_if_lt VAR_0x8005, 11, SootopolisCity_Gym_B1F_EventScript_NewBankGateOpen
	goto_if_defeated TRAINER_DAPHNE, SootopolisCity_Gym_B1F_EventScript_NewBankGateOpen
	msgbox SootopolisCity_Gym_B1F_Text_NewBankGateClosed, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_Gym_B1F_EventScript_NewBankGateOpen::
	call SootopolisCity_Gym_B1F_EventScript_OpenNewBankGate
	special DrawWholeMapView
	releaseall
	end

SootopolisCity_Gym_B1F_EventScript_FloodedRecords::
	lockall
	msgbox SootopolisCity_Gym_B1F_Text_FloodedRecords, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_Gym_B1F_Text_NeedOldBank:
	.string "Hear BEATRIZ on the old bank\n"
	.string "before you ask for my story.$"

SootopolisCity_Gym_B1F_Text_NeedNewBank:
	.string "Hear ELENA on the new bank\n"
	.string "before you read the archive.$"

SootopolisCity_Gym_B1F_Text_OldBankGateClosed:
	.string "The first gate is shut.\p"
	.string "An old-bank name is carved\n"
	.string "into the stone: BEATRIZ.$"

SootopolisCity_Gym_B1F_Text_NewBankGateClosed:
	.string "The second gate is shut.\p"
	.string "ELENA's testimony opens\n"
	.string "this crossing.$"

SootopolisCity_Gym_B1F_Text_FloodedRecords:
	.string "Names from both banks share\n"
	.string "the same soaked page.\p"
	.string "The vote named fewer people\n"
	.string "than the river took.$"

SootopolisCity_Gym_B1F_Text_AndreaIntro:
	.string "BEATRIZ: On the old bank the\n"
	.string "river was a road for everyone.\p"
	.string "I fight for the people\n"
	.string "erased from the maps.$"

SootopolisCity_Gym_B1F_Text_AndreaDefeat:
	.string "BEATRIZ: Water does not forget.$"

SootopolisCity_Gym_B1F_Text_AndreaPostBattle:
	.string "Our bank was here before the\n"
	.string "gates. The other bank's records\l"
	.string "nearly erased our names.\p"
	.string "The old-bank gate is open.\n"
	.string "Cross to the next testimony.$"

SootopolisCity_Gym_B1F_Text_CrissyIntro:
	.string "You have come all this way and you\n"
	.string "will not get to see CELINA.\p"
	.string "Not if you lose to me\n"
	.string "you will not.$"

SootopolisCity_Gym_B1F_Text_CrissyDefeat:
	.string "You are strong!\n"
	.string "Your sweet face had me\l"
	.string "completely fooled!$"

SootopolisCity_Gym_B1F_Text_CrissyPostBattle:
	.string "You might just be good\n"
	.string "enough not to be finished\l"
	.string "by CELINA in one go.$"

SootopolisCity_Gym_B1F_Text_DaphneIntro:
	.string "On the new bank, the dam\n"
	.string "saved homes from the flood.\p"
	.string "Our history is true, too.\n"
	.string "Will you hear it in battle?$"

SootopolisCity_Gym_B1F_Text_DaphneDefeat:
	.string "I had not heard the other bank.$"

SootopolisCity_Gym_B1F_Text_DaphnePostBattle:
	.string "Our homes stayed dry, but\n"
	.string "others paid the price.\p"
	.string "The memory I kept was\n"
	.string "true and incomplete.$"

SootopolisCity_Gym_B1F_Text_ConnieIntro:
	.string "Somebody ought to show you\n"
	.string "how hard a battle can be.$"

SootopolisCity_Gym_B1F_Text_ConnieDefeat:
	.string "Oh.\n"
	.string "You are strong.$"

SootopolisCity_Gym_B1F_Text_ConniePostBattle:
	.string "I shall tell you\n"
	.string "something worth knowing.\p"
	.string "Take the stair near the entrance\n"
	.string "to hear three testimonies.\p"
	.string "Each one opens a crossing\n"
	.string "toward CELINA.$"

SootopolisCity_Gym_B1F_Text_BridgetIntro:
	.string "The POKéMON GYM of the highest\n"
	.string "standing anywhere in ARAUNA...\p"
	.string "That is the AGUAS DE M'BOI GYM.$"

SootopolisCity_Gym_B1F_Text_BridgetDefeat:
	.string "What a standard you are at!$"

SootopolisCity_Gym_B1F_Text_BridgetPostBattle:
	.string "Rather than sit content in a\n"
	.string "strong GYM, I imagine training\l"
	.string "elsewhere would make you stronger.\p"
	.string "And more to the point, it\n"
	.string "looks a great deal more fun.$"

SootopolisCity_Gym_B1F_Text_OliviaIntro:
	.string "I train my POKéMON\n"
	.string "alongside CELINA.\p"
	.string "Do not take me for an\n"
	.string "easy afternoon.$"

SootopolisCity_Gym_B1F_Text_OliviaDefeat:
	.string "Beaten...$"

SootopolisCity_Gym_B1F_Text_OliviaPostBattle:
	.string "I think there is something in you.\n"
	.string "Why not stay and train with us?$"

SootopolisCity_Gym_B1F_Text_TiffanyIntro:
	.string "A careful crossing over the\n"
	.string "planks, and not a line crossed...\p"
	.string "A TRAINER doing that would be\n"
	.string "a beautiful thing to watch.$"

SootopolisCity_Gym_B1F_Text_TiffanyDefeat:
	.string "Well, excuse me!$"

SootopolisCity_Gym_B1F_Text_TiffanyPostBattle:
	.string "It is obvious enough, but\n"
	.string "how strong a TRAINER is\l"
	.string "has nothing whatever to\l"
	.string "do with how old they are.$"

SootopolisCity_Gym_B1F_Text_BethanyIntro:
	.string "When I am with my POKéMON the time\n"
	.string "goes before you can say “Oops!”$"

SootopolisCity_Gym_B1F_Text_BethanyDefeat:
	.string "Oops!$"

SootopolisCity_Gym_B1F_Text_BethanyPostBattle:
	.string "I do wish I could let go\n"
	.string "of a lost cause before I\l"
	.string "get as far as “Oops!”$"

SootopolisCity_Gym_B1F_Text_AnnikaIntro:
	.string "I can battle you with\n"
	.string "some genuinely rare\l"
	.string "POKéMON, if you like.$"

SootopolisCity_Gym_B1F_Text_AnnikaDefeat:
	.string "Oh, there now. Did you get\n"
	.string "a proper look at mine?$"

SootopolisCity_Gym_B1F_Text_AnnikaPostBattle:
	.string "I came to this house\n"
	.string "because CELINA said kind\l"
	.string "things about my darlings.\p"
	.string "Oh, if only I had met her years\n"
	.string "ago, when I was younger...$"

SootopolisCity_Gym_B1F_Text_BriannaIntro:
	.string "I keep the flooded\n"
	.string "archive. These wet pages\l"
	.string "name who opened the gate.\p"
	.string "Read them with me in battle!$"

SootopolisCity_Gym_B1F_Text_BriannaDefeat:
	.string "The ink still leaves marks.$"

SootopolisCity_Gym_B1F_Text_BriannaPostBattle:
	.string "The archive names those who\n"
	.string "voted. Many were never asked\l"
	.string "to decide the river's fate.$"
