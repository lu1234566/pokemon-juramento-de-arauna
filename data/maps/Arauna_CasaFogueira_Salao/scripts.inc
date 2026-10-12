Arauna_CasaFogueira_Salao_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Fogueira_Salao_OnTransition
	.byte 0

@ Casa da Fogueira, S09-S13 -- DRAFT written from the synopsis
@ (docs/ARCOS_RASCUNHO.md). Story Night opens with the seventh badge; HORIZON
@ comes for the recordings and the circle holds; ARAUA answers from the fire;
@ after the League and the Noise Tower, the circle welcomes them back. The listening circle above (FOGUEIRA RODA V1) is unchanged.
@
@ VAR_ARAUNA_FOGUEIRA_STATE
@   0  not started                    2  HORIZON gone, ARAUA not yet seen
@   1  story told, HORIZON in the hall 3  ARAUA seen
@                                     4  welcomed back after the tower

Fogueira_Salao_OnTransition:
	setflag FLAG_ARAUNA_FOGUEIRA_HIDE_HORIZON
	call_if_eq VAR_ARAUNA_FOGUEIRA_STATE, 1, Fogueira_Salao_ShowHorizon
	end

Fogueira_Salao_ShowHorizon:
	clearflag FLAG_ARAUNA_FOGUEIRA_HIDE_HORIZON
	return

Arauna_CasaFogueira_Salao_EventScript_Hearth::
	goto_if_set FLAG_ARAUNA_FOGUEIRA_SHARED, Arauna_CasaFogueira_Salao_EventScript_HearthReturn
	msgbox Arauna_CasaFogueira_Salao_Text_Hearth, MSGBOX_SIGN
	end

Arauna_CasaFogueira_Salao_EventScript_HearthReturn::
	msgbox Arauna_CasaFogueira_Salao_Text_HearthReturn, MSGBOX_SIGN
	end

Arauna_CasaFogueira_Salao_EventScript_Gathering::
	msgbox Arauna_CasaFogueira_Salao_Text_Gathering, MSGBOX_SIGN
	end

Arauna_CasaFogueira_Salao_EventScript_Voices::
	lockall
	faceplayer
	msgbox Fogueira_Text_ChooseCircle, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Fogueira_ListeningCircle
	goto_if_ge VAR_ARAUNA_FOGUEIRA_STATE, 1, Fogueira_Keeper_Arc
	goto_if_set FLAG_BADGE07_GET, Fogueira_StoryNight
	msgbox Fogueira_Text_StorySoon, MSGBOX_DEFAULT
	releaseall
	end
Fogueira_ListeningCircle:
	goto_if_set FLAG_ARAUNA_FOGUEIRA_SHARED, Arauna_CasaFogueira_Salao_EventScript_CircleReturn
	goto_if_set FLAG_ARAUNA_FOGUEIRA_LISTENED, Arauna_CasaFogueira_Salao_EventScript_OfferLetter
	msgbox Arauna_CasaFogueira_Salao_Text_ListenOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Arauna_CasaFogueira_Salao_EventScript_Deferred
	msgbox Arauna_CasaFogueira_Salao_Text_Listening, MSGBOX_DEFAULT
	setflag FLAG_ARAUNA_FOGUEIRA_LISTENED
	releaseall
	end

Arauna_CasaFogueira_Salao_EventScript_OfferLetter::
	goto_if_unset FLAG_ARAUNA_FOGUEIRA_MEMORIAL_READ, Arauna_CasaFogueira_Salao_EventScript_MemorialInvitation
	msgbox Arauna_CasaFogueira_Salao_Text_ShareOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Arauna_CasaFogueira_Salao_EventScript_Deferred
	msgbox Arauna_CasaFogueira_Salao_Text_Sharing, MSGBOX_DEFAULT
	setflag FLAG_ARAUNA_FOGUEIRA_SHARED
	releaseall
	end

Arauna_CasaFogueira_Salao_EventScript_MemorialInvitation::
	msgbox Arauna_CasaFogueira_Salao_Text_MemorialInvitation, MSGBOX_DEFAULT
	releaseall
	end

