#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_PATH = ROOT / "scripts" / "build_arauna.sh"
EXTRA_OVERLAY_MANIFEST = ROOT / "scripts" / "english_overlay_files_extra.txt"
OVERLAY_LINE_RE = re.compile(r'^\s*"(?P<path>[^"]+)"\s*$')
ASM_STRING_RE = re.compile(r'(?m)^\s*\.string\s+"(?P<body>(?:[^"\\]|\\.)*)"')
C_STRING_RE = re.compile(r'"(?P<body>(?:[^"\\]|\\(?:.|\n))*)"')

# These are intentionally high-confidence visible identities. Internal symbols
# such as TRAINER_WALLACE or FLAG_MET_SCOTT are never inspected by this tool.
STALE_SPEAKERS = (
    "WALLACE:", "SCOTT:", "STEVEN:", "WALLY:", "NORMAN:",
    "ROXANNE:", "BRAWLY:", "WATTSON:", "FLANNERY:", "WINONA:",
    "JUAN:", "SIDNEY:", "PHOEBE:", "GLACIA:", "DRAKE:",
    "BIRCH:", "PROF. BIRCH", "BRENDAN:", "MAY:",
    "ARCHIE:", "MAXIE:", "SHELLY:", "MATT:", "TABITHA:", "COURTNEY:",
    "MR. STONE", "MR. BRINEY", "CAPT. BRINEY", "CAPT. STERN",
)
STALE_VISIBLE_PLACES = (
    "LITTLEROOT TOWN", "OLDALE TOWN", "PETALBURG CITY", "RUSTBORO CITY",
    "DEWFORD TOWN", "MAUVILLE CITY", "LAVARIDGE TOWN", "FORTREE CITY",
    "LILYCOVE CITY", "MOSSDEEP CITY", "SOOTOPOLIS CITY", "SLATEPORT CITY",
    "CAVE OF ORIGIN", "MT. PYRE", "SKY PILLAR", "BATTLE FRONTIER",
    "FRONTIER PASS", "FRONTIER BRAINS", "TEAM AQUA", "TEAM MAGMA",
    "DEVON CORP", "HOENN", "NEW MAUVILLE", "RUSTURF TUNNEL",
    "METEOR FALLS", "SEAFLOOR CAVERN", "GRANITE CAVE", "MAGMA HIDEOUT",
    "SLATEPORT BEACH", "SAFARI ZONE ENTRANCE", "MR. BRINEY'S COTTAGE",
)
PORTUGUESE_HIGH_CONFIDENCE = (
    "VOCÊ", "NÃO ", " NÃO", "ESTÁ ", "TAMBÉM", "OBRIGADO", "OBRIGADA",
    "GINÁSIO", "CAMPEÃO", "CAMPEÃ", "CIDADE DE ", "POKÉMON VISTOS",
    "REGISTRADOS:", "AVALIAÇÃO DA ",
)

C_VISIBLE_FILES = {
    "src/strings.c",
    "src/data/trainers.h",
    "src/data/text/trainer_class_names.h",
    "src/data/script_menu.h",
    "src/landmark.c",
}


def read_extra_overlays() -> set[str]:
    return {
        raw.strip()
        for raw in EXTRA_OVERLAY_MANIFEST.read_text(encoding="utf-8").splitlines()
        if raw.strip() and not raw.lstrip().startswith("#")
    }


def load_base_overlays() -> set[str]:
    build = BUILD_PATH.read_text(encoding="utf-8")
    start = build.find("overlay_files=(")
    end = build.find("\n)", start)
    if start < 0 or end < 0:
        raise SystemExit("Visible-residue audit: cannot parse build overlay_files array")
    paths: set[str] = set()
    for raw in build[start:end].splitlines()[1:]:
        match = OVERLAY_LINE_RE.fullmatch(raw)
        if match:
            paths.add(match.group("path"))
    return paths


def visible_literals(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    rel = path.relative_to(ROOT).as_posix()
    if rel in C_VISIBLE_FILES:
        return [m.group("body") for m in C_STRING_RE.finditer(text)]
    return [m.group("body") for m in ASM_STRING_RE.finditer(text)]


def candidate_files() -> list[Path]:
    paths = list((ROOT / "data" / "maps").glob("**/scripts.inc"))
    paths.extend((ROOT / "data" / "text").glob("**/*.inc"))
    paths.extend((ROOT / "data" / "scripts").glob("**/*.inc"))
    paths.extend(ROOT / rel for rel in sorted(C_VISIBLE_FILES))
    return sorted({path for path in paths if path.is_file()})


def classify(literal: str) -> tuple[list[str], list[str], list[str]]:
    upper = literal.upper()
    speakers = [marker for marker in STALE_SPEAKERS if marker in upper]
    places = [marker for marker in STALE_VISIBLE_PLACES if marker in upper]
    pt = [marker for marker in PORTUGUESE_HIGH_CONFIDENCE if marker in upper]
    return speakers, places, pt


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit visible runtime literals after the official English renderers have been applied."
    )
    parser.add_argument(
        "--fail-owned",
        action="store_true",
        help="fail if a transactional/owned file still contains a stale speaker or high-confidence PT-BR residue",
    )
    args = parser.parse_args()

    owned = load_base_overlays() | read_extra_overlays()
    critical_owned: list[str] = []
    global_identity: list[str] = []
    global_places: list[str] = []

    for path in candidate_files():
        rel = path.relative_to(ROOT).as_posix()
        for literal in visible_literals(path):
            speakers, places, pt = classify(literal)
            if not (speakers or places or pt):
                continue
            compact = literal.replace("\\n", " ").replace("\\p", " ").replace("\\l", " ")
            compact = compact.replace("\\\n", " ")
            compact = re.sub(r"\s+", " ", compact).strip()
            if len(compact) > 120:
                compact = compact[:117] + "..."
            if speakers or pt:
                markers = speakers + pt
                line = f"{rel}: {', '.join(markers)} :: {compact}"
                global_identity.append(line)
                if rel in owned:
                    critical_owned.append(line)
            elif places:
                global_places.append(f"{rel}: {', '.join(places)} :: {compact}")

    print(
        "Rendered visible-residue audit: "
        f"{len(critical_owned)} owned critical; "
        f"{len(global_identity)} global speaker/PT candidates; "
        f"{len(global_places)} global legacy-place candidates."
    )
    if global_identity:
        print("Global speaker/PT candidates (review inventory):")
        for line in global_identity[:80]:
            print(f"  - {line}")
        if len(global_identity) > 80:
            print(f"  ... {len(global_identity) - 80} more")
    if global_places:
        print("Global legacy-place candidates (advisory inventory):")
        for line in global_places[:80]:
            print(f"  - {line}")
        if len(global_places) > 80:
            print(f"  ... {len(global_places) - 80} more")

    if args.fail_owned and critical_owned:
        raise SystemExit(
            "Rendered visible-residue audit FAILED: owned English surfaces still contain critical stale identity/PT-BR text"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
