Arauna_CasaUivo_Memorias_MapScripts::
	.byte 0

@ Casa do Uivo, U05 -- DRAFT (docs/ARCOS_RASCUNHO.md). The mother's three
@ notebooks go back in story order; the last page says what to do, and the
@ cloth beside them is how.

CasaUivo_EventScript_Memory::
	lockall
	goto_if_eq VAR_ARAUNA_UIVO_STATE, 2, CasaUivo_Memory_Sort
	goto_if_ge VAR_ARAUNA_UIVO_STATE, 3, CasaUivo_Memory_Sorted
	msgbox CasaUivo_Text_Memory, MSGBOX_DEFAULT
	releaseall
	end

CasaUivo_Memory_Sort:
	msgbox CasaUivo_Text_NotebooksLoose, MSGBOX_DEFAULT
	message CasaUivo_Text_WhichFirst
	waitmessage
	multichoice 12, 6, MULTI_ARAUNA_NOTEBOOKS, TRUE
	goto_if_ne VAR_RESULT, 0, CasaUivo_Memory_WrongOrder
	message CasaUivo_Text_WhichNext
	waitmessage
	multichoice 12, 6, MULTI_ARAUNA_NOTEBOOKS, TRUE
	goto_if_eq VAR_RESULT, 0, CasaUivo_Memory_AlreadyDown
	goto_if_ne VAR_RESULT, 1, CasaUivo_Memory_WrongOrder
	playse SE_RG_CARD_FLIP
	msgbox CasaUivo_Text_NotebooksInOrder, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_UIVO_STATE, 3
	releaseall
	end

CasaUivo_Memory_AlreadyDown:
	msgbox CasaUivo_Text_AlreadyDown, MSGBOX_DEFAULT
CasaUivo_Memory_WrongOrder:
	msgbox CasaUivo_Text_WrongOrder, MSGBOX_DEFAULT
	releaseall
	end

CasaUivo_Memory_Sorted:
	msgbox CasaUivo_Text_LastPage, MSGBOX_DEFAULT
	releaseall
	end

CasaUivo_Text_Memory:
	.string "Notebooks and drawings kept\n"
	.string "by the Hermit and his mother.\p"
	.string "Her name remains beside\n"
	.string "the stories she shared.$"

CasaUivo_Text_NotebooksLoose:
	.string "Three notebooks lie open, their\n"
	.string "pages loose.\p"
	.string "Each cover has a drawing on it.$"

CasaUivo_Text_WhichFirst:
	.string "Which notebook comes first?$"

CasaUivo_Text_WhichNext:
	.string "And which comes next?$"

CasaUivo_Text_AlreadyDown:
	.string "That one is already on the table.$"

CasaUivo_Text_WrongOrder:
	.string "You read them in that order,\n"
	.string "but the story doesn't follow.\p"
	.string "You gather the pages to start\n"
	.string "again.$"

CasaUivo_Text_NotebooksInOrder:
	.string "The cloth on stones goes last.\n"
	.string "You read the three in order.\p"
	.string "“At dusk the GUARÁ families come\n"
	.string "down to drink. A mother calls.\l"
	.string "One pup does not answer.”\p"
	.string "“In the fog the pup howls all night.\n"
	.string "The ridge thinks it is angry.\l"
	.string "It is asking where home is.”\p"
	.string "“I left my cloth on the stones.\n"
	.string "It smells of this house.\l"
	.string "The pup slept on it.\l"
	.string "At dawn its mother found it.”\p"
	.string "At the foot of the last page:\n"
	.string "“Don't chase a howl. Answer it.”$"

CasaUivo_Text_LastPage:
	.string "The last page of the last notebook:\n"
	.string "“Don't chase a howl. Answer it.”$"

CasaUivo_EventScript_Cloth::
	lockall
	goto_if_eq VAR_ARAUNA_UIVO_STATE, 3, CasaUivo_Cloth_Take
	goto_if_set FLAG_ARAUNA_UIVO_PUP_CAUGHT, CasaUivo_Cloth_Travels
	goto_if_eq VAR_ARAUNA_UIVO_STATE, 4, CasaUivo_Cloth_Carried
	goto_if_eq VAR_ARAUNA_UIVO_STATE, 5, CasaUivo_Cloth_Carried
	goto_if_ge VAR_ARAUNA_UIVO_STATE, 6, CasaUivo_Cloth_After
	msgbox CasaUivo_Text_Cloth, MSGBOX_DEFAULT
	releaseall
	end

CasaUivo_Cloth_Take:
	msgbox CasaUivo_Text_ClothTake, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CasaUivo_Cloth_Left
	playse SE_RG_BAG_POCKET
	msgbox CasaUivo_Text_ClothTaken, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_UIVO_STATE, 4
	releaseall
	end

CasaUivo_Cloth_Left:
	msgbox CasaUivo_Text_ClothLeft, MSGBOX_DEFAULT
	releaseall
	end

CasaUivo_Cloth_Carried:
	msgbox CasaUivo_Text_ClothCarried, MSGBOX_DEFAULT
	releaseall
	end

CasaUivo_Cloth_After:
	msgbox CasaUivo_Text_ClothBack, MSGBOX_DEFAULT
	releaseall
	end

CasaUivo_Cloth_Travels:
	msgbox CasaUivo_Text_ClothTravels, MSGBOX_DEFAULT
	releaseall
	end

CasaUivo_Text_Cloth:
	.string "A carefully folded cloth\n"
	.string "rests beside the notebooks.$"

CasaUivo_Text_ClothTake:
	.string "The cloth from the story.\n"
	.string "Take it to the ridge?$"

CasaUivo_Text_ClothTaken:
	.string "You take the cloth. It smells of\n"
	.string "wood smoke and old paper.$"

CasaUivo_Text_ClothLeft:
	.string "You leave it folded where it was.$"

CasaUivo_Text_ClothCarried:
	.string "The place where the cloth lay\n"
	.string "is empty. You have it with you.$"

CasaUivo_Text_ClothBack:
	.string "The cloth is folded here again.\n"
	.string "Short orange hairs cling to it.$"

CasaUivo_Text_ClothTravels:
	.string "The cloth is not here.\n"
	.string "It travels with the pup now.$"

CasaUivo_EventScript_Window::
	msgbox CasaUivo_Text_Window, MSGBOX_SIGN
	end

CasaUivo_Text_Window:
	.string "Blue light falls across\n"
	.string "the quiet wooden floor.$"
