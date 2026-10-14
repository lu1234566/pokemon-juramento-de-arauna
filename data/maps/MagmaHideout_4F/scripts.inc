MagmaHideout_4F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MagmaHideout_4F_OnTransition
	.byte 0

@ RAUL's object event is OBJ_EVENT_GFX_VAR_B, so the var has to name him before
@ the map spawns its objects. The object gfx vars are per-map scratch -- the
@ decoration rooms rewrite the same one from the save on every entry -- so this
@ claims it here and nothing else's use of it is disturbed.
MagmaHideout_4F_OnTransition:
	setvar VAR_OBJ_GFX_ID_B, ARAUNA_VIRTUAL_GFX_RAUL
	end

MagmaHideout_4F_EventScript_Maxie::
	lockall
	playbgm MUS_ENCOUNTER_MAGMA, FALSE
	msgbox MagmaHideout_4F_Text_MaxieAwakenGroudon, MSGBOX_DEFAULT
	closemessage
	delay 20
	setvar VAR_RESULT, 1
	playse SE_M_DETECT
	dofieldeffectsparkle 18, 42, 0
	waitfieldeffect FLDEFF_SPARKLE
	setvar VAR_RESULT, 1
	playfanfare MUS_AWAKEN_LEGEND
	playse SE_ORB
	special DoOrbEffect
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	delay 150
	removeobject LOCALID_MAGMA_HIDEOUT_4F_GROUDON_SLEEPING
	addobject LOCALID_MAGMA_HIDEOUT_4F_GROUDON
	waitstate
	delay 60
	applymovement LOCALID_MAGMA_HIDEOUT_4F_GROUDON, MagmaHideout_4F_Movement_GroudonApproach
	waitmovement 0
	special FadeOutOrbEffect
	setvar VAR_0x8004, 1  @ vertical pan
	setvar VAR_0x8005, 1  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 5  @ shake delay
	special ShakeCamera
	waitstate
	applymovement LOCALID_MAGMA_HIDEOUT_4F_GROUDON, MagmaHideout_4F_Movement_GroudonExit
	waitmovement 0
	removeobject LOCALID_MAGMA_HIDEOUT_4F_GROUDON
	delay 4
	setvar VAR_0x8004, 2  @ vertical pan
	setvar VAR_0x8005, 2  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 5  @ shake delay
	special ShakeCamera
	waitstate
	delay 30
	applymovement LOCALID_MAGMA_HIDEOUT_4F_MAXIE, MagmaHideout_4F_Movement_MaxieLookAround
	waitmovement 0
	msgbox MagmaHideout_4F_Text_MaxieGroudonWhatsWrong, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	delay 30
	applymovement LOCALID_MAGMA_HIDEOUT_4F_MAXIE, Common_Movement_FacePlayer
	waitmovement 0
	msgbox MagmaHideout_4F_Text_MaxieOhItWasYou, MSGBOX_DEFAULT
	closemessage
	trainerbattle_no_intro TRAINER_MAXIE_MAGMA_HIDEOUT, MagmaHideout_4F_Text_MaxieDefeat
	msgbox MagmaHideout_4F_Text_MaxieImGoingAfterGroudon, MSGBOX_DEFAULT
	closemessage
	clearflag FLAG_HIDE_SLATEPORT_CITY_CAPTAIN_STERN
	clearflag FLAG_HIDE_SLATEPORT_CITY_GABBY_AND_TY
	setvar VAR_SLATEPORT_CITY_STATE, 1
	setflag FLAG_GROUDON_AWAKENED_MAGMA_HIDEOUT
	setvar VAR_SLATEPORT_HARBOR_STATE, 1
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_MAGMA_HIDEOUT_4F_MAXIE
	removeobject LOCALID_MAGMA_HIDEOUT_4F_GRUNT_1
	removeobject LOCALID_MAGMA_HIDEOUT_4F_GRUNT_2
	removeobject LOCALID_MAGMA_HIDEOUT_4F_GRUNT_3
	removeobject LOCALID_MAGMA_HIDEOUT_4F_TABITHA
	setflag FLAG_HIDE_MAGMA_HIDEOUT_GRUNTS
	fadescreen FADE_FROM_BLACK
	releaseall
	end

MagmaHideout_4F_Movement_GroudonApproach:
	delay_16
	delay_16
	walk_slow_down
	delay_16
	delay_16
	delay_16
	walk_slow_down
	delay_16
	delay_16
	delay_16
	step_end

MagmaHideout_4F_Movement_GroudonExit:
	slide_up
	slide_up
	step_end

