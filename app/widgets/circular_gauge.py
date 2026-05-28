"""
Circular gauge widget — HUD-style radial progress indicator.

Draws an arc-based gauge with center text showing the current value.
Supports custom colors, ranges, and labels. All drawing done via QPainter
for performance on embedded hardware.
"""

import math
from PyQt6.QtCore import Qt, QRectF, QPointF, QLineF
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QConicalGradient
from PyQt6.QtWidgets import QWidget


class CircularGauge(QWidget):
    """Radial HUD gauge for displaying single-value metrics (CPU, RAM, temp)."""

    def __init__(
        self,
        value: float = 0.0,
        minimum: float = 0.0,
        maximum: float = 100.0,
        label: str = "",
        unit: str = "",
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._value = value
        self._minimum = minimum
        self._maximum = maximum
        self._label = label
        self._unit = unit
        self._color = QColor(0, 255, 136)
        self._glow_color = QColor(0, 255, 136, 40)

        self.setFixedSize(160, 180)
        self.setMinimumHeight(120)

    def set_value(self, value: float) -> None:
        """Update the gauge value. Triggers a repaint."""
        if self._maximum <= self._minimum:
            return
        self._value = max(self._minimum, min(value, self._maximum))
        self.update()

    def set_color(self, r: int, g: int, b: int) -> None:
        """Set the gauge arc color."""
        self._color = QColor(r, g, b)
        self._glow_color = QColor(r, g, b, 40)
        self.update()

    def set_label(self, label: str) -> None:
        self._label = label
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
        center_x = width / 2
        center_y = height * 0.45  # Shift gauge up to leave room for label

        # Dimensions
        radius = min(width, height * 0.5) * 0.75
        arc_width = 10
        start_angle = 135 * 16  # Qt uses 1/16 degree units
        arc_span = 270 * 16      # 270-degree arc

        # Background arc
        bg_rect = QRectF(
            center_x - radius, center_y - radius,
            radius * 2, radius * 2,
        )
        bg_pen = QPen(QColor(30, 30, 30), arc_width)
        bg_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(bg_rect, start_angle, arc_span)

        # Value arc
        ratio = (self._value - self._minimum) / (self._maximum - self._minimum) if self._maximum > self._minimum else 0
        value_span = int(ratio * arc_span)
        value_pen = QPen(self._color, arc_width)
        value_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(value_pen)
        painter.drawArc(bg_rect, start_angle, -value_span)

        # Tick marks
        tick_color = QColor(self._color)
        tick_color.setAlpha(80)
        painter.setPen(QPen(tick_color, 1))
        for i in range(11):
            angle = math.radians(135 + (i / 10) * 270)
            inner_r = radius - arc_width / 2 - 4
            outer_r = radius - arc_width / 2 - 10
            x1 = center_x + inner_r * math.cos(angle)
            y1 = center_y + inner_r * math.sin(angle)
            x2 = center_x + outer_r * math.cos(angle)
            y2 = center_y + outer_r * math.sin(angle)
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        # Center text
        value_text = self._format_value(self._value)
        font = QFont("monospace", 22, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QPen(self._color))
        painter.drawText(
            QRectF(center_x - 60, center_y - 10, 120, 36),
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
            value_text,
        )

        # Unit
        if self._unit:
            unit_font = QFont("monospace", 10)
            painter.setFont(unit_font)
            painter.setPen(QPen(QColor(128, 128, 128)))
            painter.drawText(
                QRectF(center_x - 40, center_y + 18, 80, 18),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
                self._unit,
            )

        # Label below
        if self._label:
            label_font = QFont("monospace", 9)
            painter.setFont(label_font)
            painter.setPen(QPen(QColor(100, 100, 100)))
            painter.drawText(
                QRectF(0, height - 28, width, 20),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
                self._label.upper(),
            )

        painter.end()

    def _format_value(self, value: float) -> str:
        """Format value for display."""
        if self._maximum <= 100 and self._label in ("CPU", "Memory"):
            return f"{value:.0f}"
        return f"{value:.1f}"
