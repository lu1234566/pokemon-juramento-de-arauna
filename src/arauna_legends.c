// The twenty legendaries and mythicals that wait in the world for the player.
//
// Where each one stands, which dispatcher channel draws it and which flag says
// it is gone all come from src/data/arauna_legends.h, generated from
// docs/arauna/ARAUNA_LEGENDS.csv by tools/arauna/build_legends.py.
//
// The flag is the object's own visibility flag, so "set" means "not in the
// world". It is set for three reasons:
//
//   - asleep: before the first Hall of Fame, every map sets it on the way in,
//     which keeps creatures of level 58-68 out of the main campaign;
//   - caught;
//   - knocked out, until the next Hall of Fame wakes it again.
//
// Nothing here touches the save layout: the flags are twenty story flags
// vanilla never used.

#include "global.h"
#include "arauna_legends.h"
#include "battle.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "overworld.h"
#include "pokedex.h"
#include "pokemon.h"
#include "region_map.h"
#include "string_util.h"
#include "strings.h"
#include "constants/arauna_overworld.h"
#include "constants/battle.h"
#include "constants/characters.h"
#include "constants/flags.h"
#include "constants/map_event_ids.h"
#include "constants/maps.h"
#include "constants/species.h"
#include "constants/vars.h"

struct AraunaLegend
{
    u16 species;
    u16 flag;
    u8 mapGroup;
    u8 mapNum;
    u8 localId;
    u8 channel;
    u8 overworld;
};

#include "data/arauna_legends.h"

static bool32 IsOnCurrentMap(const struct AraunaLegend *legend)
{
    return legend->mapGroup == gSaveBlock1Ptr->location.mapGroup
        && legend->mapNum == gSaveBlock1Ptr->location.mapNum;
}

static bool32 IsCaught(const struct AraunaLegend *legend)
{
    return GetSetPokedexFlag(SpeciesToNationalPokedexNum(legend->species), FLAG_GET_CAUGHT);
}

// Runs before the map's own ON_TRANSITION script, after the overworld table has
// set the dispatcher channels, so a legend wins the channel on its own map.
void AraunaLegends_OnTransition(void)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sAraunaLegends); i++)
    {
        const struct AraunaLegend *legend = &sAraunaLegends[i];

        if (!IsOnCurrentMap(legend))
            continue;
        VarSet(legend->channel == ARAUNA_OW_CHANNEL_A ? VAR_ARAUNA_OW_A : VAR_ARAUNA_OW_B,
               legend->overworld);
        if (!FlagGet(FLAG_SYS_GAME_CLEAR))
            FlagSet(legend->flag);
    }
}

// The same thing the Regi chambers do in their ON_RESUME scripts, for every
// legend at once: a caught legend is gone before the screen fades back in.
void AraunaLegends_OnResume(void)
{
    u32 i;

    if (!FlagGet(FLAG_SYS_CTRL_OBJ_DELETE) || gBattleOutcome != B_OUTCOME_CAUGHT)
        return;
    for (i = 0; i < ARRAY_COUNT(sAraunaLegends); i++)
    {
        const struct AraunaLegend *legend = &sAraunaLegends[i];

        if (IsOnCurrentMap(legend) && legend->localId == gSpecialVar_LastTalked)
            RemoveObjectEventByLocalIdAndMap(legend->localId, legend->mapNum, legend->mapGroup);
    }
}

// Hall of Fame: wake every legend the player has not caught. The first time,
// that is all twenty; afterwards, the ones knocked out since.
void AraunaLegends_Reawaken(void)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sAraunaLegends); i++)
    {
        if (IsCaught(&sAraunaLegends[i]))
            FlagSet(sAraunaLegends[i].flag);
        else
            FlagClear(sAraunaLegends[i].flag);
    }
}

static const u8 sText_SignalsHeader[] = _("The needles are still trembling.\pIt counts ");
static const u8 sText_SignalsTail[] = _(" BOND signals\nstill out in ARAUNA:");
static const u8 sText_SignalsOne[] = _(" BOND signal\nstill out in ARAUNA:");
static const u8 sText_SignalsNone[] = _("The needles have come to rest.\pEvery BOND signal it ever caught\nhas been answered.");
static const u8 sText_Colon[] = _(": ");

// The BOND sensor in Anahi's lab, after the Hall of Fame: how many legends are
// still standing in the world, grouped by place, in table order. Writes the
// message to gStringVar4 and the count to VAR_RESULT.
void AraunaLegends_BufferSignals(void)
{
    u16 sections[ARRAY_COUNT(sAraunaLegends)];
    u8 counts[ARRAY_COUNT(sAraunaLegends)];
    u32 i, j, groups = 0, total = 0;
    u8 *str;

    for (i = 0; i < ARRAY_COUNT(sAraunaLegends); i++)
    {
        const struct AraunaLegend *legend = &sAraunaLegends[i];
        u16 section;

        if (FlagGet(legend->flag))
            continue;
        section = Overworld_GetMapHeaderByGroupAndId(legend->mapGroup, legend->mapNum)->regionMapSectionId;
        for (j = 0; j < groups && sections[j] != section; j++)
            ;
        if (j == groups)
        {
            sections[groups] = section;
            counts[groups++] = 0;
        }
        counts[j]++;
        total++;
    }

    gSpecialVar_Result = total;
    if (total == 0)
    {
        StringCopy(gStringVar4, sText_SignalsNone);
        return;
    }

    str = StringCopy(gStringVar4, sText_SignalsHeader);
    str = ConvertIntToDecimalStringN(str, total, STR_CONV_MODE_LEFT_ALIGN, 2);
    str = StringCopy(str, total == 1 ? sText_SignalsOne : sText_SignalsTail);
    for (i = 0; i < groups; i++)
    {
        // Two places to a page: a new page before every odd one.
        *str++ = (i % 2 == 0) ? CHAR_PROMPT_CLEAR : CHAR_NEWLINE;
        str = GetMapName(str, sections[i], 0);
        str = StringCopy(str, sText_Colon);
        str = ConvertIntToDecimalStringN(str, counts[i], STR_CONV_MODE_LEFT_ALIGN, 2);
    }
    *str = EOS;
}