MagmaHideout_4F_Movement_MaxieLookAround:
	face_left
	delay_16
	face_right
	delay_16
	face_left
	delay_16
	face_right
	delay_16
	face_up
	delay_16
	delay_16
	step_end

MagmaHideout_4F_EventScript_Grunt11::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_11, MagmaHideout_4F_Text_Grunt11Intro, MagmaHideout_4F_Text_Grunt11Defeat
	msgbox MagmaHideout_4F_Text_Grunt11PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_4F_EventScript_Grunt12::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_12, MagmaHideout_4F_Text_Grunt12Intro, MagmaHideout_4F_Text_Grunt12Defeat
	msgbox MagmaHideout_4F_Text_Grunt12PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_4F_EventScript_Grunt13::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_13, MagmaHideout_4F_Text_Grunt13Intro, MagmaHideout_4F_Text_Grunt13Defeat
	msgbox MagmaHideout_4F_Text_Grunt13PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_4F_EventScript_Tabitha::
	trainerbattle_single TRAINER_TABITHA_MAGMA_HIDEOUT, MagmaHideout_4F_Text_TabithaIntro, MagmaHideout_4F_Text_TabithaDefeat
	msgbox MagmaHideout_4F_Text_TabithaPostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_4F_Text_Grunt11Intro:
	.string "REMEMBRANCER:\n"
	.string "The core is reacting.\p"
	.string "Stay away from the equipment.$"

MagmaHideout_4F_Text_Grunt11Defeat:
	.string "REMEMBRANCER: Readings jumped\n"
	.string "when LUZIA touched the MATRIX.$"

MagmaHideout_4F_Text_Grunt11PostBattle:
	.string "REMEMBRANCER:\n"
	.string "This isn't returning one story\n"
	.string "at a time.\p"
	.string "It's pulling thousands.$"

MagmaHideout_4F_Text_Grunt12Intro:
	.string "REMEMBRANCER:\n"
	.string "LUZIA asked for trust.\p"
	.string "I wish I'd asked for a plan.$"

MagmaHideout_4F_Text_Grunt12Defeat:
	.string "REMEMBRANCER: HORIZON will use\n"
	.string "this against all of us.$"

MagmaHideout_4F_Text_Grunt12PostBattle:
	.string "REMEMBRANCER: And they may be\n"
	.string "right about the risk.\p"
	.string "I hate admitting that.$"

MagmaHideout_4F_Text_Grunt13Intro:
	.string "REMEMBRANCER:\n"
	.string "The MATRIX opened a passage\n"
	.string "we don't know how to close.$"

MagmaHideout_4F_Text_Grunt13Defeat:
	.string "REMEMBRANCER:\n"
	.string "I can't call this simple\n"
	.string "restoration anymore.$"

MagmaHideout_4F_Text_Grunt13PostBattle:
	.string "REMEMBRANCER:\n"
	.string "Go. If LUZIA won't hear us,\n"
	.string "maybe she'll hear you.$"

MagmaHideout_4F_Text_TabithaIntro:
	.string "RAUL: Enough.\p"
	.string "You've seen more of this base\n"
	.string "than you should have.$"

MagmaHideout_4F_Text_TabithaDefeat:
	.string "RAUL: Damn...\p"
	.string "Then pass. But beating me does\n"
	.string "not make you right.$"

MagmaHideout_4F_Text_TabithaPostBattle:
	.string "RAUL: I follow LUZIA because I\n"
	.string "saw families erased on paper.\p"
	.string "That doesn't mean I'm not afraid\n"
	.string "of what she'll do.$"

MagmaHideout_4F_Text_MaxieAwakenGroudon:
	.string "LUZIA: This RECORD-MATRIX was\n"
	.string "built to find what the ARCHIVE\n"
	.string "tore away.\p"
	.string "Today it returns to Arauna.$"

MagmaHideout_4F_Text_MaxieGroudonWhatsWrong:
	.string "LUZIA: Wait...\p"
	.string "The current isn't following the\n"
	.string "MATRIX.\p"
	.string "It's pulling everything.$"

MagmaHideout_4F_Text_MaxieOhItWasYou:
	.string "LUZIA: You made it this far.\p"
	.string "If you came to stop me, show me\n"
	.string "another way.$"

MagmaHideout_4F_Text_MaxieDefeat:
	.string "LUZIA: Losing a battle doesn't\n"
	.string "make HORIZON right.\p"
	.string "But I heard what you showed me.$"

MagmaHideout_4F_Text_MaxieImGoingAfterGroudon:
	.string "LUZIA: The current escaped.\p"
	.string "Signals lead toward the coast.\p"
	.string "I'm going to PORTO DO SAL before\n"
	.string "HORIZON gets there.$"
