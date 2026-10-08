# Pokémon Juramento de Arauna — checkpoint 06B, Navel Rock V1

**Arte e verificações de host concluídas sobre `29ae94cdc2309d099cd0f8ac4fecc4775a6aef72` (Trainer Hill 06A). Compilação ARM e revisão em emulador pendentes.** São 21 mapas de Navel Rock e seu porto dependente: 6.236 células e 42 warps preservados.

## Base cumulativa recuperada

A Master Map Design Bible, os concepts e os checkpoints foram recuperados antes de editar. Referências e escolhas de ambientação constam de `NAVEL_ROCK_06B_DIRECAO_VISUAL.md`.

A branch integradora `claude/pokemon-juramento-arauna-fhk6ah` foi conferida no GitHub em 08/10/2026. Seu HEAD era `d665dc34ddea776c06c85981653a9f62aa1e19d6`; ainda não continha o 06A local. A sequência anterior permanece integrada: `802d01c341` (03C + 03B V1.1), `5d0b14e46e` (Dive), `a08835a98f6` (Safari) e `d665dc34dd` (manutenção de Petalburg/Oldale). O main `979fb6c1b6731561f3c993efd6045a9bbf096c54` estava 88 commits atrás do integrador.

A entrega inclui o incremento 06B sobre 29ae e um bundle cumulativo **06A + 06B sobre d665**, para permitir integração sem esperar o main. As correções anteriores, incluindo bordas Dive, Altering, Rota 103, porta de Oldale, Petalburg e névoa integrada, estão congeladas. Não foi feita a manutenção geral reservada ao usuário, nem remoção de bancos antigos.

## Mapas concluídos

| Grupo | Mapas | Células | Tratamento |
|---|---:|---:|---|
| Exterior | 1 | 504 | Rocha costeira, sal e madeira |
| Entrada, B1F e bifurcação | 3 | 3.247 | Galerias neutras e bordas de pedra |
| Up1–4 | 4 | 288 | Transição de pedra quente para calcário |
| Topo | 1 | 700 | Santuário claro de Ho-Oh |
| Down01–11 | 11 | 792 | Três estágios de profundidade azulada |
| Fundo | 1 | 484 | Santuário frio de Lugia |
| Porto dependente | 1 | 221 | Madeira castanha e pedra salgada |
| **Total** | **22** | **6.236** | |

Navel Rock sozinho tem 6.015 células. A inclusão do porto impede uma interrupção visual na chegada. O porto de Birth Island, que compartilhava o layout original, continua igual.

## Contrato preservado

- Todos os `map.bin`, `border.bin`, dimensões, elevações e colisões permanecem byte a byte iguais. Os 42 warps têm os mesmos destinos e índices. Objetos, gatilhos, inscrições, textos, scripts, flags, movimentos, itens e progressão não foram editados.
- Ho-Oh e Lugia mantêm seus slots nativos e nível 70. Captura, derrota, fuga, retomada, ocultação e câmera continuam nos scripts originais. Sacred Ash permanece no topo, na posição original (12,9), com sua condição de obtenção.
- O barco mantém Mystic Ticket, `FLAG_ENABLE_SHIP_NAVEL_ROCK`, seleção normal/primeira apresentação e flag do ticket mostrado. A chegada ao porto permanece em (8,4), e o retorno a Lilycove em (8,11).
- Oito layouts nativos trocam somente seus bancos visuais. Nove cópias privadas são acrescentadas no final: a tabela passa de 745 para 754, preservando todos os índices anteriores. Quatorze `map.json` trocam apenas a referência de layout; nenhum outro campo muda.
- Dezesseis bancos privados preservam os 7.651 atributos completos dos metatiles e as 498 máscaras de camada examinadas. As escadas mantêm IDs, comportamento e silhuetas. As referências e os slots de animação de General e Dewford são preservados, incluindo os seis tiles 682–687 da bandeira Dewford. Nenhum gráfico novo ocupa esses slots.
- Os callbacks são os originais: General nos primários, Dewford no exterior e `NULL` nos demais secundários. Não foi alterado código de gameplay ou de animação.

O contrato SHA-256 protege **18.156 arquivos de jogo e 4.238 outras dependências rastreadas**, totalizando **22.394 arquivos anteriores**. Os 18 arquivos existentes permitidos têm alterações estruturais restritas verificadas separadamente.

