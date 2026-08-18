#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN_ROOTS = (ROOT / "data" / "maps", ROOT / "data" / "text")

LABEL_RE = re.compile(r'^\s*(?P<label>[A-Za-z0-9_.$]+)::?\s*$')
STRING_RE = re.compile(r'^\s*\.string\s+"(?P<text>.*)"\s*$')
WORD_RE = re.compile(r"[A-Za-z']+")

# Deliberately high-signal English function/content words. A fragment needs at
# least two distinct hits before it is reported, keeping proper names and game
# vocabulary such as POKéMON / TRAINER from becoming noise by themselves.
ENGLISH_WORDS = {
    "the", "this", "that", "these", "those", "there", "here", "where",
    "what", "when", "why", "how", "who", "your", "youre", "you're",
    "you", "our", "ours", "their", "they", "them", "his", "her", "hers",
    "with", "without", "from", "into", "about", "before", "after", "again",
    "have", "has", "had", "having", "will", "would", "could", "should",
    "can", "cant", "can't", "dont", "don't", "did", "didnt", "didn't",
    "does", "doesnt", "doesn't", "was", "were", "is", "are", "isnt",
    "isn't", "arent", "aren't", "not", "but", "and", "because", "very",
    "just", "really", "still", "now", "then", "please", "thanks", "thank",
    "hello", "hi", "good", "great", "come", "go", "going", "went", "get",
    "got", "make", "made", "know", "think", "want", "need", "look", "see",
    "take", "give", "like", "little", "time", "people", "place", "thing",
}


def iter_script_files():
    seen: set[Path] = set()
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.inc")):
            if path not in seen:
                seen.add(path)
                yield path


def normalized_words(text: str) -> set[str]:
    clean = re.sub(r"\\[npl]", " ", text)
    clean = re.sub(r"\{[^}]+\}", " ", clean)
    return {word.lower() for word in WORD_RE.findall(clean)}


def audit() -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    for path in iter_script_files():
        current_label = ""
        block_fragments: dict[str, list[tuple[int, str]]] = defaultdict(list)
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            label = LABEL_RE.match(line)
            if label:
                current_label = label.group("label")
                continue
            string = STRING_RE.match(line)
            if string and current_label and "unused" not in current_label.lower():
                block_fragments[current_label].append((lineno, string.group("text")))

        for label, fragments in block_fragments.items():
            joined = " ".join(fragment for _, fragment in fragments)
            words = normalized_words(joined)
            markers = sorted(words & ENGLISH_WORDS)
            if len(markers) < 2:
                continue
            hits.append(
                {
                    "path": str(path.relative_to(ROOT)),
                    "label": label,
                    "line": fragments[0][0],
                    "english_markers": markers,
                    "marker_count": len(markers),
                    "text": joined,
                }
            )
    hits.sort(key=lambda hit: (-int(hit["marker_count"]), str(hit["path"]), int(hit["line"])))
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report likely English player-facing script blocks remaining in the Arauna surface."
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--top", type=int, default=0, help="Limit printed findings; 0 means all.")
    args = parser.parse_args()

    hits = audit()
    shown = hits[: args.top] if args.top > 0 else hits
    if args.json:
        print(json.dumps(shown, ensure_ascii=False, indent=2))
    else:
        print(f"Visible English surface audit: {len(hits)} likely block(s); showing {len(shown)}.")
        for hit in shown:
            markers = ", ".join(hit["english_markers"])
            print(f"{hit['path']}:{hit['line']} {hit['label']} [{markers}]")
            print(f"  {hit['text']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
