# Emerald residue cleanup — lot 4

This lot removes the remaining player-facing Steven identity from the PokéNav Match Call path assigned to Seu Bento.

## Visible text corrected

- all seven `MatchCall_Text_Steven*` messages are rewritten as Seu Bento dialogue in PT-BR;
- the visible PokéNav contact name changes from `STEVEN` to `SEU BENTO`;
- the visible contact description changes from `HARD AS ROCK` to `GUARDA NOMES`.

## Progression preserved

The existing `sStevenTextScripts` table, Match Call indices and availability flags are not changed. The same seven call slots therefore unlock at the same campaign states as before; only their player-facing identity and dialogue change.

## Verification scope

The deterministic Match Call cleanup verifies seven exact shared-text blocks and two exact visible constants. Generated source changes are limited to `data/text/match_call.inc` and `src/strings.c`.

## Safety boundary

Internal Emerald symbols such as `sStevenTextScripts`, `sStevenMatchCallHeader`, `FLAG_REGISTERED_STEVEN_POKENAV` and `MatchCall_Text_Steven*` remain intact as implementation wiring. No maps, flags, variables, trainer data, save structures or progression logic are changed.
