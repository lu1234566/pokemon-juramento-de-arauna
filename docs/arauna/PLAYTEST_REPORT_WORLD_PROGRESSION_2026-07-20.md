# Runtime playtest report — world progression

Date: 2026-07-20  
Branch: `agent/playtest-feedback-world-progression`  
Scope: accepted non-Pokémon world, navigation, onboarding and field-tool changes

## Build and automated checks

The branch was cloned into a clean local working directory and verified against the remote head before testing.

The following completed successfully:

```bash
bash scripts/run_repository_safety.sh /tmp/arauna-safety.log
make ARAUNA_LANGUAGE=ENGLISH -j2 -O all
TEST=1 make ARAUNA_LANGUAGE=ENGLISH -j2 check
```

Result:

- repository-safety validation passed;
- English ROM `pokeemerald-en.gba` was produced;
- engine test runner completed successfully.

## mGBA runtime route

The compiled ROM was launched in mGBA under a virtual display. Input was sent through the emulator's normal keyboard controls. Screens were sampled throughout the run, and the expected runtime text was verified from those samples.

The tested new-save route was:

1. boot ROM and reach the Arauna opening;
2. begin inside Dona Zila's house;
3. speak with Dona Zila and Professor Anahi;
4. sit with all three rescued partners during the night;
5. reach the dawn transition;
6. feed all three partners;
7. explicitly choose Pimpau;
8. observe Zila's Notebook reward text;
9. observe the full 386-entry Arauna Dex activation text;
10. leave through the house door and use the visible Vila Amanhecer east road;
11. complete the first Mist Route evidence survey;
12. return to Ciro and win the rival battle;
13. follow the stage-8 route through Mist Route;
14. enter the Old Coast Road at Route 110's northern end;
15. cross the full road and reach Porto das Redes from the north;
16. observe Porto's custom arrival identity instead of the Slateport popup;
17. meet Dona Celina;
18. collect all four Porto evidence records;
19. return to Celina and receive the Consortium confrontation objective;
20. defeat the Consortium Agent;
21. complete Celina's refrain;
22. restore Iaraco at the shoreline;
23. record the Iara-Mãe Testimony;
24. return to Celina and win the Maré Trial;
25. receive the Maré Badge;
26. receive the Tide Board from the Porto boatbuilder;
27. face verified surfable water with no party member taught Surf;
28. receive and accept the Tide Board prompt;
29. enter the water and confirm that the game remained responsive by opening the Start menu.

## Runtime results

### Passed

- new-save Arauna opening;
- night-to-dawn care sequence;
- explicit partner confirmation;
- Notebook reward and Dex activation;
- visible Vila exit;
- Mist Route survey progression;
- Ciro battle and stage-8 transition;
- full Route 110 coast-road traversal;
- Porto custom arrival;
- four-evidence investigation flow;
- Consortium Agent battle;
- Iara-Mãe Testimony;
- Maré Trial and badge reward;
- Tide Board reward;
- Tide Board prompt and calm-water entry without teaching Surf;
- continued emulator responsiveness after entering the water.

### Not yet covered by this run

- Caramelo and Quero partner branches;
- Tide Board behavior with a multi-Pokémon party;
- Tide Board behavior with a fainted lead Pokémon;
- human pixel-by-pixel visual approval of every Porto and coast-road object placement;
- long-session save/load regression;
- performance testing on original GBA hardware or flash cartridges.

## Visual verification method

This was an automated smoke playthrough rather than a replacement for human art direction. Screenshots were captured at major checkpoints, including:

- Arauna opening;
- partner-choice reward chain;
- Ciro battle;
- Porto arrival;
- Consortium Agent defeat;
- Maré Badge;
- Tide Board prompt;
- Tide Board water state.

The route and interactions were validated through the actual compiled ROM. Final visual composition still requires user review before the draft pull request is merged.

## Scope protection

No Fakemon design, battle sprite, back sprite, shiny palette, species data or Oxum-related creature art was modified during this workstream.

## CI note

GitHub-hosted Actions jobs have been terminating before recording their first step and expose no runner logs. The successful build, engine tests and mGBA route above were therefore executed locally from the current remote branch head.
