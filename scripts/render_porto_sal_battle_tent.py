#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS = {'data/text/battle_tent.inc': {'SlateportCity_BattleTentLobby_Text_WelcomeToBattleTent': [['Bem-vindo a TENDA DE BATALHA', 'de PORTO DO SAL!'], ['Aqui acontece o DESAFIO DE TROCA', 'com POKéMON alugados.']], 'SlateportCity_BattleTentLobby_Text_TakeChallenge': [['Quer participar do DESAFIO', 'DE TROCA?']], 'SlateportCity_BattleTentLobby_Text_ExplainSlateportTent': [['Na TENDA DE BATALHA daqui,', 'voce usa tres POKéMON alugados.'], ['Cada confronto e uma BATALHA', 'INDIVIDUAL.'], ['Se vencer, pode trocar um dos', 'seus POKéMON por um do rival.'], ['Venca tres batalhas seguidas', 'para receber um premio.'], ['Se quiser interromper o desafio,', 'salve o jogo antes de sair.'], ['Sem salvar, o desafio sera', 'encerrado.']], 'SlateportCity_BattleTentLobby_Text_LookForwardToNextVisit': [['Esperamos voce numa proxima vez!']], 'SlateportCity_BattleTentLobby_Text_SaveBeforeChallenge': [['Antes do desafio, preciso salvar', 'os dados. Tudo bem?']], 'SlateportCity_BattleTentLobby_Text_StepThisWay': [['Por aqui, por favor.']], 'SlateportCity_BattleTentLobby_Text_ReturnRentalMonsSaveResults': [['Obrigado por participar!'], ['Vou devolver seus POKéMON e', 'recolher os alugados.'], ['Tambem vou salvar o resultado.', 'Um momento, por favor.']], 'SlateportCity_BattleTentLobby_Text_WonThreeMatchesReturnMons': [['Parabens!', 'Voce venceu tres batalhas!'], ['Vou devolver seus POKéMON e', 'recolher os alugados.'], ['Tambem vou salvar o resultado.', 'Um momento, por favor.']], 'SlateportCity_BattleTentLobby_Text_AwardYouThisPrize': [['Pelas tres vitorias seguidas,', 'receba este premio.']], 'SlateportCity_BattleTentLobby_Text_NoRoomInBagMakeRoom': [['Ah!', 'Nao ha espaco na sua BOLSA.'], ['Abra espaco e fale comigo', 'novamente.']], 'SlateportCity_BattleTentLobby_Text_BeenWaitingForYou': [['Estavamos esperando por voce!'], ['Antes de retomar o desafio,', 'preciso salvar o jogo.']], 'SlateportCity_BattleTentLobby_Text_DidntSaveBeforeQuitting': [['Voce saiu sem salvar o desafio', 'da ultima vez.'], ['Por isso, aquela tentativa foi', 'encerrada.']], 'SlateportCity_BattleTentLobby_Text_ExplainBasicRules': [['No DESAFIO DE TROCA, voce usa', 'somente tres POKéMON.'], ['Na equipe, nao pode haver dois', 'POKéMON da mesma especie.']], 'SlateportCity_BattleTentLobby_Text_ExplainSwapPartnerRules': [['Voce so pode trocar POKéMON com', 'o treinador que voce venceu.'], ['Escolha entre os POKéMON usados', 'por esse treinador.']], 'SlateportCity_BattleTentLobby_Text_ExplainSwapNumberRules': [['Apos cada vitoria, voce pode', 'trocar um POKéMON pelo do rival.'], ['Nao ha troca depois da terceira', 'batalha do desafio.']], 'SlateportCity_BattleTentLobby_Text_ExplainSwapNotes': [['Duas regras importam nas trocas.'], ['Primeiro: antes de escolher,', 'nao e possivel ver os atributos'], ['do POKéMON que vai receber.'], ['Segundo: a ordem da equipe segue', 'a ordem original do aluguel.'], ['Trocas nao alteram essa ordem.']], 'SlateportCity_BattleTentLobby_Text_ExplainMonRules': [['Todos os POKéMON desta TENDA', 'sao alugados.'], ['Todos entram no Nivel 30.']]}, 'data/maps/SlateportCity_BattleTentLobby/scripts.inc': {'SlateportCity_BattleTentLobby_Text_CouldntFindMonForMe': [['Eu nao achei nenhum POKéMON que', 'combinasse comigo.'], ['Reclamei, mas nao me ouviram.', 'Que azar...'], ['Ei, voce! Fique com isto!']], 'SlateportCity_BattleTentLobby_Text_ExplainTorment': [['Essa e a TM41: TORMENT.'], ['Ela impede o alvo de repetir', 'o mesmo golpe logo em seguida.'], ['Nao quero atormentar voce!']], 'SlateportCity_BattleTentLobby_Text_IllTryUsingBugMons': [['Nao costumo usar POKéMON INSETO,', 'mas talvez eu tente alguns hoje.'], ['Quem sabe eu acabe gostando?']], 'SlateportCity_BattleTentLobby_Text_BattleEvenWithoutToughMons': [['Aqui da para batalhar mesmo sem', 'trazer POKéMON fortes de casa.']], 'SlateportCity_BattleTentLobby_Text_NiceIfMoreSelection': [['Seria bom ter ainda mais POKéMON', 'para escolher.']]}, 'data/maps/BattleFrontier_BattleFactoryPreBattleRoom/scripts.inc': {'BattleFrontier_BattleFactoryPreBattleRoom_Text_HoldMonsChooseFromSelection': [['Primeiro, guardamos sua equipe.'], ['Depois, escolha tres POKéMON', 'entre os nossos alugados.']], 'BattleFrontier_BattleFactoryPreBattleRoom_Text_LetUsRestoreMons': [['Obrigado por competir!', 'Vamos restaurar seus POKéMON.']], 'BattleFrontier_BattleFactoryPreBattleRoom_Text_ReadyFor2ndOpponent': [['A segunda batalha vem agora!', 'Esta pronto?']], 'BattleFrontier_BattleFactoryPreBattleRoom_Text_ReadyFor3rdOpponent': [['A terceira batalha vem agora!', 'Esta pronto?']], 'BattleFrontier_BattleFactoryPreBattleRoom_Text_SaveAndQuitGame': [['Deseja salvar e pausar agora?']], 'BattleFrontier_BattleFactoryPreBattleRoom_Text_RetireFromChallenge': [['Deseja desistir do DESAFIO', 'DE TROCA?']], 'BattleFrontier_BattleFactoryPreBattleRoom_Text_LikeToSwapMon': [['Antes da batalha, quer trocar', 'um POKéMON?']], 'BattleFrontier_BattleFactoryPreBattleRoom_Text_YourSwapIsComplete': [['Obrigado!', 'A troca de POKéMON terminou.']], 'BattleFrontier_BattleFactoryPreBattleRoom_Text_RightThisWay': [['Por aqui, por favor.']], 'BattleFrontier_BattleFactoryPreBattleRoom_Text_SavingDataPleaseWait': [['Salvando seus dados.', 'Um momento, por favor.']]}, 'data/maps/BattleFrontier_BattleFactoryLobby/scripts.inc': {'BattleFrontier_BattleFactoryLobby_Text_RulesAreListed': [['As regras de TROCA estao aqui.']], 'BattleFrontier_BattleFactoryLobby_Text_ReadWhichHeading': [['Qual parte deseja consultar?']]}, 'data/maps/BattleFrontier_BattleTowerLobby/scripts.inc': {'BattleFrontier_BattleTowerLobby_Text_ReceivedPrize': [['{PLAYER} recebeu o premio', '{STR_VAR_1}.']]}}

