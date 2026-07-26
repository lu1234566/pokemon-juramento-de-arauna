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
AraunaPorto_EventScript_DonaCelina::
	goto_if_lt VAR_ARAUNA_ARC_STAGE, 10, SlateportCity_EventScript_OldWoman
	lock
	faceplayer
	goto_if_eq VAR_ARAUNA_ARC_STAGE, 10, AraunaPorto_EventScript_DonaCelinaIntroduction
	goto_if_eq VAR_ARAUNA_ARC_STAGE, 11, AraunaPorto_EventScript_DonaCelinaInvestigation
	goto_if_eq VAR_ARAUNA_ARC_STAGE, 12, AraunaPorto_EventScript_DonaCelinaRestoreSong
	goto_if_eq VAR_ARAUNA_ARC_STAGE, 13, AraunaPorto_EventScript_DonaCelinaReturnToRiver
	goto_if_eq VAR_ARAUNA_ARC_STAGE, 14, AraunaPorto_EventScript_DonaCelinaAwardBadge
	goto AraunaSerra_EventScript_DonaCelinaTravel

AraunaPorto_EventScript_DonaCelinaIntroduction::
	msgbox AraunaPorto_Text_DonaCelinaIntroduction, MSGBOX_DEFAULT
	setflag FLAG_ARAUNA_PORTO_CELINA_MET
	setflag FLAG_ARAUNA_PORTO_NET_FOUND
	setvar VAR_ARAUNA_ARC_STAGE, 11
	release
	end

AraunaPorto_EventScript_DonaCelinaInvestigation::
	call AraunaPorto_EventScript_CheckEvidence
	goto_if_eq VAR_RESULT, TRUE, AraunaPorto_EventScript_DonaCelinaEvidenceComplete
	msgbox AraunaPorto_Text_DonaCelinaWaiting, MSGBOX_DEFAULT
	release
	end

AraunaPorto_EventScript_DonaCelinaEvidenceComplete::
	msgbox AraunaPorto_Text_DonaCelinaEvidenceComplete, MSGBOX_DEFAULT
	release
	end

AraunaPorto_EventScript_DonaCelinaRestoreSong::
	msgbox AraunaPorto_Text_DonaCelinaNetSong, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_ARC_STAGE, 13
	release
	end

AraunaPorto_EventScript_DonaCelinaReturnToRiver::
	msgbox AraunaPorto_Text_DonaCelinaReturnToRiver, MSGBOX_DEFAULT
	release
	end

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

AraunaPorto_EventScript_DonaCelinaAwardBadge::
	goto_if_set FLAG_ARAUNA_MARE_TRIAL_COMPLETE, AraunaPorto_EventScript_DonaCelinaGrantBadge
	msgbox AraunaPorto_Text_MareTrialInvitation, MSGBOX_DEFAULT
	trainerbattle_single TRAINER_ARAUNA_MARE_TRIAL, AraunaPorto_Text_MareTrialBattleIntro, AraunaPorto_Text_MareTrialBattleDefeated
	setflag FLAG_ARAUNA_MARE_TRIAL_COMPLETE
	msgbox AraunaPorto_Text_MareTrialComplete, MSGBOX_DEFAULT

AraunaPorto_EventScript_DonaCelinaGrantBadge::
	msgbox AraunaPorto_Text_DonaCelinaAwardBadge, MSGBOX_DEFAULT
	setflag FLAG_ARAUNA_BADGE_MARE
	setflag FLAG_BADGE01_GET
	setvar VAR_ARAUNA_BADGE_COUNT, 1
	setvar VAR_ARAUNA_ARC_STAGE, 15
	playfanfare MUS_OBTAIN_BADGE
	waitfanfare
	msgbox AraunaPorto_Text_MareBadgeReceived, MSGBOX_DEFAULT
	call AraunaPorto_EventScript_ZilaSeaCall
	release
	end

@ M15 — the call to Dona Zila. She asks about the sea before the badge, and the
@ answer is kept word for word: the post-game radio repeats it back.
@ Saying nothing leaves the flags clear, so the question can still be answered.
AraunaPorto_EventScript_ZilaSeaCall::
	goto_if_set FLAG_ARAUNA_SEA_DISTANCE, AraunaPorto_EventScript_SeaAlreadyTold
	goto_if_set FLAG_ARAUNA_SEA_SOUND, AraunaPorto_EventScript_SeaAlreadyTold
	goto_if_set FLAG_ARAUNA_SEA_DARK, AraunaPorto_EventScript_SeaAlreadyTold
	msgbox AraunaPorto_Text_ZilaCallIntro, MSGBOX_DEFAULT
	msgbox AraunaPorto_Text_SeaPromptDistance, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, AraunaPorto_EventScript_SeaDistance
	msgbox AraunaPorto_Text_SeaPromptSound, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, AraunaPorto_EventScript_SeaSound
	msgbox AraunaPorto_Text_SeaPromptDark, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, AraunaPorto_EventScript_SeaDark
	msgbox AraunaPorto_Text_SeaSilent, MSGBOX_DEFAULT
	return

AraunaPorto_EventScript_SeaAlreadyTold::
	return

AraunaPorto_EventScript_SeaDistance::
	setflag FLAG_ARAUNA_SEA_DISTANCE
	msgbox AraunaPorto_Text_SeaDistance, MSGBOX_DEFAULT
	return

AraunaPorto_EventScript_SeaSound::
	setflag FLAG_ARAUNA_SEA_SOUND
	msgbox AraunaPorto_Text_SeaSound, MSGBOX_DEFAULT
	return

AraunaPorto_EventScript_SeaDark::
	setflag FLAG_ARAUNA_SEA_DARK
	msgbox AraunaPorto_Text_SeaDark, MSGBOX_DEFAULT
	return

AraunaSerra_EventScript_DonaCelinaTravel::
	msgbox AraunaPorto_Text_DonaCelinaAfterBadge, MSGBOX_DEFAULT
	msgbox AraunaSerra_Text_TravelPrompt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, AraunaSerra_EventScript_StayInPorto
	goto_if_ge VAR_ARAUNA_ARC_STAGE, 20, AraunaSerra_EventScript_TravelToFallarbor
	setvar VAR_ARAUNA_ARC_STAGE, 20
	setflag FLAG_ARAUNA_SERRA_ARRIVED
	setvar VAR_METEOR_FALLS_STATE, 1
	setflag FLAG_HIDE_METEOR_FALLS_TEAM_MAGMA
	setflag FLAG_HIDE_METEOR_FALLS_TEAM_AQUA

AraunaSerra_EventScript_TravelToFallarbor::
	warp MAP_FALLARBOR_TOWN, 255, 10, 13
	waitstate
	end

AraunaSerra_EventScript_StayInPorto::
	msgbox AraunaSerra_Text_TravelLater, MSGBOX_DEFAULT
	release
	end
