# Vila Amanhecer V8 — blueprint pelos concepts

Referências: Vila Amanhecer, exterior da casa do protagonista e exterior do Laboratório Anahí, recebidos em 06/09/2026. A Design Bible define nomes, função e fluxo; os concepts dedicados definem a arquitetura. O exterior da vila é o escopo desta etapa.

- Função: primeiro lar, reencontros e preparação da jornada. A casa deve parecer acolhedora; o laboratório deve ser a construção mais recente.
- Bioma: vila rural do Sul/Sudeste, terra ocre avermelhada, mata próxima, pequenos jardins e cercas de madeira.
- Geometria: 30×26 metatiles. Casa oeste a noroeste; segunda casa deslocada para leste e para baixo; laboratório ao sul, em diagonal. Não criar uma praça grande.
- Fluxo: passagem norte estreita → curva na rua de terra → acesso às casas → pequena clareira comunitária → ramal do laboratório. A ligação com a Rota 101 permanece em x=10/11, offset 0.
- Arquitetura: telhas cerâmicas desenhadas na resolução nativa, madeira, alvenaria clara, janelas azuis e caixa de correio. Laboratório com cobertura azul-petróleo, frontão/emblema e equipamentos externos discretos.
- Paisagem: grupos de árvores completos, cercas com entradas, canteiros junto às fachadas, banco na clareira. O açude quadrado da V7 deixa de dominar o nordeste.
- Assets: tileset exclusivo da vila derivado dos elementos nativos, com paletas próprias. Não recolorir o Petalburg compartilhado. Portas animadas próprias, registradas no motor sem substituir portas de outras cidades.
- Narrativa: manter os estados/flags/diálogos. Migrar posições das casas e dos atores, coordenadas da porta, saída dinâmica do caminhão e Fly. Preservar a faixa norte das cenas de bloqueio e calçados; simular ambas as escolhas de personagem.
- Evidência: render do map.bin real, comparação com os três concepts, viewports 240×160, cenas simuladas sobre o mapa, conversão nativa dos eventos e pacote reproduzível. Não apresentar essas imagens como capturas de emulador.

Inventário: 3 warps, 5 gatilhos, 4 placas e 8 objetos. As duas coordenadas de saída dinâmica do caminhão e os dois destinos externos de Fly ainda estão na geometria antiga; fazem parte da correção funcional desta entrega.
