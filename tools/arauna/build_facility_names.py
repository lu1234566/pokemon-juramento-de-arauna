#!/usr/bin/env python3
"""Give the facility trainers Brazilian names.

The route trainers were renamed; the 526 people who staff the endgame were not.
The Battle Frontier alone fields 300 of them, the three Battle Tents 90, Trainer
Hill 32, and the contest circuit 104 -- more names than the whole overworld, all
still Hoenn's, and all in front of the player for the hours the Frontier is
meant to last.

Nothing here is a character. They are opponents drawn from a pool, and the
engine already knows each one's gender: the Battle Frontier, the Tents and
Trainer Hill by facilityClass, checked against gTowerMaleFacilityClasses and
gTowerFemaleFacilityClasses in src/battle_tower.c rather than guessed from the
class name, and the contest opponents by the overworld sprite they walk in on.
The eight Contest Hall winners are the exception -- they are a name under a
painting, with no sprite and no gender anywhere in the engine -- so they simply
alternate.

Every one of these fields is PLAYER_NAME_LENGTH, seven characters, which is
three fewer than a route trainer gets and the reason these pools are short
forms. Trainer Hill's field is ten, but it draws from the same pool.

Names may repeat one given to a route trainer. There are only so many short
Brazilian names, and two ordinary people sharing one is what ordinary names do;
within these four tables no name is used twice, exactly as in vanilla.

Only the name changes. Parties, easy-chat speeches, facility classes, AI, the
contest stat blocks and every id are untouched.

  --check   report what would be renamed
  --write   rewrite the four tables and the roster CSV
"""
from __future__ import annotations

import argparse
import collections
import csv
import itertools
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VANILLA = "c210195e"
TOWER = ROOT / "src/battle_tower.c"
ROSTER = ROOT / "docs/arauna/ARAUNA_FACILITY_NAMES.csv"

NAME_LIMIT = 7  # PLAYER_NAME_LENGTH, the shortest field of the four

WOMEN = """
ADA ADELIA ADILIA ALBA ALCINA ALDA ALICE ALINE ALZIRA AMALIA AMELIA ANA ANDREA
ANGELA ANITA ANTONIA AUREA AURORA BABI BEATRIZ BELA BENTA BIA BIANCA
BRUNA CAMILA CANDIDA CARLA CARMEM CARMO CAROL CASSIA CATIA CECILIA CELIA CELINA
CELMA CIDA CILENE CINTIA CLARA CLARICE CLAUDIA CLEIDE CLELIA CLEO CLEUZA CORA
DAIANE DALIA DALILA DALVA DANIELA DARCI DEBORA DELIA DENISE DINA DIRCE DIVA
DORA DORIS DUDA DULCE EDINA EDITE EDNA ELAINE ELBA ELENA ELIANA ELISA ELIZA
ELOA ELOISA ELSA ELVIRA ELZA EMILIA ERICA ERIKA ESTELA ESTER EUNICE EVA FABIANA
FATIMA FLAVIA FLORA FRANCA GABI GEISA GEMA GENI GILDA GINA GISELE GLAUCIA
GLORIA GRACA GRAZI GUIDA HELENA HELOISA HILDA IARA IDA IEDA IGNEZ ILDA ILZA
INES IOLANDA IRACEMA IRENE IRIS ISABEL ISADORA ISAURA ISIS IVA IVANI IVETE
IVONE IZA JACIRA JANDIRA JANE JANETE JOANA JOICE JOSEFA JOVITA JULIA JULIANA
JUREMA JUSSARA KARINA KATIA LARA LARISSA LAURA LEA LEDA LEILA LENIRA LETICIA
LIA LIDIA LIGIA LILIA LILIAN LINA LIS LISA LIVIA LOURDES LUANA LUCIA LUCILA
LUIZA LURDES MAFALDA MAGDA MAIRA MALU MANUELA MARA MARCIA MARIA MARIANA MARILDA
MARINA MARISA MARLENE MARLI MARTA MATILDE MAURA MEIRE MELISSA MERCIA MILENA
MIRIAM MIRNA MONICA MORENA NADIA NAIR NARA NATALIA NAZARE NEIDE NEIVA NELI
NELMA NEUSA NIDIA NILDA NILZA NINA NOEMIA NORA NORMA ODETE OLGA OLIVIA ONDINA
PALOMA PAULA PIEDADE RAFAELA RAQUEL REGINA RENATA RITA ROSA ROSALIA
ROSANA ROSELI ROSILDA RUTE SANDRA SARA SELMA SILVIA SIMONE SOFIA SOLANGE SONIA
SUELI SUZANA TAIS TALITA TANIA TATIANA TELMA TEREZA THAIS TINA VALERIA VANDA
VANESSA VERA VILMA VITORIA VIVI VIVIANE WILMA YARA ZELIA ZILDA ZILMA ZORAIDE
"""

