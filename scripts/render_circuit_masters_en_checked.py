#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "data/text/arauna/en/circuit_masters.json"
TRAINERS = ROOT / "src/data/trainers.h"
CLASSES = ROOT / "src/data/text/trainer_class_names.h"
BRAIN_TEXT = ROOT / "data/text/frontier_brain.inc"

MAP_FILES = [
    ROOT / "data/maps/BattleFrontier_OutsideWest/scripts.inc",
    ROOT / "data/maps/BattleFrontier_BattleTowerLobby/scripts.inc",
    ROOT / "data/maps/BattleFrontier_BattleTowerBattleRoom/scripts.inc",
    ROOT / "data/maps/BattleFrontier_Lounge2/scripts.inc",
    ROOT / "data/maps/BattleFrontier_BattleDomeLobby/scripts.inc",
    ROOT / "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.inc",
    ROOT / "data/maps/BattleFrontier_BattleDomeBattleRoom/scripts.inc",
    ROOT / "data/maps/BattleFrontier_BattleFactoryBattleRoom/scripts.inc",
    ROOT / "data/maps/BattleFrontier_BattlePikeRoomNormal/scripts.inc",
    ROOT / "data/maps/BattleFrontier_BattleArenaBattleRoom/scripts.inc",
    ROOT / "data/maps/BattleFrontier_BattlePalaceBattleRoom/scripts.inc",
    ROOT / "data/maps/BattleFrontier_BattlePyramidTop/scripts.inc",
]

OLD_TRAINER_NAMES = {
    "TRAINER_ANABEL": "ANABEL",
    "TRAINER_TUCKER": "TUCKER",
    "TRAINER_NOLAND": "NOLAND",
    "TRAINER_LUCY": "LUCY",
    "TRAINER_GRETA": "GRETA",
    "TRAINER_SPENSER": "SPENSER",
    "TRAINER_BRANDON": "BRANDON",
}

CLASS_OLD = {
    "TRAINER_CLASS_SALON_MAIDEN": "SALON MAIDEN",
    "TRAINER_CLASS_DOME_ACE": "DOME ACE",
    "TRAINER_CLASS_PALACE_MAVEN": "PALACE MAVEN",
    "TRAINER_CLASS_ARENA_TYCOON": "ARENA TYCOON",
    "TRAINER_CLASS_FACTORY_HEAD": "FACTORY HEAD",
    "TRAINER_CLASS_PIKE_QUEEN": "PIKE QUEEN",
    "TRAINER_CLASS_PYRAMID_KING": "PYRAMID KING",
}

QUOTE_LABELS = {
    f"gText_{name}{result}{tier}"
    for name in ("Anabel", "Tucker", "Noland", "Lucy", "Greta", "Spenser", "Brandon")
    for result in ("Won", "Defeat")
    for tier in ("Silver", "Gold")
}

STRING_LINE_RE = re.compile(r'(?m)^(?P<prefix>\s*\.string\s+")(?P<body>(?:[^"\\]|\\.)*)(?P<suffix>"\s*)$')


def fail(msg: str) -> None:
    raise SystemExit(f"Circuit Masters renderer: {msg}")


def load_bank() -> dict:
    data = json.loads(BANK.read_text(encoding="utf-8"))
    if set(data) != {"trainer_names", "visible_aliases", "trainer_class_display", "battle_quotes"}:
        fail("unexpected bank sections")
    if set(data["trainer_names"]) != set(OLD_TRAINER_NAMES):
        fail("trainer_names contract mismatch")
    expected_aliases = set(OLD_TRAINER_NAMES.values()) | set(CLASS_OLD.values())
    if set(data["visible_aliases"]) != expected_aliases:
        fail("visible_aliases contract mismatch")
    if set(data["battle_quotes"]) != QUOTE_LABELS:
        fail("battle quote contract mismatch")
    if data["trainer_class_display"] != "CIRCUIT MSTR":
        fail("trainer class display must be CIRCUIT MSTR")
    if len(data["trainer_class_display"]) > 12:
        fail("trainer class display exceeds 12 visible characters")
    for trainer_id, value in data["trainer_names"].items():
        if not value or len(value) > 12:
            fail(f"invalid trainer name for {trainer_id}: {value!r}")
    for label, segments in data["battle_quotes"].items():
        if not isinstance(segments, list) or not segments:
            fail(f"{label}: quote must be a non-empty list")
        for i, segment in enumerate(segments):
            visible = segment[:-1] if segment.endswith("$") else segment
            if len(visible) > 32:
                fail(f"{label}: segment wider than 32 chars: {visible!r}")
            if "$" in segment and not (i == len(segments) - 1 and segment.endswith("$")):
                fail(f"{label}: $ may appear only at the end")
        if not segments[-1].endswith("$"):
            fail(f"{label}: final segment must end with $")
    return data


def render_trainer_names(text: str, names: dict[str, str]) -> str:
    before = text
    for trainer_id, final in names.items():
        old = OLD_TRAINER_NAMES[trainer_id]
        rx = re.compile(
            rf'(\[{re.escape(trainer_id)}\]\s*=\s*\{{.*?\.trainerName\s*=\s*_\(")(?P<value>[^"]+)("\))',
            re.DOTALL,
        )
        matches = list(rx.finditer(text))
        if len(matches) != 1:
            fail(f"expected exactly one trainer block for {trainer_id}, found {len(matches)}")
        current = matches[0].group("value")
        if current not in {old, final}:
            fail(f"{trainer_id}: unexpected visible name {current!r}")
        text = rx.sub(lambda m: m.group(1) + final + m.group(3), text, count=1)
    # Prove that only the seven trainerName payloads changed.
    def mask(s: str) -> str:
        for trainer_id in names:
            rx = re.compile(
                rf'(\[{re.escape(trainer_id)}\]\s*=\s*\{{.*?\.trainerName\s*=\s*_")[^"]+("\))',
                re.DOTALL,
            )
            s = rx.sub(r'\1<MASTER_NAME>\2', s, count=1)
        return s
    if mask(before) != mask(text):
        fail("non-name bytes changed in src/data/trainers.h")
    return text


