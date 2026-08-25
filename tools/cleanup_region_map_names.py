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
    # These three already have a canon name on another visible surface, so the
    # region map was contradicting the landmark bar and the M'BOI menu.
    "MAPSEC_AQUA_HIDEOUT": "ARQUIVO CENTRAL",   # matches MAPSEC_AQUA_HIDEOUT_OLD
    "MAPSEC_NEW_MAUVILLE": "OLD POWER RELAY",   # matches LandmarkName_NewMauville
    "MAPSEC_CAVE_OF_ORIGIN": "M'BOI CORE",      # matches sText_AraunaMboiCore
    # The remaining sections that are actually drawn on the region map. Every
    # one of these except the three islands and caves without a landmark entry
    # is renamed in lockstep in LANDMARK_REPLACEMENTS, so the map and the
    # landmark bar never disagree about a place.
    "MAPSEC_PETALBURG_WOODS": "MATA DA ESPERA",  # the woods of PAMPA DA ESPERA
    "MAPSEC_ABANDONED_SHIP": "NAVIO PERDIDO",
    "MAPSEC_SHOAL_CAVE": "FURNA DA MARE",        # a furna is a sea cave
    "MAPSEC_MIRAGE_ISLAND": "ILHA MIRAGEM",
    "MAPSEC_SOUTHERN_ISLAND": "ILHA DO SUL",
    "MAPSEC_FIERY_PATH": "TRILHA DE FOGO",
    "MAPSEC_FIERY_PATH2": "TRILHA DE FOGO",
    "MAPSEC_JAGGED_PASS": "PASSO CORTADO",
    "MAPSEC_JAGGED_PASS2": "PASSO CORTADO",
    "MAPSEC_SEALED_CHAMBER": "CAMARA SELADA",
    "MAPSEC_SCORCHED_SLAB": "LAJE QUEIMADA",
    "MAPSEC_ISLAND_CAVE": "GRUTA DO GELO",
    "MAPSEC_DESERT_RUINS": "RUINAS DA AREIA",
    "MAPSEC_ANCIENT_TOMB": "TUMBA ANTIGA",
    "MAPSEC_MIRAGE_TOWER": "TORRE MIRAGEM",
    "MAPSEC_ARTISAN_CAVE": "LAPA DO ARTESAO",    # a lapa is a rock shelter
    "MAPSEC_DESERT_UNDERPASS": "TUNEL DA AREIA",
    "MAPSEC_ALTERING_CAVE": "TOCA MUTAVEL",
    "MAPSEC_TRAINER_HILL": "MORRO DOS DUELOS",
    # LandmarkName_MagmaHideout is REMEMBRANCERS BASE, which is 18 characters
    # against MAP_NAME_LENGTH=16, so the map carries the short form.
    "MAPSEC_MAGMA_HIDEOUT": "REMEMBRANCERS",
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
