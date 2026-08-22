# Baia das Luzes — Trainer Fan Club English surface

## Scope

This pass owns the inherited Lilycove Trainer Fan Club as one complete subsystem rather than treating the room and its TV output separately.

- 38 local Fan Club dialogue blocks in `data/maps/LilycoveCity_PokemonTrainerFanClub/scripts.inc`.
- 9 interview prompts/results in `data/text/tv.inc`.
- 6 `gTVTrainerFanClubSpecialTextXX` broadcast blocks in `data/text/tv.inc`.
- 53 reviewed blocks total.

## Narrative direction

The club remains a lively place where people compare TRAINERS, switch favorites, defend old favorites and react to the player's reputation. The dynamic fan mechanic is not turned into plot exposition.

The Arauna-specific layer is that reputation is treated as a story people tell rather than objective truth. Popularity, a TV score and a room full of agreement are not evidence by themselves. The interviewer's copy explicitly labels the player's answer as an opinion, and the broadcast presents its rating as a snapshot instead of a factual verdict.

Inherited Brawly-facing fan dialogue is visible as **ADEMAR**. Inherited Norman/father comparisons are visible as **ELIAS**, but avoid reducing the protagonist to a ranking against their father.

The TV special now addresses fans across **ARAUNA** instead of HOENN.

## Preserved mechanics

The renderer does not change event wiring or fan-state behavior. It preserves the counts of the following gameplay tokens:

- `VAR_LILYCOVE_FAN_CLUB_STATE`
- `FANCLUB_MEMBER1` through `FANCLUB_MEMBER8`
- `TryLoseFansFromPlayTime`
- `TryPutTrainerFanClubOnAir`
- `IsFanClubMemberFanOfPlayer`
- `GetNumFansOfPlayerInTrainerFanClub`
- `FLAG_HIDE_LILYCOVE_FAN_CLUB_INTERVIEWER`
- `FLAG_FAN_CLUB_STRENGTH_SHARED`
- `TVSHOW_FAN_CLUB_SPECIAL`
- `InterviewBefore`
- `EASY_CHAT_TYPE_FAN_QUESTION`
- `SCROLL_MULTI_POKEMON_FAN_CLUB_RATER`
- `PutFanClubSpecialOnTheAir`

The original fan acquisition/loss rules, member positions, interviewer visibility, Easy Chat answer, 0–100 rating and TV-show scheduling therefore remain Emerald-compatible.

## Renderer contract

`render_baia_luzes_fan_club_en_checked.py`:

- loads one UTF-8 JSON bank;
- requires exactly 38 `club` labels and 15 `tv` labels;
- owns only consecutive `.string` bodies beneath those exact labels;
- supports both `label:` and `label::` assembler labels;
- models dynamic placeholders conservatively as 16 visible characters;
- rejects visible segments above 32 characters;
- requires a single final `$` terminator per block;
- masks all owned bodies and demands byte-identical non-dialogue structure before/after rendering;
- checks the important Fan Club gameplay-token counts before/after rendering;
- accepts reapplication idempotently.

## Validation

Synthetic validation covered the same body-span algorithm used by the renderer:

- 53/53 labels found;
- rendering PASS;
- target-masked structure equality PASS;
- gameplay-token counts PASS;
- second render byte-identical PASS;
- sentinel labels/directives outside owned blocks preserved;
- conservative width validation PASS.

No full GBA ROM toolchain compile was performed for this pass. GitHub Actions and Codespaces are not required for it. PR #58 remains outside scope.