Arauna_CasaFogueira_Salao_EventScript_Deferred::
	msgbox Arauna_CasaFogueira_Salao_Text_Deferred, MSGBOX_DEFAULT
	releaseall
	end

Arauna_CasaFogueira_Salao_EventScript_CircleReturn::
	msgbox Arauna_CasaFogueira_Salao_Text_CircleReturn, MSGBOX_DEFAULT
	releaseall
	end

Arauna_CasaFogueira_Salao_EventScript_Bench::
	lockall
	faceplayer
	goto_if_ge VAR_ARAUNA_FOGUEIRA_STATE, 3, Fogueira_Bench_AfterNight
	goto_if_set FLAG_ARAUNA_FOGUEIRA_SHARED, Arauna_CasaFogueira_Salao_EventScript_BenchReturn
	msgbox Arauna_CasaFogueira_Salao_Text_Bench, MSGBOX_DEFAULT
	releaseall
	end

Arauna_CasaFogueira_Salao_EventScript_BenchReturn::
	msgbox Arauna_CasaFogueira_Salao_Text_BenchReturn, MSGBOX_DEFAULT
	releaseall
	end

Arauna_CasaFogueira_Salao_Text_Hearth:
	.string "Warm embers glow among the stones.$"

Arauna_CasaFogueira_Salao_Text_HearthReturn:
	.string "The same embers. A new memory.$"

Arauna_CasaFogueira_Salao_Text_Gathering:
	.string "A flame is shared by everyone.\n"
	.string "No voice has to speak alone.$"

Arauna_CasaFogueira_Salao_Text_ListenOffer:
	.string "We take turns by the fire.\n"
	.string "Silence has a place here too.\p"
	.string "Would you like to listen?$"

Arauna_CasaFogueira_Salao_Text_Listening:
	.string "A neighbor speaks softly.\n"
	.string "The circle gives them time.\p"
	.string "I used to rush home before dark.\n"
	.string "Someone was waiting at the door.\p"
	.string "Now I walk slowly past the trees.\n"
	.string "I remember how we planted them.\p"
	.string "The keeper lets the silence stay.\n"
	.string "Thank you for listening.$"

Arauna_CasaFogueira_Salao_Text_MemorialInvitation:
	.string "The memorial keeps other voices.\n"
	.string "Read them whenever you are ready.\p"
	.string "You are welcome to stay here too.$"

Arauna_CasaFogueira_Salao_Text_ShareOffer:
	.string "That unsigned letter was left\n"
	.string "for anyone willing to read it.\p"
	.string "Would you read it to the circle?$"

Arauna_CasaFogueira_Salao_Text_Sharing:
	.string "You read the letter by the fire.\n"
	.string "Nobody interrupts.\p"
	.string "A place can hold a name\n"
	.string "when a voice cannot say it yet.\p"
	.string "The keeper turns to the circle.\n"
	.string "We can hold that place together.\p"
	.string "The fire settles. You sit with\n"
	.string "them for a quiet moment.$"

Arauna_CasaFogueira_Salao_Text_Deferred:
	.string "Of course. You can just be here.\n"
	.string "Come and go as you need.$"

Arauna_CasaFogueira_Salao_Text_CircleReturn:
	.string "We remember the letter you read.\n"
	.string "You can listen with us again.\p"
	.string "Your silence is welcome too.$"

Arauna_CasaFogueira_Salao_Text_Bench:
	.string "Some come to speak. Some to rest.\n"
	.string "I like hearing the fire crackle.$"

Arauna_CasaFogueira_Salao_Text_BenchReturn:
	.string "I heard that letter differently\n"
	.string "when you read it here. Thank you.$"

Arauna_CasaFogueira_Salao_EventScript_Planter::
	lockall
	faceplayer
	goto_if_ge VAR_ARAUNA_FOGUEIRA_STATE, 3, Fogueira_Planter_AfterNight
	goto_if_set FLAG_ARAUNA_FOGUEIRA_SHARED, Arauna_CasaFogueira_Salao_EventScript_PlanterReturn
	msgbox Arauna_CasaFogueira_Salao_Text_Planter, MSGBOX_DEFAULT
	releaseall
	end

