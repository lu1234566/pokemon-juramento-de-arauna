# Hall of Fame Arauna system-UI cleanup

The scripted finale is being rewritten around Amalia/Anahi/Ciro, but the global Hall of Fame interface still switches back to English immediately afterward through five `src/strings.c` constants.

## Prepared visible values

- `Welcome to the HALL OF FAME!` -> `SALA DA FAMA DE ARAUNA!`
- saving warning -> `SALVANDO… / NAO DESLIGUE.`
- corrupted-record warning -> Portuguese Sala da Fama wording
- `HALL OF FAME No.` -> `SALA DA FAMA No.`
- `LEAGUE CHAMPION! / CONGRATULATIONS!` -> `LIGA CONQUISTADA! / PARABENS!`

The existing Anahi Pokédex rating string is already localized and is intentionally left untouched.

## Safety boundary

Only five exact player-facing string values in `src/strings.c` are targeted. The backing `gText_*` symbols, Hall of Fame record data, save calls, game-clear state, trainer data, graphics, flags and progression remain unchanged.

This is preparation-only while GitHub Actions quota is exhausted. Activate together with or immediately after the Amalia finale surface from the newest canonical main; Codespaces remains last resort.
