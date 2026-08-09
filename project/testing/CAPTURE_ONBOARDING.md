# Teste da Pokédex e do kit de captura

## Validação automática

```sh
python3 scripts/validate_capture_onboarding.py
```

O script confere os comandos de desbloqueio da Pokédex, os 386 slots, a trava
do kit, as quantidades de itens, a remoção persistente do objeto, os textos nos
dois idiomas e o uso exclusivo do gráfico oficial da Poké Ball.

## Teste manual no mGBA

1. Inicie um save novo e tente pegar o kit antes de escolher o inicial; ele
   deve permanecer no mapa e informar que está selado.
2. Escolha um inicial e confirme que a opção da Pokédex aparece no menu.
3. Abra a Pokédex e confirme que ela está no modo de 386 espécies.
4. Volte à praça e pegue o kit: devem entrar 5 Poké Balls e 3 Potions.
5. Salve e recarregue; o objeto do kit não deve reaparecer.
6. Capture um Pokémon da Rota da Neblina e confirme o registro na Pokédex.
7. Repita a escolha em saves separados para Caramelo, Querô e Pimpau.

Os Pokémon e ícones vistos nesse teste continuam sendo substitutos oficiais;
o teste não aprova nem integra sprites de Arauna.
