"""CLI interface module."""

# Import main CLI manager
from .manager import CLIManager, create_cli, main

# Import command pattern components
from .command_pattern import CommandRegistry, CommandInvoker

__all__ = [
    'CLIManager',
    'create_cli',
    'main',
    'CommandRegistry',
    'CommandInvoker'
]