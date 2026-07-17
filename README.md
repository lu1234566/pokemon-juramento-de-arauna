# Pokémon: Juramento de Arauna

ROM hack bilíngue de Pokémon Emerald ambientada em uma região original inspirada em todo o Brasil e organizada por biomas. O projeto combina fantasia sombria, investigação, batalhas planejadas, escolhas narrativas e uma Pokédex autoral de 386 espécies.

> Estado atual: versão definitiva em pré-produção. A fundação técnica bilíngue e o primeiro vertical slice existem, mas a direção de mundo, Pokédex e arte está sendo realinhada para o novo escopo.

## Visão

- Português brasileiro e inglês a partir do mesmo código-fonte.
- Narrativa madura e sombria, sem violência gráfica gratuita.
- Protagonista com personalidade, falas e escolhas.
- Região de Arauna inspirada em todo o Brasil, com biomas ficcionais conectados.
- 386 espécies de Arauna substituindo os 386 slots da Pokédex do Emerald.
- Trio inicial original: cachorro caramelo de Fogo, quero-quero de Água e pica-pau brasileiro de Planta.
- Vínculos de Coragem, Sabedoria e Compaixão com consequências narrativas.
- Direção visual compatível com o GBA e legível como Pokémon Emerald, sem copiar mapas de Hoenn.

O primeiro objetivo continua sendo um vertical slice de 30 a 60 minutos. Ele será reconstruído como prova de qualidade da versão definitiva antes da produção em massa da região e da Pokédex.

## Documentação do projeto

- [Documento de design](project/GDD.md)
- [Roadmap](project/ROADMAP.md)
- [Decisões técnicas e criativas](project/DECISIONS.md)
- [Sinopse](project/story/SYNOPSIS.md)
- [Região de Arauna](project/world/REGION.md)
- [Plano da Pokédex de 386 espécies](project/design/POKEDEX_386.md)
- [Trio de iniciais](project/design/STARTERS.md)
- [Protocolo de aprovação de sprites](project/art/SPRITE_APPROVAL.md)
- [Sistema de Vínculos](project/design/BOND_SYSTEM.md)
- [Arquitetura bilíngue](project/design/LOCALIZATION.md)
- [Plano de testes](project/testing/TEST_PLAN.md)
- [Fontes e licenças de assets](project/credits/ASSET_SOURCES.md)

## Base técnica

Este projeto parte de [`rh-hideout/pokeemerald-expansion`](https://github.com/rh-hideout/pokeemerald-expansion), versão `expansion/1.16.2`, commit `ad0fd4d17f546ca6fd8d785c8724f9382e6e9382`.

O histórico upstream permanece preservado. Atualizações do motor serão avaliadas em branches próprias e nunca incorporadas diretamente na `main` sem build e testes.

## Desenvolvimento

Depois de preparar o ambiente conforme o [INSTALL.md](INSTALL.md):

```bash
make ARAUNA_LANGUAGE=PORTUGUESE -j$(nproc)
make ARAUNA_LANGUAGE=ENGLISH -j$(nproc)
python3 scripts/check_localization.py
```

Os builds `pt-BR` e `en` são gerados da mesma fonte. A CI compila os dois idiomas e executa os testes sem publicar ROMs.

### Regra de arte

Nenhum sprite novo ou modificado pode entrar no jogo antes de existir uma prévia identificada e uma aprovação explícita de Lucas Barcelar. A aprovação de conceito não equivale automaticamente à aprovação do sprite final.

## Segurança e distribuição

ROMs comerciais, builds `.gba`, saves e credenciais não serão commitados. A ROM limpa fornecida pelo proprietário é usada apenas localmente como base de compilação. Lançamentos públicos conterão somente código permitido, documentação e patches separados para `pt-BR` e `en`.

Pokémon e suas marcas pertencem aos respectivos detentores. Este é um projeto de fã, não oficial, sem afiliação com Nintendo, Game Freak ou The Pokémon Company.
