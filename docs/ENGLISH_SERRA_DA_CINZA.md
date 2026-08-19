# Serra da Cinza — English restoration

Status: English-only migration slice.

This slice restores the full Serra da Cinza / Mt. Chimney faction confrontation as Arauna-authored English content in the official build.

## Conflict

- LUZIA uses the METEORITE as a BOND amplifier, intending to return memories taken by force;
- HORIZON argues that an uncontrolled return can violate consent just as erasure can;
- the REMEMBRANCERS are not ideologically uniform: some openly question whether forcing memories back is acceptable;
- OTACILIO asks the player to stop the uncontrolled release without pretending that this settles the larger conflict;
- after the battle, the dispute over the LIVING ARCHIVE remains unresolved.

## Machine surface

The old volcano device is visibly reframed as a BOND amplifier powered by the METEORITE. The original interaction, removal choice and item/state behavior are preserved.

## English terminology

Visible faction and system terms use:

- HORIZON;
- REMEMBRANCER / REMEMBRANCERS;
- BOND / BONDS;
- METEORITE.

Proper place names `SERRA DA CINZA` and `SERTAO DE DENTRO` remain canonical.

## Technical contract

The renderer covers 31 plot-visible text blocks only. It does not change trainer IDs or parties, event commands, movements, flags, variables, Meteorite handling, map geometry, warps or save data. The source map is backed up before the English build and restored on every exit path.
