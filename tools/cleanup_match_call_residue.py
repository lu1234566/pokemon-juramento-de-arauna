#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Populated by focused narrative cleanup lots. Each block target is:
# (relative path, string label, expected .string lines, forbidden visible tokens)
STRING_BLOCK_TARGETS: tuple[tuple[str, str, tuple[str, ...], tuple[str, ...]], ...] = (
    (
        "data/text/match_call.inc",
        "MatchCall_Text_Steven1",
        (
            r"SEU BENTO: {PLAYER}, achei uma\n",
            r"anotacao antiga hoje.\p",
            r"Um nome aparece tres vezes e\n",
            r"some na pagina seguinte.\p",
            r"Continue ouvindo as pessoas.\n",
            r"Papel sozinho nao basta.$",
        ),
        ("STEVEN", "MAUVILLE", "BIKE SHOP"),
    ),
    (
        "data/text/match_call.inc",
        "MatchCall_Text_Steven2",
        (
            r"SEU BENTO: O caminho da serra\n",
            r"voltou a respirar.\p",
            r"Marcas antigas apareceram\n",
            r"onde a pedra foi aberta.\p",
            r"Anote o que vir. Eu comparo\n",
            r"com meus cadernos.$",
        ),
        ("STEVEN",),
    ),
    (
        "data/text/match_call.inc",
        "MatchCall_Text_Steven3",
        (
            r"SEU BENTO: Certos objetos\n",
            r"guardam mais que historia.\p",
            r"Nao confunda memoria com\n",
            r"resposta.\p",
            r"Uma pista tambem pode mentir.$",
        ),
        ("STEVEN",),
    ),
    (
        "data/text/match_call.inc",
        "MatchCall_Text_Steven4",
        (
            r"SEU BENTO: O movimento no\n",
            r"litoral mudou de repente.\p",
            r"Tem equipamento sumindo dos\n",
            r"registros oficiais.\p",
            r"No porto, confira cada lista\n",
            r"duas vezes.$",
        ),
        ("STEVEN",),
    ),
    (
        "data/text/match_call.inc",
        "MatchCall_Text_Steven5",
        (
            r"SEU BENTO: Missoes do Ceu\n",
            r"esta ouvindo sinais demais.\p",
            r"Quando toda rede fala junto,\n",
            r"o silencio importa mais.\p",
            r"Confie no que voce viu.$",
        ),
        ("STEVEN", "MOSSDEEP"),
    ),
    (
        "data/text/match_call.inc",
        "MatchCall_Text_Steven6",
        (
            r"O sinal de SEU BENTO nao\n",
            r"responde.\p",
            r"So ha estatica e o ruido\n",
            r"distante da agua.$",
        ),
        ("STEVEN",),
    ),
    (
        "data/text/match_call.inc",
        "MatchCall_Text_Steven7",
        (
            r"SEU BENTO: {PLAYER}, meus\n",
            r"cadernos nao registram tudo.\p",
            r"Talvez seja melhor assim.\p",
            r"Algumas coisas precisam viver\n",
            r"na boca das pessoas.$",
        ),
        ("STEVEN",),
    ),
    (
        "data/text/match_call.inc",
        "MatchCall_Text_BirchRegisterCall",
        (
            r"ANAHI: {PLAYER}, seu POKéNAV\n",
            r"ja esta recebendo chamadas.\p",
            r"Registre meu contato tambem.\p",
            r"Se eu encontrar algo estranho,\n",
            r"aviso voce primeiro.$",
        ),
        ("PROF. BIRCH", "BIRCH:"),
    ),
    (
        "data/text/pokedex_rating.inc",
        "gBirchDexRatingText_AreYouCurious",
        (
            r"ANAHI: {PLAYER}, quer conferir\n",
            r"como seus registros estao?$",
        ),
        ("PROF. BIRCH", "BIRCH:"),
    ),
)

