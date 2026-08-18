#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "Route116" / "scripts.inc"
MAX_VISIBLE = 32

TARGETS = {
    "Route116_Text_ScoundrelMadeOffWithPeeko": (
        r"Meu PEEKO foi levado!\p",
        r"Estavamos caminhando quando um\n",
        r"sujeito estranho apareceu.\p",
        r"Ele fugiu com meu PEEKO!\n",
        r"PEEKO! Onde voce esta?$",
    ),
    "Route116_Text_WantToDigTunnel": (
        r"Eu ainda quero cavar o tunel!$",
    ),
    "Route116_Text_DiggingTunnelWhenGoonOrderedMeOut": (
        r"Eu cavava sem usar maquinas\n",
        r"quando um sujeito me expulsou.\p",
        r"Os POKéMON daqui reagem mal\n",
        r"a barulho forte.\p",
        r"Por isso paramos de usar\n",
        r"equipamento pesado.\p",
        r"Se ele fizer alguma loucura,\n",
        r"pode assustar todos eles.$",
    ),
    "Route116_Text_GoonHightailedItOutOfTunnel": (
        r"Ele saiu correndo do tunel!\p",
        r"Agora posso voltar a cavar.$",
    ),
    "Route116_Text_ThankYouTokenOfAppreciation": (
        r"Ah, e voce!\p",
        r"Voce recuperou nossa carga e\n",
        r"a levou ate o PORTO DO SAL.\p",
        r"Recebemos a confirmacao de que\n",
        r"ela chegou em seguranca.\p",
        r"Muito obrigado, {PLAYER}!\p",
        r"Nossa companhia desenvolveu\n",
        r"um novo tipo de POKé BALL.\p",
        r"Quero lhe dar uma como forma\n",
        r"de agradecimento.$",
    ),
    "Route116_Text_NewBallAvailableAtMart": (
        r"Essa nova POKé BALL agora esta\n",
        r"a venda em SERRA DO UIVO.\p",
        r"Espero que seja util!$",
    ),
    "Route116_Text_BagIsJamPacked": (
        r"Sua BOLSA esta cheia.\n",
        r"Nao consigo entregar a REPEAT BALL.$",
    ),
    "Route116_Text_TokenOfAppreciation": (
        r"Como agradecimento pela entrega,\n",
        r"tenho uma nova POKé BALL para voce.$",
    ),
    "Route116_Text_CanYouHelpMeFindGlasses": (
        r"Eu perdi meus oculos...\n",
        r"Pode me ajudar a encontrar?$",
    ),
    "Route116_Text_MayISeeThoseGlasses": (
        r"Achou uns oculos?\n",
        r"Posso dar uma olhada?$",
    ),
    "Route116_Text_NotWhatImLookingForMaybeTheyArentHere": (
        r"Hmm... Sao BLACKGLASSES.\p",
        r"Nao sao os oculos que procuro.\n",
        r"Talvez eles nem estejam aqui.$",
    ),
    "Route116_Text_CantFindGlassesNotHere": (
        r"Nao encontro meus oculos...\n",
        r"Talvez eles nem estejam aqui.$",
    ),
    "Route116_Text_NotWhatImLookingFor": (
        r"Hmm... Sao BLACKGLASSES.\p",
        r"Nao sao os oculos que procuro.$",
    ),
    "Route116_Text_RouteSignRustboro": (
        r"ROTA 116\n",
        r"{LEFT_ARROW} SERRA DO UIVO$",
    ),
    "Route116_Text_RusturfTunnelSign": (
        r"TUNEL DA ROTA 116\p",
        r"Liga SERRA DO UIVO ao\n",
        r"VALE DO SILENCIO.\p",
        r"Obras suspensas.$",
    ),
    "Route116_Text_TunnelersRestHouse": (
        r"ABRIGO DOS ESCAVADORES$",
    ),
    "Route116_Text_TrainerTipsBToStopEvolution": (
        r"DICA PARA TREINADORES\p",
        r"Para interromper uma evolucao,\n",
        r"aperte B durante o processo.\p",
        r"O POKéMON vai parar de evoluir.$",
    ),
    "Route116_Text_TrainerTipsBagHasPockets": (
        r"DICA PARA TREINADORES\p",
        r"Sua BOLSA possui varios bolsos.\p",
        r"Os itens que voce recebe vao\n",
        r"para o bolso adequado.$",
    ),
}

FORBIDDEN = (
    "PETALBURG WOODS",
    "SLATEPORT",
    "RUSTBORO",
    "VERDANTURF",
    "RUSTURF",
    "CAPT. STERN",
    "CIRO:",
    "TUNNELER'S REST HOUSE",
    "TRAINER TIPS",
    "Your BAG",
)

BLOCK_RE_TEMPLATE = r'(?m)^{label}:\n(?:\t\.string "[^\n]*"\n)+'
CONTROL_RE = re.compile(r"\\[npl]|\{[^}]+\}")


def block_re(label: str) -> re.Pattern[str]:
    return re.compile(BLOCK_RE_TEMPLATE.format(label=re.escape(label)))


def render(label: str, lines: tuple[str, ...]) -> str:
    return label + ":\n" + "".join(f'\t.string "{line}"\n' for line in lines)


def validate(text: str) -> list[str]:
    failures: list[str] = []
    for label, lines in TARGETS.items():
        match = block_re(label).search(text)
        if not match:
            failures.append(f"missing text block: {label}")
            continue
        block = match.group(0)
        if block != render(label, lines):
            failures.append(f"{label} does not match canonical Arauna text")
        for token in FORBIDDEN:
            if token.lower() in block.lower():
                failures.append(f"{label} still contains visible Emerald token: {token}")
        for raw in re.findall(r'\.string "(.*)"', block):
            for segment in re.split(r"\\[npl]", raw):
                visible = CONTROL_RE.sub("", segment).replace("$", "")
                if len(visible) > MAX_VISIBLE:
                    failures.append(
                        f"{label} exceeds {MAX_VISIBLE} visible chars: {visible!r}"
                    )
    return failures


def apply() -> int:
    text = TARGET.read_text(encoding="utf-8")
    changed = 0
    for label, lines in TARGETS.items():
        updated, count = block_re(label).subn(lambda _m: render(label, lines), text, count=1)
        if count != 1:
            raise RuntimeError(f"Could not uniquely replace {label} (matches={count})")
        if updated != text:
            changed += 1
        text = updated
    failures = validate(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    TARGET.write_text(text, encoding="utf-8")
    print(f"Route 116 visible cleanup: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Route 116 visible cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Route 116 visible cleanup PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