Arauna_CasaFogueira_Salao_EventScript_PlanterReturn::
	msgbox Arauna_CasaFogueira_Salao_Text_PlanterReturn, MSGBOX_DEFAULT
	releaseall
	end

Arauna_CasaFogueira_Salao_Text_Planter:
	.string "Those trees took years to grow.\n"
	.string "We cared for them together.$"

Arauna_CasaFogueira_Salao_Text_PlanterReturn:
	.string "The trees still need tending.\n"
	.string "I think I will go tomorrow.$"

Arauna_CasaFogueira_Salao_EventScript_Neighbor::
	lockall
	faceplayer
	goto_if_set FLAG_ARAUNA_FOGUEIRA_SHARED, Arauna_CasaFogueira_Salao_EventScript_NeighborReturn
	msgbox Arauna_CasaFogueira_Salao_Text_Neighbor, MSGBOX_DEFAULT
	releaseall
	end

Arauna_CasaFogueira_Salao_EventScript_NeighborReturn::
	msgbox Arauna_CasaFogueira_Salao_Text_NeighborReturn, MSGBOX_DEFAULT
	releaseall
	end

Arauna_CasaFogueira_Salao_Text_Neighbor:
	.string "There is no order we must follow.\n"
	.string "The keeper waits for us.$"

Arauna_CasaFogueira_Salao_Text_NeighborReturn:
	.string "Thank you for giving us time.\n"
	.string "That matters more than advice.$"

Arauna_CasaFogueira_Salao_EventScript_Boy::
	lockall
	faceplayer
	goto_if_set FLAG_ARAUNA_FOGUEIRA_SHARED, Arauna_CasaFogueira_Salao_EventScript_BoyReturn
	msgbox Arauna_CasaFogueira_Salao_Text_Boy, MSGBOX_DEFAULT
	releaseall
	end

Arauna_CasaFogueira_Salao_EventScript_BoyReturn::
	msgbox Arauna_CasaFogueira_Salao_Text_BoyReturn, MSGBOX_DEFAULT
	releaseall
	end

Arauna_CasaFogueira_Salao_Text_Boy:
	.string "I saved this place for my friend.\n"
	.string "They can come whenever they like.$"

Arauna_CasaFogueira_Salao_Text_BoyReturn:
	.string "A place can hold a name...\n"
	.string "I will remember that.$"

Arauna_CasaFogueira_Salao_EventScript_Girl::
	lockall
	faceplayer
	goto_if_ge VAR_ARAUNA_FOGUEIRA_STATE, 3, Fogueira_Girl_AfterNight
	goto_if_set FLAG_ARAUNA_FOGUEIRA_SHARED, Arauna_CasaFogueira_Salao_EventScript_GirlReturn
	msgbox Arauna_CasaFogueira_Salao_Text_Girl, MSGBOX_DEFAULT
	releaseall
	end

Arauna_CasaFogueira_Salao_EventScript_GirlReturn::
	msgbox Arauna_CasaFogueira_Salao_Text_GirlReturn, MSGBOX_DEFAULT
	releaseall
	end

Arauna_CasaFogueira_Salao_Text_Girl:
	.string "Do I have to tell a story?\n"
	.string "They said listening counts too.$"

Arauna_CasaFogueira_Salao_Text_GirlReturn:
	.string "I think I will listen today.\n"
	.string "Maybe next time I will speak.$"

@ ------------------------------------------------- S09 Story Night

Fogueira_StoryNight:
	msgbox Fogueira_Text_StoryNightInvite, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Arauna_CasaFogueira_Salao_EventScript_Deferred
	message Fogueira_Text_WhichStory
	waitmessage
	multichoice 16, 6, MULTI_ARAUNA_STORY_NIGHT, TRUE
	switch VAR_RESULT
	case 0, Fogueira_TellHowl
	case 1, Fogueira_TellTie
	goto Fogueira_TellRoad

