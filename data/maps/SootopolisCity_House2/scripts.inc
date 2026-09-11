SootopolisCity_House2_MapScripts::
	.byte 0

SootopolisCity_House2_EventScript_ExpertF::
	lock
	faceplayer
	msgbox SootopolisCity_House2_Text_DidYouKnowAboutMtPyreOrbs, MSGBOX_YESNO
	call_if_eq VAR_RESULT, YES, SootopolisCity_House2_EventScript_KnowAboutOrbs
	call_if_eq VAR_RESULT, NO, SootopolisCity_House2_EventScript_DontKnowAboutOrbs
	release
	end

SootopolisCity_House2_EventScript_KnowAboutOrbs::
	msgbox SootopolisCity_House2_Text_YesTwoOrbsSideBySide, MSGBOX_DEFAULT
	return

SootopolisCity_House2_EventScript_DontKnowAboutOrbs::
	msgbox SootopolisCity_House2_Text_OughtToVisitAndSee, MSGBOX_DEFAULT
	return

SootopolisCity_House2_Text_DidYouKnowAboutMtPyreOrbs:
	.string "MEMORIAL DOS NOMES…\p"
	.string "At its peak are two orbs placed side by\n"
	.string "side. Did you know?$"

SootopolisCity_House2_Text_YesTwoOrbsSideBySide:
	.string "The whole city is living with what\n"
	.string "happens when two ideas are taken as\l"
	.string "absolutes: remember everything, and\l"
	.string "erase the pain at any cost.$"

SootopolisCity_House2_Text_OughtToVisitAndSee:
	.string "Is that so?\n"
	.string "Perhaps you ought to visit and see…$"

