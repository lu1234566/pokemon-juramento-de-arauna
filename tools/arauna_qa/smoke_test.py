#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from arauna_qa import AraunaStateReader, MgbaBridge, SymbolTable


def main() -> int:
    parser = argparse.ArgumentParser(description="Non-destructive live mGBA smoke test")
    parser.add_argument("--sym", required=True, help="matching Arauna .sym file")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--screenshot", help="optional screenshot output path")
    args = parser.parse_args()

    symbols = SymbolTable.from_file(args.sym)
    required = ["gMain", "gPlayerAvatar", "gObjectEvents", "gMapHeader"]
    missing = [name for name in required if symbols.get(name) is None]
    if missing:
        print(json.dumps({"ok": False, "stage": "symbols", "missing": missing}, indent=2))
        return 2

    bridge = MgbaBridge.listen(args.host, args.port)
    try:
        checks: dict[str, object] = {}
        checks["ping"] = bridge.ping()
        info = bridge.info()
        checks["info"] = {
            "title": info.title,
            "game_code": info.game_code,
            "frame": info.frame,
        }
        checks["expected_game_code"] = info.game_code == "BPEE"
        state = AraunaStateReader(bridge, symbols).snapshot().to_dict()
        checks["state"] = state
        checks["state_readable"] = state["frame"] >= 0
        if args.screenshot:
            bridge.screenshot(args.screenshot)
            checks["screenshot"] = args.screenshot

        ok = bool(checks["ping"] and checks["expected_game_code"] and checks["state_readable"])
        print(json.dumps({"ok": ok, "checks": checks}, indent=2, sort_keys=True))
        return 0 if ok else 1
    finally:
        bridge.close()


if __name__ == "__main__":
    raise SystemExit(main())
