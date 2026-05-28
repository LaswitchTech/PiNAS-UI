"""
Screen 1 — System Overview.

Displays CPU, memory, storage, network, uptime, and temperature using
custom HUD widgets. Updates dynamically from SystemPoller signals.
"""

import math
from typing import Optional

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame,
)

from app.screens.base import BaseScreen
from app.widgets.circular_gauge import CircularGauge
from app.widgets.hud_bar import HUDBar
from app.widgets.info_row import InfoRow
from app.services.system_poller import SystemMetrics


class SystemScreen(BaseScreen):
    """Screen 1 — System Overview dashboard."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._metrics: Optional[SystemMetrics] = None
        self._gauges: list[CircularGauge] = []
        self._bars: list[HUDBar] = []
        self._info_widgets: list[InfoRow] = []
        self._logo_label: Optional[QLabel] = None

    # -- BaseScreen -----------------------------------------------------------

    def build_content(self) -> QWidget:
        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Top branding area
        branding = self._make_branding()
        layout.addWidget(branding)

        # Gauge row: CPU & Memory
        gauge_layout = QGridLayout()
        gauge_layout.setSpacing(12)
        self._gauges = [
            CircularGauge(label="CPU", unit="%"),
            CircularGauge(label="MEMORY", unit="%"),
        ]
        for i, gauge in enumerate(self._gauges):
            gauge.set_range(0, 100)
            gauge.setFixedHeight(160)
            gauge_layout.addWidget(gauge, 0, i)
        layout.addLayout(gauge_layout)

        # Storage bars
        storage_frame = QFrame()
        storage_frame.setProperty("class", "hud-panel")
        storage_layout = QVBoxLayout(storage_frame)
        storage_layout.setContentsMargins(0, 0, 0, 0)
        storage_layout.setSpacing(4)

        stor_label = QLabel("STORAGE")
        stor_label.setProperty("dimmed", "true")
        stor_label.setStyleSheet("font-size: 10px; letter-spacing: 2px; color: #808080; padding: 4px 12px;")
        storage_layout.addWidget(stor_label)

        # ZFS/RAID bar
        self._bars = [
            HUDBar(label="ZFS / RAID", color=(0, 255, 136)),
            HUDBar(label="ROOT (/)", color=(68, 136, 255)),
        ]
        for bar in self._bars:
            bar.setFixedHeight(28)
            storage_layout.addWidget(bar)

        layout.addWidget(storage_frame)

        # Info grid
        info_frame = QFrame()
        info_frame.setProperty("class", "hud-panel")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(0)

        info_label = QLabel("SYSTEM INFO")
        info_label.setProperty("dimmed", "true")
        info_label.setStyleSheet("font-size: 10px; letter-spacing: 2px; color: #808080; padding: 8px 12px 4px 12px;")
        info_layout.addWidget(info_label)

        self._info_widgets = [
            InfoRow("HOSTNAME", "N/A"),
            InfoRow("IPv4", "N/A"),
            InfoRow("UPTIME", "N/A"),
            InfoRow("TEMP", "N/A °C"),
        ]
        for widget in self._info_widgets:
            widget.setFixedHeight(32)
            info_layout.addWidget(widget)

        layout.addWidget(info_frame)

        # Bottom logo
        self._logo_label = QLabel()
        self._logo_label.setFixedSize(60, 60)
        self._logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(self._logo_label, 0, Qt.AlignmentFlag.AlignHCenter)

        return root

    def on_enter(self) -> None:
        """Load logo on screen enter."""
        if self._logo_label:
            from PyQt6.QtGui import QPixmap
            self._logo_label.setPixmap(
                QPixmap("app/assets/logo.svg").scaled(
                    60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                )
            )

    # -- Metric updates --------------------- --- -- -- ------ ---------------

    def update_metrics(self, metrics: SystemMetrics) -> None:
        """Apply a metrics snapshot to the screen widgets."""
        self._metrics = metrics

        # Gauges
        if self._gauges:
            self._gauges[0].set_value(metrics.cpu_percent)
            self._gauges[1].set_value(metrics.memory_percent)

        # Bars
        if self._bars and metrics.storage_total > 0:
            self._bars[0].set_value(metrics.storage_percent)
            self._bars[0].set_label(f"ZFS / RAID ({metrics.storage_used:.1f} / {metrics.storage_total:.1f} GB)")
        if len(self._bars) > 1:
            self._bars[1].set_value(85)  # Placeholder for root partition

        # Info rows
        if len(self._info_widgets) >= 4:
            self._info_widgets[0].set_value(metrics.hostname or "N/A")
            self._info_widgets[1].set_value(metrics.ipv4 or "N/A")
            self._info_widgets[2].set_value(self._format_uptime(metrics.uptime_seconds))
            temp_val = f"{metrics.temperature:.1f} {metrics.temperature_unit}" if metrics.temperature > 0 else "N/A"
            self._info_widgets[3].set_value(temp_val)

            # Color temp based on value
            temp_color = (0, 255, 136)  # green
            if metrics.temperature > 70:
                temp_color = (255, 51, 68)  # red
            elif metrics.temperature > 55:
                temp_color = (255, 170, 0)  # amber
            if metrics.temperature > 0:
                self._info_widgets[3].set_value_color(*temp_color)

    @staticmethod
    def _format_uptime(seconds: float) -> str:
        """Format uptime in days:hours:minutes."""
        if seconds <= 0:
            return "N/A"
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{days}d {hours:02d}h {minutes:02d}m"

    # -- Helpers ------ --------------- --- -- -- ------ --------------------

    def _make_branding(self) -> QWidget:
        """Create top branding strip with logo and title."""
        frame = QFrame()
        frame.setFixedHeight(70)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(12, 8, 12, 4)

        # Logo icon
        logo_label = QLabel()
        logo_label.setFixedSize(44, 44)
        logo_label.setStyleSheet("border: none; background: transparent;")
        try:
            from PyQt6.QtGui import QPixmap
            logo_label.setPixmap(
                QPixmap("app/assets/logo.svg").scaled(
                    44, 44, Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        except Exception:
            logo_label.setText("L")
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_label.setStyleSheet("color: #00ff88; font-size: 28px; font-weight: bold; font-family: monospace;")

        layout.addWidget(logo_label)

        # Title
        title_frame = QFrame()
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)

        title = QLabel("PiNAS")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #00ff88; letter-spacing: 3px;")
        title.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        title_layout.addWidget(title)

        subtitle = QLabel("SYSTEM OVERVIEW")
        subtitle.setStyleSheet("font-size: 9px; color: #808080; letter-spacing: 2px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        title_layout.addWidget(subtitle)

        layout.addWidget(title_frame)
        layout.addStretch(1)

        return frame
