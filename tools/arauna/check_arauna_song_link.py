#!/usr/bin/env python3
"""Keep ld_script.ld's song list in step with sound/song_table.inc.

The two builds place song data by different means. MODERN=1 uses
ld_script_modern.ld, which matches every song object with one wildcard
(`sound/songs/*.o(.rodata)`), so adding a song to the table is enough for it.
MODERN=0 uses ld_script.ld, which names all 551 song objects one at a time.

That difference is why the Arauna soundtrack went missing without anyone
noticing: twenty-one songs were added to sound/song_table.inc and to
sound/songs/midi/, the MODERN=1 build kept linking, and the MODERN=0 build
was left with a song table pointing at data the linker had not been told to
place. A hand-maintained list of 551 entries drifts the moment somebody adds
the 552nd, and it drifts silently.

This check closes that gap. It fails when a song exists as a source but is
not named in ld_script.ld, when ld_script.ld names a song with no source, or
when the two disagree about order -- the linker lays the song data out in the
order this list gives, and the song table indexes into it, so an order
mismatch is as wrong as an omission.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LD_SCRIPT = ROOT / "ld_script.ld"
SONG_TABLE = ROOT / "sound" / "song_table.inc"
MIDI_DIR = ROOT / "sound" / "songs" / "midi"

LD_ENTRY = re.compile(r"^\s*sound/songs/midi/(\w+)\.o\(\.rodata\);", re.M)
TABLE_ENTRY = re.compile(r"^\tsong (\w+),", re.M)


def fail(message: str) -> None:
    print(f"Arauna song link check: FAIL\n  {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    for path in (LD_SCRIPT, SONG_TABLE):
        if not path.is_file():
            fail(f"missing {path.relative_to(ROOT)}")

    listed = LD_ENTRY.findall(LD_SCRIPT.read_text(encoding="utf-8"))
    table = TABLE_ENTRY.findall(SONG_TABLE.read_text(encoding="utf-8"))

    if len(listed) != len(set(listed)):
        seen: set[str] = set()
        duplicates = sorted({s for s in listed if s in seen or seen.add(s)})
        fail(f"ld_script.ld names the same song twice: {duplicates}")

    # Unused indices in the table are filled with dummy_song_header, which is
    # a label in the table itself rather than a song object, so only entries
    # backed by a real source are expected to be placed.
    played = [s for s in table if (MIDI_DIR / f"{s}.s").is_file()]

    # A song the table plays but the linker was never told to place. This is
    # the failure the Arauna soundtrack hit.
    unplaced = [s for s in played if s not in set(listed)]
    if unplaced:
        fail("sound/song_table.inc plays songs that ld_script.ld does not "
             "place, so a MODERN=0 build indexes data the linker left out:\n"
             + "\n".join(f"    {s}" for s in unplaced))

    # A song placed but never played, or named with no source at all.
    absent = [s for s in listed if not (MIDI_DIR / f"{s}.s").is_file()]
    if absent:
        fail("ld_script.ld names song objects with no source in "
             "sound/songs/midi:\n" + "\n".join(f"    {s}" for s in absent))

    # The linker lays the data out in this order and the song table indexes
    # into it, so the shared entries have to run in the same order in both.
    shared = [s for s in listed if s in set(played)]
    expected = [s for s in played if s in set(listed)]
    if shared != expected:
        first = next(i for i, (a, b) in enumerate(zip(shared, expected))
                     if a != b)
        fail(f"ld_script.ld and sound/song_table.inc disagree about song "
             f"order from entry {first}: ld says {shared[first]!r}, the "
             f"table says {expected[first]!r}")

    print(f"Arauna song link check: OK ({len(listed)} song objects placed, "
          f"{len(played)} played, order matches).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
