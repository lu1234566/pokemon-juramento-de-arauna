# Acabamento de gráficos, áudio, habilidades e RAM

Base: `7fd3912258bd32f4ccdfd44ca08c964514d4d407`, preservando os arcos do PR #229.
Este pacote fica em uma branch própria, sem merge.

## Alterações

- Diploma: a assinatura exibida passa de GAME FREAK para ARAUNA.
- PokéNav: menu e cabeçalho do mapa passam a ARAUNA MAP; dimensões, índices de
  paleta, FULL VIEW e ZOOM VIEW são preservados.
- Coordenadas de frente e costas dos 386 Pokémon ajustadas às silhuetas nativas
  de 64×64, incluindo as variantes internas de Unown e as frentes de Castform.
  As artes e os IDs não são renumerados.
- 386 gritos originais sintetizados, com registro por família evolutiva,
  envelope e finais suaves, PCM16 mono de 11025 Hz. O conversor padrão do
  motor comprime os WAVs. As amostras e tabelas ficam em ROM.
- RIVER SONG: Iaraú aprende DISARMING VOICE no nível 1 e IARA SONG no nível 42.
  WINGED WATCH passa a incluir a redução de velocidade por paralisia.
- Proteção dos consumidores de grito quando ainda não existe um player ativo.
- Corrigida a declaração de HealPlayerParty e o acesso indexado ao PP no setter.
  A permutação/encriptação dos substructs de Pokémon permanece intacta.
- Removidos argumentos de animação e waitstates redundantes ignorados pelo
  assembler. As actions do CI passam a versões fixadas com Node 24.

## Memória

| Região | Antes, bytes | Após o primeiro build validado, bytes | Antes | Após |
|---|---:|---:|---:|---:|
| EWRAM | 249708 | 247148 | 95,26% | 94,28% |
| IWRAM | 30428 | 28892 | 92,86% | 88,17% |

O heap continua com 114688 bytes (`0x1C000`); RFU e estruturas de save não foram
reduzidos. A grade fixa passa de 10240 para 8960 células: o maior mapa carregado
precisa de 8930. O gate verifica todos os layouts e os mapas procedurais da
Battle Pyramid e da Trainer Hill. O buffer de cópia de IntrMain passa de 2048
para 512 bytes; o linker recusa uma rotina que ultrapasse esse limite.

O linker também exige pelo menos 14,5 KiB livres de EWRAM e 3,5 KiB de IWRAM,
para impedir a volta silenciosa da pressão atual.

## Validação observada antes da desconexão local

Foi compilada e executada em mGBA 0.10.2 uma primeira revisão das correções.
SHA-256 da ROM testada:
`1ad49f25ddb170a7e524cfc4802866a924c7164ea43f980445b11b295d4a289a`.

- Compilação ARM e todos os gates estáticos passaram, sem warnings de C ou ASM.
- Os 386 gritos resolveram para as próprias amostras e produziram PCM audível,
  com a música parada durante a medição.
- 21 verificações de helpers nativos cobriram multiplicadores, paralisia,
  golpes sonoros, proteções e PP nas 24 permutações de personalidade.
- Sete entradas de batalha reais confirmaram SUN CROWN, ABSOLUTE SUN,
  STORMCALL, SOUTH WIND, LONG NIGHT, OATH e FIRST LIGHT.
- Diploma, menu/mapa do PokéNav e batalhas com Caramelo, Iaraú e Arauá foram
  inspecionados visualmente. Os seis mapas máximos Route124/126/127 e seus
  correspondentes submersos carregaram grades válidas de 95×94.
- Um save normal em flash, seguido de CONTINUE em outro processo, preservou
  os 96 valores de PP, em 24 personalidades, sem Bad Egg.
- Heap livre observado: 23188 bytes em batalha e 91480 bytes no mapa do PokéNav.

Esses testes usaram configuração temporária de RAM e chamadas do código ARM
original da ROM; não representam uma campanha inteira ou cobertura completa
das 35 habilidades, doubles ou link. O harness, saves, estados e ROM não entram
no Git.

## Publicação e verificação final

O ambiente local desconectou durante a recompilação da proteção de player
nulo. Portanto, os testes nativos acima pertencem à primeira revisão; não se
atribui aquele hash à versão final. Os geradores foram recuperados e os assets
materializados diretamente no CI. A compilação final e os gates de um checkout
limpo devem ser conferidos no PR e nos logs associados ao seu head final.
