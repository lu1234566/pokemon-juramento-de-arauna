# Primeira Câmara V1 — blueprint antes da construção

Referência principal: `01_Primeira_Camara_Primeiro_Elo.png`, enviada no pacote de Locais Narrativos Dedicados. Bible, p.42: antecâmara mineral, inscrições, núcleo luminoso e altar; abertura com conquistas da Maré e Terra e porta previamente vista. A estética é pedra escura, água azul, luz ciano, inscrições, pilares e vegetação úmida; os três painéis da prancha orientam a composição.

## Implantação e primeira tela

O repositório não contém um mapa da Primeira Câmara nem uma Rota da Neblina identificada. Será criado um ramal curto no setor nordeste da Rota 101, fora da clareira e dos percursos do prólogo. Esse ramal dá acesso ao novo recinto de chegada; seu texto o identifica como Trilha da Neblina. O caminho principal, conexões, eventos e textos antigos da Rota 101 ficam preservados.

- **Chegada, 30×26:** entrada ao sul, escadaria e ponte de pedra sobre água, margem de vegetação escura e um único templo na encosta norte. O primeiro enquadramento aponta para o núcleo azul da fachada. Duas inscrições laterais comunicam as marcas da Maré e da Terra.
- **Interior, 22×24:** antecâmara de pedra, inscrições laterais, plataforma central com elo quebrado, duas colunas/estátuas e núcleo ciano na parede do fundo. Um eixo curto conduz ao altar; passagens laterais permitem contorná-lo.
- A água é ornamental bloqueada. Três elevações ligadas por degraus nativos distinguem chegada, ponte e patamar sem exigir HMs.
- Banco secundário próprio e módulos inteiros; paletas locais escuras. A fachada e o altar serão assets reais indexados, sem depender de pintura sobre o render.

## Estado funcional

Serão acrescentados dois mapas e seus layouts ao fim dos registros existentes, sem renumerar qualquer mapa/layout anterior. O exterior da Primeira Câmara abre como desvio opcional, sem bloquear a campanha existente.

A porta possui estado persistente de vista e aberta. A primeira interação registra a visita. Uma interação posterior exige `FLAG_BADGE01_GET` e `FLAG_BADGE02_GET`, as conquistas já preservadas nas adaptações das Casas da Terra e da Maré. Essas flags não são concedidas nem alteradas pela Câmara. Três flags anteriormente livres serão reservadas para porta vista, porta aberta e altar escutado.

A cena do altar usa uma escolha explícita de escutar e uma alteração visual persistente; inclui o nome Augusto e o princípio da prancha: "O que nos liga, permanece". Não implementa mudanças em atributos de POKéMON, evoluções, capturas, inventário ou um Sistema de Vínculos mecânico completo. Os diálogos novos terão versões PT-BR e EN no mesmo padrão de tradução do projeto.

## Inventário e garantias

Não há eventos antigos no novo espaço. A Rota 101 tem oito objetos, nove gatilhos do prólogo, uma placa e duas conexões; todos permanecem com identidade, posição e script intactos. A adição prevê somente o pequeno acesso, dois warps e uma placa de orientação. Nenhum sprite existente será alterado, inclusive Dalva.

Testar fechamento sem conquistas, combinações das duas conquistas, porta vista, persistência da abertura, entrada/saída nos dois sentidos, opção de recusar o altar, repetição e retorno ao mapa. Simular coordenadas alteradas por `setmetatile` nos estados fechado/aberto e altar dormente/ativo. Verificar IDs anteriores, registro de scripts, conversão de mapas, artefatos indexados, colisões, recortes 240×160 e reprodução do pacote. Build completo e emulador dependem das ferramentas disponíveis e não serão substituídos por alegações sobre PNGs.