def render_class_names(text: str, final: str) -> str:
    before = text
    for class_id, old in CLASS_OLD.items():
        rx = re.compile(rf'(\[{re.escape(class_id)}\]\s*=\s*_\(")(?P<value>[^"]+)("\),)')
        matches = list(rx.finditer(text))
        if len(matches) != 1:
            fail(f"expected exactly one class entry for {class_id}, found {len(matches)}")
        current = matches[0].group("value")
        if current not in {old, final}:
            fail(f"{class_id}: unexpected visible class {current!r}")
        text = rx.sub(lambda m: m.group(1) + final + m.group(3), text, count=1)
    def mask(s: str) -> str:
        for class_id in CLASS_OLD:
            rx = re.compile(rf'(\[{re.escape(class_id)}\]\s*=\s*_")[^"]+("\),)')
            s = rx.sub(r'\1<MASTER_CLASS>\2', s, count=1)
        return s
    if mask(before) != mask(text):
        fail("non-class bytes changed in trainer_class_names.h")
    return text


def quote_block_rx(label: str) -> re.Pattern[str]:
    return re.compile(
        rf'(?ms)^(?P<label>{re.escape(label)}::\n)(?P<body>(?:\s*\.string\s+"(?:[^"\\]|\\.)*"\s*\n)+)'
    )


def render_brain_quotes(text: str, quotes: dict[str, list[str]]) -> str:
    before = text
    for label in sorted(quotes):
        rx = quote_block_rx(label)
        matches = list(rx.finditer(text))
        if len(matches) != 1:
            fail(f"expected exactly one quote block {label}, found {len(matches)}")
        segments = quotes[label]
        lines = []
        for i, segment in enumerate(segments):
            payload = segment if i == len(segments) - 1 else segment + r"\n"
            payload = payload.replace('"', r'\"')
            lines.append(f'\t.string "{payload}"\n')
        text = rx.sub(lambda m: m.group("label") + "".join(lines), text, count=1)
    def mask(s: str) -> str:
        for label in sorted(quotes):
            s = quote_block_rx(label).sub(lambda m: m.group("label") + "<MASTER_QUOTE>\n", s, count=1)
        return s
    if mask(before) != mask(text):
        fail("non-quote bytes changed in data/text/frontier_brain.inc")
    return text


def replace_aliases_in_strings(text: str, aliases: dict[str, str], path: Path) -> str:
    before = text
    touched = 0
    def repl(match: re.Match[str]) -> str:
        nonlocal touched
        body = match.group("body")
        new = body
        for old, final in aliases.items():
            new = new.replace(old, final)
        if new != body:
            touched += 1
        return match.group("prefix") + new + match.group("suffix")
    text = STRING_LINE_RE.sub(repl, text)

    def mask_strings(s: str) -> str:
        return STRING_LINE_RE.sub(lambda m: m.group("prefix") + "<STRING>" + m.group("suffix"), s)
    if mask_strings(before) != mask_strings(text):
        fail(f"non-string bytes changed in {path.relative_to(ROOT)}")
    # Only test stale aliases in visible string payloads, never in internal labels.
    payloads = "\n".join(m.group("body") for m in STRING_LINE_RE.finditer(text))
    stale = [old for old in aliases if old in payloads]
    if stale:
        fail(f"stale visible aliases remain in {path.relative_to(ROOT)}: {', '.join(stale)}")
    return text


def render_all(write: bool) -> None:
    bank = load_bank()
    targets: dict[Path, str] = {}
    targets[TRAINERS] = render_trainer_names(TRAINERS.read_text(encoding="utf-8"), bank["trainer_names"])
    targets[CLASSES] = render_class_names(CLASSES.read_text(encoding="utf-8"), bank["trainer_class_display"])
    targets[BRAIN_TEXT] = render_brain_quotes(BRAIN_TEXT.read_text(encoding="utf-8"), bank["battle_quotes"])
    for path in MAP_FILES:
        if not path.is_file():
            fail(f"missing target map file: {path.relative_to(ROOT)}")
        targets[path] = replace_aliases_in_strings(path.read_text(encoding="utf-8"), bank["visible_aliases"], path)

    # Final identity checks.
    trainers_out = targets[TRAINERS]
    for final in bank["trainer_names"].values():
        if f'.trainerName = _("{final}")' not in trainers_out:
            fail(f"missing final trainer name {final}")
    classes_out = targets[CLASSES]
    if classes_out.count(f'_("{bank["trainer_class_display"]}")') < 7:
        fail("not all seven Frontier Brain classes render as CIRCUIT MSTR")
    for old in OLD_TRAINER_NAMES.values():
        if old in "\n".join(m.group("body") for p in MAP_FILES for m in STRING_LINE_RE.finditer(targets[p])):
            fail(f"stale old master name remains visible: {old}")

    if write:
        for path, content in targets.items():
            path.write_text(content, encoding="utf-8")
    mode = "render" if write else "check"
    print(f"Circuit Masters {mode}: PASS (7 names, 7 classes, 28 quotes, {len(MAP_FILES)} map surfaces)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    render_all(args.in_place)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
