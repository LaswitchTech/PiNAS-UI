"""
HUD Bar widget — linear progress indicator with tactical styling.

Used for storage, network, and other linear metrics. Draws a segmented
bar with accent color matching the active theme.
"""

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtWidgets import QWidget


class HUDBar(QWidget):
    """Linear progress bar with segmented HUD styling."""

    def __init__(
        self,
        value: float = 0.0,
        minimum: float = 0.0,
        maximum: float = 100.0,
        label: str = "",
        color: QColor | None = None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._value = value
        self._minimum = minimum
        self._maximum = maximum
        self._label = label
        self._color = color or QColor(0, 255, 136)
        self.setFixedHeight(32)

    def set_value(self, value: float) -> None:
        if self._maximum <= self._minimum:
            return
        self._value = max(self._minimum, min(value, self._maximum))
        self.update()

    def set_label(self, label: str) -> None:
        self._label = label
        self.update()

    def set_color(self, color: QColor) -> None:
        self._color = color
        self.update()

    def set_range(self, minimum: float, maximum: float) -> None:
        self._minimum = minimum
        self._maximum = maximum
        self.update()

    def paintEvent(self, event) -> None:  # type: ignore[override]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()
        bar_height = 8
        bar_y = (height - bar_height) / 2
        margin = 4

        # Ratio
        ratio = (self._value - self._minimum) / (self._maximum - self._minimum) if self._maximum > self._minimum else 0
        bar_width = max(4, (width - margin * 2) * max(0, min(ratio, 1.0)))

        # Background bar
        bg_pen = QPen(QColor(30, 30, 30), bar_height)
        bg_pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        painter.setPen(bg_pen)
        painter.drawLine(margin, height / 2, width - margin, height / 2)

        # Value bar
        val_color = QColor(self._color)
        val_color.setAlpha(200)
        fill_pen = QPen(val_color, bar_height)
        fill_pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        painter.setPen(fill_pen)
        painter.drawLine(margin, height / 2, margin + bar_width, height / 2)

        # End cap dot
        cap_color = QColor(self._color)
        cap_color.setAlpha(255)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(cap_color)
        cap_x = margin + bar_width
        painter.drawEllipse(QRectF(cap_x - 3, height / 2 - 3, 6, 6))

        # Label
        if self._label:
            painter.setPen(QPen(QColor(100, 100, 100)))
            painter.setFont(QFont("monospace", 9))
            painter.drawText(
                QRectF(0, 0, width, 12),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
                self._label.upper(),
            )

        # Value text below bar
        if self._maximum > 0:
            pct = f"{ratio * 100:.0f}%"
            painter.setPen(QPen(self._color))
            painter.setFont(QFont("monospace", 10, QFont.Weight.Bold))
            painter.drawText(
                QRectF(0, height - 14, width, 14),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom,
                pct,
            )

        painter.end()
