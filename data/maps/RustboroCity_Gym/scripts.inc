RustboroCity_Gym_MapScripts::
	.byte 0

RustboroCity_Gym_EventScript_Roxanne::
	trainerbattle_single TRAINER_ROXANNE_1, RustboroCity_Gym_Text_RoxanneIntro, RustboroCity_Gym_Text_RoxanneDefeat, RustboroCity_Gym_EventScript_RoxanneDefeated, NO_MUSIC
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, RustboroCity_Gym_EventScript_RoxanneRematch
	goto_if_unset FLAG_RECEIVED_TM_ROCK_TOMB, RustboroCity_Gym_EventScript_GiveRockTomb
	msgbox RustboroCity_Gym_Text_RoxannePostBattle, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_RoxanneDefeated::
	message RustboroCity_Gym_Text_ReceivedStoneBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox RustboroCity_Gym_Text_StoneBadgeInfoTakeThis, MSGBOX_DEFAULT
	setflag FLAG_DEFEATED_RUSTBORO_GYM
	setflag FLAG_BADGE01_GET
	setvar VAR_RUSTBORO_CITY_STATE, 1
	addvar VAR_PETALBURG_GYM_STATE, 1
	setvar VAR_0x8008, 1
	call Common_EventScript_SetGymTrainers
	call_if_eq VAR_PETALBURG_GYM_STATE, 6, Common_EventScript_ReadyPetalburgGymForBattle
	goto RustboroCity_Gym_EventScript_GiveRockTomb
	end

RustboroCity_Gym_EventScript_GiveRockTomb::
	giveitem ITEM_TM_ROCK_TOMB
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_TM_ROCK_TOMB
	msgbox RustboroCity_Gym_Text_ExplainRockTomb, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_RoxanneRematch::
	trainerbattle_rematch_double TRAINER_ROXANNE_1, RustboroCity_Gym_Text_RoxannePreRematch, RustboroCity_Gym_Text_RoxanneRematchDefeat, RustboroCity_Gym_Text_RoxanneRematchNeedTwoMons
	msgbox RustboroCity_Gym_Text_RoxannePostRematch, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_Josh::
	trainerbattle_single TRAINER_JOSH, RustboroCity_Gym_Text_JoshIntro, RustboroCity_Gym_Text_JoshDefeat
	msgbox RustboroCity_Gym_Text_JoshPostBattle, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_Tommy::
	trainerbattle_single TRAINER_TOMMY, RustboroCity_Gym_Text_TommyIntro, RustboroCity_Gym_Text_TommyDefeat
	msgbox RustboroCity_Gym_Text_TommyPostBattle, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_Marc::
	trainerbattle_single TRAINER_MARC, RustboroCity_Gym_Text_MarcIntro, RustboroCity_Gym_Text_MarcDefeat
	msgbox RustboroCity_Gym_Text_MarcPostBattle, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_RUSTBORO_GYM, RustboroCity_Gym_EventScript_GymGuidePostVictory
	msgbox RustboroCity_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_GymGuidePostVictory::
	msgbox RustboroCity_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_BADGE01_GET, RustboroCity_Gym_EventScript_GymStatueCertified
	goto RustboroCity_Gym_EventScript_GymStatue
	end

RustboroCity_Gym_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_BADGE01_GET, RustboroCity_Gym_EventScript_GymStatueCertified
	goto RustboroCity_Gym_EventScript_GymStatue
	end

RustboroCity_Gym_EventScript_GymStatueCertified::
	msgbox RustboroCity_Gym_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

RustboroCity_Gym_EventScript_GymStatue::
	msgbox RustboroCity_Gym_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

RustboroCity_Gym_EventScript_RegisterRoxanne::
	lockall
	pokenavcall RustboroCity_Gym_Text_RoxanneRegisterCall
	waitmessage
	delay 30
	playfanfare MUS_REGISTER_MATCH_CALL
	msgbox RustboroCity_Gym_Text_RegisteredRoxanne, MSGBOX_DEFAULT
	waitfanfare
	closemessage
	delay 30
	setflag FLAG_ENABLE_ROXANNE_MATCH_CALL
	clearflag FLAG_ENABLE_ROXANNE_FIRST_CALL
	releaseall
	end

RustboroCity_Gym_Text_GymGuideAdvice:
	.string "Easy, now. Catch your breath.\p"
	.string "This is the CASA DA TERRA — the\n"
	.string "House of the Land.\p"
	.string "BENTO keeps the old ways of these\n"
	.string "hills. He was walking these ridges\l"
	.string "before your grandfolk were born.\p"
	.string "His creatures aren't big or flashy.\n"
	.string "They just don't fall down.\p"
	.string "Endurance, child. The mountain wins\n"
	.string "by outlasting the storm.\p"
	.string "Wear him out and you'll never manage\n"
	.string "it. Hit true, and hit early.\p"
	.string "Go on. The Land is listening.$"

RustboroCity_Gym_Text_GymGuidePostVictory:
	.string "You outlasted BENTO himself!\n"
	.string "I felt these old hills hum.\p"
	.string "The mark of the CASA DA TERRA is\n"
	.string "yours now — the first of Arauna's\l"
	.string "seven Seals.\p"
	.string "One House down. Long road ahead.\n"
	.string "Walk it well, child.$"

RustboroCity_Gym_Text_JoshIntro:
	.string "I quarried these steps by hand.\n"
	.string "Nobody reaches BENTO without\l"
	.string "passing me first.$"

RustboroCity_Gym_Text_JoshDefeat:
	.string "Strong footing… you've got it.$"