MEN = """
ABEL ABILIO ADAIR ADALTO ADAO ADEMAR ADEMIR ADILSON ADOLFO ADRIANO AFONSO
AGENOR AILTON AIRTON ALAOR ALBANO ALBERTO ALCEU ALCIDES ALDO ALEX ALFREDO
ALIPIO ALMIR ALOISIO ALTAIR ALVARO AMADEU AMANCIO AMARO AMAURI AMERICO AMILCAR
ANDRE ANGELO ANIBAL ANSELMO ANTENOR ANTONIO AQUILES ARI ARIEL ARLEI ARLINDO
ARMANDO ARNALDO ARNO ARTUR ARY ASSIS ATILIO AUGUSTO AURELIO AVELINO BASILIO
BENICIO BENTO BERILO BRAULIO BRAZ BRUNO CAETANO CAIO CALIXTO CAMILO CANDIDO
CARLOS CARMELO CASSIO CELSO CESAR CICERO CLAUDIO CLEBER CLOVIS CONRADO DALTON
DAMIAO DANILO DANTE DARCY DARIO DAVI DELCIO DELFINO DELMIRO DENIS DEODORO DIEGO
DINO DIOGO DIRCEU DIVINO DJALMA DOMICIO DONATO DORIVAL DOUGLAS DURVAL EDGAR
EDILSON EDIMAR EDMAR EDMUNDO EDNALDO EDSON EDUARDO EDVALDO EGIDIO ELDER ELIAS
ELISEU ELVIO EMIDIO EMILIO ENEAS ENIO ENOQUE ERALDO ERASMO ERNANI ERNESTO
EUGENIO EURICO EVALDO EVANDRO EZIO FABIANO FABIO FAUSTO FELICIO FELIPE FIDELIS
FILINTO FIRMINO FLAVIO FRANCO GABRIEL GALDINO GENARO GENESIO GERALDO GERMANO
GERSON GETULIO GIL GILDO GILSON GIOVANI GLAUCO GONCALO GUIDO GUSTAVO HEITOR
HELIO HERALDO HERMES HIGINO HILARIO HORACIO HUGO IBERE IDALIO IGOR ILDO INACIO
IRINEU ISAIAS ISIDORO ISMAEL ISRAEL ITAMAR IVAN IVANIR IVO JACINTO JADIR JAIME
JAILSON JAIR JAMIL JARBAS JAYME JOAO JOAQUIM JOEL JONAS JONATAS JORGE JOSE
JOSIAS JOSUE JOVENAL JOVINO JUAREZ JUCA JULIANO JULIO JUSTINO JUVENAL KLEBER
LAERTE LAURO LAZARO LEANDRO LEO LEONCIO LEONEL LIVIO LOTARIO LUCA LUCAS LUCIANO
LUCIO LUDGERO LUIS LUIZ MACARIO MAGNO MANOEL MANUEL MARCELO MARCIO MARCOS
MARIANO MARINO MARIO MARTIM MATEUS MATIAS MAURO MAXIMO MIGUEL MILTON MOACIR
MODESTO MOISES MOZART MURILO NABOR NARCISO NEI NELIO NELSON NEREU NESTOR NEWTON
NICANOR NICOLAU NILDO NILO NILSON NILTON NIVALDO NIVIO NOEL OCTAVIO ODAIR
ODILON ODORICO OLAVO OLIMPIO OLIVIO ONOFRE ORESTE ORESTES ORLANDO OSCAR OSEIAS
OSMAR OSORIO OSVALDO OSWALDO OTAVIO OTELO OTHON OTONIEL OZIEL PASCOAL PAULINO
PAULO PEDRO PLINIO POMPEU QUIRINO RAFAEL RAMIRO RAUL REGIS REMIGIO RENAN RENATO
RENE RICARDO RIVALDO ROBERTO ROBSON RODOLFO RODRIGO ROGERIO ROLANDO ROMARIO
ROMEU ROMILDO ROMULO RONALDO RONAN ROQUE ROSALVO RUBEM RUBENS RUFINO RUI SABINO
SAMUEL SANDRO SATURNO SAUL SAULO SERAFIM SERGIO SEVERO SIDNEI SILAS SILVANO
SILVIO SIMAO SOARES SOLANO TADEU TELMO TEODORO TEOFILO THIAGO TIAGO TIAO
TIBERIO TIMOTEO TITO TOBIAS TOMAS TON TRAJANO TULIO UBALDO ULISSES URBANO
VALDECI VALDIR VALDO VALERIO VIANA VICENTE VITOR WAGNER WALDIR WALTER WANDER
WILSON XAVIER ZECA ZILDO ZEZINHO
"""


