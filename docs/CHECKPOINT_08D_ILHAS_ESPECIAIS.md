# Checkpoint 08D — Ilhas especiais V1

Seis mapas adaptados sobre `72b72497acecfec8a14be009c9bebff3d2621877`.
Os checkpoints visuais 08D1–08D3 têm registros separados em
`review/islands_08d/`. A aceitação jogada deste 08D ainda precisa ser feita.

| Etapa | Mapas | Células | Ambientação |
|---|---|---:|---|
| 08D1 | SouthernIsland_Exterior, SouthernIsland_Interior | 1.638 | Mata costeira, granito escuro, madeira de desembarque e clareira do encontro dos Lati |
| 08D2 | BirthIsland_Exterior, BirthIsland_Harbor | 1.121 | Basalto de ilha oceânica, terreno exposto, núcleo claro do puzzle e cais de retorno |
| 08D3 | FarawayIsland_Entrance, FarawayIsland_Interior | 2.318 | Costa de solo quente, rocha úmida, folhas densas e capim para a perseguição de Mew |

## Referências recuperadas antes da edição

A Master Map Design Bible e os 82 concepts únicos foram conferidos pelos
hashes da recuperação canônica. A Bible tem SHA-256
`366d4cbfa103fb58d8b13837fe58fdd0154c35ba8f51c0fd74f76e989a77a95d`.
Os capítulos do arquipélago (Rotas 124–126) e do centro/norte tropical
(Rotas 118–123), com seus concepts, orientam a pedra costeira, a mata e os
desembarques. A Bible não contém uma ficha específica para estas ilhas;
as três ambientações são uma proposta deste checkpoint, sem alterar enredo.

Recuperei o ZIP 08C original (`45ecb9c563b2f8234d2d1b9051dcffbc03dc84023767321f22de193a5beb42c6`),
conferi CRC, hashes internos, os 66 arquivos de payload contra o checkout da
base e os três bundles. As paletas têm CRLF no checkout, como exige
`.gitattributes`, e LF no objeto Git; seus conteúdos são iguais.
`recovery.json` registra a conferência.

A branch do projeto buscada no GitHub é `72b72497ac`. `main`, em
`979fb6c1b6731561f3c993efd6045a9bbf096c54`, está 126 commits atrás dessa base.
O incremento e os cumulativos partem de bases instaladas, com as correções
de integração incluídas. Não houve push.

## Arte e integridade funcional

São cinco pares de bancos exclusivos: Southern, Birth, IslandHarbor,
FarawayCoast e FarawayForest. Separar entrada e interior de Faraway mantém
as definições e os callbacks nativos de Rustboro e Fortree. O layout
IslandHarbor só é utilizado por BirthIsland_Harbor; Navel Rock não é afetado.

254 instâncias de IDs recebem arte de materiais, folhagem, textura do solo
e cais. Usam 479 slots gráficos estáticos livres, sem ocupar os slots de
DMA. A paleta 12 de cada par é nova; as paletas 0–11 são iguais às nativas.
As máscaras dos dois planos, os contornos dos obstáculos e os atributos
completos de cada banco permanecem iguais. São 630 máscaras conferidas e
4.135 metatiles não redesenhados com pixels iguais aos originais.

As águas e as poças conservam os metatiles e as paletas nativos. Conferi
388 referências a quarters animados e 488 comparações de estados aquáticos
nos oito quadros. Os callbacks e os slots de General, Rustboro (640–671 e
960–963) e Dewford (682–687) foram preservados. Os renders de Rustboro
mostram uma fase comum; os quarters iguais também conservam a defasagem
das faixas no jogo. Nenhum código de animação foi editado.

As 5.077 células de mapa, os borders e os arquivos de mapa e script são
iguais à base. Os 754 layouts conservam IDs e ordem; seis trocam apenas
referências dos bancos. São 10 warps, 11 objetos, três eventos de coordenada
e três eventos de fundo preservados. Não acrescentei obstáculos nem
desloquei os pontos de interação para acomodar a arte.

As seguintes dependências permanecem congeladas:

- Embarque por tickets/eventos, movimentos do ferry e retorno a Lilycove.
- Escolha entre Latios/Latias, encontro no marco, Soul Dew e flags de resultado.
- As 11 posições do triângulo de Deoxys, limites de passos, paletas do sprite,
  destruição da pedra, aproximação e flags de captura/derrota/fuga.
- Mew, sua invisibilidade por passos, IA, movimentos, Cut e efeitos do capim.
  Os quatro obstáculos em `(14,9)`, `(18,9)`, `(9,10)` e `(13,13)` continuam
  com célula `0x4E0`; a arte contempla também os IDs criados pelo Cut.
- Climas existentes, scripts de nuvens e flags de reencontro, sem nova névoa.

## Sete correções protegidas

