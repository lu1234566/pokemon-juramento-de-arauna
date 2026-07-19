# Approved Prologue and Porto Restructure

Status: approved for implementation on 2026-07-18.

This document converts the approved narrative direction into an implementation
contract. It covers the English-first runtime. PT-BR remains the canonical
writing source and must retain matching text labels when both language banks
exist.

## Approved decisions

1. **Visible east exit** — Vila Amanhecer uses the existing walkable opening
   at the east edge of its reused layout. The misplaced north warp is removed.
2. **First Link ruins deferred** — the First Link Ruin, Champion memory, and
   generic Bond trial leave the main vertical-slice route. Their maps are kept
   for a later arc, with the Ruins of the Missions as the preferred reuse.
3. **local Tide Storyteller** — a named widow from Porto das Redes becomes the
   guardian and boss of the House of Tide. Dona Zila remains the protagonist's
   mentor and participates through story nights and calls.

No map or layout will be created from scratch. Existing Emerald layouts,
tilesets, interiors, and route shells are reassigned or lightly rearranged.

## Checkpoint status

- [x] Foundation: visible east exit, Ciro identity and conditional starter
  parties, Poochyena placeholder removal, and Porto handoff.
- [x] Playable house night: the player meets Zila, Anahi, and all three
  rescued partners before the gray-figure watch and dawn transition.
- [ ] Expanded Vila Amanhecer NPC exploration and capture tutorial.
- [x] Explore-before-Ciro route pacing and scholarship departure scene.
- [x] First Link removal from the critical path; its maps remain reserved.
- [x] Porto investigation, Agent confrontation, restoration, and Tide Vigil:
  four evidence nodes, Dona Celina, prose-only Iaraco trace, and save-safe stages.
- [ ] First approved in-ROM art batch.

## Target player loop

Every House of Story follows this order:

1. learn the place through exploration and NPC testimony;
2. gather incomplete or conflicting evidence;
3. enter a field area and witness the local Desencanto;
4. restore the threatened story;
5. prove readiness in a battle against the human guardian;
6. receive the Badge, notebook chapter, and visible world-state change.

A House battle is the conclusion of its mission, not a Gym battle hidden behind
different terminology.

## Vertical-slice runtime target

### Prologue — 60 to 90 minutes

#### P0: playable night at Dona Zila's house

- Player may walk before the opening advances.
- Three household interactions establish Zila and the move to Vila Amanhecer.
- The player feeds all three rescued partners.
- Each partner receives one complete, concrete legend.
- A gray figure crosses outside; the scene shows the Desencanto without naming
  every rule.

#### P1: morning choice and Census

- Player chooses only after caring for all three partners.
- Ciro receives the type-advantaged remaining starter.
- Anahi is linked to the third starter.
- Anahi integrates the Census pages into Zila's notebook.
- Rare Candies remain test-build supplies and do not inform campaign balance.

#### P2: Vila Amanhecer exploration

Before the road opens, optional NPCs establish:

- Ciro's family and the cost of medical care;
- why a Consortium scholarship is a real temptation;
- rumors of creatures losing color;
- Porto das Redes as the next destination;
- Dona Zila's role as a teller, not the guardian of every House.

The visible eastern opening is the only route exit.

#### P3: first field route

- capture-as-agreement tutorial;
- two optional trainers;
- a short side path and item;
- notebook recovery sidequest;
- first faded-creature encounter;
- safe return to Vila Amanhecer.

Only art-approved species may appear in encounters or trainer parties.

#### P4: Ciro battle and departure

The player can catch at least one partner before the battle. Ciro uses his
assigned starter and, after the first art batch, one unique local partner. The
departure scene must include the Consortium badge, his family's material need,
and his health-care motivation.

### Arc 1: Porto das Redes — 90 to 120 minutes

#### M0: coastal arrival

Route 109 becomes the landing and mangrove approach. Pale water, silent fishers,
discarded nets, and Consortium infrastructure communicate the problem before
exposition.

