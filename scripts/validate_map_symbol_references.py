#!/usr/bin/env python3
"""Static guard for map/script symbol references that the data validators miss.

The Arauna project reuses vanilla Emerald maps by rewriting each map.json and
its scripts. Because the CI validators only inspect data and text (they never
compile or link), a whole class of build breakers slipped through:

  * a map.json weather/music set to a constant that does not exist
    (e.g. WEATHER_CLOUDY);
  * a map.json object/sign/trigger pointing at a script label that is not
    defined anywhere (e.g. SlateportCity_EventScript_PokeMartSign);
  * a script or engine .c file referencing an object LOCALID_* that no longer
    exists because the reused map dropped that object event
    (e.g. LOCALID_SLATEPORT_ENERGY_GURU, or the orphaned vanilla Slateport
    story scripts).

This validator resolves those three reference kinds statically, with no ARM
toolchain, so the failures surface in the pure-Python repository-safety job
(and locally) instead of only at link time.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAPS_DIR = ROOT / "data" / "maps"

NO_SCRIPT = {"0", "0x0", "NULL"}

# map.json fields whose value is a C constant that must resolve at link time.
# "flag" accepts "0" as well: that is the engine's always-visible sentinel.
CONSTANT_FIELDS = {
    "flag": ("FLAG_",),
    "var": ("VAR_",),
    "graphics_id": ("OBJ_EVENT_GFX_",),
    "movement_type": ("MOVEMENT_TYPE_",),
    "trainer_type": ("TRAINER_TYPE_",),
}
# Values that are plain integers, or generated at build time from the map and
# layout tables, are not resolvable from the headers alone.
GENERATED_PREFIXES = ("MAP_", "LAYOUT_", "MAPSEC_", "OBJ_EVENT_GFX_VAR_")
IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
LOCALID_RE = re.compile(r"\bLOCALID_[A-Z][A-Z0-9_]*\b")
# Mixed case matters: names like FLAG_UNUSED_0x4D4 carry a lowercase x.
DEFINE_RE = re.compile(r"^\s*#\s*define\s+([A-Za-z_][A-Za-z0-9_]*)")
LABEL_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)::")
# An enum member: a bare uppercase name followed by '=' or ',' or end of line.
ENUM_MEMBER_RE = re.compile(r"^\s*([A-Z][A-Z0-9_]{2,})\s*(?:=|,|$)")
SET_LOCALID_RE = re.compile(r"^\s*\.(?:set|equ)\s+(LOCALID_[A-Z0-9_]+)\b")


def read(path):
    return path.read_text(encoding="utf-8", errors="replace")


def defined_constants(header, prefix):
    out = set()
    path = ROOT / "include" / "constants" / header
    if path.exists():
        for line in read(path).splitlines():
            m = DEFINE_RE.match(line)
            if m and m.group(1).startswith(prefix):
                out.add(m.group(1))
    return out


def all_defined_names():
    """Every constant name the headers introduce, by #define or by enum.

    OBJ_EVENT_GFX_* and MOVEMENT_TYPE_* are enum members rather than macros, so
    collecting only #defines would report every graphics id in the project as
    undefined.
    """
    out = set()
    for path in sorted((ROOT / "include").rglob("*.h")):
        for line in read(path).splitlines():
            m = DEFINE_RE.match(line)
            if m:
                out.add(m.group(1))
                continue
            m = ENUM_MEMBER_RE.match(line)
            if m:
                out.add(m.group(1))
    return out


def iter_map_jsons():
    for mj in sorted(MAPS_DIR.glob("*/map.json")):
        try:
            yield mj, json.loads(read(mj))
        except json.JSONDecodeError as exc:
            yield mj, exc


def collect_defined_labels():
    """Every asm label defined anywhere under data/ or src/, plus C symbols."""
    labels = set()
    for base in ("data", "src", "gflib"):
        d = ROOT / base
        if not d.exists():
            continue
        for path in d.rglob("*"):
            if path.suffix not in (".inc", ".s", ".c", ".h"):
                continue
            for line in read(path).splitlines():
                m = LABEL_RE.match(line)
                if m:
                    labels.add(m.group(1))
    return labels


def collect_defined_localids():
    ids = set()
    # Manual defines (LOCALID_PLAYER, LOCALID_CAMERA, generated-OWE bounds, ...)
    for header in ("event_objects.h",):
        path = ROOT / "include" / "constants" / header
        if path.exists():
            for line in read(path).splitlines():
                m = DEFINE_RE.match(line)
                if m and m.group(1).startswith("LOCALID_"):
                    ids.add(m.group(1))
    # Named object events across every map.json.
    for _mj, data in iter_map_jsons():
        if isinstance(data, Exception):
            continue
        for obj in data.get("object_events") or []:
            lid = obj.get("local_id")
            if isinstance(lid, str) and lid.startswith("LOCALID_"):
                ids.add(lid)
    # Locally defined ids via `.set`/`.equ` in scripts (e.g. daycare mons).
    for base in ("data", "src"):
        d = ROOT / base
        if not d.exists():
            continue
        for path in d.rglob("*"):
            if path.suffix not in (".inc", ".s"):
                continue
            for line in read(path).splitlines():
                m = SET_LOCALID_RE.match(line)
                if m:
                    ids.add(m.group(1))
    return ids


def collect_referenced_localids():
    refs = {}  # name -> set(files)
    for base in ("src", "data", "gflib"):
        d = ROOT / base
        if not d.exists():
            continue
        for path in d.rglob("*"):
            if path.suffix not in (".c", ".h", ".inc", ".s"):
                continue
            rel = path.relative_to(ROOT)
            for name in LOCALID_RE.findall(read(path)):
                refs.setdefault(name, set()).add(str(rel))
    return refs


def main():
    errors = []

    weather = defined_constants("weather.h", "WEATHER_")
    songs = defined_constants("songs.h", "MUS_") | defined_constants("songs.h", "SE_")
    labels = collect_defined_labels()
    defines = all_defined_names()

    for mj, data in iter_map_jsons():
        rel = mj.relative_to(ROOT)
        if isinstance(data, Exception):
            errors.append(f"{rel}: invalid JSON: {data}")
            continue
        w = data.get("weather")
        if w and weather and w not in weather:
            errors.append(f"{rel}: unknown weather constant {w}")
        m = data.get("music")
        if m and songs and m not in songs:
            errors.append(f"{rel}: unknown music constant {m}")
        for key in ("object_events", "coord_events", "bg_events"):
            for index, ev in enumerate(data.get(key) or []):
                s = ev.get("script")
                if s and s not in NO_SCRIPT and s not in labels:
                    errors.append(f"{rel}: {key} references undefined script {s}")
                # Constant-valued fields become symbols in data/map_events.o, so
                # a stale name here survives every data check and only breaks at
                # link time, thousands of compile steps in.
                for field, prefixes in CONSTANT_FIELDS.items():
                    value = ev.get(field)
                    if not isinstance(value, str) or not IDENTIFIER_RE.match(value):
                        continue
                    if not value.startswith(prefixes):
                        continue
                    if value.startswith(GENERATED_PREFIXES) or value in defines:
                        continue
                    errors.append(
                        f"{rel}: {key}[{index}].{field} references undefined "
                        f"constant {value}"
                    )

    defined_ids = collect_defined_localids()
    for name, files in sorted(collect_referenced_localids().items()):
        if name not in defined_ids:
            where = ", ".join(sorted(files)[:3])
            errors.append(f"undefined object local id {name} (referenced in {where})")

    if errors:
        print("Map symbol reference check FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("Map symbol reference check passed: weather, music, scripts and "
          "object local ids all resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
