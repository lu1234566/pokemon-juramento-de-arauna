#!/usr/bin/env python3
"""Turn paragraphs into the .string payloads a message box wants.

Writing dialogue straight into `.string "...\\n"` lines means choosing the
break points by eye, and the eye is wrong about them: the GBA font is
variable-width and half the lines end in a slot like {STR_VAR_1}, which is a
trainer's name on one playthrough and a move name on the next. So a line that
looks safe in the file clips on screen for somebody.

Write the prose as paragraphs instead and let this break them. Each slot is
charged its worst realistic content, and the wrapper narrows its budget until
the lines even out, so no page ends on a two-word straggler.

    box = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 12}, width=34)
    box.compose(("Hi! {PLAYER}!|It's me.", "Come and battle me."))

A "|" inside a paragraph forces a break -- for a greeting that belongs on its
own line, or a beat the prose depends on. Everything else is chosen here.

The final page ends in "$"; every other page ends in "\\p"; inside a page the
first line ends in "\\n" and the rest in "\\l", which is what the engine reads
as "scroll".
"""
from __future__ import annotations

BREAK = "|"


class TextBox:
    def __init__(self, slots: dict[str, int], width: int) -> None:
        self.slots = slots
        self.width = width

    def measured(self, text: str) -> int:
        """How wide the text gets once every slot holds its worst content."""
        for slot, cost in self.slots.items():
            text = text.replace(slot, "x" * cost)
        if "{" in text:
            raise ValueError(f"unpriced placeholder in: {text!r}")
        return len(text)

    def _greedy(self, words: list[str], width: int) -> list[str]:
        lines: list[str] = []
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if current and self.measured(candidate) > width:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        return lines

    def wrap(self, paragraph: str) -> list[str]:
        lines: list[str] = []
        for chunk in paragraph.split(BREAK):
            words = chunk.split()
            best = self._greedy(words, self.width)
            for width in range(self.width - 1, self.width * 2 // 3, -1):
                candidate = self._greedy(words, width)
                if len(candidate) != len(best):
                    break
                if min(map(self.measured, candidate)) > min(map(self.measured, best)):
                    best = candidate
            lines.extend(best)
        return lines

    def compose(self, paragraphs: tuple[str, ...]) -> tuple[str, ...]:
        payloads: list[str] = []
        pages = [self.wrap(paragraph) for paragraph in paragraphs]
        if not pages or not all(pages):
            raise ValueError("every paragraph must produce at least one line")
        for index, lines in enumerate(pages):
            last_page = index == len(pages) - 1
            for position, line in enumerate(lines):
                if position == len(lines) - 1:
                    code = "$" if last_page else "\\p"
                elif position == 0:
                    code = "\\n"
                else:
                    code = "\\l"
                payloads.append(line + code)
        return tuple(payloads)
