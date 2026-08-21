# Baia das Luzes — English interior surface

This pass completes a focused set of daily-life interiors that still exposed vanilla Lilycove or mixed legacy terminology after the city exterior, Ciro encounter and waterfront/HORIZON surfaces were already covered.

## Scope

42 reviewed text blocks across exactly 8 inherited maps:

- `LilycoveCity_House1`
- `LilycoveCity_House2`
- `LilycoveCity_House3`
- `LilycoveCity_House4`
- `LilycoveCity_MoveDeletersHouse`
- `LilycoveCity_CoveLilyMotel_1F`
- `LilycoveCity_CoveLilyMotel_2F`
- `LilycoveCity_PokemonCenter_1F`

The renderer owns text only. Geometry, objects, warps, scripts, trainer data and progression remain inherited.

## Daily-life direction

Baia das Luzes should feel like a real coastal city rather than a collection of plot terminals. The houses therefore stay small and domestic: partners, sleep, Pokeblocks, family, records, Contests and stories carried by the sea.

The writing supports Arauna's themes without making every resident an exposition device. Records can connect people without replacing lived experience; useful tools are framed around choice and responsibility; rumors are treated as claims that still need sources.

## Move Deleter

The inherited service remains mechanically identical. The visible language now makes the player's choice explicit: no move is removed without a clear decision. The existing protections for Eggs, one-move Pokemon and the last current Surf user remain untouched.

Preserved mechanics include:

- `IsSelectedMonEgg`
- `GetNumMovesSelectedMonHas`
- `MoveDeleterChooseMoveToForget`
- `IsLastMonThatKnowsSurf`
- `MoveDeleterForgetMove`
- `MAX_MON_MOVES`

## Luzes Inn

The old COVE LILY / Team Aqua / GAME FREAK surface is adapted without changing its event states.

On 1F, tourism reacts to HORIZON's waterfront activity without calling the operations hub a criminal "hideout" by default.

On 2F, the Pokedex-completion room becomes a regional survey team. The inherited diploma logic is preserved through `HasAllHoennMons` and `Special_ShowDiploma`.

The inherited Scott slot is visible as **SEU BENTO**, matching his established Arauna identity. Internal Scott state and flags remain unchanged:

- `VAR_SCOTT_STATE`
- `FLAG_MET_SCOTT_IN_LILYCOVE`

## Other preserved mechanics

- TM44 REST reward and `FLAG_RECEIVED_TM_REST`;
- House 3 random family activity state through `VAR_TEMP_1`;
- Kecleon cry/event;
- motel `FLAG_BADGE07_GET` and game-clear branches;
- Pokemon Center healing, respawn and Cable Club behavior;
- Lilycove Lady graphics/state logic.

## Renderer contract

`data/text/arauna/en/baia_luzes_interiors.json` is the plain UTF-8 bank.

`scripts/render_baia_luzes_interiors_en_checked.py` enforces:

- exact 8-section file contract;
- exact 42-label contract;
- one consecutive `.string` block per owned label;
- final `$` terminator rules;
- conservative 32-character visible-line validation, modeling dynamic placeholders as 16 characters;
- target-masked non-dialogue byte stability;
- per-map gameplay-token count preservation;
- removal of owned legacy visible residue such as `CONSORCIO HORIZONTE`, `HIDEOUT`, `GAME FREAK`, `SCOTT:`, `MOSSDEEP`, `SOOTOPOLIS` and `GAME BOY ADVANCE`;
- explicit Seu Bento identity checks in both inherited Scott text blocks.

## Validation

Synthetic validation passed:

1. `--check` — PASS, 42/42 blocks;
2. `--in-place` — PASS;
3. second `--check` — PASS;
4. second `--in-place` — byte-idempotent;
5. adjacent `.align` and sentinel label survived unchanged;
6. gameplay token counts survived unchanged.

The unrelated `artifact_tool` spreadsheet warmup emitted stderr during Python startup in this environment, but every renderer process returned exit code 0.

No GitHub Actions or Codespaces are required for this pass. No full GBA ROM toolchain build is claimed here.
