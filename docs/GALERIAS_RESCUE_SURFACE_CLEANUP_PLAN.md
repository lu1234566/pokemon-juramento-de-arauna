# Galerias da Serra rescue surface cleanup

The Route 116 / Rusturf Tunnel rescue sequence still exposes Peeko, Mr. Briney, Devon, Rustboro and Rusturf wording and remains largely in English. It also inherits the same Aqua/Devon structural collision as the early woods scene.

## Canonical reinterpretation

The visible location is Galerias da Serra. The kidnapped Pokémon is simply the barqueiro's companion rather than an Emerald-specific named Peeko. The inherited Aqua grunt appears as an `AGENTE HORIZONTE` executing an off-record containment order to seize the package/data. That keeps the already-established Horizonte battle class and overworld identity while explaining why the agent's action can conflict with the later public-facing Consórcio delivery chain.

The nearby researcher later thanks the player for recovering records and completing the delivery, then grants the same Repeat Ball using the original item/progression path.

## Safety boundary

Only selected `.string` bodies across Route 116 and Rusturf Tunnel change. The stolen-goods item ID, Repeat Ball reward, Wingull/species object, HM Strength sequence, trainer party, battle trigger, flags, variables, object IDs, movements, warps and progression remain unchanged. Internal Devon/Briney/Rusturf labels stay as the Emerald implementation skeleton.

## Activation

Activate from the newest green `main` after GitHub Actions runners resume. Wire the deterministic tool into the shared cleanup runner, generate/check both map scripts, add a final user-authored validation commit and require a successful full custom Emerald ROM build before merge.
