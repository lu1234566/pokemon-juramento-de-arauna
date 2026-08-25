#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from arauna_qa import AraunaStateReader, MgbaBridge, SymbolTable, key_mask


def print_state(reader: AraunaStateReader) -> None:
    print(json.dumps(reader.snapshot().to_dict(), indent=2, sort_keys=True))


def repl(bridge: MgbaBridge, reader: AraunaStateReader) -> None:
    print("Connected. Commands: state, press KEY [frames], keys KEY..., release,")
    print("screenshot PATH, save PATH, load PATH, info, ping, reset, quit")
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
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--once",
        choices=["state", "info", "ping"],
        help="run one command after mGBA connects, then exit",
    )
    args = parser.parse_args()

    symbols = SymbolTable.from_file(args.sym)
    bridge = MgbaBridge.listen(args.host, args.port)
    try:
        reader = AraunaStateReader(bridge, symbols)
        if args.once == "state":
            print_state(reader)
        elif args.once == "info":
            print(bridge.info())
        elif args.once == "ping":
            print("pong" if bridge.ping() else "unexpected response")
        else:
            repl(bridge, reader)
    finally:
        bridge.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
