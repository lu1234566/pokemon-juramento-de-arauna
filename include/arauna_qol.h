#ifndef GUARD_ARAUNA_QOL_H
#define GUARD_ARAUNA_QOL_H

// The level the party is allowed to reach before the next boss. Derived from
// the boss parties themselves, not invented -- see src/arauna_qol.c.
u8 AraunaLevelCap(void);

// TRUE when this Pokemon has nothing more to gain: at the cap, or at MAX_LEVEL.
bool8 AraunaIsAtLevelCap(struct Pokemon *mon);

// Restores HP, PP and status for the whole party. Costs nothing.
void AraunaHealParty(void);

// How many of this species' egg moves the player could be taught, written into
// moves[] (caller supplies MAX_EGG_MOVES entries). Already-known moves are
// left out, so an empty result means there is nothing to teach.
u8 AraunaGetTeachableEggMoves(struct Pokemon *mon, u16 *moves);

// Specials, called from data/scripts/arauna_qol.inc.
void AraunaSpecial_GetLevelCap(void);
void AraunaSpecial_SetPartyToLevelCap(void);
void AraunaSpecial_HealParty(void);
void AraunaSpecial_EggMoveModeOn(void);
void AraunaSpecial_EggMoveModeOff(void);
void AraunaSpecial_ToggleInfiniteRepel(void);
void AraunaSpecial_ToggleShowIVs(void);

// Set by the script before the relearner screen opens, read by
// GetMoveRelearnerMoves so the same screen can serve egg moves.
void AraunaSetEggMoveMode(bool8 on);
bool8 AraunaGetEggMoveMode(void);

extern const u8 AraunaQol_EventScript_Menu[];

#endif // GUARD_ARAUNA_QOL_H
