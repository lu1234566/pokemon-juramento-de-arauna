#!/usr/bin/env python3
from pathlib import Path
import base64
import re

ROOT = Path.cwd()

CIRO_BRENDAN = "iVBORw0KGgoAAAANSUhEUgAAAJAAAAAgBAMAAAAPouz+AAAAMFBMVEVzxaT/1bT/xZTelHN7QUE5SnspOWIYKVIQIDne5u5zzXNKlFL/YlrFQUH///8AAAAvIM4SAAAAAXRSTlMAQObYZgAABFBJREFUeNrt1cGLXlcZBvDfd3PG3KBh7tR2IZaQlIIuAh00Fq1fzEl7wSym8Flaq5ui/8HgQqMM9i5GiUVxhCwFF7rPYDZZ3CanSYQIFj6xSBGsYy0lau184yT2jnOS6+LOmJT+BYJn817ue87L+/A+7/Pw//M/fuJ936FulKurzQdvhTOhHuLr92XDfTdWSfcSgS5YoRyP31cu5NxCc305QxiHQxcV9zpZTem+sl1OOAtuQH2Gc3VkZe9GksaQU9ylINR1g5BmLN6D2F6v41no6s9CjKS4xgCMOnb7nWYKXpSuwd3eZkCozzRDudBAmUHTklYWObs0INiPQ+kDyrtbZT9/05MOzmYfO7Jx+POjN958g1CV/e/eRtx484XE3b9/t/gDlL8vjmwM8YUE5/J3KGTzm1sPRtHIMdF7Zu40NL0ewp/0r8K3khMIYw5EjPU/nyK0KVIcjsyRyjQaVTOvot/8yw1lsvnP6kc0R2cb7yFcmPUD4n5zNszYaJnXYj8LFNuMPryg6QSbExdF1UNHMxYWKhex5ZiGadVvVk/DaDYKUer7P1eBxZn5zagQR27PQiPunuqFKaOtv/13dFFIVcV1WHjAthB7xyrpcByN5qtArGazUakQRNU7rGpcuLkoqYqYdQkhGUbWsjxCKQ+cnW6nPi7IxH5hocpNodm8srOxRDd6bDRXEe6etBYHkse0F+2RvqMencKi83uzb+ZwqCl0X9rcerBB/eW3J5Hu9Po/jjao67rbw5gH0pE4e3JdHPPJeKWfjTn0xKkcP60gPPOvyZQyWXYe36se+CpO4hcIoa6ToXCEq3dvhQb9xu1nG7bT+lZqFMJaWN6J7Mw6O1B98bnbU6aJO1M+h9dRrnMHXjk4Ad/fmpjiJw7WFE7mrnslIN/YvXZnKuDK08oit+0jkQNtmz+OncxaRJ7QoLvFOp54boLCRnX+anGHJ71zOVj2oqS4zQLx9GzY81HDpyZtu/wW5B8oUTY7ayW2vaRR+OijR4rwjcYX5t99ymPR6OHftHOPT3cfreuUTxJCrcJvCdfmUf54lFvkNmlxeLfPNxRl/8P+Vryc/PL01342Lrkw7aO/rs/FthWuOTzLbThF+XBiLPLtdx8ZsPHvgG9e/oSsMDrxfOWpZMGHvh5uKud8JngmdU1dx8z2R+o6zjXyzUj5UOLqwUkYxPXA4xkOLl2Piu6nsY1a2pCCrzTdmdUxLydzezqcyB25e7aOLuHlZo/u8dQs4KUYxklhcS0MT7KJjkbYW4u8DjnPhQmsWwLl4Ay6MFdewm4SxgqO54nxPt8xEWJi+9fNUkKZtq3DihOX7Ks7NGmQyNigGGyhQZMGxT6ed1vYDqlErq8PixpSl3AuXurG+Z62l82vOjcUyMeXoIlyg0PtKOzLO/LZdngx3heCaHWYWgsr7baVDK/tu0Jd1tOh9b0/f3y/Mw7JcnW6ZySDSZSrUX3GfwCHA8SHMYldvwAAAABJRU5ErkJggg=="
CIRO_MAY = "iVBORw0KGgoAAAANSUhEUgAAAJAAAAAgBAMAAAAPouz+AAAAMFBMVEVzxaT/3s3epJTNg3N7WlJiYnMpOUGkalJKMTnNzd5q1UFBrCD/YlrFQUH///8AAAAiB9ZeAAAAAXRSTlMAQObYZgAABMlJREFUeNrtld1rHFUYxn8zmWVGkuVMtTZV0cQPpGBrt6ZgtK27lhUrUkylfoB6X7HqaJFNoZKxSenshZ0VRC+reFX0YvFbSOnWfoDYpSNVjDc2iBRrRc9kt/SM3fX1YqIG/AsEz817Pp7zPDyc874v/D/+4yNcMvcijTJG/xvlxl4E4MVnl5w6SxCm12r9A3chdfFA7d7hLyXyMjMJoN9sZgDepFfYhQ0QAHBpz8Sd/8DTrAFYABwEiGKQKITzi4gG4Q4AEwYLuUK1qwGntr5aKy2x6M0sWhUNYARik4DI4rb8bSUCGy6MhdMAl6U06wFedUoD7Dx2SQMoA4Bfh9ArgfVdLvBXBLcGA6jPvx2VSz+xeeVvc/q6J1vFu9bPHj0JzuXx3vQ5IDh84qMIel+k7W8AVOHL6+cBZfU/igAkK4DNxVL5yNFqSDOx2L464HKplfQ1dHrIAOC+N9B7FeDncO044I2fKo2FwPiZ3lgCOC9NBeAUa78x1CVUE+vpHfafopf0fvn4BlSDWWfTyQH0ntYv2wBvo7NRgD1aZilCNzyDE8DcztPdCtidFsur1USn1bllR47xAWHJf3LiMzhcrVYGpoHjbEfDqUrvyKat0BpwtOOETMjqD30HVnfYOFvBpun0Zw8P+gTrnxEeTDj+Vfedfg+aSdJuB3hbK5UkeRyget9AB6/ZY3uFsNgsLB+qbIBwk245CpvBr3bhn4dh7bPx7RKzbC2EPdKJfp/BBqbSbq/hU2h+Df2HMK8n/X6bpNP4Mqj2T0Bwelu1clHb+Bf2LPz4KaRXr7WGJmDwnmetW5pw3KHSDGEGkg+BsN9uJynUqlMO1RJPVKy274A/1G23H/ABc8dN5fyDjYgGOutuHAc8EdGAZ2a2aICZmS0zAOnY/UYDnV3T4xqKC50gT0kxI5KAmhKRlYB6YawPvCIiqwAlImEuJAZgel1ZABZuzuOLY+vyJB4RSX2wylrSYWBEZCGBZbHIjUlOOAKoskgK4Jbz5FDDIglwZqwsYLM7S9PXPCA72H3j9wQPiLeibFOvP1yBk9FkthxYyGA0ALIWaCA1MArcfaoF2Lzlr9pbyGAvhw54BFyggX0RrrbYuU/DGmtZ7Gi440gUzX8CkF2JApReGFVAh6vQ2Kx47NoV5gfNcxt+rvF8k8I19frQs0n3sVrtdbMJBt2atQz4xrK8R4cAdZ2V1YGs3qAOFLuSHcRWvUfkk/BAg837ktueVrDh9OWA90eHwnod7xjFVlZ33wW1sqE5RAg//HprXlk0HRc4d+B2MlDjSmIxsN+IkZJWZS+WuBOiRIwGIhER8JSJYomBaWUk0qD2748joBNfig2QxFH+vhKLCGgxEodQ/OsfLRJyVhZLmRgTaVCmU46BooiJsClNuOABGfOk4ONmANSzCoDJ/nDnAUb5DgAFbs2H1B269wXAbuDuyPvFWdGAic/KUuWiZ0JARTqvtZ6oEECJiqcAVKwX1znAnZozAK5SAuCZTpRLRzHgSWRygjg3FgeYKGfQgJKXkRgbrCtWzQGkIZkGClHBzWtxLQCMNZm3md2LjgkZRudT4Hx9gCsybDitKQHEGY15oBOSX0m/txY7mQ8wuQWA/U/Pk+EDu12A4QBClz8BeE9JNBMgplIAAAAASUVORK5CYII="


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def patch_graphics() -> None:
    path = ROOT / "src/data/object_events/object_event_graphics.h"
    text = path.read_text(encoding="utf-8")
    anchor = 'const u32 gObjectEventPic_BrendanRunning[] = INCGFX_U32("graphics/object_events/pics/people/brendan/running.png", ".4bpp", "-mwidth 2 -mheight 4");\n'
    insert = anchor + (
        'const u32 gObjectEventPic_CiroBrendan[] = INCGFX_U32("graphics/object_events/pics/people/ciro/phase1_brendan.png", ".4bpp", "-mwidth 2 -mheight 4");\n'
        'const u32 gObjectEventPic_CiroMay[] = INCGFX_U32("graphics/object_events/pics/people/ciro/phase1_may.png", ".4bpp", "-mwidth 2 -mheight 4");\n'
    )
    text = replace_once(text, anchor, insert, "object_event_graphics Ciro declarations")
    path.write_text(text, encoding="utf-8")


