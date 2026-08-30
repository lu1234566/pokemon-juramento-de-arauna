#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARBOR = ROOT / "data" / "maps" / "SlateportCity_Harbor" / "scripts.inc"
STRINGS = ROOT / "src" / "strings.c"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "SlateportCity_Harbor_Text_FerryServiceUnavailable": (("ferry service",), (
        "ATENDENTE: Procura um barco?\\p",
        "Desculpe, o BARCO DE LINHA ainda\\n",
        "nao esta em operacao.$",
    )),
    "SlateportCity_Harbor_Text_MayISeeYourTicket": (("CIRO:", "DESENCANTO"), (
        "ATENDENTE: Posso ver seu BILHETE?$",
    )),
    "SlateportCity_Harbor_Text_YouMustHaveTicket": (("TICKET", "board"), (
        "ATENDENTE: Voce precisa de um\\n",
        "BILHETE para embarcar.$",
    )),
    "SlateportCity_Harbor_Text_FlashedTicketWhereTo": (("flashed the TICKET", "where"), (
        "{PLAYER} mostrou o BILHETE.\\p",
        "ATENDENTE: Perfeito.\\n",
        "Para onde deseja ir?$",
    )),
    "SlateportCity_Harbor_Text_SailAnotherTime": (("another time",), (
        "ATENDENTE: Volte quando quiser\\n",
        "viajar.$",
    )),
    "SlateportCity_Harbor_Text_LilycoveItIs": (("BAIA DAS LUZES",), (
        "ATENDENTE: BAIA DAS LUZES, certo?$",
    )),
    "SlateportCity_Harbor_Text_BattleFrontierItIs": (("BATTLE FRONTIER",), (
        "ATENDENTE: CIRCUITO DE BATALHA,\\n",
        "certo?$",
    )),
    "SlateportCity_Harbor_Text_PleaseBoardFerry": (("board the ferry",), (
        "ATENDENTE: Embarque no BARCO DE\\n",
        "LINHA e aguarde a partida.$",
    )),
    "SlateportCity_Harbor_Text_WhereWouldYouLikeToGo": (("where would you like",), (
        "ATENDENTE: Para onde deseja ir?$",
    )),
    "SlateportCity_Harbor_Text_LoveToGoDeepUnderwaterSomeday": (("bottom of the sea", "underwater"), (
        "MARINHEIRO: Viajar ate o fundo\\n",
        "do mar deve ser incrivel.\\p",
        "Um dia ainda quero descer num\\n",
        "submersivel de pesquisa.$",
    )),
    "SlateportCity_Harbor_Text_AbnormalWeather": (("sensores detectam", "DESENCANTO"), (
        "MARINHEIRO: O clima no mar anda\\n",
        "estranho em alguns pontos.\\p",
        "Correntes mudam sem aviso. Quem\\n",
        "navega precisa redobrar cuidado.$",
    )),
    "SlateportCity_Harbor_Text_SubTooSmallForMe": (("CAPT. STERN", "sub's too small"), (
        "HOMEM: Queria acompanhar o\\n",
        "ENGENHEIRO na expedicao.\\p",
        "Mas o submersivel e pequeno.\\n",
        "Comigo dentro, faltaria espaco.$",
    )),
    "SlateportCity_Harbor_Text_WontBeLongBeforeWeFinishFerry": (("MR. BRINEY", "SHIPYARD", "ferry"), (
        "ENGENHEIRO: O VETERANO esta\\n",
        "ajudando no ESTALEIRO.\\p",
        "O BARCO DE LINHA deve ficar\\n",
        "pronto em breve.$",
    )),
    "SlateportCity_Harbor_Text_FinishedMakingFerry": (("S.S. TIDAL", "MR. BRINEY"), (
        "ENGENHEIRO: {PLAYER}, ficou\\n",
        "pronto!\\p",
        "O BARCO DE LINHA finalmente pode\\n",
        "navegar.\\p",
        "A experiencia do VETERANO fez\\n",
        "toda a diferenca.\\p",
        "Quando quiser, faca uma viagem.$",
    )),
    "SlateportCity_Harbor_Text_WouldYouTradeScanner": (("SCANNER", "DEEPSEATOOTH", "DEEPSEASCALE"), (
        "ENGENHEIRO: Isso e um SCANNER!\\p",
        "Seria muito util nas expedicoes.\\p",
        "Quer troca-lo por um\\n",
        "DEEPSEATOOTH ou DEEPSEASCALE?$",
    )),
    "SlateportCity_Harbor_Text_IfYouWantToTradeLetMeKnow": (("useless to you", "SCANNER"), (
        "ENGENHEIRO: Tudo bem.\\p",
        "Se decidir trocar o SCANNER,\\n",
        "fale comigo.$",
    )),
    "SlateportCity_Harbor_Text_TradeForDeepSeaTooth": (("DEEPSEATOOTH",), (
        "ENGENHEIRO: Trocar pelo\\n",
        "DEEPSEATOOTH?$",
    )),
    "SlateportCity_Harbor_Text_TradeForDeepSeaScale": (("DEEPSEASCALE",), (
        "ENGENHEIRO: Trocar pela\\n",
        "DEEPSEASCALE?$",
    )),
    "SlateportCity_Harbor_Text_WhichOneDoYouWant": (("Which one",), (
        "ENGENHEIRO: Qual dos dois quer?$",
    )),
    "SlateportCity_Harbor_Text_HandedScannerToStern": (("SCANNER", "CAPT. STERN"), (
        "{PLAYER} entregou o SCANNER ao\\n",
        "ENGENHEIRO.$",
    )),
    "SlateportCity_Harbor_Text_ThisWillHelpResearch": (("help our research",), (
        "ENGENHEIRO: Obrigado, {PLAYER}!\\p",
        "Isto vai ajudar muito nossa\\n",
        "pesquisa.$",
    )),
}

