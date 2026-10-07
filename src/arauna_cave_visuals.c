#include "global.h"
#include "fieldmap.h"
#include "arauna_cave_visuals.h"

extern const struct MapLayout *const gMapLayouts[];
struct CaveVisualGrid
{
    u16 layoutIndex;
    const u16 *visual;
};
#include "data/arauna_cave_visuals_v2.h"

u16 AraunaCaveVisualMetatile(const struct MapLayout *layout, s32 x, s32 y, u16 nativeId)
{
    u32 i;
    s32 index;
    x -= MAP_OFFSET;
    y -= MAP_OFFSET;
    if (x < 0 || y < 0 || x >= layout->width || y >= layout->height)
        return nativeId;
    index = y * layout->width + x;
    // Changed puzzle/script cells keep their native ID. No stored map word,
    // collision, elevation, behavior or save cache is ever rewritten here.
    if ((layout->map[index] & 0x03FF) != nativeId)
        return nativeId;
    for (i = 0; i < ARRAY_COUNT(sCaveVisualGrids); i++)
        if (layout == gMapLayouts[sCaveVisualGrids[i].layoutIndex])
            return sCaveVisualGrids[i].visual[index];
    return nativeId;
}
