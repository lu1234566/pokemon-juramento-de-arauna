# Pokémon: Juramento de Arauna

ROM hack bilíngue de Pokémon Emerald ambientada em uma região original inspirada no sul do Brasil. O projeto combina fantasia sombria, investigação, batalhas planejadas e escolhas narrativas por meio do Sistema de Vínculos.

> Estado atual: pré-produção, fundação técnica validada e primeiro protótipo bilíngue em desenvolvimento. Ainda não há uma versão pública jogável.

## Visão

- Português brasileiro e inglês a partir do mesmo código-fonte.
- Narrativa madura e sombria, sem violência gráfica gratuita.
- Protagonista com personalidade, falas e escolhas.
- Três linhas de iniciais completamente originais.
- Região de Arauna, com florestas de araucárias, neblina, serras, ruínas e centros tecnológicos.
- Vínculos de Coragem, Sabedoria e Compaixão com consequências narrativas.

O primeiro objetivo jogável é um vertical slice de 30 a 60 minutos com uma vila, uma rota, uma ruína, a escolha do inicial, o rival, uma decisão de Vínculo e um miniboss.

## Documentação do projeto

- [Documento de design](project/GDD.md)
- [Roadmap](project/ROADMAP.md)
- [Decisões técnicas e criativas](project/DECISIONS.md)
- [Sinopse](project/story/SYNOPSIS.md)
- [Região de Arauna](project/world/REGION.md)
- [Trio de iniciais](project/design/STARTERS.md)
- [Sistema de Vínculos](project/design/BOND_SYSTEM.md)
- [Arquitetura bilíngue](project/design/LOCALIZATION.md)
- [Plano de testes](project/testing/TEST_PLAN.md)
- [Fontes e licenças de assets](project/credits/ASSET_SOURCES.md)

## Base técnica

Este projeto parte de [`rh-hideout/pokeemerald-expansion`](https://github.com/rh-hideout/pokeemerald-expansion), versão `expansion/1.16.2`, commit `ad0fd4d17f546ca6fd8d785c8724f9382e6e9382`.

O histórico upstream foi preservado. O remoto `upstream` deve continuar apontando para o projeto oficial; atualizações serão avaliadas em branches próprias e nunca incorporadas diretamente na `main` sem build e testes.

## Desenvolvimento

Dependências e instruções de compilação continuam documentadas no [INSTALL.md](INSTALL.md) original. Depois de preparar o ambiente:

```bash
make ARAUNA_LANGUAGE=PORTUGUESE -j$(nproc)
make ARAUNA_LANGUAGE=ENGLISH -j$(nproc)
```

Os comandos geram, respectivamente, `pokeemerald-ptbr.gba` e `pokeemerald-en.gba` em diretórios de build separados. A CI compila os dois idiomas e executa os testes oficiais em inglês sem publicar nenhuma ROM como artefato.

Valide os textos localizados antes de compilar:

```bash
python3 scripts/check_localization.py
```

### Branches

- `main`: estado estável e compilável.
- `agent/*`: implementação assistida.
- `feature/*`: funcionalidades e conteúdo.
- `fix/*`: correções.

## Segurança e distribuição

ROMs comerciais, builds `.gba`, saves, credenciais e patches não devem ser commitados. Execute antes de cada commit:

```bash
bash scripts/check_no_proprietary_files.sh
```

Quando existir uma versão distribuível, serão gerados patches separados para `pt-BR` e `en`. Nenhuma ROM completa será publicada.

## Créditos

Baseado em RHH's `pokeemerald-expansion` 1.16.2. Os créditos originais do motor estão preservados em [CREDITS.md](CREDITS.md). Novos recursos devem ser registrados em [project/credits/ASSET_SOURCES.md](project/credits/ASSET_SOURCES.md) antes da integração.

Pokémon e suas marcas pertencem aos respectivos detentores. Este é um projeto de fã, não oficial, sem afiliação com Nintendo, Game Freak ou The Pokémon Company.
