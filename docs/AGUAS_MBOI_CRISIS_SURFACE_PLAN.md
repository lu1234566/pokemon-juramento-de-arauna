# Águas de M'Boi crisis visible-surface cleanup

The mandatory Sootopolis crisis uses the correct Arauna cast in a few places, but several state-specific conversations are still broken: Seu Bento repeats the same unrelated memory monologue across multiple states, Amalia repeats her League-debt speech, one block still starts with `WALLACE:` in English, and another mixes `LEMBRANTES and AQUA`.

## Prepared continuity

Ten existing string blocks become state-specific without changing their callers:

- Seu Bento identifies the Groudon/Kyogre crisis and leads the player to Amalia at the Cave of Origin;
- at the cave entrance he explains why Amalia is there;
- during the search he reacts to Amalia's plan, Torre Juramento and Rayquaza;
- after the faction leaders leave he acknowledges Luzia/Otacilio and the remaining city risk;
- Amalia tells the player to continue to Torre Juramento when needed;
- before the leaders depart she asks the player to hear Luzia and Otacilio's explanation;
- after the crisis she thanks the player and hands over the same HM reward;
- once the reward has been given, she directs the player to Dona Celina's gym.

`SootopolisCity_Text_ExplainWaterfallGoToGym` is intentionally excluded because the badge integration PR owns the visible badge/HM explanation in that block.

## Safety boundary

Only `.string` blocks in `data/maps/SootopolisCity/scripts.inc` are targeted. Wallace/Steven/Archie/Maxie event labels and object IDs, `VAR_SOOTOPOLIS_CITY_STATE`, weather/legendary scenes, faction-leader leave flag, `ITEM_HM_WATERFALL`, Waterfall flag, gym door state, movements, maps, saves and progression remain unchanged.

This is preparation-only while GitHub Actions quota is exhausted and while the badge PR is stabilizing. Activate from the newest canonical main after that PR lands; Codespaces remains last resort.
