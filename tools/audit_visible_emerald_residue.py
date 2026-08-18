#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCAN_PATHS = (
    ROOT / "data" / "maps",
    ROOT / "data" / "text",
    ROOT / "data" / "scripts",
    ROOT / "data" / "event_scripts.s",
    ROOT / "src" / "strings.c",
    ROOT / "src" / "battle_message.c",
)

TOKENS = (
    # Legacy named characters / factions that should not leak to the player.
    "MAY",
    "BRENDAN",
    "PROF. BIRCH",
    "BIRCH",
    "STEVEN",
    "WALLY",
    "ARCHIE",
    "MAXIE",
    "SCOTT",
    "ROXANNE",
    "BRAWLY",
    "WATTSON",
    "FLANNERY",
    "NORMAN",
    "WINONA",
    "JUAN",
    "WALLACE",
    "TATE",
    "LIZA",
    "TEAM AQUA",
    "TEAM MAGMA",
    "DEVON",
    # Legacy Hoenn place / region surface names.
    "HOENN",
    "LITTLEROOT",
    "OLDALE",
    "DEWFORD",
    "LAVARIDGE",
    "FALLARBOR",
    "VERDANTURF",
    "PACIFIDLOG",
    "PETALBURG",
    "SLATEPORT",
    "MAUVILLE",
    "RUSTBORO",
    "FORTREE",
    "LILYCOVE",
    "MOSSDEEP",
    "SOOTOPOLIS",
    "EVER GRANDE",
    "GRANITE CAVE",
    "MT. CHIMNEY",
    "RUSTURF TUNNEL",
    "METEOR FALLS",
    "MT. PYRE",
    "SEAFLOOR CAVERN",
    "VICTORY ROAD",
    "SKY PILLAR",
)

ASM_STRING_RE = re.compile(r'^\s*\.string\s+"(?P<text>.*)"\s*$')
C_STRING_RE = re.compile(r'_\("(?P<text>(?:[^"\\]|\\.)*)"\)')


def iter_files(path: Path):
    if path.is_file():
        yield path
        return
    if not path.exists():
        return
    for candidate in sorted(path.rglob("*")):
        if candidate.is_file() and candidate.suffix in {".inc", ".s", ".c"}:
            yield candidate


def visible_fragments(line: str) -> list[str]:
    fragments: list[str] = []
    asm = ASM_STRING_RE.match(line.rstrip("\n"))
    if asm:
        fragments.append(asm.group("text"))
    fragments.extend(match.group("text") for match in C_STRING_RE.finditer(line))
    return fragments


def audit() -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    seen_files: set[Path] = set()
    for scan_path in SCAN_PATHS:
        for path in iter_files(scan_path):
            if path in seen_files:
                continue
            seen_files.add(path)
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except UnicodeDecodeError:
                continue
            for lineno, line in enumerate(lines, 1):
                for fragment in visible_fragments(line):
                    upper = fragment.upper()
                    matched = sorted({token for token in TOKENS if token in upper})
                    if not matched:
                        continue
                    hits.append(
                        {
                            "path": str(path.relative_to(ROOT)),
                            "line": lineno,
                            "tokens": matched,
                            "text": fragment,
                        }
                    )
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit player-facing string literals for visible Emerald/Hoenn identity residue."
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument(
        "--fail-on-hit",
        action="store_true",
        help="Exit non-zero when visible legacy tokens are found.",
    )
    args = parser.parse_args()

    hits = audit()
    if args.json:
        print(json.dumps(hits, ensure_ascii=False, indent=2))
    else:
        if not hits:
            print("Visible Emerald residue audit: PASS (0 legacy player-facing hits).")
        else:
            print(f"Visible Emerald residue audit: {len(hits)} player-facing hit(s).")
            for hit in hits:
                tokens = ", ".join(hit["tokens"])
                print(f"{hit['path']}:{hit['line']}: [{tokens}] {hit['text']}")

    return 1 if hits and args.fail_on_hit else 0


if __name__ == "__main__":
    raise SystemExit(main())
