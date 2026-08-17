#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import apply_arauna_story as base


TERM_REPLACEMENTS = {
    "PROF. BIRCH": "PROF. ANAHI",
    "PROFESSOR BIRCH": "PROFESSORA ANAHI",
    "PROF BIRCH": "PROF ANAHI",
    "TEAM AQUA": "CONSORCIO HORIZONTE",
    "TEAM MAGMA": "LEMBRANTES",
    "AQUA HIDEOUT": "ARQUIVO CENTRAL",
    "MAGMA HIDEOUT": "BASE DOS LEMBRANTES",
    "ARCHIE": "OTACILIO",
    "MAXIE": "LUZIA",
    "HOENN": "ARAUNA",
    "DEVON CORP.": "CONSORCIO HORIZONTE",
    "DEVON CORP": "CONSORCIO HORIZONTE",
}

LAB_EXACT = {
    "likeyoutohavepokemon": "ANAHI: Esse POKéMON escolheu ficar ao seu lado. Nao trate isso como propriedade. Um VINCULO so existe enquanto os dois lados continuam escolhendo.",
    "whynotgivenicknametomon": "ANAHI: Um nome pode virar memoria. Quer dar um nome a {STR_VAR_1}?",
    "mightbegoodideatogoseerival": "ANAHI: CIRO esta fazendo observacoes na ROTA 103. Ele recebeu apoio do HORIZONTE e acha que isso prova que ja entendeu o mundo. Va encontra-lo.",
    "getrivaltoteachyou": "ANAHI: Encontre CIRO na ROTA 103. Prestem atencao ao modo como seus POKéMON reagem um ao outro.",
    "dontbethatway": "ANAHI: Voce nao precisa gostar de CIRO. Mas precisa ouvir o que ele escolheu acreditar antes de decidir no que voce acredita.",
    "birchrivalgonehome": "ANAHI: CIRO saiu de novo. Desde que o HORIZONTE ofereceu uma bolsa, ele quase nao para em casa.",
    "heardyoubeatrivaltakepokedex": "ANAHI: CIRO contou sobre a batalha. Mais importante que vencer: seu POKéMON reagiu ao VINCULO de um jeito que meus sensores nao previram. Leve esta POKéDEX e registre o que encontrar.",
    "receivedpokedex": "{PLAYER} recebeu a POKéDEX!",
    "explainpokedex": "ANAHI: A POKéDEX registra especies e encontros. Eu quero outra coisa tambem: anote falhas de memoria, mudancas de comportamento e qualquer sinal de DESENCANTO.",
    "countlesspokemonawait": "ANAHI: Nao transforme a viagem numa coleta de numeros. Observe quem lembra, quem esquece e quem esta decidindo isso por eles.",
    "maygotpokedextootakethese": "CIRO: Entao ela te entregou uma POKéDEX tambem. Certo. Pegue estas POKé BOLAS. Quero ver quanto tempo voce leva para me alcancar.",
    "brendangotpokedextootakethese": "CIRO: Entao ela te entregou uma POKéDEX tambem. Certo. Pegue estas POKé BOLAS. Quero ver quanto tempo voce leva para me alcancar.",
    "catchcutepokemonwithpokeballs": "CIRO: Eu vou seguir os pontos marcados pelo HORIZONTE. Dizem que la fora existem POKéMON que quase nao sofrem DESENCANTO.",
    "catchcoolpokemonwithpokeballs": "CIRO: Eu vou seguir os pontos marcados pelo HORIZONTE. Dizem que la fora existem POKéMON que quase nao sofrem DESENCANTO.",
    "maywhereshouldigonext": "CIRO: O HORIZONTE tem equipes por toda Arauna. Se os dados deles estiverem certos, eu vou chegar antes de voce.",
    "brendanwhereshouldigonext": "CIRO: O HORIZONTE tem equipes por toda Arauna. Se os dados deles estiverem certos, eu vou chegar antes de voce.",
    "ohyourbagsfull": "Sua BOLSA esta cheia.",
    "heyyourbagsfull": "Sua BOLSA esta cheia.",
    "seriouslookingmachine": "Um sensor de VINCULO ocupa quase toda a bancada. Ha marcas de uso muito anteriores ao projeto atual do HORIZONTE.",
    "pcusedforresearch": "O PC contem dados de campo sobre POKéMON que deixaram de reconhecer lugares e pessoas familiares.",
    "crammedwithbooksonpokemon": "Cadernos de campo dividem a estante com livros sobre memoria, luto e comportamento POKéMON.",
    "booktoohardtoread": "As anotacoes misturam neurologia POKéMON, teoria de VINCULOS e muitas correcoes feitas a mao.",
}

