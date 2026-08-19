# Pokémon Juramento de Arauna

ROM hack de Pokémon Emerald em desenvolvimento, ambientada em Arauna e construída sobre a decompilação do `pokeemerald`.

## Direção atual

A implementação preserva o esqueleto técnico do Emerald — grafo de eventos, ordem de progressão, warps, flags e identificadores internos — e substitui a superfície visível pelo cânone de Arauna. Essa abordagem reduz risco de regressão em saves e progressão enquanto permite reescrever mapas, diálogos, personagens e identidade do mundo.

O núcleo narrativo atual está documentado em [`docs/ARAUANA_STORY_IMPLEMENTATION.md`](docs/ARAUANA_STORY_IMPLEMENTATION.md). Entre os elementos já integrados estão o Desencanto, o Arquivo Vivo, o Consórcio Horizonte, os Lembrantes, Professora Anahi, Dona Zila, Ciro e a linha principal ligada a M'Boi.

## Validação

A CI possui duas frentes independentes:

1. **Arauna static validation** — executa os validadores de resíduos visíveis do Emerald em modo `--check`;
2. **Build Emerald base** — instala o toolchain ARM e executa `make -j2 all`.

Os validadores existem para impedir que nomes, falas e identidades antigas do Emerald reapareçam acidentalmente em superfícies já convertidas para Arauna.

## Build local

Depois de preparar as dependências descritas em [`INSTALL.md`](INSTALL.md):

```bash
make -j2 all
```

A ROM gerada é apenas artefato local de desenvolvimento e não deve ser versionada no repositório.

## Regras de integração

- preservar IDs internos do Emerald quando a mudança for apenas de superfície;
- não alterar flags, warps, progressão ou formato de save sem uma decisão técnica explícita;
- preferir alterações pequenas e auditáveis;
- manter arte final separada de mudanças puramente técnicas quando possível;
- validar resíduos narrativos antes do merge.

## Estado

O projeto já possui uma grande passagem narrativa sobre mapas da campanha e continua em integração, limpeza de resíduos, revisão visual e testes. Não há lançamento público final neste momento.