| Arquivo | SHA-256 |
|---|---|
| src/party_menu.c | e05f9efb61cfd652e56a361ba1e8b826f614abc0e684438a0b031b036679d08f |
| src/field_player_avatar.c | 81ebe4b5761f8992cb459cf37978262358231734a1c56f8b3447346f770db95f |
| src/scrcmd.c | 98cd4b72474c3cc7dfd5dc6cf54a4a96f807733017761a2be58d62b0dcd063a9 |
| data/maps/SlateportCity_Harbor/scripts.inc | fc256e12cb37712c2a2b3e026d442e6baa55ed6560909e7cadecda83c19167ea |
| data/maps/LilycoveCity_Harbor/scripts.inc | 46ab224e74a02b311a9a38b0eb8f940b169e9e5d83844283ccda00be39ebd18c |
| data/maps/FallarborTown_CozmosHouse/scripts.inc | 798dc439a26a33d0845646eab56d599d7712e34414c712304d834ae4eb89f4a6 |
| data/maps/Route116/scripts.inc | cd955b92f802f347645b82cc1bc54aa1715d35097009f7504ec98079c46a62c5 |

O contrato protege 24.388 arquivos existentes, inclusive Centro, água do
Palace, `field_door.c`, `overworld.c`, sprites e todos os pacotes anteriores.
Só quatro registros admitem adições controladas: `layouts.json`, `graphics.h`,
`metatiles.h` e `headers.h`. O validador restaura as seis referências de
banco e retira exclusivamente o bloco 08D para comparar com a base.

Os contratos antigos não foram editados. O 08B1 tem sete diferenças
documentadas; o 08B2, seis; o 08B3 e o 08C, quatro. São as correções de
integração já registradas, verificadas pelo 08D com os hashes atuais.
O validador original do 08C continua acusando os scripts corrigidos;
nada foi revertido para fazê-lo passar.

## Validação e retomada

`validate_islands_08d.py` e os seis gates de leitura passam. O gate de mapas
tem as mesmas três observações antigas de Surf; não são novas deste pacote.
`validation.json`, `gates.json`, logs, comparações de cada mapa e previews
de água ficam em `review/islands_08d/`.

O pacote acompanha manifesto, patch binário, instalador com preflight,
backup/rollback e três bundles:

| Bundle | Base |
|---|---|
| checkpoint_08D.bundle | 72b72497ac |
| cumulative_from_08C_08D.bundle | 5c8f309fd1, o 08C do autor antes das quatro correções |
| cumulative_a594_08D.bundle | a594b3e1e6, fechamento do Frontier com manutenção |

O instalador recusa versões antigas de cada uma das sete correções,
payload corrompido, Centro modificado, IA de Mew alterada, edição local
desconhecida e base obsoleta. Também foram exercitados instalação real,
falha no segundo arquivo com rollback automático, reaplicação sem escrita
e rollback pelo backup. O registro no Git cobre o payload de ensaio;
`INSTALL_TEST.json` do ZIP repete o teste sobre o payload final, incluindo
o próprio registro de ensaio. São 17 casos em cada execução.

Os três bundles foram verificados e importados em worktrees separados das
bases correspondentes, com comparação do commit, árvore, todos os arquivos
rastreados e as sete correções. O armazenamento de objetos Git é
compartilhado nesses testes; não são um clone vazio nem recuperação direta
de main. `CUMULATIVE_TEST.json` explicita esse limite.

Este ambiente não tem compilador ARM nem mGBA. Não há ROM ou save no ZIP.
As imagens são renders nativos RGB555 sem atores. A aceitação real do 08C
registrada em `docs/INTEGRACAO_08C.md` continua preservada; não equivale a
aceitação das ilhas redesenhadas.

## Aceitação pendente no mGBA

| Sessão | Percurso e resultado a conferir |
|---|---|
| 08D1 | Embarcar com Eon Ticket; sair do cais até o marco; encontro de Latios e Latias em saves separados; pan da câmera; captura, derrota/fuga e revisita; Soul Dew; retorno pelo marinheiro; salvar/carregar |
| 08D2 | Embarcar com Aurora Ticket; completar e errar o puzzle; cores e movimentos do triângulo; destruição e batalha de Deoxys; captura, derrota/fuga e revisita; atravessar o porto e retornar pelo ferry |
| 08D3 | Embarcar com Old Sea Map; subir o relevo; clima/nuvens e inscrição; perseguir Mew junto dos quatro obstáculos; Cut e sumiço de Mew; reentrada e batalha; captura, derrota/fuga e revisita; retorno e salvar/carregar |

Depois da integração do 08D, restam 11 mapas ativos com bancos nativos:
seis de Contests e cinco de link/multiplayer. O inventário contém 528 mapas:
493 com banco Arauna, 16 módulos da Pyramid gerados em runtime, oito mapas
inativos/protótipos e esses 11 restantes. Próxima proposta: Contests em
checkpoints curtos, partindo do commit integrado do 08D.
