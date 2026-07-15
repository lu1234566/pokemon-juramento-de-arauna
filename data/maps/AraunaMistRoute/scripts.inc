AraunaMistRoute_MapScripts::
	.byte 0

AraunaMistRoute_EventScript_ReturnToVillage::
	warp MAP_ARAUNA_MAP_LAB, 255, 18, 13
	waitstate
	end

AraunaMistRoute_EventScript_EnterRuin::
	warp MAP_ARAUNA_FIRST_LINK_RUIN, 255, 10, 13
	waitstate
	end
