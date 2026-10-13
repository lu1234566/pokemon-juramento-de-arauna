#include "global.h"
#include "arauna_cries.h"
#include "m4a.h"
#include "constants/species.h"

#include "data/arauna_cries.h"

const struct ToneData *AraunaGetCryTone(u16 species, bool8 reverse)
{
    const struct ToneData *tones = reverse ? sAraunaCryTonesReverse : sAraunaCryTones;

    if (species > SPECIES_EGG && species <= SPECIES_UNOWN_QMARK)
        species = SPECIES_UNOWN;
    if (species >= NUM_SPECIES || tones[species].wav == NULL)
        return NULL;
    return &tones[species];
}
