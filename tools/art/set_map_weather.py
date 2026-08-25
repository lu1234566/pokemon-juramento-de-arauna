#!/usr/bin/env python3
"""Give each outdoor map weather that matches its Arauna biome.

Every route in the region was sitting on WEATHER_SUNNY and thirteen outdoor
maps on WEATHER_NONE, so the whole map read as one flat bright slab: the
rainforest, the ash route, the coast and the preserve all looked identical.

Two kinds of change.

RESTORE -- four routes whose header contradicted their own coord events. The
maps already carry weather triggers that switch as the player walks; the
header is what you get when you fly or warp in. Route 113 has eleven ash
triggers but arrived sunny, Route 119 and 123 have twelve cycle triggers
each, Route 120 has rain at its north end. Jagged Pass is an outdoor map that
had no weather at all.

AMBIENCE -- cosmetic weather chosen per biome. Only RAIN, RAIN_THUNDERSTORM,
DOWNPOUR, SANDSTORM and DROUGHT reach a battle (battle_util.c,
ABILITYEFFECT_SWITCH_IN_WEATHER); everything used here is scenery, so the
look changes and the balance does not. The one exception is the RESTORE set,
which puts back weather the routes already had in their own triggers.

    python3 tools/art/set_map_weather.py [--apply]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
MAPS = ROOT / "data" / "maps"

# Weather that a Pokemon's switch-in reads and turns into battle weather.
BATTLE_WEATHER = {"WEATHER_RAIN", "WEATHER_RAIN_THUNDERSTORM", "WEATHER_DOWNPOUR",
                  "WEATHER_SANDSTORM", "WEATHER_DROUGHT"}

RESTORE = {
    "Route113": ("WEATHER_VOLCANIC_ASH", "11 ash triggers; arrived sunny"),
    "Route119": ("WEATHER_ROUTE119_CYCLE", "12 cycle triggers; arrived sunny"),
    "Route123": ("WEATHER_ROUTE123_CYCLE", "12 cycle triggers; arrived sunny"),
    "Route120": ("WEATHER_RAIN", "rain triggers at the north end"),
    "JaggedPass": ("WEATHER_SUNNY", "outdoor map with no weather at all"),
}

AMBIENCE = {
    **{m: ("WEATHER_SUNNY_CLOUDS", "Atlantic forest belt") for m in (
        "Route101", "Route102", "Route103", "Route104", "Route104_Prototype",
        "Route116", "Route117", "Route121")},
    **{m: ("WEATHER_SUNNY_CLOUDS", "cerrado, open country") for m in (
        "Route110", "Route118")},
    **{m: ("WEATHER_SHADE", "serra, overcast highland") for m in (
        "Route114", "Route115", "MtPyre_Exterior")},
    **{m: ("WEATHER_SUNNY_CLOUDS", "coast and open sea") for m in (
        "Route105", "Route106", "Route107", "Route108", "Route109", "Route122",
        "Route124", "Route125", "Route126", "Route127", "Route128", "Route129",
        "Route130", "Route131", "Route132", "Route133", "Route134")},
    **{m: ("WEATHER_SUNNY_CLOUDS", "outdoor map that had none") for m in (
        "SafariZone_North", "SafariZone_Northeast", "SafariZone_Northwest",
        "SafariZone_South", "SafariZone_Southeast", "SafariZone_Southwest",
        "BattleFrontier_OutsideEast", "BattleFrontier_OutsideWest",
        "SouthernIsland_Exterior", "SkyPillar_Outside")},
    "SkyPillar_Top": ("WEATHER_FOG_HORIZONTAL", "summit above the cloud line"),
    # Caatinga stays bright and harsh: Route111 and Route112 keep WEATHER_SUNNY.
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    changed = balance = 0
    for group, table in (("restore", RESTORE), ("ambience", AMBIENCE)):
        print(f"-- {group}")
        for name, (weather, why) in sorted(table.items()):
            path = MAPS / name / "map.json"
            if not path.is_file():
                raise SystemExit(f"no such map: {name}")
            text = path.read_text(encoding="utf-8")
            current = json.loads(text)["weather"]
            if current == weather:
                continue
            if weather in BATTLE_WEATHER:
                balance += 1
            changed += 1
            print(f"   {name:<28} {current:<22} -> {weather:<24} ({why})")
            if args.apply:
                # Rewrite the one field in place so the file's formatting, key
                # order and the rest of the map data are untouched.
                new, n = re.subn(r'("weather"\s*:\s*)"[^"]*"',
                                 lambda m: m.group(1) + f'"{weather}"', text, count=1)
                if n != 1:
                    raise SystemExit(f"{name}: expected one weather field, found {n}")
                path.write_text(new, encoding="utf-8")

    verb = "changed" if args.apply else "would change"
    print(f"\n{changed} map(s) {verb}; {balance} of them use weather a battle reads.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
