"""
MainWindow — PiNAS UI application with swipeable screen container.

Manages:
- Screen container with horizontal swipe transitions
- Theme application via QSS stylesheet
- System poller integration
- Splash screen
"""

import json
import logging
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QSize
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QLabel, QFrame,
)

from app.themes.base import ThemeName, ThemePalette, all_theme_names
from app.themes.manager import ThemeManager
from app.themes.base import generate_qss
from app.services.system_poller import SystemPoller, SystemMetrics
from app.screens.system_screen import SystemScreen
from app.screens.storage_screen import StorageScreen
from app.screens.settings_screen import SettingsScreen
from app.widgets.chamfered_frame import ChamferedFrame

logger = logging.getLogger(__name__)


class SplashScreen(QMainWindow):
    """Animated splash screen shown during app startup."""

    def __init__(self, duration_ms: int = 1500) -> None:
        super().__init__(None)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(480, 800)

        # Center on screen
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2,
        )

        self._fade_out = QPropertyAnimation(self, b"windowOpacity")
        self._fade_out.setDuration(duration_ms)
        self._fade_out.setStartValue(1.0)
        self._fade_out.setEndValue(0.0)
        self._fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._fade_out.finished.connect(self.close)

    def paintEvent(self, event) -> None:  # type: ignore[override]
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(10, 10, 10))

        # Logo
        logo_path = Path(__file__).resolve().parents[1] / "assets" / "logo.svg"
        if logo_path.exists():
            pixmap = QPixmap(str(logo_path))
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                x = (self.width() - scaled.width()) // 2
                y = (self.height() - scaled.height()) // 2 - 40
                painter.drawPixmap(x, y, scaled)

        # Title
        painter.setPen(QColor(0, 255, 136))
        painter.setFont(QFont("monospace", 28, QFont.Weight.Bold))
        painter.drawText(
            QRect((self.width() - 160) // 2, self.height() // 2 + 20, 160, 40),
            Qt.AlignmentFlag.AlignCenter,
            "PiNAS",
        )

        # Version
        painter.setPen(QColor(100, 100, 100))
        painter.setFont(QFont("monospace", 10))
        painter.drawText(
            QRect((self.width() - 100) // 2, self.height() // 2 + 60, 100, 20),
            Qt.AlignmentFlag.AlignCenter,
            "v0.1.0",
        )

        # Footer
        painter.setPen(QColor(60, 60, 60))
        painter.setFont(QFont("monospace", 9))
        painter.drawText(
            QRect(0, self.height() - 40, self.width(), 20),
            Qt.AlignmentFlag.AlignCenter,
            "LASWITCHTECH",
        )

        painter.end()

    def show_splash(self, app: QApplication) -> None:
        """Show the splash screen, then fade it out."""
        self.show()
        app.processEvents()
        self._fade_out.start()


class ScreenContainer(QWidget):
    """Swipeable screen container with animated transitions."""

    def __init__(self, parent: Optional[QMainWindow] = None) -> None:
        super().__init__(parent)

        # Screens
        self._screens: list = []
        self._current_index = 0

        # Stack widget for screen content
        self._stack = QStackedWidget(self)
        self._stack.setContentsMargins(0, 0, 0, 0)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._stack)

        # Page indicators
        self._indicators: list[QFrame] = []
        indicator_frame = self._make_indicators()
        layout.addWidget(indicator_frame)

    def add_screen(self, screen: object, name: str = "") -> None:
        """Add a screen to the container."""
        self._screens.append(screen)
        content = screen.build_content()
        content.setObjectName(name)
        self._stack.addWidget(content)
        self._indicators.append(QFrame())

        # Update page indicator
        if hasattr(screen, 'on_enter'):
            screen.on_enter()

    def _make_indicators(self) -> QWidget:
        """Create page dot indicators at bottom."""
        frame = QWidget()
        frame.setFixedHeight(30)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        for i in range(len(self._screens)):
            dot = QFrame(frame)
            dot.setFixedSize(8, 8)
            dot.setStyleSheet(self._indicator_style(i == 0))
            layout.addWidget(dot)
            self._indicators.append(dot)

        layout.addStretch(1)
        return frame

    def _indicator_style(self, active: bool) -> str:
        color = "#00ff88" if active else "#333333"
        return f"QFrame {{ background-color: {color}; border-radius: 4px; }}"

    def _update_indicators(self) -> None:
        for i, dot in enumerate(self._indicators[len(self._screens):]):
            dot.setStyleSheet(self._indicator_style(i == self._current_index))

    def go_to(self, index: int) -> None:
        """Navigate to a specific screen index with animation."""
        if index < 0 or index >= len(self._screens) or index == self._current_index:
            return

        # Animate transition
        current_widget = self._stack.currentWidget()
        direction = 1 if index > self._current_index else -1

        # Simple stack transition
        self._stack.setCurrentIndex(index)

        # Exit/enter callbacks
        if hasattr(self._screens[self._current_index], 'on_exit'):
            self._screens[self._current_index].on_exit()
        if hasattr(self._screens[index], 'on_enter'):
            self._screens[index].on_enter()

        self._current_index = index
        self._update_indicators()

    def swipe_left(self) -> None:
        """Swipe to next screen."""
        self.go_to(self._current_index + 1)

    def swipe_right(self) -> None:
        """Swipe to previous screen."""
        self.go_to(self._current_index - 1)

    def current_index(self) -> int:
        return self._current_index


class MainWindow(QMainWindow):
    """Main application window with swipeable screens and theme system."""

    def __init__(self) -> None:
        super().__init__()
        self._theme_manager = ThemeManager()
        self._poller: Optional[SystemPoller] = None
        self._config = self._load_config()

        self._init_window()
        self._build_ui()
        self._apply_theme(self._theme_manager.current)
        self._start_poller()
        self._theme_manager.subscribe(self._on_theme_changed)

    # -- Window setup ------ --------- -- -------- ---------- --------- ---------

    def _init_window(self) -> None:
        screen_cfg = self._config.get("screen", {"width": 480, "height": 800})
        self.setWindowTitle("PiNAS")
        self.resize(screen_cfg.get("width", 480), screen_cfg.get("height", 800))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    # -- Config ------ -------------- ---------- ---------- --------- ---------

    def _load_config(self) -> dict:
        config_path = Path(__file__).resolve().parents[2] / "config" / "app.json"
        try:
            return json.loads(config_path.read_text())
        except Exception:
            return {}

    # -- Theme ------ -------------------------- ---------- --------- ---------

    def _apply_theme(self, theme_name: ThemeName) -> None:
        palette = self._theme_manager.palette
        qss = generate_qss(palette, self._config.get("ui", {}).get("font_size", 12))
        self.setStyleSheet(qss)

        # Update accent colors on widgets
        self._update_gauge_colors(palette.primary)

    def _update_gauge_colors(self, hex_color: str) -> None:
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        for screen in self._screens:
            if hasattr(screen, '_gauges'):
                for gauge in screen._gauges:
                    gauge.set_color(r, g, b)

    def _on_theme_changed(self, theme_name: ThemeName) -> None:
        self._apply_theme(theme_name)

    # -- Poller ------ --------------------- ---------- --------- ---------

    def _start_poller(self) -> None:
        poll_cfg = self._config.get("polling", {})
        interval = poll_cfg.get("interval_ms", 2000)
        self._poller = SystemPoller(interval_ms=interval)
        self._poller.metrics_updated.connect(self._on_metrics_updated)
        self._poller.start()

    def _on_metrics_updated(self, metrics: SystemMetrics) -> None:
        """Handle metrics from the poller. Must be called from GUI thread."""
        for screen in self._screens:
            if hasattr(screen, 'update_metrics'):
                screen.update_metrics(metrics)

    # -- UI construction ------ -- -------- ---------- --------- ---------

    def _build_ui(self) -> None:
        # Create screen instances
        self._screens = [
            SystemScreen(self),
            StorageScreen(self),
            SettingsScreen(self),
        ]

        # Chamfered border frame (clips children to inner area)
        self._chamfered_frame = ChamferedFrame()
        root_layout = QVBoxLayout(self._chamfered_frame)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        root_layout.addWidget(self._make_screen_container())
        self.setCentralWidget(self._chamfered_frame)

    def _make_screen_container(self) -> QWidget:
        """Build the swipeable screen container."""
        self._container = ScreenContainer(self._chamfered_frame)
        for i, screen in enumerate(self._screens):
            self._container.add_screen(screen, name=f"screen_{i}")
        return self._container

    # -- Touch/swipe handling ------ -- -------- ---------- ---------

    def mousePressEvent(self, event) -> None:  # type: ignore[override]
        if event.button() == Qt.MouseButton.LeftButton:
            self._press_x = event.position().x()

    def mouseReleaseEvent(self, event) -> None:  # type: ignore[override]
        if hasattr(self, '_press_x'):
            dx = event.position().x() - self._press_x
            if abs(dx) > 50:  # Swipe threshold
                if dx < 0:
                    self._container.swipe_left()
                else:
                    self._container.swipe_right()

    def wheelEvent(self, event) -> None:  # type: ignore[override]
        """Scroll/wheel also navigates screens."""
        if event.angleDelta().y() > 0:
            self._container.swipe_right()
        else:
            self._container.swipe_left()

    # -- Lifecycle ------ ----------------- ---------- --------- ---------

    def closeEvent(self, event) -> None:  # type: ignore[override]
        if self._poller:
            self._poller.wait_for_stop()
        event.accept()