Fogueira_TellHowl:
	goto_if_ge VAR_ARAUNA_UIVO_STATE, 8, Fogueira_TellHowlLived
	msgbox Fogueira_Text_TellHowlHeard, MSGBOX_DEFAULT
	goto Fogueira_StoryTold

Fogueira_TellHowlLived:
	msgbox Fogueira_Text_TellHowlLived, MSGBOX_DEFAULT
	goto Fogueira_StoryTold

Fogueira_TellTie:
	goto_if_set FLAG_ARAUNA_FIRST_LINK_MADE, Fogueira_TellTieLinked
	msgbox Fogueira_Text_TellTieHeard, MSGBOX_DEFAULT
	goto Fogueira_StoryTold

Fogueira_TellTieLinked:
	msgbox Fogueira_Text_TellTieLinked, MSGBOX_DEFAULT
	goto Fogueira_StoryTold

Fogueira_TellRoad:
	msgbox Fogueira_Text_TellRoad, MSGBOX_DEFAULT
Fogueira_StoryTold:
	msgbox Fogueira_Text_CircleKeepsIt, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_FOGUEIRA_STATE, 1
	closemessage
	goto Fogueira_HorizonArrives

@ ------------------------------------------------- S10 HORIZON at the door

Fogueira_HorizonArrives:
	playse SE_DOOR
	fadescreen FADE_TO_BLACK
	clearflag FLAG_ARAUNA_FOGUEIRA_HIDE_HORIZON
	addobject LOCALID_FOGUEIRA_AGENT_1
	addobject LOCALID_FOGUEIRA_BRENO
	addobject LOCALID_FOGUEIRA_AGENT_2
	fadescreen FADE_FROM_BLACK
	applymovement LOCALID_PLAYER, Common_Movement_FaceRight
	waitmovement 0
	msgbox Fogueira_Text_BrenoArrives, MSGBOX_DEFAULT
	msgbox Fogueira_Text_KeeperRefuses, MSGBOX_DEFAULT
	msgbox Fogueira_Text_BrenoOrders, MSGBOX_DEFAULT
	goto Fogueira_Defense

@ ------------------------------------------------- S11 the circle holds

Fogueira_Defense:
	msgbox Fogueira_Text_CircleStands, MSGBOX_DEFAULT
	goto_if_defeated TRAINER_ARAUNA_FOGUEIRA_AGENT_1, Fogueira_DefenseSecond
	trainerbattle_no_intro TRAINER_ARAUNA_FOGUEIRA_AGENT_1, Fogueira_Text_Agent1Defeat
Fogueira_DefenseSecond:
	msgbox Fogueira_Text_CircleHolds, MSGBOX_DEFAULT
	goto_if_defeated TRAINER_ARAUNA_FOGUEIRA_AGENT_2, Fogueira_DefenseBreno
	trainerbattle_no_intro TRAINER_ARAUNA_FOGUEIRA_AGENT_2, Fogueira_Text_Agent2Defeat
Fogueira_DefenseBreno:
	msgbox Fogueira_Text_BrenoStepsIn, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_ARAUNA_FOGUEIRA_ADMIN, Fogueira_Text_BrenoDefeat
	msgbox Fogueira_Text_BrenoWithdraws, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_FOGUEIRA_AGENT_1
	removeobject LOCALID_FOGUEIRA_BRENO
	removeobject LOCALID_FOGUEIRA_AGENT_2
	setflag FLAG_ARAUNA_FOGUEIRA_HIDE_HORIZON
	playse SE_DOOR
	fadescreen FADE_FROM_BLACK
	setvar VAR_ARAUNA_FOGUEIRA_STATE, 2
	goto Fogueira_Araua

@ ------------------------------------------------- S12 ARAUA in the fire

