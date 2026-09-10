# Vila Amanhecer V9 — conjunto completo

Base recuperável: `bf387be`, após a Primeira Câmara V1. Direção autorizada: aproximar a implementação das concept arts fornecidas, incluindo vila e interiores.

## Referências e composição

- Vila: três construções assimétricas, estrada vermelha sinuosa, cercas e jardins densos. Preservar as fachadas próprias da V8 e fechar os vazios com recantos usados, flores e vegetação; preservar a chegada e a saída do prólogo.
- Casa do protagonista: piso de madeira quente, paredes creme, cozinha completa, banco, mesa xadrez com cadeiras, tapetes verdes, fotos e escada. Quarto com cama verde, computador, livros, relógio e objetos pessoais.
- Casa de Ciro: mesma escala doméstica, madeira e mobiliário simples; roupa de cama e tecidos azuis, conforme a referência individual. O papel das duas casas continua dependente do personagem escolhido. A seleção visual acompanha esse papel em tempo de execução.
- Laboratório: piso claro, molduras verde-azuladas, mapa, plantas, bancada de exposição e vitrines. Duas portas levam às salas de pesquisa e equipamentos das referências. A bancada de recompensa pós-jogo continua funcional.

## Contratos preservados

Os quatro interiores domésticos mantêm dimensões, colisões, elevações, warps, gatilhos, posições de decoração e percursos do prólogo. O redesenho usa módulos completos dentro dessa geometria. Os IDs de PC ligado/desligado, caixas de mudança e manual continuam disponíveis nos dois bancos domésticos. A televisão permanece nativa porque as transmissões a atualizam pelo comportamento do motor.

O laboratório conserva a entrada (6/7,12), o ponto de retorno do resgate (6,5), os percursos centrais da Pokédex e as posições da recompensa. As duas versões de layout são reconstruídas juntas. As salas anexas são acessíveis por portas fora desses percursos, com observações ambientais sem itens, flags ou recompensas novas.

Não deslocar a escolha inicial de Pokémon da Rota 101 nesta revisão: ela já integra o resgate e a progressão do projeto. A bancada principal representa o espaço de trabalho da referência; a oferta pós-jogo mantém seus eventos reais.

## Evidência exigida

Render dos arquivos nativos; exterior, quatro interiores, duas paletas narrativas, laboratório normal/pós-jogo e dois anexos; recortes de 240×160; teste dos IDs dinâmicos e das decorações; conexões recíprocas; conversão nativa de eventos; instalação protegida e reprodução a partir do ZIP. Sem alegar execução da ROM ou emulador quando indisponíveis.
