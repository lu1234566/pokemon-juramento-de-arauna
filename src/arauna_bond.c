// The first link of the Primeira Camara (draft arc, docs/ARCOS_RASCUNHO.md).
//
// At the altar the player names one companion as their first link. The save
// keeps that creature's personality in two vars, so the link follows the
// creature itself -- through the PC, a nickname change or evolution -- and not
// a party slot.
//
// In battle, a first link whose friendship has reached
// ARAUNA_BOND_HOLD_FRIENDSHIP holds on with 1 HP the first time a hit would
// knock it out, once per battle. It borrows the Focus Band's place in the
// damage step and prints its own line instead of the item's. Link, recorded,
// Frontier, Trainer Hill, Secret Base and e-Reader battles are left alone:
// there the rules are shared with someone who never visited the altar.

#include "global.h"
#include "arauna_bond.h"
#include "battle.h"
#include "battle_anim.h"
#include "event_data.h"
#include "pokemon.h"
#include "string_util.h"
#include "constants/battle.h"
#include "constants/flags.h"
#include "constants/pokemon.h"
#include "constants/species.h"
#include "constants/vars.h"

#define BOND_EXCLUDED_BATTLES (BATTLE_TYPE_LINK | BATTLE_TYPE_RECORDED | BATTLE_TYPE_RECORDED_LINK \
                             | BATTLE_TYPE_FRONTIER | BATTLE_TYPE_TOWER_LINK_MULTI                   \
                             | BATTLE_TYPE_TRAINER_HILL | BATTLE_TYPE_SECRET_BASE                     \
                             | BATTLE_TYPE_EREADER_TRAINER)

// How much the rite itself strengthens the link.
#define RITE_FRIENDSHIP_GAIN 20

static u32 FirstLinkPersonality(void)
{
    return VarGet(VAR_ARAUNA_FIRST_LINK_LO) | ((u32)VarGet(VAR_ARAUNA_FIRST_LINK_HI) << 16);
}

void AraunaBond_TryHoldOn(u8 battler)
{
    if (!FlagGet(FLAG_ARAUNA_FIRST_LINK_MADE)
     || (gBattleTypeFlags & BOND_EXCLUDED_BATTLES)
     || gBattleStruct->araunaBondUsed
     || GetBattlerSide(battler) != B_SIDE_PLAYER)
        return;
    if (gBattleMons[battler].personality != FirstLinkPersonality()
     || gBattleMons[battler].friendship < ARAUNA_BOND_HOLD_FRIENDSHIP)
        return;
    // Only a hit that would knock it out, and only where nothing else already
    // keeps it standing.
    if (gBattleMons[battler].hp > gBattleMoveDamage
     || (gBattleMons[battler].status2 & STATUS2_SUBSTITUTE)
     || gProtectStructs[battler].endured
     || gSpecialStatuses[battler].focusBanded)
        return;

    gSpecialStatuses[battler].focusBanded = TRUE;
    gBattleStruct->araunaBondUsed = TRUE;
    gBattleStruct->araunaBondMessage = TRUE;
}

// Called where the Focus Band's message would be printed: TRUE once, right
// after the link held on.
bool8 AraunaBond_TakeMessage(void)
{
    if (!gBattleStruct->araunaBondMessage)
        return FALSE;
    gBattleStruct->araunaBondMessage = FALSE;
    return TRUE;
}

// special: the party slot in VAR_0x8004 (from ChoosePartyMon). VAR_RESULT gets
// how strong the bond reads, 0 (thin) to 3 (would hold on), or 0xFF for an Egg;
// gStringVar1 gets the creature's name.
void AraunaBond_ReadSelected(void)
{
    struct Pokemon *mon = &gPlayerParty[gSpecialVar_0x8004];
    u32 friendship;

    if (GetMonData(mon, MON_DATA_IS_EGG))
    {
        gSpecialVar_Result = 0xFF;
        return;
    }
    GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
    StringGet_Nickname(gStringVar1);
    friendship = GetMonData(mon, MON_DATA_FRIENDSHIP);
    if (friendship >= ARAUNA_BOND_HOLD_FRIENDSHIP)
        gSpecialVar_Result = 3;
    else if (friendship >= 150)
        gSpecialVar_Result = 2;
    else if (friendship >= 70)
        gSpecialVar_Result = 1;
    else
        gSpecialVar_Result = 0;
}

// special: names the creature in VAR_0x8004 as the first link.
void AraunaBond_MakeFirstLink(void)
{
    struct Pokemon *mon = &gPlayerParty[gSpecialVar_0x8004];
    u32 personality = GetMonData(mon, MON_DATA_PERSONALITY);
    u32 friendship = GetMonData(mon, MON_DATA_FRIENDSHIP) + RITE_FRIENDSHIP_GAIN;

    if (friendship > MAX_FRIENDSHIP)
        friendship = MAX_FRIENDSHIP;
    SetMonData(mon, MON_DATA_FRIENDSHIP, &friendship);
    VarSet(VAR_ARAUNA_FIRST_LINK_LO, personality & 0xFFFF);
    VarSet(VAR_ARAUNA_FIRST_LINK_HI, personality >> 16);
    FlagSet(FLAG_ARAUNA_FIRST_LINK_MADE);
}

// special: VAR_RESULT gets the party slot of the first link, or PARTY_SIZE if
// it is not in the party; gStringVar1 its name when it is.
void AraunaBond_FindFirstLink(void)
{
    u32 i;

    gSpecialVar_Result = PARTY_SIZE;
    if (!FlagGet(FLAG_ARAUNA_FIRST_LINK_MADE))
        return;
    for (i = 0; i < PARTY_SIZE; i++)
    {
        if (GetMonData(&gPlayerParty[i], MON_DATA_SPECIES) != SPECIES_NONE
         && !GetMonData(&gPlayerParty[i], MON_DATA_IS_EGG)
         && GetMonData(&gPlayerParty[i], MON_DATA_PERSONALITY) == FirstLinkPersonality())
        {
            GetMonData(&gPlayerParty[i], MON_DATA_NICKNAME, gStringVar1);
            StringGet_Nickname(gStringVar1);
            gSpecialVar_Result = i;
            return;
        }
    }
}