DIRECTIONAL_EXACT = {
    "ourbossissnatchingsomething": "HORIZONTE: O diretor saiu para buscar um componente essencial do ARQUIVO VIVO. Nao espere que eu diga onde.",
    "wheremightmagmahideoutbe": "HORIZONTE: Os LEMBRANTES montaram uma base perto da SERRA DA CINZA. Luzia quer chegar aos registros antes de nos.",
    "bosswenttojackasubmarine": "HORIZONTE: OTACILIO foi ao PORTO DO SAL. O submersivel consegue chegar as cavernas de M'BOI.",
    "bossisonroute122": "HORIZONTE: OTACILIO seguiu para o MEMORIAL DOS NOMES, na ROTA 122. Ele quer os registros guardados la.",
    "teammagmaatmtchimney": "HORIZONTE: Os LEMBRANTES estao na SERRA DA CINZA. Dizem que LUZIA pretende devolver memorias extraidas a forca.",
    "bossisinslateportcity": "HORIZONTE: OTACILIO esta no PORTO DO SAL. A demonstracao publica do ARQUIVO VIVO comeca la.",
}

SYSTEM_HINTS = (
    "received", "obtain", "nickname", "bag", "roomfor", "machine", "pcused",
    "book", "item", "pokeball", "pokéball", "pokeballs", "tm", "hm", "badge",
    "heal", "mart", "register", "storage", "trade", "cable", "lottery", "contest",
    "berry", "rod", "bike", "pokedexupgraded", "nationaldex", "movelearner",
)

CIRO_LINES = [
    "CIRO: O HORIZONTE nao me pediu para esquecer nada. So me mostrou que existe um futuro que nao precisa ser governado pelo passado.",
    "CIRO: Voce continua olhando para cada cicatriz como se ela fosse uma resposta. Eu quero saber o que existe depois dela.",
    "CIRO: Se os dados estiverem certos, o DESENCANTO pode ser tratado. Eu prefiro testar uma resposta a transformar sofrimento em tradicao.",
    "CIRO: Nao confunda minha pressa com falta de memoria. Eu lembro o bastante para saber que nao quero viver preso ao que perdi.",
]

ANAHI_LINES = [
    "ANAHI: Eu ajudei a criar os primeiros sensores de VINCULO. Na epoca achei que medir significava compreender. Hoje sei que nao e a mesma coisa.",
    "ANAHI: O DESENCANTO nao apaga apenas fatos. Ele rompe caminhos entre pessoas, lugares e POKéMON. E esses caminhos nao pertencem a uma empresa.",
    "ANAHI: Se eu continuar calada sobre o que o HORIZONTE fez com minha pesquisa, o erro tambem sera meu.",
]

VAL_LINES = [
    "VAL: Eu ainda tenho medo. Mas agora sei que coragem nao e esquecer o medo; e caminhar mesmo lembrando dele.",
    "VAL: Passei muito tempo achando que precisava virar outra pessoa para seguir viagem. Eu so precisava descobrir meu proprio ritmo.",
]

ELIAS_LINES = [
    "ELIAS: Algumas culpas nao desaparecem quando ficamos em silencio. Eu aprovei parte do projeto de M'BOI e passei anos chamando meu medo de prudencia.",
    "ELIAS: Ser seu pai nunca me deu o direito de escolher que verdade voce podia suportar. Demorei demais para entender isso.",
]

OTACILIO_LINES = [
    "OTACILIO: Eu vi o que uma memoria pode fazer com quem sobrevive. O ARQUIVO VIVO existe para que ninguem seja condenado a carregar a pior noite da propria vida para sempre.",
    "OTACILIO: Preservar tudo nao e compaixao. As vezes e apenas obrigar uma ferida a continuar aberta e chamar isso de respeito.",
    "OTACILIO: M'BOI me ensinou que lembrar tambem pode destruir. Eu me recuso a aceitar que sofrimento seja sagrado so porque aconteceu.",
]