def ciro_table(name: str, pic: str) -> str:
    lines = [f"static const struct SpriteFrameImage {name}[] = {{\n"]
    for _pass in range(2):
        for frame in range(9):
            lines.append(f"    overworld_frame({pic}, 2, 4, {frame}),\n")
    lines.append("};\n\n")
    return "".join(lines)


def patch_pic_tables() -> None:
    path = ROOT / "src/data/object_events/object_event_pic_tables.h"
    text = path.read_text(encoding="utf-8")
    anchor = "static const struct SpriteFrameImage sPicTable_BrendanMachBike[] = {\n"
    block = (
        ciro_table("sPicTable_CiroBrendan", "gObjectEventPic_CiroBrendan")
        + ciro_table("sPicTable_CiroMay", "gObjectEventPic_CiroMay")
        + anchor
    )
    text = replace_once(text, anchor, block, "object_event_pic_tables Ciro tables")
    path.write_text(text, encoding="utf-8")


def replace_images_in_struct(text: str, struct_name: str, old_table: str, new_table: str) -> str:
    pattern = re.compile(
        rf"(const struct ObjectEventGraphicsInfo {re.escape(struct_name)} = \{{.*?\n\}};)",
        re.DOTALL,
    )
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{struct_name}: expected one struct, found {len(matches)}")
    block = matches[0].group(1)
    old_line = f"    .images = {old_table},"
    new_line = f"    .images = {new_table},"
    if block.count(old_line) != 1:
        raise RuntimeError(f"{struct_name}: expected image table {old_table} exactly once")
    block2 = block.replace(old_line, new_line, 1)
    return text[:matches[0].start()] + block2 + text[matches[0].end():]


