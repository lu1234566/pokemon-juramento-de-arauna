FortreeCity_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FortreeCity_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

FortreeCity_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_FORTREE_CITY
	end

FortreeCity_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_FORTREE_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

FortreeCity_PokemonCenter_1F_EventScript_Gentleman::
	msgbox FortreeCity_PokemonCenter_1F_Text_GoToSafariZone, MSGBOX_NPC
	end

FortreeCity_PokemonCenter_1F_EventScript_Man::
	msgbox FortreeCity_PokemonCenter_1F_Text_RecordCornerIsNeat, MSGBOX_NPC
	end

FortreeCity_PokemonCenter_1F_EventScript_Boy::
	msgbox FortreeCity_PokemonCenter_1F_Text_DoYouKnowAboutPokenav, MSGBOX_NPC
	end

FortreeCity_PokemonCenter_1F_Text_GoToSafariZone:
	.string "Ei, voce esta montando uma\n"
	.string "POKéDEX?\p"
	.string "Entao visite a SAFARI ZONE.\n"
	.string "Pode encontrar coisas novas la.$"

FortreeCity_PokemonCenter_1F_Text_RecordCornerIsNeat:
	.string "Ja usou o RECORD CORNER?\p"
	.string "Ele mistura registros de\n"
	.string "TRAINERS diferentes.\p"
	.string "Nao entendo bem como funciona,\n"
	.string "mas e bem interessante.$"

FortreeCity_PokemonCenter_1F_Text_DoYouKnowAboutPokenav:
	.string "Voce tambem tem um POKéNAV!\n"
	.string "O seu parece igual ao meu.\p"
	.string "Conhece o sistema MATCH CALL?\p"
	.string "Ele permite falar com TRAINERS\n"
	.string "que voce ja registrou.\p"
	.string "Tambem mostra quem esta pronto\n"
	.string "para uma revanche.\p"
	.string "O pessoal do HORIZONTE fez\n"
	.string "um sistema bem util.$"

