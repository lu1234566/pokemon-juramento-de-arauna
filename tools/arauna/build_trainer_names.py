#!/usr/bin/env python3
"""Give the route trainers Brazilian names.

The project renamed its story cast early on -- Roxanne became Dalva, Norman
Elias, Wattson Olivia -- twenty names covering 143 entries. The other 700 were
never touched, so 434 distinct Hoenn names still appear, one on every route
battle the player starts. That is the most frequently shown untranslated
surface left in the game.

Two sets are left alone. The 64 entries a renderer rewrites for the English
build -- the Elite Four, the Frontier Brains, the grunts -- because those names
belong to that renderer and rewriting them here would fight it. And anything
already renamed, which is checked against the vanilla tree rather than guessed
from spelling.

A vanilla name that repeats is one person: ABIGAIL appears five times because
the same triathlete is rematched at five levels. The mapping is therefore from
name to name, not entry to entry, so she stays one person afterwards.

Names are drawn by gender from a pool of ordinary Brazilian given names, in a
fixed order so a rerun produces the same assignment. Nothing about the trainer
changes except what they are called: class, party, gender, music and the AI
flags are untouched.

The seventeen tag pairs are the exception that costs the most: their halves are
also spoken -- Gabby names Ty on television, Anna names Meg on the PokeNav, Luke
names Dez at Mt. Pyre -- so renaming only the battle nameplate would leave the
dialogue calling them something else. HALVES maps each half, and the rename runs
through the map scripts, the trainer text, the match-call strings in
src/strings.c and the three renderers that anchor on a speaker prefix.

  --check   report what would be renamed
  --write   rewrite src/data/trainers.h, the text that speaks a name, the roster
"""
from __future__ import annotations

import argparse
import collections
import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# The reset-to-vanilla commit: anything still matching it was never renamed.
VANILLA = "c210195e"
TRAINERS = ROOT / "src/data/trainers.h"
RENDERERS = ROOT / "scripts/english_renderers.txt"
ROSTER = ROOT / "docs/arauna/ARAUNA_TRAINER_NAMES.csv"

NAME_LIMIT = 10  # TRAINER_NAME_LENGTH

WOMEN = """
ADRIANA ALICE ALZIRA AMANDA AMELIA ANDREIA ANGELA ANITA AURORA BEATRIZ BENEDITA
BERENICE BETANIA BIANCA BRUNA CAMILA CARLA CARMEM CAROL CASSIA CATARINA CECILIA
CELIA CIDA CILENE CINTIA CLARICE CLAUDIA CLEIDE CONSUELO CRISTINA DAIANE DALILA
DAMIANA DANIELA DARCI DEBORA DENISE DIANA DIRCE DOLORES DORA DULCE EDINA EDITE
ELAINE ELENA ELIANA ELISA ELOISA ELZA EMILIA ERICA ESTELA ESTER EUNICE EVA
FABIANA FATIMA FERNANDA FLAVIA FRANCISCA GABRIELA GENI GILDA GISELE GLAUCIA
GLORIA GRAZIELA HELENA HELOISA IEDA INES IOLANDA IRACEMA IRENE ISABEL ISADORA
IVANI IVONE JANDIRA JOANA JOSEFA JOVITA JULIA JULIANA JUREMA KARINA LARISSA
LAURA LEILA LENIRA LETICIA LIGIA LILIAN LUCIA LUCIANA LUIZA LURDES MADALENA
MAFALDA MAGDA MANUELA MARA MARCIA MARGARIDA MARIANA MARILDA MARINA MARLENE
MATILDE MILENA MIRIAM MONICA NADIA NAIR NATALIA NEIDE NELMA NEUSA NILDA NOEMIA
NORMA ODETE OLGA PALOMA PATRICIA PAULA PRISCILA RAIMUNDA REGINA RENATA ROSANA
ROSELI RUTE SANDRA SELMA SIMONE SOLANGE SONIA SUELI SUZANA TANIA TATIANA TELMA
TEREZA THAIS VALDIRENE VALERIA VANDA VANESSA VERA VILMA VIRGINIA VITORIA
VIVIANE WILMA YARA ZELIA ZILDA ZORAIDE ALDA AUREA BRIGIDA CIDINHA CLEUZA
DALVINA EDNA EULALIA GUIOMAR HORTENSIA IDALINA JACIRA LEONOR LINDALVA MARLI
NAZARE ONDINA PERPETUA QUITERIA ROSALIA SEVERINA TARSILA ULISSEIA VITALINA
"""

