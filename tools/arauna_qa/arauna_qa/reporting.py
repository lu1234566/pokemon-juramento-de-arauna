from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .scenario import ScenarioResult


_SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9._-]+")


def safe_artifact_name(value: str) -> str:
    cleaned = _SAFE_NAME_RE.sub("_", value.strip()).strip("._-")
    return cleaned or "scenario"


@dataclass(frozen=True)
class ScenarioBundleResult:
    directory: str
    result_json: str
    screenshot: str | None
    save_state: str | None
    capture_errors: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ScenarioReporter:
    """Persist a scenario trace and capture failure evidence from mGBA."""

    def __init__(self, bridge):
        self.bridge = bridge

    def write(
        self,
        result: ScenarioResult,
        directory: str | Path,
        *,
        capture_failure: bool = True,
        save_failure_state: bool = True,
    ) -> ScenarioBundleResult:
        root = Path(directory)
        root.mkdir(parents=True, exist_ok=True)
        stem = safe_artifact_name(result.name)

        result_path = root / f"{stem}.result.json"
        result_path.write_text(
            json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        screenshot_path: Path | None = None
        state_path: Path | None = None
        errors: list[str] = []

        if capture_failure and not result.success:
            screenshot_path = root / f"{stem}.failure.png"
            try:
                self.bridge.screenshot(str(screenshot_path))
            except Exception as exc:
                errors.append(f"screenshot: {exc}")
                screenshot_path = None

            if save_failure_state:
                state_path = root / f"{stem}.failure.ss0"
                try:
                    self.bridge.save_state(str(state_path))
                except Exception as exc:
                    errors.append(f"save_state: {exc}")
                    state_path = None

        manifest = ScenarioBundleResult(
            directory=str(root),
            result_json=str(result_path),
            screenshot=str(screenshot_path) if screenshot_path is not None else None,
            save_state=str(state_path) if state_path is not None else None,
            capture_errors=tuple(errors),
        )
        manifest_path = root / f"{stem}.bundle.json"
        manifest_path.write_text(
            json.dumps(manifest.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return manifest
