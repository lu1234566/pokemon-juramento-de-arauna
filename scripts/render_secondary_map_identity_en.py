#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGION = ROOT / "src" / "data" / "region_map" / "region_map_sections.json"
LANDMARK = ROOT / "src" / "landmark.c"
MAP_NAME_LENGTH = 16

REGION_NAMES = {
    "MAPSEC_BATTLE_FRONTIER": "CIRCUITO BATALHA",
    "MAPSEC_PETALBURG_WOODS": "MATA DA ESPERA",
    "MAPSEC_ABANDONED_SHIP": "NAVIO ABANDONADO",
    "MAPSEC_NEW_MAUVILLE": "SUBSOLO CENTRAL",
    "MAPSEC_FIERY_PATH": "TRILHA DE CINZA",
    "MAPSEC_FIERY_PATH2": "TRILHA DE CINZA",
    "MAPSEC_JAGGED_PASS": "PASSO DA CINZA",
    "MAPSEC_JAGGED_PASS2": "PASSO DA CINZA",
    "MAPSEC_MAGMA_HIDEOUT": "BASE LEMBRANTES",
    "MAPSEC_AQUA_HIDEOUT": "ARQUIVO CENTRAL",
}

LANDMARK_NAMES = {
    "LandmarkName_PetalburgWoods": "MATA DA ESPERA",
    "LandmarkName_MrBrineysCottage": "VETERAN'S COTTAGE",
    "LandmarkName_AbandonedShip": "NAVIO ABANDONADO",
    "LandmarkName_SlateportBeach": "PRAIA PORTO SAL",
    "LandmarkName_NewMauville": "SUBSOLO CENTRAL",
    "LandmarkName_MeteorFalls": "RUINAS DA QUEDA",
    "LandmarkName_RusturfTunnel": "GALERIAS SERRA",
    "LandmarkName_MtPyre": "MEMORIAL NOMES",
    "LandmarkName_SeafloorCavern": "CAVERNAS M'BOI",
    "LandmarkName_GraniteCave": "GRUTA DAS VOZES",
    "LandmarkName_FieryPath": "TRILHA DE CINZA",
    "LandmarkName_JaggedPass": "PASSO DA CINZA",
    "LandmarkName_SkyPillar": "TORRE JURAMENTO",
    "LandmarkName_MagmaHideout": "BASE LEMBRANTES",
}


def region_pattern(mapsec: str) -> re.Pattern[str]:
    return re.compile(
        rf'(?P<prefix>"id":\s*"{re.escape(mapsec)}",\s*\n\s*"name":\s*")[^"]*(?P<suffix>")',
        re.MULTILINE,
    )


def render_region(source: str) -> str:
    out = source
    for mapsec, name in REGION_NAMES.items():
        if len(name) > MAP_NAME_LENGTH:
            raise ValueError(f"{mapsec}: {name!r} exceeds {MAP_NAME_LENGTH} chars")
        rx = region_pattern(mapsec)
        matches = list(rx.finditer(out))
        if len(matches) != 1:
            raise ValueError(f"{mapsec}: expected one region-map entry, found {len(matches)}")
        out = rx.sub(lambda m: m.group("prefix") + name + m.group("suffix"), out, count=1)
    return out


def render_landmarks(source: str) -> str:
    out = source
    for symbol, name in LANDMARK_NAMES.items():
        rx = re.compile(
            rf'(?m)^(?P<prefix>static const u8 {re.escape(symbol)}\[\] = _\(")[^"]*(?P<suffix>"\);)$'
        )
        matches = list(rx.finditer(out))
        if len(matches) != 1:
            raise ValueError(f"{symbol}: expected one landmark declaration, found {len(matches)}")
        out = rx.sub(lambda m: m.group("prefix") + name + m.group("suffix"), out, count=1)
    return out


def validate(region: str, landmarks: str) -> None:
    for mapsec, name in REGION_NAMES.items():
        match = region_pattern(mapsec).search(region)
        if not match or name not in match.group(0):
            raise ValueError(f"{mapsec}: rendered map name missing")
    for symbol, name in LANDMARK_NAMES.items():
        target = f'static const u8 {symbol}[] = _("{name}");'
        if target not in landmarks:
            raise ValueError(f"{symbol}: rendered landmark missing")
    for token in (
        "MAPSEC_BATTLE_FRONTIER",
        "MAPSEC_PETALBURG_WOODS",
        "MAPSEC_MAGMA_HIDEOUT",
        "Landmark_PetalburgWoods",
        "Landmark_MagmaHideout",
        "FLAG_LANDMARK_ABANDONED_SHIP",
    ):
        if token not in region and token not in landmarks:
            raise ValueError(f"inherited identity token disappeared: {token}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("choose --check or --in-place")

    region_source = REGION.read_text(encoding="utf-8")
    landmark_source = LANDMARK.read_text(encoding="utf-8")
    region_out = render_region(region_source)
    landmark_out = render_landmarks(landmark_source)
    validate(region_out, landmark_out)

    if args.in_place:
        if region_out != region_source:
            REGION.write_text(region_out, encoding="utf-8")
        if landmark_out != landmark_source:
            LANDMARK.write_text(landmark_out, encoding="utf-8")

    print(
        "Secondary map identity OK: "
        f"{len(REGION_NAMES)} region headers + {len(LANDMARK_NAMES)} landmarks."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
