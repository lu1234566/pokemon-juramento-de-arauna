#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from render_arauna_frontier_ui import render as render_frontier_ui

ROOT = Path(__file__).resolve().parents[1]
ASM_GLOBS = (
    "data/maps/**/scripts.inc",
    "data/text/**/*.inc",
    "data/scripts/**/*.inc",
)
C_GLOBS = ("src/**/*.c", "src/**/*.h")
SKIP_PREFIXES = ("data/text/arauna/en/",)

LEGACY_MARKERS = {
    "SCOTT": "character",
    "BIRCH": "character",
    "BRENDAN": "character",
    "MAY": "character",
    "WALLY": "character",
    "NORMAN": "character",
    "HOENN": "region",
    "LITTLEROOT": "place",
    "SLATEPORT": "place",
    "LILYCOVE": "place",
    "RUSTBORO": "place",
    "MAUVILLE": "place",
    "BATTLE FRONTIER": "postgame",
    "FRONTIER PASS": "postgame",
    "FRONTIER BRAIN": "postgame",
    "TEAM AQUA": "faction",
    "TEAM MAGMA": "faction",
    "TRICK MASTER": "character",
    "DEVON": "organization",
}

ENGLISH_WORDS = {
    "the", "you", "your", "is", "are", "this", "that", "to", "and", "of",
    "in", "for", "with", "have", "has", "will", "can", "from", "here",
    "there", "what", "when", "where", "trainer", "trainers", "battle",
    "received", "obtained", "welcome", "please", "come", "take", "get",
}
PORTUGUESE_WORDS = {
    "voce", "nao", "que", "de", "do", "da", "para", "com", "uma", "um",
    "seu", "sua", "aqui", "isso", "esta", "em", "por", "mais", "como",
    "quando", "onde", "recebeu", "batalha", "treinador", "treinadores",
}
TOKEN_RE = re.compile(r"[A-Za-zÀ-ÿ]+")
LABEL_RE = re.compile(r"^([A-Za-z0-9_]+):\s*$")
ASM_STRING_RE = re.compile(r'^\s*\.string\s+"(.*)"\s*$')
C_STRING_RE = re.compile(r'_\("((?:[^"\\]|\\.)*)"\)')
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


@dataclass(frozen=True)
class Finding:
    priority: str
    category: str
    path: str
    label: str
    markers: tuple[str, ...]
    sample: str


def clean_visible(text: str) -> str:
    text = PLACEHOLDER_RE.sub(" ", text)
    text = re.sub(r"\\[npl]", " ", text)
    text = text.replace("$", " ")
    return re.sub(r"\s+", " ", text).strip()


def classify(text: str) -> tuple[str, str, tuple[str, ...]] | None:
    visible = clean_visible(text)
    upper = visible.upper()
    markers = tuple(marker for marker in LEGACY_MARKERS if marker in upper)
    if markers:
        cats = sorted({LEGACY_MARKERS[m] for m in markers})
        return "P0", "+".join(cats), markers

    words = [w.lower() for w in TOKEN_RE.findall(visible)]
    en = sum(word in ENGLISH_WORDS for word in words)
    pt = sum(word in PORTUGUESE_WORDS for word in words)
    if en >= 3 and pt <= 1:
        return "P1", "english", ()
    return None


def scan_asm(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    current_label = "<unlabeled>"
    fragments: list[str] = []

    def flush() -> None:
        nonlocal fragments
        if not fragments:
            return
        joined = "".join(fragments)
        result = classify(joined)
        if result:
            priority, category, markers = result
            findings.append(Finding(
                priority, category, path.relative_to(ROOT).as_posix(),
                current_label, markers, clean_visible(joined)[:180],
            ))
        fragments = []

    for raw in path.read_text(encoding="utf-8").splitlines():
        label = LABEL_RE.match(raw)
        if label:
            flush()
            current_label = label.group(1)
            continue
        match = ASM_STRING_RE.match(raw)
        if match:
            fragments.append(match.group(1))
        elif fragments and raw.strip() and not raw.lstrip().startswith(".string"):
            flush()
    flush()
    return findings


def scan_c(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    source = path.read_text(encoding="utf-8")
    if path == ROOT / "src" / "strings.c":
        source = render_frontier_ui(source)

    for number, raw in enumerate(source.splitlines(), 1):
        for match in C_STRING_RE.finditer(raw):
            text = match.group(1)
            result = classify(text)
            if not result:
                continue
            priority, category, markers = result
            findings.append(Finding(
                priority, category, path.relative_to(ROOT).as_posix(),
                f"line:{number}", markers, clean_visible(text)[:180],
            ))
    return findings


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return any(rel.startswith(prefix) for prefix in SKIP_PREFIXES)


def discover() -> list[Finding]:
    asm_files: set[Path] = set()
    c_files: set[Path] = set()
    for pattern in ASM_GLOBS:
        asm_files.update(ROOT.glob(pattern))
    for pattern in C_GLOBS:
        c_files.update(ROOT.glob(pattern))

    findings: list[Finding] = []
    for path in sorted(asm_files):
        if not should_skip(path):
            findings.extend(scan_asm(path))
    for path in sorted(c_files):
        if not should_skip(path):
            findings.extend(scan_c(path))
    return sorted(findings, key=lambda x: (x.priority, x.path, x.label))


def markdown(findings: list[Finding]) -> str:
    counts = {p: sum(f.priority == p for f in findings) for p in ("P0", "P1")}
    lines = [
        "# Inventario de residuos visiveis do Emerald",
        "",
        "> Gerado por `scripts/audit_visible_residue.py`. Nao altera arquivos do jogo.",
        "",
        f"- P0 (conflito canonico): {counts['P0']}",
        f"- P1 (ingles provavel): {counts['P1']}",
        "",
        "| Prioridade | Categoria | Arquivo | Label | Marcadores | Amostra |",
        "|---|---|---|---|---|---|",
    ]
    for f in findings:
        sample = f.sample.replace("|", "\\|")
        markers = ", ".join(f.markers) if f.markers else "-"
        lines.append(
            f"| {f.priority} | {f.category} | `{f.path}` | `{f.label}` | {markers} | {sample} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", dest="json_output", type=Path)
    args = parser.parse_args()

    findings = discover()
    report = markdown(findings)
    if args.output:
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    if args.json_output:
        args.json_output.write_text(
            json.dumps([asdict(f) for f in findings], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
