"""
Background system poller service.

Runs in a QThread and emits updated metrics via Qt signals.
Catches all exceptions to prevent crashing the UI if a metric source
fails (e.g. missing /sys/class/thermal).
"""

import logging
import platform
import socket
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

import psutil
from PyQt6.QtCore import QThread, pyqtSignal

logger = logging.getLogger(__name__)


@dataclass
class SystemMetrics:
    """Immutable snapshot of all polled system metrics."""
    cpu_percent: float = 0.0
    cpu_count: int = 0
    memory_used: float = 0.0
    memory_total: float = 0.0
    memory_percent: float = 0.0
    storage_used: float = 0.0
    storage_total: float = 0.0
    storage_percent: float = 0.0
    uptime_seconds: float = 0.0
    hostname: str = ""
    ipv4: str = "N/A"
    temperature: float = 0.0
    temperature_unit: str = "°C"
    timestamp: datetime = field(default_factory=datetime.now)


def _get_uptime() -> float:
    """Return system uptime in seconds."""
    boot_time = psutil.boot_time()
    return (datetime.now() - datetime.fromtimestamp(boot_time)).total_seconds()


def _get_hostname() -> str:
    """Return system hostname."""
    try:
        return socket.gethostname()
    except Exception:
        return "N/A"


def _get_ipv4() -> str:
    """Return primary IPv4 address via connectivity check."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        addr = s.getsockname()[0]
        s.close()
        return addr
    except Exception:
        return "N/A"


def _get_temperature() -> tuple[float, str]:
    """Return system temperature reading.

    Falls back to CPU thermal zone or /sys/class/thermal.
    Returns (temperature, unit) — returns (0, "°C") if unreadable.
    """
    # Try psutil sensors (requires Linux with kernel thermal support)
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            # Use first available entry
            for name, entries in temps.items():
                if entries:
                    return entries[0].current, "°C"
    except Exception:
        pass

    # Try /sys/class/thermal on Raspberry Pi
    try:
        thermal_zones = Path("/sys/class/thermal")
        if thermal_zones.exists():
            zones = sorted(thermal_zones.iterdir())
            if zones:
                tz = zones[0] / "temp"
                if tz.exists():
                    return float(tz.read_text().strip()) / 1000.0, "°C"
    except Exception:
        pass

    return 0.0, "°C"


class SystemPoller(QThread):
    """Background thread that polls system metrics periodically.

    Emits `metrics_updated(SystemMetrics)` with a fresh snapshot each cycle.
    All exceptions are caught to ensure the UI never crashes from a bad poll.
    """

    metrics_updated = pyqtSignal(SystemMetrics)

    def __init__(self, interval_ms: int = 2000) -> None:
        super().__init__()
        self._interval_ms = interval_ms
        self._running = True

    def run(self) -> None:
        """Main polling loop. Runs until stop() is called."""
        while self._running:
            try:
                metrics = self._poll()
                self.metrics_updated.emit(metrics)
            except Exception:
                logger.exception("System poller error — metrics will be stale")
            self.msleep(self._interval_ms)

    def stop(self) -> None:
        """Request the poller to stop."""
        self._running = False

    def wait_for_stop(self, timeout_ms: int = 5000) -> None:
        """Block until the poller has stopped."""
        self.stop()
        self.wait(timeout_ms)

    def _poll(self) -> SystemMetrics:
        """Collect all metrics into a snapshot."""
        try:
            cpu_pct = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count(logical=True)
        except Exception:
            cpu_pct, cpu_count = 0.0, 0

        try:
            mem = psutil.virtual_memory()
            mem_used = mem.used / (1024 ** 3)
            mem_total = mem.total / (1024 ** 3)
            mem_pct = mem.percent
        except Exception:
            mem_used, mem_total, mem_pct = 0.0, 0.0, 0.0

        try:
            disk = psutil.disk_usage("/")
            stor_used = disk.used / (1024 ** 3)
            stor_total = disk.total / (1024 ** 3)
            stor_pct = disk.percent
        except Exception:
            stor_used, stor_total, stor_pct = 0.0, 0.0, 0.0

        try:
            uptime = _get_uptime()
        except Exception:
            uptime = 0.0

        try:
            hostname = _get_hostname()
        except Exception:
            hostname = "N/A"

        try:
            ipv4 = _get_ipv4()
        except Exception:
            ipv4 = "N/A"

        try:
            temp, unit = _get_temperature()
        except Exception:
            temp, unit = 0.0, "°C"

        return SystemMetrics(
            cpu_percent=cpu_pct, cpu_count=cpu_count,
            memory_used=mem_used, memory_total=mem_total, memory_percent=mem_pct,
            storage_used=stor_used, storage_total=stor_total, storage_percent=stor_pct,
            uptime_seconds=uptime, hostname=hostname, ipv4=ipv4,
            temperature=temp, temperature_unit=unit,
        )
