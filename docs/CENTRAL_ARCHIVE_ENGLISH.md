# Central Archive — English narrative restoration

Status: English-only migration slice.

This slice restores the authored B1F/B2F Central Archive story in the official English build while preserving the original Aqua Hideout event skeleton.

## B1F — evidence and responsibility

The lower archive exposes records that complicate every major adult around M'BOI:

- ANAHI helped build the first BOND sensors;
- CIRO's father appears among the dead;
- HORIZON later supported CIRO, while rank-and-file staff do not know what he was told;
- ELIAS approved part of the M'BOI protocols, but the archive also contains objections and reservations;
- OTACILIO lost family at M'BOI and turned the LIVING ARCHIVE into his life's work.

The staff do not present any single document as total truth. The scene distinguishes responsibility, grief, signatures, objections and institutional language instead of reducing M'BOI to one culprit.

## B2F — evacuation

The archive is being evacuated as the confrontation escalates:

- local copies are being wiped;
- M'BOI servers and BOND records are loaded first;
- BRENO stalls the player using the unchanged Matt battle slot;
- OTACILIO leaves with the transferred archive aboard the submersible;
- the route points toward CAVERNAS DE M'BOI beyond BAIA DAS LUZES.

HORIZON staff continue to disagree internally. Several lines make clear that following protocol does not automatically make an order ethical.

## Technical contract

The English wrapper reuses the existing 25 anchor-checked targets from `render_arquivo_central_surface.py`:

- 12 B1F text blocks;
- 13 B2F text blocks.

Every visible segment is kept within the 32-character GBA limit. The underlying trainer IDs, Matt/Breno battle, Electrode encounters, submarine movement, escape flags, object IDs, warps, saves and map geometry are untouched.

The two map sources are backed up before rendering and restored automatically when the English build exits or is interrupted.
