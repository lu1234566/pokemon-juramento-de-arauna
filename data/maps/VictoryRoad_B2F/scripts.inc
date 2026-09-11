VictoryRoad_B2F_MapScripts::
	.byte 0

VictoryRoad_B2F_EventScript_Vito::
	trainerbattle_single TRAINER_VITO, VictoryRoad_B2F_Text_VitoIntro, VictoryRoad_B2F_Text_VitoDefeat
	msgbox VictoryRoad_B2F_Text_VitoPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Owen::
	trainerbattle_single TRAINER_OWEN, VictoryRoad_B2F_Text_OwenIntro, VictoryRoad_B2F_Text_OwenDefeat
	msgbox VictoryRoad_B2F_Text_OwenPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Caroline::
	trainerbattle_single TRAINER_CAROLINE, VictoryRoad_B2F_Text_CarolineIntro, VictoryRoad_B2F_Text_CarolineDefeat
	msgbox VictoryRoad_B2F_Text_CarolinePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Julie::
	trainerbattle_single TRAINER_JULIE, VictoryRoad_B2F_Text_JulieIntro, VictoryRoad_B2F_Text_JulieDefeat
	msgbox VictoryRoad_B2F_Text_JuliePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Felix::
	trainerbattle_single TRAINER_FELIX, VictoryRoad_B2F_Text_FelixIntro, VictoryRoad_B2F_Text_FelixDefeat
	msgbox VictoryRoad_B2F_Text_FelixPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Dianne::
	trainerbattle_single TRAINER_DIANNE, VictoryRoad_B2F_Text_DianneIntro, VictoryRoad_B2F_Text_DianneDefeat
	msgbox VictoryRoad_B2F_Text_DiannePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_Text_VitoIntro:
	.string "I trained with my whole family. I'm not\n"
	.string "losing to anyone!$"

VictoryRoad_B2F_Text_VitoDefeat:
	.string "Better than my whole family?! Is that\n"
	.string "even possible?!$"

VictoryRoad_B2F_Text_VitoPostBattle:
	.string "I was the best in my family and I had\n"
	.string "never lost...\p"
	.string "I think I've lost my nerve. Maybe I'll go\n"
	.string "home.$"

VictoryRoad_B2F_Text_OwenIntro:
	.string "I heard about some tough young\n"
	.string "TRAINER. So that was you?$"

VictoryRoad_B2F_Text_OwenDefeat:
	.string "The little one is strong!$"

VictoryRoad_B2F_Text_OwenPostBattle:
	.string "So the rumors were true. That strong\n"
	.string "young TRAINER came from\l"
	.string "VILA AMANHECER.$"

VictoryRoad_B2F_Text_CarolineIntro:
	.string "You must be getting tired.$"

VictoryRoad_B2F_Text_CarolineDefeat:
	.string "Not a sign of tiredness!$"

VictoryRoad_B2F_Text_CarolinePostBattle:
	.string "ESTRADA DO JURAMENTO and the LEAGUE\n"
	.string "are both long challenges.\p"
	.string "Do not let tiredness win.$"

VictoryRoad_B2F_Text_JulieIntro:
	.string "Don't get comfortable just because\n"
	.string "you've won a lot of BADGES.\p"
	.string "There's always someone better.$"

VictoryRoad_B2F_Text_JulieDefeat:
	.string "You're better than me!$"

VictoryRoad_B2F_Text_JuliePostBattle:
	.string "Look at your BADGES and remember the\n"
	.string "TRAINERS you beat.$"

VictoryRoad_B2F_Text_FelixIntro:
	.string "I got a long way, but the tension is\n"
	.string "going straight to my stomach...$"

VictoryRoad_B2F_Text_FelixDefeat:
	.string "Ow... That hurts...$"

VictoryRoad_B2F_Text_FelixPostBattle:
	.string "Just thinking about how close the\n"
	.string "LEAGUE is makes me tense.\p"
	.string "All I can do is pretend to be calm.$"

VictoryRoad_B2F_Text_DianneIntro:
	.string "The best of them make it as far as this\n"
	.string "cave.\p"
	.string "So then, what do you make of it?$"

VictoryRoad_B2F_Text_DianneDefeat:
	.string "You didn't even flinch!$"

VictoryRoad_B2F_Text_DiannePostBattle:
	.string "You've got nerve! I like it! Keep it up!$"

