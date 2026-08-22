# Baía das Luzes Museum — English Surface

## Scope

This pass completes the local visible English surface for the inherited Lilycove Museum while preserving the Emerald museum/Contest-painting progression.

Runtime files owned by the renderer:

- `data/maps/LilycoveCity_LilycoveMuseum_1F/scripts.inc`
- `data/maps/LilycoveCity_LilycoveMuseum_2F/scripts.inc`

The renderer owns exactly 43 consecutive `.string` bodies:

- 24 on 1F;
- 19 on 2F.

No map geometry, movement, warp, metatile, painting, Contest, Ribbon or decoration logic is owned.

## Visible identity

The building is presented to the player as **BAIA DAS LUZES MUSEUM**.

The ground floor is framed around art, coastal history and provenance rather than treating every old object as unquestioned fact. Labels distinguish what is known from what is inferred:

- an imagined legendary-Pokémon painting is explicitly identified as an artist's interpretation;
- an old coastal painting can have a missing attribution without inventing one;
- an unreadable tablet remains meaningful evidence even though no complete reading survives;
- a replica is identified as a replica rather than presented as the original object.

This supports Arauna's themes of memory and record-keeping without turning the museum into a branch of either HORIZON or the Living Archive.

## Contemporary gallery

The second floor remains the inherited five-painting Contest gallery.

Its Arauna-facing principle is explicit: **permission comes before display**. The curator asks the player to speak with the artist and states that the museum displays nothing there without the maker's permission.

Completing the gallery still means obtaining the same five inherited Contest paintings. The text treats them as five recorded moments rather than five complete or objective accounts.

## Preserved mechanics

The checked renderer masks only owned text bodies and requires all remaining bytes in each source file to remain identical.

Representative protected tokens include:

### 1F

- `MULTI_VIEWED_PAINTINGS`
- `VAR_FACING`
- `MAP_LILYCOVE_CITY_LILYCOVE_MUSEUM_2F`
- curator object/movement wiring
- the inherited warp to 2F

### 2F

- `FLAG_COOL_PAINTING_MADE`
- `FLAG_BEAUTY_PAINTING_MADE`
- `FLAG_CUTE_PAINTING_MADE`
- `FLAG_SMART_PAINTING_MADE`
- `FLAG_TOUGH_PAINTING_MADE`
- `VAR_LILYCOVE_MUSEUM_2F_STATE`
- `CountPlayerMuseumPaintings`
- `DECOR_GLASS_ORNAMENT`
- `FLAG_RECEIVED_GLASS_ORNAMENT`
- all five `CONTEST_WINNER_MUSEUM_*` display IDs

Therefore the five paintings, museum progression, curator state, painting metatiles and Glass Ornament reward remain Emerald-compatible.

## Renderer contract

`render_baia_luzes_museum_en_checked.py` validates:

- exact bank sections (`1f`, `2f`);
- exact 24 + 19 label set;
- one occurrence of every target label;
- final `$` termination;
- no early `$` terminators;
- assembler-safe text;
- conservative 32-visible-character segments using a 16-character placeholder model;
- target-masked byte equality outside owned `.string` bodies;
- gameplay-token count preservation;
- visible `BAIA DAS LUZES MUSEUM` identity;
- 2F permission/provenance language.

The renderer is designed to be idempotent: already-rendered bodies are valid input and render to the same output.

## Build integration

The official English-only build backs up/restores both museum map scripts transactionally and invokes the checked museum renderer alongside the other Baía das Luzes surface renderers.

No rendered `scripts.inc` output is committed.

## Out of scope

- shared Contest engine;
- Contest ranks/categories;
- Ribbon logic;
- map geometry or metatiles;
- painting flags/state;
- museum reward logic;
- save format;
- PR #58.

No GitHub Actions or Codespaces are required for this text-surface pass. A full GBA ROM toolchain compile is not claimed by this document.