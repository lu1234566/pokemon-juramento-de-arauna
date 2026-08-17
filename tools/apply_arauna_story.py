#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_ROOT = ROOT / "data" / "maps"

# Keep Emerald's control-flow/progression, but replace its narrative surface.
TARGET_PREFIXES = (
    "LittlerootTown", "OldaleTown", "Route101", "Route102", "Route103",
    "PetalburgCity", "Route104", "PetalburgWoods", "RustboroCity", "Route116",
    "RusturfTunnel", "DewfordTown", "GraniteCave", "Route109", "SlateportCity",
    "Route110", "MauvilleCity", "Route117", "VerdanturfTown", "Route111",
    "Route112", "FieryPath", "Route113", "FallarborTown", "Route114",
    "MeteorFalls", "MtChimney", "JaggedPass", "LavaridgeTown", "Route118",
    "Route119", "WeatherInstitute", "FortreeCity", "Route120", "Route121",
    "Route122", "MtPyre", "Route123", "LilycoveCity", "AquaHideout",
    "MagmaHideout", "Route124", "MossdeepCity", "ShoalCave", "Route125",
    "Route126", "Route127", "Route128", "SeafloorCavern", "SootopolisCity",
    "SkyPillar", "Route129", "Route130", "Route131", "PacifidlogTown",
    "EverGrandeCity", "VictoryRoad", "PokemonLeague",
)

