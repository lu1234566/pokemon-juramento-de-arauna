BattleFrontier_ReceptionGate_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, BattleFrontier_ReceptionGate_OnFrame
	map_script MAP_SCRIPT_ON_TRANSITION, BattleFrontier_ReceptionGate_OnTransition
	.byte 0

BattleFrontier_ReceptionGate_OnTransition:
	setflag FLAG_LANDMARK_BATTLE_FRONTIER
	end

BattleFrontier_ReceptionGate_OnFrame:
	map_script_2 VAR_HAS_ENTERED_BATTLE_FRONTIER, 0, BattleFrontier_ReceptionGate_EventScript_FirstTimeEntering
	.2byte 0

BattleFrontier_ReceptionGate_EventScript_FirstTimeEntering::
	lockall
	setvar VAR_HAS_ENTERED_BATTLE_FRONTIER, 1
	playse SE_PIN
	applymovement LOCALID_FRONTIER_RECEPTION_GREETER, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_FRONTIER_RECEPTION_GREETER, Common_Movement_Delay48
	waitmovement 0
	msgbox BattleFrontier_ReceptionGate_Text_FirstTimeHereThisWay, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, BattleFrontier_ReceptionGate_Movement_PlayerApproachCounter
	waitmovement 0
	goto BattleFrontier_ReceptionGate_EventScript_ScottScene
	end

BattleFrontier_ReceptionGate_EventScript_ScottScene::
	msgbox BattleFrontier_ReceptionGate_Text_WelcomeToBattleFrontier, MSGBOX_DEFAULT
	msgbox BattleFrontier_ReceptionGate_Text_IssueFrontierPass, MSGBOX_DEFAULT
	playfanfare MUS_OBTAIN_ITEM
	message BattleFrontier_ReceptionGate_Text_ObtainedFrontierPass
	waitfanfare
	waitmessage
	msgbox BattleFrontier_ReceptionGate_Text_PlacedTrainerCardInFrontierPass, MSGBOX_DEFAULT
	setflag FLAG_SYS_FRONTIER_PASS
	msgbox BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier, MSGBOX_DEFAULT
	msgbox BattleFrontier_ReceptionGate_Text_IfItIsntPlayerYouCame, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FRONTIER_RECEPTION_GREETER, Common_Movement_WalkInPlaceFasterUp
	applymovement LOCALID_FRONTIER_RECEPTION_GUIDE, Common_Movement_WalkInPlaceFasterUp
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_FRONTIER_RECEPTION_GREETER, Common_Movement_ExclamationMark
	applymovement LOCALID_FRONTIER_RECEPTION_GUIDE, Common_Movement_ExclamationMark
	applymovement LOCALID_PLAYER, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox BattleFrontier_ReceptionGate_Text_OhMrScottGoodDay, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FRONTIER_RECEPTION_GREETER, BattleFrontier_ReceptionGate_Movement_GreeterFaceScott
	applymovement LOCALID_FRONTIER_RECEPTION_GUIDE, BattleFrontier_ReceptionGate_Movement_FacilityGuideFaceScott
	applymovement LOCALID_PLAYER, BattleFrontier_ReceptionGate_Movement_PlayerFaceScott
	applymovement LOCALID_FRONTIER_RECEPTION_SCOTT, BattleFrontier_ReceptionGate_Movement_ScottEnter
	waitmovement 0
	msgbox BattleFrontier_ReceptionGate_Text_ScottGreatToSeeYouHere, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FRONTIER_RECEPTION_SCOTT, BattleFrontier_ReceptionGate_Movement_ScottExit
	waitmovement 0
	removeobject LOCALID_FRONTIER_RECEPTION_SCOTT
	releaseall
	end

BattleFrontier_ReceptionGate_Movement_PlayerApproachCounter:
	walk_up
	walk_up
	walk_left
	walk_left
	step_end

BattleFrontier_ReceptionGate_Movement_PlayerFaceScott:
	delay_16
	delay_16
	delay_16
	delay_8
	walk_in_place_faster_right
	step_end

@ Unused
BattleFrontier_ReceptionGate_Movement_WalkDown:
	walk_down
	walk_down
	step_end

BattleFrontier_ReceptionGate_Movement_ScottEnter:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	step_end

BattleFrontier_ReceptionGate_Movement_ScottExit:
	walk_right
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

BattleFrontier_ReceptionGate_Movement_GreeterFaceScott:
	delay_16
	delay_16
	delay_16
	delay_8
	walk_in_place_faster_right
	step_end

