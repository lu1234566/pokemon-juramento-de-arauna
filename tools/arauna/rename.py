#!/usr/bin/env python3
"""Rename a word everywhere the player can read it, and nowhere else.

Two passes need this and they need exactly the same care, so it lives here
rather than being copied: the places the map renamed, and the people the story
renamed. The hard parts are not the substitution.

**Only what is displayed.** A `.string` in a script, an `_("")` in a table, and
under src/data/text the adjacent literals a description is written as. Symbol
names survive because they are mixed case (SlateportCity_Text_...) or joined by
underscores (MAPSEC_SLATEPORT_CITY, TRAINER_ROXANNE), and the word boundary
refuses both.

**The English renderers move with it.** A renderer finds the block it rewrites
by searching the base text for a phrase, so a renamed word has to be renamed in
its anchors or the renderer looks for something that no longer exists, and in
what it writes for the same reason the dialogue does -- but *not* in the lists
of tokens it asserts have NOT survived, where "MT. CHIMNEY" means "the Hoenn
name must be gone". The same file uses "MT. CHIMNEY" in both roles, so the text
cannot decide it. Python's own parse tree can, and does.

**Longest first.** "SLATEPORT CITY" is one place, not a place and a word.
"""
from __future__ import annotations

import ast
import collections
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

STRING = re.compile(r'(\.string ")((?:[^"\\]|\\.)*)(")')
QUOTED = re.compile(r'(_\(")((?:[^"\\]|\\.)*)("\))')
# A description is written as adjacent literals the compiler joins, so it never
# sits inside one _(""). Under src/data/text every quoted literal is display
# text, so there they can all be read as one.
PROSE_FILES = ("src/data/text/",)
C_STRING = re.compile(r'(")((?:[^"\\]|\\.)*)(")')
PYTHON_STRING = re.compile(r'(["\'])((?:(?!\1)[^\\]|\\.)*)(\1)')

GUARD_NAME = re.compile(r"forbidden|stale|legacy|residue|banned", re.I)


def asserts_absence(loop) -> bool:
    """True for `for token in (...): if token in body: raise`.

    A renderer loops over string lists for two opposite reasons, and the
    difference is one word. A stale-token loop raises when the token IS still
    there, so its strings are Hoenn names that must stay Hoenn. A marker loop
    raises when the phrase is NOT there, so its strings are anchors and have to
    follow the rename. `in` versus `not in` tells them apart.
    """
    for node in ast.walk(loop):
        if isinstance(node, ast.Compare) and node.ops:
            return isinstance(node.ops[0], ast.In)
    return False


def guarded(body: str) -> set[tuple[int, int, int, int]]:
    """Spans of string literals that assert something is absent.

    Three shapes, and the module's own parse tree decides each one: a name
    bound to a guard list, the subject of a `for token in (...)` that raises on
    presence, and an argument passed to a parameter the function itself calls
    `forbidden`. The last needs the callee's signature, which is why the
    functions defined in the file are read first.
    """
    tree = ast.parse(body)
    signatures = {node.name: [a.arg for a in node.args.args]
                  for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}

    protected, holders = set(), []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            parameters = signatures.get(getattr(node.func, "id", ""), [])
            for index, argument in enumerate(node.args):
                if index < len(parameters) and GUARD_NAME.search(parameters[index]):
                    holders.append(argument)
            holders += [kw.value for kw in node.keywords
                        if kw.arg and GUARD_NAME.search(kw.arg)]
        elif isinstance(node, ast.For) and asserts_absence(node):
            holders.append(node.iter)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            names = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(GUARD_NAME.search(getattr(t, "id", "")) for t in names):
                holders.append(node.value)
    for holder in holders:
        for node in ast.walk(holder):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                protected.add((node.lineno, node.col_offset,
                               node.end_lineno, node.end_col_offset))
    return protected


