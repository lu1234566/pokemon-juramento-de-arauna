#ifndef GUARD_ARAUNA_BOND_H
#define GUARD_ARAUNA_BOND_H

// A first link that trusts the player this much holds on once per battle.
#define ARAUNA_BOND_HOLD_FRIENDSHIP 220

void AraunaBond_TryHoldOn(u8 battler);
bool8 AraunaBond_TakeMessage(void);

void AraunaBond_ReadSelected(void);
void AraunaBond_MakeFirstLink(void);
void AraunaBond_FindFirstLink(void);

#endif // GUARD_ARAUNA_BOND_H
