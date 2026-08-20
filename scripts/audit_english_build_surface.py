#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_WRAPPER = ROOT / "scripts" / "build_arauna.sh"

PORTUGUESE_MARKERS = re.compile(
    r"\b(?:"
    r"voce|voces|nao|entao|tambem|porque|quando|agora|isso|aqui|"
    r"recebeu|parabens|insignia|insignias|lider|campea|consorcio|"
    r"horizonte|lembrante|lembrantes|desencanto|vinculo|vinculos|"
    r"memoria|memorias|lembranca|lembrancas|familia|familias|"
    r"chegamos|obrigado|bem-vindo|cabine|derrotou|venceu|perdeu|"
    r"arquivo\s+vivo|pontos\s+de\s+batalha"
    r")\b",
    re.IGNORECASE,
)

LEGACY_HOENN = re.compile(
    r"\b(?:"
    r"HOENN|RUSTBORO|DEWFORD|MAUVILLE|VERDANTURF|FALLARBOR|LAVARIDGE|"
    r"FORTREE|LILYCOVE|MOSSDEEP|SOOTOPOLIS|PACIFIDLOG|EVER\s+GRANDE|"
    r"PETALBURG|SLATEPORT|LITTLEROOT|OLDALE|DEVON|"
    r"TEAM\s+AQUA|TEAM\s+MAGMA|ROXANNE|BRAWLY|WATTSON|FLANNERY|"
    r"NORMAN|WINONA|JUAN|WALLACE|TATE\s*(?:&|AND)\s*LIZA|"
    r"TRICK\s+HOUSE|TRICK\s+MASTER|BATTLE\s+FRONTIER|FRONTIER\s+PASS|"
    r"FRONTIER\s+BRAIN|MR\.?\s+BRINEY|MR\.?\s+SCOTT|\bSCOTT\b"
    r")\b",
    re.IGNORECASE,
)

ASM_STRING = re.compile(r'^\s*\.string\s+"(?P<text>(?:\\.|[^"\\])*)"', re.MULTILINE)
C_STRING = re.compile(r'_\("(?P<text>(?:\\.|[^"\\])*)"\)')

SKIP_RUNTIME_PREFIXES = (
    "data/text/arauna/pt_br/",  # dormant historical bank; official selector cannot reach it
)


def extract_overlay_files(build_text: str) -> list[str]:
    match = re.search(r"(?ms)^overlay_files=\(\n(?P<body>.*?)^\)\s*$", build_text)
    if not match:
        raise ValueError("could not parse overlay_files from build_arauna.sh")
    files = re.findall(r'^\s*"([^"]+)"\s*$', match.group("body"), re.MULTILINE)
    if not files:
        raise ValueError("overlay_files list is empty")

    # build_arauna.sh appends this glob dynamically. Mirror it here exactly so
    # the audit can never leave rendered Battle Circuit maps behind.
    frontier_files = sorted(
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "data" / "maps").glob("BattleFrontier_*/scripts.inc")
        if path.is_file()
    )
    return list(dict.fromkeys(files + frontier_files))


def extract_renderers(build_text: str) -> list[str]:
    renderers = re.findall(
        r"(?m)^python3\s+(scripts/render_[^\s]+\.py)\s+--in-place\s*$",
        build_text,
    )
    if not renderers:
        raise ValueError("no active renderers found in build_arauna.sh")
    return renderers


def is_runtime_candidate(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return path.is_file() and not any(rel.startswith(prefix) for prefix in SKIP_RUNTIME_PREFIXES)


def iter_runtime_files(overlays: list[str]) -> list[Path]:
    # Match the old full residue auditor's coverage, but scan only literal text
    # after the official English render stack has been applied.
    files: set[Path] = set()
    for glob in (
        "data/maps/**/scripts.inc",
        "data/text/**/*.inc",
        "data/scripts/**/*.inc",
        "src/**/*.c",
        "src/**/*.h",
    ):
        files.update(path for path in ROOT.glob(glob) if is_runtime_candidate(path))
    files.update(
        ROOT / rel
        for rel in overlays
        if (ROOT / rel).is_file() and is_runtime_candidate(ROOT / rel)
    )
    return sorted(files)


def visible_literals(path: Path, text: str):
    regex = ASM_STRING if path.suffix == ".inc" else C_STRING
    for match in regex.finditer(text):
        literal = match.group("text")
        line = text.count("\n", 0, match.start()) + 1
        yield line, literal


def scan_runtime(overlays: list[str]) -> list[tuple[str, int, str, str]]:
    findings: list[tuple[str, int, str, str]] = []
    for path in iter_runtime_files(overlays):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        for line, literal in visible_literals(path, text):
            for kind, regex in (("portuguese", PORTUGUESE_MARKERS), ("legacy-hoenn", LEGACY_HOENN)):
                if regex.search(literal):
                    findings.append((rel, line, kind, literal))
                    break
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply the official English render stack transactionally, scan all visible runtime strings, then restore the tree."
    )
    parser.add_argument("--keep-rendered", action="store_true", help="Do not restore overlays after the audit (debug only).")
    args = parser.parse_args()

    build_text = BUILD_WRAPPER.read_text(encoding="utf-8")
    overlays = extract_overlay_files(build_text)
    renderers = extract_renderers(build_text)

    missing = [rel for rel in overlays if not (ROOT / rel).is_file()]
    if missing:
        raise SystemExit("Missing overlay files:\n" + "\n".join(f"- {rel}" for rel in missing))
    missing_renderers = [rel for rel in renderers if not (ROOT / rel).is_file()]
    if missing_renderers:
        raise SystemExit("Missing active renderers:\n" + "\n".join(f"- {rel}" for rel in missing_renderers))

    backup_root = Path(tempfile.mkdtemp(prefix="arauna-en-audit-"))
    try:
        for rel in overlays:
            src = ROOT / rel
            dst = backup_root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

        for rel in renderers:
            subprocess.run([sys.executable, rel, "--in-place"], cwd=ROOT, check=True)

        findings = scan_runtime(overlays)
        if findings:
            print(f"English build-surface audit: FAIL ({len(findings)} visible residue findings)")
            for rel, line, kind, literal in findings:
                print(f"{rel}:{line}: [{kind}] {literal}")
            return 1

        runtime_files = iter_runtime_files(overlays)
        print(
            "English build-surface audit: OK "
            f"({len(renderers)} renderers; {len(overlays)} transactional overlays; "
            f"{len(runtime_files)} runtime files scanned)."
        )
        return 0
    finally:
        if args.keep_rendered:
            print(f"Rendered tree retained; backup left at {backup_root}")
        else:
            for rel in overlays:
                shutil.copy2(backup_root / rel, ROOT / rel)
            shutil.rmtree(backup_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