## Evidências concluídas

- Seletor visual C de produção compilado no host: 6.236 células novas, 112.640 fallbacks/limites, 53.167 células anteriores de cavernas/Dive e 5.376 células dos andares gerados de Trainer Hill.
- Navegação: todos os 42 warps são alcançáveis com a colisão nativa e têm retornos recíprocos. O grafo confirma porto → topo/fundo → porto. Gatilho de Ho-Oh, interação de Lugia, Sacred Ash e marinheiro permanecem acessíveis.
- Funções C nativas do menu do barco: 2.048 configurações e 7.552 casos de seleção/cancelamento, cobrindo tickets e flags combinados; 768 predicados nativos de escadas/portas/warps.
- Execução restrita dos trechos de eventos originais: 36 casos de transição, resultados dos encontros, retomada e viagem do barco. Respostas, resultados de batalha, câmera, movimentos e animação do barco são serviços explícitos de teste.
- Arte: 647 células com piso redesenhado são transitáveis; 301 células de rodapé são bloqueadas. Conferidos atributos de 16 bits, máscaras de transparência, referências, conversão 4bpp, paletas CRLF/RGB555 e bytes reservados de animação. Quatro frames nativos de General e Dewford foram comparados. Os 108.032 pixels de céu do topo conservam a posição e a cor, preservando o contorno da rocha. As 221 células do porto de Birth Island continuam iguais nos quatro frames.
- Auditoria oficial: 8/8 grupos de falhas sem ocorrências. Variantes anteriores: 9/9, nenhuma divergência de comportamento. Composição inglesa oficial e gates estáticos passaram, incluindo 95/95 checks de capacidade de paleta e 189/189 checks do protagonista. Os logs acompanham a entrega.
- Instalação real isolada: **32/32 casos**; resultados detalhados em `review/navel_06b/install_test.json`. O teste cobre preflight, corrupção, alterações locais, main atrasado, integrador sem 06A, rollback de escrita interrompida antes e depois da criação de arquivo novo, instalação integral, idempotência, HEAD preservado, contratos, validador instalado e reconstrução determinística.

Os testes C usam os corpos das funções de produção com serviços de host explícitos. A execução de eventos é restrita, não o interpretador completo da ROM. Estas evidências não substituem uma sessão completa do motor de batalha, barco, câmera ou emulador.

## Entrega e reprodução

O ZIP oferece instalador protegido, patch binário, bundle incremental e bundle cumulativo. Escolher a alternativa apropriada em `LEIA_ME.md`: o incremento exige 29ae; quem está no integrador d665 deve usar o cumulativo. O instalador verifica tudo antes de escrever, cria backup, reverte falhas e preserva HEAD. O bundle cumulativo é conferido por fetch real em um repositório novo que contém somente d665, comparando a árvore completa e todos os hashes do payload; resultados em `CUMULATIVE_TEST.json`. Nenhuma publicação no GitHub foi feita.

```sh
python3 tools/arauna_maps/build_navel_06b.py --base /checkout-limpo-29ae94cdc2
python3 tools/arauna_maps/validate_navel_06b.py --base /checkout-limpo-29ae94cdc2
python3 tools/arauna_maps/render_navel_06b.py --base /checkout-limpo-29ae94cdc2
```

Prévias: `NavelRock_06B_Locais_Chave.png`, `NavelRock_06B_Subida_e_Descida.png` e `NavelRock_06B_Cameras.png`, além dos 22 pares de mapas e 24 pares de recortes. São renders dos bancos instalados sem atores/clima do motor, não screenshots do emulador.

## Integração pendente e próxima etapa

ARM/mGBA não estão disponíveis neste ambiente. O integrador deve compilar e conferir no jogo o barco em primeira/repetida viagem, escadas e retornos, aproximação/câmera de Ho-Oh, interação de Lugia, captura/derrota/fuga/retomada, Sacred Ash e estabilidade das animações costeiras. O ZIP não contém ROM, ELF ou save.

Depois do 06B restam 71 mapas dessa lista de pós-jogo: Bases Secretas (24) e Battle Frontier (47). Próximo bloco sugerido: **06C1 — 16 bases em cavernas**, seguido de **06C2 — oito bases em árvore/arbusto**. O conjunto da Battle Frontier permanece para os checkpoints seguintes.
