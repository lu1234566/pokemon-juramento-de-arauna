#!/usr/bin/env python3
"""Make the dialogue call places what the map calls them.

The region map was renamed a while ago: MAPSEC_SLATEPORT_CITY reads PORTO DO
SAL, MAPSEC_LILYCOVE_CITY reads BAIA DAS LUZES, and the story text the project
wrote uses those names throughout. The dialogue Emerald shipped did not follow.
A sailor still says he came from SLATEPORT while the town sign, the PokeNav and
the map all say PORTO DO SAL.

The mapping is not invented here. It is the difference between
region_map_sections.json now and at the reset-to-vanilla commit: whatever the
project decided a place is called, in the project's own file. Two adjustments
sit on top, both recorded in the CSV rather than hidden in code:

  * where prose already uses a longer form than the fourteen characters the map
    label allows -- MEMORIAL DOS NOMES against the map's MEMORIAL NOMES -- the
    prose wins, because it is what the rest of the writing already says;
  * HOENN is the region, which has no map section, and the project already
    calls it ARAUNA in the text it wrote.

Anything with a map section is named there and read from there, so the map and
the dialogue cannot drift apart; EXTRA below is only for named things that have
no section of their own, like the company and the ferry. What is left in
UNDECIDED is left on purpose: the BATTLE FRONTIER is already BATTLE CIRCUIT in
the English renderers and renaming it belongs with them, and the event islands
are never spoken of.

Generic descriptors are not names and are not touched. UNDERWATER, SECRET BASE
and INSIDE OF TRUCK stay as they are, the way a real map keeps "Rio de Janeiro"
and "the harbour" in different languages.

Replacement happens only inside strings the player reads, and CITY and TOWN go
with the name they belong to: "SLATEPORT CITY" is one place, not a place and a
word. Lines get longer, so run rewrap_text.py afterwards -- check_text_width.py
fails loudly if anyone forgets, for the message box and for the much narrower
description box in the bag.

  --check   report what would change
  --write   rewrite the scripts and the CSV
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VANILLA = "c210195e"
REGION_MAP = "src/data/region_map/region_map_sections.json"
ROSTER = ROOT / "docs/arauna/ARAUNA_PLACE_NAMES.csv"

# The map label is capped at fourteen characters; prose is not. Where the
# project's own writing already says something longer, that is the real name.
PROSE = {"MEMORIAL NOMES": "MEMORIAL DOS NOMES"}

# Named things with no map section of their own. Everything that has one is
# named there instead, so the map and the dialogue cannot drift apart.
#
# DEVON is the awkward one. The company was already CONSORCIO HORIZONTE in
# three lines and DEVON everywhere else; the short form the writing uses for it
# is HORIZONTE. Its two items cannot carry that -- an item name is thirteen
# characters -- so they are named for what they are: the package the plot is
# about, and the lens that shows what is hiding.
EXTRA = {
    "HOENN": "ARAUNA",              # the region; the text already says ARAUNA
    "DEVON GOODS": "ENCOMENDA",
    "DEVON SCOPE": "VISOR VERDADE",
    "DEVON CORPORATION": "CONSORCIO HORIZONTE",
    "DEVON CORP": "CONSORCIO HORIZONTE",
    "DEVON": "HORIZONTE",
    "TRICK HOUSE": "CASA DOS TRUQUES",
    "S.S. TIDAL": "MARE ALTA",      # the vessel; the service is the LINE FERRY
    "SAFARI ZONE ENTRANCE": "ENTRADA DA RESERVA",
    # Two half-renames from the pass that named the towns: PETALBURG WOODS and
    # NEW MAUVILLE had no name of their own then, so only the town inside them
    # changed and they came out as a town's name with an English word stuck to
    # it. Now that they are named, these are the forms to repair.
    "PAMPA DA ESPERA WOODS": "MATA DA ESPERA",
    "NEW ENCRUZILHADA": "USINA VELHA",
}

# Hoenn names the project has not decided on. Left alone, and reported.
UNDECIDED = ["BATTLE FRONTIER", "TRAINER HILL", "NAVEL ROCK", "BIRTH ISLAND",
             "FARAWAY ISLAND", "ALTERING CAVE"]

STRING = re.compile(r'(\.string ")((?:[^"\\]|\\.)*)(")')
QUOTED = re.compile(r'(_\(")((?:[^"\\]|\\.)*)("\))')
# A description is written as adjacent literals the compiler joins, so it never
# sits inside one _(""). Under src/data/text every quoted literal is display
# text, so there they can all be read as one.
PROSE_FILES = ("src/data/text/",)
C_STRING = re.compile(r'(")((?:[^"\\]|\\.)*)(")')
# An English renderer finds the block it rewrites by searching the base text for
# a phrase, so a renamed place has to be renamed in its anchors too or the
# renderer looks for something that no longer exists. Its replacement text needs
# the new name for the same reason the dialogue does. Symbol names survive
# because they are mixed case (SlateportCity_Text_...) or joined by underscores
# (MAPSEC_SLATEPORT_CITY), and the word boundary refuses both.
PYTHON_STRING = re.compile(r'(["\'])((?:(?!\1)[^\\]|\\.)*)(\1)')

# One kind of string in those scripts must not be renamed: the lists of tokens
# a renderer asserts have NOT survived into its output. "MT. CHIMNEY" there
# means "the Hoenn name must be gone", so turning it into "SERRA DA CINZA"
# would forbid the very name the renderer writes. The same file uses
# "MT. CHIMNEY" as an anchor too, so this cannot be decided by the text -- only
# by where it sits. Python's own parser answers that.
GUARD_NAME = re.compile(r"forbidden|stale|legacy|residue|banned", re.I)


def asserts_absence(loop) -> bool:
    """True for `for token in (...): if token in body: raise`.

    A renderer loops over string lists for two opposite reasons, and the
    difference is one word. A stale-token loop raises when the token IS still
    there, so its strings are Hoenn names that must stay Hoenn. A marker loop
    raises when the phrase is NOT there, so its strings are anchors and have to
    follow the rename. `in` versus `not in` tells them apart.
    """
    import ast

    for node in ast.walk(loop):
        if isinstance(node, ast.Compare) and node.ops:
            return isinstance(node.ops[0], ast.In)
    return False


def guarded(body: str) -> list[tuple[int, int, int, int]]:
    """Spans of string literals that assert something is absent.

    Three shapes, and the module's own parse tree decides each one: a name
    bound to a guard list, the subject of `for token in (...)`, and an argument
    passed to a parameter the function itself calls `forbidden`. The last needs
    the callee's signature, which is why the functions defined in the file are
    read first.
    """
    import ast

    tree = ast.parse(body)
    signatures = {node.name: [a.arg for a in node.args.args]
                  for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}

    protected, holders = [], []
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
            names = [t for t in (node.targets if isinstance(node, ast.Assign)
                                 else [node.target])]
            if any(GUARD_NAME.search(getattr(t, "id", "")) for t in names):
                holders.append(node.value)
    for holder in holders:
        for node in ast.walk(holder):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                protected.append((node.lineno, node.col_offset,
                                  node.end_lineno, node.end_col_offset))
    return protected


def rename_python(body: str, one) -> str:
    """Rewrite every string literal the parser says is not a guard token."""
    import ast

    protect = set(guarded(body))
    edits = []
    for node in ast.walk(ast.parse(body)):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        span = (node.lineno, node.col_offset, node.end_lineno, node.end_col_offset)
        if span in protect or node.lineno != node.end_lineno:
            continue
        edits.append(span)

    # ast reports a column as a UTF-8 byte offset, and these files are full of
    # "POKéMON", so slicing the line as characters lands on the wrong text.
    lines = [line.encode("utf-8") for line in body.splitlines(keepends=True)]
    for lineno, start, _, end in sorted(edits, reverse=True):
        line = lines[lineno - 1]
        literal = line[start:end].decode("utf-8")
        lines[lineno - 1] = (line[:start] + requote(literal, one).encode("utf-8")
                             + line[end:])
    return b"".join(lines).decode("utf-8")


def requote(literal: str, one) -> str:
    """Rename inside one Python literal without breaking its quoting.

    CAVERNAS M'BOI carries an apostrophe, and dropping it into a literal that
    is itself delimited by apostrophes ends the string early. The quote that
    delimits the literal is escaped inside the new text; nothing else changes.
    """
    new = PYTHON_STRING.sub(one, literal)
    quote = new[:1]
    if quote not in "\"'":
        return new
    inner = new[1:-1]
    if quote in inner.replace("\\" + quote, ""):
        inner = re.sub(r'(?<!\\)' + re.escape(quote), "\\\\" + quote, inner)
    return quote + inner + quote


def at_vanilla(path: str) -> str:
    return subprocess.run(["git", "show", f"{VANILLA}:{path}"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout


def renames() -> dict[str, str]:
    """Hoenn name -> Arauna name, from the project's own region map."""
    def sections(text):
        return {s["id"]: s["name"] for s in json.loads(text)["map_sections"]}

    before = sections(at_vanilla(REGION_MAP))
    after = sections((ROOT / REGION_MAP).read_text(encoding="utf-8"))
    out = dict(EXTRA)
    for key, new in after.items():
        old = before.get(key)
        if old and new and old != new and old.isascii() and "{" not in old:
            out[old] = PROSE.get(new, new)
    return out


