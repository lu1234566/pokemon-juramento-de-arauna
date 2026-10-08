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
    // DIVE_04_LANDMARKS_BEGIN
    // These native IDs also draw ordinary terrain. Only the tower's three
    // base coordinates receive aliases, including its temporary script state.
    if ((layout == gMapLayouts[675] || layout == gMapLayouts[711])
     && y == 56 && x >= 18 && x <= 20 && nativeId == 1008 + x - 18)
    {
        static const u16 baseVisuals[] = {515,516,523};
        return baseVisuals[x - 18];
    }
    // DIVE_04_LANDMARKS_END
    // Changed puzzle/script cells keep their native ID. No stored map word,
    // collision, elevation, behavior or save cache is ever rewritten here.
    if ((layout->map[index] & 0x03FF) != nativeId)
        return nativeId;
    for (i = 0; i < ARRAY_COUNT(sCaveVisualGrids); i++)
        if (layout == gMapLayouts[sCaveVisualGrids[i].layoutIndex])
            return sCaveVisualGrids[i].visual[index];
    return nativeId;
}
