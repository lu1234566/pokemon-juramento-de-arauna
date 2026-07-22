#include "global.h"
#include "battle.h"
#include "event_data.h"
#include "caps.h"
#include "pokemon.h"


bool32 IsAraunaNextBossLevelCapAvailable(void)
{
    return !FlagGet(FLAG_ARAUNA_BADGE_UIVO);
}

static u32 GetFullCampaignLevelCap(void)
{
    // Full-campaign badge/boss curve for the Houses beyond the implemented
    // vertical slice. The Arauna badges also set the matching FLAG_BADGE0x_GET,
    // so the standard flag list keeps a sane target once the bespoke story caps
    // run out. Each entry is the level cap while that badge is still unearned.
    static const u16 sLevelCapFlagMap[][2] = {
        {FLAG_BADGE01_GET, 15}, // Dona Celina's Mare Trial
        {FLAG_BADGE02_GET, 19}, // Hermit's Uivo Trial
        {FLAG_BADGE03_GET, 24},
        {FLAG_BADGE04_GET, 29},
        {FLAG_BADGE05_GET, 31},
        {FLAG_BADGE06_GET, 33},
        {FLAG_BADGE07_GET, 42},
        {FLAG_BADGE08_GET, 46},
        {FLAG_IS_CHAMPION,  58},
    };

    if (B_LEVEL_CAP_TYPE == LEVEL_CAP_FLAG_LIST)
    {
        for (u32 index = 0; index < ARRAY_COUNT(sLevelCapFlagMap); index++)
        {
            if (!FlagGet(sLevelCapFlagMap[index][0]))
                return sLevelCapFlagMap[index][1];
        }
    }
    return MAX_LEVEL;
}

u32 GetCurrentLevelCap(void)
{
    // The implemented vertical slice uses finer story pacing than the badge
    // list can express; once its last mandatory boss is behind us, defer to the
    // full-campaign badge curve.
    if (!IsAraunaNextBossLevelCapAvailable())
        return GetFullCampaignLevelCap();
    if (FlagGet(FLAG_ARAUNA_BADGE_MARE))
        return 27; // Hermit's Uivo Trial
    if (FlagGet(FLAG_ARAUNA_PORTO_AGENT_DEFEATED))
        return 17; // Dona Celina's Mare Trial
    if (VarGet(VAR_ARAUNA_STORY_STAGE) >= 8)
        return 12; // Consortium Agent
    return 7; // Ciro
}

u32 GetSoftLevelCapExpValue(u32 level, u32 expValue)
{
    static const u32 sExpScalingDown[5] = { 4, 8, 16, 32, 64 };
    static const u32 sExpScalingUp[5]   = { 16, 8, 4, 2, 1 };

    u32 levelDifference;
    u32 currentLevelCap = GetCurrentLevelCap();

    if (B_EXP_CAP_TYPE == EXP_CAP_NONE)
        return expValue;

    if (level < currentLevelCap)
    {
        if (B_LEVEL_CAP_EXP_UP)
        {
            levelDifference = currentLevelCap - level;
            if (levelDifference > ARRAY_COUNT(sExpScalingUp) - 1)
                return expValue + (expValue / sExpScalingUp[ARRAY_COUNT(sExpScalingUp) - 1]);
            else
                return expValue + (expValue / sExpScalingUp[levelDifference]);
        }
        else
        {
            return expValue;
        }
    }
    else if (B_EXP_CAP_TYPE == EXP_CAP_HARD)
    {
        return 0;
    }
    else if (B_EXP_CAP_TYPE == EXP_CAP_SOFT)
    {
        levelDifference = level - currentLevelCap;
        if (levelDifference > ARRAY_COUNT(sExpScalingDown) - 1)
            return expValue / sExpScalingDown[ARRAY_COUNT(sExpScalingDown) - 1];
        else
            return expValue / sExpScalingDown[levelDifference];
    }
    else
    {
       return expValue;
    }
}

u32 GetCurrentEVCap(void)
{
    static const u16 sEvCapFlagMap[][2] = {
        // Define EV caps for each milestone
        {FLAG_BADGE01_GET, MAX_TOTAL_EVS *  1 / 17},
        {FLAG_BADGE02_GET, MAX_TOTAL_EVS *  3 / 17},
        {FLAG_BADGE03_GET, MAX_TOTAL_EVS *  5 / 17},
        {FLAG_BADGE04_GET, MAX_TOTAL_EVS *  7 / 17},
        {FLAG_BADGE05_GET, MAX_TOTAL_EVS *  9 / 17},
        {FLAG_BADGE06_GET, MAX_TOTAL_EVS * 11 / 17},
        {FLAG_BADGE07_GET, MAX_TOTAL_EVS * 13 / 17},
        {FLAG_BADGE08_GET, MAX_TOTAL_EVS * 15 / 17},
        {FLAG_IS_CHAMPION, MAX_TOTAL_EVS},
    };

    if (B_EV_CAP_TYPE == EV_CAP_FLAG_LIST)
    {
        for (u32 evCap = 0; evCap < ARRAY_COUNT(sEvCapFlagMap); evCap++)
        {
            if (!FlagGet(sEvCapFlagMap[evCap][0]))
                return sEvCapFlagMap[evCap][1];
        }
    }
    else if (B_EV_CAP_TYPE == EV_CAP_VARIABLE)
    {
        return VarGet(B_EV_CAP_VARIABLE);
    }
    else if (B_EV_CAP_TYPE == EV_CAP_NO_GAIN)
    {
        return 0;
    }

    return MAX_TOTAL_EVS;
}
