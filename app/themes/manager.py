"""
ThemeManager singleton — loads, applies, and persists theme selection.

Uses a simple JSON file in the config directory for persistence.
Theme changes propagate via the QSS stylesheet applied to QApplication.
"""

import json
from pathlib import Path
from typing import Optional

from app.themes.base import ThemeName, ThemePalette, all_theme_names, get_palette

_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "theme.json"


class ThemeManager:
    """Singleton managing the active theme and its persistence."""

    _instance: Optional["ThemeManager"] = None

    def __new__(cls) -> "ThemeManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._current: ThemeName = self._load()
        self._callbacks: list = []  # list of callables: (ThemeName) -> None

    # -- public API -----------------------------------------------------------

    @property
    def current(self) -> ThemeName:
        return self._current

    @property
    def palette(self) -> ThemePalette:
        return get_palette(self._current)

    def set_theme(self, name: ThemeName) -> None:
        self._current = name
        self._save(name)
        for cb in self._callbacks:
            cb(name)

    def cycle_theme(self, steps: int = 1) -> ThemeName:
        names = all_theme_names()
        idx = (names.index(self._current) + steps) % len(names)
        self.set_theme(names[idx])
        return self._current

    def next_theme(self) -> ThemeName:
        return self.cycle_theme(1)

    def subscribe(self, callback) -> None:
        """Subscribe to theme change events."""
        self._callbacks.append(callback)

    def unsubscribe(self, callback) -> None:
        self._callbacks.remove(callback)

    def available_themes(self) -> list[ThemeName]:
        return all_theme_names()

    # -- persistence ----------------------------------------------------------

    def _load(self) -> ThemeName:
        try:
            data = json.loads(_CONFIG_PATH.read_text())
            name = data.get("theme", "unsc_green")
            if name in ThemeName.__members__:
                return ThemeName(name)
        except Exception:
            pass
        return ThemeName.UNSC_GREEN

    def _save(self, name: ThemeName) -> None:
        _CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        _CONFIG_PATH.write_text(json.dumps({"theme": name.value}, indent=2) + "\n")
