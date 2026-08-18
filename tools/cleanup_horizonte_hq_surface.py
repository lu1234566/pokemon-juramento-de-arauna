#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS: dict[str, dict[str, tuple[str, ...]]] = {
    "data/maps/RustboroCity_DevonCorp_1F/scripts.inc": {
        "RustboroCity_DevonCorp_1F_Text_WelcomeToDevonCorp": (
            r"Bem-vindo ao CONSORCIO HORIZONTE.\p",
            r"Este centro tecnico da SERRA DO UIVO\n",
            r"desenvolve equipamentos de campo,\n",
            r"medicina e sistemas de VINCULO.$",
        ),
        "RustboroCity_DevonCorp_1F_Text_StaffGotRobbed": (
            r"Um dos nossos pesquisadores perdeu\n",
            r"um pacote importante durante o campo.\p",
            r"A seguranca esta tentando recuperar\n",
            r"o material antes que seja copiado.$",
        ),
        "RustboroCity_DevonCorp_1F_Text_ThoseShoesAreOurProduct": (
            r"Esses TENIS DE CORRIDA sao de uma\n",
            r"linha testada por nossas equipes.\p",
            r"E bom ver equipamento de campo\n",
            r"sendo usado de verdade.$",
        ),
        "RustboroCity_DevonCorp_1F_Text_RobberWasntVeryBright": (
            r"O pacote roubado e importante,\n",
            r"mas os dados sao cifrados.\p",
            r"Sem a chave do HORIZONTE,\n",
            r"quase tudo parece ruido.$",
        ),
        "RustboroCity_DevonCorp_1F_Text_SoundsLikeStolenGoodsRecovered": (
            r"Disseram que o material roubado\n",
            r"do HORIZONTE foi recuperado.\p",
            r"O andar de pesquisa voltou\n",
            r"a funcionar normalmente.$",
        ),
        "RustboroCity_DevonCorp_1F_Text_OnlyAuthorizedPeopleEnter": (
            r"Desculpe. Acesso aos laboratorios\n",
            r"somente com autorizacao.$",
        ),
        "RustboroCity_DevonCorp_1F_Text_HowCouldWeGetRobbed": (
            r"Ainda nao acredito que entraram\n",
            r"na nossa rota de transporte.\p",
            r"Alguem conhecia o percurso.$",
        ),
        "RustboroCity_DevonCorp_1F_Text_YoureAlwaysWelcomeHere": (
            r"Voce recuperou material do centro.\p",
            r"Depois disso, a recepcao recebeu\n",
            r"ordens para deixar voce entrar.$",
        ),
        "RustboroCity_DevonCorp_1F_Text_RocksMetalDisplay": (
            r"Amostras de rocha e metal ocupam\n",
            r"a vitrine. Ha uma placa:\p",
            r"O CONSORCIO HORIZONTE nasceu\n",
            r"de projetos de extracao na serra.\p",
            r"Com o tempo, passou a financiar\n",
            r"pesquisa, transporte e tecnologia.\p",
            r"Os primeiros sensores de VINCULO\n",
            r"tambem foram testados aqui.$",
        ),
        "RustboroCity_DevonCorp_1F_Text_ProductDisplay": (
            r"Prototipos ocupam a vitrine.\p",
            r"Ha POKéNAVS, POKé BOLAS e\n",
            r"sensores usados por equipes de campo.\p",
            r"Um compartimento vazio traz a placa:\n",
            r"ARQUIVO VIVO - acesso restrito.$",
        ),
    },
    "data/maps/RustboroCity_DevonCorp_2F/scripts.inc": {
        "RustboroCity_DevonCorp_2F_Text_DeviceForTalkingToPokemon": (
            r"Tentamos criar um aparelho capaz\n",
            r"de interpretar sinais de VINCULO.\p",
            r"Medir resposta e facil.\n",
            r"Entender o que ela significa, nao.$",
        ),
        "RustboroCity_DevonCorp_2F_Text_DevelopingNewBalls": (
            r"Estou testando novos tipos\n",
            r"de POKé BOLAS.\p",
            r"Ainda nao chegamos a um modelo\n",
            r"bom o bastante para campo.$",
        ),
        "RustboroCity_DevonCorp_2F_Text_WeFinallyMadeNewBalls": (
            r"Terminamos dois modelos novos!\p",
            r"A REPEAT BALL ajuda com especies\n",
            r"que voce ja registrou.\p",
            r"A TIMER BALL melhora conforme\n",
            r"a batalha se prolonga.\p",
            r"Ambas foram desenvolvidas\n",
            r"pelo CONSORCIO HORIZONTE.$",
        ),
        "RustboroCity_DevonCorp_2F_Text_IMadePokenav": (
            r"Eu trabalhei no POKéNAV.\p",
            r"A ideia era unir mapa, contatos\n",
            r"e dados de campo num aparelho so.$",
        ),
        "RustboroCity_DevonCorp_2F_Text_WowThatsAPokenav": (
            r"Esse e um POKéNAV recente!\p",
            r"A rede foi criada para cruzar\n",
            r"mapas e observacoes de campo.\p",
            r"Hoje o HORIZONTE usa a mesma base\n",
            r"para acompanhar sensores de VINCULO.$",
        ),
        "RustboroCity_DevonCorp_2F_Text_DeviceToVisualizePokemonDreams": (
            r"Estou tentando visualizar padroes\n",
            r"de memoria durante o sono POKéMON.\p",
            r"Os resultados mudam demais\n",
            r"para chamar isso de leitura.$",
        ),
        "RustboroCity_DevonCorp_2F_Text_DevelopDeviceToResurrectFossils": (
            r"Meu projeto reconstrui POKéMON\n",
            r"a partir de fosseis preservados.\p",
            r"Desta vez, ele realmente funciona.$",
        ),
        "RustboroCity_DevonCorp_2F_Text_WantToBringFossilBackToLife": (
            r"Espere... isso e um fossil?\p",
            r"Posso tentar reconstruir o POKéMON\n",
            r"com o REGENERADOR DE FOSSEIS.\p",
            r"Quer deixar o fossil comigo?$",
        ),
        "RustboroCity_DevonCorp_2F_Text_OhIsThatSo": (
            r"Tudo bem.\p",
            r"Se mudar de ideia, o equipamento\n",
            r"do HORIZONTE continua disponivel.$",
        ),
        "RustboroCity_DevonCorp_2F_Text_TwoFossilsPickOne": (
            r"Voce tem dois fosseis?\p",
            r"O regenerador so processa\n",
            r"uma amostra por vez.\p",
            r"Escolha qual quer reconstruir.$",
        ),
        "RustboroCity_DevonCorp_2F_Text_HandedFossilToResearcher": (
            r"{PLAYER} entregou {STR_VAR_1}\n",
            r"ao PESQUISADOR DO HORIZONTE.$",
        ),
        "RustboroCity_DevonCorp_2F_Text_FossilRegeneratorTakesTime": (
            r"O REGENERADOR DE FOSSEIS\n",
            r"precisa de algum tempo.\p",
            r"Volte depois de caminhar um pouco.$",
        ),
        "RustboroCity_DevonCorp_2F_Text_FossilizedMonBroughtBackToLife": (
            r"Pronto!\p",
            r"O POKéMON do fossil foi reconstruido.\p",
            r"A especie registrada e {STR_VAR_2}.$",
        ),
        "RustboroCity_DevonCorp_2F_Text_ReceivedMonFromResearcher": (
            r"{PLAYER} recebeu {STR_VAR_2}\n",
            r"do PESQUISADOR DO HORIZONTE.$",
        ),
        "RustboroCity_DevonCorp_2F_Text_DevelopNewPokenavFeature": (
            r"Estou criando uma nova funcao\n",
            r"para o POKéNAV.\p",
            r"Ela deveria comparar dados de campo,\n",
            r"mas ainda gera falsos positivos.$",
        ),
        "RustboroCity_DevonCorp_2F_Text_WhatToWorkOnNext": (
            r"Agora preciso escolher o proximo\n",
            r"projeto.\p",
            r"Aqui uma boa ideia recebe recursos\n",
            r"rapido. As vezes, rapido demais.$",
        ),
    },
    "data/maps/RustboroCity_DevonCorp_3F/scripts.inc": {
        "RustboroCity_DevonCorp_3F_Text_MrStoneIHaveFavor": (
            r"DR. OTACILIO: Sou OTACILIO MEIRA,\n",
            r"diretor do CONSORCIO HORIZONTE.\p",
            r"Soube que recuperou nosso material\n",
            r"mais de uma vez. Obrigado.\p",
            r"Preciso de outro favor.\p",
            r"Leve o pacote ao PORTO DO SAL.\n",
            r"A equipe de embarque o espera la.\p",
            r"No caminho, passe pelo PORTO DAS REDES\n",
            r"e entregue esta CARTA a SEU BENTO.$",
        ),
        "RustboroCity_DevonCorp_3F_Text_MrStoneWantYouToHaveThis": (
            r"OTACILIO: Nao gosto de pedir\n",
            r"trabalho sem oferecer ferramenta.\p",
            r"Leve este aparelho com voce.$",
        ),
        "RustboroCity_DevonCorp_3F_Text_MrStoneExplainPokenavRestUp": (
            r"OTACILIO: Este e um POKéNAV.\p",
            r"Ele mostra o mapa de ARAUNA,\n",
            r"registra contatos e dados de campo.\p",
            r"O PORTO DAS REDES e o PORTO DO SAL\n",
            r"ja estao marcados.\p",
            r"Os LEMBRANTES tambem procuram\n",
            r"parte do material que voce carrega.\p",
            r"Descanse antes de seguir viagem.$",
        ),
        "RustboroCity_DevonCorp_3F_Text_MrStoneGoWithCautionAndCare": (
            r"OTACILIO: Va com cuidado, {PLAYER}.\n",
            r"Dados perdidos nao voltam sozinhos.$",
        ),
        "RustboroCity_DevonCorp_3F_Text_CountingOnYou": (
            r"OTACILIO: Estou contando com voce.$",
        ),
        "RustboroCity_DevonCorp_3F_Text_ThankYouForDeliveringLetter": (
            r"OTACILIO: SEU BENTO recebeu a CARTA?\p",
            r"Otimo. Leve isto como pagamento\n",
            r"pelo trabalho de campo.$",
        ),
        "RustboroCity_DevonCorp_3F_Text_ExplainExpShare": (
            r"OTACILIO: Um POKéMON com EXP. SHARE\n",
            r"recebe parte da experiencia da batalha\n",
            r"mesmo sem entrar em campo.\p",
            r"Pode ajudar uma equipe desigual.$",
        ),
        "RustboroCity_DevonCorp_3F_Text_NotFamiliarWithTrends": (
            r"OTACILIO: Passei anos transformando\n",
            r"pesquisa em infraestrutura.\p",
            r"Ainda me surpreende como uma ideia\n",
            r"vira costume antes de ser compreendida.$",
        ),
        "RustboroCity_DevonCorp_3F_Text_ThisIs3rdFloorWaitHere": (
            r"Este e o terceiro andar do\n",
            r"CONSORCIO HORIZONTE.\p",
            r"A diretoria funciona aqui.\p",
            r"O pacote recuperado precisa seguir\n",
            r"para o PORTO DO SAL.\p",
            r"Espere um instante.$",
        ),
        "RustboroCity_DevonCorp_3F_Text_WordWithPresidentComeWithMe": (
            r"O DR. OTACILIO quer falar com voce.\p",
            r"Por favor, acompanhe-me.$",
        ),
        "RustboroCity_DevonCorp_3F_Text_PleaseGoAhead": (
            r"Pode entrar. Ele esta esperando.$",
        ),
        "RustboroCity_DevonCorp_3F_Text_VisitCaptSternShipyard": (
            r"No PORTO DO SAL, entregue o pacote\n",
            r"a equipe responsavel pelo embarque.$",
        ),
        "RustboroCity_DevonCorp_3F_Text_RepeatAndTimerHugelyPopular": (
            r"As REPEAT BALLS e TIMER BALLS\n",
            r"do HORIZONTE tiveram boa procura.\p",
            r"O laboratorio ja prepara outro lote.$",
        ),
        "RustboroCity_DevonCorp_3F_Text_RareRocksDisplay": (
            r"Uma colecao de rochas raras\n",
            r"ocupa a vitrine da diretoria.\p",
            r"Algumas vieram de M'BOI.$",
        ),
    },
}

FORBIDDEN = (
    "DEVON",
    "HORIZONTEORATION",
    "MR. STONE",
    "STEVEN",
    "SLATEPORT",
    "DEWFORD",
    "MAGMA",
    "AQUA",
    "CAPT. STERN",
)


def marker_for(text: str, label: str) -> str:
    for suffix in ("::\n", ":\n"):
        marker = label + suffix
        if marker in text:
            return marker
    raise RuntimeError(f"Missing Horizonte HQ block: {label}")


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
            failures.append(f"{label} differs from canonical Arauna HQ text")
        for token in FORBIDDEN:
            if token in block:
                failures.append(f"{label} still exposes Emerald identity token: {token}")
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
    print(f"Horizonte HQ cleanup: {changed_total} changed; {verified_total} verified.")
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
        print("Horizonte HQ cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Horizonte HQ cleanup check PASS: {total} visible blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
