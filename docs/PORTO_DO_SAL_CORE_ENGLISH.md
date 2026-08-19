# Porto do Sal — English core restoration

Status: English-only migration slice.

This slice restores the main Porto do Sal story core in English without changing the Slateport event skeleton: museum queue and people, museum science, the oceanographic-parts confrontation, and the later submarine requisition that escalates OTACILIO's behavior.

## Museum queue and 1F — 32 blocks

The exterior queue and museum reception remain ordinary civic space rather than a faction dungeon:

- visitors remember coming to the museum as children;
- HORIZON personnel are instructed to enter quietly and pay the ¥50 civilian admission;
- some staff question vague field-inspection orders or whether vital equipment should be requisitioned;
- the reception, visitors and oceanographic interest remain intact;
- the familiar HORIZON agent still gives the original TM as repayment of a personal debt, including the bag-full branch.

## Scientific exhibits — 22 blocks

The museum keeps a strong educational identity:

- whirlpool and waterfall demonstrations;
- ocean soil, coastal sand and ripple-mark fossil displays;
- salinity, pressure and deep/surface current explanations;
- MODEL OF ARAUNA;
- coastal ferry, research submersible, unmanned pod and historic liner replicas.

Legacy Hoenn/Slateport ship-name residue is removed from the curated surface while the exhibit scripts remain mechanically unchanged.

## Museum confrontation — 13 blocks + item surface

The unchanged DEVON GOODS slot is surfaced as `OCEANIC PARTS` with an English deep-sea research description.

Chronologically, this scene is important because it happens before the submarine seizure:

- the HARBOR ENGINEER expects parts to calibrate deep-sea sensors;
- two HORIZON field agents try to requisition them for mapping M'BOI anomalies;
- after the unchanged battles, OTACILIO arrives;
- at this stage, OTACILIO refuses to turn a civilian MUSEUM into a forced operation and orders the agents to stand down and find another way.

This establishes a visible escalation when he later decides that the M'BOI emergency justifies taking the submarine without permission.

## Submarine sequence — 13 blocks

Later, readings beneath M'BOI rise with the tremors and a BOND current moves through the caverns.

HORIZON invokes emergency protocol and requisitions the research submersible. OTACILIO states that it is the only vehicle capable of reaching CAVERNAS DE M'BOI. His route is explicit:

1. CENTRAL ARCHIVE to finish loading the transferred archive;
2. then M'BOI.

The HARBOR ENGINEER objects that the vehicle was built for research, not for a faction. After departure, the unchanged DIVE progression points the player toward the caverns.

## Technical contract

This English core covers 80 visible text blocks:

- 15 museum-queue city blocks;
- 17 museum 1F reception/people blocks;
- 9 museum 1F science blocks;
- 13 museum 2F science/patron blocks;
- 13 museum 2F confrontation blocks;
- 8 city submarine-sequence blocks;
- 5 harbor submarine-sequence blocks.

Three small checked wrappers adjust only English line widths found during manual review. Final visible segments are at most 32 characters.

The following remain untouched: museum ¥50 flow, TM item and received flag, bag-full branch, `ITEM_DEVON_GOODS` internal ID, both museum trainer IDs/parties, submarine object/state movement, DIVE progression, ferry/postgame logic, Scanner trade, flags, variables, warps, saves, geometry and art.
