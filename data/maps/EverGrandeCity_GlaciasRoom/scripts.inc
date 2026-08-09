EverGrandeCity_GlaciasRoom_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, EverGrandeCity_GlaciasRoom_OnFrame
	map_script MAP_SCRIPT_ON_LOAD, EverGrandeCity_GlaciasRoom_OnLoad
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, EverGrandeCity_GlaciasRoom_OnWarp
	.byte 0

EverGrandeCity_GlaciasRoom_OnWarp:
	map_script_2 VAR_TEMP_1, 0, EverGrandeCity_GlaciasRoom_EventScript_PlayerTurnNorth
	.2byte 0

EverGrandeCity_GlaciasRoom_EventScript_PlayerTurnNorth::
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

EverGrandeCity_GlaciasRoom_OnFrame:
	map_script_2 VAR_ELITE_4_STATE, 2, EverGrandeCity_GlaciasRoom_EventScript_WalkInCloseDoor
	.2byte 0

EverGrandeCity_GlaciasRoom_EventScript_WalkInCloseDoor::
	lockall
	call PokemonLeague_EliteFour_EventScript_WalkInCloseDoor
	setvar VAR_ELITE_4_STATE, 3
	releaseall
	end

EverGrandeCity_GlaciasRoom_OnLoad:
	call_if_set FLAG_DEFEATED_ELITE_4_GLACIA, EverGrandeCity_GlaciasRoom_EventScript_ResetAdvanceToNextRoom
	call_if_eq VAR_ELITE_4_STATE, 3, EverGrandeCity_GlaciasRoom_EventScript_CloseDoor
	end

EverGrandeCity_GlaciasRoom_EventScript_ResetAdvanceToNextRoom::
	call PokemonLeague_EliteFour_EventScript_ResetAdvanceToNextRoom
	return

EverGrandeCity_GlaciasRoom_EventScript_CloseDoor::
	call PokemonLeague_EliteFour_EventScript_CloseDoor
	return

EverGrandeCity_GlaciasRoom_EventScript_Glacia::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_ELITE_4_GLACIA, EverGrandeCity_GlaciasRoom_EventScript_PostBattleSpeech
	playbgm MUS_ENCOUNTER_ELITE_FOUR, FALSE
	msgbox EverGrandeCity_GlaciasRoom_Text_IntroSpeech, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_GLACIA, EverGrandeCity_GlaciasRoom_Text_Defeat
	goto EverGrandeCity_GlaciasRoom_EventScript_Defeated
	end

EverGrandeCity_GlaciasRoom_EventScript_PostBattleSpeech::
	msgbox EverGrandeCity_GlaciasRoom_Text_PostBattleSpeech, MSGBOX_DEFAULT
	call_if_eq VAR_ARAUNA_BOND_CHOICE, 2, EverGrandeCity_GlaciasRoom_EventScript_BondWisdom
	release
	end

EverGrandeCity_GlaciasRoom_EventScript_Defeated::
	setflag FLAG_DEFEATED_ELITE_4_GLACIA
	call PokemonLeague_EliteFour_SetAdvanceToNextRoomMetatiles
	msgbox EverGrandeCity_GlaciasRoom_Text_PostBattleSpeech, MSGBOX_DEFAULT
	call_if_eq VAR_ARAUNA_BOND_CHOICE, 2, EverGrandeCity_GlaciasRoom_EventScript_BondWisdom
	release
	end

EverGrandeCity_GlaciasRoom_Text_IntroSpeech:
	.string "I am CLARA, of the ELITE.\p"
	.string "A document can lie.\p"
	.string "A memory can fail.\p"
	.string "That does not make either one\n"
	.string "useless.\p"
	.string "It makes you responsible for\n"
	.string "crossing one against the other.$"

EverGrandeCity_GlaciasRoom_Text_Defeat:
	.string "You did not choose the most\n"
	.string "comfortable proof.\p"
	.string "You chose the one that survived\n"
	.string "the questions.$"

EverGrandeCity_GlaciasRoom_Text_PostBattleSpeech:
	.string "Cross-check everything, even\n"
	.string "what you wish were true.\p"
	.string "Advance to the next room.$"

@ Bond payoff: the Wisdom rescue preserved the siphon logs, and the Guardian of
@ Proof is the one person in Arauna who would have read them.
EverGrandeCity_GlaciasRoom_EventScript_BondWisdom::
	msgbox EverGrandeCity_GlaciasRoom_Text_BondWisdom, MSGBOX_DEFAULT
	return

EverGrandeCity_GlaciasRoom_Text_BondWisdom:
	.string "CLARA: One more thing.\p"
	.string "The logs from that first ruin\n"
	.string "survived.\p"
	.string "Somebody shut a siphon down\n"
	.string "without smashing it open.\p"
	.string "I have read them.\p"
	.string "They are most of the reason\n"
	.string "I believe you.$"
