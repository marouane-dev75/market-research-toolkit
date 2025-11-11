"""Ticker Analysis Tool - A comprehensive financial analysis application."""

# Main interface (imported last to avoid circular imports)
from .interfaces.cli import main

__all__ = [
    # Main interface
    "main"
]
