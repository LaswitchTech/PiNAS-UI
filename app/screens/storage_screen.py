"""
Screen 2 — Storage / SMART (stub).

Placeholder for drive health monitoring, SMART data, and capacity
indicators. Will be implemented incrementally.
"""

from typing import Optional

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame


class StorageScreen:
    """Screen 2 — Storage/SMART dashboard (stub)."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        self._parent = parent

    def build_content(self) -> QWidget:
        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Title
        title = QLabel("STORAGE / SMART")
        title.setStyleSheet("font-size: 18px; font-weight: bold; letter-spacing: 2px; color: #00ff88;")
        layout.addWidget(title)

        # Stub content
        stub = QFrame()
        stub.setFixedHeight(200)
        stub.setStyleSheet("""
            QFrame {
                border: 1px dashed #333;
                border-left: 2px solid #00ff8840;
                background-color: #111111;
            }
        """)
        stub_layout = QVBoxLayout(stub)
        stub_layout.setContentsMargins(0, 0, 0, 0)

        msg = QLabel("DRIVE DATA COMING SOON")
        msg.setStyleSheet("font-size: 12px; color: #666; letter-spacing: 2px;")
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stub_layout.addWidget(msg)

        desc = QLabel("SMART health, temperature, and capacity data will appear here.")
        desc.setStyleSheet("font-size: 10px; color: #444;")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stub_layout.addWidget(desc)

        layout.addWidget(stub)
        layout.addStretch(1)

        return root
