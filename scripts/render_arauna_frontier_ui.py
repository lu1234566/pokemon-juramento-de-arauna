#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "src" / "strings.c"


def decl(name: str, value: str) -> str:
    return f'const u8 {name}[] = _("{value}");'


def multiline_decl(name: str, first: str, second: str) -> str:
    return f'const u8 {name}[] = _("{first}\\\n{second}");'


REPLACEMENTS = (
    (decl("gText_SymbolsEarned", "Symbols Earned"), decl("gText_SymbolsEarned", "SIMBOLOS")),
    (decl("gText_BattleRecord", "Battle Record"), decl("gText_BattleRecord", "REG. BATALHA")),
    (decl("gText_BattlePoints", "Battle Points"), decl("gText_BattlePoints", "PONTOS DE BATALHA")),
    (decl("gText_CheckFrontierMap", "Check BATTLE FRONTIER MAP."), decl("gText_CheckFrontierMap", "Ver mapa do CIRCUITO.")),
    (decl("gText_CheckTrainerCard", "Check TRAINER CARD."), decl("gText_CheckTrainerCard", "Ver CARTAO DE TREINADOR.")),
    (decl("gText_ViewRecordedBattle", "View recorded battle."), decl("gText_ViewRecordedBattle", "Ver batalha registrada.")),
    (decl("gText_PutAwayFrontierPass", "Put away the FRONTIER PASS."), decl("gText_PutAwayFrontierPass", "Guardar PASSE DO CIRCUITO.")),
    (decl("gText_CurrentBattlePoints", "Your current Battle Points."), decl("gText_CurrentBattlePoints", "Seus Pontos de Batalha.")),
    (decl("gText_CollectedSymbols", "Your collected Symbols."), decl("gText_CollectedSymbols", "Seus SIMBOLOS obtidos.")),
    (decl("gText_BattleTowerAbilitySymbol", "Battle Tower - Ability Symbol"), decl("gText_BattleTowerAbilitySymbol", "BATTLE TOWER - SIMB. TALENTO")),
    (decl("gText_BattleDomeTacticsSymbol", "Battle Dome - Tactics Symbol"), decl("gText_BattleDomeTacticsSymbol", "BATTLE DOME - SIMB. TATICA")),
    (decl("gText_BattlePalaceSpiritsSymbol", "Battle Palace - Spirits Symbol"), decl("gText_BattlePalaceSpiritsSymbol", "BATTLE PALACE - SIMB. ESPIRITO")),
    (decl("gText_BattleArenaGutsSymbol", "Battle Arena - Guts Symbol"), decl("gText_BattleArenaGutsSymbol", "BATTLE ARENA - SIMB. GARRA")),
    (decl("gText_BattleFactoryKnowledgeSymbol", "Battle Factory - Knowledge Symbol"), decl("gText_BattleFactoryKnowledgeSymbol", "BATTLE FACTORY - CONHECIMENTO")),
    (decl("gText_BattlePikeLuckSymbol", "Battle Pike - Luck Symbol"), decl("gText_BattlePikeLuckSymbol", "BATTLE PIKE - SIMB. SORTE")),
    (decl("gText_BattlePyramidBraveSymbol", "Battle Pyramid - Brave Symbol"), decl("gText_BattlePyramidBraveSymbol", "BATTLE PYRAMID - SIMB. BRAVURA")),
    (decl("gText_ThereIsNoBattleRecord", "There is no Battle Record."), decl("gText_ThereIsNoBattleRecord", "Nao ha batalha registrada.")),
    (multiline_decl("gText_BattleTowerDesc", "KO opponents and aim for the top!", "Your ability will be tested."), multiline_decl("gText_BattleTowerDesc", "Venca em sequencia e va ao topo!", "Seu talento sera testado.")),
    (multiline_decl("gText_BattleDomeDesc", "Keep winning at the tournament!", "Your tactics will be tested."), multiline_decl("gText_BattleDomeDesc", "Venca torneios sem parar!", "Sua tatica sera testada.")),
    (multiline_decl("gText_BattlePalaceDesc", "Watch your POKéMON battle!", "Your spirit will be tested."), multiline_decl("gText_BattlePalaceDesc", "Observe seus POKéMON lutarem!", "Seu espirito sera testado.")),
    (multiline_decl("gText_BattleArenaDesc", "Win battles with teamed-up POKéMON!", "Your guts will be tested."), multiline_decl("gText_BattleArenaDesc", "Venca em poucos turnos!", "Sua garra sera testada.")),
    (multiline_decl("gText_BattleFactoryDesc", "Aim for victory using rental POKéMON!", "Your knowledge will be tested."), multiline_decl("gText_BattleFactoryDesc", "Lute com POKéMON emprestados!", "Seu conhecimento sera testado.")),
    (multiline_decl("gText_BattlePikeDesc", "Select one of three paths to battle!", "Your luck will be tested."), multiline_decl("gText_BattlePikeDesc", "Escolha um de tres caminhos!", "Sua sorte sera testada.")),
    (multiline_decl("gText_BattlePyramidDesc", "Aim for the top with exploration!", "Your bravery will be tested."), multiline_decl("gText_BattlePyramidDesc", "Explore e alcance o topo!", "Sua bravura sera testada.")),
    (decl("gText_BattlePtsWon", "BATTLE POINTS WON"), decl("gText_BattlePtsWon", "PONTOS DE BATALHA")),
    (decl("gText_NumBP", "{STR_VAR_1}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}BP"), decl("gText_NumBP", "{STR_VAR_1}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}PB")),
    (decl("gText_BattleFrontier", "BATTLE FRONTIER"), decl("gText_BattleFrontier", "CIRCUITO DE BATALHA")),
)


def render(source: str) -> str:
    rendered = source
    for old, new in REPLACEMENTS:
        count = rendered.count(old)
        if count != 1:
            raise ValueError(f"expected exactly one source anchor, found {count}: {old[:90]}")
        rendered = rendered.replace(old, new, 1)
    return rendered


def validate_rendered(rendered: str) -> None:
    for old, new in REPLACEMENTS:
        if new not in rendered:
            raise ValueError(f"missing rendered target: {new[:90]}")
        if old != new and old in rendered:
            raise ValueError(f"legacy target survived rendering: {old[:90]}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the non-art Battle Frontier UI surface as Arauna's Circuito de Batalha.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.output and args.in_place:
        parser.error("use either --output or --in-place, not both")

    source = args.input.read_text(encoding="utf-8")
    rendered = render(source)
    validate_rendered(rendered)

    if args.check:
        print(f"Circuito UI renderer OK: {len(REPLACEMENTS)} exact replacements validated.")
        return 0

    if args.in_place:
        args.input.write_text(rendered, encoding="utf-8")
    elif args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
