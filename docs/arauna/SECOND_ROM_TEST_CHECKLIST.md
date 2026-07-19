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

## 1. New game, Vila Amanhecer and starter choice

- [ ] Confirm a new save opens inside Dona Zila's house, not inside Emerald's
      moving truck.
- [ ] Confirm the opening, menus and all player-facing story text are in English.
- [ ] Confirm the night arrival of Prof. Anahi, the gray figure and the next
      morning are presented without a black screen or blocked input.
- [ ] Try to leave before choosing; confirm Dona Zila stops the player.
- [ ] Interact once with Pimpau, Caramelo and Quero and confirm all three feeding
      scenes play exactly once.
- [ ] Confirm no starter can be selected before all three have been fed.
- [ ] Save after feeding all three so the three choice branches can be tested.
- [ ] Choose Pimpau (Treecko slot) and confirm the explicit YES/NO prompt,
      expected Fakemon art, name, type, level 5 data and summary screen.
- [ ] In separate save copies, repeat for Caramelo (Torchic slot) and Quero
      (Mudkip slot).
- [ ] Confirm Dona Zila acknowledges that the chosen partner already selected
      the player during the night.
- [ ] Confirm Prof. Anahi integrates the Census pages into Dona Zila's notebook.
- [ ] Immediately after confirmation, verify the Bag contains exactly **999 Rare
      Candies**.
- [ ] Talk to Prof. Anahi repeatedly and confirm the quantity never exceeds 999.
- [ ] Open POKéMON, select the starter and confirm the English **LEVEL CAP**
      action is present.
- [ ] Verify Pokedex access is enabled and the starter is recorded in the correct
      Arauna slot.
- [ ] Exit the house and confirm the popup reads **Vila Amanhecer**, never
      Littleroot Town.
- [ ] Confirm any reachable reused Oldale shell is identified as **Amanhecer
      Post**, never Oldale Town.
- [ ] Save, reset and reload; confirm the starter, Pokedex and candy quantity
      persist.

### Bag-full recovery

This edge case is optional unless a debug save is available.

- [ ] Fill the medicine pocket before starter confirmation.
- [ ] Confirm Prof. Anahi explains that the test supplies could not be added.
- [ ] Free one medicine slot and talk to Prof. Anahi again.
- [ ] Confirm all 999 Rare Candies are delivered once and cannot be duplicated.

## 2. Opening route and First Link

- [ ] Follow Ciro through the reused Emerald map shells.
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

## 5. Mandatory-boss LEVEL CAP QoL

The current target must always equal the highest-level Pokémon owned by the next
mandatory story boss:

| Story position | Next boss | Target |
|---|---|---:|
| Before First Link | Ciro — Lv. 7 | 7 |
| After Ciro | Consortium Agent — Lv. 12 | 12 |
| After the Agent | Dona Celina — Lv. 17 | 17 |
| After the Maré Badge | Hermit — Lv. 27 | 27 |

- [ ] Before fighting Ciro, select one party member and use **LEVEL CAP**; confirm
      only that Pokémon rises to Lv. 7.
- [ ] Confirm the level-up stat pages appear and every move learned across the
      skipped levels is offered in order.
- [ ] Cross an evolution threshold with **LEVEL CAP** and confirm the normal
      evolution scene and Pokédex registration occur.
- [ ] Select a Pokémon already at or above the target and confirm its level and
      EXP are not reduced or changed.
- [ ] Use Rare Candies at the target and confirm they cannot raise a Pokémon
      above the current cap.
- [ ] Defeat Ciro and confirm the target changes to Lv. 12 without requiring a
      badge or save reload.
- [ ] Defeat the Consortium Agent and confirm the target changes to Lv. 17.
- [ ] Win the Maré Badge and confirm the target changes to Lv. 27.
- [ ] Save and reload at each milestone; confirm the target is reconstructed
      from story state.
- [ ] Win the Uivo Badge and confirm **LEVEL CAP** is no longer offered because
      the next mandatory boss is not implemented in this vertical slice.

## 6. Rare Candy progression checks

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

## 7. QoL regression checks

- [ ] Verify indoor running, fast HP/EXP bars, Bag organization and automatic
      Repel renewal.
- [ ] Verify reusable TMs, IV/EV grades, alphabetical Move Reminder entries,
      pre-evolution moves and summary-screen renaming.
- [ ] Confirm **LEVEL CAP** never affects unselected party members and never
      consumes a Rare Candy.
- [ ] Confirm global EXP Share remains unavailable.
- [ ] Confirm DexNav remains unavailable.
- [ ] Confirm nature/ability services, portable PC and fast travel remain
      unavailable in this build.

## 8. Report template

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
