#include "global.h"
#include "event_data.h"
#include "field_message_box.h"
#include "pokedex.h"
#include "strings.h"

bool16 ScriptGetPokedexInfo(void)
{
    if (gSpecialVar_0x8004 == 0) // is national dex not present?
    {
        gSpecialVar_0x8005 = GetHoennPokedexCount(FLAG_GET_SEEN);
        gSpecialVar_0x8006 = GetHoennPokedexCount(FLAG_GET_CAUGHT);
    }
    else
    {
        gSpecialVar_0x8005 = GetNationalPokedexCount(FLAG_GET_SEEN);
        gSpecialVar_0x8006 = GetNationalPokedexCount(FLAG_GET_CAUGHT);
    }

    return IsNationalPokedexEnabled();
}

// This shows your regional Pokédex rating and not your National Dex.
// Jirachi and Deoxys do not count towards completion. The brackets are spread
// over the rest of the dex, ten species each when the regional dex is Hoenn's.
const u8 *GetPokedexRatingText(u16 count)
{
    static const u8 *const sRatingTexts[] = {
        gBirchDexRatingText_LessThan10,
        gBirchDexRatingText_LessThan20,
        gBirchDexRatingText_LessThan30,
        gBirchDexRatingText_LessThan40,
        gBirchDexRatingText_LessThan50,
        gBirchDexRatingText_LessThan60,
        gBirchDexRatingText_LessThan70,
        gBirchDexRatingText_LessThan80,
        gBirchDexRatingText_LessThan90,
        gBirchDexRatingText_LessThan100,
        gBirchDexRatingText_LessThan110,
        gBirchDexRatingText_LessThan120,
        gBirchDexRatingText_LessThan130,
        gBirchDexRatingText_LessThan140,
        gBirchDexRatingText_LessThan150,
        gBirchDexRatingText_LessThan160,
        gBirchDexRatingText_LessThan170,
        gBirchDexRatingText_LessThan180,
        gBirchDexRatingText_LessThan190,
        gBirchDexRatingText_LessThan200,
    };
    u32 caught = count;
    u32 target = HOENN_DEX_COUNT - 2;

    if (caught && GetSetPokedexFlag(SpeciesToNationalPokedexNum(SPECIES_JIRACHI), FLAG_GET_CAUGHT))
        caught--;
    if (caught && GetSetPokedexFlag(SpeciesToNationalPokedexNum(SPECIES_DEOXYS), FLAG_GET_CAUGHT))
        caught--;
    if (caught >= target)
        return gBirchDexRatingText_DexCompleted;
    return sRatingTexts[caught * ARRAY_COUNT(sRatingTexts) / target];
}

void ShowPokedexRatingMessage(void)
{
    ShowFieldMessage(GetPokedexRatingText(gSpecialVar_0x8004));
}
