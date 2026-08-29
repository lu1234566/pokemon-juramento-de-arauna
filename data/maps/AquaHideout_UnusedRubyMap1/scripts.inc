@ Development harness for the Arauna overworld registry.
@
@ This map is one of the unused Ruby leftovers: nothing warps into it and it had
@ no objects, so placing two here proves the mechanism without touching anything
@ the player can reach.
@
@ Object 1 names OBJ_EVENT_GFX_ARAUNA_POKEMON_A and object 2 names _B. Neither id
@ says which creature it is; both read the registry through their channel, so the
@ two stand side by side showing different species from a single pair of ids.
@ Talking to either steps its channel through the cycle below and refreshes the
@ object in place via SetAraunaPokemonOverworld.

AquaHideout_UnusedRubyMap1_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, AquaHideout_UnusedRubyMap1_OnTransition
	.byte 0

AquaHideout_UnusedRubyMap1_OnTransition::
	setvar VAR_ARAUNA_OW_A, ARAUNA_OW_QUERIBELA
	setvar VAR_ARAUNA_OW_B, ARAUNA_OW_CURUPIRA_ANCIAO
	end

@ Queribela -> Boiuna -> Iemanja -> Anhangau -> Queribela
AquaHideout_UnusedRubyMap1_EventScript_CycleChannelA::
	lock
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, ARAUNA_OW_CHANNEL_A
	compare VAR_ARAUNA_OW_A, ARAUNA_OW_QUERIBELA
	goto_if_eq AquaHideout_UnusedRubyMap1_SetBoiuna
	compare VAR_ARAUNA_OW_A, ARAUNA_OW_BOIUNA
	goto_if_eq AquaHideout_UnusedRubyMap1_SetIemanja
	compare VAR_ARAUNA_OW_A, ARAUNA_OW_IEMANJA
	goto_if_eq AquaHideout_UnusedRubyMap1_SetAnhangau
	setvar VAR_0x8006, ARAUNA_OW_QUERIBELA
	goto AquaHideout_UnusedRubyMap1_ApplyChannel

AquaHideout_UnusedRubyMap1_SetBoiuna::
	setvar VAR_0x8006, ARAUNA_OW_BOIUNA
	goto AquaHideout_UnusedRubyMap1_ApplyChannel

AquaHideout_UnusedRubyMap1_SetIemanja::
	setvar VAR_0x8006, ARAUNA_OW_IEMANJA
	goto AquaHideout_UnusedRubyMap1_ApplyChannel

AquaHideout_UnusedRubyMap1_SetAnhangau::
	setvar VAR_0x8006, ARAUNA_OW_ANHANGAU
	goto AquaHideout_UnusedRubyMap1_ApplyChannel

AquaHideout_UnusedRubyMap1_EventScript_CycleChannelB::
	lock
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, ARAUNA_OW_CHANNEL_B
	compare VAR_ARAUNA_OW_B, ARAUNA_OW_CURUPIRA_ANCIAO
	goto_if_eq AquaHideout_UnusedRubyMap1_SetPretoVelho
	setvar VAR_0x8006, ARAUNA_OW_CURUPIRA_ANCIAO
	goto AquaHideout_UnusedRubyMap1_ApplyChannel

AquaHideout_UnusedRubyMap1_SetPretoVelho::
	setvar VAR_0x8006, ARAUNA_OW_PRETO_VELHO
	goto AquaHideout_UnusedRubyMap1_ApplyChannel

AquaHideout_UnusedRubyMap1_ApplyChannel::
	special SetAraunaPokemonOverworld
	release
	end
