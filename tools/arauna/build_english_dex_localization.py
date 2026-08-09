#!/usr/bin/env python3
"""Build the English-first, player-facing localization for Arauna's 386 species."""

from __future__ import annotations

import argparse
import json
import re
import textwrap
from pathlib import Path


REGION_EN = {
    "Amazônia de Arauana": "Arauna Amazon",
    "Banhados de Arauana": "Arauna Wetlands",
    "Caatinga de Arauana": "Arauna Caatinga",
    "Campos queimados de Arauana": "Arauna Burned Fields",
    "Cavernas de Arauana": "Arauna Caves",
    "Cerrado de Arauana": "Arauna Cerrado",
    "Chapadas de Arauana": "Arauna Plateaus",
    "Cidades de Arauana": "Arauna Cities",
    "Litoral de Arauana": "Arauna Coast",
    "Mata Atlântica de Arauana": "Arauna Atlantic Forest",
    "Pampas de Arauana": "Arauna Pampas",
    "Pantanal de Arauana": "Arauna Pantanal",
    "Periferia de Arauana": "Arauna Outskirts",
    "Rio Amazonas de Arauana": "Arauna Amazon River",
    "Rio Solimões de Arauana": "Arauna Solimoes River",
    "Rios de Arauana": "Arauna Rivers",
    "Serra de Arauana": "Arauna Highlands",
    "Sertão de Arauana": "Arauna Backlands",
}

TYPE_EN = {
    "normal": "Normal", "fire": "Fire", "water": "Water", "grass": "Grass",
    "electric": "Electric", "ice": "Ice", "fighting": "Fighting",
    "poison": "Poison", "ground": "Ground", "flying": "Flying",
    "psychic": "Psychic", "bug": "Bug", "rock": "Rock", "ghost": "Ghost",
    "dragon": "Dragon", "dark": "Dark", "steel": "Steel", "fairy": "Fairy",
}

