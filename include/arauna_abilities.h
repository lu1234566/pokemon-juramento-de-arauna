#ifndef GUARD_ARAUNA_ABILITIES_H
#define GUARD_ARAUNA_ABILITIES_H

#include "constants/abilities.h"

// The Arauna abilities, gathered in one place instead of scattered as another
// thirty-five cases across the battle engine. Everything here is a pure
// decision: it reads the battlers and answers a question. The places that have
// to push a battle script -- switch-in, end of turn, contact -- stay where the
// engine already keeps that kind of code, next to the vanilla ability they
// behave like.

// TRUE for any of the thirty-five, which is how the AI and the gates tell an
// Arauna ability from an Emerald one without listing them again.
#define IS_ARAUNA_ABILITY(ability) ((ability) >= ABILITY_FOGO_LEAL && (ability) < ABILITIES_COUNT)

struct BattlePokemon;

// Applied to the finished base damage, just before the formula's +2. Covers
// every ability that multiplies damage, whether the holder is dealing it
// (LOYAL FLAME, ANCIENT FIRE, MASTER TIDE...) or taking it (SERPENT COIL,
// MOON VEIL, DRY SPELL).
s32 AraunaModifyDamage(s32 damage, struct BattlePokemon *attacker,
                       struct BattlePokemon *defender, u8 type,
                       u8 battlerIdAtk, u8 battlerIdDef);

// FIRST MOON, applied where Marvel Scale is, so it divides like a real stat.
u16 AraunaModifySpDefense(u16 spDefense, struct BattlePokemon *defender);

// Which battler's ability refuses this stat drop, or 0xFF for none. It can be
// the ally's: ETERNAL BOND guards the whole side, so the battler that answers
// is not always the one being lowered.
u8 AraunaStatDropGuard(u8 battler, u8 statId);

// TRUE for a sound move, by the list Soundproof uses.
bool8 AraunaIsSoundMove(u16 move);

bool8 AraunaBlocksFlinch(u16 ability);
bool8 AraunaBlocksBurn(u16 ability);

// RIVER SONG: sound moves cannot miss. The move list is Soundproof's.
bool8 AraunaMoveNeverMisses(u16 ability, u16 move);

// TURNED FEET: a status move from this battler moves before everything else.
bool8 AraunaMoveGetsPriority(u16 ability, u16 move);

// TUPA VOICE: an offensive electric or dragon move carries a chance to numb.
bool8 AraunaAddsParalysis(u16 ability, u8 moveType, u16 move);

#endif // GUARD_ARAUNA_ABILITIES_H
