#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import audit_visible_residue as base
from render_porto_sal_battle_tent import render_asm as render_battle_tent_asm, render_strings as render_battle_tent_strings
from render_porto_sal_berry_powder import render_city as render_berry_powder_city, render_strings as render_berry_powder_strings
from render_porto_sal_civic_signs import render as render_civic_signs
from render_porto_sal_daily_life import render as render_porto_sal_daily_life
from render_porto_sal_fan_club import render_item_descs as render_fan_club_descs, render_items as render_fan_club_items, render_map as render_fan_club
from render_porto_sal_harbor_service import render_harbor as render_harbor_service, render_strings as render_harbor_strings
from render_porto_sal_museum_people_checked import (
    render_city as render_museum_queue,
    render_museum as render_museum_people_1f,
)
from render_porto_sal_museum_science import render_1f as render_museum_science_1f, render_2f as render_museum_science_2f
from render_porto_sal_name_rater import render as render_name_rater
from render_porto_sal_seu_bento import render as render_porto_sal_seu_bento
from render_porto_sal_shipyard import render_1f as render_shipyard_1f, render_2f as render_shipyard_2f

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_RENDER_ASM = base.render_asm_source
ORIGINAL_RENDER_C = base.render_c_source


def render_asm_source(path: Path, source: str) -> str:
    rendered = ORIGINAL_RENDER_ASM(path, source)
    rendered = render_battle_tent_asm(path, rendered)
    if path == ROOT / "data" / "maps" / "SlateportCity" / "scripts.inc":
        rendered = render_museum_queue(rendered)
        rendered = render_civic_signs(rendered)
        rendered = render_porto_sal_daily_life(rendered)
        rendered = render_porto_sal_seu_bento(rendered)
        return render_berry_powder_city(rendered)
    if path == ROOT / "data" / "maps" / "SlateportCity_Harbor" / "scripts.inc":
        return render_harbor_service(rendered)
    if path == ROOT / "data" / "maps" / "SlateportCity_NameRatersHouse" / "scripts.inc":
        return render_name_rater(rendered)
    if path == ROOT / "data" / "maps" / "SlateportCity_OceanicMuseum_1F" / "scripts.inc":
        return render_museum_science_1f(render_museum_people_1f(rendered))
    if path == ROOT / "data" / "maps" / "SlateportCity_OceanicMuseum_2F" / "scripts.inc":
        return render_museum_science_2f(rendered)
    if path == ROOT / "data" / "maps" / "SlateportCity_PokemonFanClub" / "scripts.inc":
        return render_fan_club(rendered)
    if path == ROOT / "data" / "maps" / "SlateportCity_SternsShipyard_1F" / "scripts.inc":
        return render_shipyard_1f(rendered)
    if path == ROOT / "data" / "maps" / "SlateportCity_SternsShipyard_2F" / "scripts.inc":
        return render_shipyard_2f(rendered)
    return rendered


def render_c_source(path: Path, source: str) -> str:
    rendered = ORIGINAL_RENDER_C(path, source)
    if path == ROOT / "src" / "strings.c":
        rendered = render_berry_powder_strings(rendered)
        rendered = render_harbor_strings(rendered)
        return render_battle_tent_strings(rendered)
    if path == ROOT / "src" / "data" / "items.h":
        return render_fan_club_items(rendered)
    if path == ROOT / "src" / "data" / "text" / "item_descriptions.h":
        return render_fan_club_descs(rendered)
    return rendered


base.render_asm_source = render_asm_source
base.render_c_source = render_c_source


if __name__ == "__main__":
    raise SystemExit(base.main())