def pattern(mapping: dict[str, str]) -> re.Pattern:
    r"""Longest first, so SLATEPORT CITY wins over SLATEPORT."""
    names = sorted(mapping, key=len, reverse=True)
    return re.compile(r"(?<![A-Za-z_])(" + "|".join(re.escape(n) for n in names)
                      + r")(?![A-Za-z_])")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    mapping = renames()
    # "SLATEPORT CITY" is one place. Without this the CITY would survive the
    # rename and the line would read "PORTO DO SAL CITY".
    for hoenn, arauna in list(mapping.items()):
        for suffix in (" CITY", " TOWN"):
            if hoenn.endswith(suffix):
                mapping[hoenn[:-len(suffix)]] = arauna
    finder = pattern(mapping)

    tracked = subprocess.run(["git", "ls-files", "data", "src", "scripts"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.split()
    files = [f for f in tracked if f.endswith((".inc", ".h", ".c"))]

    hits, per_file = collections.Counter(), collections.Counter()

    def renamer(name: str):
        def one(found):
            head, text, tail = found.groups()
            new = finder.sub(lambda m: mapping[m.group(1)], text)
            for word in finder.findall(text):
                hits[word] += 1
                per_file[name] += 1
            return head + new + tail
        return one

    changed = []
    for name in files:
        path = ROOT / name
        body = path.read_text(encoding="utf-8", errors="replace")
        one = renamer(name)
        updated = QUOTED.sub(one, STRING.sub(one, body))
        if name.startswith(PROSE_FILES):
            updated = C_STRING.sub(one, updated)
        if updated != body:
            changed.append((path, updated))

    for name in sorted(f for f in tracked
                       if f.startswith("scripts/") and f.endswith(".py")):
        path = ROOT / name
        body = path.read_text(encoding="utf-8")
        updated = rename_python(body, renamer(name))
        if updated != body:
            changed.append((path, updated))

    print(f"{sum(hits.values())} mentions in player-visible strings, "
          f"{len(changed)} files")
    for word, count in hits.most_common():
        print(f"  {count:4}  {word:18} -> {mapping[word]}")
    print("  worst files: "
          + ", ".join(f"{name} ({count})" for name, count in per_file.most_common(5)))

    left = collections.Counter()
    undecided = re.compile(r"(?<![A-Za-z_])(" + "|".join(re.escape(n) for n in UNDECIDED)
                           + r")(?![A-Za-z_])")
    for name in files:
        for found in STRING.finditer((ROOT / name).read_text(encoding="utf-8",
                                                             errors="replace")):
            for word in undecided.findall(found.group(2)):
                left[word] += 1
    print("still Hoenn because the project has not named them: "
          + ", ".join(f"{word} ({count})" for word, count in left.most_common()))

    if not args.write:
        return 0

    for path, updated in changed:
        path.write_text(updated, encoding="utf-8")
    with ROSTER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["hoenn_name", "arauna_name", "mentions", "source"])
        for hoenn, arauna in sorted(mapping.items()):
            source = ("region map" if hoenn not in EXTRA else "already used in the text")
            writer.writerow([hoenn, arauna, hits.get(hoenn, 0), source])
        for word in UNDECIDED:
            writer.writerow([word, "", left.get(word, 0), "not named yet"])
    print(f"\nwrote {len(changed)} files and {ROSTER.relative_to(ROOT)}"
          "\nnow run rewrap_text.py --write: these lines are longer than they were")
    return 0


if __name__ == "__main__":
    sys.exit(main())
