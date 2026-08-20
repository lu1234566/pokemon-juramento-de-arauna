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
    r"RUSTBORO|DEWFORD|MAUVILLE|VERDANTURF|FALLARBOR|LAVARIDGE|"
    r"FORTREE|LILYCOVE|MOSSDEEP|SOOTOPOLIS|PACIFIDLOG|EVER\s+GRANDE|"
    r"PETALBURG|SLATEPORT|LITTLEROOT|OLDALE|DEVON|"
    r"TEAM\s+AQUA|TEAM\s+MAGMA|ROXANNE|BRAWLY|WATTSON|FLANNERY|"
    r"NORMAN|WINONA|JUAN|WALLACE|TATE\s*(?:&|AND)\s*LIZA"
    r")\b",
    re.IGNORECASE,
)

ASM_STRING = re.compile(r'^\s*\.string\s+"(?P<text>(?:\\.|[^"\\])*)"', re.MULTILINE)
C_STRING = re.compile(r'_\("(?P<text>(?:\\.|[^"\\])*)"\)')


def extract_overlay_files(build_text: str) -> list[str]:
    match = re.search(r"(?ms)^overlay_files=\(\n(?P<body>.*?)^\)\s*$", build_text)
    if not match:
        raise ValueError("could not parse overlay_files from build_arauna.sh")
    files = re.findall(r'^\s*"([^"]+)"\s*$', match.group("body"), re.MULTILINE)
    if not files:
        raise ValueError("overlay_files list is empty")
    return files


def extract_renderers(build_text: str) -> list[str]:
    renderers = re.findall(
        r"(?m)^python3\s+(scripts/render_[^\s]+\.py)\s+--in-place\s*$",
        build_text,
    )
    if not renderers:
        raise ValueError("no active renderers found in build_arauna.sh")
    return renderers


def iter_runtime_files() -> list[Path]:
    files = sorted((ROOT / "data" / "maps").glob("**/scripts.inc"))
    files.extend(
        path
        for path in (
            ROOT / "src" / "strings.c",
            ROOT / "src" / "data" / "trainers.h",
            ROOT / "src" / "data" / "text" / "trainer_class_names.h",
            ROOT / "data" / "text" / "berries.inc",
            ROOT / "src" / "data" / "items.h",
            ROOT / "src" / "data" / "text" / "item_descriptions.h",
        )
        if path.is_file()
    )
    return files


def visible_literals(path: Path, text: str):
    regex = ASM_STRING if path.suffix == ".inc" else C_STRING
    for match in regex.finditer(text):
        literal = match.group("text")
        line = text.count("\n", 0, match.start()) + 1
        yield line, literal


def scan_runtime() -> list[tuple[str, int, str, str]]:
    findings: list[tuple[str, int, str, str]] = []
    for path in iter_runtime_files():
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        for line, literal in visible_literals(path, text):
            for kind, regex in (("portuguese", PORTUGUESE_MARKERS), ("legacy-hoenn", LEGACY_HOENN)):
                match = regex.search(literal)
                if match:
                    findings.append((rel, line, kind, literal))
                    break
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply the official English render stack transactionally, scan visible runtime strings, then restore the tree."
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

        findings = scan_runtime()
        if findings:
            print(f"English build-surface audit: FAIL ({len(findings)} visible residue findings)")
            for rel, line, kind, literal in findings:
                print(f"{rel}:{line}: [{kind}] {literal}")
            return 1

        print(
            "English build-surface audit: OK "
            f"({len(renderers)} renderers; {len(overlays)} transactional overlays; "
            f"{len(iter_runtime_files())} runtime files scanned)."
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
