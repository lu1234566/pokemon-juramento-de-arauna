# Pokémon Juramento de Arauna

ROM hack de Pokémon Emerald em desenvolvimento, ambientada em Arauna e construída sobre a decompilação do `pokeemerald`.

## Direção atual

A implementação preserva o esqueleto técnico do Emerald — grafo de eventos, ordem de progressão, warps, flags, variáveis e identificadores internos — e substitui a superfície visível pelo cânone de Arauna. Essa abordagem reduz risco de regressão em saves e progressão enquanto permite reescrever diálogos, personagens, identidade do mundo e, em passes separados, os mapas.

O núcleo narrativo está documentado em [`docs/ARAUANA_STORY_IMPLEMENTATION.md`](docs/ARAUANA_STORY_IMPLEMENTATION.md). A build oficial é **English-only**. Nomes próprios canônicos de Arauna, como Vila Amanhecer, M'Boi e Seu Bento, são preservados quando apropriado; isso não reabre um modo PT-BR.

## Fonte de verdade da build

A build oficial é dirigida por manifestos e falha fechada:

- `scripts/english_renderers.txt` — ordem oficial dos **66** renderizadores English-only;
- `scripts/english_overlay_files_extra.txt` — **40** fontes finais adicionadas ao conjunto transacional de backup/restore;
- `scripts/check_english_only_policy.py` — trava política, ordem e integração da build;
- `scripts/check_arauna_story_coverage.py` — exige **16/16** estágios canônicos e **346** blocos runtime de lacuna final cobertos;
- `scripts/audit_rendered_visible_residue_en.py` — inventário pós-render de identidades antigas/PT-BR residual; superfícies transacionais críticas falham a validação;
- `scripts/check_arauna_static.sh` — executa a mesma composição transacional da build oficial sem exigir o toolchain ARM.

Os arquivos temporariamente renderizados são restaurados em qualquer saída normal, erro ou interrupção do wrapper oficial.

## Validação local sem compilar a ROM

Depois de clonar o repositório:

```bash
bash scripts/check_arauna_static.sh
```

Esse comando aplica os renderizadores na ordem oficial, executa os gates English-only/cobertura, valida Weather Institute e a política de arquivos proprietários e restaura as fontes. Apenas o `make` final é substituído por um no-op de validação.

## Build local oficial

Prepare as dependências do `pokeemerald` descritas em [`INSTALL.md`](INSTALL.md), incluindo `gcc-arm-none-eabi`, `binutils-arm-none-eabi` e `libpng-dev`, e execute:

```bash
bash scripts/build_arauna.sh -j2 all
```

Também é aceito, por compatibilidade:

```bash
bash scripts/build_arauna.sh en -j2 all
```

Entradas `ptbr`, `pt-br`, `portuguese` e `portugues` são rejeitadas explicitamente. Não existe build oficial PT-BR.

Com `MODERN=1`, o alvo esperado é:

```text
build/arauna-en/pokemon-juramento-de-arauna-en_modern.gba
```

A ROM gerada é artefato local de desenvolvimento e não deve ser versionada.

## CI

O workflow possui duas responsabilidades:

1. **repository-safety** chama somente `scripts/check_arauna_static.sh`, evitando uma segunda lista manual de renderizadores;
2. **Build Arauna English ROM** instala o toolchain ARM e chama `scripts/build_arauna.sh -j2 all`.

O projeto não depende de GitHub Actions para editar ou integrar conteúdo. A CI é apenas uma superfície de validação quando estiver disponível.

## Regras de integração

- preservar IDs internos do Emerald quando a mudança for apenas de superfície;
- não alterar flags, warps, progressão ou formato de save sem decisão técnica explícita;
- preferir alterações pequenas, determinísticas e auditáveis;
- manter arte/mapas separados de mudanças puramente técnicas quando possível;
- todo renderer oficial deve estar no manifesto e possuir limites de escrita/verificação apropriados;
- não declarar build/playtest como aprovado sem executar de fato o toolchain/emulador correspondente.

## Estado de prontidão

A infraestrutura English-only e a cobertura canônica possuem gates fail-closed. A auditoria de prontidão de 23/08/2026 fechou lacunas runtime que estavam fora do conjunto canônico anterior, incluindo:

- a transição M'Boi → Oath Tower ainda expunha a cena vanilla de Wallace/Cave of Origin;
- uma fala opcional em Route 119 ainda citava Cave of Origin;
- uma ponte de PokéNav em Route 105 ainda registrava DAD NORMAN / DEVON's MR. STONE em vez de ELIAS / OTACILIO;
- a sidequest do SCANNER no navio abandonado ainda enviava o jogador a CAPT. STERN em vez do HARBOR ENGINEER;
- landmarks do mapa regional ainda exibiam identidades vanilla como MT. PYRE, SKY PILLAR, RUSTURF TUNNEL, MAGMA HIDEOUT, GRANITE CAVE e NEW MAUVILLE; somente equivalências já estabelecidas no cânone foram substituídas.

O repositório ainda está em desenvolvimento. Uma compilação ARM completa e um playtest em ROM continuam sendo evidências separadas da validação estática; mapas e polimento visual também permanecem em passes próprios.

A antiga documentação de localização bilíngue de 19/08/2026 é mantida apenas como registro histórico e não descreve a build atual.
