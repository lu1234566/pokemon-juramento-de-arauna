Arauna_CasaFogueira_Salao_MapScripts::
	.byte 0

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
