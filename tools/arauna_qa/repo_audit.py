#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from arauna_qa.repo_map import RepoMapIndex


def main() -> int:
    parser = argparse.ArgumentParser(description="Static Arauna map/event index and integrity audit")
    parser.add_argument("--repo", default=".", help="repository root")
    parser.add_argument("--map", dest="map_key", help="MAP_* id or map directory/name to summarize")
    parser.add_argument("--runtime", nargs=2, type=int, metavar=("GROUP", "NUM"), help="resolve runtime map pair")
    parser.add_argument("--validate", action="store_true", help="validate layouts, groups, events, connections and warps")
    args = parser.parse_args()

    index = RepoMapIndex.from_repo(args.repo)
    output: dict[str, object] = {
        "maps": len(index.maps_by_id),
        "layouts": len(index.layouts),
        "runtime_entries": len(index.runtime_map_names),
    }

    if args.map_key:
        output["map"] = index.summarize(args.map_key)

    if args.runtime:
        resolved = index.from_runtime(*args.runtime)
        output["runtime"] = resolved.to_dict() if resolved else None

    exit_code = 0
    if args.validate:
        issues = index.validate()
        output["validation"] = {
            "ok": not issues,
            "issue_count": len(issues),
            "by_code": dict(sorted(Counter(issue.code for issue in issues).items())),
            "issues": [issue.to_dict() for issue in issues],
        }
        if issues:
            exit_code = 1

    print(json.dumps(output, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
