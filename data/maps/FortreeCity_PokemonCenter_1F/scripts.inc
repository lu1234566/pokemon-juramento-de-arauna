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
	.string "Hey, are you putting a POKéDEX\n"
	.string "together?\p"
	.string "Then visit the RESERVA ARAUNA. You may\n"
	.string "find new things there.$"

FortreeCity_PokemonCenter_1F_Text_RecordCornerIsNeat:
	.string "Have you used the RECORD CORNER?\p"
	.string "It mixes together the records of\n"
	.string "different TRAINERS.\p"
	.string "I don't really follow how it works, but\n"
	.string "it's fascinating.$"

FortreeCity_PokemonCenter_1F_Text_DoYouKnowAboutPokenav:
	.string "You have a POKéNAV too! Yours looks\n"
	.string "just like mine.\p"
	.string "Do you know the MATCH CALL system?\p"
	.string "It lets you talk to TRAINERS you've\n"
	.string "registered.\p"
	.string "It also shows who's ready for a rematch.\p"
	.string "The people at HORIZON built a genuinely\n"
	.string "useful system.$"