def at_vanilla(path: Path) -> str:
    return subprocess.run(
        ["git", "show", f"{VANILLA}:{path.relative_to(ROOT)}"], cwd=ROOT,
        capture_output=True, text=True, check=True).stdout


def tower_genders() -> tuple[set[str], set[str]]:
    """The engine's own lists, not a guess from the class name."""
    body = TOWER.read_text(encoding="utf-8")

    def listed(symbol: str) -> set[str]:
        block = re.search(r"const u8 " + symbol + r"\[\d+\] =\s*\{(.*?)\};", body, re.S)
        return set(re.findall(r"FACILITY_CLASS_\w+", block.group(1)))

    return listed("gTowerMaleFacilityClasses"), listed("gTowerFemaleFacilityClasses")


# The contest opponents carry an overworld sprite instead of a facility class.
FEMALE_GFX = re.compile(r"WOMAN|GIRL|LASS|TWIN|PICNICKER|HEX_MANIAC|BEAUTY|TEALA"
                        r"|EXPERT_F|TUBER_F|POKEFAN_F")

# Each table, its file, and how a name and its gender sit together in the text.
# `pattern` must capture the name as `name`; `female` says how to read the row.
TABLES = [
    ("battle frontier", "src/data/battle_frontier/battle_frontier_trainers.h",
     r'\.facilityClass = (?P<class>FACILITY_CLASS_\w+),\n\s*\.trainerName = _\("(?P<name>[^"]+)"\)'),
    ("battle tent", "src/data/battle_frontier/battle_tent.h",
     r'\.facilityClass = (?P<class>FACILITY_CLASS_\w+),\n\s*\.trainerName = _\("(?P<name>[^"]+)"\)'),
    ("trainer hill", "src/data/battle_frontier/trainer_hill.h",
     r'\.name = _\("(?P<name>[^"]+)"\),\n\s*\.facilityClass = (?P<class>FACILITY_CLASS_\w+)'),
    ("contest opponent", "src/data/contest_opponents.h",
     r'\.trainerName = _\("(?P<name>[^"]+)"\),\n\s*\.trainerGfxId = (?P<gfx>OBJ_EVENT_GFX_\w+)'),
    # No sprite, no facility class, no gender: a name under a painting.
    ("contest hall", "src/data/contest_opponents.h",
     r'\.monName = _\("[^"]*"\),\n\s*\.trainerName = _\("(?P<name>[^"]+)"\)'),
]


