# Cavernas de M'Boi — English climax restoration

Status: English-only migration slice.

This slice restores the authored Seafloor Cavern Room 9 climax as Arauna-native English while preserving the Emerald legendary-event skeleton.

## Otacilio

OTACILIO reaches the archive core believing the RECORD-MATRIX can synchronize the LIVING ARCHIVE with the ancient current beneath M'BOI.

His reasoning remains understandable but dangerous: if the system can contain and control the current, he believes the DISENCHANTMENT can be managed instead of allowed to destroy more families.

The player defeats him, but the synchronization continues. The RECORD-MATRIX responds without a command and the archive breaks containment.

## Collapse

The scene then shifts from ideology to consequence:

- readings rise across Arauna;
- OTACILIO realizes the LIVING ARCHIVE spread the current instead of containing it;
- LUZIA confronts him but refuses to waste time assigning blame during the emergency;
- both ancient currents are reported as reacting;
- the party moves toward AGUAS DE M'BOI to see the regional effect.

The text intentionally avoids assigning either current to a specific internal legendary species. Existing Groudon/Kyogre event IDs remain implementation details.

## Technical contract

The English wrapper reuses all 15 anchor-checked targets from `render_mboi_climax_surface.py` and keeps every visible segment within the 32-character GBA limit.

The underlying Archie/Maxie trainer/event slots, legendary species IDs, orb/record behavior, battle logic, camera, movements, flags, weather transition, warps, saves and map geometry are untouched.