C_TARGETS = {'gText_Challenge': ('CHALLENGE', 'DESAFIO'), 'gText_Exit': ('EXIT', 'SAIR'), 'gText_BasicRules': ('BASIC RULES', 'REGRAS BASICAS'), 'gText_SwapPartners': ('SWAP: PARTNER', 'TROCA: RIVAL'), 'gText_SwapNumber': ('SWAP: NUMBER', 'TROCA: NUMERO'), 'gText_SwapNotes': ('SWAP: NOTES', 'TROCA: NOTAS'), 'gText_BattlePokemon': ('BATTLE POKéMON', 'POKéMON DA TENDA'), 'gText_GoOn': ('GO ON', 'CONTINUAR'), 'gText_Rest': ('REST', 'PAUSAR'), 'gText_Retire': ('RETIRE', 'DESISTIR')}

STRING_BLOCK_RE_TEMPLATE = r"(?m)^{label}:\n(?:\t\.string .*\n)+"
C_DECL_TEMPLATE = 'const u8 {name}[] = _("{value}");'


def make_block(label: str, pages: list[list[str]]) -> str:
    lines = [f"{label}:"]
    for page_index, page in enumerate(pages):
        if not page or len(page) > 2:
            raise ValueError(f"{label}: each page must contain one or two lines")
        for line_index, text in enumerate(page):
            if len(text) > 32:
                raise ValueError(f"{label}: line exceeds 32 chars ({len(text)}): {text}")
            is_last_line = line_index == len(page) - 1
            is_last_page = page_index == len(pages) - 1
            if not is_last_line:
                suffix = r"\n"
            elif not is_last_page:
                suffix = r"\p"
            else:
                suffix = "$"
            lines.append(f'\t.string "{text}{suffix}"')
    return "\n".join(lines) + "\n"


