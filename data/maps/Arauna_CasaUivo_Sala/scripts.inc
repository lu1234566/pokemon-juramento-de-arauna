Arauna_CasaUivo_Sala_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CasaUivo_Sala_OnTransition
	.byte 0

@ Casa do Uivo, U03-U11 -- DRAFT written from the synopsis
@ (docs/ARCOS_RASCUNHO.md). The Hermit speaks through his notebook: every line
@ of his is written and turned toward the room. Nothing here stands in for
@ Libras; the signed scene still waits for its qualified translation.
@
@ VAR_ARAUNA_UIVO_STATE
@   0  not started          5  pup calmed (or caught), the ridge gathers
@   1  consent given        6  the Hermit retold it
@   2  notebooks asked      7  the record is signed
@   3  notebooks in order   8  HOWL SEAL given
@   4  cloth taken

CasaUivo_Sala_OnTransition:
	setvar VAR_OBJ_GFX_ID_E, ARAUNA_VIRTUAL_GFX_HERMIT
	setflag FLAG_ARAUNA_UIVO_HIDE_NEIGHBOR
	setflag FLAG_ARAUNA_UIVO_HIDE_CIRCLE
	call_if_ge VAR_ARAUNA_UIVO_STATE, 5, CasaUivo_Sala_ShowCircle
	end

CasaUivo_Sala_ShowCircle:
	clearflag FLAG_ARAUNA_UIVO_HIDE_NEIGHBOR
	clearflag FLAG_ARAUNA_UIVO_HIDE_CIRCLE
	setobjectxyperm LOCALID_CASA_UIVO_NEIGHBOR, 5, 7
	setobjectmovementtype LOCALID_CASA_UIVO_NEIGHBOR, MOVEMENT_TYPE_FACE_RIGHT
	return

CasaUivo_EventScript_Welcome::
	msgbox CasaUivo_Text_Welcome, MSGBOX_SIGN
	end

CasaUivo_Text_Welcome:
	.string "Take a seat where everyone\n"
	.string "can see one another.$"

CasaUivo_EventScript_Books::
	lockall
	msgbox CasaUivo_Text_Books, MSGBOX_DEFAULT
	goto_if_lt VAR_ARAUNA_UIVO_STATE, 7, CasaUivo_EventScript_ReleaseAll
	msgbox CasaUivo_Text_BooksSigned, MSGBOX_DEFAULT
	releaseall
	end

CasaUivo_EventScript_ReleaseAll:
	releaseall
	end

CasaUivo_Text_Books:
	.string "Stories are kept here in\n"
	.string "notebooks and drawings.\p"
	.string "Their authors are named\n"
	.string "beside each record.$"

CasaUivo_Text_BooksSigned:
	.string "The newest record tells of a pup\n"
	.string "lost in the fog.\p"
	.string "Your name is under the Hermit's,\n"
	.string "and his under his mother's.$"

CasaUivo_EventScript_Drawings::
	msgbox CasaUivo_Text_Drawings, MSGBOX_SIGN
	end

CasaUivo_Text_Drawings:
	.string "Drawings show where people sit\n"
	.string "and how they share the room.\p"
	.string "No one should be hidden\n"
	.string "behind another person.$"

@ ---------------------------------------------------------------- the Hermit

CasaUivo_EventScript_Hermit::
	lock
	faceplayer
	switch VAR_ARAUNA_UIVO_STATE
	case 0, CasaUivo_Hermit_Start
	case 1, CasaUivo_Hermit_Account
	case 2, CasaUivo_Hermit_Notebooks
	case 3, CasaUivo_Hermit_Cloth
	case 4, CasaUivo_Hermit_GoGently
	case 5, CasaUivo_Hermit_Retelling
	case 6, CasaUivo_Hermit_Record
	case 7, CasaUivo_Hermit_Seal
	goto CasaUivo_Hermit_ReplayOffer

CasaUivo_Hermit_After:
	msgbox CasaUivo_Text_HermitAfter, MSGBOX_DEFAULT
	release
	end

@ U03 -- consent. Before the second badge the visit stays as it was.
CasaUivo_Hermit_Start:
	msgbox CasaUivo_Text_Hermit, MSGBOX_DEFAULT
	goto_if_unset FLAG_BADGE02_GET, CasaUivo_EventScript_Release
	msgbox CasaUivo_Text_HermitAsks, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CasaUivo_Hermit_Declined
	setvar VAR_ARAUNA_UIVO_STATE, 1
	goto CasaUivo_Hermit_Account

CasaUivo_Hermit_Declined:
	msgbox CasaUivo_Text_HermitDeclined, MSGBOX_DEFAULT
	release
	end

CasaUivo_EventScript_Release:
	release
	end

