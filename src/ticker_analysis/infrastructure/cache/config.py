"""
Cache Configuration Module

This module provides cache configuration using the centralized config system.
"""

from typing import Dict, Any, List
from pathlib import Path
from ...config import get_config_manager


class CacheConfig:
    """Configuration settings for the cache system using centralized config."""
    
    @classmethod
    def get_cache_dir(cls) -> Path:
        """
        Get the cache directory path from src.ticker_analysis.config.
        
        Returns:
            Path: Cache directory path
        """
        try:
            config_manager = get_config_manager()
            cache_dir = config_manager.get_cache_directory()
            return Path(cache_dir)
        except Exception:
            # Fallback to default
            return Path("data")
    
    @classmethod
    def is_cache_enabled(cls, data_type: str) -> bool:
        """
        Check if caching is enabled for a data type.
        
        Args:
            data_type: Type of financial data
            
        Returns:
            bool: True if caching is enabled
        """
        try:
            config_manager = get_config_manager()
            return config_manager.is_cache_enabled(data_type)
        except Exception:
            # Fallback to enabled
            return True
    
    @classmethod
    def get_ttl_hours(cls, data_type: str) -> int:
        """
        Get TTL in hours for a data type.
        
        Args:
            data_type: Type of financial data
            
        Returns:
            int: TTL in hours
        """
        try:
            config_manager = get_config_manager()
            return config_manager.get_cache_ttl_hours(data_type)
        except Exception:
            # Fallback to 24 hours
            return 24
    
    @classmethod
    def get_all_data_types(cls) -> List[str]:
        """
        Get list of all supported data types from src.ticker_analysis.config.
        
        Returns:
            List of data type names
        """
        try:
            config_manager = get_config_manager()
            config = config_manager.get_config()
            return list(config.data.cache.keys())
        except Exception:
            # Fallback to default types
            return [
                'company_info',
                'income_statements',
                'balance_sheets',
                'cash_flows',
                'dividends',
                'price_data'
            ]
    
    @classmethod
    def get_cache_config(cls, data_type: str) -> Dict[str, Any]:
        """
        Get cache configuration for a specific data type.
        
        Args:
            data_type: Type of financial data
            
        Returns:
            Dict containing cache configuration
        """
        try:
            config_manager = get_config_manager()
            cache_config = config_manager.get_cache_config(data_type)
            return {
                'ttl_hours': cache_config.ttl_hours,
                'enabled': cache_config.enabled,
                'description': f'{data_type.replace("_", " ").title()} data'
            }
        except Exception:
            return {
                'ttl_hours': 24,
                'enabled': True,
                'description': 'Unknown data type'
            }
    
    @classmethod
    def get_cache_stats_summary(cls) -> Dict[str, Any]:
        """
        Get a summary of cache configuration.
        
        Returns:
            Dict containing cache configuration summary
        """
        try:
            config_manager = get_config_manager()
            config = config_manager.get_config()
            
            cache_configs = {}
            enabled_count = 0
            
            for data_type, cache_config in config.data.cache.items():
                cache_configs[data_type] = {
                    'ttl_hours': cache_config.ttl_hours,
                    'enabled': cache_config.enabled,
                    'description': f'{data_type.replace("_", " ").title()} data'
                }
                if cache_config.enabled:
                    enabled_count += 1
            
            return {
                'cache_directory': str(config_manager.get_cache_directory()),
                'total_data_types': len(cache_configs),
                'enabled_data_types': enabled_count,
                'data_types': cache_configs
            }
        except Exception:
            return {
                'cache_directory': 'data',
                'total_data_types': 0,
                'enabled_data_types': 0,
                'data_types': {}
            }

    # Cache directory structure - get from config
    @classmethod
    def get_cache_directories(cls) -> List[str]:
        """
        Get list of cache directories that should be created.
        
        Returns:
            List of directory names
        """
        return cls.get_all_data_types()
    
    # For backward compatibility
    CACHE_DIRECTORIES = property(lambda self: self.get_cache_directories())