RustboroCity_Gym_Text_JoshPostBattle:
	.string "BENTO says a hill is just patience\n"
	.string "wearing a stone coat. You'll see\l"
	.string "what he means soon enough.$"

RustboroCity_Gym_Text_TommyIntro:
	.string "My folk have read this land for six\n"
	.string "generations. Let's see if it likes\l"
	.string "you.$"

RustboroCity_Gym_Text_TommyDefeat:
	.string "The Land let you pass. Huh.$"

RustboroCity_Gym_Text_TommyPostBattle:
	.string "BENTO won't rush you and won't tire.\p"
	.string "Beat him fast, or don't beat him\n"
	.string "at all.$"

RustboroCity_Gym_Text_MarcIntro:
	.string "You came up the whole ridge for a\n"
	.string "Seal? Then you already understand\l"
	.string "the Land a little.$"

RustboroCity_Gym_Text_MarcDefeat:
	.string "Sure-footed AND stubborn. Good.$"

RustboroCity_Gym_Text_MarcPostBattle:
	.string "BENTO chose the small, tough ones on\n"
	.string "purpose. Anyone can swing a boulder.\p"
	.string "Not everyone can refuse to fall.$"

RustboroCity_Gym_Text_RoxanneIntro:
	.string "Clay takes any mark while it is\n"
	.string "still soft.\p"
	.string "Once it hardens, pulling a mark\n"
	.string "out breaks the brick.\p"
	.string "Did your Census come to copy\n"
	.string "ours, or to ask who may read it?\p"
	.string "You said: to leave a copy where\n"
	.string "the story was born.\p"
	.string "Then hold that promise when the\n"
	.string "ground starts to give way.$"

RustboroCity_Gym_Text_RoxanneDefeat:
	.string "You did not defeat the land.\n"
	.string "Land does not enter a dispute.\p"
	.string "You defeated the wish to call\n"
	.string "this place empty.\p"
	.string "Take the Charter. The original\n"
	.string "stays with us here.$"

RustboroCity_Gym_Text_ReceivedStoneBadge:
	.string "{PLAYER} received the STONE BADGE\n"
	.string "from BENTO.$"

RustboroCity_Gym_Text_StoneBadgeInfoTakeThis:
	.string "The STONE BADGE heightens the ATTACK\n"
	.string "power of your POKéMON.\p"
	.string "It also enables them to use the HM move\n"
	.string "CUT outside of battle.\p"
	.string "Please take this with you, too.$"

RustboroCity_Gym_Text_ExplainRockTomb:
	.string "That TECHNICAL MACHINE, TM39,\n"
	.string "contains ROCK TOMB.\p"
	.string "It not only inflicts damage by dropping\n"
	.string "rocks, it also lowers SPEED.\p"
	.string "If you use a TM, it instantly teaches\n"
	.string "the move to a POKéMON.\p"
	.string "Remember, a TM can be used only once,\n"
	.string "so think before you use it.$"

RustboroCity_Gym_Text_RoxannePostBattle:
	.string "Six more Houses wait beyond these\n"
	.string "hills, each with its own keeper and\l"
	.string "its own hard lesson.\p"
	.string "Walk to them slow. The Land isn't\n"
	.string "going anywhere.$"

RustboroCity_Gym_Text_GymStatue:
	.string "CASA DA TERRA — the House of\n"
	.string "the Land. Keeper: BENTO.$"

RustboroCity_Gym_Text_GymStatueCertified:
	.string "CASA DA TERRA\p"
	.string "Those who outlasted the hills:\n"
	.string "{PLAYER}$"

RustboroCity_Gym_Text_RoxanneRegisterCall:
	.string "… … … … … …\n"
	.string "… … … … … Beep!\p"
	.string "BENTO: Oh, hello, {PLAYER}?\n"
	.string "This is BENTO of the Land House.\p"
	.string "I heard from NABOR that you're\n"
	.string "moving up through the ranks of\l"
	.string "TRAINERS at an incredible clip.\p"
	.string "Well, I'd rather not think that\n"
	.string "I can't beat you.\p"
	.string "I promise, I will shape up my GYM\n"
	.string "so that you may challenge us again.\p"
	.string "I hope you'll be looking forward to\n"
	.string "that occasion as much as me!\p"
	.string "… … … … … …\n"
	.string "… … … … … Click!$"

RustboroCity_Gym_Text_RegisteredRoxanne:
	.string "Registered GYM LEADER BENTO\n"
	.string "in the POKéNAV.$"

RustboroCity_Gym_Text_RoxannePreRematch:
	.string "BENTO: I'm so glad to see you again.\n"
	.string "I'm BENTO, the GYM LEADER here.\p"
	.string "I'm sure we've both experienced many\n"
	.string "battles since we last met.\p"
	.string "I would like to see how much better\n"
	.string "we've become. Let us battle!$"

RustboroCity_Gym_Text_RoxanneRematchDefeat:
	.string "Grr…\n"
	.string "Again, I have lost…$"

RustboroCity_Gym_Text_RoxannePostRematch:
	.string "BENTO: I still have much to learn\n"
	.string "when it comes to battling POKéMON.\p"
	.string "That awareness makes me love battling\n"
	.string "all that much more!$"

RustboroCity_Gym_Text_RoxanneRematchNeedTwoMons:
	.string "BENTO: I'm so glad to see you again.\n"
	.string "I'm BENTO, the GYM LEADER here.\p"
	.string "I'm sure we've both experienced many\n"
	.string "battles since we last met.\p"
	.string "I would like to see how much better\n"
	.string "we've become…\p"
	.string "Oh, no…\n"
	.string "You only have one POKéMON with you?\p"
	.string "Please return with at least one more\n"
	.string "POKéMON.$"