LOCATION_CONTEXTS = [
    ("LittlerootTown", "VILA AMANHECER", "Aqui o Juramento ainda e contado de boca em boca. Dona Zila diz que um nome so morre quando ninguem mais o pronuncia."),
    ("OldaleTown", "VILA DA PASSAGEM", "Um Pokemon local deixou de responder ao proprio nome. Os moradores chamam o fenomeno de DESENCANTO."),
    ("PetalburgCity", "PAMPA DA ESPERA", "A cidade vive entre partidas e retornos. Elias conhece mais sobre o desastre de M'BOI do que aceita contar."),
    ("RustboroCity", "SERRA DO UIVO", "O CONSORCIO HORIZONTE trouxe emprego e obras. Tambem trouxe maquinas capazes de medir VINCULOS."),
    ("RusturfTunnel", "GALERIAS DA SERRA", "Equipamentos escondidos retiram vestigios de memoria de pessoas e Pokemon. Alguem esta testando o ARQUIVO VIVO."),
    ("DewfordTown", "PORTO DAS REDES", "Pescadores lembram de uma comunidade que os registros oficiais dizem nunca ter existido."),
    ("GraniteCave", "GRUTA DAS VOZES", "Seu Bento escreve nomes que os outros esqueceram. Para ele, papel nao substitui memoria; apenas impede o silencio."),
    ("SlateportCity", "PORTO DO SAL", "O ARQUIVO VIVO e apresentado como a cura do DESENCANTO. Os LEMBRANTES tentam impedir a demonstracao."),
    ("MauvilleCity", "ENCRUZILHADA CENTRAL", "A cidade prosperou com o HORIZONTE. Ciro agora veste o uniforme de quem promete construir o futuro."),
    ("VerdanturfTown", "VALE DO SILENCIO", "Familias deslocadas vivem aqui. Muitas lembram a perda, mas ja nao conseguem dizer o nome do lugar que perderam."),
    ("FallarborTown", "CAMPO DAS CINZAS", "O DESENCANTO avanca onde a terra ja foi ferida. Zila percebe que o padrao e mais antigo que o Consorcio."),
    ("MeteorFalls", "RUINAS DA QUEDA", "Os LEMBRANTES procuram uma memoria mineral de Arauna. Luzia acredita que nada deve ser esquecido, mesmo quando lembrar destrua quem restou."),
    ("MtChimney", "SERRA DA CINZA", "Luzia tenta devolver memorias extraidas a forca. O jogador descobre que preservar tudo tambem pode ser violencia."),
    ("LavaridgeTown", "SERTAO DE DENTRO", "Cinza, calor e abandono marcaram esta regiao. Aqui o luto nao e tratado como fraqueza."),
    ("WeatherInstitute", "INSTITUTO DAS AGUAS", "Dados climaticos provam que o DESENCANTO cresce ao redor das instalacoes do ARQUIVO VIVO."),
    ("FortreeCity", "MATA DO MEIO", "Pokemon selvagens esquecem rotas, cantos e habitos passados entre geracoes."),
    ("MtPyre", "MEMORIAL DOS NOMES", "Os nomes de mortos e desaparecidos sao mantidos aqui. O HORIZONTE comeca a retirar registros em nome da estabilidade."),
    ("LilycoveCity", "BAIA DAS LUZES", "Por tras da fachada moderna fica o centro de operacoes do ARQUIVO VIVO."),
    ("AquaHideout", "ARQUIVO CENTRAL", "O jogador encontra os arquivos de M'BOI: Anahi ajudou a criar os sensores, o pai de Ciro morreu no desastre e familias foram pagas para se calar."),
    ("MagmaHideout", "ARQUIVO CENTRAL", "O jogador encontra os arquivos de M'BOI: Anahi ajudou a criar os sensores, o pai de Ciro morreu no desastre e familias foram pagas para se calar."),
    ("MossdeepCity", "MISSOES DO CEU", "O HORIZONTE pretende usar a rede regional de comunicacao para ampliar o ARQUIVO VIVO."),
    ("SeafloorCavern", "CAVERNAS DE M'BOI", "Otacilio volta ao lugar onde perdeu a familia. Luzia chega para libertar tudo que foi armazenado. Os dois extremos colidem."),
    ("SootopolisCity", "AGUAS DE M'BOI", "O colapso do Arquivo espalha lembrancas alheias e vazios de memoria por toda Arauna."),
    ("SkyPillar", "TORRE DO JURAMENTO", "O Caderno de Zila guarda versoes contraditorias da regiao. Sua forca esta justamente em nao escolher uma unica verdade."),
    ("PacifidlogTown", "CASA DA FOGUEIRA", "Aqui historias sao repetidas para continuar vivas, nao para permanecer identicas."),
    ("EverGrandeCity", "ESTRADA DO JURAMENTO", "A Liga e o ultimo rito da viagem. Vencer nao apaga o que aconteceu; apenas define quem voce sera depois."),
    ("VictoryRoad", "ESTRADA DO JURAMENTO", "Val reaparece mais forte. Ele aprendeu a carregar o passado sem permitir que o passado escolha todos os seus passos."),
    ("PokemonLeague", "CASA MAIOR", "Amalia Serrano sabia que a versao oficial de M'BOI era incompleta. Agora ela precisa responder pelo silencio que ajudou a manter."),
]

GENERIC_ROUTE_CONTEXT = "As estradas de Arauna guardam sinais do DESENCANTO: nomes riscados, historias incompletas e Pokemon que hesitam diante de lugares conhecidos."

TERM_REPLACEMENTS = {
    "PROF. BIRCH": "PROF. ANAHI",
    "PROFESSOR BIRCH": "PROFESSORA ANAHI",
    "PROF BIRCH": "PROF ANAHI",
    "TEAM AQUA": "CONSORCIO HORIZONTE",
    "TEAM MAGMA": "LEMBRANTES",
    "AQUA": "HORIZONTE",
    "MAGMA": "LEMBRANTES",
    "ARCHIE": "OTACILIO",
    "MAXIE": "LUZIA",
}

