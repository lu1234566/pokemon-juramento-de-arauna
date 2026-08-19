# Baia das Luzes — common English city surface

Status: English-only narrative continuation.

This slice completes the outdoor/common Lilycove replacement around the already-integrated Ciro encounter, turning the city into BAIA DAS LUZES without changing its Emerald event structure.

## HORIZON waterfront presence

The four existing Aqua object slots now read as HORIZON staff around the waterfront operations hub. They are not written as interchangeable villains:

- one accidentally reveals equipment movements;
- a junior employee believes the work matters but is uneasy about not knowing every decision;
- one politely enforces a restricted service tunnel;
- another admits that M'BOI made the old dream of one system solving everything difficult to defend.

The WAILMER event is reframed as coastal signal-buoy testing that temporarily blocks civilian boats. The existing pre/post-submarine state remains intact.

## City life

Ordinary residents keep BAIA DAS LUZES from becoming only a faction headquarters:

- the Contest Hall attracts trainers from across Arauna;
- a visitor wonders about coastal species unique to the region;
- an art dealer discusses the museum's paintings, crafts and old maps;
- an elderly couple remembers a proposal on the changing waterfront;
- a missing-POKéMON misunderstanding becomes a small example of blaming HORIZON too quickly rather than proof of wrongdoing;
- honeymoon visitors react to a distant large POKéMON silhouette without naming an internal legendary species.

## Signs and services

Visible signs now use Arauna-native surfaces for:

- BAIA DAS LUZES CONTEST HALL;
- LUZES INN;
- BAIA DAS LUZES MUSEUM and the player's exhibit state;
- BAIA DAS LUZES HARBOR, including pre/post ferry-service states;
- Trainer Fan Club;
- BAIA DAS LUZES DEPT. STORE;
- Move Deleter.

Rumors about SKY PILLAR / Route 131 are surfaced as TORRE DO JURAMENTO.

## Technical contract

The renderer changes 32 text blocks that are disjoint from the 19 labels handled by `render_baia_luzes_ciro_en.py`. Build order is intentionally Ciro first, common city surface second.

A single small checked wrapper only adjusts six English line breaks found during manual width auditing. Every final visible segment is at most 32 characters.

Submarine-state flags, WAILMER metatiles and trainer event, museum painting counter, badge state, Contest/Department Store/Move Deleter/Harbor functionality, rival event and trainer IDs, objects, warps, saves, geometry and art remain untouched.
