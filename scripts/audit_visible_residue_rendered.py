#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import audit_visible_residue as base
from render_porto_sal_civic_signs import render as render_civic_signs
from render_porto_sal_daily_life import render as render_porto_sal_daily_life
from render_porto_sal_museum_people_checked import (
    render_city as render_museum_queue,
    render_museum as render_museum_people_1f,
)
from render_porto_sal_museum_science import render_1f as render_museum_science_1f, render_2f as render_museum_science_2f
from render_porto_sal_seu_bento import render as render_porto_sal_seu_bento
from render_porto_sal_shipyard import render_1f as render_shipyard_1f, render_2f as render_shipyard_2f

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_RENDER_ASM = base.render_asm_source


def render_asm_source(path: Path, source: str) -> str:
    rendered = ORIGINAL_RENDER_ASM(path, source)
    if path == ROOT / "data" / "maps" / "SlateportCity" / "scripts.inc":
        return render_porto_sal_seu_bento(render_porto_sal_daily_life(render_civic_signs(render_museum_queue(rendered))))
    if path == ROOT / "data" / "maps" / "SlateportCity_OceanicMuseum_1F" / "scripts.inc":
        return render_museum_science_1f(render_museum_people_1f(rendered))
    if path == ROOT / "data" / "maps" / "SlateportCity_OceanicMuseum_2F" / "scripts.inc":
        return render_museum_science_2f(rendered)
    if path == ROOT / "data" / "maps" / "SlateportCity_SternsShipyard_1F" / "scripts.inc":
        return render_shipyard_1f(rendered)
    if path == ROOT / "data" / "maps" / "SlateportCity_SternsShipyard_2F" / "scripts.inc":
        return render_shipyard_2f(rendered)
    return rendered


base.render_asm_source = render_asm_source


if __name__ == "__main__":
    raise SystemExit(base.main())
