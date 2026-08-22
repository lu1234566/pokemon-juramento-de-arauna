# Baía das Luzes Harbor + Event Tickets — English Surface

## Scope

This pass completes the visible post-game ferry surface that starts at the inherited Lilycove harbor and follows the special event-ticket routes.

Owned runtime text sources:

- `data/maps/LilycoveCity_Harbor/scripts.inc`
- `data/text/event_ticket_1.inc`
- `data/text/event_ticket_2.inc`

The checked renderer owns exactly 25 `.string` bodies:

- 11 Harbor blocks;
- 6 event-ticket bank 1 blocks;
- 8 event-ticket bank 2 blocks.

It also changes one exact visible destination declaration in `src/strings.c`:

- `gText_BattleFrontier`: `BATTLE FRONTIER` → `BATTLE CIRCUIT`.

The existing Porto do Sal harbor renderer independently changes `gText_LilycoveCity` and `gText_SlateportCity` to `BAIA DAS LUZES` and `PORTO DO SAL`; the three declarations are disjoint and intentionally compose in the official build.

## Bug fixed

Before this pass, `LilycoveCity_Harbor_Text_MayISeeYourTicket` contained unrelated Portuguese Ciro/DESENCANTO dialogue even though the label is the ferry attendant's ticket prompt.

The Harbor now restores the correct interaction surface:

- attendant asks for the ticket;
- ticket validation leads to destination selection;
- PORTO DO SAL is the regular coastal destination;
- BATTLE CIRCUIT is the post-game battle destination;
- return dialogue names BAIA DAS LUZES.

No Ciro dialogue belongs to or survives in this owned Harbor surface.

## Special tickets

The inherited Eon Ticket, Aurora Ticket, Mystic Ticket and Old Sea Map mechanics remain unchanged.

The English rewrite removes stale Lilycove/Slateport naming and reframes distant-island travel as uncertain navigation rather than comic pirate dialogue.

The inherited Briney-visible Old Sea Map intervention is presented as **SEU BENTO**. This changes only player-facing identity/text; the internal object/local-ID names remain untouched.

Seu Bento's position is deliberately cautious: an old map is evidence of a possible route, not a guarantee that the route or destination is understood.

Southern Island inscriptions and the Faraway Island fading inscription are not owned by this renderer when they are already useful and compatible with Arauna's themes.

## Mechanics preserved

The checked renderer masks only target text bodies and requires the remainder of each owned text file to stay byte-identical.

For the Harbor script it additionally preserves token counts for the critical ferry state machine, including:

- `FLAG_SYS_GAME_CLEAR`;
- all four event-island enable flags;
- EON/AURORA/MYSTIC ticket and OLD SEA MAP item checks;
- all four shown-ticket flags;
- `ScriptMenu_CreateLilycoveSSTidalMultichoice`;
- `GetLilycoveSSTidalSelection`;
- all special-island warp destinations;
- `MAP_SS_TIDAL_CORRIDOR`;
- `MAP_BATTLE_FRONTIER_OUTSIDE_WEST`;
- `VAR_SS_TIDAL_STATE` / `SS_TIDAL_BOARD_LILYCOVE`;
- ferry and Seu Bento/Briney internal object IDs;
- `Common_EventScript_FerryDepart`.

Therefore ticket eligibility, one-time presentation state, destination selection, boarding movements and all inherited warps remain mechanically unchanged.

## Renderer contract

`render_baia_luzes_harbor_tickets_en_checked.py` validates:

- exact `harbor`, `ticket1`, `ticket2` bank sections;
- exact 11 + 6 + 8 label sets;
- exactly one occurrence of every target label;
- final `$` and no premature terminators;
- assembler-safe text;
- conservative 32-visible-character segments using a 16-character placeholder model;
- target-masked byte equality outside owned text bodies;
- critical Harbor gameplay-token counts;
- removal of stale player-facing `CIRO`, `DESENCANTO`, `LILYCOVE`, `SLATEPORT`, `BRINEY:` and `CAPT. BRINEY` from the owned blocks;
- required visible identities `BAIA DAS LUZES`, `PORTO DO SAL`, `BATTLE CIRCUIT`, and `SEU BENTO`;
- exact/idempotent replacement of the single global `gText_BattleFrontier` declaration.

## Deliberate non-ownership

This pass does **not**:

- rename internal `LILYCOVE` symbols, map constants or local IDs;
- change ticket items or flags;
- change event-island availability;
- change ferry menus or selection indices;
- change any warp;
- activate the old Portuguese `render_arauna_frontier_ui.py`;
- rewrite the Battle Circuit facilities;
- alter saves or progression;
- touch PR #58.

No GitHub Actions or Codespaces are required for this surface pass. A full GBA ROM toolchain compile is not claimed here.