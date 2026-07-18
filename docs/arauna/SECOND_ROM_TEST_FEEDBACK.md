# Second ROM test feedback log

This log separates observations made against the first downloaded second-test ROM
from fixes that still require a new build.

## Tested baseline

- Source branch: `agent/second-rom-test-prep`
- Source commit: `4daac149fa5a3995dd1f53d32880badee347f7b9`
- ROM SHA-256:
  `c244df332de8bf06ab81839283b23753382555b60ec6746a8a6d59789f22078b`
- Language: English
- Save contract: new save

## 2026-07-18 immediate feedback

| Severity | Observation | Root cause | Fix status |
| --- | --- | --- | --- |
| Blocker | NEW GAME entered unchanged Littleroot Town | `NewGameInitData` still called the vanilla moving-truck warp; the Arauna maps existed but were unreachable | Fixed on PR #53: new games enter Dona Zila's house |
| Blocker | No 999 Rare Candies after keeping the starter | The one-time supply hook existed only in the unreachable Arauna Research Center choice | Fixed on PR #53: the reachable home confirmation calls the one-time supply hook |
| Major | Oldale Town remained unchanged and kept its vanilla name | The active ROM was still following Route 101 into untouched vanilla progression | Fixed at the identity layer on PR #53 as AMANHECER POST; the canonical campaign no longer uses the vanilla opening path |

## Retest rule

Do not use the baseline ROM above to verify these fixes; compiled ROM files cannot
change after download. Retest them only from a clean English build of
`agent/fix-second-test-entrypoint`, starting from **NEW GAME**.

Additional feedback from the baseline ROM is still useful and should be appended
here with location, reproduction steps, expected behavior, observed behavior and
severity.