# Populated by focused cleanup lots for visible constants that are not
# assembler-style .string blocks. Each replacement is:
# (relative path, exact old text, exact new text)
EXACT_REPLACEMENTS: tuple[tuple[str, str, str], ...] = (
    (
        "src/strings.c",
        'const u8 gText_StevenMatchCallDesc[] = _("HARD AS ROCK");',
        'const u8 gText_StevenMatchCallDesc[] = _("GUARDA NOMES");',
    ),
    (
        "src/strings.c",
        'const u8 gText_StevenMatchCallName[] = _("STEVEN");',
        'const u8 gText_StevenMatchCallName[] = _("SEU BENTO");',
    ),
    (
        "src/strings.c",
        'const u8 gText_ProfBirchMatchCallName[] = _("PROF. BIRCH");',
        'const u8 gText_ProfBirchMatchCallName[] = _("PROF. ANAHI");',
    ),
    (
        "src/strings.c",
        'const u8 gText_ProfBirchMatchCallDesc[] = _("{PKMN} PROF.");',
        'const u8 gText_ProfBirchMatchCallDesc[] = _("PESQUISADORA");',
    ),
    (
        "src/strings.c",
        'const u8 gText_HOFDexRating[] = _("Spotted POKéMON: {STR_VAR_1}!\\nOwned POKéMON: {STR_VAR_2}!\\pPROF. BIRCH\'s POKéDEX rating!\\pPROF. BIRCH: Let\'s see…\\p");',
        'const u8 gText_HOFDexRating[] = _("POKéMON vistos: {STR_VAR_1}!\\nRegistrados: {STR_VAR_2}!\\pAvaliacao da PROF. ANAHI!\\pANAHI: Vamos ver…\\p");',
    ),
    (
        "src/strings.c",
        'const u8 gText_BirchInTrouble[] = _("PROF. BIRCH is in trouble!\\nRelease a POKéMON and rescue him!");',
        'const u8 gText_BirchInTrouble[] = _("ANAHI esta em perigo!\\nSolte um POKéMON e ajude-a!");',
    ),
)


def block_pattern(label: str) -> re.Pattern[str]:
    # Map scripts generally use `Label:` while shared text tables may use
    # global assembler labels (`Label::`). Accept both and preserve the form.
    return re.compile(
        rf"(?m)^{re.escape(label)}(?P<suffix>::?)\n(?:\t\.string \"[^\n]*\"\n)+"
    )


def replace_string_block(text: str, label: str, lines: tuple[str, ...]) -> tuple[str, bool]:
    pattern = block_pattern(label)

    def replacement(match: re.Match[str]) -> str:
        suffix = match.group("suffix")
        return label + suffix + "\n" + "".join(f'\t.string "{line}"\n' for line in lines)

    updated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f"Could not uniquely replace {label} (matches={count})")
    return updated, updated != text


def extract_block(text: str, label: str) -> str:
    match = block_pattern(label).search(text)
    if not match:
        raise RuntimeError(f"Missing text block: {label}")
    return match.group(0)


def validate_block(
    block: str,
    rel_path: str,
    label: str,
    expected_lines: tuple[str, ...],
    forbidden_tokens: tuple[str, ...],
) -> list[str]:
    failures: list[str] = []
    for line in expected_lines:
        if f'\t.string "{line}"' not in block:
            failures.append(f"{rel_path}: {label} missing expected line: {line}")
    for token in forbidden_tokens:
        if token in block:
            failures.append(f"{rel_path}: {label} still contains visible legacy token: {token}")
    return failures


def apply() -> int:
    changed_files: set[Path] = set()

    for rel_path, label, lines, forbidden_tokens in STRING_BLOCK_TARGETS:
        path = ROOT / rel_path
        original = path.read_text(encoding="utf-8")
        updated, changed = replace_string_block(original, label, lines)
        if changed:
            path.write_text(updated, encoding="utf-8")
            changed_files.add(path)
        failures = validate_block(
            extract_block(updated, label), rel_path, label, lines, forbidden_tokens
        )
        if failures:
            raise RuntimeError("; ".join(failures))

    for rel_path, old, new in EXACT_REPLACEMENTS:
        path = ROOT / rel_path
        original = path.read_text(encoding="utf-8")
        if new in original and old not in original:
            continue
        count = original.count(old)
        if count != 1:
            raise RuntimeError(
                f"Could not uniquely replace exact text in {rel_path} (matches={count})"
            )
        updated = original.replace(old, new, 1)
        path.write_text(updated, encoding="utf-8")
        changed_files.add(path)

    print(
        "Arauna Match Call cleanup: "
        f"{len(changed_files)} file(s) changed; "
        f"{len(STRING_BLOCK_TARGETS)} block target(s) and "
        f"{len(EXACT_REPLACEMENTS)} exact replacement(s) verified."
    )
    return 0


def check() -> int:
    failures: list[str] = []

    for rel_path, label, lines, forbidden_tokens in STRING_BLOCK_TARGETS:
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        failures.extend(
            validate_block(
                extract_block(text, label), rel_path, label, lines, forbidden_tokens
            )
        )

    for rel_path, old, new in EXACT_REPLACEMENTS:
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        if old in text:
            failures.append(f"{rel_path}: legacy exact text remains: {old}")
        if new not in text:
            failures.append(f"{rel_path}: expected replacement missing: {new}")

    if failures:
        print("Arauna Match Call cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "Arauna Match Call cleanup check PASS: "
        f"{len(STRING_BLOCK_TARGETS)} block target(s), "
        f"{len(EXACT_REPLACEMENTS)} exact replacement(s)."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