CHARACTER_LINES = {
    "birch": "ANAHI: Eu estudei os VINCULOS antes de entender o que minhas pesquisas permitiriam fazer. Se eu continuar calada, o erro tambem sera meu.",
    "rival": "CIRO: Nao quero passar a vida preso ao que esta vila perdeu. O HORIZONTE me deu uma chance de seguir em frente. Vou descobrir se voce consegue acompanhar.",
    "may": "CIRO: O futuro nao espera por quem vive olhando para tras. Pelo menos era nisso que eu acreditava.",
    "brendan": "CIRO: O futuro nao espera por quem vive olhando para tras. Pelo menos era nisso que eu acreditava.",
    "wally": "VAL: Eu ainda tenho medo. Mas agora sei que coragem nao e esquecer o medo; e caminhar mesmo lembrando dele.",
    "norman": "ELIAS: Algumas culpas nao desaparecem quando ficamos em silencio. Eu aprovei parte do projeto de M'BOI. Passei anos chamando meu medo de prudencia.",
    "archie": "OTACILIO: Eu nao quero poder. Quero um mundo em que nenhuma pessoa seja obrigada a carregar para sempre a pior coisa que ja viveu.",
    "aqua": "HORIZONTE: O Arquivo preserva o que o tempo destruiria. Um dia voces vao agradecer por nao precisarem mais sofrer para lembrar.",
    "maxie": "LUZIA: Ninguem tem o direito de escolher que memoria merece morrer. Se for preciso devolver toda a dor de uma vez, eu vou devolver.",
    "magma": "LEMBRANTE: Apagar uma historia porque ela incomoda quem manda e apenas outra forma de violencia.",
    "steven": "SEU BENTO: Quando um nome some da boca das pessoas, eu escrevo. Nao para substituir quem lembra. Para deixar uma pista para quem vier procurar.",
    "wallace": "AMALIA: Arauna sobreviveu a verdade pela metade por tempo demais. A Liga tambem tem dividas com os nomes que foram deixados para tras.",
    "juan": "DONA CELINA: Agua parada apodrece. Agua que corre leva coisas embora. Viver e aprender o que guardar e o que deixar seguir.",
}

LEADER_LINES = {
    "roxanne": "DALVA: Pedra guarda marcas. Algumas rachaduras contam mais que monumentos inteiros.",
    "brawly": "ADEMAR: O mar devolve coisas quando quer. Homem nenhum manda na memoria da agua.",
    "wattson": "OLIVIA: Energia move uma cidade. Isso nao significa que toda fonte de energia deva ser aceita.",
    "flannery": "NARA: Cinza e o que sobra depois do fogo. Nao e o fim de tudo; mas tambem nao devemos fingir que nada queimou.",
    "winona": "LIDIA: A mata ensina caminhos sem escrever placas. Quando os Pokemon esquecem esses caminhos, alguma coisa muito antiga foi ferida.",
    "tate": "CECILIA: Do alto, cidades parecem pequenas. As vidas dentro delas nunca sao.",
    "liza": "CAETANO: Um sinal pode atravessar o ceu. Isso nao lhe da o direito de atravessar a mente de alguem.",
}

FUNCTIONAL_HINTS = (
    "RunningShoes", "Pokedex", "Pokédex", "PokeNav", "PokéNav", "MachBike", "AcroBike",
    "Bike", "Itemfinder", "Rod", "Berry", "TM", "HM", "Heal", "Mart", "Cable", "Trade",
    "PC", "Storage", "Bag", "MoveTutor", "Lottery", "Contest", "SecretBase", "Decoration",
    "GiveItem", "Received", "Obtain", "Found", "Purchase", "Buy", "Sell",
)

MAJOR_STORY_WORDS = (
    "Birch", "Rival", "May", "Brendan", "Wally", "Norman", "Aqua", "Magma", "Archie",
    "Maxie", "Steven", "Wallace", "Juan", "Roxanne", "Brawly", "Wattson", "Flannery",
    "Winona", "Tate", "Liza", "Groudon", "Kyogre", "Rayquaza", "Orb", "Submarine",
    "Weather", "SpaceCenter", "MtPyre", "Seafloor", "SkyPillar", "Devon",
)