BattleFrontier_ReceptionGate_Movement_FacilityGuideFaceScott:
	delay_16
	delay_16
	delay_16
	delay_8
	walk_in_place_faster_left
	step_end

BattleFrontier_ReceptionGate_EventScript_Greeter::
	lock
	faceplayer
	msgbox BattleFrontier_ReceptionGate_Text_WelcomeToBattleFrontier, MSGBOX_DEFAULT
	msgbox BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier, MSGBOX_DEFAULT
	release
	end

BattleFrontier_ReceptionGate_EventScript_FacilityGuide::
	lock
	faceplayer
	msgbox BattleFrontier_ReceptionGate_Text_YourGuideToFacilities, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout::
	message BattleFrontier_ReceptionGate_Text_LearnAboutWhich2
	waitmessage
	setvar VAR_0x8004, SCROLL_MULTI_BF_RECEPTIONIST
	special ShowScrollableMultichoice
	switch VAR_RESULT
	case 0, BattleFrontier_ReceptionGate_EventScript_BattleTower
	case 1, BattleFrontier_ReceptionGate_EventScript_BattleDome
	case 2, BattleFrontier_ReceptionGate_EventScript_BattlePalace
	case 3, BattleFrontier_ReceptionGate_EventScript_BattleArena
	case 4, BattleFrontier_ReceptionGate_EventScript_BattleFactory
	case 5, BattleFrontier_ReceptionGate_EventScript_BattlePike
	case 6, BattleFrontier_ReceptionGate_EventScript_BattlePyramid
	case 7, BattleFrontier_ReceptionGate_EventScript_RankingHall
	case 8, BattleFrontier_ReceptionGate_EventScript_ExchangeCorner
	case 9, BattleFrontier_ReceptionGate_EventScript_ExitFacilityGuide
	case MULTI_B_PRESSED, BattleFrontier_ReceptionGate_EventScript_ExitFacilityGuide
	end

BattleFrontier_ReceptionGate_EventScript_BattleTower::
	msgbox BattleFrontier_ReceptionGate_Text_BattleTowerInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_BattleDome::
	msgbox BattleFrontier_ReceptionGate_Text_BattleDomeInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_BattlePalace::
	msgbox BattleFrontier_ReceptionGate_Text_BattlePalaceInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_BattleArena::
	msgbox BattleFrontier_ReceptionGate_Text_BattleArenaInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_BattleFactory::
	msgbox BattleFrontier_ReceptionGate_Text_BattleFactoryInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_BattlePike::
	msgbox BattleFrontier_ReceptionGate_Text_BattlePikeInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_BattlePyramid::
	msgbox BattleFrontier_ReceptionGate_Text_BattlePyramidInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_RankingHall::
	msgbox BattleFrontier_ReceptionGate_Text_RankingHallInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_ExchangeCorner::
	msgbox BattleFrontier_ReceptionGate_Text_ExchangeCornerInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_ExitFacilityGuide::
	msgbox BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier, MSGBOX_DEFAULT
	release
	end

BattleFrontier_ReceptionGate_EventScript_RulesGuide::
	lock
	faceplayer
	msgbox BattleFrontier_ReceptionGate_Text_YourGuideToRules, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout::
	message BattleFrontier_ReceptionGate_Text_LearnAboutWhat
	waitmessage
	multichoice 15, 0, MULTI_FRONTIER_RULES, FALSE
	switch VAR_RESULT
	case 0, BattleFrontier_ReceptionGate_EventScript_LevelMode
	case 1, BattleFrontier_ReceptionGate_EventScript_Level50
	case 2, BattleFrontier_ReceptionGate_EventScript_OpenLevel
	case 3, BattleFrontier_ReceptionGate_EventScript_MonEntry
	case 4, BattleFrontier_ReceptionGate_EventScript_HoldItems
	case 5, BattleFrontier_ReceptionGate_EventScript_ExitRulesGuide
	case MULTI_B_PRESSED, BattleFrontier_ReceptionGate_EventScript_ExitRulesGuide
	end

BattleFrontier_ReceptionGate_EventScript_LevelMode::
	msgbox BattleFrontier_ReceptionGate_Text_LevelModeInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_Level50::
	msgbox BattleFrontier_ReceptionGate_Text_Level50Info, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_OpenLevel::
	msgbox BattleFrontier_ReceptionGate_Text_OpenLevelInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_MonEntry::
	msgbox BattleFrontier_ReceptionGate_Text_MonEntryInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_HoldItems::
	msgbox BattleFrontier_ReceptionGate_Text_HoldItemsInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_ExitRulesGuide::
	msgbox BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier, MSGBOX_DEFAULT
	release
	end

