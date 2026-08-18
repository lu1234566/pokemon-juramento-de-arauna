VictoryRoad_B1F_MapScripts::
	.byte 0

VictoryRoad_B1F_EventScript_Samuel::
	trainerbattle_single TRAINER_SAMUEL, VictoryRoad_B1F_Text_SamuelIntro, VictoryRoad_B1F_Text_SamuelDefeat
	msgbox VictoryRoad_B1F_Text_SamuelPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_EventScript_Shannon::
	trainerbattle_single TRAINER_SHANNON, VictoryRoad_B1F_Text_ShannonIntro, VictoryRoad_B1F_Text_ShannonDefeat
	msgbox VictoryRoad_B1F_Text_ShannonPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_EventScript_Michelle::
	trainerbattle_single TRAINER_MICHELLE, VictoryRoad_B1F_Text_MichelleIntro, VictoryRoad_B1F_Text_MichelleDefeat
	msgbox VictoryRoad_B1F_Text_MichellePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_EventScript_Mitchell::
	trainerbattle_single TRAINER_MITCHELL, VictoryRoad_B1F_Text_MitchellIntro, VictoryRoad_B1F_Text_MitchellDefeat
	msgbox VictoryRoad_B1F_Text_MitchellPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_EventScript_Halle::
	trainerbattle_single TRAINER_HALLE, VictoryRoad_B1F_Text_HalleIntro, VictoryRoad_B1F_Text_HalleDefeat
	msgbox VictoryRoad_B1F_Text_HallePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_Text_SamuelIntro:
	.string "Quanto mais perto da LIGA fico,\n"
	.string "mais nervoso eu me sinto...$"

VictoryRoad_B1F_Text_SamuelDefeat:
	.string "Eu nao consegui fazer nada...$"

VictoryRoad_B1F_Text_SamuelPostBattle:
	.string "A LIGA parece longe de novo...\n"
	.string "Que decepcao...$"

VictoryRoad_B1F_Text_ShannonIntro:
	.string "Na LIGA, voce precisa\n"
	.string "da confianca dos seus POKéMON.$"

VictoryRoad_B1F_Text_ShannonDefeat:
	.string "A confianca entre voces e forte.$"

VictoryRoad_B1F_Text_ShannonPostBattle:
	.string "Quanto mais tempo passam juntos,\n"
	.string "mais cresce a confianca entre\n"
	.string "TRAINER e POKéMON.$"

VictoryRoad_B1F_Text_MichelleIntro:
	.string "Isto nao e a chegada.\n"
	.string "E so mais um passo ate a LIGA.$"

VictoryRoad_B1F_Text_MichelleDefeat:
	.string "Esse e o caminho!$"

VictoryRoad_B1F_Text_MichellePostBattle:
	.string "Voce vai ficar bem!\n"
	.string "Seus POKéMON estao prontos.$"

VictoryRoad_B1F_Text_MitchellIntro:
	.string "Meus POKéMON sao uma forca\n"
	.string "de outro mundo!$"

VictoryRoad_B1F_Text_MitchellDefeat:
	.string "Nunca enfrentei alguem assim.$"

VictoryRoad_B1F_Text_MitchellPostBattle:
	.string "Mesmo fora de batalha, da para\n"
	.string "sentir a forca que existe entre\n"
	.string "voce e seus POKéMON.$"

VictoryRoad_B1F_Text_HalleIntro:
	.string "Ei, relaxe um pouco!\n"
	.string "Vamos lutar sem tanta tensao.$"

VictoryRoad_B1F_Text_HalleDefeat:
	.string "Uau!\n"
	.string "Que maravilha!$"

VictoryRoad_B1F_Text_HallePostBattle:
	.string "Sim, esta e a ESTRADA DO\n"
	.string "JURAMENTO.\p"
	.string "Mas ela nao e tao diferente\n"
	.string "do caminho que trouxe voce ate\n"
	.string "aqui. Aproveite o restante!$"

