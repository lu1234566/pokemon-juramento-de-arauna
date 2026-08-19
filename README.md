# Pokémon Juramento de Arauna

ROM hack de Pokémon Emerald em desenvolvimento, ambientada em Arauna e construída sobre a decompilação do `pokeemerald`.

## Direção atual

A implementação preserva o esqueleto técnico do Emerald — grafo de eventos, ordem de progressão, warps, flags e identificadores internos — e substitui a superfície visível pelo cânone de Arauna. Essa abordagem reduz risco de regressão em saves e progressão enquanto permite reescrever mapas, diálogos, personagens e identidade do mundo.

O núcleo narrativo atual está documentado em [`docs/ARAUANA_STORY_IMPLEMENTATION.md`](docs/ARAUANA_STORY_IMPLEMENTATION.md). Entre os elementos já integrados estão o Desencanto, o Arquivo Vivo, o Consórcio Horizonte, os Lembrantes, Professora Anahi, Dona Zila, Ciro e a linha principal ligada a M'Boi.

## Validação

A CI possui duas frentes:

1. **Arauna static validation** — executa os validadores de resíduos visíveis do Emerald e o contrato da introdução bilíngue;
2. **Build Arauna (intro ptbr/en)** — tenta compilar duas variantes da introdução a partir do mesmo commit, em diretórios isolados.

Os validadores existem para impedir que nomes, falas e identidades antigas do Emerald reapareçam acidentalmente em superfícies já convertidas para Arauna.

## Build local

Depois de preparar as dependências descritas em [`INSTALL.md`](INSTALL.md), a build padrão continua em português na introdução:

```bash
make MODERN=1 -j2 all
```

Para testar explicitamente as duas variantes da introdução:

```bash
bash scripts/build_arauna.sh ptbr -j2 all
bash scripts/build_arauna.sh en -j2 all
```

A arquitetura e as limitações desse protótipo estão em [`docs/LOCALIZATION_CURRENT_STATE_2026_08_19.md`](docs/LOCALIZATION_CURRENT_STATE_2026_08_19.md). **A variante `en` ainda não representa uma tradução completa do jogo**; neste estágio, a seleção bilíngue cobre a introdução de Anahi.

As ROMs geradas são apenas artefatos locais de desenvolvimento e não devem ser versionadas no repositório.

## Regras de integração

- preservar IDs internos do Emerald quando a mudança for apenas de superfície;
- não alterar flags, warps, progressão ou formato de save sem uma decisão técnica explícita;
- preferir alterações pequenas e auditáveis;
- manter arte final separada de mudanças puramente técnicas quando possível;
- validar resíduos narrativos antes do merge.

## Estado

O projeto já possui uma grande passagem narrativa sobre mapas da campanha e continua em integração, limpeza de resíduos, localização incremental, revisão visual e testes. Não há lançamento público final neste momento.