@ U04 -- his written account, and the ridge comes through the door.
CasaUivo_Hermit_Account:
	msgbox CasaUivo_Text_HermitAccount, MSGBOX_DEFAULT
	closemessage
	playse SE_EXIT
	clearflag FLAG_ARAUNA_UIVO_HIDE_NEIGHBOR
	addobject LOCALID_CASA_UIVO_NEIGHBOR
	applymovement LOCALID_CASA_UIVO_NEIGHBOR, CasaUivo_Movement_NeighborComesIn
	waitmovement 0
	applymovement LOCALID_PLAYER, Common_Movement_FaceDown
	waitmovement 0
	msgbox CasaUivo_Text_NeighborBurstsIn, MSGBOX_DEFAULT
	applymovement LOCALID_CASA_UIVO_CHILD, Common_Movement_FaceLeft
	waitmovement 0
	msgbox CasaUivo_Text_ChildObjects, MSGBOX_DEFAULT
	applymovement LOCALID_PLAYER, Common_Movement_FaceUp
	waitmovement 0
	msgbox CasaUivo_Text_HermitAsksHelp, MSGBOX_DEFAULT
	msgbox CasaUivo_Text_NeighborWaits, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CASA_UIVO_NEIGHBOR, CasaUivo_Movement_NeighborGoesOut
	waitmovement 0
	removeobject LOCALID_CASA_UIVO_NEIGHBOR
	setvar VAR_ARAUNA_UIVO_STATE, 2
	release
	end

CasaUivo_Hermit_Notebooks:
	msgbox CasaUivo_Text_HermitNotebooks, MSGBOX_DEFAULT
	release
	end

CasaUivo_Hermit_Cloth:
	msgbox CasaUivo_Text_HermitCloth, MSGBOX_DEFAULT
	release
	end

CasaUivo_Hermit_GoGently:
	msgbox CasaUivo_Text_HermitGoGently, MSGBOX_DEFAULT
	release
	end

@ U08-U09 -- the Hermit leads the retelling; the player is in the circle,
@ not at its center.
CasaUivo_Hermit_Retelling:
	msgbox CasaUivo_Text_RoomIsFull, MSGBOX_DEFAULT
	goto_if_set FLAG_ARAUNA_UIVO_PUP_CAUGHT, CasaUivo_Hermit_RetellingCaught
	msgbox CasaUivo_Text_RetellingHome, MSGBOX_DEFAULT
	goto CasaUivo_Hermit_RetellingDone

CasaUivo_Hermit_RetellingCaught:
	msgbox CasaUivo_Text_RetellingTravels, MSGBOX_DEFAULT
CasaUivo_Hermit_RetellingDone:
	msgbox CasaUivo_Text_CircleAnswers, MSGBOX_DEFAULT
	setvar VAR_ARAUNA_UIVO_STATE, 6
	goto CasaUivo_Hermit_Record

@ U10 -- the record and the public commitment. Saying no is a whole answer.
CasaUivo_Hermit_Record:
	msgbox CasaUivo_Text_HermitAsksToSign, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CasaUivo_Hermit_NotSigning
	goto CasaUivo_Hermit_AccessChoice

CasaUivo_Hermit_RecordAccepted:
	setvar VAR_ARAUNA_UIVO_STATE, 7
	playse SE_EXP_MAX
	msgbox CasaUivo_Text_Signing, MSGBOX_DEFAULT
	goto CasaUivo_Hermit_Seal

CasaUivo_Hermit_NotSigning:
	msgbox CasaUivo_Text_HermitNoSign, MSGBOX_DEFAULT
	release
	end

@ U11 -- the HOWL SEAL, carved on a bell.
CasaUivo_Hermit_Seal:
	msgbox CasaUivo_Text_SealOffered, MSGBOX_DEFAULT
	giveitem ITEM_SOOTHE_BELL
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setvar VAR_ARAUNA_UIVO_STATE, 8
	msgbox CasaUivo_Text_SealExplained, MSGBOX_DEFAULT
	release
	end

CasaUivo_Movement_NeighborComesIn:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_in_place_faster_up
	step_end

CasaUivo_Movement_NeighborGoesOut:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

CasaUivo_Text_Hermit:
	.string "He turns a notebook toward you.\p"
	.string "“Please sit where we can see\n"
	.string "each other. Take your time.”$"

CasaUivo_Text_HermitAsks:
	.string "He turns the page and writes.\p"
	.string "“Something has been howling\n"
	.string "on the ridge at night.”\p"
	.string "“My mother once wrote about\n"
	.string "a howl like that.”\p"
	.string "“Would you read her story with\n"
	.string "me? You can say no.”$"