CATEGORY_EN = dict(
    line.split("\t", 1)
    for line in """Alarmante	Raucous
Alarme	Alarm
Alegria	Joy
Amaldiçoado	Cursed
Amor	Love
Amuleto	Charm
Ancestral	Ancestral
Anelídeo	Annelid
Anfíbio	Amphibian
Anteater	Anteater
Aquático	Aquatic
Arara	Macaw
Arco-íris	Rainbow
Argila	Clay
Arte	Art
Assombração	Haunting
Astro	Celestial
Ataque	Attack
Aurora	Dawn
Ave-de-Rapina	Raptor
Azulzinho	Blue
Bandido	Bandit
Bando	Pack
Bateria	Battery
Beata	Devout
Bicudo	Big-Beak
Bigode	Whisker
Bochechudo	Chubby-Cheek
Boi	Ox
Bolinha	Rolling
Boneco	Puppet
Boto	RiverDolphin
Bromélia	Bromeliad
Broto	Sprout
Bruxa	Witch
Cabelim	Curly-Hair
Cabra	Goat
Cacto	Cactus
Camaleão	Chameleon
Camuflado	Camouflage
Cantor	Singer
Capivara	Capybara
Capoeira	Capoeira
Cardume	Schooling
Carniceiro	Scavenger
Casco	Shell
Casulo	Cocoon
Cavalgadura	Mount
Caverna	Cave
Caçador	Hunter
Caçadora	Huntress
Cegonha	Stork
Cerrado	Cerrado
Cervo	Deer
Chamuscado	Scorched
Chocalho	Rattle
Chocolate	Chocolate
Choque	Shock
Chorume	Leachate
Chá	Tea
Cimento	Cement
Cobra-Fogo	Fire-Snake
Cobra-Grande	Great-Snake
Cobra-grande	Great-Snake
Colhereiro	Spoonbill
Colibri	Hummingbird
Concha	Shell
Conselheiro	Advisor
Constritora	Constrictor
Corredor	Runner
Corredora	Runner
Corrosão	Corrosion
Cortejo	Procession
Coruja	Owl
Crepúsculo	Twilight
Criador	Creator
Cristal	Crystal
Crustáceo	Crustacean
Curioso	Curious
Cão-Dragão	Dragon-Dog
Depósito	Dump
Descarte	Litter
Deus	God
Deusa	Goddess
Devora	Devourer
Devorador	Devourer
Disco	Disc
Divino	Divine
Ecolocalizador	Echolocator
Emboscada	Ambush
Encantado	Enchanted
Encantadora	Enchantress
Energético	Energetic
Enxofre	Sulfur
Erudita	Scholar
Ervas	Herbal
Escavador	Burrower
Escultor	Sculptor
Escultura	Sculpture
Esgoto	Sewer
Espectro	Specter
Espiga	Grain
Espírito	Spirit
Estelar	Stellar
Estrela	Star
Falante	Talker
Farsante	Trickster
Fedido	Stench
Fermentação	Ferment
Ferramenteiro	Toolmaker
Ferroada	Stinger
Ferrão	Stinger
Festeiro	Reveler
Fio	Wire
Fios	Threads
Flamejante	Blazing
Flor	Flower
Florido	Blooming
Flutuante	Floating
Focinho-longo	Long-Snout
Fogo	Fire
Foice	Scythe
Fole	Bellows
Formigueiro	Anthill
Forró	Forro
Fortaleza	Fortress
Frugívoro	Fruit-Eater
Fruta	Fruit
Frutífero	Fruit-Bearer
Furtivo	Stealth
Fóssil	Fossil
Gigante	Giant
Girino	Tadpole
Guardiã	Guardian
Guardião	Guardian
Guerreira	Warrior
Guerreiro	Warrior
Iluminação	Lighting
Insetívoro	Insectivore
Instrumento	Instrument
Inteligente	Clever
Iridescente	Iridescent
Isca	Lure
Ladrão	Thief
Lagarta	Caterpillar
Lagarto	Lizard
Lanterna	Lantern
Lenta	Slow
Lento	Slow
Lua	Moon
Lunar	Lunar
Lutador	Fighter
Lâmina	Blade
Lã	Wool
Mancha	Stain
Manchada	Spotted
Mandíbula	Jaw
Manso	Gentle
Mar	Sea
Marinho	Marine
Marteleta	Hammer-Beak
Marujo	Sailor
Mefítico	Noxious
Mel	Honey
Mensageiro	Messenger
Metal	Metal
Miado	Mewing
Milagre	Miracle
Montanha	Mountain
Mãe	Mother
Mãe-d'Água	Water-Mother
Mítico	Mythical
Nadador	Swimmer
Nenúfar	Water-Lily
Noturno	Nocturnal
Origem	Origin
Palmeira	Palm
Papagaio	Parrot
Parede	Wall
Passistas	Dancer
Pedreiro	Builder
Peixe	Fish
Peluda	Hairy
Periquito	Parakeet
Perna-longa	Long-Legged
Perneta	One-Legged
Pescadora	Fisher
Pintura	Paint
Pinça	Pincer
Placa	Armor-Plate
Poeira	Dust
Poeta	Poet
Poluição	Pollution
Pomba	Pigeon
Praga	Pest
Predador	Predator
Preguiçoso	Lazy
Quilombo	Quilombo
Rainha	Queen
Raiz	Root
Rato	Rat
Recicla	Recycler
Reciclável	Recyclable
Redentor	Redeemer
Rei	King
Renda	Lace
Resiliente	Resilient
Rio	River
Ritmo	Rhythm
Rocha	Rock
Roedor	Rodent
Roedora	Rodent
Rua	Street
Réptil	Reptile
Sal	Salt
Saltador	Jumper
Salto	Leaping
Sapo	Toad
Seca	Drought
Seixo	Pebble
Semente	Seed
Sentinela	Sentinel
Sereia	Mermaid
Serpente	Serpent
Sinal	Signal
Sol	Sun
Solar	Solar
Soldado	Soldier
Sombra	Shadow
Sonhador	Dreamer
Superstição	Bad-Omen
Suprema	Supreme
Supremo	Supreme
Sábio	Sage
Tambor	Drum
Tempestade	Storm
Tentáculo	Tentacle
Terra	Earth
Territorial	Territorial
Terror	Terror
Traquinas	Prankster
Trepadeira	Vine
Trovão	Thunder
Uivador	Howler
Vampiro	Vampire
Vento	Wind
Verde	Verdant
Vetor	Vector
Vigia	Watchman
Viola	Viola
Vira-lata	Stray
Vulcão	Volcano
Xamã	Shaman
Zen	Zen
Águia	Eagle
Árvore	Tree""".splitlines()
)

