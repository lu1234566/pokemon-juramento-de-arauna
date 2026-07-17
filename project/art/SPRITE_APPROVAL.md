# Protocolo de aprovação de sprites

## Regra principal

Nenhum sprite novo ou modificado será integrado ao jogo antes de Lucas Barcelar receber uma prévia claramente identificada e responder com aprovação explícita.

Silêncio, aprovação do conceito escrito ou aprovação de outra forma evolutiva não contam como aprovação do sprite apresentado.

## Escopo

O protocolo vale para:

- sprites frontais e traseiros de espécies;
- animações de batalha;
- ícones de menu;
- overworlds de personagens e Pokémon;
- sprites de treinadores;
- retratos, footprints e shinies;
- revisões de paleta ou pixel que alterem aparência percebida.

## Pacote de prévia

Cada pedido de aprovação deve informar:

- ID e nome/codinome do asset;
- versão da proposta;
- dimensões e quantidade de cores;
- comparação com a versão anterior, quando existir;
- paleta sobre fundo claro e escuro;
- visualização em escala nativa e ampliada sem suavização;
- observações sobre legibilidade no GBA;
- opções de resposta: aprovar, aprovar com ajustes ou rejeitar.

## Registro

Assets seguem os estados:

`draft` → `awaiting-approval` → `approved` → `integrated` → `verified-in-mGBA`

Uma aprovação registra data, versão e responsável. Alterações visuais posteriores retornam o asset para `awaiting-approval`.

## Separação entre arte e código

- Propostas podem existir fora dos diretórios compilados.
- Placeholders oficiais ou formas geométricas identificadas podem validar mecânicas sem fingir que são arte final.
- Branches de sprite não devem misturar alterações narrativas ou grandes mudanças de mapa.
- A integração acontece somente após aprovação e inclui validação de formato, paleta, animação, shiny, ícone e sprite traseiro quando aplicável.

## Exceções

Correções estritamente técnicas que não alterem a aparência percebida — por exemplo, nome de arquivo ou referência quebrada — podem ser feitas sem nova aprovação visual. Se houver dúvida sobre impacto visual, a mudança volta para aprovação.