MEN = """
ABEL ADEMIR ADILSON ADRIANO AFONSO AILTON AIRTON ALBERTO ALCEU ALCIDES ALDO
ALFREDO ALOISIO ALVARO AMADEU AMILCAR ANDERSON ANIBAL ANSELMO ANTENOR ANTONIO
ARLINDO ARMANDO ARNALDO ARTUR AUGUSTO AURELIO BALTAZAR BASILIO BENEDITO BENICIO
BERNARDO BRAULIO BRUNO CAIO CAMILO CANDIDO CARLOS CASSIANO CELSO CESAR CICERO
CLAUDIO CLEBER CLOVIS CRISTIANO DANILO DARIO DAVI DEMETRIO DIEGO DIOGO DIONISIO
DJALMA DOMINGOS DONATO DORIVAL DOUGLAS DURVAL EDGAR EDILSON EDMUNDO EDNALDO
EDSON EDUARDO ELISEU EMILIANO EMILIO ENEAS ERASMO ERNANI ERNESTO EUCLIDES
EUGENIO EURICO EVANDRO EVARISTO EZEQUIEL FABIANO FABIO FAUSTO FELICIO FELIPE
FERNANDO FIRMINO FLAVIO FLORIANO FREDERICO GABRIEL GASPAR GENARO GERALDO GERSON
GETULIO GILBERTO GILDO GILSON GLAUCO GONCALO GUSTAVO HEITOR HELIO HENRIQUE
HERALDO HERMES HIGINO HILARIO HIPOLITO HORACIO HUGO HUMBERTO IGOR INACIO IRINEU
ISAIAS ISMAEL IVAN IVO JAIME JAIR JANUARIO JERONIMO JOAQUIM JORGE JOSE JOVINO
JUCA JULIO JURANDIR JUSTINO LAERTE LAURO LEANDRO LEONARDO LEONEL LINDOLFO LIVIO
LOURIVAL LUCAS LUCIANO LUIS LUIZ MANOEL MANUEL MARCELO MARCIO MARCOS MARIO
MARTIM MATEUS MAURICIO MAURO MAXIMO MIGUEL MILTON MOACIR MOISES MURILO NABOR
NELSON NESTOR NEWTON NICOLAU NILTON NIVALDO NOEL NORBERTO ODAIR ODILON OLAVO
OLEGARIO OLIVIO ORESTES ORLANDO OSCAR OSMAR OSVALDO OTAVIO OTONIEL PASCOAL
PATRICIO PAULO PEDRO PERCIVAL PLINIO PORFIRIO QUIRINO RAFAEL RAIMUNDO RAMIRO
REINALDO REMIGIO RENATO RICARDO ROBERTO RODOLFO RODRIGO ROGERIO ROLANDO ROMEU
ROMUALDO RONALDO ROQUE RUBENS RUI SAMUEL SANDRO SAULO SERAFIM SERGIO SEVERINO
SILAS SILVERIO SILVIO SIQUEIRA SOCRATES TARCISIO TEODORO TIAGO TIMOTEO TITO
TOBIAS TOMAS TULIO ULISSES URBANO VALDEMAR VALDIR VALENTIM VALERIO VICENTE
VIRGILIO VITOR VLADIMIR WAGNER WALDEMAR WALDIR WALTER WILSON XAVIER ZACARIAS
ABILIO AGENOR ALAOR ALIPIO ALTAIR AMANCIO AMERICO ANACLETO AQUILES ARNO ASSIS
ATILIO AVELINO BELMIRO BENJAMIM BERILO BRAZ CALIXTO CARMELO CELESTINO CIPRIANO
CLEMENTE CONRADO CUSTODIO DALTON DANTE DEODORO DIRCEU ERALDO EVALDO FABRICIO
FIDELIS FILINTO FORTUNATO GALDINO GERVASIO GILDASIO HAMILTON HELVECIO HERIBERTO
ILDO ISIDORO ITAMAR JACINTO JADIR JAMIL JARBAS JOEL JONAS JOSIAS JOVENAL
JUVENAL LADISLAU LEOCADIO LEOPOLDO LIBERATO LINDOMAR LISANDRO LOTARIO LUDGERO
MACARIO MAGNO MARCIANO MARIANO MATIAS MEDEIROS MODESTO NARCISO NATALINO
NAZARENO NELIO NEREU NICANOR OCTAVIO ODORICO OLIMPIO ONOFRE ORIVALDO OSEIAS
OSORIO OTELO PACIFICO PAULINO POMPEU PROSPERO QUINTINO REGIS RENAN RIVALDO
ROMARIO ROMILDO ROSALVO RUFINO SABINO SALVADOR SATURNO SIDNEI SOARES SOLANO
TEIXEIRA TELMO TEOFILO TIBERIO TRAJANO UBIRATAN VALFRIDO VIANA VITORINO
ZEFERINO
"""