#### M1: town investigation

Slateport is reassigned to Porto das Redes. Six to eight NPCs distribute these
facts:

- fishers drowned;
- the survivors stopped singing;
- a mine discharges waste upstream;
- the Consortium regularized the mine;
- Iaraco depends on the fishing songs;
- a widow keeps an unfinished embroidered net.

The House of Tide is visible but its guardian will not begin the Vigil yet.

#### M2: four evidence nodes

1. memorial containing the fishers' names;
2. mine-discharge authorization or sign;
3. dockworker testimony containing the surviving line of the song;
4. embroidered net containing the unfinished final verse.

The notebook records the evidence without solving the investigation for the
player.

#### M3: Consortium field confrontation

The current Agent battle is reused at the discharge site. The Agent appears in
dialogue before fighting and uses a unique industrial-themed party. The pre-
battle heal remains because this battle closes a field sequence.

#### M4: restoration

The local widow completes the song with the player. Iaraco regains its form and
Iara-Mae appears as a non-capturable Testimony. The scene must preserve the
approved line about memory cleaning the dead.

#### M5: Tide Vigil

Dona Celina, the named local Storyteller, has appeared at least twice before the
fight. Her
three-Pokemon team represents current, mangrove endurance, and transmitted
memory. Initial target levels are 14, 15, and 17, tuned without debug candies.

Rewards:

- Mare Badge;
- notebook chapter;
- Testimony blessing;
- changed water/NPC state;
- clear opening to the next route;
- Ciro scene showing deeper Consortium involvement.

## Existing map allocation

| Narrative function | Reused Emerald/Arauna asset |
| --- | --- |
| Dona Zila's house | AraunaPlayerHouse |
| Vila Amanhecer | AraunaMapLab |
| Research annex | AraunaResearchCenter |
| first field route | AraunaMistRoute / early-route shell |
| mangrove landing | Route109 |
| Porto das Redes | SlateportCity |
| widow's home | existing Slateport interior |
| House of Tide | Shipyard, Museum, or another existing interior |
| Consortium discharge site | existing industrial interior/route segment |
| later First Link material | AraunaFirstLinkRuin and Chamber |

## Boss rules

- Guardian is named and introduced before the challenge.
- Badge objective is completed before the battle.
- Consecutive story bosses cannot share the same lead species.
- Rival, Agent, and guardian parties must have distinct visual identities.
- Losses are retry-safe and do not repeat long cutscenes.
- A heal is placed before long mandatory gauntlets, not before every trainer.
- Levels are balanced with no Rare Candy use.

## Art gate

A species cannot enter the runtime encounter table or a story trainer party
until it has:

- 64x64 indexed front sprite;
- matching back sprite and icon;
- Emerald-readable silhouette and outline;
- no antialiasing or illustration-style detail;
- in-ROM battle and Pokedex screenshots reviewed;
- cultural/sensitivity review when derived from named traditions.

The first batch covers every species visible in the Prologue and Porto,
including all three starter lines, Ciro's local partner, the Agent party,
Iaraco, and the House of Tide team. Unapproved Oxum, Preguicim, Cervalo, and
Curupira-Anciao art stays out of the critical path.

A faded story encounter uses dedicated desaturated art. Until that asset passes
the gate, the event is communicated through tiles, sound, and prose rather than
a Poochyena overworld placeholder.

## Delivery gates

1. Foundation correction: east exit, Ciro identity/party, placeholder removal,
   player-facing development text removal.
2. Prologue scene script and state graph.
3. Prologue implementation and isolated playtest.
4. Porto investigation implementation.
5. Tide restoration, Agent encounter, and guardian battle.
6. Full 2.5-to-3.5-hour vertical-slice playtest.
7. Balance, art, and regression pass before second-House work.

Each gate must keep the ROM buildable and the previous save policy explicit.