CUSTOM_DEX = {
    1: "A caramel-coated street pup. When it trusts a Trainer, its tail lights a small, steady flame that never burns a friendly hand.",
    2: "It guards open-air markets. The embers across its back move like fleas and bite only those who try to steal.",
    3: "Legends say every caramel dog that saves a life is reborn as Draguará. Its turquoise flames warm but never harm the innocent.",
    4: "It never fully sleeps. One eye watches its nest, and its quero-quero cry can echo for miles when danger approaches.",
    5: "After its first molt, its feathers become iridescent dragonfly membranes. It hovers above water and hunts with exact precision.",
    6: "Four dragonfly wings support its slender lapwing body. A single wingbeat can launch a stream strong enough to split a trunk.",
    7: "Its soft beak drills bark for larvae. It trains by hammering dry stumps all day, then returns to its nest with a headache.",
    8: "Its beak hardens like ironwood. It drums complex rhythms on trees that other Bicopau understand as messages.",
    9: "Its beak calcified into a granite wedge. It carves caves into stone cliffs with blows that ring like bells.",
    10: "It is not a single ant, but an entire colony walking in the shape of a giant one. The colony scatters when threatened.",
    11: "The queen of the leaf-cutter ants. It commands armies able to strip every leaf from a tree in one night.",
    12: "It lives in riverside groups and lets any friendly POKéMON rest on its back, including tired Trainers.",
    13: "Its huge beak is hollow and light. It swallows fruit whole and spits seeds far away, planting forests on its own.",
    14: "It steals anything that shines. Trainers quickly learn to keep their Gym Badges at the bottom of their bags.",
    15: "The elder of the Sagüim troop. It reads the future in river reflections and can predict rain a week ahead.",
    16: "It appears after wildfires. Its body is a blue flame-serpent that hunts those who deliberately burn the forest.",
    17: "Its feet point backward. The tracks it leaves confuse hunters and guide them deeper into the forest.",
    18: "The true lord of the forest. Wherever it steps, a century-old tree can rise in a single night.",
    19: "Its song enchants fishers. Those who follow it into the river are said to join its court forever.",
    20: "It has only one leg and rides inside whirlwinds. It loves putting out campfires and teasing careless Trainers.",
}


def generic_description(entry: dict, category: str, region: str) -> str:
    types = [TYPE_EN[value] for value in entry.get("types", ["normal"])]
    affinity = "/".join(types)
    templates = (
        f"{entry['name']}, the {category} POKéMON, inhabits {region}. Its {affinity} nature reflects Brazil's wildlife and legends.",
        f"Found in {region}, {entry['name']} is known as the {category} POKéMON. It carries a distinct {affinity} affinity.",
        f"{entry['name']} lives in {region}. This {affinity} POKéMON embodies a part of Brazil's nature, folklore, or culture.",
    )
    return templates[(int(entry["id"]) - 1) % len(templates)]


