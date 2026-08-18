#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Keep the Emerald event graph and object scripts intact. These replacements
# touch only visible text blocks whose vanilla identities leak through Arauna.
TARGETS = (
    (
        "data/maps/RustboroCity/scripts.inc",
        "RustboroCity_Text_GymSign",
        (r"SERRA DO UIVO\n", r"RESPONSAVEL: DALVA\p", r"A serra lembra.$"),
    ),
    (
        "data/maps/DewfordTown/scripts.inc",
        "DewfordTown_Text_GymSign",
        (r"PORTO DAS REDES\n", r"RESPONSAVEL: ADEMAR\p", r"O mar devolve historias.$"),
    ),
    (
        "data/maps/MauvilleCity/scripts.inc",
        "MauvilleCity_Text_GymSign",
        (r"ENCRUZILHADA CENTRAL\n", r"RESPONSAVEL: OLIVIA\p", r"Toda rede deixa rastros.$"),
    ),
    (
        "data/maps/LavaridgeTown/scripts.inc",
        "LavaridgeTown_Text_GymSign",
        (r"CASA DA CINZA\n", r"RESPONSAVEL: NARA\p", r"Cinza tambem guarda memoria.$"),
    ),
    (
        "data/maps/PetalburgCity/scripts.inc",
        "PetalburgCity_Text_GymSign",
        (r"PAMPA DA ESPERA\n", r"RESPONSAVEL: ELIAS\p", r"Voltar nao apaga o caminho.$"),
    ),
    (
        "data/maps/FortreeCity/scripts.inc",
        "FortreeCity_Text_GymSign",
        (r"MATA DO MEIO\n", r"RESPONSAVEL: LIDIA\p", r"Escute antes de subir.$"),
    ),
    (
        "data/maps/MossdeepCity/scripts.inc",
        "MossdeepCity_Text_GymSign",
        (r"MISSOES DO CEU\n", r"CECILIA E CAETANO\p", r"Toda estrela tem testemunhas.$"),
    ),
    (
        "data/maps/SootopolisCity/scripts.inc",
        "SootopolisCity_Text_GymSign",
        (r"M'BOI\n", r"RESPONSAVEL: DONA CELINA\p", r"A agua lembra por nos.$"),
    ),
    (
        "data/maps/RustboroCity/scripts.inc",
        "RustboroCity_Text_WeShortenItToDevon",
        (
            r"O CONSORCIO HORIZONTE mantem\n",
            r"um centro tecnico na serra.\p",
            r"Muita gente daqui depende dele,\n",
            r"mas nem todos confiam no projeto.$",
        ),
    ),
    (
        "data/maps/RustboroCity/scripts.inc",
        "RustboroCity_Text_MayHiLetsRegister",
        (
            r"CIRO: Voce ativou o contato\n",
            r"do seu POKéNAV? Registre o meu.\p",
            r"Assim ninguem pode dizer que eu\n",
            r"sumi quando chegar antes de voce.$",
        ),
    ),
    (
        "data/maps/RustboroCity/scripts.inc",
        "RustboroCity_Text_RegisteredMay",
        (r"CIRO foi registrado\n", r"no POKéNAV.$"),
    ),
    (
        "data/maps/RustboroCity/scripts.inc",
        "RustboroCity_Text_BrendanHiLetsRegister",
        (
            r"CIRO: Voce ativou o contato\n",
            r"do seu POKéNAV? Registre o meu.\p",
            r"Assim ninguem pode dizer que eu\n",
            r"sumi quando chegar antes de voce.$",
        ),
    ),
    (
        "data/maps/RustboroCity/scripts.inc",
        "RustboroCity_Text_RegisteredBrendan",
        (r"CIRO foi registrado\n", r"no POKéNAV.$"),
    ),
    (
        "data/maps/RustboroCity/scripts.inc",
        "RustboroCity_Text_DevonCorpSign",
        (r"CONSORCIO HORIZONTE\p", r"CENTRO TECNICO\n", r"SERRA DO UIVO.$"),
    ),
    (
        "data/maps/RustboroCity/scripts.inc",
        "RustboroCity_Text_DevonCorpBranchOfficeSign",
        (
            r"CONSORCIO HORIZONTE\p",
            r"ACESSO RESTRITO A FUNCIONARIOS\n",
            r"E PESSOAL AUTORIZADO.$",
        ),
    ),
)

LEGACY_TOKENS = (
    "ROXANNE",
    "BRAWLY",
    "WATTSON",
    "FLANNERY",
    "NORMAN",
    "WINONA",
    "TATE & LIZA",
    "TATE AND LIZA",
    "LIZA & TATE",
    "JUAN",
    "MAY:",
    "BRENDAN:",
    "Registered MAY",
    "Registered BRENDAN",
    "HORIZONTEORATION",
    "DEVON",
)


def replace_string_block(text: str, label: str, lines: tuple[str, ...]) -> tuple[str, bool]:
    pattern = re.compile(
        rf"(?m)^{re.escape(label)}:\n(?:\t\.string \"[^\n]*\"\n)+"
    )
    replacement = label + ":\n" + "".join(f'\t.string "{line}"\n' for line in lines)
    new_text, count = pattern.subn(lambda _match: replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f"Could not uniquely replace {label} (matches={count})")
    return new_text, new_text != text


def extract_block(text: str, label: str) -> str:
    match = re.search(
        rf"(?m)^{re.escape(label)}:\n(?:\t\.string \"[^\n]*\"\n)+",
        text,
    )
    if not match:
        raise RuntimeError(f"Missing text block: {label}")
    return match.group(0)


def validate_block(block: str, rel_path: str, label: str, expected_lines: tuple[str, ...]) -> list[str]:
    failures: list[str] = []
    for line in expected_lines:
        if f'\t.string "{line}"' not in block:
            failures.append(f"{rel_path}: {label} missing expected line: {line}")
    for token in LEGACY_TOKENS:
        if token in block:
            failures.append(f"{rel_path}: {label} still contains legacy token: {token}")
    return failures


def apply() -> int:
    changed_files: set[Path] = set()
    for rel_path, label, lines in TARGETS:
        path = ROOT / rel_path
        original = path.read_text(encoding="utf-8")
        updated, did_change = replace_string_block(original, label, lines)
        if did_change:
            path.write_text(updated, encoding="utf-8")
            changed_files.add(path)
        block = extract_block(updated, label)
        failures = validate_block(block, rel_path, label, lines)
        if failures:
            raise RuntimeError("; ".join(failures))
    print(
        f"Arauna visible-residue cleanup: {len(changed_files)} file(s) changed; "
        f"{len(TARGETS)} target block(s) verified."
    )
    return 0


def check() -> int:
    failures: list[str] = []
    for rel_path, label, expected_lines in TARGETS:
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        block = extract_block(text, label)
        failures.extend(validate_block(block, rel_path, label, expected_lines))
    if failures:
        print("Arauna visible-residue cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Arauna visible-residue cleanup check PASS: {len(TARGETS)} target block(s) are Arauna-native.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
