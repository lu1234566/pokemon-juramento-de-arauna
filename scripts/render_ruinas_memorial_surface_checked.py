#!/usr/bin/env python3
from __future__ import annotations

import re

import render_ruinas_memorial_surface as base


def patch_width_sensitive_payloads() -> None:
    markers, _ = base.MEMORIAL_TARGETS["MtPyre_Summit_Text_ArchieWeGotTheOrbLetsGo"]
    base.MEMORIAL_TARGETS["MtPyre_Summit_Text_ArchieWeGotTheOrbLetsGo"] = (
        markers,
        (
            "OTACILIO: Temos o REGISTRO\\n",
            "MATRIZ. Recolham a equipe.\\p",
            "Vamos.$",
        ),
    )

    markers, _ = base.MEMORIAL_TARGETS["MtPyre_Summit_Text_HoennTrioTale"]
    base.MEMORIAL_TARGETS["MtPyre_Summit_Text_HoennTrioTale"] = (
        markers,
        (
            "GUARDIA: Durante muito tempo,\\n",
            "contamos que lembrar era sempre\\n",
            "justo. Esquecer era sempre\\n",
            "tratado como perda.\\p",
            "M'BOI mostrou que absolutos\\n",
            "tambem ferem.\\p",
            "O novo JURAMENTO nao manda\\n",
            "lembrar tudo nem apagar a dor.\\p",
            "Ele exige que nenhuma pessoa\\n",
            "decida sozinha pelo resto.$",
        ),
    )


def patch_item_description_layout() -> None:
    base.ITEM_DESC_RE = re.compile(
        r'(?ms)^static const u8 sMagmaEmblemDesc\[\] = _\(\n'
        r'(?P<body>.*?^\s*"[^"\n]*"\);)'
    )


patch_width_sensitive_payloads()
patch_item_description_layout()

render_meteor = base.render_meteor
render_memorial = base.render_memorial
render_items = base.render_items
render_item_descs = base.render_item_descs
rendered_sources = base.rendered_sources
METEOR_PATH = base.METEOR_PATH
MEMORIAL_PATH = base.MEMORIAL_PATH
ITEMS_PATH = base.ITEMS_PATH
ITEM_DESCS_PATH = base.ITEM_DESCS_PATH
METEOR_TARGETS = base.METEOR_TARGETS
MEMORIAL_TARGETS = base.MEMORIAL_TARGETS


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