LUZIA_LINES = [
    "LUZIA: Ninguem tem o direito de escolher que memoria merece morrer. O HORIZONTE chama censura de tratamento porque a palavra soa mais limpa.",
    "LUZIA: Se devolver as memorias doer, entao vai doer. Dor nao autoriza ninguem a reescrever a vida de outra pessoa.",
    "LUZIA: O problema nunca foi lembrar demais. Foi deixar quem tem poder decidir quais lembrancas os outros podem conservar.",
]

HORIZONTE_LINES = [
    "HORIZONTE: O ARQUIVO VIVO nao apaga pessoas. Ele separa trauma de identidade. Pelo menos e isso que nos ensinaram.",
    "HORIZONTE: Os sensores detectam VINCULOS instaveis antes do DESENCANTO completo. Isso pode salvar familias inteiras.",
    "HORIZONTE: OTACILIO diz que memoria sem escolha e outra forma de prisao. Eu ainda estou tentando decidir se concordo.",
    "HORIZONTE: O projeto de M'BOI foi um desastre. O ARQUIVO atual existe justamente porque aprendemos com ele. E o que consta nos relatorios.",
    "HORIZONTE: Nao somos soldados. Somos tecnicos, guardas e pesquisadores. Isso nao torna todas as nossas ordens certas.",
]

LEMBRANTE_LINES = [
    "LEMBRANTE: Se uma historia incomoda quem manda, ela vira 'ruido', depois 'trauma', depois desaparece do registro.",
    "LEMBRANTE: LUZIA diz que memoria devolvida sem permissao ainda e melhor que memoria roubada. Nem todos aqui concordam com essa parte.",
    "LEMBRANTE: Guardar um nome pode ser resistencia. Obrigar alguem a reviver tudo tambem pode ser violencia.",
    "LEMBRANTE: O HORIZONTE quer uma Arauna estavel. Eu quero uma Arauna que saiba por que suas ruinas existem.",
]

MEMORIAL_LINES = [
    "Os nomes gravados aqui pertencem a mortos, desaparecidos e lugares que deixaram de existir nos mapas oficiais.",
    "Uma placa recente cobre marcas mais antigas. Alguem tentou organizar a memoria do lugar como se fosse um arquivo administrativo.",
    "DONA ZILA: Nome repetido nao ressuscita ninguem. Mas impede que o silencio finja que aquela pessoa nunca existiu.",
    "Um funcionario do HORIZONTE fotografa cada inscricao antes de autorizar a retirada de algumas placas.",
]

MBOI_LINES = [
    "Os sensores enlouquecem. As cavernas de M'BOI ainda carregam VINCULOS que o ARQUIVO nunca conseguiu classificar.",
    "Gravacoes antigas misturam ordens de evacuacao, pedidos de socorro e trechos que alguem marcou para exclusao.",
    "OTACILIO e LUZIA chegaram ao mesmo lugar por razoes opostas: um quer encerrar a dor; a outra quer devolver tudo. Nenhum perguntou a quem tera de viver com a escolha.",
    "O ARQUIVO reage como se memoria e esquecimento fossem forcas fisicas. Pela primeira vez fica claro que ele nunca esteve realmente sob controle humano.",
]

SOOTOPOLIS_LINES = [
    "As aguas carregam lembrancas que nao pertencem a quem as recebe. Pessoas reconhecem nomes que nunca ouviram e esquecem rostos que amam.",
    "IARA-MAE puxa VINCULOS de volta. ANHANGUERA encerra os que nao podem continuar. O colapso obrigou as duas correntes a se manifestar ao mesmo tempo.",
    "A cidade inteira sente o resultado de duas ideias transformadas em absolutos: lembrar tudo e apagar a dor a qualquer custo.",
]

SKY_LINES = [
    "O CADERNO DE ZILA guarda versoes contraditorias da mesma historia. Nenhuma pagina reivindica ser a unica verdadeira.",
    "O JURAMENTO nunca prometeu memoria perfeita. Prometeu que nenhuma pessoa escolheria sozinha o que todos os outros deveriam esquecer.",
    "Entre rasuras e paginas remendadas, o caderno prova que uma memoria pode mudar sem deixar de pertencer a quem a viveu.",
]

SPACE_LINES = [
    "A rede de comunicacao daqui pode espalhar o protocolo do ARQUIVO VIVO por toda Arauna. Por isso o HORIZONTE e os LEMBRANTES vieram ate aqui.",
    "Um sinal capaz de atravessar a regiao inteira tambem poderia sincronizar milhares de sensores de VINCULO ao mesmo tempo.",
    "Os engenheiros insistem que comunicacao nao e controle. Os cabos no andar superior sugerem que alguem pretende testar essa diferenca.",
]