def read(table: str, path: Path, pattern: str, male: set[str], female: set[str],
         alternate: itertools.cycle) -> list[dict]:
    out = []
    for found in re.finditer(pattern, at_vanilla(path)):
        groups = found.groupdict()
        if groups.get("class"):
            is_female = groups["class"] in female
            if not is_female and groups["class"] not in male:
                raise SystemExit(f"{groups['class']} is in neither tower gender list")
        elif groups.get("gfx"):
            is_female = bool(FEMALE_GFX.search(groups["gfx"]))
        else:
            is_female = next(alternate)
        out.append({"table": table, "path": path, "name": groups["name"],
                    "female": is_female})
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    male, female = tower_genders()
    alternate = itertools.cycle([True, False])
    people = []
    for table, path, pattern in TABLES:
        people += read(table, ROOT / path, pattern, male, female, alternate)

    # Fourteen vanilla names are used twice, in two different facilities, and
    # they are two different people -- so the assignment is per entry, in the
    # order the tables are read, not per name as it was for the route trainers.
    women, men = WOMEN.split(), MEN.split()
    long_ones = [n for n in women + men if len(n) > NAME_LIMIT]
    pools = {True: iter(women), False: iter(men)}
    short = []
    for person in people:
        pick = next(pools[person["female"]], None)
        if pick is None:
            short.append(person["name"])
            continue
        person["arauna"] = pick

    wanted = collections.Counter(p["female"] for p in people)
    print(f"{len(people)} facility trainers: {wanted[True]} women, {wanted[False]} men")
    print(f"  pools hold {len(women)} women and {len(men)} men")
    print(f"  names over {NAME_LIMIT} characters in the pools: {len(long_ones)} {long_ones[:5]}")
    print(f"  ran out of names for: {len(short)} {short[:5]}")
    clashes = sorted(n for n, c in collections.Counter(
        p.get("arauna") for p in people).items() if c > 1)
    print(f"  two people given the same name: {len(clashes)} {clashes[:5]}")
    for table, _, _ in TABLES:
        rows = [p for p in people if p["table"] == table]
        print(f"  {table:18} {len(rows):4}   "
              + ", ".join(f"{p['name']}->{p.get('arauna', '?')}" for p in rows[:3]))

    if long_ones or short or clashes:
        raise SystemExit("refusing: fix the pools first")

    # The decision is made against each file's vanilla text, so a file someone
    # has already edited is left alone and a second run rewrites nothing.
    changed, skipped = 0, []
    for path in sorted({p["path"] for p in people}):
        body = path.read_text(encoding="utf-8")
        if body != at_vanilla(path):
            skipped.append(path.name)
            continue
        for table, relative, pattern in TABLES:
            if ROOT / relative != path:
                continue
            rows = iter(p for p in people if p["table"] == table)

            def rename(found, rows=rows):
                person = next(rows)
                assert found.group("name") == person["name"]
                return found.group(0).replace(f'_("{person["name"]}")',
                                              f'_("{person["arauna"]}")')

            body, count = re.subn(pattern, rename, body)
            changed += count
        if args.write:
            path.write_text(body, encoding="utf-8")
    print(f"  {changed} names to rewrite"
          + (f"; left alone because already edited: {skipped}" if skipped else ""))

    if not args.write:
        return 0

    with ROSTER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["table", "gender", "vanilla_name", "arauna_name"])
        for person in people:
            writer.writerow([person["table"],
                             "F" if person["female"] else "M",
                             person["name"], person["arauna"]])
    print(f"\nwrote the four tables and {ROSTER.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
