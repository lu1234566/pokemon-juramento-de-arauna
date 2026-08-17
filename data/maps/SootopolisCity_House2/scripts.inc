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
	.string "As duas forcas antigas de\nArauna reagiram ao colapso.\p"
	.string "IARA-MAE puxa os nomes de\nvolta. ANHANGUERA tenta\p"
	.string "encerrar o que nao pode\ncontinuar. Nenhuma delas foi\p"
	.string "feita para obedecer a seres\nhumanos.$"

SootopolisCity_House2_Text_YesTwoOrbsSideBySide:
	.string "As duas forcas antigas de\nArauna reagiram ao colapso.\p"
	.string "IARA-MAE puxa os nomes de\nvolta. ANHANGUERA tenta\p"
	.string "encerrar o que nao pode\ncontinuar. Nenhuma delas foi\p"
	.string "feita para obedecer a seres\nhumanos.$"

SootopolisCity_House2_Text_OughtToVisitAndSee:
	.string "Voce vai continuar mesmo\nsabendo que AGUAS DE M'BOI\p"
	.string "guarda partes da historia que\nmuita gente preferia deixar\p"
	.string "enterradas?$"

