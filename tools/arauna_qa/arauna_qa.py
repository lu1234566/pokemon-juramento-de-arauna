#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[1]
sys.path.insert(0, str(ROOT))

from arauna_qa import AraunaStateReader, Explorer, MgbaBridge, Navigator, RepoMapIndex, SymbolTable, key_mask


def print_state(reader: AraunaStateReader) -> None:
    print(json.dumps(reader.snapshot().to_dict(), indent=2, sort_keys=True))


def print_map(reader: AraunaStateReader, map_index: RepoMapIndex) -> None:
    state = reader.snapshot()
    if state.map_group is None or state.map_num is None:
        raise RuntimeError("runtime map group/number are unavailable")
    map_def = map_index.from_runtime(state.map_group, state.map_num)
    if map_def is None:
        raise RuntimeError(f"unknown runtime map ({state.map_group},{state.map_num})")
    print(json.dumps(map_index.summarize(map_def.id), indent=2, sort_keys=True))


def repl(bridge: MgbaBridge, reader: AraunaStateReader, map_index: RepoMapIndex) -> None:
    navigator = Navigator(bridge, reader, map_index=map_index)
    explorer = Explorer(navigator, map_index)
    print("Connected. Commands: state, map, step DIR, walk DIR..., walkto X Y, explore [targets], press KEY [frames],")
    print("keys KEY..., release, screenshot PATH, save PATH, load PATH, info, ping, reset, quit")
    while True:
        try:
            raw = input("arauna-qa> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not raw:
            continue
        try:
            args = shlex.split(raw)
            command = args[0].lower()
            if command in {"quit", "exit"}:
                return
            if command == "state":
                print_state(reader)
            elif command == "map":
                print_map(reader, map_index)
            elif command == "step":
                if len(args) != 2:
                    raise ValueError("usage: step DIRECTION")
                print(json.dumps(navigator.step(args[1]).to_dict(), indent=2, sort_keys=True))
            elif command == "walk":
                if len(args) < 2:
                    raise ValueError("usage: walk DIRECTION [DIRECTION ...]")
                results = navigator.walk_sequence(args[1:])
                print(json.dumps([result.to_dict() for result in results], indent=2, sort_keys=True))
            elif command == "walkto":
                if len(args) != 3:
                    raise ValueError("usage: walkto X Y")
                result = navigator.walk_to(int(args[1]), int(args[2]))
                print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
            elif command == "explore":
                if len(args) > 2:
                    raise ValueError("usage: explore [MAX_TARGETS]")
                max_targets = int(args[1]) if len(args) == 2 else 64
                result = explorer.explore_current_map(max_targets=max_targets)
                print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
            elif command == "press":
                if len(args) not in {2, 3}:
                    raise ValueError("usage: press KEY [frames]")
                frames = int(args[2]) if len(args) == 3 else 2
                bridge.press(args[1], frames=frames)
            elif command == "keys":
                if len(args) < 2:
                    raise ValueError("usage: keys KEY [KEY ...]")
                bridge.set_keys(args[1:])
            elif command == "release":
                bridge.release_keys()
            elif command == "screenshot":
                bridge.screenshot(args[1])
            elif command == "save":
                bridge.save_state(args[1])
            elif command == "load":
                bridge.load_state(args[1])
            elif command == "info":
                print(bridge.info())
            elif command == "ping":
                print("pong" if bridge.ping() else "unexpected response")
            elif command == "reset":
                bridge.reset()
            elif command == "mask":
                print(key_mask(args[1:]))
            else:
                print(f"unknown command: {command}")
        except Exception as exc:
            print(f"error: {exc}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="Arauna mGBA QA controller")
    parser.add_argument("--sym", required=True, help="matching pokeemerald .sym file")
    parser.add_argument("--repo", default=str(REPO_ROOT), help="Arauna repository root")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--once",
        choices=["state", "map", "info", "ping"],
        help="run one command after mGBA connects, then exit",
    )
    args = parser.parse_args()

    symbols = SymbolTable.from_file(args.sym)
    map_index = RepoMapIndex.from_repo(args.repo)
    bridge = MgbaBridge.listen(args.host, args.port)
    try:
        reader = AraunaStateReader(bridge, symbols)
        if args.once == "state":
            print_state(reader)
        elif args.once == "map":
            print_map(reader, map_index)
        elif args.once == "info":
            print(bridge.info())
        elif args.once == "ping":
            print("pong" if bridge.ping() else "unexpected response")
        else:
            repl(bridge, reader, map_index)
    finally:
        bridge.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
