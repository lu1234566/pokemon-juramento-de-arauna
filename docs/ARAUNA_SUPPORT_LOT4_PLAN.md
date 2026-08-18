# Arauna support characters — lot 4

Ciro's mother now has a dedicated visual identity in the single-player story without expanding Emerald's one-byte object graphics ID format.

Implementation choice:
- reuse `OBJ_EVENT_GFX_LINK_RECEPTIONIST` (ID 28), a connectivity/multiplayer-only overworld slot that is not needed by the normal campaign;
- replace that slot's 144x32 sheet with the converted mother-of-Ciro artwork remapped to its existing NPC_3 runtime palette;
- target only `LOCALID_RIVALS_HOUSE_1F_MOM` in the two gender-dependent rival-house maps.

No coordinates, scripts, flags, warps, movement, story progression, object-ID limits or dynamic graphics IDs are changed. The only tradeoff is that the Link Receptionist would share this visual in optional link/multiplayer facilities, which are outside Arauna's intended single-player campaign.
