#!/usr/bin/env python3
"""
PiNAS UI — Application entry point.

Launches the main window with splash screen. All configuration is
loaded from config/app.json at runtime.
"""

import sys
import logging
from pathlib import Path

# Add project root to path so app package resolves
sys.path.insert(0, str(Path(__file__).resolve().parent))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from app.app import MainWindow, SplashScreen

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("PiNAS")
    app.setOrganizationName("LaswitchTech")

    # Set default font
    font = QFont("monospace", 12)
    app.setFont(font)

    # Show splash
    splash = SplashScreen(duration_ms=1500)
    splash.show_splash(app)

    # Show main window after splash
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