# The seventeen tag-battle pairs are the one group whose names the player also
# reads in dialogue: each half introduces itself and calls the other by name, in
# map scripts, in the trainer text and on the PokeNav. So they are mapped half by
# half and the halves are rewritten wherever they are spoken. A pair name has to
# fit the same ten characters as anyone else's, and " & " eats three of them, so
# the two halves together have seven -- which is why these are short forms.
# Gender is kept: Ty and Luke are men, Jay and Dez are women.
HALVES = {
    "GABBY": "BIA",   "TY": "TITO",
    "KATE": "NEIA",   "JOY": "LU",
    "ANNA": "ANA",    "MEG": "DUDA",
    "AMY": "ANE",     "LIV": "VIVI",
    "GINA": "NINA",   "MIA": "GI",
    "MIU": "IZA",     "YUKI": "YARA",
    "DEZ": "LIA",     "LUKE": "LUCA",
    "LEA": "LEA",     "JED": "JAIR",
    "KIRA": "IARA",   "DAN": "TON",
    "TORI": "TINA",   "TIA": "MIA",
    "KIM": "LIS",     "IRIS": "IRIS",
    "TYRA": "TAIS",   "IVY": "IVA",
    "MEL": "MEL",     "PAUL": "SAUL",
    "JOHN": "NEI",    "JAY": "ADA",
    "RELI": "NELI",   "IAN": "IAN",
    "LILA": "LILA",   "ROY": "RUI",
    "LISA": "LISA",   "RAY": "RAI",
}