CasaUivo_Text_HermitDeclined:
	.string "He nods and closes the notebook.\p"
	.string "“Another day, then.\n"
	.string "The chair stays yours.”$"

CasaUivo_Text_HermitAccount:
	.string "He writes slowly, then holds the\n"
	.string "notebook up for you to read.\p"
	.string "“My mother lived on this ridge\n"
	.string "all her life.”\p"
	.string "“She wrote everything down, for\n"
	.string "me and for whoever came after.”\p"
	.string "“The GUARÁ families came down\n"
	.string "at dusk when I was small.”\p"
	.string "“She said a howl is not a threat.\n"
	.string "It is a question.”$"

CasaUivo_Text_NeighborBurstsIn:
	.string "A hiker hurries in, out of breath.\p"
	.string "“Sorry to barge in! It howled\n"
	.string "again, right above the houses.”\p"
	.string "“Nobody slept. Some of the miners\n"
	.string "want to chase it off with lamps\l"
	.string "and pans tonight.”$"

CasaUivo_Text_ChildObjects:
	.string "The girl by the drawings jumps up.\p"
	.string "“That will only scare it more!”$"

CasaUivo_Text_HermitAsksHelp:
	.string "The Hermit writes quickly and\n"
	.string "turns the page to the room.\p"
	.string "“Noise answers noise. My mother\n"
	.string "knew what to do.”\p"
	.string "“But her notebooks fell when the\n"
	.string "shelf broke. The pages are mixed.”\p"
	.string "“They are in the memory room, at\n"
	.string "the back. Would you sort them?”$"

CasaUivo_Text_NeighborWaits:
	.string "The hiker rubs his neck.\p"
	.string "“I'll ask the others to wait.\n"
	.string "But not for long.”$"

CasaUivo_Text_HermitNotebooks:
	.string "He points to the door at the back.\p"
	.string "“The memory room. Her notebooks\n"
	.string "are on the table.”$"

CasaUivo_Text_HermitCloth:
	.string "He reads the last page twice.\p"
	.string "“Her cloth is beside the notebooks.\n"
	.string "Please take it to the ridge.”$"

CasaUivo_Text_HermitGoGently:
	.string "“The howl comes from the rocks\n"
	.string "by the waterfall. Go gently.”$"

CasaUivo_Text_RoomIsFull:
	.string "The room is full. People from the\n"
	.string "ridge sit where all can see.\p"
	.string "The Hermit stands. He holds up his\n"
	.string "mother's notebooks, one by one,\l"
	.string "so the whole room can read them.\p"
	.string "Then he turns to a new page,\n"
	.string "written in his own hand.$"

CasaUivo_Text_RetellingHome:
	.string "You give the cloth back. He folds\n"
	.string "it beside the open notebooks.\p"
	.string "“Last night the howl was a pup\n"
	.string "lost in the fog.”\p"
	.string "“Tonight it is home. {PLAYER}\n"
	.string "answered it, the way she did.”$"

CasaUivo_Text_RetellingTravels:
	.string "“Last night the howl was a pup\n"
	.string "lost in the fog.”\p"
	.string "“Now it travels with {PLAYER},\n"
	.string "and her cloth goes with it.”$"

CasaUivo_Text_CircleAnswers:
	.string "The hiker clears his throat.\p"
	.string "“We were ready with the lamps.\n"
	.string "I'm glad we waited.”\p"
	.string "The girl holds up a drawing:\n"
	.string "a small orange pup on a cloth.$"

CasaUivo_Text_HermitAsksToSign:
	.string "The Hermit opens the record at\n"
	.string "the page with his mother's name.\p"
	.string "“The ridge should keep this story.\n"
	.string "Will you sign it with us?”$"

CasaUivo_Text_HermitNoSign:
	.string "“You don't have to.\n"
	.string "A story is shared, never taken.”$"

CasaUivo_Text_Signing:
	.string "You write your name under the\n"
	.string "Hermit's, below his mother's.\p"
	.string "One by one, the people of the\n"
	.string "ridge add theirs.\p"
	.string "The hiker signs last and looks\n"
	.string "around the room.\p"
	.string "“From now on, nobody on this ridge\n"
	.string "chases a howl. We answer it.”$"

CasaUivo_Text_SealOffered:
	.string "The Hermit presses a small bell\n"
	.string "into your hands.\p"
	.string "A howling GUARÁ is carved on the\n"
	.string "handle: the ridge's HOWL SEAL.$"

CasaUivo_Text_SealExplained:
	.string "He writes one more line.\p"
	.string "“For listening first.”$"

CasaUivo_Text_HermitAfter:
	.string "“The record is on the shelf now.\n"
	.string "Come and read it when you like.”$"

@ ---------------------------------------------------------------- the circle