Fogueira_Araua:
	msgbox Fogueira_Text_FireRises, MSGBOX_DEFAULT
	closemessage
	playse SE_M_SACRED_FIRE
	fadescreenspeed FADE_TO_WHITE, 6
	playmoncry SPECIES_DEOXYS, CRY_MODE_NORMAL
	waitmoncry
	fadescreenspeed FADE_FROM_WHITE, 6
	msgbox Fogueira_Text_ArauaSeen, MSGBOX_DEFAULT
	msgbox Fogueira_Text_KeeperOnAraua, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_FOGUEIRA_STATE, 3
	releaseall
	end

@ ------------------------------------------------- the keeper afterwards, S13

Fogueira_Keeper_Arc:
	goto_if_eq VAR_ARAUNA_FOGUEIRA_STATE, 1, Fogueira_Keeper_StillHere
	goto_if_eq VAR_ARAUNA_FOGUEIRA_STATE, 2, Fogueira_Araua
	goto_if_eq VAR_ARAUNA_FOGUEIRA_STATE, 3, Fogueira_Keeper_Waiting
	goto_if_unset FLAG_SYS_GAME_CLEAR, Fogueira_Keeper_AfterReturn
	goto_if_unset FLAG_ARAUNA_TOWER_COMPLETE, Fogueira_Keeper_AfterReturn
	call_if_unset FLAG_ARAUNA_ARAUA_AWAKENED, Fogueira_FirstLegend
Fogueira_Keeper_AfterReturn:
	msgbox Fogueira_Text_KeeperAfterReturn, MSGBOX_DEFAULT
	releaseall
	end

Fogueira_Keeper_StillHere:
	msgbox Fogueira_Text_KeeperStillHere, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Fogueira_Defense
	msgbox Fogueira_Text_KeeperWeHold, MSGBOX_DEFAULT
	releaseall
	end

Fogueira_Keeper_Waiting:
	goto_if_unset FLAG_SYS_GAME_CLEAR, Fogueira_Keeper_WaitingText
	goto_if_set FLAG_ARAUNA_TOWER_COMPLETE, Fogueira_Return
Fogueira_Keeper_WaitingText:
	msgbox Fogueira_Text_KeeperWaiting, MSGBOX_DEFAULT
	releaseall
	end

Fogueira_Return:
	call_if_unset FLAG_ARAUNA_ARAUA_AWAKENED, Fogueira_FirstLegend
	msgbox Fogueira_Text_Return, MSGBOX_DEFAULT
	giveitem ITEM_SACRED_ASH
	goto_if_eq VAR_RESULT, FALSE, Fogueira_ReturnBagFull
	setvar VAR_ARAUNA_FOGUEIRA_STATE, 4
	msgbox Fogueira_Text_ReturnAsh, MSGBOX_DEFAULT
	releaseall
	end

Fogueira_ReturnBagFull:
	msgbox gText_TooBadBagIsFull, MSGBOX_DEFAULT
	releaseall
	end

Fogueira_EventScript_Breno::
	msgbox Fogueira_Text_BrenoWaits, MSGBOX_NPC
	end

Fogueira_EventScript_Agent::
	msgbox Fogueira_Text_AgentRecords, MSGBOX_NPC
	end

Fogueira_Bench_AfterNight:
	msgbox Fogueira_Text_BenchAfterNight, MSGBOX_DEFAULT
	releaseall
	end

Fogueira_Planter_AfterNight:
	msgbox Fogueira_Text_PlanterAfterNight, MSGBOX_DEFAULT
	releaseall
	end

Fogueira_Girl_AfterNight:
	msgbox Fogueira_Text_GirlAfterNight, MSGBOX_DEFAULT
	releaseall
	end

Fogueira_Text_StoryNightInvite:
	.string "You've come a long way since you\n"
	.string "first sat with us.\p"
	.string "Tonight is Story Night. Every voice\n"
	.string "in the circle may tell one story.\p"
	.string "Will you tell one?$"

Fogueira_Text_WhichStory:
	.string "Which story will you tell?$"

Fogueira_Text_TellHowlLived:
	.string "You tell of a howl on the ridge,\n"
	.string "a lost pup and a folded cloth.\p"
	.string "You tell how the Hermit wrote it\n"
	.string "down, and how the ridge signed it.\p"
	.string "When you say “Answer it,” half\n"
	.string "the circle says it with you.$"

