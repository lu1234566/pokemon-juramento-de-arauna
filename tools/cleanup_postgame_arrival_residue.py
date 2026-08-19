#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from postgame_arrival_targets import RECEPTION_TARGETS, SSTIDAL_TARGETS

ROOT = Path(__file__).resolve().parents[1]
TARGETS_BY_FILE = {
    ROOT / "data" / "maps" / "SSTidalCorridor" / "scripts.inc": SSTIDAL_TARGETS,
    ROOT / "data" / "maps" / "BattleFrontier_ReceptionGate" / "scripts.inc": RECEPTION_TARGETS,
}
MAX_VISIBLE_WIDTH = 32
PLACEHOLDER_WIDTHS = {"{PLAYER}": 7, "{KUN}": 0, "{STR_VAR_1}": 10}
REQUIRED_INTERNAL = {
    "SSTidalCorridor/scripts.inc": (
        "VAR_SS_TIDAL_SCOTT_STATE", "VAR_SS_TIDAL_STATE", "LOCALID_SS_TIDAL_SCOTT",
        "FLAG_MET_SCOTT_ON_SS_TIDAL", "MAP_LILYCOVE_CITY_HARBOR",
        "MAP_SLATEPORT_CITY_HARBOR", "TRAINER_PHILLIP", "TRAINER_NAOMI",
    ),
    "BattleFrontier_ReceptionGate/scripts.inc": (
        "VAR_HAS_ENTERED_BATTLE_FRONTIER", "FLAG_SYS_FRONTIER_PASS",
        "LOCALID_FRONTIER_RECEPTION_SCOTT", "SCROLL_MULTI_BF_RECEPTIONIST",
        "MULTI_FRONTIER_RULES", "MULTI_FRONTIER_PASS_INFO",
    ),
}
FORBIDDEN = (
    "SCOTT:", "MR. SCOTT", "BATTLE FRONTIER", "FRONTIER PASS",
    "SLATEPORT CITY", "LILYCOVE CITY", "MR. BRINEY", "S.S. TIDAL",
)


def render(label: str, lines: tuple[str, ...]) -> str:
    return label + ":\n" + "".join(f'\t.string "{line}"\n' for line in lines)


def bounds(text: str, label: str) -> tuple[int, int]:
    marker = label + ":\n"
    start = text.find(marker)
    if start < 0:
        raise RuntimeError(f"Missing text block: {label}")
    end = text.find("\n\n", start)
    return start, len(text) if end < 0 else end + 1


def extract(text: str, label: str) -> str:
    start, end = bounds(text, label)
    return text[start:end]


def visible_width(segment: str) -> int:
    visible = segment
    for token, width in PLACEHOLDER_WIDTHS.items():
        visible = visible.replace(token, "X" * width)
    visible = re.sub(r"\{[^}]+\}", "", visible)
    return len(visible.replace("$", ""))


def validate_file(path: Path, text: str, targets: dict[str, tuple[str, ...]]) -> list[str]:
    failures: list[str] = []
    key = f"{path.parent.name}/{path.name}"
    for sentinel in REQUIRED_INTERNAL[key]:
        if sentinel not in text:
            failures.append(f"{key}: missing internal sentinel {sentinel}")
    for label, lines in targets.items():
        block = extract(text, label)
        if block != render(label, lines):
            failures.append(f"{key}: non-canonical block {label}")
        for token in FORBIDDEN:
            if token in block:
                failures.append(f"{key}: legacy visible token {token} in {label}")
        for segment in re.split(r"\\[npl]", "".join(lines)):
            if segment and visible_width(segment) > MAX_VISIBLE_WIDTH:
                failures.append(f"{key}: line wider than 32 in {label}: {segment!r}")
    return failures


def apply() -> int:
    changed = 0
    for path, targets in TARGETS_BY_FILE.items():
        text = path.read_text(encoding="utf-8")
        for label, lines in targets.items():
            start, end = bounds(text, label)
            replacement = render(label, lines)
            if text[start:end] != replacement:
                text = text[:start] + replacement + text[end:]
                changed += 1
        failures = validate_file(path, text, targets)
        if failures:
            raise RuntimeError("; ".join(failures))
        path.write_text(text, encoding="utf-8")
    print(f"Post-game arrival cleanup: {changed} changed; {sum(map(len, TARGETS_BY_FILE.values()))} verified.")
    return 0


def check() -> int:
    failures: list[str] = []
    for path, targets in TARGETS_BY_FILE.items():
        failures.extend(validate_file(path, path.read_text(encoding="utf-8"), targets))
    if failures:
        print("Post-game arrival cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Post-game arrival cleanup check PASS: {sum(map(len, TARGETS_BY_FILE.values()))} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    return check() if parser.parse_args().check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
