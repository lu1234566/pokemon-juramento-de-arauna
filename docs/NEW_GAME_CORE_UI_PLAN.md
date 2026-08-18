# New-game core UI localization

Professora Anahi already owns the rewritten opening speech, but a few global constants around that same flow still switch back to English before the player reaches Vila Amanhecer.

## Prepared visible values

- `NEW GAME` -> `NOVO JOGO`
- `CONTINUE` -> `CONTINUAR`
- `OPTION` -> `OPCOES`
- character-creation `BOY` / `GIRL` -> `MENINO` / `MENINA`
- global Pokémon introduction sentence -> Portuguese
- starter confirmation -> `Escolher este POKéMON?`

Mystery Gift/Event and broader system menus are deliberately outside this focused lot so they can be audited separately instead of broadening the startup change without execution.

## Safety boundary

Only seven exact player-facing values in `src/strings.c` are targeted. The inherited `gText_Birch*` symbol names, character-creation branches, player gender values, starter species, selection logic, save initialization, menu indexes and progression remain untouched.

This is preparation-only while GitHub Actions quota is exhausted. Activate from the newest canonical main through the deterministic cleanup sequence; Codespaces remains last resort.
