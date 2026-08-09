#!/usr/bin/env python3
"""Keep the CI repository-safety job and the local safety runner in lockstep.

`scripts/run_repository_safety.sh` exists so a developer can run, before every
commit, "the same checks CI runs" (HANDOFF section 7). That promise only holds
if the two lists actually match -- and they had silently drifted apart:

  * scripts/validate_map_symbol_references.py ran in CI only, so the local
    runner missed a link-time build breaker the pre-commit check was meant to
    catch;
  * scripts/validate_priority10_npcs.py ran in the local runner only, so CI
    never enforced it.

Each side was missing a check the other had. This guard resolves the set of
project scripts (scripts/*.{py,sh} and tools/arauna/*.py) invoked by the CI
`repository-safety` job and by the local runner, and fails when they differ.
It has no ARM toolchain dependency, so it runs in the same pure-Python job it
protects.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/build.yml"
RUNNER = ROOT / "scripts/run_repository_safety.sh"

# Any invocation of a checked-in project script; the paths that drifted all
# live under these two trees. Config/lint steps (json.tool on devcontainer.json,
# bash -n on the visual shells) are matched here too via their .sh paths.
SCRIPT_RE = re.compile(r"(?:scripts|tools/arauna)/[A-Za-z0-9_./-]+\.(?:py|sh)")


def scripts_in(text: str) -> set[str]:
    return set(SCRIPT_RE.findall(text))


def main() -> int:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    # Only the repository-safety job; the build-and-test job runs make, not
    # these validators, and must not count toward parity.
    job = workflow.split("build-and-test:", 1)[0]
    if "repository-safety:" not in job:
        print("cannot find repository-safety job in build.yml", file=sys.stderr)
        return 1

    ci = scripts_in(job)
    runner = scripts_in(RUNNER.read_text(encoding="utf-8"))
    # The runner never invokes itself; ignore it if a future edit references it.
    runner.discard("scripts/run_repository_safety.sh")
    ci.discard("scripts/run_repository_safety.sh")

    only_ci = sorted(ci - runner)
    only_runner = sorted(runner - ci)
    if only_ci or only_runner:
        lines = ["CI repository-safety and scripts/run_repository_safety.sh have drifted:"]
        for path in only_ci:
            lines.append(f"  in CI but missing from the runner: {path}")
        for path in only_runner:
            lines.append(f"  in the runner but missing from CI: {path}")
        lines.append("Add each listed check to the other side so both stay in lockstep.")
        print("\n".join(lines), file=sys.stderr)
        return 1

    print(f"Safety check parity confirmed: {len(ci)} checks run in both CI and the local runner.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