BattleFrontier_ReceptionGate_EventScript_FrontierPassGuide::
	lock
	faceplayer
	msgbox BattleFrontier_ReceptionGate_Text_YourGuideToFrontierPass, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFrontierPassInfoToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_ChooseFrontierPassInfoToLearnAbout::
	message BattleFrontier_ReceptionGate_Text_LearnAboutWhich1
	waitmessage
	multichoice 16, 4, MULTI_FRONTIER_PASS_INFO, FALSE
	switch VAR_RESULT
	case 0, BattleFrontier_ReceptionGate_EventScript_Symbols
	case 1, BattleFrontier_ReceptionGate_EventScript_RecordBattle
	case 2, BattleFrontier_ReceptionGate_EventScript_BattlePoints
	case 3, BattleFrontier_ReceptionGate_EventScript_ExitFrontierPassGuide
	case MULTI_B_PRESSED, BattleFrontier_ReceptionGate_EventScript_ExitFrontierPassGuide
	end

BattleFrontier_ReceptionGate_EventScript_Symbols::
	msgbox BattleFrontier_ReceptionGate_Text_SymbolsInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFrontierPassInfoToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_RecordBattle::
	msgbox BattleFrontier_ReceptionGate_Text_RecordedBattleInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFrontierPassInfoToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_BattlePoints::
	msgbox BattleFrontier_ReceptionGate_Text_BattlePointsInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFrontierPassInfoToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_ExitFrontierPassGuide::
	msgbox BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier, MSGBOX_DEFAULT
	release
	end

BattleFrontier_ReceptionGate_Text_FirstTimeHereThisWay:
	.string "Is this your first visit? Right this way,\n"
	.string "please!$"

BattleFrontier_ReceptionGate_Text_WelcomeToBattleFrontier:
	.string "This is the BATTLE CIRCUIT! Welcome to\n"
	.string "the final challenge.$"

BattleFrontier_ReceptionGate_Text_IssueFrontierPass:
	.string "On a first visit we hand out the\n"
	.string "CIRCUIT PASS.\p"
	.string "It's good at every facility in this\n"
	.string "complex.\p"
	.string "Here you are!$"

BattleFrontier_ReceptionGate_Text_ObtainedFrontierPass:
	.string "{PLAYER} received the CIRCUIT PASS.$"

BattleFrontier_ReceptionGate_Text_PlacedTrainerCardInFrontierPass:
	.string "The TRAINER's data was recorded on the\n"
	.string "PASS.$"

BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier:
	.string "Make the most of everything the BATTLE\n"
	.string "CIRCUIT has to offer!$"

BattleFrontier_ReceptionGate_Text_IfItIsntPlayerYouCame:
	.string "???: {PLAYER}{KUN}! So you came.$"

BattleFrontier_ReceptionGate_Text_OhMrScottGoodDay:
	.string "GUIDE: Ah! MR. BENTO! Good morning, sir!$"

BattleFrontier_ReceptionGate_Text_ScottGreatToSeeYouHere:
	.string "MR. BENTO: Good to see you here. Take\n"
	.string "your time and look around.\p"
	.string "I want you to find out how far your way\n"
	.string "of battling holds up.\p"
	.string "I keep a room nearby. Drop in whenever\n"
	.string "you like.$"

BattleFrontier_ReceptionGate_Text_YourGuideToFacilities:
	.string "I'm the guide to the BATTLE CIRCUIT\n"
	.string "facilities.$"

BattleFrontier_ReceptionGate_Text_LearnAboutWhich2:
	.string "Which one would you like to know about?$"

BattleFrontier_ReceptionGate_Text_BattleTowerInfo:
	.string "The BATTLE TOWER is the great tower,\n"
	.string "the symbol of the CIRCUIT.\p"
	.string "There are SINGLE, DOUBLE, MULTI and\n"
	.string "LINK MULTI challenges.$"

BattleFrontier_ReceptionGate_Text_BattleDomeInfo:
	.string "The BATTLE DOME is the building shaped\n"
	.string "like a great egg.\p"
	.string "It runs tournaments in two formats:\n"
	.string "SINGLE and DOUBLE.$"

BattleFrontier_ReceptionGate_Text_BattlePalaceInfo:
	.string "The BATTLE PALACE is the red building\n"
	.string "on the right.\p"
	.string "There are SINGLE and DOUBLE\n"
	.string "challenges.$"

