#!/usr/bin/env python3
"""Build the 386-slot Arauna art-production manifest from the supplied Dex export."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from PIL import Image


ASSET_FIELDS = ("front", "back", "icon", "shiny", "animation")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dex", type=Path, required=True)
    parser.add_argument("--sprites", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    payload = json.loads(args.dex.read_text(encoding="utf-8"))
    pokemon = payload.get("pokemon", [])
    if len(pokemon) != 386:
        raise SystemExit(f"expected 386 Dex entries, found {len(pokemon)}")

    rows = []
    for expected_id, entry in enumerate(pokemon, start=1):
        number = int(entry["id"])
        if number != expected_id:
            raise SystemExit(f"Dex sequence mismatch: expected {expected_id}, found {number}")

        source_name = Path(entry.get("spriteFile") or "").name
        source_path = args.sprites / source_name if source_name else None
        has_reference = bool(source_path and source_path.is_file())
        width = height = mode = ""
        if has_reference:
            with Image.open(source_path) as image:
                width, height = image.size
                mode = image.mode

        row = {
            "dex": f"{number:03d}",
            "name": entry["name"],
            "types": "/".join(entry.get("types", [])),
            "biome_or_region": entry.get("region", ""),
            "reference_file": source_name if has_reference else "",
            "reference_status": "available" if has_reference else "missing",
            "reference_width": width,
            "reference_height": height,
            "reference_mode": mode,
            "production_status": "pilot-awaiting-approval" if number in (1, 4, 7) else "queued" if has_reference else "blocked-no-reference",
        }
        for field in ASSET_FIELDS:
            row[f"needs_{field}"] = "candidate-awaiting-approval" if number in (1, 4, 7) else "yes"
        rows.append(row)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    available = sum(row["reference_status"] == "available" for row in rows)
    missing = len(rows) - available
    print(f"wrote {args.out}: total={len(rows)}, references={available}, missing={missing}")


if __name__ == "__main__":
    main()
