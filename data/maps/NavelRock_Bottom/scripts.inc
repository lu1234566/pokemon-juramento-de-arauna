NavelRock_Bottom_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, NavelRock_Bottom_OnTransition
	.byte 0

NavelRock_Bottom_OnTransition:
	@ The inherited Lugia overworld is not Piraruacu art. Keep it hidden and
	@ let the submerged altar itself carry the encounter.
	setflag FLAG_HIDE_LUGIA
	end

NavelRock_Bottom_EventScript_Lugia::
	lock
	goto_if_set FLAG_CAUGHT_LUGIA, NavelRock_Bottom_EventScript_EmptyAltar
	msgbox NavelRock_Bottom_Text_PiraruacuAwakens, MSGBOX_DEFAULT
	playbgm MUS_ARAUNA_LEGEND_ENCOUNTER, FALSE
	waitse
	playmoncry SPECIES_REGIROCK, CRY_MODE_ENCOUNTER  @ #377 Piraruacu
	delay 40
	waitmoncry
	setwildbattle SPECIES_REGIROCK, 70  @ #377 Piraruacu
	special BattleSetup_StartLegendaryBattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, NavelRock_Bottom_EventScript_PiraruacuFled
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, NavelRock_Bottom_EventScript_PiraruacuFled
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, NavelRock_Bottom_EventScript_PiraruacuFled
	setflag FLAG_CAUGHT_LUGIA
	release
	end

NavelRock_Bottom_EventScript_PiraruacuFled::
	setvar VAR_0x8004, SPECIES_REGIROCK
	goto Common_EventScript_LegendaryFlewAway
	end

NavelRock_Bottom_EventScript_EmptyAltar::
	msgbox NavelRock_Bottom_Text_EmptyAltar, MSGBOX_DEFAULT
	release
	end

NavelRock_Bottom_Text_PiraruacuAwakens:
	.string "The black water rises without a wave.\p"
	.string "Something enormous breathes below.$"

NavelRock_Bottom_Text_EmptyAltar:
	.string "The deep water is quiet now.$"
