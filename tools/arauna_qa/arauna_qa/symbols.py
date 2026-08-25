from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Symbol:
    name: str
    address: int
    size: int | None = None
    kind: str | None = None


class SymbolTable:
    def __init__(self, symbols: dict[str, Symbol]):
        self._symbols = symbols

    @classmethod
    def from_file(cls, path: str | Path) -> "SymbolTable":
        symbols: dict[str, Symbol] = {}
        for raw_line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue

            try:
                address = int(parts[0], 16)
            except ValueError:
                continue

            # pokeemerald's `make syms` normally writes:
            #   ADDRESS TYPE SIZE NAME
            # Be lenient so GNU objdump variations still work.
            name = parts[-1]
            kind = parts[1] if len(parts) >= 3 else None
            size = None
            if len(parts) >= 4:
                try:
                    size = int(parts[-2], 16)
                except ValueError:
                    size = None

            # Keep the first occurrence. Local/static duplicate names can exist;
            # the symbols used by the harness are expected to be unique.
            symbols.setdefault(name, Symbol(name=name, address=address, size=size, kind=kind))
        return cls(symbols)

    def get(self, name: str) -> Symbol | None:
        return self._symbols.get(name)

    def require(self, name: str) -> Symbol:
        symbol = self.get(name)
        if symbol is None:
            raise KeyError(
                f"symbol {name!r} not found. Rebuild the ROM and run `make syms`, "
                "then point --sym at the matching .sym file."
            )
        return symbol

    def address(self, name: str) -> int:
        return self.require(name).address

    def __contains__(self, name: str) -> bool:
        return name in self._symbols