class Renamer:
    """Applies one old-word -> new-word table across everything displayed."""

    def __init__(self, mapping: dict[str, str], keep=None) -> None:
        """`keep(text)` may return False to leave one whole string alone."""
        self.mapping = mapping
        self.keep = keep
        names = sorted(mapping, key=len, reverse=True)   # longest first
        self.finder = re.compile(r"(?<![A-Za-z_])("
                                 + "|".join(re.escape(n) for n in names)
                                 + r")(?![A-Za-z_])")
        self.hits = collections.Counter()
        self.per_file = collections.Counter()

    def _one(self, name: str):
        def substitute(found):
            head, text, tail = found.groups()
            if self.keep is not None and not self.keep(text):
                return head + text + tail
            for word in self.finder.findall(text):
                self.hits[word] += 1
                self.per_file[name] += 1
            return head + self.finder.sub(lambda m: self.mapping[m.group(1)], text) + tail
        return substitute

    def _requote(self, literal: str, one) -> str:
        """Rename inside one Python literal without breaking its quoting.

        CAVERNAS M'BOI carries an apostrophe, and dropping it into a literal
        delimited by apostrophes ends the string early. The delimiter is
        escaped inside the new text; nothing else changes.
        """
        new = PYTHON_STRING.sub(one, literal)
        quote = new[:1]
        if quote not in "\"'":
            return new
        inner = new[1:-1]
        if quote in inner.replace("\\" + quote, ""):
            inner = re.sub(r"(?<!\\)" + re.escape(quote), "\\\\" + quote, inner)
        return quote + inner + quote

    def _python(self, body: str, one) -> str:
        protect = guarded(body)
        edits = [(node.lineno, node.col_offset, node.end_lineno, node.end_col_offset)
                 for node in ast.walk(ast.parse(body))
                 if isinstance(node, ast.Constant) and isinstance(node.value, str)]
        edits = [span for span in edits if span not in protect and span[0] == span[2]]

        # ast reports a column as a UTF-8 byte offset, and these files are full
        # of "POKéMON", so slicing the line as characters lands on wrong text.
        lines = [line.encode("utf-8") for line in body.splitlines(keepends=True)]
        for lineno, start, _, end in sorted(edits, reverse=True):
            line = lines[lineno - 1]
            literal = line[start:end].decode("utf-8")
            lines[lineno - 1] = (line[:start]
                                 + self._requote(literal, one).encode("utf-8")
                                 + line[end:])
        return b"".join(lines).decode("utf-8")

    def apply(self) -> list[tuple[Path, str]]:
        tracked = subprocess.run(["git", "ls-files", "data", "src", "scripts"],
                                 cwd=ROOT, capture_output=True, text=True,
                                 check=True).stdout.split()
        changed = []
        for name in (f for f in tracked if f.endswith((".inc", ".h", ".c"))):
            path = ROOT / name
            body = path.read_text(encoding="utf-8", errors="replace")
            one = self._one(name)
            updated = QUOTED.sub(one, STRING.sub(one, body))
            if name.startswith(PROSE_FILES):
                updated = C_STRING.sub(one, updated)
            if updated != body:
                changed.append((path, updated))

        # The English text a renderer writes is not in the renderer: it is in a
        # JSON bank under data/text. A key there is a symbol name in mixed case,
        # so the word boundary refuses it and only the payloads are touched.
        for name in (f for f in tracked
                     if f.startswith("data/text/") and f.endswith(".json")):
            path = ROOT / name
            body = path.read_text(encoding="utf-8")
            updated = C_STRING.sub(self._one(name), body)
            if updated != body:
                changed.append((path, updated))

        for name in sorted(f for f in tracked
                           if f.startswith("scripts/") and f.endswith(".py")):
            path = ROOT / name
            body = path.read_text(encoding="utf-8")
            updated = self._python(body, self._one(name))
            if updated != body:
                changed.append((path, updated))
        return changed

    def report(self) -> None:
        print(f"{sum(self.hits.values())} mentions in player-visible strings")
        for word, count in self.hits.most_common():
            print(f"  {count:4}  {word:22} -> {self.mapping[word]}")
        print("  worst files: " + ", ".join(f"{name} ({count})" for name, count
                                            in self.per_file.most_common(5)))


def count(words, where=("data", "src")) -> collections.Counter:
    """How often each word is still displayed anywhere."""
    if not words:
        return collections.Counter()
    finder = re.compile(r"(?<![A-Za-z_])("
                        + "|".join(re.escape(w) for w in words) + r")(?![A-Za-z_])")
    found = collections.Counter()
    tracked = subprocess.run(["git", "ls-files", *where], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.split()
    for name in (f for f in tracked if f.endswith((".inc", ".h", ".c"))):
        body = (ROOT / name).read_text(encoding="utf-8", errors="replace")
        for match in list(STRING.finditer(body)) + list(QUOTED.finditer(body)):
            for word in finder.findall(match.group(2)):
                found[word] += 1
    return found
