# Liga de Arauna — Caminho das Quatro Vozes, interiores V1

Os 15 mapas internos da Liga receberam uma direção visual comum de pedra,
vidro azul e dourado. O hall principal ganhou um mosaico cerimonial de 64 ×
64 pixels; as quatro câmaras usam violeta, rosa, azul e verde, como na prancha
fornecida. Os símbolos antigos dos pisos foram substituídos por mosaicos e
os grandes enfeites laterais deram lugar a painéis de pedra inscritos.
A sala final recebeu outro mosaico, enquanto corredores, registro de memória
e espaços de apoio acompanham os materiais do conjunto.

Os nomes das câmaras na referência orientam a arte. Esta entrega preserva os
personagens, textos, batalhas e progressão atuais; não certifica a implementação
dos novos arcos L01–L05 descritos na Bíblia.

Foram preservados 43 warps, 24 objetos, todos os gatilhos, scripts, bordas,
dimensões, colisões, elevação e comportamentos. Os slots 992–995 e 1016 das
animações da Elite não foram reutilizados. As portas continuam nos mesmos IDs.

Instalação isolada, reaplicação, conflito, reprodução, mapjson e validação
nativa fazem parte do pacote. Build ARM completo e emulador ficam pendentes.

## Instalação no repositório

- `EverGrandeCity_PokemonCenter_1F`: o pacote partia de uma base anterior ao
  lote 06 e traria de volta `OBJ_EVENT_GFX_SCOTT`. Entrou só o layout novo; o
  objeto continua `OBJ_EVENT_GFX_STEVEN`.
- Os 15 layouts repetem, tile a tile, colisão, elevação e comportamento dos
  antigos. Os 34 metatiles que scripts e código trocam em jogo (portas e
  holofotes da Elite, porta do Cable Club, balcão, escada rolante) existem
  nos tilesets novos com o mesmo desenho e o mesmo comportamento.
- A animação de porta do Cable Club (`field_door.c`) e a da escada rolante
  usam quadros próprios; continuam com as cores antigas durante a animação.
- Build ARM, gates e emulador (os 11 mapas acessíveis por warp) verificados.
