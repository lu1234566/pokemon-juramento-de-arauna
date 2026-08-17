# Inherited Emerald admin event discovery

Generated from the current Arauna branch before targeted graphics replacement.

```text
data/maps/EverGrandeCity_SidneysRoom/scripts.inc:79:	.string "Eh, it was fun, so it doesn't matter.$"
data/maps/Route108/scripts.inc:9:Route108_EventScript_Matthew::
data/maps/Route108/scripts.inc:10:	trainerbattle_single TRAINER_MATTHEW, Route108_Text_MatthewIntro, Route108_Text_MatthewDefeated
data/maps/Route108/scripts.inc:11:	msgbox Route108_Text_MatthewPostBattle, MSGBOX_AUTOCLOSE
data/maps/Route108/map.json:64:      "script": "Route108_EventScript_Matthew",
data/maps/PacifidlogTown_PokemonCenter_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/maps/MossdeepCity_SpaceCenter_2F/scripts.inc:164:MossdeepCity_SpaceCenter_2F_EventScript_Tabitha::
data/maps/MossdeepCity_SpaceCenter_2F/scripts.inc:256:	case 1, MossdeepCity_SpaceCenter_2F_EventScript_DefeatedMaxieTabitha
data/maps/MossdeepCity_SpaceCenter_2F/scripts.inc:260:MossdeepCity_SpaceCenter_2F_EventScript_DefeatedMaxieTabitha::
data/maps/MossdeepCity_SpaceCenter_2F/scripts.inc:265:	applymovement LOCALID_SPACE_CENTER_TABITHA, Common_Movement_WalkInPlaceFasterDown
data/maps/MossdeepCity_SpaceCenter_2F/scripts.inc:269:	applymovement LOCALID_SPACE_CENTER_TABITHA, Common_Movement_WalkInPlaceFasterRight
data/maps/MossdeepCity_SpaceCenter_2F/scripts.inc:284:	removeobject LOCALID_SPACE_CENTER_TABITHA
data/maps/MossdeepCity_SpaceCenter_2F/scripts.inc:332:MossdeepCity_SpaceCenter_2F_EventScript_TabithaTrainer::
data/maps/MossdeepCity_SpaceCenter_2F/scripts.inc:333:	trainerbattle TRAINER_BATTLE_SET_TRAINER_B, TRAINER_TABITHA_MOSSDEEP, LOCALID_NONE, MossdeepCity_SpaceCenter_Text_TabithaDefeat, MossdeepCity_SpaceCenter_Text_TabithaDefeat
data/maps/MossdeepCity_SpaceCenter_2F/scripts.inc:477:MossdeepCity_SpaceCenter_Text_TabithaDefeat:
data/maps/MossdeepCity_SpaceCenter_2F/map.json:116:      "local_id": "LOCALID_SPACE_CENTER_TABITHA",
data/maps/MossdeepCity_SpaceCenter_2F/map.json:126:      "script": "MossdeepCity_SpaceCenter_2F_EventScript_Tabitha",
data/maps/LilycoveCity_DepartmentStore_4F/scripts.inc:56:	.string "It's no easy matter to decide which TM\n"
data/maps/DewfordTown_Hall/scripts.inc:361:	.string "Ah, no matter. It's astonishing!$"
data/maps/LavaridgeTown_PokemonCenter_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/maps/DewfordTown_PokemonCenter_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/maps/RustboroCity_PokemonCenter_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/maps/BattleFrontier_OutsideWest/scripts.inc:424:	.string "matter what, until I get a Symbol.$"
data/maps/SootopolisCity/scripts.inc:739:	msgbox SootopolisCity_Text_OhDoesntMatter, MSGBOX_DEFAULT
data/maps/VerdanturfTown_PokemonCenter_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/maps/MossdeepCity_PokemonCenter_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/maps/Route110_TrickHousePuzzle5/scripts.inc:966:	.string "MATTERS OF MONEY ARE MY SOLE FOCUS.$"
data/maps/LilycoveCity_PokemonCenter_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/maps/SlateportCity_PokemonCenter_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/maps/FortreeCity_PokemonCenter_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/maps/EverGrandeCity_PokemonLeague_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/maps/MeteorFalls_1F_1R/scripts.inc:255:	.string "Heh, it doesn't matter!\p"
data/maps/SeafloorCavern_Room3/scripts.inc:4:SeafloorCavern_Room3_EventScript_Shelly::
data/maps/SeafloorCavern_Room3/scripts.inc:5:	trainerbattle_single TRAINER_SHELLY_SEAFLOOR_CAVERN, SeafloorCavern_Room3_Text_ShellyIntro, SeafloorCavern_Room3_Text_ShellyDefeat
data/maps/SeafloorCavern_Room3/scripts.inc:6:	msgbox SeafloorCavern_Room3_Text_ShellyPostBattle, MSGBOX_AUTOCLOSE
data/maps/SeafloorCavern_Room3/scripts.inc:14:SeafloorCavern_Room3_Text_ShellyIntro:
data/maps/SeafloorCavern_Room3/scripts.inc:18:SeafloorCavern_Room3_Text_ShellyDefeat:
data/maps/SeafloorCavern_Room3/scripts.inc:22:SeafloorCavern_Room3_Text_ShellyPostBattle:
data/maps/SeafloorCavern_Room3/map.json:118:      "script": "SeafloorCavern_Room3_EventScript_Shelly",
data/maps/Route112/scripts.inc:128:	.string "easy matter to get back to LAVARIDGE.$"
data/maps/PetalburgCity_PokemonCenter_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/maps/OldaleTown_PokemonCenter_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/maps/BattleFrontier_ScottsHouse/scripts.inc:258:	.string "it doesn't matter who they are.\p"
data/maps/BattleFrontier_BattlePalaceLobby/scripts.inc:606:	.string "may prefer to attack no matter what.\p"
data/maps/MtChimney/scripts.inc:53:	removeobject LOCALID_MT_CHIMNEY_TABITHA
data/maps/MtChimney/scripts.inc:394:MtChimney_EventScript_Tabitha::
data/maps/MtChimney/scripts.inc:395:	trainerbattle_single TRAINER_TABITHA_MT_CHIMNEY, MtChimney_Text_TabithaIntro, MtChimney_Text_TabithaDefeat
data/maps/MtChimney/scripts.inc:396:	msgbox MtChimney_Text_TabithaPostBattle, MSGBOX_AUTOCLOSE
data/maps/MtChimney/scripts.inc:552:MtChimney_Text_TabithaIntro:
data/maps/MtChimney/scripts.inc:559:MtChimney_Text_TabithaDefeat:
data/maps/MtChimney/scripts.inc:564:MtChimney_Text_TabithaPostBattle:
data/maps/MtChimney/map.json:46:      "local_id": "LOCALID_MT_CHIMNEY_TABITHA",
data/maps/MtChimney/map.json:56:      "script": "MtChimney_EventScript_Tabitha",
data/maps/BattleFrontier_PokemonCenter_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/maps/AquaHideout_B2F/scripts.inc:6:	call_if_set FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE, AquaHideout_B2F_EventScript_PreventMattNoticing
data/maps/AquaHideout_B2F/scripts.inc:9:AquaHideout_B2F_EventScript_PreventMattNoticing::
data/maps/AquaHideout_B2F/scripts.inc:13:AquaHideout_B2F_EventScript_MattNoticePlayer::
data/maps/AquaHideout_B2F/scripts.inc:15:	setvar VAR_0x8008, LOCALID_AQUA_HIDEOUT_MATT
data/maps/AquaHideout_B2F/scripts.inc:25:AquaHideout_B2F_EventScript_Matt::
data/maps/AquaHideout_B2F/scripts.inc:26:	trainerbattle_single TRAINER_MATT, AquaHideout_B2F_Text_MattIntro, AquaHideout_B2F_Text_MattDefeat, AquaHideout_B2F_EventScript_SubmarineEscape
data/maps/AquaHideout_B2F/scripts.inc:27:	msgbox AquaHideout_B2F_Text_MattPostBattle, MSGBOX_DEFAULT
data/maps/AquaHideout_B2F/scripts.inc:32:	setvar VAR_0x8008, LOCALID_AQUA_HIDEOUT_MATT
data/maps/AquaHideout_B2F/scripts.inc:48:	msgbox AquaHideout_B2F_Text_MattPostBattle, MSGBOX_DEFAULT
data/maps/AquaHideout_B2F/scripts.inc:89:AquaHideout_B2F_Text_MattIntro:
data/maps/AquaHideout_B2F/scripts.inc:99:AquaHideout_B2F_Text_MattDefeat:
data/maps/AquaHideout_B2F/scripts.inc:107:AquaHideout_B2F_Text_MattPostBattle:
data/maps/AquaHideout_B2F/map.json:18:      "local_id": "LOCALID_AQUA_HIDEOUT_MATT",
data/maps/AquaHideout_B2F/map.json:28:      "script": "AquaHideout_B2F_EventScript_Matt",
data/maps/AquaHideout_B2F/map.json:178:      "script": "AquaHideout_B2F_EventScript_MattNoticePlayer"
data/maps/AquaHideout_B2F/map.json:187:      "script": "AquaHideout_B2F_EventScript_MattNoticePlayer"
data/maps/Route119_WeatherInstitute_2F/scripts.inc:41:Route119_WeatherInstitute_2F_EventScript_Shelly::
data/maps/Route119_WeatherInstitute_2F/scripts.inc:42:	trainerbattle_single TRAINER_SHELLY_WEATHER_INSTITUTE, Route119_WeatherInstitute_2F_Text_ShellyIntro, Route119_WeatherInstitute_2F_Text_ShellyDefeat, Route119_WeatherInstitute_2F_EventScript_ShellyDefeated
data/maps/Route119_WeatherInstitute_2F/scripts.inc:43:	msgbox Route119_WeatherInstitute_2F_Text_ShellyPostBattle, MSGBOX_AUTOCLOSE
data/maps/Route119_WeatherInstitute_2F/scripts.inc:46:Route119_WeatherInstitute_2F_EventScript_ShellyDefeated::
data/maps/Route119_WeatherInstitute_2F/scripts.inc:47:	msgbox Route119_WeatherInstitute_2F_Text_ShellyPostBattle, MSGBOX_DEFAULT
data/maps/Route119_WeatherInstitute_2F/scripts.inc:50:	applymovement LOCALID_WEATHER_INSTITUTE_2F_GRUNT_3, Route119_WeatherInstitute_2F_Movement_GruntApproachShelly
data/maps/Route119_WeatherInstitute_2F/scripts.inc:56:	applymovement LOCALID_WEATHER_INSTITUTE_2F_SHELLY, Common_Movement_ExclamationMark
data/maps/Route119_WeatherInstitute_2F/scripts.inc:58:	applymovement LOCALID_WEATHER_INSTITUTE_2F_SHELLY, Common_Movement_Delay48
data/maps/Route119_WeatherInstitute_2F/scripts.inc:70:	removeobject LOCALID_WEATHER_INSTITUTE_2F_SHELLY
data/maps/Route119_WeatherInstitute_2F/scripts.inc:164:Route119_WeatherInstitute_2F_Movement_GruntApproachShelly:
data/maps/Route119_WeatherInstitute_2F/scripts.inc:250:Route119_WeatherInstitute_2F_Text_ShellyIntro:
data/maps/Route119_WeatherInstitute_2F/scripts.inc:255:Route119_WeatherInstitute_2F_Text_ShellyDefeat:
data/maps/Route119_WeatherInstitute_2F/scripts.inc:259:Route119_WeatherInstitute_2F_Text_ShellyPostBattle:
data/maps/Route119_WeatherInstitute_2F/map.json:46:      "local_id": "LOCALID_WEATHER_INSTITUTE_2F_SHELLY",
data/maps/Route119_WeatherInstitute_2F/map.json:56:      "script": "Route119_WeatherInstitute_2F_EventScript_Shelly",
data/maps/EverGrandeCity_PokemonCenter_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/maps/VerdanturfTown_BattleTentLobby/scripts.inc:329:	.string "It doesn't matter how strong it is,\n"
data/maps/VerdanturfTown_BattleTentLobby/scripts.inc:349:	.string "Well, it doesn't matter.\p"
data/maps/VerdanturfTown_BattleTentLobby/scripts.inc:371:	.string "It doesn't matter what the rules are,\n"
data/maps/SootopolisCity_PokemonCenter_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/maps/MagmaHideout_4F/scripts.inc:69:	removeobject LOCALID_MAGMA_HIDEOUT_4F_TABITHA
data/maps/MagmaHideout_4F/scripts.inc:122:MagmaHideout_4F_EventScript_Tabitha::
data/maps/MagmaHideout_4F/scripts.inc:123:	trainerbattle_single TRAINER_TABITHA_MAGMA_HIDEOUT, MagmaHideout_4F_Text_TabithaIntro, MagmaHideout_4F_Text_TabithaDefeat
data/maps/MagmaHideout_4F/scripts.inc:124:	msgbox MagmaHideout_4F_Text_TabithaPostBattle, MSGBOX_AUTOCLOSE
data/maps/MagmaHideout_4F/scripts.inc:166:MagmaHideout_4F_Text_TabithaIntro:
data/maps/MagmaHideout_4F/scripts.inc:171:MagmaHideout_4F_Text_TabithaDefeat:
data/maps/MagmaHideout_4F/scripts.inc:175:MagmaHideout_4F_Text_TabithaPostBattle:
data/maps/MagmaHideout_4F/map.json:74:      "local_id": "LOCALID_MAGMA_HIDEOUT_4F_TABITHA",
data/maps/MagmaHideout_4F/map.json:84:      "script": "MagmaHideout_4F_EventScript_Tabitha",
data/maps/MauvilleCity_PokemonCenter_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/maps/FallarborTown_PokemonCenter_2F/map.json:27:      "script": "Common_EventScript_UnionRoomAttendant",
data/scripts/cable_club.inc:823:CableClub_EventScript_UnionRoomAttendant::
```
