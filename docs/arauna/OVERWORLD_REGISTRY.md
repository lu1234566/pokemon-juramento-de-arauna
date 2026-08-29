# Overworlds Arauna — registry dinâmico

Os 46 redraws PixelLab estão todos registrados e selecionáveis, gastando **dois**
ids de object event em vez de 46.

## Como colocar um Pokémon Arauna num mapa

No Porymap, dê ao object event um destes graphics:

| Graphics | Canal | Seletor |
|---|---|---|
| `OBJ_EVENT_GFX_ARAUNA_POKEMON_A` | A | `VAR_ARAUNA_OW_A` |
| `OBJ_EVENT_GFX_ARAUNA_POKEMON_B` | B | `VAR_ARAUNA_OW_B` |

O id não diz qual criatura é. Quem diz é o seletor, num `on_transition` do mapa:

```
setvar VAR_ARAUNA_OW_A, ARAUNA_OW_BOIUNA
setvar VAR_ARAUNA_OW_B, ARAUNA_OW_IEMANJA
```

Para trocar com o jogo já rodando, sem recarregar o mapa:

```
setvar VAR_0x8004, <localId do object>
setvar VAR_0x8005, ARAUNA_OW_CHANNEL_A
setvar VAR_0x8006, ARAUNA_OW_ANHANGAU
special SetAraunaPokemonOverworld
```

Os 46 valores `ARAUNA_OW_*` estão em `include/constants/arauna_overworld.h`.

## Duas reservas que você precisa saber

### `VAR_OBJ_GFX_ID_C` e `VAR_OBJ_GFX_ID_D` não estão mais livres

São os seletores dos canais A e B. Estão marcados como `RESERVED` na própria
linha em que são definidos, em `include/constants/vars.h`, porque é ali que
alguém procurando uma var sobrando vai olhar.

Escrever nessas vars a partir de qualquer outro lugar **repinta silenciosamente**
qualquer overworld Arauna que estiver na tela. Isso não é só uma convenção:
`tools/arauna/check_overworld_registry.py` roda dentro de
`scripts/check_arauna_static.sh` e **falha** se qualquer arquivo fora do sistema
Arauna passar a citar essas vars, nomeando o arquivo invasor.

`VAR_OBJ_GFX_ID_B` é a única var de object-gfx que continua sem dono. Foi
verificado que o vanilla nunca escreve nas três (B, C, D); as outras treze são
usadas por rival, Battle Frontier, Pike, Dome, Arena e Tower.

### Dois canais é o teto, e o motivo é paleta

Um `ObjectEventGraphicsInfo` nomeia **um** slot de paleta, e dois objetos no
mesmo slot com tags diferentes brigam pelo banco. O canal A usa
`PALSLOT_NPC_SPECIAL`; o B usa `16 + PALSLOT_NPC_SPECIAL_REFLECTION`, que é a
válvula de escape do próprio engine — `TrySetupObjectEventSprite` subtrai 16 e
faz `_PatchObjectPalette` direto naquele banco.

Uma terceira espécie simultânea precisaria de um banco OBJ livre no campo, e não
existe: 0–11 estão no enum de PALSLOT e 12–15 são field effects e interface. Se
um dia precisar de mais, o caminho é carregar paleta sob demanda ao entrar na
tela, não gastar mais ids.

Vários objetos **do mesmo canal** no mesmo mapa são livres — todos mostram a
mesma criatura.

## O mapa de harness fica

`AquaHideout_UnusedRubyMap1` continua no build, permanentemente. A decisão foi
essa e não "remover antes do release", por três razões concretas:

1. **O jogador não alcança.** É uma sobra de Ruby: nenhum warp aponta para ela,
   `connections.inc` está vazio, e a única citação do id fora da própria pasta é
   a linha do enum em `map_groups.h`. Sem um warp de debug, é inacessível.
2. **É a única prova executável do mecanismo.** Removê-la deixaria o registry sem
   como ser verificado em hardware. Os dois objetos lado a lado, um por canal,
   são exatamente a demonstração de que duas criaturas diferentes aparecem juntas
   a partir de dois ids.
3. **Custa quase nada.** Dois object events e um script numa `events.inc` que já
   existia — ~200 bytes. As 46 sheets estão na ROM de qualquer jeito, porque o
   registry é que as referencia.

O risco real não é o mapa existir; é alguém ligar um warp nele depois e um
jogador cair lá. Por isso o verificador tem um teste de alcançabilidade: se
qualquer arquivo fora da pasta do mapa passar a citar
`MAP_AQUA_HIDEOUT_UNUSED_RUBY_MAP1`, ou se o mapa ganhar conexões, o
`check_arauna_static.sh` falha.

### Se um dia quiser tirar mesmo assim

São dois arquivos e nada mais:

```
git checkout <commit anterior> -- data/maps/AquaHideout_UnusedRubyMap1/
```

Depois remova o teste de harness em `tools/arauna/check_overworld_registry.py`.
O registry, os dois ids dispatcher, as vars reservadas e os 46 assets continuam
funcionando sem ele — o harness só demonstra, não sustenta.

## O que não mudou

Nada persistente. Desde `c8557cb2` os únicos headers tocados são
`constants/event_objects.h`, `constants/vars.h` e o novo
`constants/arauna_overworld.h`, todos só `#define`, sem uma struct dentro.
`ObjectEventTemplate.graphicsId` e `ObjectEvent.graphicsId` continuam `u8`,
`SaveBlock1` é byte-idêntico e saves antigos continuam válidos. O verificador
confere isso a cada execução.