CasaUivo_EventScript_Child::
	lock
	faceplayer
	goto_if_ge VAR_ARAUNA_UIVO_STATE, 5, CasaUivo_Child_Drawing
	msgbox CasaUivo_Text_Child, MSGBOX_DEFAULT
	release
	end

CasaUivo_Child_Drawing:
	msgbox CasaUivo_Text_ChildDrawing, MSGBOX_DEFAULT
	release
	end

CasaUivo_Text_Child:
	.string "“You can sit beside me.\n"
	.string "There is room for everyone.”$"

CasaUivo_Text_ChildDrawing:
	.string "“I'm drawing the pup for the wall.\n"
	.string "This one with the cloth is you!”$"

CasaUivo_EventScript_Neighbor::
	lock
	faceplayer
	goto_if_ge VAR_ARAUNA_UIVO_STATE, 7, CasaUivo_Neighbor_Signed
	msgbox CasaUivo_Text_Neighbor, MSGBOX_DEFAULT
	release
	end

CasaUivo_Neighbor_Signed:
	msgbox CasaUivo_Text_NeighborSigned, MSGBOX_DEFAULT
	release
	end

CasaUivo_Text_Neighbor:
	.string "“We had the lamps ready.\n"
	.string "Strange to think of it now.”$"

CasaUivo_Text_NeighborSigned:
	.string "“Next time it howls, I'll go up\n"
	.string "with a cloth, not a lamp.”$"

CasaUivo_EventScript_Weaver::
	msgbox CasaUivo_Text_Weaver, MSGBOX_NPC
	end

CasaUivo_Text_Weaver:
	.string "“I wove that cloth with her, years\n"
	.string "ago. I never thought it would be\l"
	.string "needed again.”$"

CasaUivo_EventScript_Miner::
	msgbox CasaUivo_Text_Miner, MSGBOX_NPC
	end

CasaUivo_Text_Miner:
	.string "“Down in the tunnels everything\n"
	.string "echoes twice.”\p"
	.string "“Up here we're learning to\n"
	.string "listen once.”$"


@ Production fallback: replay the written account, never pretend it is Libras.
CasaUivo_Hermit_ReplayOffer:
	msgbox CasaUivo_Text_ReplayOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CasaUivo_Hermit_After
	msgbox CasaUivo_Text_HermitAccount, MSGBOX_DEFAULT
	msgbox CasaUivo_Text_RoomIsFull, MSGBOX_DEFAULT
	goto_if_set FLAG_ARAUNA_UIVO_PUP_CAUGHT, CasaUivo_Hermit_ReplayCaught
	msgbox CasaUivo_Text_RetellingHome, MSGBOX_DEFAULT
	goto CasaUivo_Hermit_ReplayEnd
CasaUivo_Hermit_ReplayCaught:
	msgbox CasaUivo_Text_RetellingTravels, MSGBOX_DEFAULT
CasaUivo_Hermit_ReplayEnd:
	msgbox CasaUivo_Text_CircleAnswers, MSGBOX_DEFAULT
	release
	end
CasaUivo_Text_ReplayOffer:
	.string "Read his written account again?\n"
	.string "The mission will not repeat.$"

CasaUivo_Hermit_AccessChoice:
	goto_if_ge VAR_ARAUNA_UIVO_ACCESS, 1, CasaUivo_Hermit_RecordAccepted
	msgbox CasaUivo_Text_InterpreterOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, CasaUivo_Access_Interpreter
	msgbox CasaUivo_Text_ClassesOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, CasaUivo_Access_Classes
	msgbox CasaUivo_Text_CouncilOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CasaUivo_Hermit_NotSigning
	setvar VAR_ARAUNA_UIVO_ACCESS, 3
	goto CasaUivo_Access_Chosen
CasaUivo_Access_Interpreter:
	setvar VAR_ARAUNA_UIVO_ACCESS, 1
	goto CasaUivo_Access_Chosen
CasaUivo_Access_Classes:
	setvar VAR_ARAUNA_UIVO_ACCESS, 2
CasaUivo_Access_Chosen:
	msgbox CasaUivo_Text_AccessChosen, MSGBOX_DEFAULT
	goto CasaUivo_Hermit_RecordAccepted
CasaUivo_Text_InterpreterOffer:
	.string "He writes: 'This room must change.'\p"
	.string "Fund a community interpreter?$"
CasaUivo_Text_ClassesOffer:
	.string "Start regular Libras classes\n"
	.string "for the community?$"
CasaUivo_Text_CouncilOffer:
	.string "Form a bilingual council with\n"
	.string "deaf residents leading it?$"
CasaUivo_Text_AccessChosen:
	.string "The village records the commitment.\p"
	.string "He writes: 'You will have to return.\n"
	.string "A promise needs people, not ink.'$"
