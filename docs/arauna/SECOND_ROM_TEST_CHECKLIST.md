# Second ROM test checklist

This pass validates the first English-only playable route of **Pokémon: Juramento
de Arauna**, from a new game through the Uivo Badge. Campaign maps in this build
reuse existing Pokémon Emerald layouts and objects; do not judge them as final
custom maps.

## Build contract

- Build with `make ARAUNA_LANGUAGE=ENGLISH -j$(nproc) -O all`.
- Confirm the local output is `pokeemerald-en.gba`.
- Do not commit or upload the ROM, save files, screenshots containing licensed
  ROM data, or patches to the repository.
- Start from a **new save**. Old saves are outside this test's compatibility
  contract.
- Record the commit SHA, emulator name/version and platform before playing.

## 1. New game and research center

- [ ] Confirm the opening, menus and all player-facing story text are in English.
- [ ] Confirm the player reaches the Arauna Research Center without a blocked
      warp, broken collision or black screen.
- [ ] Save before choosing a starter so the three branches can be tested.
- [ ] Choose Pimpau (Treecko slot) and confirm the expected Fakemon art, name,
      type, level 5 data and summary screen.
- [ ] In separate save copies, repeat for Caramelo (Torchic slot) and Querô
      (Mudkip slot).
- [ ] Confirm Dr. Maia lets the player keep the chosen starter.
- [ ] Immediately after confirmation, verify the Bag contains exactly **999 Rare
      Candies**.
- [ ] Talk to Dr. Maia repeatedly and confirm the quantity never exceeds 999.
- [ ] Verify Pokédex access is enabled and the starter is recorded in the correct
      Arauna slot.
- [ ] Save, reset and reload; confirm the starter, Pokédex and candy quantity
      persist.

### Bag-full recovery

This edge case is optional unless a debug save is available.

- [ ] Fill the medicine pocket before starter confirmation.
- [ ] Confirm Maia explains that the test supplies could not be added.
- [ ] Free one medicine slot and talk to Maia again.
- [ ] Confirm all 999 Rare Candies are delivered once and cannot be duplicated.

## 2. Opening route and First Link

- [ ] Follow Nilo through the reused Emerald map shells.
- [ ] Check every entrance, exit, ledge, stair, sign and map connection used by
      the critical path.
- [ ] Enter and leave the Mist Route in both directions.
- [ ] Trigger the affected Pokémon scene and complete the required rescue.
- [ ] Complete the capture onboarding and verify a caught Fakemon enters the
      party or PC normally.
- [ ] Intentionally white out once; confirm recovery returns to a safe healing
      point without corrupting story progress.
- [ ] Save and reload before and after the First Link chamber.
- [ ] Test each Bond choice from separate save copies and verify that only the
      selected state persists.
- [ ] Open the Pokédex in the Research Center and verify numbering, seen/caught
      state, descriptions and the relevant front/back artwork.

## 3. Porto das Redes and Maré Badge

- [ ] Reach the Route 109 landing and confirm the reused beach layout has no
      trapping collision or invalid connection.
- [ ] Enter reused Slateport areas and verify every campaign warp.
- [ ] Meet Zila and confirm her dialogue advances only once.
- [ ] Trigger the Iaraco sequence and verify its restored state survives a
      save/reload.
- [ ] Complete the chosen-legend and Iara-Mãe testimony events.
- [ ] After the testimony, start the mandatory TIDE VIGIL battle against Zila.
- [ ] Lose once and confirm the testimony remains complete, the badge is not
      awarded and talking to Zila retries only the battle.
- [ ] Win the TIDE VIGIL and receive the **Maré Badge** once.
- [ ] Confirm backtracking does not repeat the boss reward or regress flags.
- [ ] Check encounter levels, healing access, money and item availability before
      using Rare Candies; then record the same fights after controlled leveling.

## 4. Serra do Uivo and Uivo Badge

- [ ] Reach reused Fallarbor Town and Route 114 without a broken connection.
- [ ] Learn the initial Libras signs and confirm the state persists.
- [ ] Complete the hermit communication event.
- [ ] Traverse the reused Meteor Falls areas, checking warps, stairs, water
      boundaries and return paths.
- [ ] Trigger the desaturated Lobisomem encounter.
- [ ] Use the Libras story interaction and confirm the Lobisomem is calmed once.
- [ ] After calming Lobisomem, start the mandatory TRIAL OF ECHOES battle.
- [ ] Lose once and confirm Lobisomem remains calm, the badge is not awarded and
      talking to the hermit retries only the battle.
- [ ] Win the TRIAL OF ECHOES and receive the **Uivo Badge** once.
- [ ] Save, reset and reload after the badge; verify both badges and story states
      remain correct.
- [ ] Backtrack to Porto and the Research Center to check that earlier NPCs and
      map gates remain in their completed states.

## 5. Rare Candy progression checks

Use the candies as test instrumentation, not as the expected difficulty curve.

- [ ] Record each starter's stats and moves before leveling.
- [ ] Raise each starter one level at a time around every evolution threshold.
- [ ] Confirm evolution species, art, types, abilities, learnsets and Pokédex
      registration.
- [ ] Spot-check at least one captured Fakemon from every accessible habitat.
- [ ] Cancel one evolution, level again and verify the evolution can be retried.
- [ ] Check move-learning with a full moveset, including replace and decline
      paths.
- [ ] Confirm the quantity decreases correctly and remains valid after
      save/reload.
- [ ] Do not use the candy-assisted results as balance approval; replay major
      fights at natural levels before reporting difficulty.

## 6. QoL regression checks

- [ ] Verify indoor running, fast HP/EXP bars, Bag organization and automatic
      Repel renewal.
- [ ] Verify reusable TMs, IV/EV grades, alphabetical Move Reminder entries,
      pre-evolution moves and summary-screen renaming.
- [ ] Confirm global EXP Share remains unavailable.
- [ ] Confirm DexNav remains unavailable.
- [ ] Confirm nature/ability services, portable PC and fast travel remain
      unavailable in this build.

## 7. Report template

Copy this block into the test report for every issue:

```text
Build commit:
Emulator and version:
Platform:
New save: yes/no
Location:
Story stage / badges:
Starter:
Steps to reproduce:
Expected:
Observed:
Reproducibility:
Save available privately: yes/no
Screenshot or short recording available privately: yes/no
Severity: blocker / major / minor / cosmetic
```

The second test is complete only when a new save can reach the Uivo Badge, save
and reload there, and backtrack without a progression blocker. The 999 Rare
Candies are temporary test supplies and must be removed or explicitly gated
before a public release.