def render_asm(path: Path, source: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    targets = TARGETS.get(rel)
    if not targets:
        return source
    rendered = source
    for label, pages in targets.items():
        pattern = re.compile(STRING_BLOCK_RE_TEMPLATE.format(label=re.escape(label)))
        replacement = make_block(label, pages)
        rendered, count = pattern.subn(lambda _: replacement, rendered, count=1)
        if count != 1:
            raise ValueError(f"{rel}: expected exactly one block for {label}, found {count}")
    return rendered


def render_strings(source: str) -> str:
    rendered = source
    for name, (old_value, new_value) in C_TARGETS.items():
        old = C_DECL_TEMPLATE.format(name=name, value=old_value)
        new = C_DECL_TEMPLATE.format(name=name, value=new_value)
        count = rendered.count(old)
        if count != 1:
            raise ValueError(f"src/strings.c: expected exactly one declaration for {name}, found {count}")
        rendered = rendered.replace(old, new, 1)
    return rendered


def mask_asm(source: str) -> str:
    return re.sub(r"(?m)^\t\.string .*\n", "", source)


def validate_structure(path: Path, source: str, rendered: str) -> None:
    if mask_asm(source) != mask_asm(rendered):
        raise ValueError(f"{path.relative_to(ROOT)}: non-text structure changed")


def validate_rendered() -> None:
    for rel in TARGETS:
        path = ROOT / rel
        source = path.read_text(encoding="utf-8")
        rendered = render_asm(path, source)
        validate_structure(path, source, rendered)
        for label, block_pages in TARGETS[rel].items():
            expected = make_block(label, block_pages)
            if expected not in rendered:
                raise ValueError(f"{rel}: rendered block missing for {label}")

    strings_path = ROOT / "src" / "strings.c"
    strings_source = strings_path.read_text(encoding="utf-8")
    strings_rendered = render_strings(strings_source)
    for name, (_, new_value) in C_TARGETS.items():
        expected = C_DECL_TEMPLATE.format(name=name, value=new_value)
        if expected not in strings_rendered:
            raise ValueError(f"src/strings.c: rendered declaration missing for {name}")


def apply_in_place() -> None:
    for rel in TARGETS:
        path = ROOT / rel
        source = path.read_text(encoding="utf-8")
        rendered = render_asm(path, source)
        validate_structure(path, source, rendered)
        path.write_text(rendered, encoding="utf-8")

    strings_path = ROOT / "src" / "strings.c"
    strings_path.write_text(render_strings(strings_path.read_text(encoding="utf-8")), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Porto do Sal Battle Tent and its shared rental/swap UI in PT-BR.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()

    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    validate_rendered()
    if args.in_place:
        apply_in_place()
        print(f"Porto do Sal Battle Tent renderer applied: {sum(len(v) for v in TARGETS.values())} blocks + {len(C_TARGETS)} UI strings.")
    else:
        print(f"Porto do Sal Battle Tent renderer OK: {sum(len(v) for v in TARGETS.values())} blocks + {len(C_TARGETS)} UI strings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
