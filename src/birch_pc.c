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

// This shows your regional Pokédex rating and not your National Dex, at the
// PC and over the PokéNav. It counts what completion counts (see
// GetPokedexCompletionCount), and the brackets are spread over that total, ten
// species each when it is Hoenn's 200.
const u8 *GetPokedexRatingText(void)
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
    u16 target;
    u32 caught = GetPokedexCompletionCount(&target);

    if (caught >= target)
        return gBirchDexRatingText_DexCompleted;
    return sRatingTexts[caught * ARRAY_COUNT(sRatingTexts) / target];
}

void ShowPokedexRatingMessage(void)
{
    ShowFieldMessage(GetPokedexRatingText());
}
