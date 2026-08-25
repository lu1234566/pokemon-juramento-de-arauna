from __future__ import annotations

import socket
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


class ProtocolError(RuntimeError):
    pass


@dataclass(frozen=True)
class BridgeInfo:
    title: str
    game_code: str
    frame: int


KEY_BITS = {
    "A": 0,
    "B": 1,
    "SELECT": 2,
    "START": 3,
    "RIGHT": 4,
    "LEFT": 5,
    "UP": 6,
    "DOWN": 7,
    "R": 8,
    "L": 9,
}


def key_mask(keys: str | Iterable[str]) -> int:
    if isinstance(keys, str):
        keys = [keys]
    mask = 0
    for key in keys:
        normalized = key.upper()
        try:
            bit = KEY_BITS[normalized]
        except KeyError as exc:
            raise ValueError(f"unknown GBA key: {key}") from exc
        mask |= 1 << bit
    return mask


class MgbaBridge:
    def __init__(self, conn: socket.socket):
        self._conn = conn
        self._reader = conn.makefile("r", encoding="utf-8", newline="\n")
        self._lock = threading.Lock()
        self._next_id = 1

    @classmethod
    def listen(
        cls,
        host: str = "127.0.0.1",
        port: int = 8765,
        timeout: float | None = None,
    ) -> "MgbaBridge":
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((host, port))
            server.listen(1)
            if timeout is not None:
                server.settimeout(timeout)
            conn, _ = server.accept()
        bridge = cls(conn)
        bridge._consume_hello()
        return bridge

    def close(self) -> None:
        try:
            self._reader.close()
        finally:
            self._conn.close()

    def _consume_hello(self) -> None:
        line = self._reader.readline()
        if not line:
            raise ProtocolError("mGBA disconnected before bridge hello")
        parts = line.rstrip("\r\n").split("\t", 2)
        if len(parts) < 3 or parts[1] != "HELLO" or parts[2] != "ARAUNA_QA_BRIDGE_V1":
            raise ProtocolError(f"unexpected bridge hello: {line!r}")

    def _request(self, command: str, *args: object) -> str:
        with self._lock:
            request_id = str(self._next_id)
            self._next_id += 1
            fields = [request_id, command]
            for arg in args:
                text = str(arg)
                if "\t" in text or "\n" in text or "\r" in text:
                    raise ValueError("protocol arguments may not contain tabs/newlines")
                fields.append(text)
            self._conn.sendall(("\t".join(fields) + "\n").encode("utf-8"))

            while True:
                line = self._reader.readline()
                if not line:
                    raise ProtocolError("mGBA disconnected")
                parts = line.rstrip("\r\n").split("\t", 2)
                if len(parts) < 2:
                    continue
                if parts[0] != request_id:
                    # V1 only emits HELLO out of band; ignore any future async lines.
                    continue
                status = parts[1]
                payload = parts[2] if len(parts) == 3 else ""
                if status == "OK":
                    return payload
                raise ProtocolError(payload or f"{command} failed")

    def ping(self) -> bool:
        return self._request("PING") == "PONG"

    def info(self) -> BridgeInfo:
        payload = self._request("INFO")
        title, game_code, frame_text = payload.split("|", 2)
        return BridgeInfo(title=title, game_code=game_code, frame=int(frame_text))

    def read8(self, address: int) -> int:
        return int(self._request("READ8", hex(address)))

    def read16(self, address: int) -> int:
        return int(self._request("READ16", hex(address)))

    def read32(self, address: int) -> int:
        return int(self._request("READ32", hex(address)))

    def read_range(self, address: int, length: int) -> bytes:
        return bytes.fromhex(self._request("READRANGE", hex(address), length))

    def set_keys(self, keys: str | Iterable[str] | int) -> None:
        mask = keys if isinstance(keys, int) else key_mask(keys)
        self._request("SETKEYS", mask)

    def release_keys(self) -> None:
        self.set_keys(0)

    def press(self, keys: str | Iterable[str] | int, frames: int = 2) -> None:
        mask = keys if isinstance(keys, int) else key_mask(keys)
        self._request("PRESS", mask, frames)

    def screenshot(self, path: str | Path) -> None:
        self._request("SCREENSHOT", str(path))

    def save_state(self, path: str | Path) -> None:
        self._request("SAVESTATE", str(path))

    def load_state(self, path: str | Path) -> None:
        self._request("LOADSTATE", str(path))

    def reset(self) -> None:
        self._request("RESET")