STRING_REPLACEMENTS = {
    'const u8 gText_LilycoveCity[] = _("BAIA DAS LUZES");':
        'const u8 gText_LilycoveCity[] = _("BAIA DAS LUZES");',
    'const u8 gText_SlateportCity[] = _("PORTO DO SAL");':
        'const u8 gText_SlateportCity[] = _("PORTO DO SAL");',
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("PLAYER", payload).replace("$", "")
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths() -> None:
    for label, (_, payloads) in TARGETS.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(f"{label}: {len(segment)} visible chars: {segment!r}")


def render_harbor(source: str) -> str:
    validate_widths()
    rendered = source
    for label, (markers, payloads) in TARGETS.items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one block, found {len(matches)}")
        body = matches[0].group("body")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: source marker missing: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]

    def mask(text: str) -> str:
        masked = text
        for label in TARGETS:
            match = block_pattern(label).search(masked)
            if not match:
                raise ValueError(f"{label}: cannot mask missing block")
            start, end = match.span("body")
            masked = masked[:start] + '\t.string "<ARAUNA_RENDERED_BLOCK>"\n\n' + masked[end:]
        return masked

    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering Porto do Sal harbor service")
    for token in ("CAPT. STERN", "MR. BRINEY", "S.S. TIDAL", "LILYCOVE CITY", "ferry service"):
        for label in TARGETS:
            if token in block_pattern(label).search(rendered).group("body"):
                raise ValueError(f"{label}: stale harbor token survived: {token}")
    return rendered


def render_strings(source: str) -> str:
    rendered = source
    for old, new in STRING_REPLACEMENTS.items():
        count = rendered.count(old)
        if count != 1:
            raise ValueError(f"expected one city-name UI anchor, found {count}: {old}")
        rendered = rendered.replace(old, new, 1)
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Porto do Sal harbor, ferry, scanner and destination surface.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    harbor = render_harbor(HARBOR.read_text(encoding="utf-8"))
    strings = render_strings(STRINGS.read_text(encoding="utf-8"))
    if args.check:
        print(f"Porto do Sal harbor renderer OK: {len(TARGETS)} dialogue blocks + 2 city menu literals validated.")
        return 0
    if args.in_place:
        HARBOR.write_text(harbor, encoding="utf-8")
        STRINGS.write_text(strings, encoding="utf-8")
        return 0
    print(harbor, end="" if harbor.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
