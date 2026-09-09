Arauna_CasaUivo_Memorias_MapScripts::
	.byte 0

CasaUivo_EventScript_Memory::
	msgbox CasaUivo_Text_Memory, MSGBOX_SIGN
	end

CasaUivo_Text_Memory:
	.string "Notebooks and drawings kept\n"
	.string "by the Hermit and his mother.\p"
	.string "Her name remains beside\n"
	.string "the stories she shared.$"

CasaUivo_EventScript_Cloth::
	msgbox CasaUivo_Text_Cloth, MSGBOX_SIGN
	end

CasaUivo_Text_Cloth:
	.string "A carefully folded cloth\n"
	.string "rests beside the notebooks.$"

CasaUivo_EventScript_Window::
	msgbox CasaUivo_Text_Window, MSGBOX_SIGN
	end

CasaUivo_Text_Window:
	.string "Blue light falls across\n"
	.string "the quiet wooden floor.$"