BattleFrontier_ReceptionGate_Text_BattleArenaInfo:
	.string "The BATTLE ARENA is in the middle right\n"
	.string "of the CIRCUIT.\p"
	.string "It runs a short knockout tournament.$"

BattleFrontier_ReceptionGate_Text_BattleFactoryInfo:
	.string "The BATTLE FACTORY is the large\n"
	.string "building nearest the entrance.\p"
	.string "You battle there with rented POKéMON\n"
	.string "and may trade them.\p"
	.string "There are SINGLE and DOUBLE formats.$"

BattleFrontier_ReceptionGate_Text_BattlePikeInfo:
	.string "The BATTLE PIKE is the POKéMON-shaped\n"
	.string "building on the left.\p"
	.string "Every room makes you choose before you\n"
	.string "go on.$"

BattleFrontier_ReceptionGate_Text_BattlePyramidInfo:
	.string "The BATTLE PYRAMID is the huge pyramid\n"
	.string "in the complex.\p"
	.string "The challenge is to explore and win your\n"
	.string "way to the top.$"

BattleFrontier_ReceptionGate_Text_RankingHallInfo:
	.string "The RANKING HALL is near the BATTLE\n"
	.string "TOWER.\p"
	.string "It holds the best records of everyone\n"
	.string "who has taken on the CIRCUIT.$"

BattleFrontier_ReceptionGate_Text_ExchangeCornerInfo:
	.string "The EXCHANGE CORNER is near the BATTLE\n"
	.string "TOWER.\p"
	.string "Trade your Battle Points for rewards\n"
	.string "there.$"

BattleFrontier_ReceptionGate_Text_YourGuideToRules:
	.string "I'm the guide to the rules the CIRCUIT\n"
	.string "challenges have in common.$"

BattleFrontier_ReceptionGate_Text_LearnAboutWhat:
	.string "Which rule would you like to know about?$"

BattleFrontier_ReceptionGate_Text_LevelModeInfo:
	.string "The challenges use two modes: Level 50\n"
	.string "and Open Level.$"

BattleFrontier_ReceptionGate_Text_Level50Info:
	.string "Level 50 takes POKéMON at level 50 or\n"
	.string "below.\p"
	.string "Your opponents will never bring POKéMON\n"
	.string "under level 50.\p"
	.string "It's the mode to start with.$"

BattleFrontier_ReceptionGate_Text_OpenLevelInfo:
	.string "Open Level has no level limit to enter.\p"
	.string "Opponents follow the level of your\n"
	.string "POKéMON,\p"
	.string "but never drop below level 60.$"

BattleFrontier_ReceptionGate_Text_MonEntryInfo:
	.string "Almost any POKéMON can enter the\n"
	.string "challenges.\p"
	.string "EGGS and a few species aren't allowed.\p"
	.string "How many you need varies between\n"
	.string "facilities.\p"
	.string "Don't use two POKéMON of the same\n"
	.string "species in one challenge.$"

BattleFrontier_ReceptionGate_Text_HoldItemsInfo:
	.string "Entered POKéMON can't hold the same\n"
	.string "items.\p"
	.string "Every member has to come in with a\n"
	.string "different item.$"

BattleFrontier_ReceptionGate_Text_YourGuideToFrontierPass:
	.string "I'm the guide to the CIRCUIT PASS.$"

BattleFrontier_ReceptionGate_Text_LearnAboutWhich1:
	.string "Which part would you like to know\n"
	.string "about?$"

BattleFrontier_ReceptionGate_Text_SymbolsInfo:
	.string "The CIRCUIT has seven great facilities.\p"
	.string "Anyone who stands out can be given a\n"
	.string "SYMBOL at each one.\p"
	.string "To earn them, you'll have to win again\n"
	.string "and again.\p"
	.string "It isn't easy. Good luck!$"

BattleFrontier_ReceptionGate_Text_RecordedBattleInfo:
	.string "The PASS can keep the record of a\n"
	.string "battle.\p"
	.string "It can be a bout with friends or a\n"
	.string "CIRCUIT challenge,\p"
	.string "apart from matches at the BATTLE PIKE\n"
	.string "and the BATTLE PYRAMID.\p"
	.string "You decide at the end of a battle\n"
	.string "whether to save the record.$"

BattleFrontier_ReceptionGate_Text_BattlePointsInfo:
	.string "Battle Points reward anyone who stands\n"
	.string "out on the CIRCUIT.\p"
	.string "They can be traded for rewards at the\n"
	.string "EXCHANGE CORNER.$"
