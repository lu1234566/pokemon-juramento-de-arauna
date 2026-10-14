Route119_House_MapScripts::
	.byte 0

Route119_House_EventScript_Woman::
	msgbox Route119_House_Text_RumorAboutCaveOfOrigin, MSGBOX_NPC
	end

Route119_House_EventScript_Wingull::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_WINGULL, CRY_MODE_NORMAL
	msgbox Route119_House_Text_Wingull, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Route119_House_Text_RumorAboutCaveOfOrigin:
	.string "Travelers say the deep chambers\n"
	.string "under M'BOI carry old voices.\p"
	.string "I cannot tell if it is history,\n"
	.string "weather, or only a story.\p"
	.string "Still, people here listen.$"

Route119_House_Text_Wingull:
	.string "Foliao: Pihyoh!$"