WEATHER_LINES = [
    "Os dados mostram picos de DESENCANTO perto de instalacoes que usam sensores de VINCULO em grande escala.",
    "Os pesquisadores cruzaram chuva, temperatura e relatos de perda de memoria. O clima nao explica o padrao; a infraestrutura do ARQUIVO explica melhor.",
    "O HORIZONTE veio buscar os servidores. Os dados daqui contradizem a versao oficial sobre a seguranca do ARQUIVO VIVO.",
]


def choose(lines: list[str], label: str) -> str:
    digest = int(hashlib.sha1(label.encode("utf-8")).hexdigest()[:8], 16)
    return lines[digest % len(lines)]


def suffix_of(label: str) -> str:
    return label.split("_Text_", 1)[1].lower() if "_Text_" in label else label.lower()


def safe_escape_asm(text: str) -> str:
    """Keep Emerald text controls intact and remove technical underscores from generated prose."""
    return text.replace("_", " ").replace('"', '\\"')


def safe_term_replacements(text: str) -> str:
    for old, new in TERM_REPLACEMENTS.items():
        text = text.replace(old, new)
    return text


def semantic_story_message(label: str, old_body: str, map_name: str) -> str | None:
    suffix = suffix_of(label)
    old = base.normalize_old(old_body)
    old_low = old.lower()
    location, context = base.context_for(map_name)

    # Exact early-game beats come first so progression prompts keep their meaning.
    if map_name.startswith("LittlerootTown_ProfessorBirchsLab") and suffix in LAB_EXACT:
        return LAB_EXACT[suffix]
    if suffix in DIRECTIONAL_EXACT:
        return DIRECTIONAL_EXACT[suffix]

    # Signs carry Arauna's place identity, but ordinary object/system text is preserved.
    if "townsign" in suffix or "citysign" in suffix or suffix == "sign":
        return f"{location}. {context}"

    if any(token in suffix for token in SYSTEM_HINTS):
        return None

    # Legendary climax: reinterpret the same Emerald triggers without changing them.
    legendary = any(k in suffix or k in old_low for k in ("groudon", "kyogre", "rayquaza", "orb"))
    if legendary:
        if map_name.startswith("SkyPillar"):
            return choose(SKY_LINES, label)
        if map_name.startswith("Sootopolis"):
            return choose(SOOTOPOLIS_LINES, label)
        if map_name.startswith("SeafloorCavern"):
            return choose(MBOI_LINES, label)
        return "Os sensores registram duas correntes antigas sob Arauna: uma conserva VINCULOS; a outra permite que eles terminem. O ARQUIVO tentou transformar ambas em ferramentas."

    # Speaker detection uses the actual text-label suffix / original speaker, never the map filename.
    if suffix.startswith(("may", "brendan", "rival")) or "may:" in old_low or "brendan:" in old_low:
        return choose(CIRO_LINES, label)
    if "birch" in suffix or "prof. birch:" in old_low or "professor birch:" in old_low:
        return choose(ANAHI_LINES, label)
    if "wally" in suffix or "wally:" in old_low:
        return choose(VAL_LINES, label)
    if "norman" in suffix or "norman:" in old_low:
        return choose(ELIAS_LINES, label)
    if "archie" in suffix or "archie:" in old_low:
        return choose(OTACILIO_LINES, label)
    if "maxie" in suffix or "maxie:" in old_low:
        return choose(LUZIA_LINES, label)

    # Gym/story figures retain their roles but gain Arauna identities.
    leader_lines = {
        "roxanne": "DALVA: Pedra guarda marcas. Algumas rachaduras contam mais que monumentos inteiros.",
        "brawly": "ADEMAR: O mar devolve coisas quando quer. Homem nenhum manda na memoria da agua.",
        "wattson": "OLIVIA: Energia move uma cidade. Isso nao significa que toda fonte de energia deva ser aceita.",
        "flannery": "NARA: Cinza e o que sobra depois do fogo. Nao e o fim de tudo; tambem nao devemos fingir que nada queimou.",
        "winona": "LIDIA: Quando os POKéMON esquecem caminhos transmitidos entre geracoes, alguma coisa antiga foi ferida.",
        "tate": "CECILIA: Do alto, cidades parecem pequenas. As vidas dentro delas nunca sao.",
        "liza": "CAETANO: Um sinal pode atravessar o ceu. Isso nao lhe da o direito de atravessar a mente de alguem.",
        "steven": "SEU BENTO: Quando um nome some da boca das pessoas, eu escrevo. Nao para substituir quem lembra; para deixar uma pista.",
        "wallace": "AMALIA: Arauna sobreviveu a verdade pela metade por tempo demais. A Liga tambem tem dividas com quem foi apagado.",
        "juan": "DONA CELINA: Viver e aprender o que guardar e o que deixar seguir. Escolher isso pelo outro e que nao cabe a nos.",
    }
    for key, line in leader_lines.items():
        if key in suffix or f"{key}:" in old_low:
            return line

    # Major plot locations get varied, contextual dialogue only for plot-related blocks.
    plot_old = any(k in old_low for k in (
        "team aqua", "team magma", "archie", "maxie", "submarine", "mt. pyre",
        "weather institute", "space center", "devon", "hideout", "orb",
    ))
    plot_suffix = any(k in suffix for k in (
        "grunt", "admin", "aqua", "magma", "team", "boss", "submarine", "hideout",
        "mtpyre", "spacecenter", "weather", "steal", "attack",
    ))

    if map_name.startswith("MtPyre_Summit") and (plot_old or plot_suffix):
        return choose(MEMORIAL_LINES, label)
    if map_name.startswith("SeafloorCavern") and (plot_old or plot_suffix):
        return choose(MBOI_LINES, label)
    if map_name.startswith("AquaHideout") and (plot_old or plot_suffix):
        return choose(HORIZONTE_LINES, label)
    if map_name.startswith("MagmaHideout") and (plot_old or plot_suffix):
        return choose(LEMBRANTE_LINES, label)
    if map_name.startswith("MossdeepCity_SpaceCenter") and (plot_old or plot_suffix):
        return choose(SPACE_LINES, label)
    if map_name.startswith("Route119_WeatherInstitute") and (plot_old or plot_suffix):
        return choose(WEATHER_LINES, label)
    if map_name.startswith("SootopolisCity") and (plot_old or plot_suffix):
        return choose(SOOTOPOLIS_LINES, label)
    if map_name.startswith("SkyPillar") and (plot_old or plot_suffix):
        return choose(SKY_LINES, label)
    if (map_name.startswith("SlateportCity") or map_name.startswith("MtChimney")) and (plot_old or plot_suffix):
        if "team magma" in old_low or "maxie" in old_low or "magma" in suffix:
            return choose(LEMBRANTE_LINES, label)
        return choose(HORIZONTE_LINES, label)

    # Plot references elsewhere are renamed safely, but their original functional/directional wording is retained.
    return None


