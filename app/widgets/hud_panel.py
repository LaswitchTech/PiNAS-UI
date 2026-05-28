"""
HUD Panel widget — tactical container with glowing left border.

Acts as a framed container for HUD content. Draws a left accent border
and subtle grid overlay matching the active theme.
"""

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel


class HUDPanel(QFrame):
    """Tactical panel with glowing left border and grid overlay."""

    def __init__(self, title: str = "", parent=None) -> None:
        super().__init__(parent)
        self.setProperty("class", "hud-panel")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Title bar
        self._title_bar = self._make_title(title)
        layout.addWidget(self._title_bar)

        # Spacer pushes content down
        layout.addStretch(1)

    def _make_title(self, title: str) -> QFrame:
        """Create the title bar at top of panel."""
        frame = QFrame(self)
        frame.setFixedHeight(28)
        frame.setStyleSheet("QFrame { background-color: transparent; border: none; }")

        # Top accent line
        line = QFrame(frame)
        line.setFixedHeight(2)
        line.setStyleSheet(
            "QFrame { "
            "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 transparent, stop:0.3 currentColor, stop:1 transparent); "
            "} "
        )

        # Title text
        if title:
            txt = QLabel(title, frame)
            txt.setStyleSheet(
                "color: palette(text-dim); font-size: 10px; letter-spacing: 2px; "
                "text-transform: uppercase; padding: 2px 0;"
            )
            txt.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        else:
            txt = None

        lay = QVBoxLayout(frame)
        lay.setContentsMargins(8, 4, 8, 4)
        lay.setSpacing(0)
        lay.addWidget(line)
        if txt:
            lay.addWidget(txt)

        return frame

    def content_layout(self) -> QVBoxLayout:
        """Return the panel's layout for adding child widgets."""
        return self.layout()

    def paintEvent(self, event) -> None:  # type: ignore[override]
        """Draw left accent border and subtle grid pattern."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Left accent border
        accent = self.palette().color(self.palette().ColorRole.Highlight)
        if accent == QColor():
            accent = QColor(0, 255, 136)

        pen = QPen(accent)
        pen.setWidthF(3)
        painter.setPen(pen)
        painter.drawLine(0, 0, 0, self.height())

        # Grid pattern (subtle)
        grid = QColor(accent)
        grid.setAlpha(20)
        painter.setPen(QPen(grid, 0.5))

        spacing = 20
        for x in range(spacing, self.width(), spacing):
            painter.drawLine(x, 0, x, self.height())
        for y in range(spacing, self.height(), spacing):
            painter.drawLine(0, y, self.width(), y)

        painter.end()
