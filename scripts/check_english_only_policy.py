#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(f"English-only policy violation: {message}")


selector = (ROOT / "data/text/birch_speech.inc").read_text(encoding="utf-8")
if 'data/text/arauna/en/birch_speech.inc' not in selector:
    fail("intro selector does not include the English bank")
if "pt_br" in selector or "ARAUNA_LANGUAGE" in selector:
    fail("intro selector still exposes a Portuguese/runtime language path")

build = (ROOT / "scripts/build_arauna.sh").read_text(encoding="utf-8")
active_build_lines = [
    line.strip()
    for line in build.splitlines()
    if line.strip() and not line.lstrip().startswith("#")
]
if not any("Portuguese builds are disabled" in line for line in active_build_lines):
    fail("build wrapper does not explicitly reject Portuguese builds")
if any("python3 scripts/render_" in line for line in active_build_lines):
    fail("official build still invokes legacy localized render overlays")
if "BUILD_DIR=\"build/arauna-en\"" not in build:
    fail("official build output is not the English-only target")

workflow = (ROOT / ".github/workflows/build.yml").read_text(encoding="utf-8")
if "ptbr" in workflow.lower() or "pt-br" in workflow.lower():
    fail("CI still references a Portuguese build")
if "matrix:" in workflow:
    fail("CI still uses the former language build matrix")

print("English-only policy: OK")
