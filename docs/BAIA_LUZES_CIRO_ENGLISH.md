# Baia das Luzes — Ciro confrontation in English

Status: English-only narrative continuation.

This slice rewrites the existing Lilycove rival encounter as Ciro's first direct confrontation after his search through the Memorial dos Nomes.

## Context

Ciro comes to BAIA DAS LUZES looking for answers about M'BOI and his father. HORIZON gives him a summary, but the material contains no names or signatures.

This is not an instant faction reversal. Ciro still believes moving forward matters and still rejects the idea that suffering should become a permanent identity. What changes is his willingness to accept institutional editing as treatment.

## Battle arc

The unchanged May/Brendan rival branches now surface the same Ciro voice:

- he challenges the player because he needs to know whether doubt made him weaker;
- before the battle he insists that discovering HORIZON's omissions does not erase who he is;
- after losing, he recognizes that anger is not a direction;
- he repeats that the past should not govern the future, but rejects anyone editing that past and calling it treatment;
- later progression branches show him reading M'BOI from multiple sides rather than relying only on HORIZON records.

The postgame branch keeps the same idea: surviving the crisis does not make the historical record complete.

## City surface

The city sign now identifies `BAIA DAS LUZES` in English and describes the modern waterfront as the location of HORIZON's operations hub.

## Technical contract

The renderer changes 19 text blocks:

- 9 internal May-branch rival texts;
- 9 internal Brendan-branch rival texts;
- 1 city sign.

All visible segments are at most 32 characters. Structural masking rejects non-dialogue edits.

Starter-dependent trainer IDs/parties, declined-battle flag, rival-met flag, player-gender routing, fly-out effect, object placement, warps, saves, geometry and art are untouched.
