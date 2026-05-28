"""
ChamferedFrame — visible chamfered border matching the physical bezel.

Draws a black background with a green chamfered rectangle border
that sits inside the physical bezel's corner cutouts.

Physical specs:
  Screen: 55mm (w) x 96mm (h), 480x800 px
  Chamfer: 45-degree cut, 8mm legs on each axis (hypothenuse ~11.3mm)
  Border offset: 3px from the chamfer line toward the bezel edge

Pixel conversions:
  Width:  480 / 55  = 8.727 px/mm
  Height: 800 / 96  = 8.333 px/mm
  Chamfer: 70px (w) x 67px (h)
  Margin:  3px
"""

from PyQt6.QtCore import Qt, QSize, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QPolygonF, QRegion
from PyQt6.QtWidgets import QFrame


# ---------------------------------------------------------------------------
# Physical dimensions -> pixels
# ---------------------------------------------------------------------------
_SCREEN_W_MM, _SCREEN_H_MM = 55, 96
_SCREEN_W_PX, _SCREEN_H_PX = 480, 800

_PPM_X = _SCREEN_W_PX / _SCREEN_W_MM   # 8.727
_PPM_Y = _SCREEN_H_PX / _SCREEN_H_MM   # 8.333

_CHAMFER_MM = 8

# Pixel margin between chamfer tip and inner UI edge
_MARGIN = 3

_CHAMFER_X = int(round(_CHAMFER_MM * _PPM_X))   # 70
_CHAMFER_Y = int(round(_CHAMFER_MM * _PPM_Y))   # 67


def _make_chamfered_polygon(w: int, h: int) -> QPolygonF:
    """Return the 8-point chamfered-rectangle polygon for the border line.

    The chamfer tip sits exactly at the screen edge corners.
    The border line starts {_MARGIN}px past each chamfer endpoint.
    """
    return QPolygonF([
        # Top edge: start from left margin
        QPointF(_MARGIN, 0),
        # Top-right chamfer: from top edge inward
        QPointF(_CHAMFER_X + _MARGIN, 0),
        # Top-right chamfer line: down to right edge
        QPointF(_SCREEN_W_PX, _CHAMFER_Y - _MARGIN),
        # Right edge
        QPointF(_SCREEN_W_PX, h - _CHAMFER_Y + _MARGIN),
        # Bottom-right chamfer line: to bottom edge
        QPointF(_CHAMFER_X + _MARGIN, h),
        # Bottom edge
        QPointF(_MARGIN, h),
        # Bottom-left chamfer: to left edge
        QPointF(0, h - _CHAMFER_Y + _MARGIN),
        # Bottom-left chamfer line: up to top
        QPointF(0, _CHAMFER_Y - _MARGIN),
    ])


def _make_chamfered_region(w: int, h: int) -> QRegion:
    """Return a QRegion for clipping children to the inner chamfered area.

    The inner region starts at the chamfer endpoints on each axis.
    """
    return QRegion(QPolygonF([
        # Top-left chamfer line (top endpoint first)
        QPointF(_CHAMFER_X, 0),
        QPointF(0, _CHAMFER_Y),
        # Left edge
        QPointF(0, h - _CHAMFER_Y),
        # Bottom-left chamfer line
        QPointF(_CHAMFER_X, h),
        # Bottom edge
        QPointF(w - _CHAMFER_X, h),
        # Bottom-right chamfer line
        QPointF(w, h - _CHAMFER_Y),
        # Right edge
        QPointF(w, _CHAMFER_Y),
        # Top-right chamfer line
        QPointF(w - _CHAMFER_X, 0),
    ]).toPolygon())


class ChamferedFrame(QFrame):
    """QFrame with black bg + green chamfered border line + clipped children."""

    def __init__(
        self,
        border_color: str = "#00ff88",
        border_width: int = 2,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._border_color = QColor(border_color)
        self._border_width = border_width
        self.setStyleSheet("QFrame { background-color: #000000; }")

    def paintEvent(self, event) -> None:  # type: ignore[override]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(self._border_color, self._border_width)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawPolygon(_make_chamfered_polygon(self.width(), self.height()))

    def resizeEvent(self, event) -> None:  # type: ignore[override]
        super().resizeEvent(event)
        self.setMask(_make_chamfered_region(self.width(), self.height()))

    def minimumSizeHint(self) -> QSize:  # type: ignore[override]
        return QSize(_CHAMFER_X + _MARGIN + 1, _CHAMFER_Y + _MARGIN + 1)