def build_localization(source: dict) -> dict:
    localized = []
    missing_categories = set()
    missing_regions = set()
    for entry in source["pokemon"]:
        source_category = re.sub(r"^Pokémon\s+", "", entry["category"], flags=re.IGNORECASE)
        if source_category not in CATEGORY_EN:
            missing_categories.add(source_category)
            continue
        if entry["region"] not in REGION_EN:
            missing_regions.add(entry["region"])
            continue
        category = CATEGORY_EN[source_category]
        region = REGION_EN[entry["region"]]
        if len(category) > 12:
            raise ValueError(f"category exceeds 12 characters: {source_category} -> {category}")
        localized.append({
            "id": int(entry["id"]),
            "category": category,
            "region": region,
            "dex": CUSTOM_DEX.get(int(entry["id"]), generic_description(entry, category, region)),
        })
    if missing_categories:
        raise ValueError(f"missing categories: {sorted(missing_categories)}")
    if missing_regions:
        raise ValueError(f"missing regions: {sorted(missing_regions)}")
    if len(localized) != 386 or [entry["id"] for entry in localized] != list(range(1, 387)):
        raise ValueError("English localization must contain consecutive IDs 001-386")
    return {
        "language": "en",
        "region": "Arauna",
        "total": 386,
        "notes": "Names remain Brazilian proper nouns. Player-facing category, habitat, and Dex text are English.",
        "pokemon": localized,
    }


def wrapped_description(text: str, width: int = 36, lines: int = 4) -> list[str]:
    text = " ".join(text.replace("\n", " ").split()).replace('"', "'").replace("—", "-").replace("–", "-")
    wrapped = textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False)
    if len(wrapped) > lines:
        wrapped = wrapped[:lines]
        wrapped[-1] = wrapped[-1].rstrip(".,;: ")
        if len(wrapped[-1]) >= width - 2:
            wrapped[-1] = wrapped[-1][:width - 3].rstrip()
        wrapped[-1] += "..."
    return wrapped


def replace_header_localization(header: str, localization: dict) -> str:
    prefix, *blocks = re.split(r"(?=    \[SPECIES_)", header)
    if len(blocks) != 386:
        raise ValueError(f"expected 386 species blocks, found {len(blocks)}")
    output = [prefix]
    for block, localized in zip(blocks, localization["pokemon"]):
        category = localized["category"].replace('"', "'")
        block, category_count = re.subn(
            r'(\.categoryName\s*=\s*_\(")[^"]*("\),)',
            rf"\g<1>{category}\g<2>",
            block,
            count=1,
        )
        lines = wrapped_description(localized["dex"])
        description = "\n".join(f'            "{line}\\n"' for line in lines[:-1])
        if lines:
            last = lines[-1] if lines[-1].endswith((".", "!", "?")) else lines[-1] + "."
            description += ("\n" if description else "") + f'            "{last}"'
        replacement = f".description = COMPOUND_STRING(\n{description}),\n        .pokemonScale"
        block, dex_count = re.subn(
            r"\.description\s*=\s*COMPOUND_STRING\(\n.*?\),\n        \.pokemonScale",
            lambda _match: replacement,
            block,
            count=1,
            flags=re.DOTALL,
        )
        if category_count != 1 or dex_count != 1:
            raise ValueError(f"could not localize species {localized['id']:03d}")
        output.append(block)
    return "".join(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("docs/arauna/source/pokedex.json"))
    parser.add_argument("--out", type=Path, default=Path("docs/arauna/source/pokedex.en.json"))
    parser.add_argument("--header", type=Path)
    args = parser.parse_args()

    source = json.loads(args.source.read_text(encoding="utf-8"))
    localization = build_localization(source)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(localization, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.header:
        header = args.header.read_text(encoding="utf-8")
        args.header.write_text(replace_header_localization(header, localization), encoding="utf-8")

    print(f"wrote {len(localization['pokemon'])} English entries to {args.out}")


if __name__ == "__main__":
    main()
