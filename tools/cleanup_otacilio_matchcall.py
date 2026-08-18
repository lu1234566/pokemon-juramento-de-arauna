#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATCH_CALL = ROOT / "data" / "text" / "match_call.inc"
STRINGS = ROOT / "src" / "strings.c"

CALLS: dict[str, tuple[str, ...]] = {
    "MatchCall_Text_MrStone1": (
        r"OTACILIO: {PLAYER}, o POKéNAV\n",
        r"esta funcionando como deveria.\p",
        r"Use os contatos para registrar\n",
        r"o que encontrar pelo caminho.\p",
        r"Eu estarei no centro da SERRA DO UIVO.$",
    ),
    "MatchCall_Text_MrStone2": (
        r"OTACILIO: Ainda esta com a CARTA?\p",
        r"SEU BENTO esta no PORTO DAS REDES.\n",
        r"Entregue a ele antes de seguir.\p",
        r"O pacote vai para o PORTO DO SAL.$",
    ),
    "MatchCall_Text_MrStone3": (
        r"OTACILIO: Entao encontrou SEU BENTO.\p",
        r"Quando voltar a SERRA DO UIVO,\n",
        r"passe no meu escritorio.\p",
        r"Tenho algo pelo trabalho concluido.$",
    ),
    "MatchCall_Text_MrStone4": (
        r"OTACILIO: As GALERIAS DA SERRA\n",
        r"ja foram um projeto do HORIZONTE.\p",
        r"Suspendemos a obra quando ficou claro\n",
        r"que a fauna seria deslocada.\p",
        r"Nem toda eficiencia justifica o custo.$",
    ),
    "MatchCall_Text_MrStone5": (
        r"OTACILIO: Soube que ELIAS e seu pai.\p",
        r"Ele participou de decisoes que ainda\n",
        r"pesam sobre o projeto de M'BOI.\p",
        r"Imagino que voce ja tenha perguntas.$",
    ),
    "MatchCall_Text_MrStone6": (
        r"OTACILIO: Voce enfrentou ELIAS?\p",
        r"Familia e VINCULO nao tornam uma\n",
        r"decisao automaticamente correta.\p",
        r"E bom que voce tenha descoberto isso cedo.$",
    ),
    "MatchCall_Text_MrStone7": (
        r"CONSORCIO HORIZONTE, bom dia.\p",
        r"{PLAYER}? O DR. OTACILIO saiu.\n",
        r"A agenda dele mudou de repente.\p",
        r"Posso registrar que voce ligou.$",
    ),
    "MatchCall_Text_MrStone8": (
        r"...{PLAYER}? O sinal esta ruim.\p",
        r"Voce disse... SERRA DA CINZA?\p",
        r"Nao estou recebendo os dados.\n",
        r"Tente novamente fora da area.$",
    ),
    "MatchCall_Text_MrStone9": (
        r"...{PLAYER}? Estou perdendo o sinal.\p",
        r"Cavernas... M'BOI...?\p",
        r"Saia da zona subterranea antes\n",
        r"de tentar transmitir os registros.$",
    ),
    "MatchCall_Text_MrStone10": (
        r"OTACILIO: {PLAYER}, ouvi relatos\n",
        r"sobre o que aconteceu em M'BOI.\p",
        r"O ARQUIVO VIVO foi criado para\n",
        r"impedir outra noite como aquela.\p",
        r"Nao vou fingir que isso encerra\n",
        r"a discussao sobre como ele deve ser usado.$",
    ),
    "MatchCall_Text_MrStone11": (
        r"OTACILIO: Sua voz mudou, {PLAYER}.\p",
        r"Voce ja nao parece esperar que\n",
        r"alguem escolha a resposta por voce.\p",
        r"Continue assim. Mesmo quando\n",
        r"a resposta contrariar a minha.$",
    ),
}

EXACT = {
    'const u8 gText_MrStoneMatchCallDesc[] = _("DEVON PRES");': 'const u8 gText_MrStoneMatchCallDesc[] = _("DIRETOR");',
    'const u8 gText_MrStoneMatchCallName[] = _("MR. STONE");': 'const u8 gText_MrStoneMatchCallName[] = _("OTACILIO");',
}

FORBIDDEN = ("MR. STONE", "DEVON", "STEVEN", "RUSTBORO", "DEWFORD", "PETALBURG", "NORMAN")


def marker_for(text: str, label: str) -> str:
    for suffix in ("::\n", ":\n"):
        marker = label + suffix
        if marker in text:
            return marker
    raise RuntimeError(f"Missing Otacilio Match Call block: {label}")


def bounds(text: str, label: str) -> tuple[int, int, str]:
    marker = marker_for(text, label)
    start = text.find(marker)
    end = text.find("\n\n", start)
    if end < 0:
        end = len(text)
    else:
        end += 1
    return start, end, marker


def render(marker: str, lines: tuple[str, ...]) -> str:
    return marker + "".join(f'\t.string "{line}"\n' for line in lines)


def validate_calls(text: str) -> list[str]:
    failures: list[str] = []
    for label, lines in CALLS.items():
        start, end, marker = bounds(text, label)
        block = text[start:end]
        if block != render(marker, lines):
            failures.append(f"{label} differs from canonical OTACILIO call")
        for token in FORBIDDEN:
            if token in block:
                failures.append(f"{label} still exposes legacy token: {token}")
    return failures


def validate_strings(text: str) -> list[str]:
    failures: list[str] = []
    for old, new in EXACT.items():
        if new not in text:
            failures.append(f"missing Otacilio PokéNav constant: {new}")
        if old in text:
            failures.append(f"legacy Mr. Stone PokéNav constant remains: {old}")
    return failures


def apply() -> int:
    call_text = MATCH_CALL.read_text(encoding="utf-8")
    call_changed = 0
    for label, lines in CALLS.items():
        start, end, marker = bounds(call_text, label)
        replacement = render(marker, lines)
        if call_text[start:end] != replacement:
            call_text = call_text[:start] + replacement + call_text[end:]
            call_changed += 1
    failures = validate_calls(call_text)
    if failures:
        raise RuntimeError("; ".join(failures))
    MATCH_CALL.write_text(call_text, encoding="utf-8")

    string_text = STRINGS.read_text(encoding="utf-8")
    exact_changed = 0
    for old, new in EXACT.items():
        if new in string_text and old not in string_text:
            continue
        count = string_text.count(old)
        if count != 1:
            raise RuntimeError(f"Expected exactly one {old!r}, found {count}")
        string_text = string_text.replace(old, new, 1)
        exact_changed += 1
    failures = validate_strings(string_text)
    if failures:
        raise RuntimeError("; ".join(failures))
    STRINGS.write_text(string_text, encoding="utf-8")

    print(f"Otacilio Match Call cleanup: {call_changed} calls and {exact_changed} PokéNav constants changed.")
    return 0


def check() -> int:
    failures = validate_calls(MATCH_CALL.read_text(encoding="utf-8"))
    failures.extend(validate_strings(STRINGS.read_text(encoding="utf-8")))
    if failures:
        print("Otacilio Match Call cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Otacilio Match Call cleanup check PASS: {len(CALLS)} calls and {len(EXACT)} constants.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