def safe_process_script(path: Path) -> tuple[int, int]:
    map_name = path.parent.name
    if not map_name.startswith(base.TARGET_PREFIXES):
        return 0, 0

    original = path.read_text(encoding="utf-8")
    changed_blocks = 0
    total_blocks = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal changed_blocks, total_blocks
        total_blocks += 1
        label = match.group("label")
        body = match.group("body")
        msg = base.story_message(label, body, map_name)

        if msg is None:
            body2 = base.apply_term_replacements(body)
            if body2 != body:
                changed_blocks += 1
            return f"{label}:\n{body2}"

        changed_blocks += 1
        return f"{label}:\n{base.emit_message(msg)}"

    replaced = base.TEXT_BLOCK_RE.sub(repl, original)

    marker = "\t.string \"<ARAUANA_TEXT_BLOCK>\"\n"
    before_structure = base.TEXT_BLOCK_RE.sub(lambda m: f"{m.group('label')}:\n{marker}", original)
    after_structure = base.TEXT_BLOCK_RE.sub(lambda m: f"{m.group('label')}:\n{marker}", replaced)
    if before_structure != after_structure:
        raise RuntimeError(f"Non-dialogue script structure changed: {path}")

    if replaced != original:
        path.write_text(replaced, encoding="utf-8")
    return changed_blocks, total_blocks


def main() -> None:
    base.escape_asm = safe_escape_asm
    base.apply_term_replacements = safe_term_replacements
    base.story_message = semantic_story_message
    base.process_script = safe_process_script
    base.main()


if __name__ == "__main__":
    main()
