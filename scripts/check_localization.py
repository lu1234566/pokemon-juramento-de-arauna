#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHARMAP = ROOT / "charmap.txt"
SOURCE_DIRECTORIES = {
    "en": ROOT / "data/text/arauna/en",
    "pt-BR": ROOT / "data/text/arauna/pt_br",
}
MAX_VISIBLE_LINE_LENGTH = 32
PLACEHOLDER_WIDTHS = {"PLAYER": 7}
REQUIRED_RUNTIME_LABELS = {
    "gText_ThisIsAPokemon",
    "gText_Boy",
    "gText_Girl",
}

# The first playable release is intentionally English-only. Portuguese source
# files remain valuable translation work, but new English runtime labels do not
# have to be mirrored until the Portuguese build is re-enabled.
REQUIRE_FULL_LABEL_PARITY = False

LABEL_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)::$")
STRING_RE = re.compile(r'^\s*\.string\s+"(.*)"\s*$')
TOKEN_RE = re.compile(r"\{([^{}]+)\}")
LINE_BREAK_RE = re.compile(r"\\[nlp]")
CHARMAP_ENTRY_RE = re.compile(r"^'((?:\\.|[^'])*)'\s*=")


def parse_sources(paths: list[Path]) -> tuple[list[str], dict[str, str]]:
    labels: list[str] = []
    text_by_label: dict[str, list[str]] = {}
    current_label: str | None = None

    for path in paths:
        current_label = None
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            label_match = LABEL_RE.match(line)
            if label_match:
                current_label = label_match.group(1)
                if current_label in text_by_label:
                    raise ValueError(f"{path}:{line_number}: duplicate label {current_label}")
                labels.append(current_label)
                text_by_label[current_label] = []
                continue

            string_match = STRING_RE.match(line)
            if string_match:
                if current_label is None:
                    raise ValueError(f"{path}:{line_number}: string without a label")
                text_by_label[current_label].append(string_match.group(1))

    if not labels:
        raise ValueError("no localized labels found")

    return labels, {label: "".join(parts) for label, parts in text_by_label.items()}


def expanded_length(line: str) -> int:
    line = line.replace("$", "")

    def replace_token(match: re.Match[str]) -> str:
        token = match.group(1)
        if " " in token:
            return ""
        return "X" * PLACEHOLDER_WIDTHS.get(token, len(token) + 2)

    return len(TOKEN_RE.sub(replace_token, line))


def load_supported_characters() -> set[str]:
    characters: set[str] = set()
    for line in CHARMAP.read_text(encoding="utf-8").splitlines():
        match = CHARMAP_ENTRY_RE.match(line)
        if not match:
            continue
        token = match.group(1)
        if len(token) == 1:
            characters.add(token)
        elif token == r"\'":
            characters.add("'")
    return characters


def validate_characters(language: str, texts: dict[str, str], supported: set[str]) -> list[str]:
    errors: list[str] = []
    for label, text in texts.items():
        visible_text = TOKEN_RE.sub("", LINE_BREAK_RE.sub("", text))
        unsupported = sorted({character for character in visible_text if character not in supported})
        if unsupported:
            rendered = ", ".join(f"U+{ord(character):04X} {character!r}" for character in unsupported)
            errors.append(f"{language}:{label}: unsupported characters: {rendered}")
    return errors


def validate_line_lengths(language: str, texts: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for label, text in texts.items():
        for line_number, line in enumerate(LINE_BREAK_RE.split(text), 1):
            length = expanded_length(line)
            if length > MAX_VISIBLE_LINE_LENGTH:
                errors.append(
                    f"{language}:{label}: visual line {line_number} has {length} characters "
                    f"(maximum {MAX_VISIBLE_LINE_LENGTH}): {line!r}"
                )
    return errors


def main() -> int:
    sources = {
        language: sorted(directory.glob("*.inc"))
        for language, directory in SOURCE_DIRECTORIES.items()
    }
    parsed = {language: parse_sources(paths) for language, paths in sources.items()}
    supported_characters = load_supported_characters()
    reference_language = "en"
    reference_labels, reference_texts = parsed[reference_language]
    errors: list[str] = []

    missing_runtime_labels = REQUIRED_RUNTIME_LABELS - set(reference_labels)
    if missing_runtime_labels:
        errors.append(
            "en: missing required runtime labels: "
            + ", ".join(sorted(missing_runtime_labels))
        )

    for language, (labels, texts) in parsed.items():
        if REQUIRE_FULL_LABEL_PARITY and labels != reference_labels:
            errors.append(f"{language}: label order differs from {reference_language}")

        for label, text in texts.items():
            if not text.endswith("$"):
                errors.append(f"{language}:{label}: localized string is not terminated with $")

        # Shared labels must keep the same runtime placeholder contract even
        # while one language contains more labels than the other.
        for label in set(reference_texts) & set(texts):
            expected = Counter(TOKEN_RE.findall(reference_texts[label]))
            actual = Counter(TOKEN_RE.findall(texts[label]))
            if actual != expected:
                errors.append(
                    f"{language}:{label}: tokens {dict(actual)} differ from "
                    f"{reference_language} {dict(expected)}"
                )

        errors.extend(validate_line_lengths(language, texts))
        errors.extend(validate_characters(language, texts, supported_characters))

    if errors:
        print("Localization validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    parity_note = "full parity" if REQUIRE_FULL_LABEL_PARITY else "shared-label placeholder parity"
    print(
        f"Localization check passed for {len(parsed)} languages, "
        f"{len(reference_labels)} English labels, and {parity_note}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
