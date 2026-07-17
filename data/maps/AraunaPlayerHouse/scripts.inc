AraunaPlayerHouse_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, AraunaPlayerHouse_OnFrame
	.byte 0

AraunaPlayerHouse_OnFrame:
	map_script_2 VAR_ARAUNA_STORY_STAGE, 0, AraunaPlayerHouse_EventScript_WakeUp
	.2byte 0

AraunaPlayerHouse_EventScript_WakeUp::
	lockall
	msgbox AraunaPlayerHouse_Text_WakeUp, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_STORY_STAGE, 1
	releaseall
	end

AraunaPlayerHouse_EventScript_Responsible::
	lock
	faceplayer
	goto_if_eq VAR_ARAUNA_STORY_STAGE, 1, AraunaPlayerHouse_EventScript_CenterReminder
	msgbox AraunaPlayerHouse_Text_ResponsibleAfterCall, MSGBOX_DEFAULT
	release
	end

AraunaPlayerHouse_EventScript_CenterReminder::
	msgbox AraunaPlayerHouse_Text_CenterReminder, MSGBOX_DEFAULT
	release
	end
