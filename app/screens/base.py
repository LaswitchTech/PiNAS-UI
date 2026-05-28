"""
BaseScreen abstract class — interface for all swipeable screen pages.

Each screen must implement `build_content()` to return a QWidget with
the screen's layout hierarchy.
"""

from abc import ABC, abstractmethod
from typing import Optional

from PyQt6.QtWidgets import QWidget


class BaseScreen(ABC):
    """Abstract base for all screen pages."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        self._parent = parent

    @abstractmethod
    def build_content(self) -> QWidget:
        """Return the root widget containing this screen's content."""
        ...

    def on_enter(self) -> None:
        """Called when this screen becomes active. Override for setup."""
        pass

    def on_exit(self) -> None:
        """Called when this screen is leaving. Override for cleanup."""
        pass
