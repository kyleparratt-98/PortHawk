"""
PortSentry - Real-time port monitoring tool.

This package provides a command-line tool for monitoring network port activity
in real-time with a live-updating, color-coded display.
"""

__version__ = "1.0.0"
__author__ = "PortSentry Team"
__description__ = "Real-time port monitoring tool"

# Import key classes for easier access
from port_sentry.monitor import PortMonitor, ConnectionInfo
from port_sentry.ui import ConsoleUI
from port_sentry.cli import CLI

# Define public API
__all__ = [
    "__version__",
    "__author__",
    "__description__",
    "PortMonitor",
    "ConnectionInfo",
    "ConsoleUI",
    "CLI",
]
