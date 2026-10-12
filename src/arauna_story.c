// Creatures that stand in a story scene (draft arcs, docs/ARCOS_RASCUNHO.md).
//
// The walking redraws are placed by tools/arauna/build_overworld_placement.py,
// one map each, from the wild tables. A scene creature is different: it is
// there because the story put it there, and its own object flag decides when.
// This only picks which redraw the dispatcher channel shows on that map; it
// runs after the placement table and the legends, so the scene wins.

#include "global.h"
#include "arauna_story.h"
#include "event_data.h"
#include "constants/arauna_overworld.h"
#include "constants/maps.h"
#include "constants/vars.h"

struct AraunaSceneCreature
{
    u8 mapGroup;
    u8 mapNum;
    u8 channel;
    u8 overworld;
};

static const struct AraunaSceneCreature sSceneCreatures[] =
{
    // Casa do Uivo, U06-U07: the pup howling above the waterfall.
    { MAP_GROUP(MAP_ARAUNA_CASA_UIVO_REFUGIO), MAP_NUM(MAP_ARAUNA_CASA_UIVO_REFUGIO), ARAUNA_OW_CHANNEL_A, ARAUNA_OW_GUARACIM },
};

void AraunaStory_OnTransition(void)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sSceneCreatures); i++)
    {
        const struct AraunaSceneCreature *scene = &sSceneCreatures[i];

        if (scene->mapGroup == gSaveBlock1Ptr->location.mapGroup
         && scene->mapNum == gSaveBlock1Ptr->location.mapNum)
            VarSet(scene->channel == ARAUNA_OW_CHANNEL_A ? VAR_ARAUNA_OW_A : VAR_ARAUNA_OW_B,
                   scene->overworld);
    }
}
