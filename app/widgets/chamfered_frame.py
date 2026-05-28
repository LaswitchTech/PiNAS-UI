"""
ChamferedFrame — background frame with visible chamfered-border.

Draws a black background with a visible chamfered-rectangle border
matching the physical bezel's 45-degree corners (11.5mm / 98px).
All child widgets are clipped to the inner polygon.
"""

from PyQt6.QtCore import Qt, QRectF, QSize, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QPolygonF, QRegion, QPolygon
from PyQt6.QtWidgets import QFrame


# Layout constants (pixels at 480x800 on 4.3" display)
_MARGIN = 100  # 2px gutter + 98px chamfer inset
_CHAMFER = 98  # 11.5mm at ~217 DPI


def _make_chamfered_rect(width: int, height: int) -> QPolygonF:
    """Return the chamfered-rectangle polygon (integer coords)."""
    pts = [
        QPointF(_MARGIN, _MARGIN),
        QPointF(width - _MARGIN, _MARGIN),
        QPointF(width, _MARGIN + _CHAMFER),
        QPointF(width, height - _MARGIN - _CHAMFER),
        QPointF(width - _MARGIN, height - _MARGIN),
        QPointF(_MARGIN, height - _MARGIN),
        QPointF(0, height - _MARGIN - _CHAMFER),
        QPointF(0, _MARGIN + _CHAMFER),
    ]
    return QPolygonF(pts)


def _make_chamfered_region(width: int, height: int) -> QRegion:
    """Return a QRegion for clipping to the inner chamfered area."""
    return QRegion(_make_chamfered_rect(width, height))


class ChamferedFrame(QFrame):
    """QFrame with a chamfered visible border and clipped children."""

    def __init__(
        self,
        border_color: str = "#00ff88",
        border_width: int = 2,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._border_color = QColor(border_color)
        self._border_width = border_width
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet("QFrame { background-color: #000000; }")

    def paintEvent(self, event) -> None:  # type: ignore[override]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Chamfered border line
        pen = QPen(self._border_color, self._border_width)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawPolygon(_make_chamfered_rect(self.width(), self.height()))

    def resizeEvent(self, event) -> None:  # type: ignore[override]
        super().resizeEvent(event)
        # Clip children to the inner chamfered area
        region = QRegion(QPolygon([p.toPoint() for p in _make_chamfered_rect(self.width(), self.height())]))
        self.setMask(region)

    def minimumSizeHint(self) -> QSize:  # type: ignore[override]
        return QSize(2 * _MARGIN + 1, 2 * _MARGIN + 1)