Fogueira_Text_TellHowlHeard:
	.string "You tell of a howl you heard on\n"
	.string "a mountain ridge, far from here.\p"
	.string "You never learned whose it was.\n"
	.string "The circle listens all the same.$"

Fogueira_Text_TellTieLinked:
	.string "You tell of a broken tie in a\n"
	.string "chamber under the mist.\p"
	.string "You tell them the name you spoke\n"
	.string "there, and why you chose it.\p"
	.string "Your first link shifts beside\n"
	.string "you as if it understood.$"

Fogueira_Text_TellTieHeard:
	.string "You tell of a broken tie in a\n"
	.string "chamber under the mist.\p"
	.string "One name is carved there: AUGUSTO.\n"
	.string "Nobody here knew him.\p"
	.string "The keeper repeats the name,\n"
	.string "so the fire hears it too.$"

Fogueira_Text_TellRoad:
	.string "You tell your own road: the town\n"
	.string "where it began, the GYMS, the\l"
	.string "people who stopped to talk.\p"
	.string "It isn't finished.\n"
	.string "Nobody asks you to finish it.$"

Fogueira_Text_CircleKeepsIt:
	.string "KEEPER: The circle keeps it now,\n"
	.string "and you keep it too.\p"
	.string "That's the only way a story can\n"
	.string "be kept.$"

Fogueira_Text_BrenoArrives:
	.string "BRENO: HORIZON. Nobody move.\p"
	.string "We're here for the recordings.\n"
	.string "Everything said at this fire\l"
	.string "goes to the LIVING ARCHIVE.\p"
	.string "There it's safe. Nothing in there\n"
	.string "is ever forgotten.$"

Fogueira_Text_KeeperRefuses:
	.string "KEEPER: Nobody here agreed to that.$"

Fogueira_Text_BrenoOrders:
	.string "BRENO: Agreement is a formality.\n"
	.string "Agents, start recording.$"

Fogueira_Text_CircleStands:
	.string "Around the fire, people stand up\n"
	.string "one by one.\p"
	.string "Nobody steps back.\n"
	.string "You step forward with them.$"

Fogueira_Text_Agent1Defeat:
	.string "My recorder caught nothing but\n"
	.string "people singing over me!$"

Fogueira_Text_CircleHolds:
	.string "The planter and the neighbor stand\n"
	.string "in front of the memorial door.\p"
	.string "The children hum, loud enough that\n"
	.string "no recorder can pick out a word.$"

Fogueira_Text_Agent2Defeat:
	.string "This room won't stay quiet long\n"
	.string "enough to archive...$"

Fogueira_Text_BrenoStepsIn:
	.string "BRENO: Fine. I'll do it myself.$"

Fogueira_Text_BrenoDefeat:
	.string "You can't archive a room\n"
	.string "that won't stop talking.$"

Fogueira_Text_BrenoWithdraws:
	.string "BRENO: Pack it up. We're done here.\p"
	.string "Remember this when you find out\n"
	.string "what forgetting costs.$"

Fogueira_Text_FireRises:
	.string "The door bangs shut behind them.\p"
	.string "Then the fire roars up to the\n"
	.string "roof beams!$"

Fogueira_Text_ArauaSeen:
	.string "For a moment a shape stands in the\n"
	.string "flames, with wings of sparks.\p"
	.string "It looks at every face in the\n"
	.string "circle, yours last.\p"
	.string "Then it's only a fire again.$"

Fogueira_Text_KeeperOnAraua:
	.string "KEEPER: Wings in an ember.\p"
	.string "My grandmother said it comes when\n"
	.string "a circle refuses to be silenced.\p"
	.string "I always thought that was\n"
	.string "just a story.$"

Fogueira_Text_KeeperStillHere:
	.string "KEEPER: They're still here, with\n"
	.string "their recorders on.\p"
	.string "Will you stand with the circle?$"