FLAVOR = [
    "Tem gente que chama de DESENCANTO. Eu chamava de distraicao, ate minha mae esquecer a cancao que cantava desde crianca.",
    "O HORIZONTE consertou a estrada daqui. Nao sei se isso torna mais facil perguntar o que existe debaixo dela.",
    "Dona Zila diz que uma historia muda toda vez que e contada. Talvez seja por isso que ainda esta viva.",
    "Ultimamente alguns Pokemon param diante de suas antigas casas como se nunca tivessem estado ali.",
    "Meu avo dizia que lembrar tambem cansa. Mas escolher pelo outro o que ele deve esquecer parece pior.",
    "Existem placas novas por toda parte. Curioso e que alguns nomes antigos desapareceram quando elas chegaram.",
]

TEXT_BLOCK_RE = re.compile(
    r"(?m)^(?P<label>[A-Za-z0-9_]+_Text_[A-Za-z0-9_]+):\n(?P<body>(?:\t\.string .*\n)+)"
)


def context_for(map_name: str) -> tuple[str, str]:
    for prefix, location, context in LOCATION_CONTEXTS:
        if map_name.startswith(prefix):
            return location, context
    return map_name.upper(), GENERIC_ROUTE_CONTEXT


def normalize_old(body: str) -> str:
    parts = re.findall(r'\.string\s+"(.*)"', body)
    return " ".join(parts)


