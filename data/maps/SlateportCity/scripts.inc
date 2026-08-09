@ Arauna reuses the Slateport City map as Porto das Redes. The original
@ Slateport story (Capt. Stern interview, Scott scenes, Team Aqua grunts,
@ Gabby & Ty) referenced NPC objects that the Porto layout removed, so those
@ vanilla scripts were dropped. Only the map-scripts entry point and the two
@ simple ambient NPCs reused as early-game fallbacks are kept below; all Porto
@ and Serra logic follows.

SlateportCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SlateportCity_OnTransition
	.byte 0

SlateportCity_OnTransition:
	setflag FLAG_VISITED_SLATEPORT_CITY
	end

SlateportCity_EventScript_OldWoman::
	lock
	faceplayer
	call_if_eq VAR_SLATEPORT_CITY_STATE, 1, SlateportCity_EventScript_OldWomanSternInterview
	msgbox SlateportCity_Text_HowTownIsBornAndGrows, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_OldWomanSternInterview::
	msgbox SlateportCity_Text_CaptSternBeingInterviewed, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_Sailor1::
	msgbox SlateportCity_Text_SeaIsSoWet, MSGBOX_NPC
	end

SlateportCity_Text_HowTownIsBornAndGrows:
	.string "Where the water is clean, the fruits\n"
	.string "of bountiful harvest gather.\p"
	.string "And where people gather, a market\n"
	.string "soon starts.\p"
	.string "That is how a town is born and grows.$"

SlateportCity_Text_CaptSternBeingInterviewed:
	.string "I was hoping that it was a famous star\n"
	.string "so I could get an autograph.\p"
	.string "But who's that being interviewed?\n"
	.string "Isn't that CAPT. STERN?$"

SlateportCity_Text_SeaIsSoWet:
	.string "The sea is just so vast…\p"
	.string "Could the sea have been made by\n"
	.string "the tears shed by POKéMON?$"

@ Arauna reuses Slateport City as Porto das Redes and the House of Tide.
AraunaPorto_EventScript_Dockworker::
	goto_if_lt VAR_ARAUNA_ARC_STAGE, 10, SlateportCity_EventScript_Sailor1
	lock
	faceplayer
	goto_if_set FLAG_ARAUNA_PORTO_DOCK_SONG_HEARD, AraunaPorto_EventScript_DockworkerAfter
	msgbox AraunaPorto_Text_DockworkerSong, MSGBOX_DEFAULT
	setflag FLAG_ARAUNA_PORTO_DOCK_SONG_HEARD
	release
	end

AraunaPorto_EventScript_DockworkerAfter::
	msgbox AraunaPorto_Text_DockworkerAfter, MSGBOX_DEFAULT
	release
	end

AraunaPorto_EventScript_ConsortiumAgent::
	goto_if_lt VAR_ARAUNA_ARC_STAGE, 10, AraunaPorto_EventScript_ConsortiumAgentDenial
	lock
	faceplayer
	goto_if_set FLAG_ARAUNA_PORTO_AGENT_DEFEATED, AraunaPorto_EventScript_ConsortiumAgentAfter
	call AraunaPorto_EventScript_CheckEvidence
	goto_if_eq VAR_RESULT, FALSE, AraunaPorto_EventScript_ConsortiumAgentDenial
	msgbox AraunaPorto_Text_ConsortiumAgentConfrontation, MSGBOX_DEFAULT
	special HealPlayerParty
	msgbox AraunaPorto_Text_ConsortiumAgentPreparation, MSGBOX_DEFAULT
	trainerbattle_single TRAINER_ARAUNA_TECH_AGENT, AraunaPorto_Text_ConsortiumAgentBattleIntro, AraunaPorto_Text_ConsortiumAgentBattleDefeated
	setflag FLAG_ARAUNA_PORTO_AGENT_DEFEATED
	setvar VAR_ARAUNA_ARC_STAGE, 12
	msgbox AraunaPorto_Text_ConsortiumAgentAfterBattle, MSGBOX_DEFAULT
	release
	end

AraunaPorto_EventScript_ConsortiumAgentDenial::
	msgbox AraunaPorto_Text_ConsortiumAgentDenial, MSGBOX_DEFAULT
	release
	end

AraunaPorto_EventScript_ConsortiumAgentAfter::
	msgbox AraunaPorto_Text_ConsortiumAgentAfter, MSGBOX_DEFAULT
	release
	end

AraunaPorto_EventScript_CheckEvidence::
	setvar VAR_RESULT, FALSE
	goto_if_unset FLAG_ARAUNA_PORTO_MEMORIAL_HEARD, AraunaPorto_EventScript_CheckEvidenceReturn
	goto_if_unset FLAG_ARAUNA_PORTO_PERMIT_FOUND, AraunaPorto_EventScript_CheckEvidenceReturn
	goto_if_unset FLAG_ARAUNA_PORTO_DOCK_SONG_HEARD, AraunaPorto_EventScript_CheckEvidenceReturn
	goto_if_unset FLAG_ARAUNA_PORTO_NET_FOUND, AraunaPorto_EventScript_CheckEvidenceReturn
	goto_if_unset FLAG_ARAUNA_PORTO_IARACO_SEEN, AraunaPorto_EventScript_CheckEvidenceReturn
	setvar VAR_RESULT, TRUE
AraunaPorto_EventScript_CheckEvidenceReturn::
	return
