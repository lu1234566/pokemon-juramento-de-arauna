# Legendary & Mythical Events — Arauna

Status: **Wave 1 implemented on `feat/legendary-mythical-events`**.

The event pass deliberately reuses Emerald's mature static-encounter machinery
where it fits, but the visible species identity follows the Arauna engine
mapping, not the vanilla constant name.

## Wave 1 — implemented

Ten of the 31 special species now have concrete acquisition events:

- **Guaraciana #329 / Jaciana #330** — the post-League roaming pair. The TV
  report is rewritten around the sun-red / moon-blue sightings. The chosen one
  roams at Lv.55; the opposite member appears on Southern Island, using the two
  custom Latias/Latios overworlds that were already built specifically for
  Guaraciana and Jaciana.
- **Verdejante #338** — Ancient Tomb, Lv.60. The old Registeel shrine is now an
  Arauna relic seal; the internal Registeel flags remain only for save
  compatibility.
- **Terraão #342** — Desert Ruins, Lv.60, through the old Regirock seal.
- **Marulho #344** — Island Cave, Lv.60, through the old Regice seal.
- **Estrelinha #347** — Birth Island, Lv.65. Solving the triangle breaks it into
  light and directly awakens Estrelinha; no Deoxys sprite is shown.
- **Iemanjã #382** — Marine Cave, Lv.70. The stale Kyogre overworld is kept
  hidden; the player senses the presence before battle.
- **Oxumará #383** — Terra Cave, Lv.70. Same treatment, avoiding stale Groudon
  art.
- **Curupixel #384** — Faraway Island, Lv.65. The hide-and-seek encounter is
  retained because the Mew object slot already carries Curupixel's Arauna
  palette/art wiring.
- **Arauá #386** — Sky Pillar Top, Lv.75. The summit object and music were
  already Arauá-specific; the stale battle target is corrected from the
  Rayquaza engine slot to Arauá's actual `SPECIES_DEOXYS` slot.

## Engine correction

`BattleSetup_StartLegendaryBattle` previously let its `default` case fall
through to Groudon. That meant any newly scripted legend in an ordinary engine
slot silently gained Groudon's transition/flags. The default is now a true
generic legendary transition.

The old comment/theme routing also incorrectly treated `SPECIES_RAYQUAZA` as
Arauá. The current canonical mapping is:

- `SPECIES_RAYQUAZA` = **#384 Curupixel**
- `SPECIES_DEOXYS` = **#386 Arauá**

Arauá now receives `MUS_ARAUNA_ARAUA_BATTLE`; Curupixel uses the shared
legendary theme.

## Save compatibility

Wave 1 does **not** expand the save layout. Native anchor flags such as
`FLAG_DEFEATED_REGIROCK` remain internal state keys even when their visible
encounter is now an Arauna species. Renaming those flags would add risk without
changing anything the player sees.

The remaining 21 species and their intended anchors are tracked in
`docs/arauna/ARAUNA_LEGENDARY_MYTHICAL_EVENTS.csv`. New persistent flags will
be allocated from proven-unused flag aliases only when each event is actually
implemented.

## Art rule

A vanilla legendary sprite is never shown merely because its event code is
convenient. If the slot has no confirmed Arauna overworld, the event uses a
relic, environmental presence, altar, or puzzle trigger until dedicated art is
available. This is why Marine Cave and Terra Cave hide their inherited
Kyogre/Groudon objects and Birth Island does not spawn Deoxys.
