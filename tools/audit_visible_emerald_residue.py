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
ASM_LABEL_RE = re.compile(r'^\s*(?P<label>[A-Za-z0-9_.$]+)::?\s*$')
C_STRING_RE = re.compile(r'_\("(?P<text>(?:[^"\\]|\\.)*)"\)')
TOKEN_PATTERNS = {
    token: re.compile(rf"(?<![A-Z0-9]){re.escape(token)}(?![A-Z0-9])")
    for token in TOKENS
}


def iter_files(path: Path):
    if path.is_file():
        yield path
        return
    if not path.exists():
        return
    for candidate in sorted(path.rglob("*")):
        if candidate.is_file() and candidate.suffix in {".inc", ".s", ".c"}:
            yield candidate


def match_tokens(fragment: str) -> list[str]:
    upper = fragment.upper()
    return sorted(token for token, pattern in TOKEN_PATTERNS.items() if pattern.search(upper))


def audit_asm_file(path: Path, lines: list[str]) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    current_label = ""
    for lineno, line in enumerate(lines, 1):
        label_match = ASM_LABEL_RE.match(line)
        if label_match:
            current_label = label_match.group("label")
            continue
        asm_match = ASM_STRING_RE.match(line)
        if not asm_match:
            continue
        if "unused" in current_label.lower():
            continue
        fragment = asm_match.group("text")
        matched = match_tokens(fragment)
        if not matched:
            continue
        hits.append(
            {
                "path": str(path.relative_to(ROOT)),
                "line": lineno,
                "label": current_label or None,
                "tokens": matched,
                "text": fragment,
            }
        )
    return hits


def audit_c_file(path: Path, lines: list[str]) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    for lineno, line in enumerate(lines, 1):
        if "unused" in line.lower():
            continue
        for match in C_STRING_RE.finditer(line):
            fragment = match.group("text")
            matched = match_tokens(fragment)
            if not matched:
                continue
            hits.append(
                {
                    "path": str(path.relative_to(ROOT)),
                    "line": lineno,
                    "label": None,
                    "tokens": matched,
                    "text": fragment,
                }
            )
    return hits


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
            if path.suffix in {".inc", ".s"}:
                hits.extend(audit_asm_file(path, lines))
            elif path.suffix == ".c":
                hits.extend(audit_c_file(path, lines))
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
                label = f" {hit['label']}" if hit.get("label") else ""
                print(f"{hit['path']}:{hit['line']}:{label} [{tokens}] {hit['text']}")

    return 1 if hits and args.fail_on_hit else 0


if __name__ == "__main__":
    raise SystemExit(main())
