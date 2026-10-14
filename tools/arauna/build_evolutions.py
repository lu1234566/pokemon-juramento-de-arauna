#!/usr/bin/env python3
"""Generate gEvolutionTable from the approved Arauna evolution design.

Inputs, both versioned so a run is reproducible:

  docs/arauna/ARAUNA_EVOLUTIONS.csv         the 81 approved relations
  docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv which engine species each Arauna
                                            dex number occupies

An Arauna dex number is not an engine species id: #001 Caramelo lives in
SPECIES_TORCHIC and #007 Pimpau in SPECIES_TREECKO, so the relations only make
sense once translated through the mapping.

The design is validated before anything is emitted: no self-evolution, no two
species evolving into the same one, no cycles, levels inside 2..80, and levels
strictly increasing along a chain.

  --check   validate and report what would change; write nothing
  --write   replace src/data/pokemon/evolution.h

REFUSES TO WRITE while the engine still holds the vanilla dex. The relations
are expressed in engine species constants, so applying them before the Arauna
species table is installed would state things like "Raticate evolves into
Spearow": correct for Arauna, nonsense for the dex actually compiled. Pass
--force only when the Arauna dex is in place.
"""
from __future__ import annotations
import argparse, csv, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVOS = ROOT / "docs/arauna/ARAUNA_EVOLUTIONS.csv"
MAP = ROOT / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv"
TABLE = ROOT / "src/data/pokemon/evolution.h"
NAMES = ROOT / "src/data/text/species_names.h"


def load():
    evos = list(csv.DictReader(EVOS.open(encoding="utf-8")))
    mapping = {int(r["arauna_dex"]): r for r in csv.DictReader(MAP.open(encoding="utf-8"))}
    return evos, mapping


def validate(evos, mapping):
    problems = []
    rel = {}
    for r in evos:
        a, b = int(r["arauna_dex"]), int(r["target_dex"])
        method = r["method"]
        parameter = r.get("parameter") or r["level"]
        lv = int(parameter) if method == "EVO_LEVEL" else 0
        if a == b:
            problems.append(f"#{a} evolves into itself")
        if b not in mapping:
            problems.append(f"#{a} targets #{b}, which is not in the dex mapping")
        if method == "EVO_LEVEL" and not 2 <= lv <= 80:
            problems.append(f"#{a} has an implausible level {lv}")
        if method not in {"EVO_LEVEL", "EVO_FRIENDSHIP", "EVO_FRIENDSHIP_DAY", "EVO_FRIENDSHIP_NIGHT", "EVO_ITEM"}:
            problems.append(f"#{a} uses unsupported method {method}")
        if method.startswith("EVO_FRIENDSHIP") and parameter != "0":
            problems.append(f"#{a}: friendship parameter must be zero")
        if method == "EVO_ITEM":
            items = (ROOT / "include/constants/items.h").read_text()
            if not re.search(r"^#define\s+" + re.escape(parameter) + r"\s+", items, re.M):
                problems.append(f"#{a}: unknown evolution item {parameter}")
        rel[a] = (b, method, parameter)
    for target, n in Counter(value[0] for value in rel.values()).items():
        if n > 1:
            problems.append(f"#{target} is the target of {n} different species")
    for a, (b, method, parameter) in rel.items():
        if method == "EVO_LEVEL" and b in rel and rel[b][1] == "EVO_LEVEL" and int(rel[b][2]) <= int(parameter):
            problems.append(f"chain #{a} -> #{b} does not increase")
    for a in rel:
        seen, cur = [], a
        while cur in rel and cur not in seen:
            seen.append(cur)
            cur = rel[cur][0]
        if cur in seen:
            problems.append(f"cycle through {seen}")
            break
    return rel, problems


def arauna_dex_installed() -> bool:
    """True when the engine species table is Arauna's rather than vanilla's."""
    if not NAMES.exists():
        return True  # newer layout; the caller decides
    # Look at the displayed name, not the slot's constant: the Arauna table
    # still writes [SPECIES_BULBASAUR], it just calls it Formilim.
    return '_("BULBASAUR")' not in NAMES.read_text(encoding="utf-8", errors="replace")


def render(rel, mapping) -> str:
    width = max(len(mapping[a]["species_constant"]) for a in rel)
    lines = ["const struct Evolution gEvolutionTable[NUM_SPECIES][EVOS_PER_MON] =", "{"]
    for a in sorted(rel):
        b, method, parameter = rel[a]
        src, dst = mapping[a]["species_constant"], mapping[b]["species_constant"]
        name, tname = mapping[a]["full_name"], mapping[b]["full_name"]
        lines.append(f"    [{src}]{' ' * (width - len(src))} = "
                     f"{{{{{method}, {parameter}, {dst}}}}}, // #{a:03d} {name} -> #{b:03d} {tname}")
    lines += ["};", ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="write even though the vanilla dex is still installed")
    args = ap.parse_args()

    evos, mapping = load()
    rel, problems = validate(evos, mapping)
    if problems:
        for p in problems:
            print(f"evolution design problem: {p}", file=sys.stderr)
        return 1
    print(f"design OK: {len(rel)} relations, "
          f"{sum(1 for a in rel if rel[a][0] in rel)} of them mid-chain")

    if not args.write:
        current = TABLE.read_text(encoding="utf-8") if TABLE.exists() else ""
        compiled = {m[0]: (m[3], m[1], m[2].strip()) for m in re.findall(
            r"\[(SPECIES_\w+)\]\s*=\s*\{\{(EVO_\w+),\s*([^,]+),\s*(SPECIES_\w+)\}\}", current)}
        expected = {mapping[a]["species_constant"]: (mapping[b]["species_constant"], method, parameter)
                    for a, (b, method, parameter) in rel.items()}
        if compiled != expected:
            for species in sorted(set(compiled) | set(expected)):
                if compiled.get(species) != expected.get(species):
                    print(f"evolution drift: {species}: compiled={compiled.get(species)} expected={expected.get(species)}")
            return 1
        print(f"evolution source equivalence PASS: {len(expected)} methods, parameters and targets")
        if not arauna_dex_installed():
            print("\nNOT APPLYING: the engine still holds the vanilla species table.\n"
                  "These relations are written in engine species constants and only read\n"
                  "correctly once the Arauna dex occupies them.")
        return 0

    if not arauna_dex_installed() and not args.force:
        print("refusing to write: the vanilla dex is still installed (use --force to override)",
              file=sys.stderr)
        return 1
    TABLE.write_text(render(rel, mapping), encoding="utf-8")
    print(f"wrote {TABLE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
