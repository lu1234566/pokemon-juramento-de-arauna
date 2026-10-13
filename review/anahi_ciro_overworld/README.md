# ANAHI e CIRO fase 1: overworld

Entrega `Arauna_Anahi_e_Ciro_Overworld` (13/10/2026). Aqui ficam o `LEIA-ME.md`,
`validation.json`, `prompts.json` e `SHA256SUMS.txt` do pacote, como vieram.
As prévias e GIFs não foram copiados; os PNGs instalados estão em:

| personagem | folha | paleta |
|---|---|---|
| ANAHI | `graphics/object_events/pics/people/prof_birch.png` | `graphics/object_events/palettes/anahi.pal` |
| CIRO fase 1 | `graphics/object_events/pics/people/ciro/phase1_may.png` e `phase1_brendan.png` | `graphics/object_events/palettes/ciro_f1.pal` |

Os índices dos pixels entraram intactos. O PNG da ANAHI trazia 15 entradas de
paleta e nenhum `tRNS`; foi regravado com as 16 entradas da JASC entregue e o
índice 0 transparente, que é o que `tools/validate_arauna_character_assets.py`
exige. As JASC foram regravadas com CRLF, como as outras do projeto.

Conferido na ROM montada: `gObjectEventPic_ProfBirch`, `gObjectEventPic_CiroMay`,
`gObjectEventPal_Anahi` e `gObjectEventPal_CiroF1` batem byte a byte com os
`compiled/overworld.4bpp` e `compiled/overworld.gbapal` da entrega.

No mGBA: a cena do resgate na Rota 101 (ANAHI correndo do cachorro, as três
direções de caminhada), o CIRO entrando no quarto e andando até o jogador, e
a ANAHI no laboratório. `rota101.png`, `quarto_ciro.png` e `laboratorio.png`
são quadros dessas sessões.
