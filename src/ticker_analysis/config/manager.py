"""
Configuration Manager for Ticker Analysis Tool.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List


class ConfigManager:
    """Manages configuration for the ticker analysis application."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_file: Path to the configuration file
        """
        if config_file is None:
            # Default to config.yml in the same directory
            config_file = Path(__file__).parent / "config.yml"
        
        self.config_file = Path(config_file)
        self._config = None
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._config = yaml.safe_load(f) or {}
            else:
                self._config = {}
        except Exception as e:
            print(f"Warning: Could not load config file {self.config_file}: {e}")
            self._config = {}
    
    def get_config(self) -> Dict[str, Any]:
        """Get the full configuration dictionary."""
        return self._config.copy()
    
    def get_cache_directory(self) -> str:
        """Get the cache directory path."""
        cache_config = self._config.get('cache', {})
        cache_dir = cache_config.get('directory', './cache_data')
        return os.path.expanduser(cache_dir)
    
    def is_cache_enabled(self, data_type: str = 'default') -> bool:
        """Check if caching is enabled for a specific data type."""
        cache_config = self._config.get('cache', {})
        return cache_config.get('enabled', True)
    
    def get_cache_ttl_hours(self, data_type: str = 'default') -> int:
        """Get cache TTL in hours for a specific data type."""
        cache_config = self._config.get('cache', {})
        return cache_config.get('ttl_hours', 24)
    
    def get_cache_config(self, data_type: str = 'default') -> Dict[str, Any]:
        """Get cache configuration for a specific data type."""
        cache_config = self._config.get('cache', {})
        return {
            'enabled': cache_config.get('enabled', True),
            'ttl_hours': cache_config.get('ttl_hours', 24),
            'directory': self.get_cache_directory()
        }
    
    def get_telegram_config(self) -> Dict[str, Any]:
        """Get Telegram notification configuration."""
        # Check both locations for backward compatibility
        notifications = self._config.get('notifications', {})
        telegram_from_notifications = notifications.get('telegram', {})
        telegram_from_root = self._config.get('telegram', {})
        
        # Prefer notifications.telegram, fallback to root telegram
        telegram = telegram_from_notifications if telegram_from_notifications else telegram_from_root
        
        return {
            'bot_token': telegram.get('bot_token', ''),
            'chat_id': telegram.get('chat_id', ''),
            'enabled': telegram.get('enabled', False)
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        logging_config = self._config.get('logging', {})
        return {
            'level': logging_config.get('level', 'INFO'),
            'format': logging_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            'file': logging_config.get('file', None)
        }
    
    def is_price_monitor_enabled(self) -> bool:
        """Check if price monitoring is enabled."""
        price_monitor = self._config.get('price_monitor', {})
        return price_monitor.get('enabled', False)
    
    def get_price_thresholds(self) -> List[str]:
        """Get list of price threshold strings."""
        price_monitor = self._config.get('price_monitor', {})
        return price_monitor.get('thresholds', [])
    
    def are_price_notifications_enabled(self) -> bool:
        """Check if price notifications are enabled."""
        price_monitor = self._config.get('price_monitor', {})
        notifications = price_monitor.get('notifications', {})
        return notifications.get('enabled', False)
    
    def get_price_notification_template(self) -> str:
        """Get the price notification message template."""
        price_monitor = self._config.get('price_monitor', {})
        notifications = price_monitor.get('notifications', {})
        return notifications.get('message_template',
                                '✅ Price Alert: {triggered_count} threshold(s) triggered\n\n{details}')


# Global config manager instance
_config_manager = None


def get_config_manager() -> ConfigManager:
    """Get the global configuration manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def set_config_manager(config_manager: ConfigManager) -> None:
    """Set the global configuration manager instance."""
    global _config_manager
    _config_manager = config_manager