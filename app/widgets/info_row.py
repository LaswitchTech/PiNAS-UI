"""
Info Row widget — key-value pair display for HUD panels.

Used to show labeled metrics like hostname, IP, uptime, etc.
in a clean tactical format.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel


class InfoRow(QWidget):
    """Single line of key:value information for HUD panels."""

    def __init__(self, key: str = "", value: str = "", parent=None) -> None:
        super().__init__(parent)
        self.setFixedHeight(28)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(8)

        self._key_label = QLabel(key, self)
        self._key_label.setProperty("dimmed", "true")
        self._key_label.setStyleSheet("font-size: 10px; letter-spacing: 1px;")
        self._key_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self._value_label = QLabel(value, self)
        self._value_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        self._value_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(self._key_label)
        layout.addSpacing(8)
        layout.addWidget(self._value_label)

    def set_key(self, key: str) -> None:
        self._key_label.setText(key)

    def set_value(self, value: str) -> None:
        self._value_label.setText(value)

    def set_value_color(self, r: int, g: int, b: int) -> None:
        self._value_label.setStyleSheet(
            f"font-size: 12px; font-weight: bold; color: rgb({r}, {g}, {b});"
        )
