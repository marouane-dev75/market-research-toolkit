"""Configuration module for ticker analysis."""

from .manager import get_config_manager, set_config_manager, ConfigManager

__all__ = [
    'get_config_manager',
    'set_config_manager', 
    'ConfigManager'
]