def patch_graphics_info() -> None:
    path = ROOT / "src/data/object_events/object_event_graphics_info.h"
    text = path.read_text(encoding="utf-8")
    text = replace_images_in_struct(
        text,
        "gObjectEventGraphicsInfo_RivalBrendanNormal",
        "sPicTable_BrendanNormal",
        "sPicTable_CiroBrendan",
    )
    text = replace_images_in_struct(
        text,
        "gObjectEventGraphicsInfo_RivalMayNormal",
        "sPicTable_MayNormal",
        "sPicTable_CiroMay",
    )
    path.write_text(text, encoding="utf-8")


def write_pngs() -> None:
    out = ROOT / "graphics/object_events/pics/people/ciro"
    out.mkdir(parents=True, exist_ok=True)
    (out / "phase1_brendan.png").write_bytes(base64.b64decode(CIRO_BRENDAN))
    (out / "phase1_may.png").write_bytes(base64.b64decode(CIRO_MAY))


def validate() -> None:
    g = (ROOT / "src/data/object_events/object_event_graphics.h").read_text(encoding="utf-8")
    p = (ROOT / "src/data/object_events/object_event_pic_tables.h").read_text(encoding="utf-8")
    i = (ROOT / "src/data/object_events/object_event_graphics_info.h").read_text(encoding="utf-8")
    assert g.count("gObjectEventPic_CiroBrendan") == 1
    assert g.count("gObjectEventPic_CiroMay") == 1
    assert p.count("sPicTable_CiroBrendan") == 1
    assert p.count("sPicTable_CiroMay") == 1
    assert i.count(".images = sPicTable_CiroBrendan,") == 1
    assert i.count(".images = sPicTable_CiroMay,") == 1
    assert "gObjectEventGraphicsInfo_BrendanNormal" in i
    assert "gObjectEventGraphicsInfo_MayNormal" in i


def main() -> None:
    write_pngs()
    patch_graphics()
    patch_pic_tables()
    patch_graphics_info()
    validate()
    print("Ciro phase 1 overworld mapping generated successfully")


if __name__ == "__main__":
    main()
