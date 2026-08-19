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
	.string "E sua primeira visita?\nPor favor, venha por aqui!$"

BattleFrontier_ReceptionGate_Text_WelcomeToBattleFrontier:
	.string "Este e o CIRCUITO DE BATALHA!\nBem-vindo ao desafio final.$"

BattleFrontier_ReceptionGate_Text_IssueFrontierPass:
	.string "Na primeira visita entregamos\no PASSE DO CIRCUITO.\p"
	.string "Ele vale em todas as instalacoes\ndeste complexo.\p"
	.string "Aqui esta!$"

BattleFrontier_ReceptionGate_Text_ObtainedFrontierPass:
	.string "{PLAYER} recebeu o\nPASSE DO CIRCUITO.$"

BattleFrontier_ReceptionGate_Text_PlacedTrainerCardInFrontierPass:
	.string "Os dados do TREINADOR foram\nregistrados no PASSE.$"

BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier:
	.string "Aproveite tudo que o CIRCUITO\nDE BATALHA oferece!$"

BattleFrontier_ReceptionGate_Text_IfItIsntPlayerYouCame:
	.string "???: {PLAYER}{KUN}! Entao voce veio.$"

BattleFrontier_ReceptionGate_Text_OhMrScottGoodDay:
	.string "GUIA: Ah! SEU BENTO!\nBom dia, senhor!$"

BattleFrontier_ReceptionGate_Text_ScottGreatToSeeYouHere:
	.string "SEU BENTO: Bom ver voce aqui.\nExplore tudo com calma.\p"
	.string "Quero que descubra ate onde\nseu modo de batalhar aguenta.\p"
	.string "Tenho um quarto aqui perto.\nPasse la quando quiser.$"

BattleFrontier_ReceptionGate_Text_YourGuideToFacilities:
	.string "Sou o guia das instalacoes do\nCIRCUITO DE BATALHA.$"

BattleFrontier_ReceptionGate_Text_LearnAboutWhich2:
	.string "Sobre qual quer saber?$"

BattleFrontier_ReceptionGate_Text_BattleTowerInfo:
	.string "A BATTLE TOWER e a grande torre\ne simbolo do CIRCUITO.\p"
	.string "Ha desafios SINGLE, DOUBLE,\nMULTI e LINK MULTI.$"

BattleFrontier_ReceptionGate_Text_BattleDomeInfo:
	.string "O BATTLE DOME e o predio em\nforma de grande ovo.\p"
	.string "La ocorrem torneios em duas\nmodalidades: SINGLE e DOUBLE.$"

BattleFrontier_ReceptionGate_Text_BattlePalaceInfo:
	.string "O BATTLE PALACE e o predio\nvermelho do lado direito.\p"
	.string "Ha desafios SINGLE e DOUBLE.$"

BattleFrontier_ReceptionGate_Text_BattleArenaInfo:
	.string "A BATTLE ARENA fica na parte\ncentral direita do CIRCUITO.\p"
	.string "Ali ocorre um torneio curto\nbaseado em nocautes.$"

BattleFrontier_ReceptionGate_Text_BattleFactoryInfo:
	.string "A BATTLE FACTORY e o grande\npredio mais perto da entrada.\p"
	.string "Ali voce luta com POKéMON\nemprestados e pode troca-los.\p"
	.string "Ha modalidades SINGLE e DOUBLE.$"

BattleFrontier_ReceptionGate_Text_BattlePikeInfo:
	.string "A BATTLE PIKE e o predio com\nforma de POKéMON a esquerda.\p"
	.string "Cada sala obriga voce a fazer\numa escolha antes de seguir.$"

BattleFrontier_ReceptionGate_Text_BattlePyramidInfo:
	.string "A BATTLE PYRAMID e a enorme\npiramide do complexo.\p"
	.string "O desafio exige explorar e\nvencer batalhas ate o topo.$"

BattleFrontier_ReceptionGate_Text_RankingHallInfo:
	.string "O RANKING HALL fica perto da\nBATTLE TOWER.\p"
	.string "La ficam os melhores registros\nde quem enfrentou o CIRCUITO.$"

BattleFrontier_ReceptionGate_Text_ExchangeCornerInfo:
	.string "O EXCHANGE CORNER fica perto\nda BATTLE TOWER.\p"
	.string "Troque seus Pontos de Batalha\npor recompensas ali.$"

BattleFrontier_ReceptionGate_Text_YourGuideToRules:
	.string "Sou o guia das regras comuns\naos desafios do CIRCUITO.$"

BattleFrontier_ReceptionGate_Text_LearnAboutWhat:
	.string "Sobre qual regra quer saber?$"

BattleFrontier_ReceptionGate_Text_LevelModeInfo:
	.string "Os desafios usam dois modos:\nLevel 50 e Open Level.$"

BattleFrontier_ReceptionGate_Text_Level50Info:
	.string "No Level 50 entram POKéMON de\nnivel 50 ou menos.\p"
	.string "Seus adversarios nunca terao\nPOKéMON abaixo do nivel 50.\p"
	.string "E o modo indicado para comecar.$"

BattleFrontier_ReceptionGate_Text_OpenLevelInfo:
	.string "No Open Level nao ha limite de\nnivel para entrar.\p"
	.string "Os adversarios acompanham o\nnivel dos seus POKéMON,\p"
	.string "mas nunca ficam abaixo do\nnivel 60.$"

BattleFrontier_ReceptionGate_Text_MonEntryInfo:
	.string "Quase todo POKéMON pode entrar\nnos desafios.\p"
	.string "OVOS e algumas especies nao\nsao permitidos.\p"
	.string "A quantidade exigida varia\nentre as instalacoes.\p"
	.string "Nao use dois POKéMON da mesma\nespecie no mesmo desafio.$"

BattleFrontier_ReceptionGate_Text_HoldItemsInfo:
	.string "POKéMON inscritos nao podem\nsegurar itens iguais.\p"
	.string "Cada integrante deve entrar\ncom um item diferente.$"

BattleFrontier_ReceptionGate_Text_YourGuideToFrontierPass:
	.string "Sou o guia do PASSE DO CIRCUITO.$"

BattleFrontier_ReceptionGate_Text_LearnAboutWhich1:
	.string "Sobre qual parte quer saber?$"

BattleFrontier_ReceptionGate_Text_SymbolsInfo:
	.string "O CIRCUITO possui sete grandes\ninstalacoes.\p"
	.string "Quem se destaca pode receber\num SIMBOLO em cada uma.\p"
	.string "Para conquista-los, sera preciso\nvencer repetidas vezes.\p"
	.string "Nao e facil. Boa sorte!$"

BattleFrontier_ReceptionGate_Text_RecordedBattleInfo:
	.string "O PASSE pode guardar o registro\nde uma batalha.\p"
	.string "Pode ser uma luta com amigos\nou um desafio do CIRCUITO,\p"
	.string "exceto partidas da BATTLE PIKE\ne da BATTLE PYRAMID.\p"
	.string "Voce decide ao fim da batalha\nse quer salvar o registro.$"

BattleFrontier_ReceptionGate_Text_BattlePointsInfo:
	.string "Pontos de Batalha premiam quem\nse destaca no CIRCUITO.\p"
	.string "Eles podem ser trocados por\nrecompensas no EXCHANGE CORNER.$"
