# Battle Circuit Masters — English identity surface

This pass replaces the last visible Emerald Frontier Brain identities while preserving the complete inherited Battle Frontier battle/progression machinery.

## Visible Circuit Masters

| Internal Emerald slot | Arauna visible name | Facility focus |
| --- | --- | --- |
| `TRAINER_ANABEL` | **MAIRA** | Battle Tower — adaptation and consistency |
| `TRAINER_TUCKER` | **DARIO** | Battle Dome — brackets, timing and public pressure |
| `TRAINER_NOLAND` | **NILO** | Battle Factory — unfamiliar/rental teams |
| `TRAINER_LUCY` | **IARA** | Battle Pike — uncertainty and judgment under chance |
| `TRAINER_GRETA` | **RITA** | Battle Arena — commitment under three-turn judgment |
| `TRAINER_SPENSER` | **AMARO** | Battle Palace — trust and Pokemon autonomy |
| `TRAINER_BRANDON` | **TADEU** | Battle Pyramid — endurance and route/resource judgment |

All seven inherited Frontier Brain trainer classes display as **CIRCUIT MSTR** in battle UI. In prose, legacy titles such as `SALON MAIDEN`, `DOME ACE` and `PIKE QUEEN` are reduced to **MASTER** so the facilities retain their own names while the people belong to one coherent Circuit Masters system.

## Battle-result voice

`data/text/arauna/en/circuit_masters.json` owns exactly **28** result quotes: Silver/Gold win and defeat speech for each of the seven Masters.

The writing differentiates each facility without changing its rules:

- MAIRA reads streaks as adaptation rather than raw dominance.
- DARIO treats crowds and tournament brackets as pressure, not proof.
- NILO focuses on learning the rental team actually available.
- IARA distinguishes chance from the judgment made after chance acts.
- RITA emphasizes clarity and commitment inside Arena judging.
- AMARO frames autonomy as partnership rather than obedience.
- TADEU treats endurance as resource and route judgment, not stubbornness.

## Checked renderer

`scripts/render_circuit_masters_en_checked.py` owns four narrow surfaces:

1. `.trainerName` in the exact seven Frontier Brain entries of `src/data/trainers.h`;
2. the exact seven Frontier Brain class display strings in `src/data/text/trainer_class_names.h`;
3. the exact 28 result-quote labels in `data/text/frontier_brain.inc`;
4. old Brain names/titles only inside `.string` payloads of twelve selected Battle Circuit map scripts.

Internal labels such as `BattleAnabel`, `ReadyForTuckerSilver`, `TRAINER_LUCY`, `TRAINER_CLASS_PIKE_QUEEN` and all `FRONTIER_*` identifiers are intentionally untouched.

The renderer validates the JSON section/key sets, trainer/class lengths, 32-character quote segments, final `$` termination, one exact trainer/class anchor per target, non-dialogue byte stability, and absence of the seven old visible names in the owned map string surfaces. It is designed to be idempotent.

## Preserved mechanics

This pass does **not** alter:

- Trainer IDs or opponent IDs;
- trainer pictures, object graphics or animations;
- teams, moves, held items, AI or battle modes;
- Silver/Gold streak thresholds;
- `frontier_getbrainstatus`, `frontier_isbrain`, `frontier_givesymbol` or Symbol flags;
- Battle Point rewards;
- recorded battles, saves, warps or facility state;
- facility order, maps or layouts.

The existing Emerald character sprites remain as functional visual slots for this text/identity pass. Replacing their art, if desired, is a separate graphics task and must not be coupled to battle logic.

## Build integration

The official English build backs up every source file this renderer can touch, applies the renderer after the existing Battle Circuit UI/pass overlays, compiles, and restores the original sources on exit or interruption. No rendered map source is committed.

No full GBA toolchain compile is claimed by this document. GitHub Actions and Codespaces are outside this pass, and legacy PR #58 remains untouched.
