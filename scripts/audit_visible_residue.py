#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from render_aguas_mboi_daily_surface import (
    render_berries as render_aguas_berries,
    render_city as render_aguas_mboi,
    render_tower as render_torre_outside,
)
from render_arauna_frontier_ui import render as render_frontier_ui
from render_arquivo_central_surface import render_b1f as render_arquivo_b1f, render_b2f as render_arquivo_b2f
from render_lembrantes_core_surface import render_3f1 as render_lembrantes_3f1, render_3f2 as render_lembrantes_3f2, render_4f as render_lembrantes_4f
from render_lembrantes_lower_surface import render_1f as render_lembrantes_1f, render_2f1 as render_lembrantes_2f1, render_2f2 as render_lembrantes_2f2
from render_mt_chimney_surface import render as render_mt_chimney
from render_petalburg_woods_surface import render as render_petalburg_woods
from render_ruinas_memorial_surface_checked import (
    render_item_descs,
    render_items,
    render_memorial,
    render_meteor,
)

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
    "MAGMA EMBLEM": "faction",
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


def render_asm_source(path: Path, source: str) -> str:
    if path == ROOT / "data" / "maps" / "PetalburgWoods" / "scripts.inc":
        return render_petalburg_woods(source)
    if path == ROOT / "data" / "maps" / "MtChimney" / "scripts.inc":
        return render_mt_chimney(source)
    if path == ROOT / "data" / "maps" / "MeteorFalls_1F_1R" / "scripts.inc":
        return render_meteor(source)
    if path == ROOT / "data" / "maps" / "MtPyre_Summit" / "scripts.inc":
        return render_memorial(source)
    if path == ROOT / "data" / "maps" / "AquaHideout_B1F" / "scripts.inc":
        return render_arquivo_b1f(source)
    if path == ROOT / "data" / "maps" / "AquaHideout_B2F" / "scripts.inc":
        return render_arquivo_b2f(source)
    if path == ROOT / "data" / "maps" / "SootopolisCity" / "scripts.inc":
        return render_aguas_mboi(source)
    if path == ROOT / "data" / "maps" / "SkyPillar_Outside" / "scripts.inc":
        return render_torre_outside(source)
    if path == ROOT / "data" / "maps" / "MagmaHideout_1F" / "scripts.inc":
        return render_lembrantes_1f(source)
    if path == ROOT / "data" / "maps" / "MagmaHideout_2F_1R" / "scripts.inc":
        return render_lembrantes_2f1(source)
    if path == ROOT / "data" / "maps" / "MagmaHideout_2F_2R" / "scripts.inc":
        return render_lembrantes_2f2(source)
    if path == ROOT / "data" / "maps" / "MagmaHideout_3F_1R" / "scripts.inc":
        return render_lembrantes_3f1(source)
    if path == ROOT / "data" / "maps" / "MagmaHideout_3F_2R" / "scripts.inc":
        return render_lembrantes_3f2(source)
    if path == ROOT / "data" / "maps" / "MagmaHideout_4F" / "scripts.inc":
        return render_lembrantes_4f(source)
    if path == ROOT / "data" / "text" / "berries.inc":
        return render_aguas_berries(source)
    return source


def render_c_source(path: Path, source: str) -> str:
    if path == ROOT / "src" / "strings.c":
        return render_frontier_ui(source)
    if path == ROOT / "src" / "data" / "items.h":
        return render_items(source)
    if path == ROOT / "src" / "data" / "text" / "item_descriptions.h":
        return render_item_descs(source)
    return source


def scan_asm(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    current_label = "<unlabeled>"
    fragments: list[str] = []
    source = render_asm_source(path, path.read_text(encoding="utf-8"))

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

    for raw in source.splitlines():
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
    source = render_c_source(path, path.read_text(encoding="utf-8"))

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
