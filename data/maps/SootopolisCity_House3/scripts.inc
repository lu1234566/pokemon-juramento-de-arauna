SootopolisCity_House3_MapScripts::
	.byte 0

SootopolisCity_House3_EventScript_Woman::
	lock
	faceplayer
	msgbox SootopolisCity_House3_Text_JuanHasManyFansDoYou, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, SootopolisCity_House3_EventScript_HaveFans
	msgbox SootopolisCity_House3_Text_LonesomeTryWorkingHarder, MSGBOX_DEFAULT
	release
	end

SootopolisCity_House3_EventScript_HaveFans::
	msgbox SootopolisCity_House3_Text_YouMustBePrettyStrong, MSGBOX_DEFAULT
	release
	end

SootopolisCity_House3_EventScript_Girl::
	msgbox SootopolisCity_House3_Text_TrainerFanClubWasWild, MSGBOX_NPC
	end

SootopolisCity_House3_Text_JuanHasManyFansDoYou:
	.string "AMALIA: Arauna sobreviveu a\nverdade pela metade por tempo\p"
	.string "demais. A Liga tambem tem\ndividas com os nomes que foram\p"
	.string "deixados para tras.$"

SootopolisCity_House3_Text_YouMustBePrettyStrong:
	.string "Existem placas novas por toda\nparte. Curioso e que alguns\p"
	.string "nomes antigos desapareceram\nquando elas chegaram.$"

SootopolisCity_House3_Text_LonesomeTryWorkingHarder:
	.string "Ultimamente alguns Pokemon\nparam diante de suas antigas\p"
	.string "casas como se nunca tivessem\nestado ali.$"

SootopolisCity_House3_Text_TrainerFanClubWasWild:
	.string "Tem gente que chama de\nDESENCANTO. Eu chamava de\p"
	.string "distraicao, ate minha mae\nesquecer a cancao que cantava\p"
	.string "desde crianca.$"

