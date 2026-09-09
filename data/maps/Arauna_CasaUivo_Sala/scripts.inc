Arauna_CasaUivo_Sala_MapScripts::
	.byte 0

CasaUivo_EventScript_Welcome::
	msgbox CasaUivo_Text_Welcome, MSGBOX_SIGN
	end

CasaUivo_Text_Welcome:
	.string "Take a seat where everyone\n"
	.string "can see one another.$"

CasaUivo_EventScript_Books::
	msgbox CasaUivo_Text_Books, MSGBOX_SIGN
	end

CasaUivo_Text_Books:
	.string "Stories are kept here in\n"
	.string "notebooks and drawings.\p"
	.string "Their authors are named\n"
	.string "beside each record.$"

CasaUivo_EventScript_Drawings::
	msgbox CasaUivo_Text_Drawings, MSGBOX_SIGN
	end

CasaUivo_Text_Drawings:
	.string "Drawings show where people sit\n"
	.string "and how they share the room.\p"
	.string "No one should be hidden\n"
	.string "behind another person.$"

CasaUivo_EventScript_Hermit::
	msgbox CasaUivo_Text_Hermit, MSGBOX_NPC
	end

CasaUivo_Text_Hermit:
	.string "He turns a notebook toward you.\p"
	.string "“Please sit where we can see\n"
	.string "each other. Take your time.”$"

CasaUivo_EventScript_Child::
	msgbox CasaUivo_Text_Child, MSGBOX_NPC
	end

CasaUivo_Text_Child:
	.string "“You can sit beside me.\n"
	.string "There is room for everyone.”$"