def escape_asm(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def emit_message(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    wrapped = textwrap.wrap(text, width=31, break_long_words=False, break_on_hyphens=False)
    if not wrapped:
        wrapped = ["..."]
    pages = [wrapped[i:i + 2] for i in range(0, len(wrapped), 2)]
    out = []
    for i, page in enumerate(pages):
        payload = "\\n".join(page)
        payload += "\\p" if i < len(pages) - 1 else "$"
        out.append(f'\t.string "{escape_asm(payload)}"\n')
    return "".join(out)


def story_message(label: str, old_body: str, map_name: str) -> str | None:
    old = normalize_old(old_body)
    low = label.lower()
    location, context = context_for(map_name)

    # Preserve tutorials/items unless they are directly tied to the old plot.
    if any(h.lower() in low for h in FUNCTIONAL_HINTS) and not any(w.lower() in low for w in MAJOR_STORY_WORDS):
        return None

    if "townsign" in low or "citysign" in low or low.endswith("_text_sign"):
        return f"{location}. {context}"

    # Central cast / antagonist slots.
    for key, line in CHARACTER_LINES.items():
        if key in low or key in old.lower():
            # Steven's late-game role is Ciro rather than Seu Bento.
            if key == "steven" and (map_name.startswith("Mossdeep") or map_name.startswith("Sootopolis") or map_name.startswith("PokemonLeague")):
                return "CIRO: Eu aceitei o uniforme porque ele abriu portas. Agora sei de quem eram as vozes que ficaram trancadas do outro lado. Nao vou fingir que nunca vesti aquilo."
            return line

    for key, line in LEADER_LINES.items():
        if key in low or key in old.lower():
            return line

    # Old legendary/weather climax becomes the two impulses of Arauna.
    if any(k in low or k in old.lower() for k in ("groudon", "kyogre", "rayquaza", "orb")):
        if map_name.startswith("SkyPillar"):
            return "O CADERNO DE ZILA nao guarda uma verdade perfeita. Guarda pessoas tentando lembrar juntas. O JURAMENTO nunca foi impedir o esquecimento; foi impedir que alguem escolhesse o esquecimento dos outros."
        if map_name.startswith("Sootopolis"):
            return "As duas forcas antigas de Arauna reagiram ao colapso. IARA-MAE puxa os nomes de volta. ANHANGUERA tenta encerrar o que nao pode continuar. Nenhuma delas foi feita para obedecer a seres humanos."
        return "Os sensores registram duas correntes antigas sob Arauna: uma conserva VINCULOS; a outra permite que eles terminem. O Arquivo tentou transformar ambas em ferramentas."

    # Story-heavy generic blocks in key locations receive location-specific narrative.
    if any(w.lower() in low for w in MAJOR_STORY_WORDS):
        return context

    # Question labels must remain questions so yes/no scripts still make sense.
    if any(k in low for k in ("ask", "question", "want", "would", "ready", "shall")) or "?" in old:
        return f"Voce vai continuar mesmo sabendo que {location} guarda partes da historia que muita gente preferia deixar enterradas?"

    # Replace most ambient NPC flavor in story locations so Emerald's worldbuilding disappears.
    digest = int(hashlib.sha1(label.encode()).hexdigest()[:8], 16)
    return FLAVOR[digest % len(FLAVOR)]


def apply_term_replacements(text: str) -> str:
    for old, new in TERM_REPLACEMENTS.items():
        text = text.replace(old, new)
    return text


def process_script(path: Path) -> tuple[int, int]:
    map_name = path.parent.name
    if not map_name.startswith(TARGET_PREFIXES):
        return 0, 0

    original = path.read_text(encoding="utf-8")
    replaced = apply_term_replacements(original)
    changed_blocks = 0
    total_blocks = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal changed_blocks, total_blocks
        total_blocks += 1
        label = match.group("label")
        body = match.group("body")
        msg = story_message(label, body, map_name)
        if msg is None:
            # Still apply entity renames inside functional text.
            body2 = apply_term_replacements(body)
            if body2 != body:
                changed_blocks += 1
            return f"{label}:\n{body2}"
        changed_blocks += 1
        return f"{label}:\n{emit_message(msg)}"

    replaced = TEXT_BLOCK_RE.sub(repl, replaced)
    if replaced != original:
        path.write_text(replaced, encoding="utf-8")
    return changed_blocks, total_blocks


def main() -> None:
    changed_files = 0
    changed_blocks = 0
    total_blocks = 0
    touched = []

    for path in sorted(MAP_ROOT.glob("*/scripts.inc")):
        c, t = process_script(path)
        if c:
            changed_files += 1
            changed_blocks += c
            total_blocks += t
            touched.append(str(path.relative_to(ROOT)))

    report = ROOT / "docs" / "ARAUANA_STORY_IMPLEMENTATION.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        "# Pokemon Juramento de Arauna - Story implementation\n\n"
        "This pass preserves the vanilla Pokemon Emerald event graph, flags, warps, badge order and route progression while replacing the narrative surface of the principal story maps with the Arauna canon.\n\n"
        "## Canon\n"
        "- Core theme: memory, grief, erasure and consent.\n"
        "- Phenomenon: Desencanto.\n"
        "- Technology: Arquivo Vivo.\n"
        "- Corporate force: Consorcio Horizonte, led by Dr. Otacilio Meira.\n"
        "- Radical opposition: Lembrantes, led by Luzia Ferraz.\n"
        "- Mentor: Professora Anahi, who helped create the first Vinculo sensors.\n"
        "- Oral-memory keeper: Dona Zila.\n"
        "- Rival: Ciro, initially sponsored by Horizonte.\n"
        "- Father: Elias, connected to the approvals behind the M'Boi disaster.\n"
        "- Final thesis: nobody has the right to decide for someone else what deserves to be remembered.\n\n"
        "## Structural rule\n"
        "No route-order, badge-order, warp, progression flag, map connection or core event trigger is intentionally changed by this tool. Existing Emerald story slots are reinterpreted instead.\n\n"
        f"## Patch statistics\n- Script files changed: {changed_files}\n- Dialogue blocks rewritten/renamed: {changed_blocks}\n- Dialogue blocks inspected in touched files: {total_blocks}\n\n"
        "## Touched files\n" + "\n".join(f"- `{p}`" for p in touched) + "\n",
        encoding="utf-8",
    )

    print(f"Arauna story: changed {changed_blocks} dialogue blocks across {changed_files} script files")
    print(f"Report: {report.relative_to(ROOT)}")
    if changed_files < 25 or changed_blocks < 100:
        raise SystemExit("Story rewrite coverage unexpectedly low; refusing to publish")


if __name__ == "__main__":
    main()
