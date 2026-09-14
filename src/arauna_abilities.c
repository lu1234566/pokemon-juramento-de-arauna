#include "global.h"
#include "battle.h"
#include "battle_util.h"
#include "arauna_abilities.h"
#include "pokemon.h"
#include "util.h"
#include "constants/abilities.h"
#include "constants/battle.h"
#include "constants/moves.h"
#include "constants/pokemon.h"

// The sound moves RIVER SONG works on. It is Soundproof's list plus the two
// Arauna moves that are plainly sound -- a voice and a song -- which belong on
// it whichever ability is asking.
static const u16 sAraunaSoundMoves[] =
{
    MOVE_GROWL, MOVE_ROAR, MOVE_SING, MOVE_SUPERSONIC, MOVE_SCREECH, MOVE_SNORE,
    MOVE_UPROAR, MOVE_METAL_SOUND, MOVE_GRASS_WHISTLE, MOVE_HYPER_VOICE,
    MOVE_DISARMING_VOICE, MOVE_CANTO_DA_IARA,
};

bool8 AraunaIsSoundMove(u16 move)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sAraunaSoundMoves); i++)
    {
        if (sAraunaSoundMoves[i] == move)
            return TRUE;
    }
    return FALSE;
}

// Speed as the turn order sees it: the stat with its stat stages applied.
// Paralysis is left out on purpose -- WINGED WATCH asks who is quicker by
// nature, not who is limping this turn.
static u32 EffectiveSpeed(struct BattlePokemon *mon)
{
    return (mon->speed * gStatStageRatios[mon->statStages[STAT_SPEED]][0])
         / gStatStageRatios[mon->statStages[STAT_SPEED]][1];
}

static bool8 IsWeather(u16 mask)
{
    return (WEATHER_HAS_EFFECT && (gBattleWeather & mask)) != 0;
}

s32 AraunaModifyDamage(s32 damage, struct BattlePokemon *attacker,
                       struct BattlePokemon *defender, u8 type,
                       u8 battlerIdAtk, u8 battlerIdDef)
{
    bool8 calm = !(WEATHER_HAS_EFFECT && (gBattleWeather & B_WEATHER_ANY));

    switch (attacker->ability)
    {
    case ABILITY_FOGO_LEAL:
        if (type == TYPE_FIRE || type == TYPE_DRAGON)
            damage = (115 * damage) / 100;
        break;
    case ABILITY_VIGIA_ALADO:
        if ((type == TYPE_WATER || type == TYPE_BUG)
         && EffectiveSpeed(attacker) > EffectiveSpeed(defender))
            damage = (120 * damage) / 100;
        break;
    case ABILITY_BICO_GRANITO:
        if (type == TYPE_ROCK)
            damage = (120 * damage) / 100;
        break;
    case ABILITY_CANTO_RIO:
        if (AraunaIsSoundMove(gCurrentMove))
            damage = (130 * damage) / 100;
        break;
    case ABILITY_SOL_PRIMEIRO:
        if ((type == TYPE_FIRE || type == TYPE_PSYCHIC) && IsWeather(B_WEATHER_SUN))
            damage = (120 * damage) / 100;
        break;
    case ABILITY_FOGO_ANTIGO:
        if (type == TYPE_FIRE)
        {
            // Rain already halved this above, inside the formula. Doubling it
            // back is the only way to undo it from here, and it is exact up to
            // the one unit that integer halving throws away.
            if (IsWeather(B_WEATHER_RAIN))
                damage *= 2;
            damage = (120 * damage) / 100;
        }
        break;
    case ABILITY_MARE_MESTRA:
        if ((type == TYPE_WATER || type == TYPE_DRAGON) && IsWeather(B_WEATHER_RAIN))
            damage = (120 * damage) / 100;
        break;
    case ABILITY_ULTIMA_LUZ:
        if ((type == TYPE_DARK || type == TYPE_FIRE) && attacker->hp * 2 <= attacker->maxHP)
            damage = (125 * damage) / 100;
        break;
    case ABILITY_REI_DO_RIO:
        if (type == TYPE_WATER || type == TYPE_DRAGON)
            damage = (115 * damage) / 100;
        break;
    case ABILITY_MAR_SAGRADO:
        if (type == TYPE_FAIRY && IsWeather(B_WEATHER_RAIN))
            damage = (120 * damage) / 100;
        break;
    case ABILITY_ESSENCIA:
        if (type == TYPE_DRAGON || type == TYPE_PSYCHIC)
            damage = (110 * damage) / 100;
        break;
    }

    switch (defender->ability)
    {
    case ABILITY_COBRA_GRANDE:
        if (defender->hp == defender->maxHP)
            damage = (75 * damage) / 100;
        break;
    case ABILITY_VEU_LUNAR:
        if (calm && IS_TYPE_SPECIAL(type))
            damage = (80 * damage) / 100;
        break;
    case ABILITY_SECA_BRAVA:
        if (type == TYPE_WATER)
            damage /= 2;
        break;
    }

    return damage;
}

u16 AraunaModifySpDefense(u16 spDefense, struct BattlePokemon *defender)
{
    if (defender->ability == ABILITY_LUA_PRIMEVA
     && !(WEATHER_HAS_EFFECT && (gBattleWeather & B_WEATHER_ANY)))
        spDefense = (125 * spDefense) / 100;

    return spDefense;
}

u8 AraunaStatDropGuard(u8 battler, u8 statId)
{
    u8 ally;

    switch (gBattleMons[battler].ability)
    {
    case ABILITY_RESISTENCIA:
    case ABILITY_ESSENCIA:
    case ABILITY_LACO_ETERNO:
        return battler;
    case ABILITY_BICO_GRANITO:
        if (statId == STAT_DEF)
            return battler;
        break;
    }

    // ETERNAL BOND covers the whole side, so the ally can be the one refusing.
    if (gBattleTypeFlags & BATTLE_TYPE_DOUBLE)
    {
        ally = BATTLE_PARTNER(battler);
        if (!(gAbsentBattlerFlags & gBitTable[ally]) && gBattleMons[ally].hp != 0
         && gBattleMons[ally].ability == ABILITY_LACO_ETERNO)
            return ally;
    }

    return 0xFF;
}

bool8 AraunaBlocksFlinch(u16 ability)
{
    return (ability == ABILITY_REI_DO_RIO || ability == ABILITY_RESISTENCIA);
}

bool8 AraunaBlocksBurn(u16 ability)
{
    return (ability == ABILITY_FOGO_LEAL);
}

bool8 AraunaMoveNeverMisses(u16 ability, u16 move)
{
    return (ability == ABILITY_CANTO_RIO && AraunaIsSoundMove(move));
}

bool8 AraunaMoveGetsPriority(u16 ability, u16 move)
{
    return (ability == ABILITY_PE_INVERSO && gBattleMoves[move].power == 0
         && move != MOVE_NONE);
}

bool8 AraunaAddsParalysis(u16 ability, u8 moveType, u16 move)
{
    return (ability == ABILITY_VOZ_DE_TUPA
         && (moveType == TYPE_ELECTRIC || moveType == TYPE_DRAGON)
         && gBattleMoves[move].power != 0);
}
