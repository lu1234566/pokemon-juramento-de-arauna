#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/text/match_call.inc"
MAX_VISIBLE = 32

TARGETS = {
    "MatchCall_PersonalizedText25": (
        r"Oi, {PLAYER}. Aqui e {STR_VAR_1}.\p",
        r"DALVA chamou minha atencao\n",
        r"na aula hoje.\p",
        r"Ela explica onde eu errei.\n",
        r"Assim fica mais facil aprender.$",
    ),
    "MatchCall_PersonalizedText26": (
        r"Aqui e {STR_VAR_1}!\p",
        r"DALVA treinou comigo ontem.\p",
        r"Eu perdi feio, mas aprendi\n",
        r"mais do que esperava.$",
    ),
    "MatchCall_PersonalizedText59": (
        r"Aqui e {STR_VAR_1}!\p",
        r"Treinei em PORTO DAS REDES.\p",
        r"ADEMAR esta ainda mais forte.\n",
        r"O mar nao facilita para ninguem.$",
    ),
    "MatchCall_Text_Roxanne_Preparing": (
        r"DALVA: Ola, {PLAYER}!\p",
        r"Estou treinando de novo.\p",
        r"Ainda preciso de um tempo.\n",
        r"Quando eu voltar, nos falamos.$",
    ),
    "MatchCall_Text_Roxanne_PreparingPostGame": (
        r"DALVA: Parabens, {PLAYER}!\p",
        r"Soube da sua conquista.\p",
        r"Eu ainda estou treinando.\n",
        r"Depois quero outra batalha.$",
    ),
    "MatchCall_Text_Roxanne_RematchReady": (
        r"DALVA: {PLAYER}, estou pronta!\p",
        r"Volte a SERRA DO UIVO.\n",
        r"Quero lutar com voce de novo.$",
    ),
    "MatchCall_Text_Roxanne_PostRematch": (
        r"DALVA: Nossa batalha deixou\n",
        r"mais uma marca na pedra.$",
    ),
    "MatchCall_Text_Brawly_Preparing": (
        r"ADEMAR: Ola, {PLAYER}!\p",
        r"O mar nao para de ensinar.\p",
        r"Estou treinando outra vez.\n",
        r"Quando der, volte por aqui.$",
    ),
    "MatchCall_Text_Brawly_PreparingPostGame": (
        r"ADEMAR: Parabens, {PLAYER}!\p",
        r"A noticia chegou pelo porto.\p",
        r"Ainda estou treinando.\n",
        r"Depois teremos outra luta.$",
    ),
    "MatchCall_Text_Brawly_RematchReady": (
        r"ADEMAR: O desafio voltou!\p",
        r"PORTO DAS REDES espera voce.\n",
        r"Venha quando quiser.$",
    ),
    "MatchCall_Text_Brawly_PostRematch": (
        r"ADEMAR: Uma boa batalha\n",
        r"sempre deixa nova corrente.$",
    ),
    "MatchCall_Text_Wattson_Preparing": (
        r"OLIVIA: Ola, {PLAYER}.\p",
        r"Estou recalibrando a rede.\p",
        r"Ainda preciso de um tempo.\n",
        r"Depois teremos outra luta.$",
    ),
    "MatchCall_Text_Wattson_PreparingPostGame": (
        r"OLIVIA: Parabens, {PLAYER}!\p",
        r"Soube do que voce conquistou.\p",
        r"Estou revendo meus circuitos.\n",
        r"Depois quero testar voce.$",
    ),
    "MatchCall_Text_Wattson_RematchReady": (
        r"OLIVIA: A rede esta pronta!\p",
        r"Volte a ENCRUZILHADA.\n",
        r"Quero testar voce outra vez.$",
    ),
    "MatchCall_Text_Wattson_PostRematch": (
        r"OLIVIA: Nossa batalha ainda\n",
        r"faz a rede parecer pequena.$",
    ),
    "MatchCall_Text_Flannery_Preparing": (
        r"NARA: {PLAYER}, ainda treino.\p",
        r"Cinza tambem guarda calor.\p",
        r"Quando o desafio reabrir,\n",
        r"quero enfrentar voce de novo.$",
    ),
    "MatchCall_Text_Flannery_PreparingPostGame": (
        r"NARA: Parabens, {PLAYER}!\p",
        r"A noticia chegou ate aqui.\p",
        r"Eu ainda tenho o que aprender.\n",
        r"Depois quero outra batalha.$",
    ),
    "MatchCall_Text_Flannery_RematchReady": (
        r"NARA: Estamos prontos!\p",
        r"Volte a SERTAO DE DENTRO.\n",
        r"O fogo ainda esta aceso.$",
    ),
    "MatchCall_Text_Flannery_PostRematch": (
        r"NARA: Cada batalha deixa\n",
        r"uma cinza diferente.$",
    ),
    "MatchCall_Text_Winona_Preparing": (
        r"LIDIA: Ola, {PLAYER}!\p",
        r"Estou refazendo meus caminhos.\p",
        r"Quando o desafio reabrir,\n",
        r"nao vou repetir os mesmos erros.$",
    ),
    "MatchCall_Text_Winona_PreparingPostGame": (
        r"LIDIA: Parabens, {PLAYER}!\p",
        r"A noticia chegou pela mata.\p",
        r"Eu continuo treinando.\n",
        r"Depois quero outra batalha.$",
    ),
    "MatchCall_Text_Winona_RematchReady": (
        r"LIDIA: O desafio reabriu!\p",
        r"Volte a MATA DO MEIO.\n",
        r"Estarei esperando voce.$",
    ),
    "MatchCall_Text_Winona_PostRematch": (
        r"LIDIA: Perder nao apaga\n",
        r"o caminho que aprendemos.$",
    ),
    "MatchCall_Text_TateLiza_Preparing": (
        r"CECILIA: {PLAYER}, estamos\n",
        r"treinando outra vez.\p",
        r"CAETANO: Quando reabrirmos,\n",
        r"queremos outra batalha.$",
    ),
    "MatchCall_Text_TateLiza_PreparingPostGame": (
        r"CECILIA: Parabens, {PLAYER}!\p",
        r"CAETANO: Soube da conquista.\p",
        r"CECILIA: Ainda treinamos.\n",
        r"CAETANO: Depois nos vemos.$",
    ),
    "MatchCall_Text_TateLiza_RematchReady": (
        r"CECILIA: Estamos prontos!\p",
        r"CAETANO: MISSOES DO CEU\n",
        r"espera voce.$",
    ),
    "MatchCall_Text_TateLiza_PostRematch": (
        r"CECILIA: A batalha mostrou\n",
        r"outra forma de olhar o ceu.\p",
        r"CAETANO: Vamos repetir um dia.$",
    ),
    "MatchCall_Text_Juan_Preparing": (
        r"DONA CELINA: Ola, {PLAYER}.\p",
        r"A agua segue ensinando.\p",
        r"AMALIA tambem deixou marcas\n",
        r"neste caminho.\p",
        r"Ainda preciso de um tempo.$",
    ),
    "MatchCall_Text_Juan_PreparingPostGame": (
        r"DONA CELINA: Parabens.\p",
        r"Voce chegou muito longe.\p",
        r"Eu continuo aprendendo aqui.\n",
        r"Depois teremos outra luta.$",
    ),
    "MatchCall_Text_Juan_RematchReady": (
        r"DONA CELINA: Reabrimos.\p",
        r"Volte a AGUAS DE M'BOI.\n",
        r"Estarei esperando voce.$",
    ),
    "MatchCall_Text_Juan_PostRematch": (
        r"DONA CELINA: Algumas lutas\n",
        r"continuam correndo na memoria.$",
    ),
}

FORBIDDEN = (
    "ROXANNE", "RUSTBORO", "BRAWLY", "DEWFORD", "WATTSON", "MAUVILLE",
    "FLANNERY", "LAVARIDGE", "WINONA", "FORTREE", "TATE", "LIZA",
    "MOSSDEEP", "JUAN", "SOOTOPOLIS", "WALLACE",
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
        expected = render(label, lines)
        if block != expected:
            failures.append(f"{label} does not match canonical Arauna Match Call text")
        for token in FORBIDDEN:
            if token in block:
                failures.append(f"{label} still contains Emerald identity: {token}")
        for raw in re.findall(r'\.string "(.*)"', block):
            for segment in re.split(r"\\[npl]", raw):
                visible = CONTROL_RE.sub("", segment).replace("$", "")
                if len(visible) > MAX_VISIBLE:
                    failures.append(f"{label} exceeds {MAX_VISIBLE} visible chars: {visible!r}")
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
    print(f"Gym leader Match Call cleanup: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Gym leader Match Call check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Gym leader Match Call PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