Fogueira_Text_KeeperWeHold:
	.string "KEEPER: Then we'll hold as long as\n"
	.string "we can. Come back to us.$"

Fogueira_Text_KeeperWaiting:
	.string "KEEPER: Go on. The circle will be\n"
	.string "here when the long road is done.$"

Fogueira_Text_Return:
	.string "KEEPER: You came back.\p"
	.string "The NOISE TOWER has fallen silent.\n"
	.string "Its records are with their people.\p"
	.string "The circle saved your place.\n"
	.string "And this is for you.$"

Fogueira_Text_ReturnAsh:
	.string "Ash from the night the fire stood\n"
	.string "up for us.\p"
	.string "They say it wakes those who have\n"
	.string "fallen. Use it for someone you\l"
	.string "won't let be forgotten.\p"
	.string "And if that shape in the fire ever\n"
	.string "calls you, follow it.$"

Fogueira_Text_KeeperAfterReturn:
	.string "KEEPER: Sit a while. There's always\n"
	.string "a new story, and an old one.$"

Fogueira_Text_BrenoWaits:
	.string "BRENO: Go on, make your speech.\n"
	.string "It'll be on file by morning.$"

Fogueira_Text_AgentRecords:
	.string "The agent keeps a recorder pointed\n"
	.string "at the fire.$"

Fogueira_Text_BenchAfterNight:
	.string "My hands were shaking the whole\n"
	.string "time. But nobody left the circle.$"

Fogueira_Text_PlanterAfterNight:
	.string "They wanted to keep our stories\n"
	.string "safe. In a box. Without us.$"

Fogueira_Text_GirlAfterNight:
	.string "I didn't tell a story, but I hummed\n"
	.string "so loud their recorder broke!$"


Fogueira_Text_ChooseCircle:
	.string "Join the listening circle?\p"
	.string "Choose NO to ask about Story Night\n"
	.string "or the road beyond the League.$"

Fogueira_Text_StorySoon:
	.string "KEEPER: Story Night will come.\n"
	.string "You can rest here until then.$"

@ Act 32: the final telling occurs after the League and the Noise Tower.
Fogueira_FirstLegend:
	msgbox Fogueira_Text_FirstLegend, MSGBOX_DEFAULT
	call_if_ge VAR_ARAUNA_UIVO_STATE, 8, Fogueira_FirstLegend_Howl
	call_if_set FLAG_ARAUNA_FIRST_LINK_MADE, Fogueira_FirstLegend_Link
	closemessage
	playse SE_M_SACRED_FIRE
	fadescreenspeed FADE_TO_WHITE, 6
	playmoncry SPECIES_DEOXYS, CRY_MODE_NORMAL
	waitmoncry
	fadescreenspeed FADE_FROM_WHITE, 6
	msgbox Fogueira_Text_FirstLegendAwake, MSGBOX_DEFAULT
	setflag FLAG_ARAUNA_ARAUA_AWAKENED
	return
Fogueira_FirstLegend_Howl:
	msgbox Fogueira_Text_FirstLegendHowl, MSGBOX_DEFAULT
	return
Fogueira_FirstLegend_Link:
	msgbox Fogueira_Text_FirstLegendLink, MSGBOX_DEFAULT
	return
Fogueira_Text_FirstLegend:
	.string "The tower is quiet. Stories still\n"
	.string "need people to carry them.\p"
	.string "You tell of the League and of\n"
	.string "the records given back.\p"
	.string "KEEPER: The first legend is not\n"
	.string "the oldest. It is the next one\l"
	.string "we agree to carry together.$"
Fogueira_Text_FirstLegendHowl:
	.string "You tell of a pup and a cloth,\n"
	.string "and a room that learned to wait.$"
Fogueira_Text_FirstLegendLink:
	.string "You tell of the companion you chose\n"
	.string "in the chamber under the mist.$"
Fogueira_Text_FirstLegendAwake:
	.string "The last page catches the firelight.\n"
	.string "ARAUA opens its wings.\p"
	.string "It stays long enough to hear\n"
	.string "each voice, and every silence.$"
