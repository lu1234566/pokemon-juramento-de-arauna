#include "global.h"
#include "event_data.h"
#include "field_player_avatar.h"
#include "config/arauna.h"

#undef PartyHasMonWithSurf

extern bool8 PartyHasMonWithSurf(void);

bool8 AraunaPartyHasMonWithSurf(void)
{
    if (FlagGet(FLAG_ARAUNA_BOARD_FIELD_UNLOCKED))
        return TRUE;

    return PartyHasMonWithSurf();
}
