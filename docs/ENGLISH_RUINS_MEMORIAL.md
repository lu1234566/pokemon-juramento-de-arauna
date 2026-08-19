# Ruinas da Queda and Memorial dos Nomes — English restoration

Status: English-only migration slice.

This slice restores the Ruinas da Queda bridge and the Memorial dos Nomes confrontation/aftermath as Arauna-authored English content while preserving the original Emerald event skeleton.

## Ruinas da Queda

- REMEMBRANCERS take the METEORITE after using a mineral researcher as a guide;
- HORIZON arrives too late and pursues them toward SERRA DA CINZA;
- OTACILIO explicitly warns the protagonist not to mistake cooperation against an uncontrolled release for agreement with him;
- the scene now flows directly into the English Serra da Cinza confrontation.

## Memorial dos Nomes

HORIZON agents are ordered to remove memorial plaques and records under a security protocol. Their dialogue shows discomfort with ownership and removal rather than presenting the faction as a uniform block.

The conflict exposes two RECORD-MATRICES: one taken by HORIZON and one by the REMEMBRANCERS. Later dialogue preserves the two ancient currents without assigning them to specific internal legendary species slots.

The memorial's final thesis is expressed through the OATH: memory and forgetting both become violence when one person chooses for everyone else.

## Item surface

The unchanged `ITEM_MAGMA_EMBLEM` slot is rendered as:

- `REMEM. EMBLEM`;
- description: an emblem carried by REMEMBRANCERS that opens their base.

No item ID, use logic or save representation changes.

## Technical contract

The English wrapper reuses the existing 34 anchor-checked text targets and rendering functions. It also preserves the item-description layout workaround required by `item_descriptions.h`.

No trainer IDs/parties, flags, variables, object movements, record/orb event flow, legendary IDs, warps, saves, map geometry or art are changed. PR #58 remains untouched.
