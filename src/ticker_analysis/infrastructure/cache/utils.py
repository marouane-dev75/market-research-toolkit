"""
Cache Utilities Module

This module provides utility functions for cache operations and key generation.
"""

import hashlib
from typing import Optional, Any, Dict
from datetime import datetime


class CacheUtils:
    """Utility functions for cache operations."""
    
    @staticmethod
    def generate_cache_key(ticker: str, data_type: str, 
                          frequency: Optional[str] = None,
                          period: Optional[str] = None,
                          **kwargs) -> str:
        """
        Generate a unique cache key for the given parameters.
        
        Args:
            ticker: Stock ticker symbol
            data_type: Type of financial data
            frequency: Data frequency (annual/quarterly) - optional
            period: Time period for data - optional
            **kwargs: Additional parameters
            
        Returns:
            str: Unique cache key
        """
        # Create a string representation of all parameters
        params = {
            'ticker': ticker.upper(),
            'data_type': data_type.lower(),
            'frequency': frequency.lower() if frequency else 'none',
            'period': period.lower() if period else 'none',
            **kwargs
        }
        
        # Sort parameters for consistent key generation
        param_string = '|'.join(f"{k}:{v}" for k, v in sorted(params.items()))
        
        # Generate hash for uniqueness
        hash_obj = hashlib.md5(param_string.encode())
        param_hash = hash_obj.hexdigest()[:8]
        
        # Create readable cache key
        cache_key = f"{ticker.upper()}_{data_type}_{frequency or 'none'}_{period or 'none'}_{param_hash}"
        
        return cache_key
    
    @staticmethod
    def generate_simple_cache_key(ticker: str, data_type: str) -> str:
        """
        Generate a simple cache key for data types that don't need complex parameters.
        
        Args:
            ticker: Stock ticker symbol
            data_type: Type of financial data
            
        Returns:
            str: Simple cache key
        """
        return f"{ticker.upper()}_{data_type}"
    
    @staticmethod
    def is_valid_ticker(ticker: str) -> bool:
        """
        Validate ticker symbol format.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            bool: True if ticker format is valid
        """
        if not ticker or not isinstance(ticker, str):
            return False
        
        # Basic validation - ticker should be alphanumeric and reasonable length
        ticker = ticker.strip().upper()
        return (len(ticker) >= 1 and 
                len(ticker) <= 10 and 
                ticker.replace('.', '').replace('-', '').isalnum())
    
    @staticmethod
    def sanitize_ticker(ticker: str) -> str:
        """
        Sanitize ticker symbol for use in file names and cache keys.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            str: Sanitized ticker symbol
        """
        if not ticker:
            return ""
        
        # Convert to uppercase and remove invalid characters
        sanitized = ticker.upper().strip()
        # Replace common special characters with underscores
        sanitized = sanitized.replace('.', '_').replace('-', '_').replace('/', '_')
        
        return sanitized
    
    @staticmethod
    def format_cache_size(size_bytes: int) -> str:
        """
        Format cache size in human-readable format.
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            str: Formatted size string
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    @staticmethod
    def format_time_ago(timestamp: datetime) -> str:
        """
        Format timestamp as time ago string.
        
        Args:
            timestamp: Datetime object
            
        Returns:
            str: Human-readable time ago string
        """
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "Just now"
    
    @staticmethod
    def validate_cache_data(data: Any, data_type: str) -> bool:
        """
        Validate cached data structure based on data type.
        
        Args:
            data: Cached data to validate
            data_type: Type of financial data
            
        Returns:
            bool: True if data structure is valid
        """
        if data is None:
            return False
        
        # Basic validation based on data type
        if data_type == 'company_info':
            # Should be a single object with ticker attribute
            return hasattr(data, 'ticker')
        elif data_type in ['income_statements', 'balance_sheets', 'cash_flows']:
            # Should be a list of objects
            return isinstance(data, list) and len(data) > 0
        elif data_type == 'dividends':
            # Should be a list of dividend objects
            return isinstance(data, list)
        elif data_type == 'price_data':
            # Should be a list of price objects
            return isinstance(data, list) and len(data) > 0
        
        return True  # Default to valid for unknown types
    
    @staticmethod
    def get_cache_key_info(cache_key: str) -> Dict[str, str]:
        """
        Extract information from a cache key.
        
        Args:
            cache_key: Cache key to parse
            
        Returns:
            Dict containing parsed information
        """
        parts = cache_key.split('_')
        
        if len(parts) >= 2:
            return {
                'ticker': parts[0],
                'data_type': parts[1],
                'frequency': parts[2] if len(parts) > 2 and parts[2] != 'none' else None,
                'period': parts[3] if len(parts) > 3 and parts[3] != 'none' else None,
                'hash': parts[-1] if len(parts) > 4 else None
            }
        
        return {'ticker': '', 'data_type': '', 'frequency': None, 'period': None, 'hash': None}