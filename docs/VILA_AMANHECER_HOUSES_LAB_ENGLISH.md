# Vila Amanhecer — houses and Anahi laboratory in English

Status: English-only migration slice.

This slice completes the main indoor opening surfaces around the already-restored Vila Amanhecer / Route 101 exterior sequence while preserving the inherited Emerald house and Birch-lab event graph.

## Player home + Ciro home — 30 blocks

The existing house-cleanup contract is reused as the source-of-truth for exact labels and pre-render anchors.

### Player home

The English surface preserves:

- MOM settling into the new home with the player;
- the inherited clock setup, framed as a clock ELIAS left behind;
- the PAMPA DA ESPERA TV report about ELIAS;
- MOM directing the player toward PROF. ANAHI;
- resting and return-home dialogue;
- the inherited badge/gift branch;
- POKéNAV registration with MOM.

### Ciro home and room

Both internal May/Brendan branches display the same CIRO identity and voice:

- CIRO is already doing fieldwork with HORIZON support;
- his family describes the grant, maps, sensors and constant travel;
- the first player/CIRO meeting remains brief and competitive;
- ROUTE 103 notes establish his early confidence in HORIZON data;
- the inherited rival POKé BALL remains untouched mechanically.

## Professor Anahi laboratory — 50 blocks

The complete visible lab surface is now English rather than a mixture of authored Portuguese and Emerald residue.

### Early game

- the aide explains ANAHI's fieldwork and history with BOND sensors;
- ANAHI frames the starter relationship as mutual choice rather than ownership;
- names are introduced as potential anchors of memory;
- CIRO is sent to ROUTE 103 as the player's first ideological counterpoint;
- after the rival battle, the POKéDEX becomes a field record for species, memory gaps, behavioral changes and DESECHANTMENT;
- both internal rival-gender branches give the same CIRO dialogue and original five POKé BALLS.

### Lab environment

The machine, PC, bookshelf and notes reinforce ANAHI's research without forcing exposition into every conversation. The BOND sensor visibly predates HORIZON's current project, and the lab contains records about POKéMON losing recognition of familiar people and places.

### National Dex and postgame

The inherited National Dex sequence now emphasizes that more data does not remove the duty to ask better questions. CIRO's later dialogue evolves rather than repeating his early HORIZON position.

### Additional starter reward

The inherited Cyndaquil / Totodile / Chikorita reward remains intact. The visible framing treats the choice as selecting a partner rather than claiming a prize.

### Battle Circuit call

The internal Scott call slot remains structurally unchanged but visibly belongs to SEU BENTO, directing the player toward the BATTLE CIRCUIT by ferry from PORTO DO SAL or BAIA DAS LUZES.

## Technical contract

Two renderers cover 80 blocks:

- `scripts/render_vila_amanhecer_houses_en.py`: 30 blocks across three house maps, reusing `tools/cleanup_littleroot_house_residue.py` as its exact source contract;
- `scripts/render_anahi_lab_en.py`: 50 lab blocks with width, residue, structural-mask and gameplay-token validation.

The build backs up and restores all four newly touched sources transactionally.

Preserved mechanics include clock flow, TV state, rest, badge gift, POKéNAV registration, rival gender routing, Route 103 progression, POKéDEX acquisition, five-Poké-Ball gift, National Dex, Cyndaquil/Totodile/Chikorita species IDs, extra-starter state, Match Call/Battle Circuit trigger, flags, variables, warps, saves, geometry and art.

English-only. PR #58 untouched.
