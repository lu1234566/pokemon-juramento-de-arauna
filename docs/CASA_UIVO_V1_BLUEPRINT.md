# Casa do Uivo V1 — direção e contrato narrativo

Base local: Serra do Uivo V4, commit `6efd240bdb109c6f069d163d564757949d132bc9`.
Referência principal: `review/casa_uivo_v1_concepts/Casa_do_Uivo.png`, extraída do pacote de locais narrativos fornecido pelo usuário.
O mapa é produzido com metatiles e gráficos nativos; a ilustração é referência visual e não é rasterizada no chão.

## Composição implementada

| Ambiente | Dimensões | Elementos da referência transpostos |
|---|---:|---|
| Refúgio | 26 × 28 | Fachada de madeira com frontão alto, encosta rochosa atrás do telhado, cascata à esquerda, duas tochas, escadaria e pátio de pedra |
| Sala principal | 15 × 13 | Madeira quente, livros e desenhos no perímetro, assentos laterais, tapete vermelho e centro livre para conversa |
| Sala das memórias | 13 × 11 | Janela azul ao fundo, duas luminárias, mesa com cadernos, armários e área silenciosa |

A escala da arquitetura, a simplificação da ornamentação e os grafismos de móveis foram adaptados ao grid de 16 × 16. Não se promete equivalência pixel a pixel com a ilustração. A cachoeira e as tochas são cenário estático nesta entrega.

O acesso fica num ramal lateral do patamar intermediário da Serra. Uma passagem de pedra entre a Casa da Terra e a casa do Cortador leva ao refúgio. Apenas 13 células da cidade mudam; os prédios completos, cenas, rotas e os doze warps anteriores permanecem no lugar. Não existe saída alternativa do refúgio para contornar a progressão.

## Entradas e retorno

| Origem | Célula / warp | Destino | Célula / warp |
|---|---|---|---|
| RustboroCity / Serra | (4,34), 12 | Refúgio | (12,27), 0 |
| Refúgio | (14,13), 1 | Sala principal | (7,12), 0 |
| Sala principal | (13,2), 1 | Sala das memórias | (6,10), 0 |

Todas as ligações são recíprocas. Portas usam `MB_NON_ANIMATED_DOOR` e saídas usam `MB_SOUTH_ARROW_WARP`. As salas novas usam elevação 3; a passagem na cidade mantém a elevação 5 do patamar. A entrada por warp faz a transição entre mapas.

## Vínculo com o roteiro

Fontes consultadas: Design Bible, página 42 (Casa do Uivo) e página 50 (sequência de produção); Roteiro Canônico v2.0, seção 20, cenas U01–U11 e direção de Libras 20.1; Bíblia Narrativa v1.3, Arco 2. Os trechos e suas identidades estão em `review/casa_uivo_v1_canon.json` e no snapshot.

A Casa é um refúgio/sala comunitária associado ao Eremita surdo, à mãe falecida e aos registros compartilhados em Libras. Não substitui a Casa da Terra de Dalva nem concede uma insígnia extra. A visita ambiental contém cadernos, desenhos e uma peça de tecido; não completa o enigma ou retira objetos do memorial. Os onze textos já estão em inglês, conforme a política atual do projeto; a conversa do Eremita é apresentada por escrito num caderno. As falas ambientais são novas e não são apresentadas como tradução de Libras.

Os dois NPCs usam representações genéricas nativas existentes (`OLD_MAN`, `LITTLE_GIRL`), com paletas distintas e poses comuns. Não são sprites finais de sinalização nem um novo pipeline de personagens. O retângulo (5,5)–(9,8) da sala principal contém 20 células livres; o Eremita em (7,4) e a plateia cabem juntos em um recorte de 240 × 160. A criança fica fora desse retângulo e não assume o papel de intérprete obrigatório.

## Contrato para a implementação posterior do arco

| Cenas | Necessidade preservada | Estado nesta entrega |
|---|---|---|
| U03–U04 | Consentimento, relato do Eremita e interrupção da comunidade | Palco e circulação disponíveis; eventos de história não implementados |
| U05 | Cadernos da mãe organizados por sequência narrativa | Sala, objetos e leitura ambiental implementados; enigma não implementado |
| U06–U09 | Busca, batalha de acalmar e reconto liderado pelo Eremita | Dependem de mapas/cenas/sistema de pânico posteriores |
| U10–U11 | Compromisso público, registro e Selo do Uivo | Nenhuma recompensa, variável ou flag concedida pela visita |

A seção 20.1 determina tradução qualificada para Libras, revisão por pessoa surda sinalizante, storyboard legível, legendas e replay. Esses materiais não constam da base local. Esta versão não inventa movimentos de mãos, não apresenta poses de caminhada como Libras e não marca U03–U11 como concluídas. A criação de estados por flags, a cena assinada e a liberação narrativa do Pampa deverão seguir esse contrato em etapa própria. Os nomes de flags do roteiro não foram alocados nesta entrega.
