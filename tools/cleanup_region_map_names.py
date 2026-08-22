#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "src" / "data" / "region_map" / "region_map_sections.json"
MAP_NAME_LENGTH = 16

NAMES = {
    "MAPSEC_LITTLEROOT_TOWN": "VILA AMANHECER",
    "MAPSEC_OLDALE_TOWN": "VILA DA PASSAGEM",
    "MAPSEC_DEWFORD_TOWN": "PORTO DAS REDES",
    "MAPSEC_LAVARIDGE_TOWN": "CASA DA CINZA",
    "MAPSEC_FALLARBOR_TOWN": "CAMPO DAS CINZAS",
    "MAPSEC_VERDANTURF_TOWN": "VALE DO SILENCIO",
    "MAPSEC_PACIFIDLOG_TOWN": "CASA DA FOGUEIRA",
    "MAPSEC_PETALBURG_CITY": "PAMPA DA ESPERA",
    "MAPSEC_SLATEPORT_CITY": "PORTO DO SAL",
    "MAPSEC_MAUVILLE_CITY": "ENCRUZILHADA",
    "MAPSEC_RUSTBORO_CITY": "SERRA DO UIVO",
    "MAPSEC_FORTREE_CITY": "MATA DO MEIO",
    "MAPSEC_LILYCOVE_CITY": "BAIA DAS LUZES",
    "MAPSEC_MOSSDEEP_CITY": "MISSOES DO CEU",
    "MAPSEC_SOOTOPOLIS_CITY": "AGUAS DE M'BOI",
    "MAPSEC_EVER_GRANDE_CITY": "ESTR. JURAMENTO",
    "MAPSEC_GRANITE_CAVE": "GRUTA DAS VOZES",
    "MAPSEC_MT_CHIMNEY": "SERRA DA CINZA",
    "MAPSEC_SAFARI_ZONE": "ARAUNA PRESERVE",
    "MAPSEC_BATTLE_FRONTIER": "BATTLE CIRCUIT",
    "MAPSEC_RUSTURF_TUNNEL": "GALERIAS SERRA",
    "MAPSEC_METEOR_FALLS": "RUINAS DA QUEDA",
    "MAPSEC_METEOR_FALLS2": "RUINAS DA QUEDA",
    "MAPSEC_MT_PYRE": "MEMORIAL NOMES",
    "MAPSEC_AQUA_HIDEOUT_OLD": "ARQUIVO CENTRAL",
    "MAPSEC_SEAFLOOR_CAVERN": "CAVERNAS M'BOI",
    "MAPSEC_VICTORY_ROAD": "ESTR. JURAMENTO",
    "MAPSEC_SKY_PILLAR": "TORRE JURAMENTO",
}


def pattern(mapsec: str) -> re.Pattern[str]:
    return re.compile(
        rf'(?P<prefix>"id":\s*"{re.escape(mapsec)}",\s*\n\s*"name":\s*")[^"]*(?P<suffix>")',
        re.MULTILINE,
    )


def find_name(text: str, mapsec: str) -> str | None:
    match = pattern(mapsec).search(text)
    if not match:
        return None
    whole = match.group(0)
    marker = '"name":'
    return whole.split(marker, 1)[1].split('"', 2)[1]


def validate(text: str) -> list[str]:
    failures: list[str] = []
    for mapsec, expected in NAMES.items():
        if len(expected) > MAP_NAME_LENGTH:
            failures.append(
                f"{mapsec}: {expected!r} exceeds MAP_NAME_LENGTH={MAP_NAME_LENGTH}"
            )
        current = find_name(text, mapsec)
        if current is None:
            failures.append(f"missing map section {mapsec}")
        elif current != expected:
            failures.append(f"{mapsec}: expected {expected!r}, found {current!r}")
    return failures


def apply() -> int:
    text = TARGET.read_text(encoding="utf-8")
    changed = 0
    for mapsec, expected in NAMES.items():
        if len(expected) > MAP_NAME_LENGTH:
            raise RuntimeError(
                f"{mapsec}: {expected!r} exceeds MAP_NAME_LENGTH={MAP_NAME_LENGTH}"
            )
        rx = pattern(mapsec)
        if len(rx.findall(text)) != 1:
            raise RuntimeError(f"Expected exactly one {mapsec} entry")
        updated = rx.sub(lambda m: m.group("prefix") + expected + m.group("suffix"), text, count=1)
        if updated != text:
            changed += 1
        text = updated
    failures = validate(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    TARGET.write_text(text, encoding="utf-8")
    print(f"Region-map Arauna names: {changed} changed; {len(NAMES)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Region-map Arauna name check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Region-map Arauna name check PASS: {len(NAMES)} entries within {MAP_NAME_LENGTH} chars.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
