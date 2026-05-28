"""
Screen 3 — Settings (stub).

Placeholder for WiFi, hostname, system controls, and theme customization.
Will be implemented incrementally.
"""

from typing import Optional

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton


class SettingsScreen:
    """Screen 3 — Settings dashboard (stub)."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        self._parent = parent

    def build_content(self) -> QWidget:
        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Title
        title = QLabel("SETTINGS")
        title.setStyleSheet("font-size: 18px; font-weight: bold; letter-spacing: 2px; color: #00ff88;")
        layout.addWidget(title)

        # Settings sections
        sections = [
            ("NETWORK", ["WiFi Configuration", "Hostname", "Network Settings"]),
            ("SYSTEM", ["Theme", "Reboot", "Shutdown", "Update"]),
        ]

        for section_title, items in sections:
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    border: 1px solid #1a3a2a;
                    border-left: 2px solid #00ff88;
                    background-color: #0d1a0d;
                }
            """)
            section_layout = QVBoxLayout(frame)
            section_layout.setContentsMargins(0, 0, 0, 0)
            section_layout.setSpacing(0)

            # Section header
            header = QLabel(section_title)
            header.setStyleSheet("font-size: 10px; color: #608060; letter-spacing: 2px; padding: 8px 12px 4px 12px;")
            section_layout.addWidget(header)

            # Buttons
            for item in items:
                btn = QPushButton(f"  {item}")
                btn.setFixedHeight(40)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                        border-top: 1px solid #1a2a1a;
                        color: #00cc66;
                        text-align: left;
                        font-size: 12px;
                        font-family: monospace;
                        padding-left: 16px;
                    }
                    QPushButton:hover {
                        background-color: #00ff8815;
                    }
                """)
                section_layout.addWidget(btn)

            layout.addWidget(frame)

        layout.addStretch(1)

        return root
