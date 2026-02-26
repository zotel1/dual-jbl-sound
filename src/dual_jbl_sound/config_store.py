from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ConfigStore:
    base_dir: Path | None = None

    def _default_base_dir(self) -> Path:
        return Path.home() / ".config" / "dual-jbl-sound"

    def _config_path(self) -> Path:
        base = self.base_dir or self._default_base_dir()
        return base / "config.json"

    def load(self) -> dict[str, Any] | None:
        path = self._config_path()
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def save(self, data: dict[str, Any]) -> None:
        path = self._config_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")

    def clear(self) -> None:
        path = self._config_path()
        if path.exists():
            path.unlink()
