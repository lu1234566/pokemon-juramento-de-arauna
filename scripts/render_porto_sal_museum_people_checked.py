#!/usr/bin/env python3
from __future__ import annotations

import render_porto_sal_museum_people as base


def patch(targets, label, payloads):
    markers, _ = targets[label]
    targets[label] = (markers, payloads)


patch(base.CITY_TARGETS, "SlateportCity_Text_BossIsBrilliant", (
    "HORIZONTE: Diretor quer avaliar\\n", "equipamentos oceanograficos.\\p",
    "Nao sei por que vieram tantos.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_RemindsMeOfLongLineForGames", (
    "HORIZONTE: Faz tempo que nao\\n", "vejo fila desse tamanho.\\p",
    "Parece lancamento de jogo.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_WhyAreWeLiningUp", (
    "HORIZONTE: Por que pagar ¥50?\\p",
    "HORIZONTE: Porque e um MUSEU\\n", "civil. Pague e entre.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_ShouldveBroughtMyGameBoy", (
    "HORIZONTE: Devia trazer algo\\n", "para passar o tempo.\\p",
    "Essa fila nao anda.$",
))
patch(base.CITY_TARGETS, "SlateportCity_Text_HotSpringsAfterOperation", (
    "HORIZONTE: Depois da missao,\\n", "eu pago o jantar.\\p",
    "Se a gente sair daqui hoje.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_CanLearnForNefariousDeeds", (
    "HORIZONTE: Os modelos explicam\\n", "correntes e pressao.\\p",
    "Isso pode ser util em campo.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_RustboroBungled", (
    "HORIZONTE: Se a outra operacao\\n", "desse certo, eu nao estaria aqui.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_RememberMeTakeThis", (
    "HORIZONTE: Lembra de mim?\\p", "Voce me venceu antes.\\p",
    "Esta TM nao devia estar comigo.\\n", "Leve. Considere uma divida.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_HopeINeverSeeYouAgain", (
    "HORIZONTE: Estamos quites.\\p", "Espero que na proxima vez\\n",
    "nao estejamos em lados opostos.$",
))
patch(base.MUSEUM_TARGETS, "SlateportCity_OceanicMuseum_1F_Text_YouHaveToTakeThis", (
    "HORIZONTE: Sua bolsa esta cheia?\\p", "Volte com espaco. Ainda preciso\\n",
    "lhe entregar essa TM.$",
))

render_city = base.render_city
render_museum = base.render_museum
CITY_TARGETS = base.CITY_TARGETS
MUSEUM_TARGETS = base.MUSEUM_TARGETS
CITY_PATH = base.CITY_PATH
MUSEUM_PATH = base.MUSEUM_PATH


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
