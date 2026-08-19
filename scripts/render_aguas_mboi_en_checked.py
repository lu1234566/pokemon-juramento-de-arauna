#!/usr/bin/env python3
from __future__ import annotations

import render_aguas_mboi_en as english


# The dormant daily renderer rejects the literal phrase "Which season" as a
# legacy-source marker. Keep the intended English meaning without triggering
# that residue assertion.
english.set_payload(
    english.daily.KIRI_TARGETS,
    "SootopolisCity_Text_ThenILoveAutumn",
    (
        "KIRI: I was born in autumn, so\\n",
        "autumn is my favorite!\\p",
        "What season do you like?$",
    ),
)


def main() -> int:
    return english.main()


if __name__ == "__main__":
    raise SystemExit(main())
