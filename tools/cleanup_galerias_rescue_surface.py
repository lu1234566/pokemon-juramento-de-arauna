#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS: dict[str, dict[str, tuple[str, ...]]] = {
    "data/maps/Route116/scripts.inc": {
        "Route116_Text_ScoundrelMadeOffWithPeeko": (
            r"BARQUEIRO: Levaram minha companheira!\p",
            r"Um agente entrou nas GALERIAS DA SERRA\n",
            r"com ela e o pacote roubado.\p",
            r"Por favor, traga-a de volta.$",
        ),
        "Route116_Text_DiggingTunnelWhenGoonOrderedMeOut": (
            r"Eu trabalhava nas galerias quando\n",
            r"um agente mandou todo mundo sair.\p",
            r"Os POKéMON daqui reagem mal\n",
            r"a barulho e equipamento pesado.\p",
            r"Se ele fizer alguma besteira,\n",
            r"a passagem inteira pode virar caos.$",
        ),
        "Route116_Text_GoonHightailedItOutOfTunnel": (
            r"O agente saiu correndo das galerias.\p",
            r"Agora posso voltar ao trabalho.$",
        ),
        "Route116_Text_ThankYouTokenOfAppreciation": (
            r"PESQUISADOR: {PLAYER}!\p",
            r"Voce recuperou meus registros,\n",
            r"o pacote e ainda garantiu a entrega.\p",
            r"O centro da SERRA DO UIVO confirmou\n",
            r"que tudo chegou ao destino.\p",
            r"Quero agradecer com uma POKé BOLA\n",
            r"que acabou de entrar em producao.$",
        ),
        "Route116_Text_NewBallAvailableAtMart": (
            r"Essa POKé BOLA tambem sera vendida\n",
            r"na loja da SERRA DO UIVO.\p",
            r"Experimente quando puder.$",
        ),
        "Route116_Text_TokenOfAppreciation": (
            r"PESQUISADOR: Ainda quero lhe dar\n",
            r"a POKé BOLA que separei como agradecimento.$",
        ),
        "Route116_Text_BagIsJamPacked": (
            r"PESQUISADOR: Sua BOLSA esta cheia.\p",
            r"Abra espaco e fale comigo.$",
        ),
        "Route116_Text_RouteSignRustboro": (
            r"ROTA 116\n",
            r"{LEFT_ARROW} SERRA DO UIVO$",
        ),
        "Route116_Text_RusturfTunnelSign": (
            r"GALERIAS DA SERRA\p",
            r"PASSAGEM EM MANUTENCAO$",
        ),
    },
    "data/maps/RusturfTunnel/scripts.inc": {
        "RusturfTunnel_Text_ComeAndGetSome": (
            r"AGENTE HORIZONTE: Veio atras de mim?\p",
            r"Entao venha buscar.$",
        ),
        "RusturfTunnel_Text_Peeko": (
            r"POKéMON: Pii pihyoh!$",
        ),
        "RusturfTunnel_Text_GruntIntro": (
            r"AGENTE HORIZONTE: Que trabalho ruim.\p",
            r"Eu devia recolher o pacote sem\n",
            r"chamar atencao, e agora estou preso\n",
            r"numa galeria sem saida.\p",
            r"Nao vou devolver os dados sem luta.$",
        ),
        "RusturfTunnel_Text_GruntDefeat": (
            r"AGENTE HORIZONTE: Isso saiu\n",
            r"completamente do plano.$",
        ),
        "RusturfTunnel_Text_GruntTakePackage": (
            r"AGENTE HORIZONTE: Chega.\p",
            r"A ordem era recolher esse pacote\n",
            r"sem deixar registro.\p",
            r"Se voce quer tanto, fique com ele.\n",
            r"Eu nao vou responder por isso.$",
        ),
        "RusturfTunnel_Text_PeekoGladToSeeYouSafe": (
            r"BARQUEIRO: Ai esta voce!\p",
            r"Ainda bem que esta segura.$",
        ),
        "RusturfTunnel_Text_ThankYouLetsGoHomePeeko": (
            r"BARQUEIRO: Voce salvou minha companheira.\p",
            r"Nao vou esquecer disso, {PLAYER}.\n",
            r"Se precisar cruzar o mar, me procure.\p",
            r"Vamos para casa.$",
        ),
    },
}

FORBIDDEN = (
    "PEEKO",
    "MR. BRINEY",
    "DEVON",
    "RUSTBORO",
    "RUSTURF",
)


def marker_for(text: str, label: str) -> str:
    for suffix in ("::\n", ":\n"):
        marker = label + suffix
        if marker in text:
            return marker
    raise RuntimeError(f"Missing Galerias rescue block: {label}")


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


def validate_file(text: str, targets: dict[str, tuple[str, ...]]) -> list[str]:
    failures: list[str] = []
    for label, lines in targets.items():
        start, end, marker = bounds(text, label)
        block = text[start:end]
        if block != render(marker, lines):
            failures.append(f"{label} differs from canonical Galerias text")
        for token in FORBIDDEN:
            if token in block:
                failures.append(f"{label} still exposes Emerald token: {token}")
    return failures


def apply() -> int:
    changed_total = 0
    verified_total = 0
    for relpath, targets in TARGETS.items():
        path = ROOT / relpath
        text = path.read_text(encoding="utf-8")
        changed = 0
        for label, lines in targets.items():
            start, end, marker = bounds(text, label)
            replacement = render(marker, lines)
            if text[start:end] != replacement:
                text = text[:start] + replacement + text[end:]
                changed += 1
        failures = validate_file(text, targets)
        if failures:
            raise RuntimeError("; ".join(failures))
        path.write_text(text, encoding="utf-8")
        changed_total += changed
        verified_total += len(targets)
        print(f"{relpath}: {changed} changed; {len(targets)} verified.")
    print(f"Galerias rescue cleanup: {changed_total} changed; {verified_total} verified.")
    return 0


def check() -> int:
    failures: list[str] = []
    total = 0
    for relpath, targets in TARGETS.items():
        path = ROOT / relpath
        failures.extend(
            f"{relpath}: {failure}"
            for failure in validate_file(path.read_text(encoding="utf-8"), targets)
        )
        total += len(targets)
    if failures:
        print("Galerias rescue cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Galerias rescue cleanup check PASS: {total} visible blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
