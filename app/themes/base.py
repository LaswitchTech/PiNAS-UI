"""
Base theme class and color palette for PiNAS UI.

Provides the ThemePalette dataclass and Theme base class that all
presets inherit from. Colors are applied as QSS (Qt Style Sheets)
across the entire application.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class ThemePalette:
    """Immutable color palette for a single theme."""
    primary: str          # e.g. "#00ff88" — main accent color
    secondary: str        # e.g. "#00cc66" — supporting color
    background: str       # e.g. "#0a0a0a" — dark backdrop
    panel_bg: str         # e.g. "#111111" — panel backgrounds
    panel_border: str     # e.g. "#1a3a2a" — panel borders
    text: str             # e.g. "#e0e0e0" — primary text
    text_dim: str         # e.g. "#808080" — dimmed text
    glow: str             # e.g. "#00ff8840" — glow overlay alpha
    success: str          # e.g. "#00ff88" — healthy state
    warning: str          # e.g. "#ffaa00" — caution state
    danger: str           # e.g. "#ff3344" — error state
    grid_line: str        # e.g. "#1a1a1a" — subtle grid overlay


class ThemeName(str, Enum):
    UNSC_GREEN = "unsc_green"
    BLUE = "blue"
    AMBER = "amber"
    RED = "red"
    PURPLE = "purple"
    WHITE = "white"


# --- Color presets -----------------------------------------------------------

_PALETTES: dict[ThemeName, ThemePalette] = {
    ThemeName.UNSC_GREEN: ThemePalette(
        primary="#00ff88", secondary="#00cc66", background="#000000",
        panel_bg="#0d1a0d", panel_border="#1a3a2a", text="#e0ffe8",
        text_dim="#608060", glow="#00ff8840", success="#00ff88",
        warning="#ffaa00", danger="#ff3344", grid_line="#112211",
    ),
    ThemeName.BLUE: ThemePalette(
        primary="#4488ff", secondary="#3366cc", background="#080a10",
        panel_bg="#0c1020", panel_border="#1a2a4a", text="#d0e0ff",
        text_dim="#607090", glow="#4488ff40", success="#4488ff",
        warning="#ffaa00", danger="#ff3344", grid_line="#111828",
    ),
    ThemeName.AMBER: ThemePalette(
        primary="#ffbb33", secondary="#cc8800", background="#0f0a05",
        panel_bg="#1a1408", panel_border="#3a2a10", text="#fff0d0",
        text_dim="#807050", glow="#ffbb3340", success="#ffbb33",
        warning="#ff6600", danger="#ff3344", grid_line="#221a0a",
    ),
    ThemeName.RED: ThemePalette(
        primary="#ff4444", secondary="#cc2222", background="#0f0808",
        panel_bg="#1a0c0c", panel_border="#3a1a1a", text="#ffe0e0",
        text_dim="#805050", glow="#ff444440", success="#ff4444",
        warning="#ffaa00", danger="#ff1111", grid_line="#221111",
    ),
    ThemeName.PURPLE: ThemePalette(
        primary="#aa55ff", secondary="#8833cc", background="#0a0810",
        panel_bg="#100c1a", panel_border="#2a1a3a", text="#e8d0ff",
        text_dim="#706080", glow="#aa55ff40", success="#aa55ff",
        warning="#ffaa00", danger="#ff3344", grid_line="#1a1128",
    ),
    ThemeName.WHITE: ThemePalette(
        primary="#ffffff", secondary="#cccccc", background="#111111",
        panel_bg="#1a1a1a", panel_border="#333333", text="#f0f0f0",
        text_dim="#888888", glow="#ffffff20", success="#ffffff",
        warning="#ffaa00", danger="#ff3344", grid_line="#222222",
    ),
}


def get_palette(name: ThemeName) -> ThemePalette:
    """Return the palette for the given theme name."""
    return _PALETTES[name]


def all_theme_names() -> list[ThemeName]:
    """Return ordered list of all available theme names."""
    return list(_PALETTES.keys())


# --- QSS generation ----------------------------------------------------------

def _hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
    """Convert hex color to rgba() string."""
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


def generate_qss(palette: ThemePalette, font_size: int = 12) -> str:
    """Generate a full QSS stylesheet from a palette.

    Applied to QApplication at runtime to theme all widgets uniformly.
    """
    p, s, bg, pb = palette.primary, palette.secondary, palette.background, palette.panel_bg
    txt, tdim = palette.text, palette.text_dim
    pb_rgb = _hex_to_rgba(palette.panel_border, 0.5)
    bg_rgb = _hex_to_rgba(bg)
    grid_rgb = _hex_to_rgba(palette.grid_line, 0.3)

    return f"""
        QMainWindow, QApplication {{
            background-color: {bg_rgb};
            color: {txt};
            font-family: monospace;
            font-size: {font_size}px;
        }}

        QWidget {{
            background-color: transparent;
            border: none;
        }}

        QFrame {{
            background-color: {pb_rgb};
            border-left: 2px solid {palette.panel_border};
            border-radius: 0px;
        }}

        QFrame.hud-panel {{
            background-color: transparent;
            border-left: 2px solid {palette.panel_border};
        }}

        QLabel {{
            color: {txt};
            background-color: transparent;
        }}

        QLabel[dimmed] {{
            color: {tdim};
        }}

        QPushButton {{
            background-color: transparent;
            border: 1px solid {p};
            border-left: 3px solid {p};
            color: {p};
            padding: 8px 16px;
            font-family: monospace;
            font-size: {font_size}px;
            text-align: left;
        }}

        QPushButton:hover {{
            background-color: {_hex_to_rgba(p, 0.15)};
            border-color: {s};
            border-left-color: {s};
        }}

        QPushButton:pressed {{
            background-color: {_hex_to_rgba(p, 0.25)};
        }}

        QComboBox {{
            background-color: {_hex_to_rgba(pb, 0.8)};
            border: 1px solid {palette.panel_border};
            border-left: 2px solid {p};
            color: {txt};
            padding: 6px 10px;
            font-family: monospace;
            font-size: {font_size}px;
        }}

        QComboBox::drop-down {{
            border: none;
        }}

        QComboBox QAbstractItemView {{
            background-color: {pb_rgb};
            color: {txt};
            selection-background-color: {_hex_to_rgba(p, 0.2)};
            border: 1px solid {palette.panel_border};
        }}

        QSlider::groove:horizontal {{
            border: 1px solid {palette.panel_border};
            height: 6px;
            background: {grid_rgb};
            border-radius: 0px;
        }}

        QSlider::handle:horizontal {{
            background: {p};
            border: 1px solid {s};
            width: 18px;
            margin: -6px 0;
        }}

        QProgressBar {{
            border: 1px solid {palette.panel_border};
            border-left: 2px solid {p};
            background: {grid_rgb};
            height: 12px;
            text-align: center;
            color: {tdim};
            font-size: {font_size - 2}px;
        }}

        QProgressBar::chunk {{
            background: {p};
            border-radius: 0px;
        }}
    """
