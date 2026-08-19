# First HORIZON forest encounter — English restoration

Status: English-only migration slice.

The first scripted faction encounter in Petalburg Woods is again Arauna-authored content in the official build.

## Visible sequence

- the field researcher is monitoring unusual changes in the local POKéMON population;
- a HORIZON agent arrives to seize the researcher's field reports;
- the player protects the researcher using the unchanged Emerald battle slot;
- after losing, the agent reveals that HORIZON is already moving on SERRA DO UIVO;
- the researcher leaves to follow that lead and still gives the original GREAT BALL reward.

## English terminology

The visible organization name is `HORIZON`. Legacy `CONSORCIO HORIZONTE`, `DEVON RESEARCHER`, `PETALBURG WOODS`, `RUSTBORO` and `TEAM AQUA` text is rejected inside the curated blocks.

## Technical contract

The renderer changes only the twelve `.string` blocks used by the encounter. Trainer IDs and parties, object IDs, movements, Great Ball reward, bag-full branch, `VAR_PETALBURG_WOODS_STATE`, warps, saves and map geometry are untouched.

The source map is backed up before rendering and restored automatically after the English build finishes or is interrupted.
