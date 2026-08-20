#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(f"English-only policy violation: {message}")


selector = (ROOT / "data/text/birch_speech.inc").read_text(encoding="utf-8")
if 'data/text/arauna/en/birch_speech.inc' not in selector:
    fail("intro selector does not include the English bank")
if "pt_br" in selector or "ARAUNA_LANGUAGE" in selector:
    fail("intro selector still exposes a Portuguese/runtime language path")

build_path = ROOT / "scripts/build_arauna.sh"
build = build_path.read_text(encoding="utf-8")
active_build_lines = [
    line.strip()
    for line in build.splitlines()
    if line.strip() and not line.lstrip().startswith("#")
]
if not any("Portuguese builds are disabled" in line for line in active_build_lines):
    fail("build wrapper does not explicitly reject Portuguese builds")
if "BUILD_DIR=\"build/arauna-en\"" not in build:
    fail("official build output is not the English-only target")

# English-only rendering is intentionally transactional: reviewed English
# overlays are applied in-place only for the duration of the build and restored
# afterwards. The old policy incorrectly rejected every renderer invocation,
# including the English renderers that now define the official build surface.
for raw in active_build_lines:
    if "python3" not in raw:
        continue
    match = re.search(r"python3\s+([^\s]+)", raw)
    if not match:
        continue
    rel = match.group(1)
    lowered = rel.lower()
    if any(token in lowered for token in ("pt_br", "pt-br", "portuguese", "portugues")):
        fail(f"official build invokes a Portuguese renderer: {rel}")
    if rel in {
        "tools/apply_arauna_story.py",
        "tools/apply_arauna_story_safe.py",
    }:
        fail(f"official build invokes a legacy broad story mutator: {rel}")
    script = ROOT / rel
    if rel.startswith("scripts/render_") and not script.is_file():
        fail(f"official build references a missing renderer: {rel}")

if "data/text/arauna/pt_br" in build:
    fail("official build references the dormant Portuguese text bank")

workflow = (ROOT / ".github/workflows/build.yml").read_text(encoding="utf-8")
if "ptbr" in workflow.lower() or "pt-br" in workflow.lower():
    fail("CI still references a Portuguese build")
if "matrix:" in workflow:
    fail("CI still uses the former language build matrix")

print("English-only policy: OK")
