#include "global.h"
#include "fieldmap.h"
#include "arauna_border_visuals.h"
#include "arauna_cave_visuals.h"

extern const struct Tileset gTileset_AraunaRoute119BorderV1;
extern const struct Tileset gTileset_AraunaRoute118BorderV1;

extern const struct Tileset gTileset_AraunaBorderRoute124ArtV2;
extern const struct Tileset gTileset_AraunaBorderRoute126ArtV2;
extern const struct Tileset gTileset_AraunaBorderRoute110ArtV2;
extern const struct Tileset gTileset_AraunaBorderMauvilleCityArtV2;
extern const struct Tileset gTileset_AraunaBorderSlateportCityArtV2;
extern const struct Tileset gTileset_AraunaBorderEverGrandeCityArtV2;
extern const struct Tileset gTileset_AraunaBorderRoute128ArtV2;
extern const struct Tileset gTileset_AraunaBorderRoute103ArtV2;

extern const struct Tileset gTileset_AraunaBorderRoute124ArtSulV1;
extern const struct Tileset gTileset_AraunaBorderRoute126ArtSulV1;
extern const struct Tileset gTileset_AraunaBorderRoute110ArtSulV1;
extern const struct Tileset gTileset_AraunaBorderMauvilleCityArtSulV1;
extern const struct Tileset gTileset_AraunaBorderSlateportCityArtSulV1;
extern const struct Tileset gTileset_AraunaBorderEverGrandeCityArtSulV1;
extern const struct Tileset gTileset_AraunaBorderRoute128ArtSulV1;
extern const struct Tileset gTileset_AraunaBorderRoute103ArtSulV1;
extern const struct Tileset gTileset_AraunaBorderPetalburgCityArtSulV1;
extern const struct Tileset gTileset_AraunaBorderRoute104ArtSulV1;
extern const struct Tileset gTileset_AraunaBorderRustboroCityArtSulV1;
extern const struct Tileset gTileset_AraunaBorderRoute111ArtSulV1;
extern const struct Tileset gTileset_AraunaBorderRoute117ArtSulV1;
extern const struct Tileset gTileset_AraunaBorderRoute118ArtSulV1;
extern const struct Tileset gTileset_AraunaBorderRoute115ArtSulV1;
extern const struct Tileset gTileset_AraunaBorderLavaridgeTownArtSulV1;
extern const struct Tileset gTileset_AraunaBorderRoute112ArtSulV1;
extern const struct Tileset gTileset_AraunaBorderRoute102ArtSulV1;
extern const struct Tileset gTileset_AraunaBorderOldaleTownArtSulV1;
extern const struct Tileset gTileset_AraunaBorderRoute105ArtSulV1;
extern const struct Tileset gTileset_AraunaBorderRoute119ArtSulV1;

struct BorderVisualAlias
{
    u16 nativeId;
    u16 visualId;
};

#include "data/arauna_border_visuals.h"
#include "data/arauna_border_priority_v2.h"
#include "data/arauna_border_sul_v1.h"

bool8 AraunaMapUsesBorderVisuals(const struct MapLayout *layout)
{
    return layout->secondaryTileset == &gTileset_AraunaRoute119BorderV1
        || layout->secondaryTileset == &gTileset_AraunaRoute118BorderV1
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute124ArtV2
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute126ArtV2
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute110ArtV2
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute124ArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute126ArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute110ArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderMauvilleCityArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderSlateportCityArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderEverGrandeCityArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute128ArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute103ArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderPetalburgCityArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute104ArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderRustboroCityArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute111ArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute117ArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute118ArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute115ArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderLavaridgeTownArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute112ArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute102ArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderOldaleTownArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute105ArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute119ArtSulV1
        || layout->secondaryTileset == &gTileset_AraunaBorderMauvilleCityArtV2
        || layout->secondaryTileset == &gTileset_AraunaBorderSlateportCityArtV2
        || layout->secondaryTileset == &gTileset_AraunaBorderEverGrandeCityArtV2
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute128ArtV2
        || layout->secondaryTileset == &gTileset_AraunaBorderRoute103ArtV2;
}

bool8 AraunaConnectionNeedsFullReload(const struct MapLayout *from, const struct MapLayout *to)
{
    // Vanilla connections always share the primary bank; most Arauna routes
    // bring their own, so the old tiles and palettes 0-5 must not survive.
    return from->primaryTileset != to->primaryTileset
        || AraunaMapUsesBorderVisuals(from)
        || AraunaMapUsesBorderVisuals(to);
}

u16 AraunaBorderVisualMetatile(const struct MapLayout *layout, s32 x, s32 y, u16 nativeId)
{
    const struct BorderVisualAlias *aliases = NULL;
    u32 count = 0;
    u32 i;

    // FillSouthConnection: source Route118 x=33..79, y=0..6.
    if (layout->secondaryTileset == &gTileset_AraunaRoute119BorderV1
     && x >= 0 && x < 47 && y >= 147 && y < 154)
    {
        aliases = sRoute119BorderAliases;
        count = ARRAY_COUNT(sRoute119BorderAliases);
    }
    // FillNorthConnection: source Route119 x=0..39, y=133..139.
    else if (layout->secondaryTileset == &gTileset_AraunaRoute118BorderV1
          && x >= 47 && x < 87 && y >= 0 && y < MAP_OFFSET)
    {
        aliases = sRoute118BorderAliases;
        count = ARRAY_COUNT(sRoute118BorderAliases);
    }

    for (i = 0; i < count; i++)
        if (aliases[i].nativeId == nativeId)
            return aliases[i].visualId;
    for (i = 0; i < ARRAY_COUNT(sSulBorderRegions); i++)
    {
        const struct SulBorderRegion *region = &sSulBorderRegions[i];
        u32 j;
        if (layout->secondaryTileset != region->bank || x < region->x1 || x >= region->x2 || y < region->y1 || y >= region->y2)
            continue;
        for (j = 0; j < region->count; j++)
            if (region->aliases[j].nativeId == nativeId)
                return region->aliases[j].visualId;
    }
    for (i = 0; i < ARRAY_COUNT(sPriorityBorderRegions); i++)
    {
        const struct PriorityBorderRegion *region = &sPriorityBorderRegions[i];
        u32 j;
        if (layout->secondaryTileset != region->bank || x < region->x1 || x >= region->x2 || y < region->y1 || y >= region->y2)
            continue;
        for (j = 0; j < region->count; j++)
            if (region->aliases[j].nativeId == nativeId)
                return region->aliases[j].visualId;
    }
    return AraunaCaveVisualMetatile(layout, x, y, nativeId);
}
