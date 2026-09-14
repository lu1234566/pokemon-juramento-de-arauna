NavelRock_Top_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, NavelRock_Top_OnTransition
	.byte 0

NavelRock_Top_OnTransition:
	setflag FLAG_HIDE_HO_OH
	setvar VAR_TEMP_1, 0
	goto_if_set FLAG_CAUGHT_HO_OH, NavelRock_Top_EventScript_CloseSolarisTrigger
	goto_if_set FLAG_DEFEATED_HO_OH, NavelRock_Top_EventScript_CloseSolarisTrigger
	end

NavelRock_Top_EventScript_CloseSolarisTrigger::
	setvar VAR_TEMP_1, 1
	return

NavelRock_Top_EventScript_HoOh::
	lockall
	setvar VAR_TEMP_1, 1
	msgbox NavelRock_Top_Text_SolarisAwakens, MSGBOX_DEFAULT
	playbgm MUS_ARAUNA_LEGEND_ENCOUNTER, FALSE
	setweather WEATHER_NONE
	doweather
	waitse
	playmoncry SPECIES_REGISTEEL, CRY_MODE_ENCOUNTER  @ #379 Solaris
	delay 40
	waitmoncry
	setwildbattle SPECIES_REGISTEEL, 70  @ #379 Solaris
	special BattleSetup_StartLegendaryBattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, NavelRock_Top_EventScript_DefeatedSolaris
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, NavelRock_Top_EventScript_RanFromSolaris
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, NavelRock_Top_EventScript_RanFromSolaris
	setflag FLAG_CAUGHT_HO_OH
	releaseall
	end

NavelRock_Top_EventScript_DefeatedSolaris::
	setflag FLAG_DEFEATED_HO_OH
	setvar VAR_0x8004, SPECIES_REGISTEEL
	goto Common_EventScript_LegendaryFlewAway
	end

NavelRock_Top_EventScript_RanFromSolaris::
	setvar VAR_0x8004, SPECIES_REGISTEEL
	goto Common_EventScript_LegendaryFlewAway
	end

NavelRock_Top_Text_SolarisAwakens:
	.string "A white sun opens above the altar.\p"
	.string "Heat gathers into a living shape.$"