# Where a half is spoken. Every hit in these files is a name -- either a
# "NAME:" speaker prefix or one half naming the other -- which is why a plain
# word-boundary rewrite is safe here and would not be repo-wide: "RAY" is also
# a move name and "JOY" an easy-chat word, both outside this list.
def text_files() -> list[Path]:
    tracked = subprocess.run(["git", "ls-files", "data"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.split()
    return ([ROOT / f for f in tracked if f.endswith((".inc", ".s"))]
            + [ROOT / "src/strings.c"]          # the PokeNav match-call names
            # Three renderers anchor on a half's speaker prefix and put it back
            # in the English text they write. Rewriting the base without them
            # would leave the anchors matching nothing.
            + [ROOT / "scripts/render_memorial_lower_floors_en.py",
               ROOT / "scripts/render_porto_sal_daily_life.py",
               ROOT / "scripts/render_porto_sal_submersivel.py"])


def at_vanilla() -> str:
    return subprocess.run(["git", "show", f"{VANILLA}:src/data/trainers.h"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout


def entries(text: str) -> dict[str, tuple[str, bool]]:
    out = {}
    for block in re.finditer(r"\[(TRAINER_\w+)\] =\s*\{(.*?)\n    \},", text, re.S):
        name = re.search(r'\.trainerName = _\("([^"]*)"\)', block.group(2))
        gender = re.search(r"\.encounterMusic_gender = ([^,\n]*)", block.group(2))
        out[block.group(1)] = (name.group(1) if name else "",
                               "F_TRAINER_FEMALE" in (gender.group(1) if gender else ""))
    return out


def renderer_owned(current: str) -> set[str]:
    """Entries some English renderer rewrites; they are not ours to rename.

    Found by running them and seeing which names moved, then throwing the
    result away -- which means `git checkout -- data src`, so uncommitted work
    under those trees would go with it. Hence the guard.
    """
    dirty = subprocess.run(["git", "status", "--porcelain", "data", "src"], cwd=ROOT,
                           capture_output=True, text=True, check=True).stdout.strip()
    if dirty:
        raise SystemExit("commit or stash data/ and src/ first: this pass runs the "
                         "renderers and reverts them afterwards.\n" + dirty)
    before = entries(current)
    saved = TRAINERS.read_text(encoding="utf-8")
    try:
        for line in RENDERERS.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                subprocess.run([sys.executable, f"scripts/{line}", "--in-place"],
                               cwd=ROOT, capture_output=True)
        after = entries(TRAINERS.read_text(encoding="utf-8"))
    finally:
        subprocess.run(["git", "checkout", "--", "data", "src"], cwd=ROOT,
                       capture_output=True)
        TRAINERS.write_text(saved, encoding="utf-8")
    return {key for key in after if before.get(key, ("", False))[0] != after[key][0]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    current = TRAINERS.read_text(encoding="utf-8")
    vanilla = entries(at_vanilla())
    now = entries(current)
    owned = renderer_owned(current)

    # Still carrying the name the vanilla game gave it, and nobody else's to change.
    # TRAINER_NONE has no name at all and is not a person; leave it empty.
    todo = {key: value for key, value in now.items()
            if key not in owned and key in vanilla and vanilla[key][0] == value[0]
            and value[0]}

    gendered: dict[str, bool] = {}
    for _, (name, female) in todo.items():
        gendered[name] = gendered.get(name, False) or female

    pairs = {name: " & ".join(HALVES[half] for half in name.split(" & "))
             for name in gendered if " & " in name}
    unknown = sorted(half for name in gendered if " & " in name
                     for half in name.split(" & ") if half not in HALVES)

    women = WOMEN.split()
    men = MEN.split()
    taken = ({value[0] for key, value in now.items() if key not in todo}
             | set(HALVES.values()))
    mapping, exhausted = {}, []
    for name in sorted(gendered):
        if name in pairs:
            mapping[name] = pairs[name]
            continue
        pool = women if gendered[name] else men
        pick = next((candidate for candidate in pool
                     if candidate not in taken and candidate not in mapping.values()), None)
        if pick is None:
            exhausted.append(name)
            continue
        mapping[name] = pick

    over = [n for n in mapping.values() if len(n) > NAME_LIMIT]
    clashes = sorted(n for n, c in collections.Counter(mapping.values()).items() if c > 1)
    halves = {old: new for old, new in HALVES.items()
              for name in pairs if old in name.split(" & ")}
    spoken = [path for path in text_files()
              if re.search(r"(?<![A-Za-z_])(" + "|".join(halves) + r")(?![A-Za-z_])",
                           path.read_text(encoding="utf-8", errors="replace"))] if halves else []

    print(f"{len(todo)} entries still carry a vanilla name, {len(gendered)} distinct")
    print(f"  renamed: {len(mapping)}   pool exhausted for: {len(exhausted)} {exhausted[:5]}")
    print(f"  over {NAME_LIMIT} characters: {len(over)} {over[:5]}")
    print(f"  two people given the same name: {len(clashes)} {clashes[:5]}")
    print(f"  halves without a mapping: {len(unknown)} {unknown[:5]}")
    print(f"  left to their renderer: {len(owned)} entries")
    print(f"  {len(pairs)} tag pairs, their halves spoken in {len(spoken)} files")
    for name in sorted(mapping)[:6]:
        print(f"   {name:12} -> {mapping[name]}")

    if exhausted or over or clashes or unknown:
        print("refusing: fix the pools first", file=sys.stderr)
        return 1
    if not mapping:
        # Everyone has already been renamed. Say so and leave the roster alone
        # rather than rewriting it as an empty file.
        print("nothing left carrying a vanilla name")
        return 0
    if not args.write:
        return 0

    def swap(match):
        name = match.group(1)
        return f'.trainerName = _("{mapping.get(name, name)}")'

    # Only rewrite inside the entries we own, so a name shared with a renderer
    # entry is not caught by accident.
    def per_entry(block):
        if block.group(1) not in todo:
            return block.group(0)
        return re.sub(r'\.trainerName = _\("([^"]*)"\)', swap, block.group(0))

    updated = re.sub(r"\[(TRAINER_\w+)\] =\s*\{.*?\n    \},", per_entry, current, flags=re.S)
    TRAINERS.write_text(updated, encoding="utf-8")

    # All halves at once: TIA becomes MIA and MIA becomes GI, so replacing them
    # one after another would run the first result through the second rule.
    if halves:
        spoken_pattern = re.compile(r"(?<![A-Za-z_])(" + "|".join(halves) + r")(?![A-Za-z_])")
        for path in spoken:
            body = path.read_text(encoding="utf-8")
            path.write_text(spoken_pattern.sub(lambda m: halves[m.group(1)], body),
                            encoding="utf-8")

    with ROSTER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["vanilla_name", "gender", "arauna_name", "entries"])
        for name in sorted(mapping):
            count = sum(1 for value in todo.values() if value[0] == name)
            # A pair entry carries no female flag of its own; each half keeps
            # the gender it had, which HALVES records rather than this column.
            gender = "pair" if name in pairs else ("F" if gendered[name] else "M")
            writer.writerow([name, gender, mapping[name], count])
    print(f"\nwrote {TRAINERS.relative_to(ROOT)}, {ROSTER.relative_to(ROOT)} "
          f"and {len(spoken)} files where a pair is spoken")
    return 0


if __name__ == "__main__":
    sys.exit(main())
