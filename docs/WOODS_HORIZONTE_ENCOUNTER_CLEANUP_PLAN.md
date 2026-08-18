# Early woods / Horizonte encounter cleanup

The inherited Petalburg Woods robbery scene currently exposes a particularly confusing mix: the victim is still called a Devon researcher while the attacker was mechanically Team Aqua but has already been surface-renamed to Consórcio Horizonte. That makes the same visible corporate identity appear on both sides of the scene.

## Canonical reinterpretation

The victim is now a generic independent `PESQUISADOR` documenting early Desencanto signs in local Pokémon. The inherited Aqua grunt slot remains an `AGENTE HORIZONTE`, trying to seize the field notes as sensitive data. This fits the established Arauna conflict without inventing a new named character.

The agent's later reference points toward the Consórcio technical center in Serra do Uivo. The researcher keeps the original Great Ball reward and then leaves using the existing event flow.

## Safety boundary

Only twelve `.string` bodies in `data/maps/PetalburgWoods/scripts.inc` are targeted. Trainer ID/party, battle trigger, Great Ball item grant, object IDs, movements, removal flags, map geometry and progression remain unchanged. Internal Devon/Aqua-named labels remain as Emerald implementation skeleton.

## Activation

Activate from the newest green `main` after GitHub Actions jobs can start again. Wire the tool into the shared cleanup runner, generate/check the map script, add a final user-authored validation commit and require a successful full custom Emerald ROM build before merge.
