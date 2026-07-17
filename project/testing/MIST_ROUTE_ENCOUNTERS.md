# Teste dos encontros da Rota da Neblina

## Validação automática

Execute:

```sh
python3 scripts/validate_mist_route_encounters.py
```

O validador confirma:

- uma única tabela terrestre para `MAP_ARAUNA_MIST_ROUTE`;
- taxa 20 e os 12 slots na ordem esperada;
- níveis entre 2 e 5;
- ausência de tabelas de água, pesca e quebra de pedras;
- mapa ainda idêntico ao casco aprovado da Rota 101;
- nomes e números dos três iniciais nos textos português e inglês.

## Teste manual no mGBA

1. Comece um save novo e escolha qualquer um dos três iniciais.
2. Vença Nilo e entre na Rota da Neblina.
3. Caminhe em diferentes áreas de grama até iniciar pelo menos 20 batalhas.
4. Confirme que todos os selvagens estão entre os níveis 2 e 5.
5. Confirme que só aparecem Wurmple, Seedot, Taillow, Marill, Aipom, Ralts e
   Murkrow.
6. Atravesse a rota e enfrente o agente técnico; confirme que o percurso dá
   oportunidade suficiente de chegar preparado à equipe de níveis 5 e 6.

O teste manual não aprova sprites. Os gráficos exibidos continuam sendo os
oficiais usados como substitutos técnicos.
