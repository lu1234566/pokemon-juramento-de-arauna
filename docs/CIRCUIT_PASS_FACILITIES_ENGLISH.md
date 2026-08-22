# Battle Circuit — cross-facility CIRCUIT PASS terminology

## Scope

This pass closes remaining visible `FRONTIER PASS` terminology in six inherited Battle Circuit facilities after the public reception established **CIRCUIT PASS**.

Exactly **17 reviewed text blocks** are owned:

- BATTLE DOME lobby: 1;
- BATTLE PALACE battle room: 4;
- BATTLE ARENA battle room: 4;
- BATTLE FACTORY battle room: 3;
- BATTLE PIKE normal room: 3;
- BATTLE PYRAMID top: 2.

The pass is deliberately limited to record-battle prompts and Circuit Master/Symbol recognition messages.

## Visible continuity

The following inherited leader and Symbol identities remain intact:

- SPENSER / PALACE MAVEN / Spirits Symbol;
- GRETA / ARENA TYCOON / Guts Symbol;
- NOLAND / FACTORY HEAD / Knowledge Symbol;
- LUCY / PIKE QUEEN / Luck Symbol;
- BRANDON / PYRAMID KING / Brave Symbol;
- BATTLE DOME facility identity and record flow.

Only the player-facing pass name changes to **CIRCUIT PASS**.

## Preserved mechanics

No facility challenge engine is redesigned. The checked renderer preserves all non-dialogue bytes outside owned strings and representative mechanic tokens per map, including:

- Dome save, win-streak, BP and record-battle flow;
- Palace Brain status, streak, special battle, record-disabled state and Spirits Symbol award;
- Arena save/record flow, Greta Brain path and Guts Symbol award;
- Factory rental-battle special, streak/swap state, Noland Brain path and Knowledge Symbol award;
- Pike room generation/battles, Lucy Brain status, win streak and Luck Symbol award;
- Pyramid save/challenge state, Brandon special battle and Brave Symbol award;
- `frontier_getsymbols`, `frontier_givesymbol` and `MUS_OBTAIN_SYMBOL` where used;
- battle outcomes, movements, warps, object IDs and saves.

Internal `FRONTIER_*`, Brain and facility identifiers remain untouched.

## Renderer guarantees

`scripts/render_circuit_pass_facilities_en_checked.py` enforces:

- exact six-section JSON contract;
- exact 1 + 4 + 4 + 3 + 3 + 2 label ownership;
- final `$` terminator discipline;
- conservative 32-visible-character limit;
- masked byte equality outside owned `.string` bodies;
- per-facility gameplay-token count preservation;
- rejection of `FRONTIER PASS` inside owned output;
- required CIRCUIT PASS plus facility-specific leader/Symbol context.

## Build integration

The six source maps join the transactional Arauna English overlay and the checked renderer runs after the Battle Tower Circuit Pass renderer.

No rendered `scripts.inc` output is committed.

## Build status

No full GBA toolchain compile is claimed for this text-overlay pass. GitHub Actions and Codespaces are not used. Legacy PR #58 remains outside scope.
