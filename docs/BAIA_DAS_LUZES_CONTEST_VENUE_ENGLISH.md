# Baia das Luzes — Contest venue English surface

## Scope

This pass completes the local visible surface of the inherited Lilycove Contest venue without rewriting the shared Contest engine.

Owned surface: **53 reviewed blocks across 2 maps**.

- `LilycoveCity_ContestHall/scripts.inc`: 36 stage, contestant, judge, audience and sign blocks.
- `LilycoveCity_ContestLobby/scripts.inc`: 17 local lobby, artist, Ribbon and Pokeblock blocks.

The shared reception/rank/link-contest machinery in `data/scripts/contest_hall.inc` is deliberately outside ownership. Its functional copy remains generic and its event graph is not modified.

## Narrative direction

The venue is framed as a major Baia das Luzes performance space. Contest categories remain mechanically identical, while local dialogue puts more emphasis on partnership, preparation, timing and the Pokemon's comfort.

- SMARTNESS rewards preparation and reading the stage rather than caricaturing intelligence.
- BEAUTY remains a performance category without reducing worth to appearance.
- CUTENESS avoids judging people by looks and focuses on comfortable, expressive partnerships.
- Grooming dialogue explicitly recognizes when a Pokemon dislikes excessive fuss.
- Losing or choosing the wrong category is treated as feedback rather than humiliation.

The three visible stage signs identify the venue as **BAIA DAS LUZES**.

## Museum bridge

The inherited Contest Artist path remains intact. The local English surface now names the **BAIA DAS LUZES MUSEUM**, while preserving the player's yes/no choice over whether the painting is offered for exhibition.

No museum acceptance logic is changed. The artist still uses the inherited painting, Ribbon and patron-update machinery.

## Preserved mechanics

Target-masked byte equality preserves all non-owned source bytes. Representative token counts are also checked.

Hall:
- Smartness/Beauty/Cuteness MC and Judge object IDs;
- original facing/movement wiring.

Lobby:
- `VAR_LILYCOVE_CONTEST_LOBBY_STATE`;
- `SaveMuseumContestPainting`;
- `GiveMonArtistRibbon`;
- `GAME_STAT_RECEIVED_RIBBONS`;
- `FLAG_RECEIVED_POKEBLOCK_CASE`;
- `POKENEWS_BLENDMASTER`;
- all five Contest painting flags;
- `ClearLinkContestFlags`;
- `VAR_CONTEST_RANK` and `VAR_CONTEST_CATEGORY`.

Ranks, categories, entry validation, Link Contests, Pokeblock Case delivery, museum paintings and Ribbon progression therefore remain Emerald-compatible.

## Renderer contract

`render_baia_luzes_contest_venue_en_checked.py`:

- loads one UTF-8 JSON bank;
- requires exactly 36 Hall and 17 Lobby labels with the correct map-label prefixes;
- requires every target label to resolve exactly once in its source file;
- owns only consecutive `.string` bodies;
- supports legacy physical string continuations;
- models dynamic placeholders conservatively as 16 visible characters;
- rejects visible segments over 32 characters;
- requires a single final `$` terminator;
- masks every owned body and requires byte-identical non-dialogue structure;
- checks representative Contest/Painting/Ribbon/Pokeblock gameplay-token counts;
- is idempotent on already-rendered sources.

## Validation

Synthetic validation using the production body-span/masking code:

- 53/53 labels PASS;
- conservative width contract PASS;
- render PASS;
- target-masked structure equality PASS;
- gameplay-token count preservation PASS;
- second render byte-identical PASS;
- sentinel labels/directives outside owned text preserved.

No full GBA ROM toolchain compile was run. GitHub Actions and Codespaces were not required. PR #58 remains outside scope.
