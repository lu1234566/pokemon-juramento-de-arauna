PacifidlogTown_House5_MapScripts::
	.byte 0

PacifidlogTown_House5_EventScript_MirageIslandWatcher::
	lock
	faceplayer
	specialvar VAR_RESULT, IsMirageIslandPresent
	goto_if_eq VAR_RESULT, TRUE, PacifidlogTown_House5_EventScript_MirageIslandPresent
	msgbox PacifidlogTown_House5_Text_CantSeeMirageIslandToday, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_House5_EventScript_MirageIslandPresent::
	msgbox PacifidlogTown_House5_Text_CanSeeMirageIslandToday, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_House5_EventScript_Gentleman::
	msgbox PacifidlogTown_House5_Text_MirageIslandAppearDependingOnWeather, MSGBOX_NPC
	end

PacifidlogTown_House5_Text_CantSeeMirageIslandToday:
	.string "From the fire, I can't see\n"
	.string "ILHA MIRAGEM today…$"

PacifidlogTown_House5_Text_CanSeeMirageIslandToday:
	.string "Look out past the water!\n"
	.string "ILHA MIRAGEM has appeared!$"

PacifidlogTown_House5_Text_MirageIslandAppearDependingOnWeather:
	.string "Around the fire, everyone tells\n"
	.string "the island a different way.\p"
	.string "Some say it's the weather turning.\n"
	.string "Others, that it comes and goes.$"
