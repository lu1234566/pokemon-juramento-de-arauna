// Quality-of-life additions for Juramento de Arauna.
//
// Everything here is opt-in from the player's side: nothing fires on its own,
// and the only rule it changes without being asked is the experience ceiling,
// which is the point of having a level cap at all.
//
// Save layout is untouched. AUTO RUN, WARD and POTENTIAL persist in
// bits that struct SaveBlock2 already reserved as padding inside the existing
// options word, so an old save still loads.

#include "global.h"
#include "arauna_qol.h"
#include "daycare.h"
#include "event_data.h"
#include "pokemon.h"
#include "party_menu.h"
#include "script_pokemon_util.h"
#include "constants/daycare.h"
#include "constants/flags.h"
#include "constants/pokemon.h"

// The cap is the ace of the next boss still ahead of the player, read off the
// parties in src/data/trainer_parties.h rather than chosen by feel:
//
//   badges  next boss                    ace
//   0       Serra do Uivo                15
//   1       Porto das Redes              19
//   2       Encruzilhada                 24
//   3       Casa da Cinza                29
//   4       Pampa da Espera              31
//   5       Mata do Meio                 33
//   6       Missoes do Ceu               42
//   7       Aguas de M'Boi               46
//   8       Elite, first seat            49
//   champion                             58  (the champion's own ace)
//
// So a capped party can match the boss's strongest Pokemon and never overshoot
// it. The jump from 33 to 42 across the sixth badge is the game's own, not
// something added here; it is the one place where a player will feel the cap
// as a wall rather than a guide.
static const u8 sLevelCapByBadges[NUM_BADGES + 1] =
{
    [0] = 15,
    [1] = 19,
    [2] = 24,
    [3] = 29,
    [4] = 31,
    [5] = 33,
    [6] = 42,
    [7] = 46,
    [8] = 49,
};

#define ARAUNA_CAP_CHAMPION 58

u8 AraunaLevelCap(void)
{
    u8 badges = 0;
    u8 i;

    // Past the Elite the cap opens to the champion's ace, and after the story
    // is finished it opens entirely -- there is no boss left to pace against.
    if (FlagGet(FLAG_SYS_GAME_CLEAR))
        return MAX_LEVEL;

    for (i = 0; i < NUM_BADGES; i++)
    {
        if (FlagGet(FLAG_BADGE01_GET + i))
            badges++;
    }

    if (badges >= NUM_BADGES
        && FlagGet(FLAG_DEFEATED_ELITE_4_SIDNEY)
        && FlagGet(FLAG_DEFEATED_ELITE_4_PHOEBE)
        && FlagGet(FLAG_DEFEATED_ELITE_4_GLACIA)
        && FlagGet(FLAG_DEFEATED_ELITE_4_DRAKE))
        return ARAUNA_CAP_CHAMPION;

    return sLevelCapByBadges[badges];
}

bool8 AraunaIsAtLevelCap(struct Pokemon *mon)
{
    u8 level = GetMonData(mon, MON_DATA_LEVEL);

    if (level >= MAX_LEVEL)
        return TRUE;

    return level >= AraunaLevelCap();
}

void AraunaHealParty(void)
{
    HealPlayerParty();
}

u8 AraunaGetTeachableEggMoves(struct Pokemon *mon, u16 *moves)
{
    u16 all[EGG_MOVES_ARRAY_COUNT];
    u8 count = GetEggMoves(mon, all);
    u8 out = 0;
    u8 i, j;

    for (i = 0; i < count; i++)
    {
        bool8 known = FALSE;

        for (j = 0; j < MAX_MON_MOVES; j++)
        {
            if (GetMonData(mon, MON_DATA_MOVE1 + j) == all[i])
            {
                known = TRUE;
                break;
            }
        }

        if (!known)
            moves[out++] = all[i];
    }

    return out;
}

// ---------------------------------------------------------------------------
// Specials. The menu itself is a script, so these are the pieces the script
// cannot do on its own.
// ---------------------------------------------------------------------------

#include "field_screen_effect.h"
#include "script.h"
#include "sound.h"
#include "start_menu.h"
#include "constants/songs.h"

// Reports the cap into VAR_RESULT so the script can print it.
void AraunaSpecial_GetLevelCap(void)
{
    gSpecialVar_Result = AraunaLevelCap();
}

// LEVEL uses the existing Rare Candy move/evolution flow, one selected level
// at a time. No direct EXP jump and no inventory item is consumed.
void AraunaSpecial_SetPartyToLevelCap(void)
{
    AraunaChooseMonToLevel();
}

// Full restore for the party, free and anywhere.
void AraunaSpecial_HealParty(void)
{
    AraunaHealParty();
    PlayFanfare(MUS_HEAL);
}

// Flips the relearner screen between level-up moves and egg moves.
void AraunaSpecial_EggMoveModeOn(void)
{
    AraunaSetEggMoveMode(TRUE);
}

void AraunaSpecial_EggMoveModeOff(void)
{
    AraunaSetEggMoveMode(FALSE);
}

// The two switches the menu offers. Each reports its new state in VAR_RESULT so
// the script can say which way it went without duplicating the knowledge.
void AraunaSpecial_ToggleInfiniteRepel(void)
{
    gSaveBlock2Ptr->optionsInfiniteRepel ^= 1;
    gSpecialVar_Result = gSaveBlock2Ptr->optionsInfiniteRepel;
}

void AraunaSpecial_ToggleShowIVs(void)
{
    gSaveBlock2Ptr->optionsShowIVs ^= 1;
    gSpecialVar_Result = gSaveBlock2Ptr->optionsShowIVs;
}
